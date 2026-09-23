from pathlib import Path
import fitz,json,re
R=Path(__file__).resolve().parents[3]; A=Path(__file__).parent;Q=R/'tmp/pdfs/expanded-results-20260923';F=Path('/Users/duchongyang/.cache/babeldoc/fonts')
r=json.loads((Q/'translation-result.json').read_text());tr=fitz.open(next(x for x in r['filePaths'] if 'LR_dual' in x));en=fitz.open(R/'output/pdf/main.pdf');d=fitz.open()
for i in range(len(en)):
 p=d.new_page(width=1224,height=792);p.show_pdf_page(fitz.Rect(0,0,612,792),en,i);p.show_pdf_page(fitz.Rect(612,0,1224,792),en if i==len(en)-1 else tr,i,clip=None if i==len(en)-1 else fitz.Rect(612,0,1224,792))
# Manual corrections after visual review. Coordinates refer to the Chinese half.
P=[
(0,(54,175,306,188),'摘要',9,True,'center'),
(0,(90,97,530,120),'自进化智能体技能是否在学习技能？',12,True,'center'),
(0,(54,188,306,336),'自进化智能体将经验存储在持久技能中，但任务得分提高后，哪些有用行为能够复用仍有待解释。我们通过重复配对评估与受控任务变化，诊断 SkillEvolver、SPARK 和 CoEvoSkills 的最终技能。分析区分总体效用的重复出现与逐题结果的一致性，并将净增益分解为改进和损失；进一步区分零分任务上的收益与满分执行上的损失。三种方法两次均提高源任务均分，任务变化却揭示了不同的有效范围。SkillEvolver 通过更频繁的改进和更少的原有成功损失，在各类受测变化下保持正向收益。这些结果从有用行为在源任务之外的持续性及分布刻画技能学习。',9,False,'left'),
(0,(54,336,306,354),'关键词—智能体技能，自进化，诊断评估，技能复用，泛化',8.5,False,'left'),
(0,(54,390,307,473),'持久技能为智能体提供了一条无需更新模型参数的改进路径。指令、脚本和参考资料让后续执行能够利用已有经验。SkillEvolver、SPARK 和 CoEvoSkills 分别通过基于部署的修订、经验证轨迹的蒸馏和协同进化验证来构建技能产物 [1–3]。这些产物引出了标题中的问题：系统生成得分更高的技能时，哪些有用行为得以持久保留？',9,False,'left'),
(0,(54,558,307,654),'我们提出两个相关问题。收益能否持续，在哪些任务变化下持续？重复源任务评估检验配对效用是否反复出现，冻结技能的变体评估揭示同一指导能够满足哪些需求。哪些逐题变化构成了观察到的提升？正向均值可能来自广泛的收益，也可能只是大量收益与损失抵消后的微小差额。识别这些模式，可以区分新增的有用行为与对执行者原有成功行为的干扰。',9,False,'left'),
(0,(315,258,569,352),'三种方法在两次运行中均有正向源任务平均增益，但这种一致性在任务变化后不再成立。SkillEvolver 在三类变化下均为正；SPARK 的收益取决于变化类型；CoEvoSkills 在三类变化下的平均增益均为负。实例替换时分化最明显。分解分析揭示了这些均值的组成：三种方法都能在部分变体上带来较大增益，但改进频率和原有成功受到的损失不同。',9,False,'left'),
(0,(315,541,561,558),'随后，智能体使用冻结技能执行任务 x：',9,False,'left'),
(1,(54,333,307,414),'为解释观察到的效用，我们考察其逐题分布。跨运行的一致性刻画同一批任务是否反复受益。分开统计正负分数变化，可以区分较小效应与正负抵消。按无技能分数分组，可区分零分任务上的帮助与满分执行上的损失。这些测量均以配对任务为分析单位，回答技能相关行为的不同问题。',9,False,'left'),
(1,(54,530,310,577),'我们在 SkillsBench [4] 上评估 SkillEvolver [1]、SPARK [2] 和 CoEvoSkills [3]，每种方法运行两次，并与同题无技能执行配对。同一方法两次采用相同任务集：分别为81、84和85题。',8.5,False,'left'),
(1,(54,580,306,606),'我们报告0–100分制的平均验证器奖励及平均同题差值。对包含 N 个任务的运行，配对增益为',8.5,False,'left'),
(1,(54,674,307,691),'3.2. 两次运行均有正向源任务效用',9,True,'left'),
(1,(54,692,307,728),'三种方法两次均有正向平均配对增益（表1）。SkillEvolver 为25.61和25.02分，CoEvoSkills 为10.24和9.76分，SPARK 为1.84和6.45分。',8.3,False,'left'),
(1,(315,179,570,207),'SkillEvolver 和 CoEvoSkills 的无技能分数虽变化较大，增益却相近。配对比较揭示了技能条件绝对分数可能掩盖的重复效用。',8.3,False,'left'),
(1,(315,211,569,295),'逐题结果也存在差异。SkillEvolver 每次的改进数至少为退化数的四倍；CoEvoSkills 两次均改进17题，分别退化9题和10题。SPARK 首次的改进与退化数接近，第二次为13次改进、5次退化。增益同时反映逐题变化的幅度和频率。冻结技能的变体评估检验源任务收益背后的指导能否持续适应不同需求。',9,False,'left'),
(1,(315,307,563,323),'3.3. 用任务变化检验哪些指导仍然有效',9,True,'left'),
(1,(315,473,567,585),'源任务改进不等于有效泛化。三种方法两次均提高源任务均分，变体结果却分化。SkillEvolver 保持11.94分的正向平均增益；SPARK 的 +0.65 接近零；CoEvoSkills 则低于无技能基线5.01分。SkillEvolver 的改进数多于退化数（47比20），另两种方法相反。SPARK 接近零的均值混合了方向相反的变化，并非所有影响均可忽略。SkillEvolver 同时具有更大的正向均值和更频繁的改进。',9,False,'left'),
(2,(98,275,515,287),'按无技能基线分组的变体结果',8,True,'left'),
(2,(173,286,231,301),'无技能零分',8.2,True,'center'),
(2,(245,286,314,301),'零分→正分',8.2,True,'center'),
(2,(328,286,379,301),'零分→满分',8.2,True,'center'),
(2,(395,286,452,301),'无技能满分',8.2,True,'center'),
(2,(464,286,523,301),'满分→降分',8.2,True,'center'),
(2,(54,345,568,400),'表1. 最终技能在源任务与受控变体上的效用。奖励、配对增益 Δ、正向贡献 G 与负向贡献 L 均按0–100分制报告，未四舍五入前满足 Δ=G−L。I/R/T 分别为改进、退化和持平数。P1为输入表示变化，P2为任务实例变化，P3为耦合需求变化。变体结果描述性汇总历史评估与补跑，每个技能结果均与同一变体的无技能结果配对。下半表统计从零分或满分基线出发的变化；每种方法另有10个基线得分介于两者之间的变体。',8.5,False,'left'),
(2,(54,404,304,422),'4. 净技能增益从何而来？',9,True,'center'),
(2,(54,425,305,467),'我们区分平均效用的三个组成因素：跨运行中受益任务的一致性、正负变化的平衡，以及技能在不同无技能得分水平下对执行结果的帮助或损失。',9,False,'left'),
(2,(54,479,306,496),'4.1. 均值反复为正，不代表同一批任务受益',9,True,'left'),
(2,(54,497,307,580),'匹配两次源任务运行中的任务身份，可检验正向均值有多少来自重复改进。SkillEvolver 两次分别改进27题和26题，但只有14题两次均改进；SPARK 和 CoEvoSkills 的重合数分别为3和7。在至少改进一次的任务中，两次均改进的比例分别为14/39、3/19和7/27。因此，SkillEvolver 和 CoEvoSkills 几乎不变的平均增益，也伴随着受益任务的变化。',8.8,False,'left'),
(2,(54,581,307,678),'逐题转变进一步解释了这种变化。SkillEvolver 首次改进的27题中，14题仍改进，12题变为持平，1题变为退化。SPARK 的9题分别变为3题改进、4题持平、2题退化；CoEvoSkills 的17题分别变为7题改进、9题持平、1题退化。失去原有优势，多数表现为与无技能执行持平，较少反转为负向差值。反过来，三种方法分别有10、7、10题由首次持平变为第二次改进。',9,False,'left'),
(2,(54,685,307,723),'CoEvoSkills 有5题两次均退化，另两种方法没有。这揭示了正向总体均值下反复出现的源任务损失。两次',8.5,False,'left'),
(2,(315,404,565,461),'运行提供了两种不同的观察：各方法的总体效用两次均为正，但支撑收益的任务只部分重合。这是两次运行中配对结果的比较，共同对象是任务；每次运行采用其记录的技能条件和执行结果。',9,False,'left'),
(2,(315,470,565,485),'4.2. 收益与损失可能近乎抵消',9,True,'left'),
(2,(315,485,565,514),'令 dᵢ 为技能与无技能奖励之差。为区分较小效应与正负抵消，我们将变体均值分解为正、负两项：',8.5,False,'left'),
(3,(54,71,307,113),'其他变体上损失多少，而非只有 SkillEvolver 能带来较大逐题改进。其47次改进与20次退化使正向变化占优；SPARK（32比37）与 CoEvoSkills（26比41）的关系则相反。',8.8,False,'left'),
(3,(54,125,307,142),'4.3. 帮助零分任务，保留满分结果',9,True,'left'),
(3,(54,153,307,247),'按无技能奖励分组，可具体解释这些变化。每种方法的变体集均有126次零分无技能执行。SkillEvolver 使其中42个获得正分，包括40个满分；SPARK 有30个变为满分；CoEvoSkills 有25个获得正分，包括23个满分。由零分转为正分的比例分别为33.3%、23.8%和19.8%。SkillEvolver 的优势包括：在无技能执行未获验证器奖励的变体上，更频繁地取得收益。',9,False,'left'),
(3,(54,247,307,323),'另一端点刻画无技能满分变体上的损失。SkillEvolver 的86个此类变体中，16个降分，15个降为零；SPARK 的85个中，29个降分，27个降为零；CoEvoSkills 的85个中，32个降分且均降为零。丢失满分的比例分别为18.6%、34.1%和37.6%。每种方法另有10个中间基线变体，计入总体结果，但不计入这两个端点。',8.8,False,'left'),
(3,(54,619,309,714),'各方法发表的构建流程提示了这些需求与技能学习的联系。SkillEvolver 对照成功和失败的部署，并检查对训练实例常量的依赖 [1]；SPARK 蒸馏经环境验证的执行轨迹 [2]；CoEvoSkills 通过协同进化的替代验证器提供详细修订反馈 [3]。这些机制依赖不同的证据来保留指导。行为结果使“从源实例中抽象指导”成为解释差异的具体方向，尤其是 P2 上的分化。检验这种解释，',9,False,'left'),
(3,(315,71,566,88),'需要保持评估不变，仅调整构建反馈。',9,False,'left'),
(3,(315,122,565,204),'端点分析为泛化增加了一个要求：技能应帮助遇到困难的执行者，同时保留其已有的正确决策。无技能条件使两种方向均可观测。从零分转为正分，表示记录中出现了额外的有用行为；从满分下降，则表示技能执行的分数低于其配对的满分无技能执行。只报告前一种变化，会掩盖效应的重要组成部分。',9,False,'left'),
]
for i,b,tx,sz,bold,align in P:
 rect=fitz.Rect(b);rect.x0+=612;rect.x1+=612;d[i].add_redact_annot(rect,fill=(1,1,1))
