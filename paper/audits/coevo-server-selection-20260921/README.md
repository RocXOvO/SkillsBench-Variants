# CoEvoSkills server-native selection, 2026-09-21

The user delegated selection among duplicate evaluations. We applied one non-score ranking rule to all 85 tasks: choose the complete pair with the latest `evaluated_at_unix` after checking that both raw result files have matching task identities and rewards, finished timestamps, and no recorded exception. A timestamp tie is broken by summary path lexical order. Baseline and evolved results remain paired.

This is a post-hoc selection decision made after the previous scores were visible, not a preregistered selection rule. It resolves which existing records are used; it does not establish uniformity of all historical adapter versions. No experiments were run or modified. The original Overleaf manuscript remains unchanged.

## Result

| Tasks | Baseline mean ×100 | CoEvoSkills mean ×100 | Paired delta ×100 | Improved | Degraded | Unchanged |
|---:|---:|---:|---:|---:|---:|---:|
| 85 | 23.54 | 33.31 | +9.76 | 17 | 10 | 58 |

## Previously conflicting tasks

| Task | Batch | Baseline | CoEvoSkills |
|---|---|---:|---:|
| earthquake-phase-association | r26 | 0 | 1 |
| gravitational-wave-detection | r49 | 1 | 0 |
| lean4-proof | r26 | 1 | 1 |
| offer-letter-generator | r26 | 1 | 1 |

## Files and verification

- `selection-manifest.json`: all 85 selected pairs, source paths, source/result SHA-256 hashes, timestamps, adapter revisions, selection reasons, and exact aggregate values.
- `candidates.json`: 106 complete candidate rows read from server rep02 summary files. Some rows can refer to the same trial pair. All 106 passed the stated raw-result checks.
- `selected-scores.tsv`: one row per selected task.
- `resolve.py`: read-only SSH audit and local selection/aggregation script. It overwrites these local derived files when rerun; no remote writes.

The selected 85 task names exactly match the previous coverage audit. This manifest refers only to the server-native experiment and excludes the migrated local 86-task experiment.
