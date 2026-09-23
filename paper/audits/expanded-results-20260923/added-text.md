# Revised diagnostic section (English source)

```latex
\section{What Produces the Net Skill Gain?}
\label{sec:skill-reuse}

We distinguish three contributors to mean utility: agreement on which tasks improve across runs, the balance between positive and negative changes, and whether the skill helps or harms execution at different no-skill reward levels.

\subsection{Recurring Means Do Not Imply the Same Tasks Improve}

Matching task identities across the two source-task runs reveals how much of the positive mean comes from recurring improvements. SkillEvolver improves 27 tasks in run 1 and 26 in run 2, but only 14 improve in both. The corresponding overlaps are three for SPARK and seven for CoEvoSkills. Across tasks that improve at least once, these counts are 14 of 39, three of 19, and seven of 27. Thus, the nearly unchanged mean gains of SkillEvolver and CoEvoSkills coexist with changes in which tasks benefit.

The transitions clarify this variation. Of SkillEvolver's 27 first-run improvements, 14 remain improvements, 12 become ties, and one becomes a regression. SPARK's nine first-run improvements become three improvements, four ties, and two regressions. CoEvoSkills' 17 become seven improvements, nine ties, and one regression. Losing an observed advantage most often means becoming tied with the no-skill execution, rather than reversing the sign. Conversely, ten, seven, and ten tasks move from a first-run tie to a second-run improvement for SkillEvolver, SPARK, and CoEvoSkills, respectively.

CoEvoSkills also regresses on five of the same tasks in both runs; neither other method has a task that regresses twice. This identifies a recurring source-task cost within a positive overall mean. The two runs therefore supply two distinct observations: each method has positive aggregate utility twice, while the task identities supporting that utility are only partly shared. These are comparisons of paired outcomes across runs; the shared object is the task, with each run using its recorded skill condition and execution.

\subsection{Benefits and Losses Can Nearly Cancel}

To distinguish small effects from cancellation, let $d_i=r_i^{\mathrm{skill}}-r_i^{\mathrm{no\text{-}skill}}$. We separate the variant mean into positive and negative contributions:
\begin{equation}
G=\frac{100}{N}\sum_i\max(d_i,0),\quad
L=\frac{100}{N}\sum_i\max(-d_i,0).
\end{equation}
The paired gain is $\Delta=G-L$. Both terms use all evaluated variants as their denominator, so they account for the frequency and magnitude of score changes together.

SkillEvolver contributes 18.89 points of improvement against 6.95 points of loss, leaving the observed $+11.94$ gain. SPARK contributes 13.73 positive points and 13.08 negative points. Its $+0.65$ mean therefore masks substantial movement in both directions. CoEvoSkills contributes 10.98 positive points, but its 15.98-point loss outweighs them. Its negative average includes useful changes on some variants alongside a larger cost elsewhere.

The conditional magnitudes further distinguish these patterns. Among improved variants, the average increase is 89.23 points for SkillEvolver, 94.82 for SPARK, and 93.30 for CoEvoSkills. Among regressed variants, the average loss is 77.16, 78.15, and 86.16 points. All three methods can produce large gains where they help. Their overall separation comes from how often those gains occur and how much is lost on other variants, rather than SkillEvolver alone producing large individual improvements. Its 47 improvements and 20 regressions give positive changes more weight; the balance reverses for SPARK (32 versus 37) and CoEvoSkills (26 versus 41).

\subsection{Helping Zero-Reward Tasks and Preserving Full-Reward Tasks}

Conditioning on the no-skill reward gives the changes a concrete interpretation. Each method's variant set contains 126 zero-reward no-skill executions. SkillEvolver raises 42 of them to positive reward, including 40 to full reward. SPARK raises 30 to full reward, and CoEvoSkills raises 25 to positive reward, including 23 to full reward. The respective rates of moving beyond zero are 33.3\%, 23.8\%, and 19.8\%. SkillEvolver's advantage thus includes more frequent gains on variants where the executor receives no verifier credit without the skill.

The other endpoint measures losses on variants with a full-reward no-skill execution. Among SkillEvolver's 86 full-reward no-skill variants, 16 fall below full reward, including 15 that fall to zero. SPARK lowers 29 of 85, including 27 to zero; CoEvoSkills lowers 32 of 85, all to zero. The rates of losing full reward are 18.6\%, 34.1\%, and 37.6\%. Each method also has ten intermediate-baseline variants, which remain included in the aggregate results but are outside these endpoint counts.

These two directions explain why counting newly successful tasks alone is insufficient. SPARK and CoEvoSkills both turn many zero-reward cases into full-reward outcomes, yet lose full reward on almost as many or more baseline successes. SkillEvolver combines the highest rate of gains from zero with the lowest rate of losses from full reward. Its broader utility is expressed in both acquiring a benefit and preserving outcomes that the executor already achieves.
```

# Large table

Six source-task runs plus nine P1/P2/P3 rows; no combined all-variant row. The lower panel reports baseline-conditioned counts. All measurements are derived from the existing audited records.
