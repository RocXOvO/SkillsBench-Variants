# SkillsBench experiments in the manuscript

The manuscript includes a main-text section, `Experiments on SkillsBench`, with six evaluations: two runs each for SkillEvolver, SPARK, and CoEvoSkills. CoEvoSkills uses the same 85 tasks in both runs. The new section is in `skillsbench-experiments.tex` and is included before `Identifying Retained Skill Effects`.

Build with `make`. The compiled manuscript has 8 pages; the six-run table is on page 3. The current deliverable is `../../output/pdf/main.pdf`.

The original Overleaf version is preserved in commit `121a618` and tag `paper-overleaf-original`. The earlier superseded revision is preserved in commit `59f5097`. Raw experiment evidence remains local and unchanged.

Derived task alignment, source hashes, all paired scores, and the aggregation script are in `../audits/six-run-maintext-20260921/`. Server-native CoEvoSkills source selection is in `../audits/coevo-server-selection-20260921/`.
