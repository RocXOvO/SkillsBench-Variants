"""Verify a Docker save archive without loading images or running containers."""
import hashlib
import gzip
import io
import json
import re
import sys
import tarfile
import time
import subprocess
from pathlib import Path, PurePosixPath

archive=Path(sys.argv[1]);selection=Path(sys.argv[2]);report=Path(sys.argv[3])
expected=set(json.loads(selection.read_text())['image_ids'])
fixture_evidence=json.loads(Path(sys.argv[4]).read_text())
assert fixture_evidence['all_verified']
accepted_files={(v['blob_sha256'],v['layer_path'],v['file_sha256']):v for v in fixture_evidence['files']}
accepted_public_files=[]
secret=re.compile(rb'(?<![A-Za-z0-9_/-])(?:hf_[A-Za-z0-9]{30,}|gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{35,})(?![A-Za-z0-9_-])|-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----\r?\n[A-Za-z0-9+/=\r\n]{120,}-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----')
public_fixtures=[]
bad=[];configs={};manifests=[];layer_hashes=set();blob_hashes=set();blob_objects={};blob_sizes={};layer_by_blob={};uncompressed_layer_bytes={};members=0;layer_files=0;seen=set();last_progress=time.monotonic()

def progress():
    global last_progress
    now=time.monotonic()
    if now-last_progress>=30:
        print(json.dumps({'stage':'image_archive_scan','members':members,'layer_files':layer_files,'image_configs':len(configs),'layer_digests':len(layer_hashes)}),flush=True)
        last_progress=now

class DigestReader:
    def __init__(self,stream):self.stream=stream;self.digest=hashlib.sha256();self.size=0
    def read(self,n=-1):
        data=self.stream.read(n);self.digest.update(data);self.size+=len(data);return data

class Prefixed:
    def __init__(self,prefix,stream):self.prefix=prefix;self.stream=stream
    def read(self,n=-1):
        if n<0:
            data=self.prefix+self.stream.read();self.prefix=b'';return data
        data=self.prefix[:n];self.prefix=self.prefix[n:]
        return data+self.stream.read(n-len(data))

def credential_path(name):
    s='/'+name.lstrip('./')
    return any(x in s for x in ('/.codex/auth.json','/provider.env','/credentials.json','/.ssh/id_rsa','/.ssh/id_ed25519','/.aws/credentials','/.cache/huggingface/token','/.huggingface/token','/.netrc','/application_default_credentials.json'))

def scan_layer(member_name,stream,prefix):
    global layer_files
    with tarfile.open(fileobj=Prefixed(prefix,stream),mode='r|') as layer:
        for f in layer:
            if credential_path(f.name):bad.append({'member':member_name,'layer_path':f.name,'reason':'credential filename'})
            if not f.isfile():continue
            layer_files+=1
            if layer_files%1000==0:progress()
            if f.size<=1024*1024:
                data=layer.extractfile(f).read()
                if b'\0' not in data:
                    for match in secret.finditer(data.replace(b'\\n', b'\n')):
                        file_key=(member_name.rsplit('/',1)[-1],f.name,hashlib.sha256(data).hexdigest())
                        if file_key in accepted_files:
                            evidence=accepted_files[file_key]
                            accepted_public_files.append({'member':member_name,'layer_path':f.name,'file_sha256':file_key[2], 'classification':evidence['classification'], 'primary_source':evidence['primary_source']})
                            continue
                        token_sha = hashlib.sha256(match.group()).hexdigest()
                        if (f.name.endswith('/transformers/testing_utils.py')
                            and token_sha == '5de261506c0ff857b7c1af7059f842fb0a36d1ca2e4895da542c5eb726f2c802'
                            and b'https://hub-ci.huggingface.co' in data
                            and b'__DUMMY_TRANSFORMERS_USER__' in data
                            and b'only usable on the sandboxed CI instance' in data):
                            public_fixtures.append({'member': member_name, 'layer_path': f.name,
                                'file_sha256': hashlib.sha256(data).hexdigest(),
                                'token_sha256': token_sha,
                                'classification': 'upstream public sandbox CI fixture',
                                'primary_source': 'https://github.com/huggingface/transformers/blob/main/src/transformers/testing_utils.py'})
                        else:
                            bad.append({'member':member_name,'layer_path':f.name,'reason':'credential pattern'})
    for block in iter(lambda:stream.read(4*1024*1024),b''):pass
    layer_hashes.add('sha256:'+stream.digest.hexdigest())
    uncompressed_layer_bytes['sha256:'+stream.digest.hexdigest()]=stream.size
    return 'sha256:'+stream.digest.hexdigest()

decompress = None
if archive.suffix == '.zst':
    decompress = subprocess.Popen(['zstd','--long=31','--decompress','--stdout',str(archive)],stdout=subprocess.PIPE)
    context = tarfile.open(fileobj=decompress.stdout,mode='r|')
else:
    context = tarfile.open(archive,'r|gz')
