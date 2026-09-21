"""Recompute the six selected runs and align each method's task sets."""
from pathlib import Path
import hashlib, json, math
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
sources=[]
def read(path):
 p=ROOT/path;raw=p.read_bytes();sources.append({'path':path,'sha256':hashlib.sha256(raw).hexdigest()});return json.loads(raw)
def stats(method,run,rows,origin):
 rows=sorted(rows,key=lambda x:x['task']);assert len({x['task'] for x in rows})==len(rows)
 n=len(rows);ds=[x['evolved_reward']-x['baseline_reward'] for x in rows]
 return {'method':method,'run':run,'origin':origin,'n':n,'baseline':math.fsum(x['baseline_reward'] for x in rows)/n,'skill':math.fsum(x['evolved_reward'] for x in rows)/n,'delta':math.fsum(ds)/n,'improved':sum(x>0 for x in ds),'regressed':sum(x<0 for x in ds),'tied':sum(x==0 for x in ds),'tasks':rows}
def simple(rows):return [{k:r[k] for k in ['task','baseline_reward','evolved_reward']} for r in rows]
e='paper/maintext-20260921/evidence/'
a=read(e+'skillevolver-first81.json')
p='experiments/skillevolver-skillsbench/runs/skillevolver-codex-subscription-gpt55-medium-paper81-fresh-paired76-final.json'
b=read(p);assert sources[-1]['sha256']==a['original_76']['sha256']
r1=simple(b['tasks'])+simple(a['existing_recoveries'])
b=read(e+'skillevolver-repeat2-81.json');r2=simple(b['tasks'])
assert {x['task'] for x in r1}=={x['task'] for x in r2}
runs=[stats('SkillEvolver',1,r1,'Local execution, transferred to server; ChatGPT subscription'),stats('SkillEvolver',2,r2,'Local execution, transferred to server; ChatGPT subscription')]
for i in [1,2]:
 d=read(e+f'spark-server-runs-r2/rep0{i}-summary.json')
 rows=[{'task':r['task'],'baseline_reward':r['baseline_reward'],'evolved_reward':r['generated_reward']} for r in d['per_task_delta'].values()]
 assert all(r['valid_pair'] for r in d['per_task_delta'].values())
 run=stats('SPARK',i,rows,'Server-native; OpenLux API')
 run['skill_generation_coverage']=d['skill_generation_coverage'];runs.append(run)
assert {x['task'] for x in runs[2]['tasks']}=={x['task'] for x in runs[3]['tasks']}
u=read('experiments/coevoskills-skillsbench/reports/union87-minus-google-auth-final-r71.json')
a=read('experiments/coevoskills-skillsbench/reports/finalized85-zero-start-paired-final-r66.json');assert sources[-1]['sha256']==u['sources'][0]['sha256']
extra=read('experiments/coevoskills-skillsbench/'+u['sources'][1]['path']);assert sources[-1]['sha256']==u['sources'][1]['sha256']
local=dict(a['per_task']);local['mhc-layer-impl']={'task':'mhc-layer-impl','baseline_reward':u['sources'][1]['baseline_reward'],'evolved_reward':u['sources'][1]['evolved_reward']}
s=read('paper/audits/coevo-server-selection-20260921/selection-manifest.json');server={x['row']['task']:x['row'] for x in s['tasks']}
common=sorted(set(local)&set(server));assert len(common)==85
assert set(local)-set(server)=={'mhc-layer-impl'} and not set(server)-set(local)
checks=[]
for t in common:
 sel=a['selections'][t];p=Path(sel['result_path']);raw=p.read_bytes();d=json.loads(raw)
 assert hashlib.sha256(raw).hexdigest()==sel['result_sha256'],t
 assert d['baseline_reward']==local[t]['baseline_reward'] and d['evolved_reward']==local[t]['evolved_reward'],t
 checks.append({'task':t,**{k:sel[k] for k in ['source','result_path','result_sha256']}})
runs.extend([stats('CoEvoSkills',1,simple([local[t] for t in common]),'Local execution, transferred to server; ChatGPT subscription'),stats('CoEvoSkills',2,simple([server[t] for t in common]),'Server-native; OpenLux API')])
for r in runs:assert r['improved']+r['regressed']+r['tied']==r['n']
result={'sources':sources,'coevo_alignment':{'rule':'Task-name intersection of the two selected runs, independent of reward.','common_tasks':common,'removed_from_local':[local['mhc-layer-impl']],'removed_from_server':[],'local_selected_result_checks':checks,'server_selection_manifest':'paper/audits/coevo-server-selection-20260921/selection-manifest.json'},'runs':runs}
(OUT/'six-runs.json').write_text(json.dumps(result,indent=2)+'\n')
(OUT/'paired-scores.tsv').write_text('method\trun\ttask\tbaseline\tskill\tdelta\n'+''.join(f"{r['method']}\t{r['run']}\t{x['task']}\t{x['baseline_reward']}\t{x['evolved_reward']}\t{x['evolved_reward']-x['baseline_reward']}\n" for r in runs for x in r['tasks']))
lines=[]
for i,r in enumerate(runs):
 if i and i%2==0:lines.append(r'\midrule')
 lines.append(f"{r['method']} & {r['run']} & {r['n']} & {100*r['baseline']:.2f} & {100*r['skill']:.2f} & $+{100*r['delta']:.2f}$ & {r['improved']} & {r['regressed']} & {r['tied']} "+r'\\')
(OUT/'table-rows.tex').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
