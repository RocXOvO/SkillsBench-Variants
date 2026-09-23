"""Repair observed PDF2zh layout/translation defects on the Chinese half only."""
from pathlib import Path
import fitz,json,html
ROOT=Path(__file__).resolve().parents[3]
FONT=Path('/Users/duchongyang/.cache/babeldoc/fonts')
PATCHES=[
(0,(90,97,521,119),'自进化智能体技能是否在学习技能？',12,True,'center'),
(0,(54,632,300,674),'三种方法呈现出不同的结果。它们在标准任务的两次运行中均有正向配对增益。在任务变体上，SkillEvolver 在全部三类',8.5,False,'left'),
(0,(315,173,560,215),'变化下均保持正向平均增益；SPARK 的收益取决于变化类型，CoEvoSkills 则由正转负。实例变化的分化最明显。因此，源任务收益反复出现与泛化是技能的不同属性。',8.5,False,'left'),
(0,(360,448,519,464),'2. 问题定义',9,True,'center'),
(0,(315,574,559,591),'随后，智能体使用冻结技能执行任务 x：',9,False,'left'),
(1,(54,176,298,191),'2.2. 诊断技能学到了什么',9,True,'left'),
(1,(54,362,300,378),'3. 诊断技能效用的范围',9,True,'center'),
(1,(54,453,309,502),'我们在 SkillsBench [4] 上评估 SkillEvolver [1]、SPARK [2] 和 CoEvoSkills [3]，每种方法运行两次。每次将技能条件与同题无技能执行配对。同一方法的两次运行使用相同任务集：SkillEvolver 81 题、SPARK 84 题、CoEvoSkills 85 题。',8.5,False,'left'),
(1,(54,621,301,680),'三种方法在两次运行中的平均配对增益均为正（表1）。SkillEvolver 提高25.61和25.02分，CoEvoSkills 提高10.24和9.76分，SPARK 提高1.84和6.45分。前两者的无技能分数虽变化较大，增益却相近。因此，跨运行的收益比技能条件的绝对分数更稳定。',8.5,False,'left'),
(1,(54,684,301,722),'逐题结果也有差异。SkillEvolver 每次运行的改进数至少是退化数的四倍；CoEvoSkills 两次均改进17题，分别退化9题和10题。',8.5,False,'left'),
(1,(315,333,568,366),'表1. SkillsBench 上每种方法的两次运行。平均验证器奖励及配对增益 Δ 均按0–100分制报告。I/R/T 分别为改进、退化和持平的任务数。',8.5,False,'left'),
(2,(54,208,310,264),'表2. 任务变化下的技能效用，汇总历史评估与补跑结果。每种方法均与同一变体的无技能基线配对。P1/P2/P3 分别为表示、实例和需求变化。B部分给出变体数 N 与配对增益 Δ；分数及 I/R/T 定义同表1。',8.5,False,'left'),
(2,(315,248,568,332),'SPARK 从经环境验证的轨迹中蒸馏技能，保留执行证据、检查与经验教训 [2]。其调度结果说明，这类证据可以支持成功复用。总体结果有升有降，进一步引出了抽象问题：已验证的执行说明哪些做法在源任务上有效；实例变化后，仍需判断哪些选择应保留、哪些应重新计算。P2 上的下降使这一区别对解释其结果尤为重要。',9,False,'left'),
(2,(315,682,559,718),'因此，评估应报告源任务的配对效用，在不同任务变化下检验同一冻结技能，',8.5,False,'left'),
(3,(54,262,301,321),'评估技能效用与使用。SkillsBench 覆盖多样任务，SWE-Skills-Bench 研究软件工程中的技能使用 [4,5]。SkillLearnBench 评估真实任务上的持续技能生成 [6]。《从原始经验到',8.5,False,'left'),
(3,(315,71,560,134),'技能使用》区分经验生成、技能提取与下游使用 [7]。我们的研究将重复的源任务结果、受控任务变化和技能层面的案例联系起来，补充这些评估。核心研究对象是冻结技能的适用范围，而不仅是它在源任务上的分数。',9,False,'left'),
]
def repair(doc,clean):
 records=[]
 for pi,box,t,size,bold,align in PATCHES:
  r=fitz.Rect(box)+(612,0,612,0);p=doc[pi];p.add_redact_annot(r,fill=(1,1,1));p.apply_redactions(images=0,graphics=0)
  css=f'@font-face{{font-family:CN;src:url(SourceHanSerifCN-Regular.ttf)}} @font-face{{font-family:CN;font-weight:bold;src:url(SourceHanSerifCN-Bold.ttf)}} *{{margin:0;padding:0}} div{{font-family:CN;font-size:{size}pt;line-height:1.18;font-weight:{"bold" if bold else "normal"};text-align:{align}}}'
  spare,scale=p.insert_htmlbox(r,'<div>'+html.escape(t)+'</div>',css=css,archive=fitz.Archive(str(FONT)),scale_low=.85)
  assert spare>=0,(pi,t,spare)
  records.append({'page':pi+1,'rect':list(r),'text':t,'font_pt':size,'scale':scale})
 # Preserve the source's readable numeric table typography instead of the plugin's variable shrinkage.
 for pi,box in [(1,(325,231,550,328)),(2,(71,70,283,203))]:
  r=fitz.Rect(box);dst=r+(612,0,612,0);p=doc[pi];p.add_redact_annot(dst,fill=(1,1,1));p.apply_redactions(images=0,graphics=2);p.show_pdf_page(dst,clean,pi,clip=r)
  records.append({'page':pi+1,'table_restored_from_english':list(dst),'reason':'Preserve nine-point table data and unambiguous headers; translated caption defines notation.'})
 # Bibliographic author names/titles are kept in their original citation form.
 p=doc[4];r=fitz.Rect(612,0,1224,792);p.add_redact_annot(r,fill=(1,1,1));p.apply_redactions(images=0,graphics=2);p.show_pdf_page(r,clean,4)
 doc.subset_fonts()
 (ROOT/'paper/audits/experiment-aligned-rewrite-20260923/chinese-repairs.json').write_text(json.dumps({'repairs':records,'reference_policy':'Chinese half uses original English bibliography to preserve names, citation boundaries and titles.','english_half_unchanged':True},ensure_ascii=False,indent=2)+'\n')
