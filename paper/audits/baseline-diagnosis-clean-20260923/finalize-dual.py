"""Finalize the plugin translation, repair observed defects, and emit a clean bilingual PDF."""
from pathlib import Path
import json,fitz,html,unicodedata,hashlib,shutil
R=Path(__file__).resolve().parents[3];A=Path(__file__).parent;Q=R/'tmp/pdfs/baseline-diagnosis-clean-20260923';F=Path('/Users/duchongyang/.cache/babeldoc/fonts')
result=json.loads((Q/'translation-result.json').read_text());translated=fitz.open(next(p for p in result['filePaths'] if 'LR_dual' in p));clean=fitz.open(R/'output/pdf/main.pdf')
# The final English abstract and one heading were clarified after translation.
# Use the final compiled English pages verbatim; manually align the Chinese abstract/heading below.
d=fitz.open()
for i,p in enumerate(clean):
 n=d.new_page(width=1224,height=792);n.show_pdf_page(fitz.Rect(0,0,612,792),clean,i);n.show_pdf_page(fitz.Rect(612,0,1224,792),translated,i,clip=fitz.Rect(612,0,1224,792))
P=[
(0,(90,97,521,120),'自进化智能体技能是否在学习技能？',12,True,'center'),
(0,(54,189,306,336),'自进化智能体将经验存储在持久技能中，但任务分数提高后，技能究竟学到了什么仍有待解释。我们研究收益能否在源任务之外持续，以及技能中的哪些决策解释了成功与失败。我们通过重复的配对评估、受控任务变化，以及技能内容和执行轨迹检查，诊断 SkillEvolver、SPARK 和 CoEvoSkills 的最终技能产物，并以其构建过程作为解释背景。三种方法的源任务收益均反复出现，但任务变化揭示了不同的有效复用范围。对照案例将复用结果与区分有效答案和候选答案、保留正确解所需约束的指导联系起来。这些发现连接了基准收益与持久决策指导，并区分产生有用技能、应用其指导和在任务变化后保持收益。',9,False,'left'),
(0,(54,338,301,354),'关键词—智能体技能，自进化，诊断评估，技能复用，泛化',8.5,False,'left'),
(0,(54,392,306,474),'持久技能为智能体提供了一条无需更新模型参数的改进路径。指令、脚本和参考资料让后续执行能够利用已有经验。SkillEvolver、SPARK 和 CoEvoSkills 分别通过基于部署的修订、经验证轨迹的蒸馏和协同进化验证来构建技能产物 [1–3]。这些产物引出了标题中的问题：系统生成得分更高的技能时，哪些有用行为得以持久保留？',9,False,'left'),
(0,(54,559,302,656),'我们提出两个相关问题。收益是否持续，在哪些任务变化下持续？重复的源任务评估检验配对效用是否反复出现，冻结技能的变体评估揭示同一指导能够满足哪些需求。技能及其使用中的哪些决策解释了观察结果？对照执行可以揭示技能是否提供关键的正确性标准，以及执行者是否将它用于新任务。这两个问题将有用行为的存在及范围，与行为如何产生的解释联系起来。',9,False,'left'),
(0,(315,258,568,352),'三种方法在两次运行中均有正向源任务平均增益，但任务变化打破了这种一致性。SkillEvolver 在全部三类变化下保持正向收益。SPARK 的收益取决于变化类型，CoEvoSkills 则在三类变化下均为负向均值。实例替换时的分化最明显。案例说明，执行程序只是问题的一部分：执行者还须区分目标信号与误导候选，以及有效的调度修复与仅满足可行性的排程。',9,False,'left'),
(0,(315,352,564,421),'本文贡献在于诊断观察到的技能收益代表什么。重复配对评估检验效用是否反复出现，受控变体界定其范围，技能产物层面的案例则识别与复用成功及失败相关的决策。这些结果共同说明，分数优势可以通过构建后保留、并在执行中实际使用的指导来解释。',9,False,'left'),
(0,(315,562,554,578),'随后，智能体使用冻结技能执行任务 x：',9,False,'left'),
(1,(54,455,300,499),'我们首先检验最终技能是否反复对源任务产生收益，再冻结技能并改变任务，考察收益能够适应哪些需求。配对的无技能执行为这两种比较提供参照。',9,False,'left'),
(1,(54,526,307,575),'我们在 SkillsBench [4] 上评估 SkillEvolver [1]、SPARK [2] 和 CoEvoSkills [3]，每种方法运行两次。每次将技能条件与同题无技能执行配对。同一方法两次运行使用相同任务集：SkillEvolver 81题，SPARK 84题，CoEvoSkills 85题。',8.5,False,'left'),
(1,(54,578,300,604),'我们报告0–100分制的平均验证器奖励，以及技能与无技能条件的平均同题差值。对包含 N 个任务的运行，配对增益为',8.5,False,'left'),
(1,(54,677,301,692),'3.2. 两次运行均有正向源任务效用',9,True,'left'),
(1,(54,694,301,722),'三种方法两次均有正向平均配对增益（表1）。SkillEvolver 提高25.61和25.02分，',8.5,False,'left'),
(1,(315,175,568,216),'CoEvoSkills 提高10.24和9.76分，SPARK 提高1.84和6.45分。SkillEvolver 和 CoEvoSkills 的无技能分数虽变化较大，增益却相近。配对比较揭示了技能条件的绝对分数会掩盖的重复效用。',8.5,False,'left'),
(1,(315,218,572,301),'逐题结果也有差异。SkillEvolver 每次运行的改进数至少为退化数的四倍；CoEvoSkills 两次均改进17题，分别退化9题和10题。SPARK 首次的改进与退化数接近，第二次为13次改进、5次退化。增益因此同时反映逐题变化的幅度和频率。冻结技能的变体评估检验这些收益背后的指导能否持续适应不同任务需求。',9,False,'left'),
(1,(315,414,568,444),'表1. SkillsBench 上每种方法的两次运行。平均验证器奖励及配对增益 Δ 均按0–100分制报告。I/R/T 分别为改进、退化和持平的任务数。',8.5,False,'left'),
(1,(315,572,568,625),'完整记录包含222个变体，以及无技能和三种方法共886条条件级结果。表2汇总历史评估与补跑：SkillEvolver 覆盖222个变体，SPARK 和 CoEvoSkills 各覆盖221个。每个技能条件均与同一变体的无技能结果配对。',8.5,False,'left'),
(1,(315,626,568,721),'源任务改进不等于有效泛化。三种方法两次均提高源任务平均奖励，变体结果却分化。SkillEvolver 的平均增益为11.94分，SPARK 的 +0.65 接近零，CoEvoSkills 则低于无技能基线5.01分。SkillEvolver 的改进数多于退化数（47比20），另两种方法则相反。SPARK 接近零的均值汇集了方向相反的变化。',9,False,'left'),
(2,(54,71,303,95),'这并非每个变体都变化很小。SkillEvolver 同时具有更大的正向均值和多于退化的改进数。',8.5,False,'left'),
(2,(54,95,304,216),'实例替换带来的分化最明显。SkillEvolver 在三类变化下均为正，P2 增益最大（+14.56）。SPARK 和 CoEvoSkills 在 P2 上下降也最明显（−5.23 和 −9.51）。SPARK 在表示和需求变化下保持正向均值，底层实例变化后却失去优势。P2 要求根据新数据或实例结构重新计算决策，因此重命名输入后仍然有用的程序，在决策本身变化后可能失效。SkillEvolver 在 P1–P3 上均有正向收益，呈现最广的效用持续范围；CoEvoSkills 的负向均值说明，源任务指导在任务变化后可能适得其反。',9,False,'left'),
(2,(54,368,309,425),'表2. 任务变化下的技能效用，描述性汇总历史评估与补跑结果。每种方法均与同一变体的无技能基线配对。P1/P2/P3 分别为表示、实例和需求变化。B部分给出变体数 N 与配对增益 Δ；分数及 I/R/T 定义同表1。',8.5,False,'left'),
(2,(54,437,301,453),'4. 定位复用成功与失败的环节',9,True,'center'),
(2,(315,115,559,131),'4.2. 保留定义正确修复的规则',9,True,'left'),
(2,(54,549,302,613),'在系外行星检测中，SkillEvolver 技能在输入列重排（P1）和要求两个信号（P3）时均成功。CoEvoSkills 两者均失败：将恒星调制报告为目标信号，并将一个信号及其谐波视为两个独立信号。两种技能均未通过替换实例的 P2 变体。',9,False,'left'),
(2,(54,613,302,723),'差异体现在技能要求执行者检查什么。SkillEvolver 将候选发现、信号诊断和精炼分开，指导执行者处理误导峰值、符合凌日的持续时间及谐波关系。CoEvoSkills 也包含相位折叠、奇偶及残差检查，但执行时未能排除误导候选。检查流程的存在不如其标准能否区分关键候选更有解释力。SkillEvolver 在 P1 和 P3 成功，说明指导适用于变化后的输入和需求。其 P2 失败则',9,False,'left'),
(2,(315,422,563,506),'SPARK 从经环境验证的轨迹中蒸馏技能，保留执行证据、检查和经验教训 [2]。调度结果说明这些证据能支持成功复用。总体结果有升有降，提出了抽象问题：验证过的执行说明哪些做法在源任务上有效；实例变化后，仍须决定哪些选择应保留、哪些应重新计算。P2 上的下降使这一区分对理解结果尤为重要。',9,False,'left'),
(2,(315,517,568,614),'CoEvoSkills 从协同进化的替代验证器获取详细修订反馈，而真实评测器仅返回不透明的通过或失败信号 [3]。因此，替代验证器对正确性条件的覆盖范围与技能保留的指导相关。这为调度失败提供了一个可能解释：技能虽有多个检查，复用仍依赖此次执行中未落实的条件。反馈覆盖范围和对源实例的抽象程度，是解释不同效用范围的候选原因。',9,False,'left'),
(2,(315,670,561,710),'标准任务与变体结果揭示了最终技能的两个属性。三种方法的源任务效用均反复出现，但其适用范围随任务变化而分化。SkillEvolver 在 P1–P3 上均有正向增益，支持各类受测变化下的有效复用。',8.5,False,'left'),
(3,(54,71,300,128),'SPARK 在 P1 和 P3 上为正、P2 上为负，定位了更具体的困难：调整输入表示或需求可以保持收益，替换底层实例却可能消除收益。CoEvoSkills 的负向均值说明，对源任务有用的指导可能妨碍变化后的任务。',9,False,'left'),
(3,(54,135,303,202),'整体适用范围中也存在局部边界。SkillEvolver 的 P2 均值最强，却未通过替换实例的信号检测案例。SPARK 的整体变体收益接近零，却通过全部三个调度变体。成功与失败因此取决于技能与具体任务需求的交互：整体比较指出调查方向，案例解释哪些决策有效、哪些失效。',9,False,'left'),
(3,(54,220,303,235),'5.2. 在构建与使用中保留正确性标准',9,True,'left'),
(3,(54,394,301,481),'生命周期视角使反馈也成为诊断依据。部署失败揭示指令不明确之处，经验证的轨迹提供成功过程的证据，替代验证器反馈指出需要检查的条件。每种构建机制都须将这些证据转化为后续执行者可用的指导。我们的结果将研究问题定位在这种转化及使用过程：哪些决策得以保留，何时仍然适用，以及执行者遵循它们时会发生什么？',9,False,'left'),
(3,(315,71,562,98),'这将报告的分数与持久技能旨在改进的行为联系起来。',9,False,'left'),
(3,(315,210,574,320),'评估技能效用与使用。SkillsBench 覆盖多样任务，SWE-Skills-Bench 研究软件工程中的技能使用 [4,5]。SkillLearnBench 评估真实任务上的持续技能生成 [6]。《从原始经验到技能使用》区分经验生成、技能提取与下游使用 [7]。我们将这些评估层面与技能学习的识别联系起来：重复结果刻画最终技能效用，任务变化检验其持续性，技能层面的案例解释不同结果背后的决策。解释的对象是执行中使用的持久技能产物。',9,False,'left'),
(3,(315,347,561,486),'我们的诊断将自进化技能的分数收益与持久技能产物承载的行为联系起来。三种方法均表现出反复出现的源任务效用，受控任务变化则揭示明显不同的复用范围。SkillEvolver 在表示、实例和需求变化下均保持正向平均收益，其他方法则表现出更局部或负面的复用效果。对照案例将差异定位到区分有效答案和维持修复约束的决策，包括执行者是否落实技能已有的检查。这使学习问题具体化：经验须转化为有用指导，且任务变化后仍须支持正确决策。因此，评估技能学习需要连接构建过程、存储内容和实际使用，基准分数记录了这一过程的结果。',9,False,'left'),
]
records=[]
for i,box,t,size,bold,align in P:
 p=d[i];r=fitz.Rect(box)+(612,0,612,0);p.add_redact_annot(r,fill=(1,1,1));p.apply_redactions(images=0,graphics=0)
 css=f'@font-face{{font-family:CN;src:url(SourceHanSerifCN-Regular.ttf)}} @font-face{{font-family:CN;font-weight:bold;src:url(SourceHanSerifCN-Bold.ttf)}} *{{margin:0;padding:0}} div{{font-family:CN;font-size:{size}pt;line-height:1.18;font-weight:{"bold" if bold else "normal"};text-align:{align}}}'
 spare,scale=p.insert_htmlbox(r,'<div>'+html.escape(t)+'</div>',css=css,archive=fitz.Archive(str(F)),scale_low=.85);assert spare>=0,(i,t,spare)
 records.append({'page':i+1,'rect':list(r),'text':t,'font_pt':size,'scale':scale})