for p in d:p.apply_redactions(images=0,graphics=0)
checks=[]
for i,b,tx,sz,bold,align in P:
 rect=fitz.Rect(b);rect.x0+=612;rect.x1+=612
 css=f'@font-face{{font-family:CN;src:url(SourceHanSerifCN-Regular.ttf)}} @font-face{{font-family:CN;src:url(SourceHanSerifCN-Bold.ttf);font-weight:bold}} body{{font-family:CN;font-size:{sz}pt;line-height:1.3;margin:0;color:#000;text-align:{align};font-weight:{"bold" if bold else "normal"}}}'
 spare,scale=d[i].insert_htmlbox(rect,tx,css=css,archive=fitz.Archive(str(F)),scale_low=.75)
 assert spare>=0,(i,b,tx,spare);checks.append({'page':i+1,'rect':b,'font':sz,'scale':scale})
for y in [272.45697,299.94601]:d[2].draw_line((702.095,y),(1135.323,y),color=(0,0,0),width=.498)
def norm(t):return re.sub(r'\s+','',t)
for i,p in enumerate(d):
 assert norm(p.get_text(clip=fitz.Rect(0,0,612,792)))==norm(en[i].get_text()),i
 assert not list(p.annots() or [])
out=R/'output/pdf/main-bilingual-en-zh.pdf';d.subset_fonts();d.save(out,garbage=4,deflate=True)
for i,p in enumerate(d):p.get_pixmap(matrix=fitz.Matrix(1.3,1.3),clip=fitz.Rect(612,0,1224,792)).save(str(Q/f'zh-final-{i+1}.png'))
(A/'bilingual-repairs.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n');print('pages',len(d),'minimum repair scale',min(x['scale'] for x in checks))
