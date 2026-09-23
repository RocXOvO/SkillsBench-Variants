# 本轮重写原文

以下为当前 LaTeX 英文原文。完整变更见同目录补丁。

## 摘要与引言

```latex
\begin{abstract}
Self-evolving agent skills turn execution experience into persistent instructions and code, but improved performance on the source task leaves open what has been learned. We study this question through repeated standard-task evaluations, controlled task variations, and inspection of the resulting skills and their use. Our diagnosis distinguishes source-task utility from usefulness under changes to input representation, task instances, and requirements. We examine SkillEvolver, SPARK, and CoEvoSkills, connecting their observed reuse patterns to the decision rules preserved in their skills and the feedback used during skill construction. The results reveal different scopes of generalization despite positive source-task gains, and motivate evaluating skills by how they guide decisions when the task changes.

\end{abstract}

\begin{keywords}
Agent skills, self-evolution, diagnostic evaluation, skill reuse, generalization
\end{keywords}

\section{Introduction}

Persistent agent skills store instructions, scripts, and references that an executor can reuse across tasks. Skill-generation and evolution methods turn execution experience into these external artifacts without changing the executor's model parameters. SkillEvolver refines skills from their deployment outcomes, SPARK distills environment-verified trajectories, and CoEvoSkills jointly evolves skills and a surrogate verifier~\cite{zhang2026skillevolver,zhou2026spark,zhang2026coevoskills}. Their common goal is to make experience useful beyond the attempt that produced it.

Success on the source task does not reveal the scope of that usefulness. A skill can help by encoding a procedure that adapts to new inputs, or by preserving choices that happen to work on one instance. Both can raise a benchmark score. The distinction becomes visible when the executor must reinterpret an input, solve a replacement instance, or satisfy an additional requirement while using the same skill. These changes test what the artifact preserves from experience and what the executor must still infer.

We investigate this distinction as a diagnostic study of skill reuse. We first measure each method's gain over a same-task no-skill baseline in two standard-task runs. We then freeze the skills and examine their utility under changes to representation, instances, and requirements. Finally, we inspect contrasting examples to connect successful and unsuccessful reuse to the guidance expressed in the skills. This sequence moves from whether a skill helps to where it helps and what its contents suggest about the difference.

The resulting picture differs across methods. All three show positive paired gains in both standard-task runs. Under task variation, SkillEvolver retains positive average gains across all three change types, SPARK's gains depend on the type of change, and CoEvoSkills' average gains reverse sign. Instance changes produce the clearest separation. Thus recurring source-task gains and generalization describe different properties of an evolved skill.

The case evidence makes this distinction concrete. In signal detection, selecting a strong candidate is insufficient when the signal can be confused with background variability or a harmonic. In scheduling, a feasible output can still violate the task's repair rules. Successful reuse in these examples accompanies skills that preserve criteria for choosing and checking a result. We interpret these differences in light of the methods' feedback and skill-construction procedures.

This paper contributes a diagnosis of skill learning through three complementary forms of evidence:
\begin{itemize}
    \item \textbf{Repeated utility measurement.} Six standard-task runs establish the observed paired benefits of SkillEvolver, SPARK, and CoEvoSkills on their evaluated tasks.
    \item \textbf{Task-variation analysis.} Representation, instance, and requirement changes expose different scopes of frozen-skill usefulness across the recorded variant evaluations.
    \item \textbf{Skill-level interpretation.} Contrasting reuse examples connect outcomes to preserved decision criteria and motivate an explanation based on feedback coverage and abstraction from the source instance.
\end{itemize}
```

## 后半篇

