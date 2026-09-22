# Skill-reuse analysis and manuscript placement

## Author request and scope

Rewrite the former “Tracing the Source of Transfer” subsection at a more general
analytical level, using the previously recommended paper as a writing reference,
and check its place in the manuscript. Preserve the author's source-only review:
no PDF, translation, comparison PDF or Zotero update in this revision.

## Writing reference

Wang et al., *Reinforcement Learning for Self-Improving Agent with Skill Library*,
ACL 2026, DOI 10.18653/v1/2026.acl-long.69.

- Official metadata: https://aclanthology.org/2026.acl-long.69/
- Full paper: https://aclanthology.org/2026.acl-long.69.pdf
- Read on 2026-09-22: Sections 4.2–4.4, especially the skill-usage analysis and
  its pointers to execution examples in Appendix G and skill examples in Appendix H.

The writing pattern used here is to organize the main text around an analytical
question and observed behavior, with detailed examples supporting the analysis.
SAGE's ablations support its own mechanism claims; its findings are not evidence
for this manuscript's methods. No text, numerical result, or causal conclusion
is imported from SAGE. It is a writing reference, not a new manuscript citation.

## Placement decision

Keep the SkillsBench experiments after Problem Formulation and before Identifying
Retained Skill Effects. The progression is utility on standard tasks, behavioral
scope on variants, interpretation of reusable content, then the complementary
retention and lifecycle intervention studies. The new subsection stays directly
after the variant results, where its evidence is introduced.

Rewrite the introduction's study overview to explain these complementary roles
and the two groups of methods. Rename the subsection to “Skill Reuse under Task
Variation” and link it explicitly to the subsequent retention and attribution
sections. Do not present the trace inspection as an intervention identifying the
cause of the aggregate method difference.

## Evidence and edit boundaries

- Aggregate observations: `../full-variant-records-20260922/statistics.json` and
  the unchanged standard-task table.
- Qualitative content: `case-evidence.json`, including the inspected SkillEvolver
  and CoEvoSkills skill files, exoplanet execution excerpts, scheduling execution
  excerpts and the scheduling verifier predicates.
- Scope wording remains “inspected” and “examined ... cases”; no benchmark-wide
  content coding or causal ablation is claimed.
- The old numerical examples remain in `case-evidence.json` and Git history.
- No numbers, table rows, experiment records or other mechanism-study content
  are changed in this writing revision.

## Replacement text

### Skill Reuse under Task Variation

SkillEvolver's positive gains across P1–P3 indicate that the utility of its frozen skills extends beyond the source instances. The weaker or negative variant gains of SPARK and CoEvoSkills show that improvement on the original task and usefulness after task changes are distinct properties. This makes the content preserved during reuse central to interpreting the results.

Two complementary forms of content emerge from the inspected skill files and execution traces: diagnostic rules for choosing and revising a procedure, and constraints for checking the resulting output. In the examined SkillEvolver cases, these rules remain explicit while input handling and solution construction adapt to the variant. Corresponding failure traces reveal that reusing a procedure can preserve much of the workflow while missing a decision or constraint needed for correctness. These observations suggest that reusable decision rules, including when they apply and how their outputs should be checked, are a useful unit of analysis for skill transfer.

Within the lifecycle audit, variant performance characterizes the scope of observed utility. The subsequent mechanism studies examine persistence under fresh deployment and the contributions of feedback, revision, selection, skill content, and evaluation.

### 中文对照（供作者审阅；未重新生成双语 PDF）

SkillEvolver 在 P1–P3 上均取得正向收益，表明其冻结技能的效用能够延伸到原始任务实例之外。SPARK 和 CoEvoSkills 在变体上的收益较弱或为负，说明原任务上的改进与任务变化后的有效性是不同的性质。因此，理解这些结果，需要进一步考察技能在复用时保留了什么内容。

对所检查的技能文件和执行轨迹的分析，呈现出两类互补内容：指导过程选择与调整的诊断规则，以及检验输出是否正确的约束。在所分析的 SkillEvolver 案例中，这些规则得到明确保留，而输入处理和解的构造随变体调整。对应的失败轨迹表明，复用已有过程时，即使保留了大部分工作流程，也可能遗漏决定正确性的判断或约束。这些观察提示，可复用的决策规则及其适用条件和输出检查方式，是分析技能迁移的一个有用单位。

在本文的生命周期审计框架中，变体表现刻画了已观察到的技能效用能够延伸到什么范围。后续机制研究进一步检验这种改进在重新执行时能否保持，并分析反馈、修订、选择、技能内容与评估各自的作用。
