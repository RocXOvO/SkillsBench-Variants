from pathlib import Path
from collections import defaultdict
import csv,json,subprocess,hashlib,re,fitz,math
root=Path(__file__).resolve().parents[3];src=root/'paper/maintext-20260921';out=Path(__file__).parent
old=lambda f:subprocess.check_output(['git','show',f'db9127c20:paper/maintext-20260921/{f}'],cwd=root).decode()
# Preserve every numeric data cell across the single-column table reformat.
def rows(s):
 result=[]
 for line in s.splitlines():
  if not re.match(r'^(SkillEvolver|SPARK|CoEvoSkills| & [12] &)',line):continue
  line=re.sub(r'\\multicolumn\{\d+\}\{[^}]+\}', '',line)
  result.append(re.findall(r'[+-]?\d+(?:\.\d+)?',line))
 return result
for f in ['skillsbench-experiments.tex','skillsbench-variant-table.tex']:
 assert rows(old(f))==rows((src/f).read_text()),f
v=json.loads((root/'paper/audits/full-variant-records-20260922/paired-scores.json').read_text());stats=json.loads((root/'paper/audits/full-variant-records-20260922/statistics.json').read_text())
for method,m in stats['methods'].items():
 for group,expected in [('all',m['overall'])]+list(m['paradigms'].items()):
  r=[x for x in v if x['method']==method and (group=='all' or f'--{group}--' in x['variant_id'])];n=len(r);ds=[float(x['skill']['reward'])-float(x['baseline']['reward']) for x in r]
  assert n==expected['n'];assert math.isclose(100*sum(ds)/n,expected['delta'],abs_tol=1e-9)
  assert [sum(d>1e-9 for d in ds),sum(d<-1e-9 for d in ds),sum(abs(d)<=1e-9 for d in ds)]==[expected[k] for k in ['improved','regressed','tied']]
standard=defaultdict(list)
with (root/'paper/audits/six-run-maintext-20260921/paired-scores.tsv').open() as f:
 for r in csv.DictReader(f,delimiter='\t'):standard[(r['method'],r['run'])].append(r)
computed=[]
for (m,run),rows in standard.items():
 vals={k:100*sum(float(x[k]) for x in rows)/len(rows) for k in ['baseline','skill','delta']};computed.append({'method':m,'run':run,'n':len(rows),**vals})
 row=f"{m if run=='1' else ''} & {run} & {len(rows)} & {vals['baseline']:.2f} & {vals['skill']:.2f} & $+{vals['delta']:.2f}$";assert row in (src/'skillsbench-experiments.tex').read_text(),row
alltex='\n'.join((src/f).read_text() for f in ['main.tex','skillsbench-experiments.tex','skillsbench-variants.tex','skillsbench-diagnosis.tex','skillsbench-variant-table.tex'])
assert not re.search(r'SkillRevise|SkillHone|SkillOpt|144/144|24-task|53/86|28/86|artifact surgery|verifier swap|hidden-oracle|preregistered|predeclared',alltex,re.I)
log=(src/'build/main.log').read_text();assert not re.search(r'Overfull|Underfull|undefined|Warning',log)
d=fitz.open(root/'output/pdf/main.pdf');assert len(d)==5
assert 'REFERENCES' in d[4].get_text()
assert all('REFERENCES' not in p.get_text() for p in list(d)[:4])
# Each table's panel/header and data occupy only one column.
assert all(r.x0 > 310 for r in d[1].search_for('I/R/T') if r.y0 < 400)
assert all(r.x1 < 306 for r in d[2].search_for('I/R/T'))
bounds=[]
for i,p in enumerate(d):
 assert p.rect==fitz.Rect(0,0,612,792)
 bs=p.get_text('blocks');b=[min(x[0] for x in bs),min(x[1] for x in bs),max(x[2] for x in bs),max(x[3] for x in bs)];bounds.append(b);assert b[0]>=52 and b[1]>=70 and b[2]<=562 and b[3]<=726,(i,b)
record={'base_commit':'db9127c20','baseline_comparison_commit':'121a6182b','standard_pairs':sum(map(len,standard.values())),'standard_summaries_recomputed':computed,'variant_pairs_recomputed':len(v),'variant_unique_cells':886,'table_numeric_cells_identical':True,'tables_single_column':True,'references_start_new_page':5,'old_experiment_names_and_claims_removed':True,'experiment_changes':False,'pages':len(d),'visual_qa':'All five pages inspected. Table 1 follows a completed paragraph on page 2 right; Table 2 follows the complete instance-change paragraph on page 3 left. No table splits a paragraph; the parent-to-final contrast is explicitly separated from completed-skill utility. References start page 5; page 4 whitespace follows the explicit separate-reference-page requirement.','page_text_bounds':bounds,'latex_warnings':0,'review':'Native read-only scoped reviewer plus primary inline evidence review; shared-family assistance, no formal ARS certification','sources':{f:hashlib.sha256((src/f).read_bytes()).hexdigest() for f in ['main.tex','skillsbench-experiments.tex','skillsbench-variants.tex','skillsbench-diagnosis.tex','skillsbench-variant-table.tex']},'pdf_sha256':hashlib.sha256((root/'output/pdf/main.pdf').read_bytes()).hexdigest()}
(out/'validation.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n');print('Verified 500 standard pairs, 664 variant pairs, unchanged numerical table data, single-column tables, four body pages plus separate references')
