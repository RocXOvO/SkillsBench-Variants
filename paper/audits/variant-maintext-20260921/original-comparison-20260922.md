# 最新稿与最初 Overleaf 原版对比（2026-09-22）

基线：Git `121a6182b`，其 `main.tex` 与本机最初 Overleaf 源码逐字节一致。不是最早另行提供的 `PDF/main.pdf`，也不是上一轮修改稿。

## 本轮摘要修改

将两组方法及实验操作的枚举合并为围绕全文研究问题的一句概述：

> We combine repeated evaluations, controlled task variations, and lifecycle interventions to examine whether improvements from skill evolution persist and transfer, and to trace their origins to feedback, revision, selection, skill content, and evaluation.

中文：我们结合重复评估、受控任务变化和生命周期干预，考察技能进化带来的改进能否持续并迁移，并追溯反馈、修订、选择、技能内容及评估在其中的作用。

本轮没有调整正文实验分数、逐题选源或实验运行。

## 相对最初原版的累计内容差异

| 最新稿位置 | 内容变化 | 红色标记 |
|---|---|---|
| 第1页摘要 | 将原版方法枚举替换为改进的保持、迁移与来源的整体研究概述 | 替换句子 |
| 第1页引言 | 新增三个方法的评估与技能/轨迹分析概述 | 新增段落 |
| 第2页问题定义末尾 | 将 “The next two sections…” 改成 “The following experiments…” | 替换句子；批注保留原文 |
| 第2–3页实验部分 | 新增 SkillsBench 设置、配对指标、每方法两次标准任务结果、独立变体结果 | 整个新增实验部分 |
| 第3页表1、表2 | 新增六次标准任务结果和三种方法的变体结果 | 表头、数值与表注 |
| 第3页迁移归因 | 新增系外行星周期检测和调度案例分析 | 两个案例段落及标题 |
| 第7页结论 | 新增变体结果概括和轨迹归因总结 | 两句新增内容 |
| 第8页参考文献 | 新增 SkillEvolver 和 SPARK 条目 | 两条文献 |

共29个 PDF 高亮注释，采用红色 #ff6666、透明度0.35，并附中文说明。双语阅读版左侧英文采用同样标记。图表移动、自动编号和引用年份字母的变化不整块涂色。

## 累计排版差异

删除导致大块空白的 FloatBarrier，提前声明浮动图表；压缩生命周期图的返回箭头；调整证据主张表的浮动选项。最新稿共8页，两张新增实验表位于第3页。模板、纸张、字号及页边距保持一致。

## 核对

- 基线和最新 PDF 的结构预检均 PASS。
- 已检查8页缩略总览和第1、2、3、7、8页高亮细节；正文与表格无溢出。
- 高亮 PDF 与清洁 PDF 的逐页提取文本相同。
- 正文语义对比除上表列出的累计改动外保持一致；原有图表仅改变放置与返回箭头形状。
- 当前 LaTeX 编译无未定义引用、无 Overfull；实验设置首行存在一个 Underfull hbox 警告。
