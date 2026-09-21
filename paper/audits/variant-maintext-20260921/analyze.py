from pathlib import Path
import json,collections,hashlib
import numpy as np
R=Path(__file__).resolve().parent
records=json.loads((R/'selected-historical-records.json').read_text())
evidence=json.loads((R/'server-evidence.json').read_text())
cs=['no_skill','skillevolver','spark','coevoskills'];rows={(x['variant_id'],x['condition']):x for x in records}
vs=sorted({v for v,c in rows});cells=collections.defaultdict(list)
for m in evidence['manifests']:
 for c in m.get('cells',[]):cells[c['variant_id'],c['condition']].append({**c,'manifest_path':m['path'],'manifest_sha256':m['sha256']})
assert len(vs)==198
for v in vs:
 for c in cs[1:]:assert len({x['coverage_status'] for x in cells[v,c]})==1
available=[v for v in vs if all(cells[v,c][0]['coverage_status']=='available' for c in cs[1:])]
assert len(available)==103
raw={(x['variant_id'],x['condition']):x for x in evidence['results']}
for x in raw.values():assert x['reward_matches']
def calc(variants):
 a=np.array([[rows[v,c]['reward'] for c in cs] for v in variants]);out={'n':len(variants),'families':len({v.split('--')[0] for v in variants}),'conditions':{}}
 for j,c in enumerate(cs):
  ds=a[:,j]-a[:,0];out['conditions'][c]={'mean':float(a[:,j].mean()),'delta':float(ds.mean()),'improved':int((ds>0).sum()),'regressed':int((ds<0).sum()),'tied':int((ds==0).sum())}
 families=sorted({v.split('--')[0] for v in variants});sums=np.array([a[[v.split('--')[0]==f for v in variants]].sum(axis=0) for f in families]);counts=np.array([sum(v.split('--')[0]==f for v in variants) for f in families]);rng=np.random.default_rng(20260921);indices=rng.integers(0,len(families),size=(20000,len(families)));means=sums[indices].sum(axis=1)/counts[indices].sum(axis=1)[:,None]
 out['evolver_comparisons']={}
 for j,c in [(2,'spark'),(3,'coevoskills')]:
  diff=means[:,1]-means[:,j];out['evolver_comparisons'][c]={'difference':float((a[:,1]-a[:,j]).mean()),'family_bootstrap_95_ci':np.quantile(diff,[.025,.975]).tolist(),'wins':int((a[:,1]>a[:,j]).sum()),'losses':int((a[:,1]<a[:,j]).sum()),'ties':int((a[:,1]==a[:,j]).sum())}
 return out
stats={'historical_complete_cohort':calc(vs),'all_artifacts_available_cohort':calc(available),'paradigms':{p:calc([v for v in vs if '--'+p+'--' in v]) for p in ['p1','p2','p3']},'bootstrap':{'unit':'base-task family','draws':20000,'seed':20260921,'interval':'percentile 95%; all variants of each sampled family retained'},'strict_literal_valid_sensitivity':calc([v for v in vs if all(rows[v,c]['status']=='valid' for c in cs)])}
(R/'statistics.json').write_text(json.dumps(stats,indent=2)+'\n')
ledger=[]
for v in vs:
 for c in cs:
  x=raw[v,c];m=min(cells[v,c],key=lambda x:x['manifest_path']);ledger.append({**x,'paradigm':v.split('--')[1],'all_artifacts_available':v in available,'coverage_status':m['coverage_status'],'skill_path':m['skill_path'],'skill_files':m['skill_files'],'manifest_path':m['manifest_path'],'manifest_sha256':m['manifest_sha256']})
(R/'score-provenance.json').write_text(json.dumps(ledger,indent=2)+'\n')
(R/'paired-scores.tsv').write_text('variant\tall_artifacts_available\tno_skill\tskillevolver\tspark\tcoevoskills\n'+''.join(v+'\t'+str(v in available)+'\t'+'\t'.join(str(rows[v,c]['reward']) for c in cs)+'\n' for v in vs))
print(json.dumps(stats,indent=2))