```latex
\section{Explaining the Observed Scope of Reuse}
\label{sec:skill-reuse}

The variant results locate differences in skill utility. We examine two task families to make those differences interpretable: signal detection, where the executor must choose between plausible candidates, and scheduling, where the output must satisfy specific repair rules. These cases connect observed outcomes to the guidance preserved in the frozen skills.

\subsection{Distinguishing a Candidate from a Valid Answer}

In exoplanet detection, the SkillEvolver skill supports successful detection after input columns are rearranged (P1) and after the task requires two signals (P3). The CoEvoSkills skill fails both variants: its use leads to stellar modulation being reported as the target signal, and a signal and its harmonic being treated as two separate signals. Both skills fail the replacement-instance P2 variant.

The difference is visible in what the skills ask the executor to check. SkillEvolver separates candidate discovery, signal diagnosis, and refinement. Its guidance addresses misleading peaks, transit-like durations, and harmonic relationships. CoEvoSkills also includes validation, including phase-fold, odd/even, and residual checks, but its use in these variants does not resolve the misleading candidates. The presence of a checking routine is therefore less informative than whether its criteria distinguish the alternatives that matter on the changed task. SkillEvolver's successful P1 and P3 deployments illustrate that distinction, while its P2 failure shows that those criteria do not solve every new instance.

\subsection{Preserving the Rules That Define a Correct Repair}

In scheduling, the SkillEvolver and SPARK skills succeed on all three variants; the CoEvoSkills skill succeeds only on P3. In P1, using CoEvoSkills yields an otherwise feasible schedule that fails a required local-minimality check on the baseline-relative repair. Feasibility checks alone do not capture this local-minimality requirement.

The SkillEvolver skill explicitly retains local minimality and baseline-relative repair rules. These rules specify how an acceptable repair differs from an arbitrary feasible schedule, and remain relevant after the input names or scheduling instance change. The CoEvoSkills skill covers several structural and feasibility checks, yet the failed deployment misses the decisive repair condition. The contrast concerns which correctness conditions survive in the reusable guidance. SPARK's success across the same three variants also shows that this form of successful reuse is not exclusive to one method.

\subsection{Construction Feedback and Skill Content}

The construction procedures offer an interpretation of these skill-level differences. SkillEvolver compares successful and failed deployments of a candidate skill and patches missing or misleading guidance. Its independent audit also checks reliance on training-instance constants~\cite{zhang2026skillevolver}. This exposes failures in using the skill and encourages rules that a later executor can apply to a different input. The scheduling and signal-detection skills reflect that emphasis by retaining criteria for checking a repair or discriminating between candidate signals.

SPARK grounds skill distillation in environment-verified trajectories, preserving execution evidence, checks, and lessons~\cite{zhou2026spark}. Its scheduling result shows that such evidence can support successful reuse. Its mixed aggregate profile raises a separate question about abstraction: a verified execution supplies evidence for what worked on the source task, while changed instances require determining which choices should be retained and which should be recomputed. The observed decline on P2 makes that distinction especially relevant to interpreting its results.

CoEvoSkills obtains detailed revision feedback from a co-evolving surrogate verifier, while the ground-truth oracle returns an opaque pass/fail signal~\cite{zhang2026coevoskills}. This makes the surrogate's coverage of correctness conditions relevant to the guidance retained in the skill. This provides a plausible account of the scheduling failure: the skill preserves many checks, but successful reuse still depends on a condition those checks did not enforce in that deployment. Across the cases, feedback coverage and abstraction from the source instance are candidate explanations for the different scopes of utility.

\section{Implications for Reusable Skill Learning}

\subsection{Average Gain and Improvement Frequency}

SPARK illustrates a distinction between the size and frequency of benefits. Its overall variant mean is slightly positive even though regressions outnumber improvements. A near-zero aggregate therefore does not mean that the skill has no effect: beneficial and harmful changes offset one another. SkillEvolver's positive mean is accompanied by more improvements than regressions, whereas CoEvoSkills has both a negative mean and more regressions. These outcome profiles describe whether a skill's aggregate utility reflects broad benefit among changed outcomes or a balance of opposing changes.

\subsection{Implications for Skill Construction and Evaluation}

The cases suggest a concrete target for skill construction: preserve how to recognize a valid result, as well as how to produce a candidate. A useful skill helps the executor decide when its procedure applies, what must be adapted, and which checks must hold before accepting the output. The feedback-based account connects this target to the methods' construction procedures as an interpretation of the observed patterns.

Evaluation should correspondingly report paired source-task utility, examine the same frozen artifact under distinct task changes, and inspect cases where the outcomes diverge. The three probes describe a profile of applicability: passing one change does not substitute for checking another. Reporting that profile alongside improvement and regression counts exposes behavior that a single average hides. It also makes the learning question concrete: which decisions remain useful when the source task no longer supplies the same inputs or demands the same output?

\section{Related Work}

\noindent\textbf{Learning persistent skills from experience.}
SkillEvolver, SPARK, and CoEvoSkills make experience persistent through different construction loops: deployment-grounded revision, verified-trajectory distillation, and co-evolutionary verification, respectively~\cite{zhang2026skillevolver,zhou2026spark,zhang2026coevoskills}. These methods motivate our focus on the artifact delivered to a later executor. We study how that artifact's usefulness changes after its source task is varied, and interpret the resulting behavior through its retained guidance.

\noindent\textbf{Evaluating skill utility and use.}
SkillsBench evaluates skill utility across diverse tasks, while SWE-Skills-Bench studies skill use in software engineering~\cite{li2026skillsbench,han2026sweskillsbench}. SkillLearnBench evaluates continual skill generation on real-world tasks~\cite{zhong2026skilllearnbench}. From Raw Experience to Skill Consumption separates experience generation, skill extraction, and downstream consumption~\cite{huang2026rawexperience}. Our study complements these evaluations by connecting repeated source-task outcomes with controlled variations of the task and skill-level examples. The central object is the scope of usefulness of a frozen skill, rather than its score on the source task alone.

\section{Conclusion}

We examine what self-evolving agent skills preserve through repeated standard-task evaluations, task variation, and inspection of skill reuse. SkillEvolver, SPARK, and CoEvoSkills all yield positive source-task gains in both runs, but their variant results differ substantially. SkillEvolver has the broadest observed generalization profile, remaining positive under representation, instance, and requirement changes. SPARK's benefit depends on the change type, while CoEvoSkills' averages become negative. The inspected examples associate successful reuse with guidance for selecting valid results and preserving task-specific correctness rules. Together, these findings show why diagnosing skill learning requires examining how a frozen artifact guides behavior after the task changes.
```
