# Experiment-aligned manuscript revision — 2026-09-23

The author's instruction was to update the previously untouched rear sections to reflect their actual SkillEvolver, SPARK and CoEvoSkills experiments, removing the unrelated SkillRevise/SkillHone/SkillOpt material. Pre-revision commit: `644ae4916`. Original Overleaf comparison baseline: `121a6182b`.

## Changes

- Replaced abstract and introduction promises of lifecycle interventions with repeated source-task utility, controlled task variation, and skill-level interpretation. The abstract contains no detailed score inventory.
- Retained the generic skill-update/execution equations and aligned the research questions with the performed evaluations.
- Kept every numeric value in both result tables; made two concise wording adjustments in experimental setup.
- Moved the skill examples from subsection 3.4 to a developed section 4. It now distinguishes candidate selection from answer validity, feasibility from repair correctness, and interprets the three methods' construction feedback. CoEvoSkills' existing checks are explicitly acknowledged.
- Removed the inherited 24-task retention panel, Invoice/Energy/SearchQA mediation cases, Radar/Spreadsheet verifier studies, oracle/integrity controls, old tables 3–5, and the lifecycle-intervention diagram.
- Replaced their discussion/reporting/limitations material with implications grounded in the actual observations: mean benefit versus improvement frequency, retained decision rules, and evaluation across task-change types.
- Rewrote related work and conclusion around the performed study. Unused bibliography entries remain in the source database but are not printed.
- Following the latest instruction, converted both tables to single-column layouts and placed references on a separate page. The result is four body pages plus one references page, with unchanged body font and margins. Both tables follow complete result discussions. The generic lifecycle figure follows its definitions. Compact table headings retain all counts, gains, and improvement/regression/tie values.

## Evidence and interpretation

The 500 standard-task paired rows and 664 variant paired rows were recomputed from the preserved audit records. Every numeric table cell is unchanged from the previous content. The pre-layout rewritten manuscript is preserved in checkpoint `3c5c19068`; its prose is unchanged by the single-column revision. The full variant summary remains descriptive across historical/recovery settings. No causal feedback intervention, component ablation, or parent-to-final comparison is presented as performed.

The signal-detection case retains SkillEvolver's P1/P3 success and both inspected skills' P2 failure. The scheduling case retains SkillEvolver/SPARK success on all three variants and CoEvoSkills success only on P3. The P1 failure is described as local minimality, not global earliest-start optimality.

Primary method descriptions were checked at:
- https://arxiv.org/html/2605.10500v1 — contrastive deployment feedback and independent audit.
- https://arxiv.org/html/2605.09192v1 — verified trajectory distillation and preserved execution evidence.
- https://arxiv.org/html/2604.01687v2 — surrogate diagnostics and opaque oracle pass/fail.
- https://arxiv.org/abs/2602.12670 — SkillsBench.
- https://arxiv.org/abs/2603.15401 — SWE-Skills-Bench.
- https://arxiv.org/abs/2604.20087 — SkillLearnBench.
- https://arxiv.org/abs/2605.23899 — experience, extraction, consumption.

## Execution record

ARS academic-paper revision guidance, writing-quality checks, and PDF rendering checks were applied. One read-only native reviewer inspected the actual evidence and the revised claims. This was scoped author-directed editing, not a full ARS pipeline or a certification of submission readiness. Native patches and the final Git diff record the changed surface; no formal author-adjudication artifact was fabricated.

`validate.py` checks the source/table invariants, recalculates reported metrics, scans for removed claims, and verifies PDF bounds. `validation.json` records results. `highlight-original-comparison.py` marks the current cumulative changes; deleted original material is listed in `highlights.json` rather than painted onto absent pages. The baseline and superseded versions remain in Git and Zotero's recoverable storage.

## Final rendering and library state

The clean English PDF has four body pages and a separate fifth page of references. The bilingual file preserves the English text exactly and carries 59 red highlight annotations against the original Overleaf version. PDF2zh generated the Chinese reading copy; visible broken headings, cross-column fragments and shrunk text were corrected in `repair-chinese.py`. Numeric tables and bibliographic names/titles retain original English typography on the Chinese side; captions and body text are translated. All five Chinese pages were visually inspected.

Zotero attachment `DYD9FMCX` was imported and its bytes verified against the local deliverable. It was opened on page 3 to verify the single-column table and red highlights. The original baseline `RTB7QH9K` remains active; superseded attachment `4WVW6YXC` was moved to the recoverable trash after the new file was verified. The trash was not emptied.
