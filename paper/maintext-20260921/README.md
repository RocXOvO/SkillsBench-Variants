# SkillsBench experiments in the manuscript

The manuscript includes a main-text section, `Experiments on SkillsBench`, with six evaluations: two runs each for SkillEvolver, SPARK, and CoEvoSkills. CoEvoSkills uses the same 85 tasks in both runs. The new section is in `skillsbench-experiments.tex` and is included before `Identifying Retained Skill Effects`.

Build with `make`. The compiled manuscript has 8 pages; both the six-run table and the variant table are on page 3. The current deliverable is `../../output/pdf/main.pdf`.

The original Overleaf version is preserved in commit `121a618` and tag `paper-overleaf-original`. The earlier superseded revision is preserved in commit `59f5097`. Raw experiment evidence remains local and unchanged.

Derived task alignment, source hashes, all paired scores, and the aggregation script are in `../audits/six-run-maintext-20260921/`. Server-native CoEvoSkills source selection is in `../audits/coevo-server-selection-20260921/`.

The variant analysis is in `skillsbench-variants.tex`: separate paired evaluations of 206 SkillEvolver variants, 204 SPARK variants, and 204 CoEvoSkills variants, followed by trace-based attribution in exoplanet period detection and scheduling. Source selection, scores, uncertainty calculations, and case evidence are in `../audits/variant-maintext-20260921/`.

The current per-method variant statistics and selected source hashes are in `per-method-statistics.json` and `per-method-paired-scores.json`. Earlier shared-set analyses remain archived in the same audit directory. `skillsbench-variant-table.tex` queues the variant table immediately after the standard-task table to keep both within the experiments section.
