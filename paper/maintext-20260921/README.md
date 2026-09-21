# 本地论文源码与正文实验合入

本目录可独立编译。主文件为 `main.tex`，使用从用户 Overleaf 项目复制的 AAAI 2027 模板。

```bash
cd /Users/duchongyang/Documents/ICLR/paper/maintext-20260921
make
```

生成 `build/main.pdf`。也可直接运行：

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

## 文件

- `main.tex`：完整论文正文，已同步修改摘要、引言、实验设置和结论。
- `skillsbench-standard.tex`：正文标准任务结果、配对指标和主表。
- `skillsbench-variants.tex`：正文变体设计、具体结果分析及例示表。
- `skillsbench-records.tex`：附录中的结果来源、历史冲突和修复细节。
- `references.bib`、`aaai2027.sty`、`aaai2027.bst`：参考文献和模板。
- `evidence-map.json`、`paper-selection.json`、`variant-results-paper-r6.md`、`evidence/`：已核验的实验记录与逐格视图。
- `changes.diff`、`integration-changes.json`、`validation.json`：相对 Overleaf 原始正文的修改、合入说明和编译核验记录。

## 来源版本

源项目为 `https://www.overleaf.com/project/6aafd725b37acd9be4c6226b`，由用户提供链接并在桌面 Edge 中打开。ZIP 下载被 Edge 阻止后，通过编辑器全选复制四份完整文件，在本机以 UTF-8 保存；每个文件的长度和文本指纹均与浏览器复制内容一致。原始文件和 SHA-256 记录保存在 `../overleaf-original-20260921/`，本次未修改在线项目。

该 Overleaf 版本编译为 7 页，正文研究 SkillRevise、SkillHone 和 SkillOpt；它与此前本机 `PDF/main.pdf` 的 8 页 SkillOpt-Lite/SkillRevise 版本不同。本目录以用户提供的 Overleaf 源码为底稿。此前本机 PDF 和 2026-09-20 的附录合并版均保留。

## 当前 ARS 修订 r2（2026-09-21）

正文主表统一展示五组有确定汇总的结果，取消后端分块标题。SPARK 只采用服务器原生的 Rep01 与 Rep02，均为相同84题、OpenLux、请求GPT-5.5 medium、评测超时倍率0.5：

- Rep01：17.82 → 19.66，配对增益+1.84点，9提升/8退步/67持平。
- Rep02：14.37 → 20.81，配对增益+6.45点，13提升/5退步/66持平。

本机迁移到服务器的 SPARK 86题/修正85题记录已从论文采用值撤下，原始资料保留。336份逐臂结果的奖励与哈希均核验一致。原始汇总、生成来源与复算在 `evidence/spark-server-runs-r2/`。

CoEvoSkills 第二次空白行移出主表；85题已覆盖、四题存在冲突、最终选源待定的状态留在附录，未按较新或较高分选择。

摘要、引言和结论中的五组增益范围为1.84–25.61点。变体正文和原有实验数据保持上一版内容。9页PDF编译无警告、逐页检查通过。

`revisions/ars-r2/` 保存修改前稿、差异、修改清单和核验记录。当前PDF：`../../output/pdf/main-results-integrated-20260921.pdf`。在线 Overleaf 和服务器实验均未修改。
