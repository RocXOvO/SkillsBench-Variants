from pathlib import Path
import json,subprocess
root=Path(__file__).resolve().parent
selected=json.loads((root/'selected-historical-records.json').read_text())
inv=json.loads((root/'formal-attempt-inventory-main-r33-20260920.json').read_text())
variants={x['variant_id'] for x in selected}
paths=sorted({x['manifest'] for x in inv['rows'] if x['variant_id'] in variants})
payload={'selected':selected,'manifests':paths}
remote='''import json,hashlib\nfrom pathlib import Path\npayload=json.loads(PAYLOAD)\nout={'results':[],'manifests':[]}\nfor x in payload['selected']:\n p=Path(x['path']);raw=p.read_bytes();d=json.loads(raw); reward=d.get('reward');out['results'].append({'variant_id':x['variant_id'],'condition':x['condition'],'path':str(p),'sha256':hashlib.sha256(raw).hexdigest(),'reward':reward,'status':d.get('status'),'reward_matches':reward==x['reward']})\nfor path in payload['manifests']:\n p=Path(path)\n if not p.exists():out['manifests'].append({'path':path,'missing':True});continue\n raw=p.read_bytes();d=json.loads(raw)\n cells=[]\n for c in d.get('cells',[]):\n  cells.append({k:c.get(k) for k in ['variant_id','condition','coverage_status','skill_path','skill_files','source','public_path','agent_timeout_sec','verifier_timeout_sec','protocol_id','release_manifest_sha256']})\n out['manifests'].append({'path':path,'sha256':hashlib.sha256(raw).hexdigest(),'metadata':{k:v for k,v in d.items() if not isinstance(v,(list,dict))},'cells':cells})\nprint(json.dumps(out))\n'''.replace('PAYLOAD',repr(json.dumps(payload)))
r=subprocess.run(['ssh','-o','BatchMode=yes','amax@219.223.251.70','python3 -'],input=remote,text=True,capture_output=True,check=True)
data=json.loads(r.stdout);(root/'server-evidence.json').write_text(json.dumps(data,indent=2)+'\n')
print('results',len(data['results']),'mismatches',[x for x in data['results'] if not x['reward_matches']],'manifests',len(data['manifests']))
