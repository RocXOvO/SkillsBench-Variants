import json,hashlib
from pathlib import Path
import fitz
R=Path(__file__).resolve().parents[3];A=Path(__file__).parent
s=json.loads((A/'statistics.json').read_text())
for m in ['SkillEvolver','SPARK','CoEvoSkills']:
 for label,z in s[m]['rows'].items():
  assert z['improved']+z['regressed']+z['tied']==z['n']
  assert abs(z['gain_mass']-z['loss_mass']-z['delta'])<1e-9
 assert sum(s[m]['repeat_sign_counts'].values())==s[m]['rows']['Source run 1']['n']
t=(R/'paper/maintext-20260921/skillsbench-variant-table.tex').read_text()
assert 'Variants: all' not in t
assert t.count('Variants: P')==9 and t.count('Source run')==6
out={}
for name in ['main.pdf','main-bilingual-en-zh.pdf']:
 p=R/'output/pdf'/name
 if not p.exists():continue
 d=fitz.open(p);out[name]={'pages':len(d),'annotations':sum(len(list(x.annots() or [])) for x in d),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 assert out[name]['annotations']==0
out['layout']='English pages 1–5 visually inspected; table page 3 starts after complete paragraph and precedes section 4; references separate page 5.'
out['zotero']='Pending: desktop getApp returned timeoutReached (-10005). No attachment was changed.'
(A/'verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
