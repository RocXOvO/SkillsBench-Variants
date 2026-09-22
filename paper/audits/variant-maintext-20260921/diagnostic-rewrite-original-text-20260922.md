# Diagnostic-theme revision: exact English prose

The manuscript wording is reproduced below. Only LaTeX formatting is converted; tables and the unchanged equation remain in the PDF.

## Introduction: replacement study overview

We organize the evidence as a diagnosis of utility, behavioral scope, and gain attribution. Standard-task evaluations of SkillEvolver, SPARK, and CoEvoSkills first establish the observed utility of completed artifacts across two runs. Controlled task changes then reveal different scopes of usefulness, and artifact and trace inspection examines the decisions preserved during reuse. This motivates the next diagnostic step: locating an improvement in the artifact's evolution history. Complementary studies of SkillRevise, SkillHone, and SkillOpt use retention tests and lifecycle interventions to examine trace-conditioned revision, history-based iterative honing, and validation-gated editing. Each study addresses a specific part of the identification question.

## Diagnosing the Scope of Skill Utility

The first diagnostic question is where a completed skill is useful. A positive source-task result can arise from content that applies across instances or from a procedure fitted to the original task. We distinguish these possibilities by first examining paired utility in two standard-task runs, then deploying frozen skills under three forms of task variation. Inspection of skill content and execution traces connects the resulting utility profiles to decisions made during deployment.

### Experimental Setup

We evaluate SkillEvolver [zhang2026skillevolver], SPARK [zhou2026spark], and CoEvoSkills [zhang2026coevoskills] on SkillsBench [li2026skillsbench], with two runs per method. Each run pairs an execution using the generated or evolved skill with a no-skill execution of the same task. Both runs of each method use the same task set: 81 tasks for SkillEvolver, 84 for SPARK, and 85 for CoEvoSkills.

We report mean verifier reward on a 0–100 scale and the mean within-task difference between the skill and no-skill conditions. For a run with $N$ tasks, the paired gain is

[The unchanged paired-gain equation is in the manuscript.]

We also count tasks with positive, negative, and zero differences.

### Source-Task Gains Recur across Runs

All three methods have positive mean paired gains in both runs (Table 1). SkillEvolver gains 25.61 and 25.02 points, and CoEvoSkills gains 10.24 and 9.76 points. For both methods, the aggregate advantage is similar across runs even though absolute rewards change substantially. SkillEvolver's no-skill mean rises from 30.20 to 37.32, while CoEvoSkills' falls from 42.21 to 23.54. A comparison of skill-condition scores alone would obscure this pattern. The within-task contrast locates the observed benefit relative to what the executor achieves without the artifact in each run.

Task-level outcomes clarify how those means arise. SkillEvolver improves 27 tasks and regresses six in run 1, followed by 26 improvements and three regressions in run 2. CoEvoSkills improves 17 tasks in each run, with nine and ten regressions. SPARK has positive gains of 1.84 and 6.45 points, but its first run has nearly balanced improvements and regressions (nine versus eight), whereas the second has 13 improvements and five regressions. A repeated positive mean can therefore coexist with different concentrations of benefit and harm.

The common finding is a recurring aggregate benefit on the source tasks, with heterogeneous effects across individual tasks. The next diagnostic question is which parts of this usefulness survive task changes. The next comparison holds the source skill fixed and changes the task, so that the executor must reuse existing content rather than receive a skill evolved for the new instance.

### Task Changes Separate Different Scopes of Utility

**Probing what must change during reuse.**
We apply each source-task skill to controlled variants without further evolution. Input-representation changes (P1) modify names, column arrangements, or schemas. The executor must recover the same semantic roles from a different presentation. Task-instance changes (P2) replace the data or instance structure, requiring the procedure to operate on new values and relationships. Coupled-requirement changes (P3) alter or add requirements that must be satisfied together, requiring the executor to adapt its solution while preserving the relevant constraints. These probes separate input interpretation, instance-specific computation, and requirement handling; they are not successive difficulty levels.

The complete record contains 222 variants and 886 condition-level results across no skill and the three methods. Table 2 summarizes historical and recovery evaluations for 222 SkillEvolver variants and 221 each for SPARK and CoEvoSkills. Each method's utility is measured against the no-skill result on the same variant. The paired contrast measures utility under the changed task; P1–P3 locate its behavioral scope.

**Source-task gains have different extensions.**
The positive source-task results lead to three distinct variant profiles. SkillEvolver increases mean reward from 41.87 to 53.81, a gain of 11.94 points, with 47 improvements and 20 regressions. Its skill utility extends beyond the instances on which the artifacts were produced. SPARK's average gain is much smaller, at 0.65 points, with 32 improvements and 37 regressions. CoEvoSkills changes from 41.61 to 36.60, a decline of 5.01 points, with 26 improvements and 41 regressions. Thus, a positive result on the original tasks can accompany positive, nearly neutral, or negative average utility after task variation. Source-task success alone does not characterize the scope of a skill.

**Instance changes expose the clearest separation.**
SkillEvolver remains positive under all three probes: 11.85 points on P1, 14.56 on P2, and 9.72 on P3. Improvements outnumber regressions within each category, at 15 versus seven, 15 versus six, and 17 versus seven. Its positive overall result is therefore supported across all three types of change rather than being concentrated in one category. The largest gain occurs on P2, where the source instance has been replaced and the executor must recompute a solution using the new task data.

