# Variant results and trace-based attribution

## Purpose

Add variant results to the paper's main experiments and organize the analysis around the original paper's question: which skill-level decisions transfer when inputs, instances, and requirements change? Use direct findings and trace-based attribution, with no added limitations discussion.

## Results

| Cohort | N | No skill | SkillEvolver | SPARK | CoEvoSkills |
|---|---:|---:|---:|---:|---:|
| Complete historical four-condition cohort | 198 | 41.90 | 56.80 | 43.63 | 39.34 |
| Every method supplies an artifact | 103 | 51.21 | 69.87 | 57.17 | 51.46 |

The common historical cohort spans 71 base-task families. Its 103-variant artifact-available subset spans 36 families. SkillEvolver exceeds SPARK by 12.70 points (family-bootstrap 95% CI 1.97–24.35), and CoEvoSkills by 18.42 (6.68–30.36), within the supplied-artifact subset. These are descriptive contrasts of the recorded evaluations. The family bootstrap uses 20,000 draws, seed 20260921, resampling families and retaining all of their variants together.

## Evidence and reproduction

- `selection-policy.json`: exact eligibility and source-selection rule, the four excluded conflict variants, coverage counts, and pinned-source SHA-256 hashes. The 48 separate-protocol recoveries are not pooled into this historical comparison.
- `selected-historical-records.json`: the 792 selected records, preserving full score precision and original source paths.
- `score-provenance.json`: server-read result hashes, score/status checks, and launch-manifest skill availability. Every selected result matched its recorded score.
- `paired-scores.tsv`: one row per variant, all four scores and artifact-availability membership.
- `analyze.py`: exact mean/delta/count computations, family bootstrap, paradigm breakdown, and literal-valid sensitivity analysis (191 variants; ranking unchanged).
- `fetch_evidence.py`: read-only remote fetch/verification. It relies on the locally retained pinned inventory; raw inventory and launch metadata are excluded from Git.
- `case-evidence.json`: 13 source hashes, the frozen skill texts, focused execution excerpts, and the original scheduling verifier result. SkillEvolver and CoEvoSkills artifacts are each byte-identical between the exoplanet P1/P3 cases.
- `coverage.json`: full reviewed-scope ledger and separate three-cell file-reading check results, preserving their protocol identities.
- `added-text.md`: exact added section text for author review.

## Manuscript edits

Added two experiment subsections and a two-panel table. Updated the standard-results transition, added one finding to the abstract, and linked the new experiment in the introduction and conclusion. Existing mechanism experiments, figures, references, and limitations text are preserved.

ARS academic-paper drafting and formatting guidance was applied. A bounded native subagent independently read the two task-family artifacts/trajectories and checked the case paragraphs; it flagged one unsupported availability-causation sentence, which was replaced with a factual statement of coverage differences. This is a focused evidence check, not a formal peer-review or full ARS pipeline certification.
