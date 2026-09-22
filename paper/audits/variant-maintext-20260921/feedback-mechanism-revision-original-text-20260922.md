# 本次重写原文


**Task Changes Separate Different Scopes of Utility**

We apply each source-task skill to controlled variants without further evolution. Input-representation changes (P1) alter names, column arrangements, or schemas; task-instance changes (P2) replace the data or instance structure; coupled-requirement changes (P3) alter or add requirements that must be satisfied together. These variations test whether a frozen skill remains useful when the executor must reinterpret inputs, recompute a solution, or accommodate new requirements.

The complete record contains 222 variants and 886 condition-level results across no skill and the three methods. Table 2 summarizes historical and recovery evaluations for 222 SkillEvolver variants and 221 each for SPARK and CoEvoSkills, pairing each skill condition with the no-skill result on the same variant.


**Source-task improvement does not imply useful generalization.**
All three methods improve mean reward on the source tasks in both runs, but their variant results diverge. SkillEvolver retains a positive mean gain of 11.94 points, SPARK is close to neutral at +0.65, and CoEvoSkills falls below the no-skill baseline at -5.01. SkillEvolver also improves more variants than it regresses (47 versus 20), whereas SPARK and CoEvoSkills show the reverse. Thus, the source-task gains of the latter two methods do not translate into a consistent advantage on changed tasks.


**Replacing the instance produces the largest divergence.**
SkillEvolver remains positive under all three changes, with its largest gain on P2 (+14.56). P2 is also where SPARK and CoEvoSkills decline most (-5.23 and -9.51). SPARK retains positive averages under representation and requirement changes, but loses its advantage when the underlying instance changes. SkillEvolver's positive results across P1–P3 indicate a broader observed scope of skill utility. CoEvoSkills' negative averages across all three changes show that its source-task benefit is particularly sensitive to reuse conditions.


**What the Evolved Skills Preserve**


**Successful skills retain guidance for choosing and checking.**
In exoplanet detection, the SkillEvolver skill supports successful detection after input columns are rearranged (P1) and after the task requires two signals (P3). The CoEvoSkills skill fails both variants: its use leads to stellar modulation being reported as the target signal, and a signal and its harmonic being treated as two separate signals. The SkillEvolver skill explicitly organizes candidate discovery, signal diagnosis, and refinement, including checks for misleading peaks. This case suggests that preserving criteria for accepting a result can be more useful under task changes than retaining a search routine alone. Both skills fail the replacement-instance P2 variant, so the successful checks address only part of this task family's variation.

A similar distinction appears in scheduling. The SkillEvolver and SPARK skills succeed on all three variants; the CoEvoSkills skill succeeds only on P3. In P1, using the CoEvoSkills skill yields an otherwise valid schedule that fails the requirement to place each operation at its earliest feasible time. The SkillEvolver skill explicitly includes this local-minimality requirement and baseline-relative repair rules. Here, successful reuse depends on preserving the task's repair conditions in the skill.


**The feedback used to build a skill helps explain its contents.**
The two methods differ in how they turn experience into revisions. SkillEvolver compares successful and failed deployments of a candidate skill, then patches guidance that was missing or misleading. Its independent audit also checks for reliance on training-instance constants (Zhang et al., SkillEvolver, 2026). These mechanisms directly target both omitted conditions and instance-specific assumptions. The rules retained in our scheduling and signal-detection skills are consistent with that emphasis: they describe what to check when reusing a procedure.

CoEvoSkills obtains detailed revision feedback from a co-evolving surrogate verifier; the ground-truth oracle returns only an opaque pass/fail signal (Zhang et al., CoEvoSkills, 2026). Consequently, discovering an omitted condition depends on the surrogate reconstructing it from the task and observed outputs. This offers a plausible explanation for a skill that covers many feasibility checks but misses a condition needed for successful reuse, as in the scheduling example. Both methods generate reusable skill packages; the relevant difference is which failure information becomes persistent guidance. Our interpretation is that feedback coverage and abstraction from the source instance help determine the scope of the resulting skill.


**Connecting utility to the evolution process.**
The results identify useful skills and differences in their applicability; the examples suggest how retained guidance relates to those differences. The next studies test where improvements enter the lifecycle, using parent-to-final comparisons and interventions on feedback, selection, skill content, and verification in SkillRevise, SkillHone, and SkillOpt.

## 中文对照：新增解释的核心

SkillEvolver 对比使用候选技能后的成功与失败执行，再修补缺失或具有误导性的指导，并由独立审查检查技能是否依赖训练实例中的常量。这些机制针对遗漏的条件和实例特有的假设。我们检查的调度及信号检测技能中保留的规则，与这种设计取向一致。

CoEvoSkills 的详细修订反馈来自共同演化的代理验证器，真实评测只返回不透明的通过或失败信号。因此，发现遗漏条件依赖代理验证器从任务和输出中重新推导这些条件。这为调度案例中“覆盖许多可行性检查，却遗漏复用所需条件”的现象提供了一种可能解释。两种方法都生成可复用技能；讨论的区别是哪些失败信息最终变成了持久指导。正文将反馈覆盖及对源实例的抽象作为解释，而非已经验证的因果结论。