P2 also produces the largest average decline for the other two methods: 5.23 points for SPARK and 9.51 points for CoEvoSkills. This shared location of their largest decline makes instance changes particularly informative for the diagnosis. The relevant question is whether a source artifact helps the executor reconstruct the procedure for a new instance, rather than merely repeat an execution that worked before. SkillEvolver shows the strongest positive utility profile on this probe.

**Representation and requirements reveal different sensitivities.**
SPARK gains 2.00 points on P1 and 4.53 on P3 despite its negative P2 result. Its overall mean consequently combines benefits under some changes with losses under another. CoEvoSkills declines on both P1 and P3, by 3.59 and 2.42 points, so its negative overall result extends across the three probes. These profiles explain why a single aggregate variant score is an incomplete description: handling renamed inputs, instantiating a procedure on new data, and satisfying coupled requirements are different demands on skill reuse. The breakdown locates the observed strengths and failures without treating all task changes as interchangeable.

**Benefit magnitude and benefit frequency differ.**
SPARK's positive mean coexists with more regressions than improvements. Reward magnitudes determine the mean, whereas the sign counts describe how often the outcome changes in each direction. Both are needed to interpret utility. Moreover, 155 of 222 SkillEvolver variants, 152 of 221 SPARK variants, and 154 of 221 CoEvoSkills variants tie with their no-skill counterparts. Most evaluations therefore preserve the baseline reward, and the aggregate differences arise from a minority of changed outcomes. A reward tie does not reveal whether the executor ignored the skill or followed a different trajectory to the same score. This motivates inspecting how skill content enters execution, rather than inferring skill use directly from the final reward.

### Tracing Utility to Decisions Made during Reuse

The variant profiles establish where skill utility is observed. To examine how that utility is expressed, we inspect the source artifacts and execution traces in the signal-detection and scheduling cases. The analytical unit is a decision that connects stored content to a changed task: recognizing the inputs, choosing or revising an operation, and checking the resulting output. This separates the procedure available in the artifact from the behavior actually produced when the executor applies it.

**Diagnostic rules preserve criteria while allowing new solutions.**
The inspected SkillEvolver signal-detection artifact separates candidate discovery, diagnosis, and local refinement. Its rules specify when a candidate requires further checking and when the search should be adjusted. In the P1 and P3 executions, the executor uses these checks to distinguish competing explanations and revise the search before choosing an output. The reusable element is the criterion for accepting a candidate; the candidate itself and the numerical search settings are recomputed from the changed input.

This distinction matters because a stored action sequence can remain executable while the reason for trusting its result has changed. In the corresponding CoEvoSkills failure traces, executing the period-search routine does not reliably resolve the competing signal interpretations. The contrast directs attention to the checks between operations: whether an intermediate result is accepted, rejected, or used to trigger another search. The table records an outcome difference; the trace shows the decision at which the executions diverge.

The same task family also exposes a boundary of this behavior: both skills fail on the replacement-instance P2 variant. Successful reuse under a changed representation or requirement does not ensure success when the underlying signal changes. This within-family contrast makes the scope question concrete. The diagnostic rules help resolve some changed executions, while the replacement instance remains a failure even with those rules available.

**Output constraints preserve the task contract.**
The scheduling case exposes a complementary form of reusable content. The inspected SkillEvolver artifact states repair constraints relative to the supplied instance and baseline schedule. This permits the concrete schedule to change while preserving the conditions that make the repair valid. The corresponding executions handle changed inputs and requirements while retaining those checks. SkillEvolver and SPARK both succeed on the three inspected scheduling variants, showing that this behavior is not exclusive to a single method.

The CoEvoSkills P1 failure is more localized: the output satisfies other structural and policy checks but violates the required local-minimality condition. The diagnostic value lies in this separation. Producing a largely valid schedule and preserving the full repair contract are different outcomes, even when they arise from similar high-level workflows. Examining the failed predicate connects the reward change to a specific behavioral requirement rather than treating the entire execution as an undifferentiated failure.

**From behavioral evidence to lifecycle attribution.**
Across these cases, successful reuse combines preserved decision criteria with task-dependent execution. Input names, search parameters, and constructed solutions can change, while diagnostic checks and correctness constraints remain relevant. This provides a concrete interpretation of the behavior sought by the variant probes: a useful skill supplies guidance for recomputing a solution, including how to recognize and correct an unsuitable intermediate result. SkillEvolver's positive profile across P1–P3 is consistent with this pattern, and the inspected traces show instances in which the pattern is expressed.

The diagnostic sequence now separates three objects: the utility of a completed artifact, the scope of that utility under task changes, and the decisions observed during its use. Locating an improvement in the evolution process requires an additional contrast: the actual parent artifact against the adopted final artifact, followed by interventions on the feedback, selection, content, or verifier involved. The following studies apply these contrasts to SkillRevise, SkillHone, and SkillOpt. They move from identifying useful behavior to testing whether it is retained and which lifecycle components produce it.

## Conclusion: replacement first paragraph

We diagnose where the gains from self-evolving persistent skills reside and how far they extend. All three methods in the standard-task evaluations have positive paired gains in both runs, but task variation separates their utility profiles. SkillEvolver remains positive across representation, instance, and requirement changes; SPARK combines gains on two probes with a decline on instance changes; CoEvoSkills declines on all three. The inspected traces identify decision criteria and correctness checks expressed during successful reuse. Complementary lifecycle interventions show that adopted artifact components can change behavior, selected outcomes can disappear under fresh deployment, and fixed outputs can receive different verdicts under different verifiers. Together, these findings distinguish useful artifacts, their behavioral scope, and the processes that produce or measure their apparent improvement.
