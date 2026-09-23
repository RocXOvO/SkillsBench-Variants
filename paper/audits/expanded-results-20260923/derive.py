import csv,json,hashlib
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[3]; A=Path(__file__).parent
vp=R/'paper/audits/full-variant-records-20260922/paired-scores.json'; sp=R/'paper/audits/six-run-maintext-20260921/paired-scores.tsv'
v=json.loads(vp.read_text()); s=list(csv.DictReader(sp.open(),delimiter='\t'))
def sign(x): return 1 if x>1e-9 else -1 if x<-1e-9 else 0
def stats(p):
 b=[x[0] for x in p];d=[y-x for x,y in p]; n=len(p)
 return dict(n=n,baseline=100*sum(b)/n,skill=100*sum(y for x,y in p)/n,delta=100*sum(d)/n,improved=sum(sign(x)==1 for x in d),regressed=sum(sign(x)==-1 for x in d),tied=sum(sign(x)==0 for x in d),gain_mass=100*sum(max(x,0) for x in d)/n,loss_mass=100*sum(max(-x,0) for x in d)/n,baseline_zero=sum(x==0 for x,y in p),zero_to_positive=sum(x==0 and y>0 for x,y in p),zero_to_full=sum(x==0 and y==1 for x,y in p),baseline_full=sum(x==1 for x,y in p),full_to_lower=sum(x==1 and y<1 for x,y in p),full_to_zero=sum(x==1 and y==0 for x,y in p))
report={}
for method,key in [('SkillEvolver','skillevolver'),('SPARK','spark'),('CoEvoSkills','coevoskills')]:
 rows=[]; sd={}
 for run in ['1','2']:
  rr=[x for x in s if x['method']==method and x['run']==run];sd[run]={x['task']:sign(float(x['delta'])) for x in rr};rows.append(('Source run '+run,stats([(float(x['baseline']),float(x['skill'])) for x in rr])))
 vv=[x for x in v if x['method']==key]
 for label,part in [('Variants: all',vv)]+[(f'Variants: P{k}',[x for x in vv if f'--p{k}--' in x['variant_id']]) for k in range(1,4)]:
  rows.append((label,stats([(x['baseline']['reward'],x['skill']['reward']) for x in part])))
 report[method]={'rows':dict(rows),'repeat_sign_counts':dict(Counter(f'{sd["1"][t]},{sd["2"][t]}' for t in sd['1']))}
report['provenance']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [vp,sp]}
(A/'statistics.json').write_text(json.dumps(report,indent=2)+'\n')
