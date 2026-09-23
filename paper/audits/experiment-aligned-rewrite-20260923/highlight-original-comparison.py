"""Reproduce red content highlights relative to the original Overleaf manuscript."""
from pathlib import Path
import fitz, json, hashlib, unicodedata, subprocess
ROOT=Path(__file__).resolve().parents[3]
DOC=fitz.open(ROOT/'output/pdf/main.pdf')
records=[]
def canon(t):return ''.join(c.lower() for c in unicodedata.normalize('NFKD',t) if c.isalnum())
def mark(page,rects,text,comment):
    pdf_page=DOC[page]
    a=pdf_page.add_highlight_annot([fitz.Rect(r).quad for r in rects])
    a.set_colors(stroke=(1,.4,.4));a.set_opacity(.35)
    a.set_info(title='Codex · 与最初原版对比 · 2026-09-23',subject='相对原始 Overleaf 版本的新增或替换内容',content=comment);a.update()
    records.append({'page':page+1,'text':text,'comment':comment,'color':'#ff6666','rects':[list(r) for r in rects]})
def search(text,comment):
    stream=[];mapping=[]
    for pi,p in enumerate(DOC):
        for bi,b in enumerate(p.get_text('rawdict')['blocks']):
            if b['type']!=0:continue
            for li,l in enumerate(b['lines']):
                for span in l['spans']:
                    for c in span['chars']:
                        for v in canon(c['c']):
                            stream.append(v);mapping.append((pi,(bi,li),c['bbox']))
    target=canon(text);joined=''.join(stream)
    assert joined.count(target)==1,(text,joined.count(target))
    start=joined.index(target);groups={}
    for pi,k,box in mapping[start:start+len(target)]:
        page_groups=groups.setdefault(pi,{})
        if k in page_groups:page_groups[k]|=fitz.Rect(box)
        else:page_groups[k]=fitz.Rect(box)
    for pi,g in groups.items():mark(pi,g.values(),text,comment)
def blocks(pi,indices,comment):
    bs=DOC[pi].get_text('dict')['blocks']
    for i in indices:
        b=bs[i];assert b['type']==0
        mark(pi,[l['bbox'] for l in b['lines']],' '.join(''.join(s['text'] for s in l['spans']) for l in b['lines']),comment)

source=(ROOT/'paper/maintext-20260921/main.tex').read_text()
abstract=source.split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0].strip()
search(abstract,'摘要重写：用重复评估、任务变体和技能案例概述实际完成的诊断研究，删除旧干预实验承诺。')
search('Agent skills, self-evolution, diagnostic evaluation, skill reuse, generalization','关键词更新：与技能复用诊断主题一致。')
phase=None
for pi,page in enumerate(DOC):
 for bi,block in enumerate(page.get_text('dict')['blocks']):
  if block['type']!=0:continue
  t=' '.join(''.join(sp['text'] for sp in l['spans']) for l in block['lines']);c=canon(t)
  if c.endswith('introduction'):phase='intro'
  if c.endswith('problemformulation'):phase=None
  if 'diagnosingwhataskillhaslearned' in c:phase='body'
  if c.endswith('references') and len(c)<20:phase=None
  if phase:
   blocks(pi,[bi],'引言重写：围绕实际三种方法、重复运行、任务变体和技能复用组织研究。' if phase=='intro' else '相对最初原版新增或重写：真实实验结果、技能案例、诊断解释、讨论、相关工作与结论。')
  elif 'feedbackfromexecutionandevaluation' in c:
   blocks(pi,[bi],'问题定义调整：移除与本研究无关的答案反馈表述。')
  elif 'ourevaluationsexaminetheutilityofthecompletedskill' in c:
   blocks(pi,[bi],'图1说明更新：指出本研究实际评估的是完成技能的效用和变体复用。')
import re
reference_text=' '.join(p.get_text() for p in DOC).split('REFERENCES')[-1]
for title,comment in [('SkillEvolver: Skill Learning as a Meta-Skill','新增参考文献：SkillEvolver。'),('Evidence Over Plans: Online Trajectory Verification for Skill Distillation','新增参考文献：SPARK。')]:
 entries=re.split(r'(?=\[\d+\])',reference_text)
 entry=next(e for e in entries if canon(title) in canon(e));search(entry.strip(),comment)
out=ROOT/'output/pdf/main-revision-highlighted.pdf';DOC.save(out,garbage=4,deflate=True)
base=subprocess.check_output(['git','show','121a6182b:paper/maintext-20260921/main.tex'],cwd=ROOT)
assert base==(ROOT/'paper/overleaf-original-20260921/main.tex').read_bytes()
record={'baseline_commit':'121a6182b','baseline':'Original Overleaf source; distinct from PDF/main.pdf','baseline_tex_sha256':hashlib.sha256(base).hexdigest(),'current_pdf_sha256':hashlib.sha256((ROOT/'output/pdf/main.pdf').read_bytes()).hexdigest(),'annotations':records,'deleted_from_baseline':['SkillRevise/SkillHone/SkillOpt experiments and their dependent text','Original tables 1/2/3 and lifecycle-intervention figure','Original lifecycle reporting protocol and limitations about unrelated experiments'],'highlight_policy':'Mark rewritten paragraphs/headings and inserted experiments relative to original Overleaf. Do not mark unchanged title, generic equations, or citation renumbering; deleted material is listed in the change record.'}
(ROOT/'paper/audits/experiment-aligned-rewrite-20260923/highlights.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
assert [p.get_text() for p in fitz.open(out)]==[p.get_text() for p in fitz.open(ROOT/'output/pdf/main.pdf')]
print('Saved',len(records),'highlights on pages',sorted(set(a['page'] for a in records)))
