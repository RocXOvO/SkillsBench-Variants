# Experiments on SkillsBench


## Experimental Setup

We evaluate SkillEvolver ([Zhang et al., 2026](https://arxiv.org/abs/2605.10500)), SPARK ([Zhou et al., 2026](https://arxiv.org/abs/2605.09192)), and CoEvoSkills ([Zhang et al., 2026](https://arxiv.org/abs/2604.01687)) on SkillsBench ([Li et al., 2026](https://arxiv.org/abs/2602.12670)), with two runs per method. Each run pairs an execution using the generated or evolved skill with a no-skill execution of the same task. Both runs of each method use the same task set: 81 tasks for SkillEvolver, 84 for SPARK, and 85 for CoEvoSkills.

We report mean verifier reward on a 0–100 scale and the mean within-task difference between the skill and no-skill conditions. For a run with $N$ tasks, the paired gain is
$$
\Delta = \frac{100}{N}\sum_{i=1}^{N}
\left(r_i^{\mathrm{skill}}-r_i^{\mathrm{no\text{-}skill}}\right).
$$
We also count tasks with positive, negative, and zero differences.


| Method | Run | Tasks | No skill | Skill | Δ | Improved | Regressed | Tied |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SkillEvolver | 1 | 81 | 30.20 | 55.81 | +25.61 | 27 | 6 | 48 |
| SkillEvolver | 2 | 81 | 37.32 | 62.34 | +25.02 | 26 | 3 | 52 |
| SPARK | 1 | 84 | 17.82 | 19.66 | +1.84 | 9 | 8 | 67 |
| SPARK | 2 | 84 | 14.37 | 20.81 | +6.45 | 13 | 5 | 66 |
| CoEvoSkills | 1 | 85 | 42.21 | 52.44 | +10.24 | 17 | 9 | 59 |
| CoEvoSkills | 2 | 85 | 23.54 | 33.31 | +9.76 | 17 | 10 | 58 |

**Table 1.** Two runs per method on SkillsBench. Scores are mean verifier rewards multiplied by 100; Δ is the mean paired gain in percentage points. Each method uses an identical task set across its two runs.


## Results across Two Runs

All three methods achieve positive mean paired gains in both runs (Table 1). SkillEvolver improves from 30.20 to 55.81 in run 1 and from 37.32 to 62.34 in run 2, yielding gains of 25.61 and 25.02 percentage points. The corresponding task counts are 27 improvements versus six regressions, and 26 improvements versus three regressions.

SPARK increases mean reward from 17.82 to 19.66 in run 1 and from 14.37 to 20.81 in run 2. Its paired gain rises from 1.84 to 6.45 points, with nine versus 13 improved tasks and eight versus five regressions. CoEvoSkills improves from 42.21 to 52.44 and from 23.54 to 33.31 on the aligned 85-task set. Its paired gains are 10.24 and 9.76 points, with 17 improved tasks in each run and nine versus ten regressions.

The direction of the average gain repeats for every method. SkillEvolver's gain remains near 25 points and CoEvoSkills' near ten, while SPARK shows a larger change in gain between runs. Improvements and regressions coexist within each run, making the paired task outcomes informative alongside the aggregate score. The benchmark results quantify the utility of generated and evolved skills under paired deployment. The variant experiments below examine how these gains extend to changed tasks and which artifact-level decisions support transfer.
