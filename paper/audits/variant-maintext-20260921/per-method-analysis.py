"""Rebuild method-specific historical variant pairs; optional read-only SSH verification."""
from pathlib import Path
import argparse, collections, hashlib, json, subprocess
R = Path(__file__).resolve().parent
ROOT = R.parents[2]
EXP = ROOT / 'experiments/skillsbench-transfer/dev-v0.7'
METHODS = ['skillevolver', 'spark', 'coevoskills']
STATUSES = {'valid', 'valid_budget_exhaustion', 'scientific_failure', 'passed'}
parser = argparse.ArgumentParser()
parser.add_argument('--verify-server', action='store_true')
args = parser.parse_args()
invpath = R / 'formal-attempt-inventory-main-r33-20260920.json'
ledgerpath = EXP / 'reviewed-recovery-coverage-20260920-r1.json'
inv = json.loads(invpath.read_text())
ledger = json.loads(ledgerpath.read_text())
identities = {(x['variant_id'], x['condition']) for x in ledger['historical_pairs']}
assert len(identities) == 838
candidates = collections.defaultdict(list)
def add(x, variant=None, condition=None):
    key = x.get('variant_id', variant), x.get('condition', condition)
    if key in identities and x.get('status') in STATUSES and isinstance(x.get('reward'), (int, float)):
        candidates[key].append({**x, 'variant_id': key[0], 'condition': key[1]})
for row in inv['rows']:
    for x in filter(None, [row['parent']] + row['sidecars']):
        add({**x, 'manifest': row['manifest']}, row['variant_id'], row['condition'])
for x in inv['indexed_results'] + inv['audited_reevaluation_results']:
    add(x)
assert set(candidates) == identities
conflicts = {k: xs for k, xs in candidates.items() if len({x['reward'] for x in xs}) > 1}
selected = {k: min(xs, key=lambda x: (x['status'] != 'valid', x['path']))
            for k, xs in candidates.items() if k not in conflicts}
oldrecords = json.loads((R / 'selected-historical-records.json').read_text())
oldvariants = {x['variant_id'] for x in oldrecords}
assert len(oldvariants) == 198
for x in oldrecords:
    assert selected[x['variant_id'], x['condition']]['path'] == x['path']
    assert selected[x['variant_id'], x['condition']]['reward'] == x['reward']
cohorts = {m: sorted(v for v, c in selected if c == m and (v, 'no_skill') in selected) for m in METHODS}
needed = {(v, c) for m, vs in cohorts.items() for v in vs for c in ['no_skill', m]}
provenance = {(x['variant_id'], x['condition']): x for x in json.loads((R / 'score-provenance.json').read_text())}
additional = [selected[k] for k in sorted(needed) if k not in provenance]
if args.verify_server:
    remote = '''import json, hashlib
from pathlib import Path
out=[]
for x in PAYLOAD:
 p=Path(x['path']); raw=p.read_bytes(); data=json.loads(raw)
 assert data['reward']==x['reward'], str(p)
 assert data.get('status')==x['status'], str(p)
 out.append({**x,'sha256':hashlib.sha256(raw).hexdigest(),'reward_verified':True,'status_verified':True})
print(json.dumps(out))
'''.replace('PAYLOAD', repr(additional))
    result = subprocess.run(['ssh','-o','BatchMode=yes','amax@219.223.251.70','python3 -'], input=remote, text=True, capture_output=True, check=True)
    (R / 'per-method-additional-provenance.json').write_text(json.dumps(json.loads(result.stdout), indent=2)+'\n')
extra = json.loads((R / 'per-method-additional-provenance.json').read_text())
assert {(x['variant_id'],x['condition']) for x in extra} == {(x['variant_id'],x['condition']) for x in additional}
provenance.update({(x['variant_id'],x['condition']):x for x in extra})
def stats(vs, m):
    baseline = [selected[v,'no_skill']['reward'] for v in vs]
    skill = [selected[v,m]['reward'] for v in vs]
    ds = [s-b for b,s in zip(baseline,skill)]
    return {'n':len(vs), 'families':len({v.split('--')[0] for v in vs}),
            'baseline_mean':sum(baseline)/len(vs), 'skill_mean':sum(skill)/len(vs), 'delta':sum(ds)/len(vs),
            'improved':sum(d>0 for d in ds),'regressed':sum(d<0 for d in ds),'tied':sum(d==0 for d in ds)}
report = {'scale':'reward 0–1; multiply means and delta by 100 for manuscript',
          'selection':'For each method independently require unambiguous historical rewards for that method and no_skill on the same variant. Exclude only identities with conflicting eligible rewards. Prefer literal-valid status then lexicographic path among agreeing observations.',
          'protocol':'Use only the 838 historical identities pinned by the r1 ledger and inherited unchanged by final r5. Do not pool the 48 separately reported recoveries or three subsequent file-reading checks.',
          'source_files':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [ledgerpath,invpath]],
          'conflicts':[{'variant_id':v,'condition':c,'rewards':sorted({x['reward'] for x in xs}),'paths':sorted({x['path'] for x in xs})} for (v,c),xs in sorted(conflicts.items())],
          'methods':{}, 'additional_unique_results_verified':len(extra)}
paired=[]
for m,vs in cohorts.items():
    report['methods'][m]={'overall':stats(vs,m),
       'paradigms':{p:stats([v for v in vs if '--'+p+'--' in v],m) for p in ['p1','p2','p3']},
       'added_vs_prior_common_198':sorted(set(vs)-oldvariants),
       'removed_vs_prior_common_198':sorted(oldvariants-set(vs))}
    for v in vs:
        pair={'method':m,'variant_id':v,'paradigm':v.split('--')[1], 'new_vs_prior_common_198':v not in oldvariants}
        for c,name in [('no_skill','baseline'),(m,'skill')]:
            x=selected[v,c];e=provenance[v,c]
            assert x['path']==e['path'] and x['reward']==e['reward']
            pair[name]={'reward':x['reward'],'status':x['status'],'path':x['path'],'sha256':e['sha256']}
        pair['delta']=pair['skill']['reward']-pair['baseline']['reward'];paired.append(pair)
(R / 'per-method-statistics.json').write_text(json.dumps(report,indent=2)+'\n')
(R / 'per-method-paired-scores.json').write_text(json.dumps(paired,indent=2)+'\n')
print(json.dumps({m:v['overall'] for m,v in report['methods'].items()},indent=2))
print('Additional source files read and hashed:',len(extra))
