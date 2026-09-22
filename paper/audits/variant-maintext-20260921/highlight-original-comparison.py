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
    a.set_info(title='Codex · 与最初原版对比 · 2026-09-22',subject='相对原始 Overleaf 版本的新增或替换内容',content=comment);a.update()
    records.append({'page':page+1,'text':text,'comment':comment,'color':'#ff6666','rects':[list(r) for r in rects]})
def search(text,comment):
    found=[]
    for pi,p in enumerate(DOC):
        stream=[];mapping=[]
        for bi,b in enumerate(p.get_text('rawdict')['blocks']):
            if b['type']!=0:continue
            for li,l in enumerate(b['lines']):
                for s in l['spans']:
                    for c in s['chars']:
                        for v in canon(c['c']):stream.append(v);mapping.append(((bi,li),c['bbox']))
        target=canon(text);start=''.join(stream).find(target)
        if start<0:continue
        groups={}
        for k,box in mapping[start:start+len(target)]:
            if k in groups:groups[k]|=fitz.Rect(box)
            else:groups[k]=fitz.Rect(box)
        found.append((pi,groups))
    assert len(found)==1,(text,len(found))
    pi,g=found[0];mark(pi,g.values(),text,comment)
def blocks(pi,indices,comment):
    bs=DOC[pi].get_text('dict')['blocks']
    for i in indices:
        b=bs[i];assert b['type']==0
        mark(pi,[l['bbox'] for l in b['lines']],' '.join(''.join(s['text'] for s in l['spans']) for l in b['lines']),comment)
abstract='We combine repeated evaluations, controlled task variations, and lifecycle interventions to examine whether improvements from skill evolution persist and transfer, and to trace their origins to feedback, revision, selection, skill content, and evaluation.'
search(abstract,'摘要替换：围绕改进能否保持、迁移及其来源合并实验概述；替换原版 Across SkillRevise 开头的方法枚举句。')
search('We organize the experiments around utility, behavioral scope, and lifecycle attribution. Repeated standard-task evaluations of SkillEvolver, SPARK, and CoEvoSkills measure skill utility, and controlled task variants examine how far that utility extends. Inspection of skill content and execution traces then identifies reusable decisions expressed during deployment. Complementary mechanism studies in SkillRevise, SkillHone, and SkillOpt examine retention and the origins of observed gains. These studies represent trace-conditioned revision, history-based iterative honing, and validation-gated bounded editing in frozen-agent systems with persistent external skill artifacts.','引言替换：说明标准任务、变体评估、技能复用分析与后续机制研究的关系。')
search('The following experiments address these questions in turn.','替换原文：The next two sections address these questions in turn. 因新增实验章节而更新衔接。')
blocks(1,range(12,21),'相对基线新增的 SkillsBench 实验：设置、配对指标、两次重复结果及变体评估。')
blocks(2,range(0,5),'新增表1：三个方法、各两次重复的标准任务配对结果。')
blocks(2,range(5,8),'新增表2：纳入补跑与文件读取修复，描述性汇总 SkillEvolver 222、SPARK 221、CoEvoSkills 221 个变体。')
blocks(2,range(8,12),'新增变体实验：分别报告各方法完整记录的总体效果和 P1/P2/P3 结果。')
blocks(2,range(12,14),'新增技能复用分析：提炼诊断规则、适用条件和正确性约束，并衔接保持性与生命周期研究。')
search('In the recorded variant evaluations, SkillEvolver retains positive mean gains across changes in input representation, task-instance structure, and coupled requirements; SPARK shows gains on two types of change, while CoEvoSkills shows declines on all three. Execution traces connect successful cases to reusable diagnostic steps and preservation of task constraints.','结论新增：概括完整变体记录的结果及技能复用观察。')
search('Zhang, G.; Zhu, E.; Zhou, J.; Jia, C.; and Wang, H. 2026a. SkillEvolver: Skill Learning as a Meta-Skill. arXiv:2605.10500.','新增参考文献：SkillEvolver。')
search('Zhou, Y.; Dong, Z.; Wang, Z.; Jin, C.; Zhao, S.; Guo, B.; Gu, D.; Zhang, L.; Zhou, M.; and Metaxas, D. N. 2026b. Evidence Over Plans: Online Trajectory Verification for Skill Distillation. arXiv:2605.09192.','新增参考文献：SPARK。')
out=ROOT/'output/pdf/main-revision-highlighted.pdf';DOC.save(out,garbage=4,deflate=True)
base=subprocess.check_output(['git','show','121a6182b:paper/maintext-20260921/main.tex'],cwd=ROOT)
assert base==(ROOT/'paper/overleaf-original-20260921/main.tex').read_bytes()
record={'baseline_commit':'121a6182b','baseline':'Original Overleaf manuscript, not the separately supplied PDF/main.pdf.','baseline_tex_sha256':hashlib.sha256(base).hexdigest(),'current_pdf_sha256':hashlib.sha256((ROOT/'output/pdf/main.pdf').read_bytes()).hexdigest(),'scope':'All substantive text, table and bibliography additions/replacements relative to the original. Layout moves and automatic numbering changes are recorded separately.','layout_changes':['Removed FloatBarrier breaks and advanced float declarations to keep figures/tables near the relevant discussion.','Changed the lifecycle feedback arrow to a compact orthogonal path.','Changed the claim table placement from H to !t.'],'annotations':records}
(ROOT/'paper/audits/variant-maintext-20260921/original-comparison-highlights-20260922.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
assert [p.get_text() for p in fitz.open(out)]==[p.get_text() for p in fitz.open(ROOT/'output/pdf/main.pdf')]
print('Saved',len(records),'highlights on pages',sorted(set(a['page'] for a in records)))