for i,box in [(1,(325,312,551,410)),(2,(70,229,290,365))]:
 p=d[i];r=fitz.Rect(box);dst=r+(612,0,612,0);p.add_redact_annot(dst,fill=(1,1,1));p.apply_redactions(images=0,graphics=2);p.show_pdf_page(dst,clean,i,clip=r)
 records.append({'page':i+1,'restore_table_from_english':list(dst)})
p=d[4];r=fitz.Rect(612,0,1224,792);p.add_redact_annot(r,fill=(1,1,1));p.apply_redactions(images=0,graphics=2);p.show_pdf_page(r,clean,4)
canon=lambda s:''.join(c.lower() for c in unicodedata.normalize('NFKD',s) if c.isalnum())
for cp,dp in zip(clean,d):assert canon(cp.get_text())==canon(dp.get_text(clip=fitz.Rect(0,0,612,792)))
assert len(d)==5 and sum(len(list(p.annots() or [])) for p in d)==0
d.subset_fonts();out=R/'output/pdf/main-bilingual-en-zh.pdf';d.save(out,garbage=4,deflate=True);d.close();d=fitz.open(out)
for i,p in enumerate(d):p.get_pixmap(matrix=fitz.Matrix(1.45,1.45),clip=fitz.Rect(612,0,1224,792)).save(Q/f'final-zh-{i+1}.png')
target=R/'tmp/pdfs/zotero-final-comparison-20260922/最新双语-基线主旨修订-无标记-20260923.pdf';shutil.copy2(out,target)
(A/'chinese-repairs.json').write_text(json.dumps({'repairs':records,'reference_policy':'Original English bibliography on both halves.','english_final_source_used':True,'highlight_annotations':0},ensure_ascii=False,indent=2)+'\n')
files={}
for name in ['main.pdf','main-bilingual-en-zh.pdf']:
 p=R/'output/pdf'/name;x=fitz.open(p);files[name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'pages':len(x),'annotations':sum(len(list(p.annots() or [])) for p in x)}
record={'base_commit':'db9127c20','translation':{'plugin':'Zotero PDF2zh','service':'siliconflowfree','task_id':json.loads((Q/'translation-task.json').read_text())['taskId'],'result':result,'final_abstract_and_heading_aligned_manually':True},'files':files,'validation':{'english_identical_to_final_clean':True,'annotations':0},'zotero':{'status':'pending import','import_path':str(target),'baseline_key':'RTB7QH9K','superseded_key':'LUKZUDRG'}}
(A/'bilingual-zotero.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n');print(json.dumps(files,indent=2))
