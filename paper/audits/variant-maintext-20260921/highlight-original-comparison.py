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
search(abstract,'摘要替换：围绕改进能否保持、迁移及其来源概述研究。')
search("We organize the evidence as a diagnosis of utility, behavioral scope, and gain attribution. Standard-task evaluations of SkillEvolver, SPARK, and CoEvoSkills first establish the observed utility of completed artifacts across two runs. Controlled task changes then reveal different scopes of usefulness, and artifact and trace inspection examines the decisions preserved during reuse. This motivates the next diagnostic step: locating an improvement in the artifact's evolution history. Complementary studies of SkillRevise, SkillHone, and SkillOpt use retention tests and lifecycle interventions to examine trace-conditioned revision, history-based iterative honing, and validation-gated editing. Each study addresses a specific part of the identification question.",'引言替换：按效用、行为范围、收益归因组织诊断证据，并区分两组方法承担的研究问题。')
search('The following experiments address these questions in turn.','因新增实验章节而更新衔接。')
assert 'Diagnosing the Scope' in DOC[1].get_text('blocks')[12][4]
blocks(1,range(12,len(DOC[1].get_text('dict')['blocks'])),'新增实验：诊断问题、实验设置、标准任务重复结果与配对分析。')
assert 'Table 1:' in DOC[2].get_text()
assert 'Table 2:' in DOC[2].get_text()
blocks(2,range(len(DOC[2].get_text('dict')['blocks'])),'新增标准任务与完整变体表；不同任务变化下的技能效用分析。')
assert 'Tracing Utility' in DOC[3].get_text()
assert 'Identifying Retained Skill Effects' not in DOC[3].get_text()
blocks(3,range(len(DOC[3].get_text('dict')['blocks'])),'新增诊断分析：收益范围、幅度与频率、轨迹决策、成功与失败边界及生命周期归因衔接。')
search('We diagnose where the gains from self-evolving persistent skills reside and how far they extend. All three methods in the standard-task evaluations have positive paired gains in both runs, but task variation separates their utility profiles. SkillEvolver remains positive across representation, instance, and requirement changes; SPARK combines gains on two probes with a decline on instance changes; CoEvoSkills declines on all three. The inspected traces identify decision criteria and correctness checks expressed during successful reuse. Complementary lifecycle interventions show that adopted artifact components can change behavior, selected outcomes can disappear under fresh deployment, and fixed outputs can receive different verdicts under different verifiers. Together, these findings distinguish useful artifacts, their behavioral scope, and the processes that produce or measure their apparent improvement.','结论重写：总结收益存在、范围分化、行为决策与生命周期机制的诊断关系。')
search('Zhang, G.; Zhu, E.; Zhou, J.; Jia, C.; and Wang, H. 2026a. SkillEvolver: Skill Learning as a Meta-Skill. arXiv:2605.10500.','新增参考文献：SkillEvolver。')
search('Zhou, Y.; Dong, Z.; Wang, Z.; Jin, C.; Zhao, S.; Guo, B.; Gu, D.; Zhang, L.; Zhou, M.; and Metaxas, D. N. 2026b. Evidence Over Plans: Online Trajectory Verification for Skill Distillation. arXiv:2605.09192.','新增参考文献：SPARK。')
out=ROOT/'output/pdf/main-revision-highlighted.pdf';DOC.save(out,garbage=4,deflate=True)
base=subprocess.check_output(['git','show','121a6182b:paper/maintext-20260921/main.tex'],cwd=ROOT)
assert base==(ROOT/'paper/overleaf-original-20260921/main.tex').read_bytes()
record={'baseline_commit':'121a6182b','baseline':'Original Overleaf manuscript, not the separately supplied PDF/main.pdf.','baseline_tex_sha256':hashlib.sha256(base).hexdigest(),'current_pdf_sha256':hashlib.sha256((ROOT/'output/pdf/main.pdf').read_bytes()).hexdigest(),'scope':'All substantive text, table and bibliography additions/replacements relative to the original. Layout moves and automatic numbering changes are recorded separately.','layout_changes':['Removed FloatBarrier breaks and advanced float declarations to keep figures/tables near the relevant discussion.','Changed the lifecycle feedback arrow to a compact orthogonal path.','Changed claim and artifact-mediation tables from H to !t to prevent column gaps.','Used ragged-bottom pages to prevent stretched paragraph gaps.','Withdrew the two provisional flow figures; this revision adds no figure.'],'annotations':records}
(ROOT/'paper/audits/variant-maintext-20260921/original-comparison-highlights-20260922.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
assert [p.get_text() for p in fitz.open(out)]==[p.get_text() for p in fitz.open(ROOT/'output/pdf/main.pdf')]
print('Saved',len(records),'highlights on pages',sorted(set(a['page'] for a in records)))
