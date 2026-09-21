# Six-run main-text revision

## Author request and scope

Align the two CoEvoSkills runs and write the six selected results into the manuscript's main experimental section using academic-research-suite writing guidance. Use direct methods/results language and add no defensive limitations discussion. This is a scoped section-writing task, not a full ARS review or integrity certification.

## Task alignment

The intersection contains exactly 85 task names. The local 86-task run contains one additional task, `mhc-layer-impl`, with baseline/evolved rewards 0/0. Removing that task yields 42.2088235294 / 52.4440000000 and a paired gain of 10.2351764706 on the 0–100 scale. The server run is unchanged: 23.5449023529 / 33.3060576471, gain 9.7611552941.

`aggregate.py` checks both methods' other paired task sets, verifies the CoEvoSkills input summary hashes and all 85 local selected result hashes/scores, and writes the six-run manifest, 500 paired score rows, and table rows. The server CoEvoSkills manifest and raw-result checks are preserved in the previous audit directory. All 85 paired task identities match between the two CoEvoSkills runs.

## Selected experiments

- SkillEvolver: both local runs archived on the server, 81 tasks each.
- SPARK: server-native Rep01 budget rerun and Rep02, 84 tasks each. The migrated local SPARK experiment is excluded.
- CoEvoSkills: the local run and server-native run, aligned to 85 tasks each. Server source selection follows the post-hoc latest-valid-pair rule authorized and recorded in the preceding audit.

## Manuscript changes

- Add `Experiments on SkillsBench`, containing setup, paired metric, one six-row table, and results analysis.
- Replace one roadmap sentence to accommodate the inserted section.
- Append verified SkillEvolver and SPARK paper references.
- Keep all original abstracts, mechanism studies, figures, tables, and limitations prose intact. No new limitations section or appendix is added.

## Writing and citation provenance

Used ARS academic-paper workflow, draft-writer role guidance, writing-quality reference, and formatter guidance inline. No independent reviewer or full-pipeline verification is claimed.

New reference metadata verified from primary arXiv pages:
- SkillEvolver: https://arxiv.org/abs/2605.10500
- SPARK: https://arxiv.org/abs/2605.09192

Existing CoEvoSkills reference checked: https://arxiv.org/abs/2604.01687

`added-text.md` reproduces the added prose and table for author review. `validation.json` records the build, numeric, and preservation checks.