with context as outer:
    for m in outer:
        members+=1
        assert not m.name.startswith('/') and '..' not in PurePosixPath(m.name).parts,m.name
        assert m.name not in seen,m.name
        seen.add(m.name)
        if not m.isfile():continue
        stream=DigestReader(outer.extractfile(m));prefix=stream.read(512)
        layer_diff=None
        if prefix.startswith(b'\x1f\x8b'):
            with gzip.GzipFile(fileobj=Prefixed(prefix,stream),mode='rb') as gz:
                inflated=DigestReader(gz)
                layer_diff=scan_layer(m.name,inflated,inflated.read(512))
            for block in iter(lambda:stream.read(4*1024*1024),b''):pass
        elif m.name.endswith('/layer.tar') or (len(prefix)>262 and prefix[257:262]==b'ustar') or (m.size>=1024 and prefix==b'\0'*512):
            layer_diff=scan_layer(m.name,stream,prefix)
        else:
            if m.size<=4*1024*1024:
                data=prefix+stream.read()
                if secret.search(data.replace(b'\\n',b'\n')):bad.append({'member':m.name,'reason':'credential pattern'})
                if data[:1] in (b'{',b'['):
                    try:d=json.loads(data)
                    except (ValueError,UnicodeError):d=None
                    if isinstance(d,dict) and 'rootfs' in d and 'config' in d:
                        image_id='sha256:'+hashlib.sha256(data).hexdigest()
                        configs[image_id]=d
                        for env in d.get('config', {}).get('Env', []):
                            key, _, value = env.partition('=')
                            if re.search(r'(?:API_KEY|TOKEN|SECRET|PASSWORD|PRIVATE_KEY)$',key,re.I) and value:
                                bad.append({'member':m.name,'reason':'credential environment field','key':key})
                    if m.name.startswith('blobs/sha256/') and isinstance(d,dict):
                        blob_objects['sha256:'+m.name.rsplit('/',1)[-1]]=d
                    if m.name=='manifest.json':manifests=d
            else:
                for block in iter(lambda:stream.read(4*1024*1024),b''):pass
        assert stream.size==m.size,(m.name,stream.size,m.size)
        if m.name.startswith('blobs/sha256/'):
            assert stream.digest.hexdigest()==m.name.rsplit('/',1)[-1],{'blob_digest_mismatch':m.name}
            blob_hashes.add('sha256:'+stream.digest.hexdigest())
            blob_sizes['sha256:'+stream.digest.hexdigest()]=m.size
            if layer_diff:layer_by_blob['sha256:'+stream.digest.hexdigest()]=layer_diff
        progress()

if decompress is not None:
    for block in iter(lambda:decompress.stdout.read(4*1024*1024),b''):pass
    assert decompress.wait()==0,'outer zstd stream validation failed'

def available_amd64_configs(image):
    obj=blob_objects.get(image,configs.get(image))
    assert obj is not None,{'missing_image_descriptor':image}
    if 'rootfs' in obj and 'config' in obj:return [image]
    if 'manifests' in obj:
        result=[]
        for desc in obj['manifests']:
            platform=desc.get('platform',{})
            if platform.get('os')!='linux' or platform.get('architecture')!='amd64':continue
            h=desc['digest'];assert h in blob_hashes,{'missing_amd64_manifest':h,'image':image}
            assert blob_sizes[h]==desc['size']
            result+=available_amd64_configs(h)
        assert result,{'no_linux_amd64_config':image}
        return result
    assert 'config' in obj and 'layers' in obj,{'unknown_manifest':image}
    cfg=obj['config'];h=cfg['digest'];assert h in configs and blob_sizes[h]==cfg['size']
    ordered=[]
    for desc in obj['layers']:
        digest=desc['digest'];assert digest in layer_by_blob and blob_sizes[digest]==desc['size']
        ordered.append(layer_by_blob[digest])
    assert ordered==configs[h]['rootfs']['diff_ids'],{'ordered_layer_diffs_mismatch':image}
    return [h]

image_configs={i:available_amd64_configs(i) for i in sorted(expected)}
for i,ids in image_configs.items():
    for cfg in ids:
        diffs=set(configs[cfg].get('rootfs',{}).get('diff_ids',[]))
        assert diffs<=layer_hashes,{'image':i,'unverified_layer_diff_ids':sorted(diffs-layer_hashes)}
Path(str(report)+'.graph-check.json').write_text(json.dumps({'expected_images':len(expected),'verified_original_image_ids':sorted(expected),'original_image_to_linux_amd64_config':image_configs, 'archive_members':members,'verified_blob_digests':len(blob_hashes),'verified_layer_digests':len(layer_hashes),'layer_files_scanned':layer_files,'uncompressed_unique_layer_bytes':sum(uncompressed_layer_bytes.values()),'unresolved_credential_findings':bad,'public_fixture_matches':accepted_public_files+public_fixtures},indent=2)+'\n')
assert not bad,{'rejected_credential_members':bad}
h=hashlib.sha256();parts=[];part_size=128*1024*1024
with archive.open('rb') as f:
    while True:
        ph=hashlib.sha256();size=0
        while size<part_size:
            block=f.read(min(8*1024*1024,part_size-size))
            if not block:break
            h.update(block);ph.update(block);size+=len(block)
        if not size:break
        index=len(parts)+1;name=archive.name+'.chunk-'+str(index).zfill(3)
        parts.append({'name':name,'bytes':size,'sha256':ph.hexdigest(),'part':index,'url':'https://github.com/RocXOvO/SkillsBench-Variants/releases/download/deployment-supplement-20261012/'+name})
result={'status':'VERIFIED','archive':archive.name,'bytes':archive.stat().st_size,'sha256':h.hexdigest(),
        'expected_images':len(expected),'verified_original_image_ids':sorted(expected),'original_image_to_linux_amd64_config':image_configs,
        'parts':parts,'uncompressed_unique_layer_bytes':sum(uncompressed_layer_bytes.values()),'archive_members':members,'verified_blob_digests':len(blob_hashes),'verified_layer_digests':len(layer_hashes),'layer_files_scanned':layer_files,
        'credential_filename_or_pattern_matches':bad,'public_sandbox_ci_fixture_matches':public_fixtures,'documented_public_image_fixture_matches':accepted_public_files,'credential_scan_pattern_version':6,'new_image_loads':0,'new_builds':0,'new_containers':0}
report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('verified_original_image_ids','original_image_to_linux_amd64_config','parts')}),flush=True)
