"""Read server records, apply a post-hoc non-score selection rule, save provenance."""
import json, subprocess, hashlib, math
from pathlib import Path
from datetime import datetime, timezone
REMOTE = r'''
from pathlib import Path
import json,hashlib
root=Path('/data/amax/coevoskills-repro/src/coevoskills/runs')
items=[]
for p in sorted(root.glob('*rep02*/*summary*.json')):
 try:d=json.loads(p.read_text())
 except (ValueError,OSError):continue
 rows=d.get('per_task',[])
 if isinstance(rows,dict):rows=list(rows.values())
 for row in rows:
  if not isinstance(row,dict) or row.get('complete') is not True:continue
  if not all(k in row for k in ['task','baseline_reward','evolved_reward','trial_dirs','evaluated_at_unix']):continue
  item={'summary_path':str(p),'summary_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'row':row,'trials':{},'validation_errors':[]}
  for side in ['baseline','evolved']:
   try:
    rp=Path(row['trial_dirs'][side])/'result.json'; raw=rp.read_bytes(); result=json.loads(raw)
    reward=result.get('verifier_result',{}).get('rewards',{}).get('reward')
    item['trials'][side]={'result_path':str(rp),'result_sha256':hashlib.sha256(raw).hexdigest(),'task':result.get('task_name'),'reward':reward,'finished_at':result.get('finished_at'),'exception_info':result.get('exception_info')}
    if result.get('task_name')!=row['task']:item['validation_errors'].append(side+': task mismatch')
    if reward!=row[side+'_reward']:item['validation_errors'].append(side+': reward mismatch')
    if not result.get('finished_at'):item['validation_errors'].append(side+': unfinished')
    if result.get('exception_info'):item['validation_errors'].append(side+': exception')
   except Exception as e:item['validation_errors'].append(side+': '+str(e))
  items.append(item)
print(json.dumps(items))
'''
def main():
 out=Path(__file__).resolve().parent
 response=subprocess.run(['ssh','-o','BatchMode=yes','amax@219.223.251.70','python3 -'],input=REMOTE,text=True,capture_output=True,check=True)
 candidates=json.loads(response.stdout)
 groups={}
 for x in candidates:
  row=x['row']
  if not all(isinstance(row[k],(int,float)) and math.isfinite(row[k]) for k in ['baseline_reward','evolved_reward','evaluated_at_unix']):x['validation_errors'].append('non-finite numeric field')
  if x['validation_errors']:continue
  groups.setdefault(row['task'],[]).append(x)
 selected=[]
 for task,items in sorted(groups.items()):
  chosen=max(items,key=lambda x:(x['row']['evaluated_at_unix'],x['summary_path']))
  selected.append({**chosen,'selection_reason':'Latest evaluated_at_unix among complete pairs with matching finished exception-free raw results; summary path lexical order breaks timestamp ties.','candidate_count':len(items)})
 n=len(selected)
 b=sum(x['row']['baseline_reward'] for x in selected)/n
 e=sum(x['row']['evolved_reward'] for x in selected)/n
 ds=[x['row']['evolved_reward']-x['row']['baseline_reward'] for x in selected]
 report={'created_utc':datetime.now(timezone.utc).isoformat(),'experiment':'CoEvoSkills server-native rep02','selection_status':'post_hoc_user_authorized_resolution','authorization':'User delegated choice among duplicate records on 2026-09-21. This rule was adopted after earlier scores were visible; it is not a preregistered rule or a newly run experiment.','rule':'Latest evaluated_at_unix among complete pairs whose raw baseline/evolved result files match the task and scores, have finished timestamps, and have no exception. Preserve whole pairs. Tie-break: lexicographically greatest summary path. Apply to every task, without using reward as a selection criterion.','task_count':n,'baseline_mean_reward':b,'evolved_mean_reward':e,'mean_reward_delta':sum(ds)/n,'improved':sum(d>0 for d in ds),'degraded':sum(d<0 for d in ds),'unchanged':sum(d==0 for d in ds),'candidate_rows':len(candidates),'rejected_candidate_rows':sum(bool(x['validation_errors']) for x in candidates),'tasks':selected}
 (out/'candidates.json').write_text(json.dumps(candidates,ensure_ascii=False,indent=2)+'\n')
 (out/'selection-manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 (out/'selected-scores.tsv').write_text('task\tbaseline_reward\tevolved_reward\tdelta\tsummary_path\n'+''.join(f"{x['row']['task']}\t{x['row']['baseline_reward']}\t{x['row']['evolved_reward']}\t{x['row']['evolved_reward']-x['row']['baseline_reward']}\t{x['summary_path']}\n" for x in selected))
 print(json.dumps({k:v for k,v in report.items() if k!='tasks'},indent=2))
 for x in selected:
  if x['row']['task'] in ['earthquake-phase-association','gravitational-wave-detection','lean4-proof','offer-letter-generator']:print(x['row']['task'],x['row']['baseline_reward'],x['row']['evolved_reward'],x['summary_path'])
 print('REJECTIONS',[(x['row']['task'],x['validation_errors']) for x in candidates if x['validation_errors']])
 assert n==85,f'Expected 85 tasks, found {n}'
if __name__=='__main__':main()
