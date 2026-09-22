# Full variant-record source revision

The author requested inclusion of the completed recovery results and asked that
PDF, bilingual, highlighted-difference and Zotero regeneration wait until the
remaining text review is complete. This revision changes LaTeX source only.

## Scope and interpretation

The final ledger covers 222 variants and 886 distinct variant-condition cells:
222 no-skill, 222 SkillEvolver, 221 SPARK, and 221 CoEvoSkills observations. The
excluded SPARK/CoEvoSkills cells are both the PG audiobook P3 variant. A baseline
observation can be reused in three method comparisons, so the 664 paired rows
are not 1,328 distinct executions.

All 838 historical cells and 48 recovery identities are accounted for. The
three completed file-reading repairs replace the corresponding inline-delivery
observations in this new summary; the old ledger and all old results are
preserved. In particular, SPARK AgentOps P2 changes from 1 to 0. This leaves
838 historical, 45 other recovery and three file-reading repair observations.

The table is explicitly a descriptive summary across recorded settings. It
does not turn recovery protocols into an identical intervention or identify a
uniform-protocol causal effect. The historical-only comparison is preserved in
the earlier audit directory and Git history.

## Duplicate observations

Five historical cells have conflicting eligible scores. To include their
variants without selecting high rewards, this revision extends the prior
literal-valid-status / lexicographic-path selection rule to those cells. The
rule was chosen after collection; it is not preregistered and does not certify
that the selected record is more scientifically valid than its alternative.
`selection-policy.json` preserves every candidate, selected path, reward and
hash. `statistics.json` also reports sensitivity over all 32 combinations of
the conflicting scores. The overall signs stay positive for SkillEvolver and
SPARK and negative for CoEvoSkills across these combinations.

## Verification and reproduction

`analyze.py` reads the pinned local ledgers, verifies the selected and conflicting
result files on the server through read-only SSH, and computes the per-method
and P1/P2/P3 summaries. It never starts or changes an experiment. The 892 unique
files read comprise 886 selected records plus six alternative conflict records.
`selected-records.json` contains the complete 886-cell selection;
`paired-scores.json` holds the 664 comparisons with source hashes.

The previous statement that SkillEvolver has double-digit gains under all
three changes is replaced: in this full-record summary P3 is +9.72 points.
No compiled or translated deliverable is regenerated in this revision.
