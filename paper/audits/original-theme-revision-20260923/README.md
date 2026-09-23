# Return to original research objectives — 2026-09-23

User instruction: “再次去看一遍原论文，根据原文的主题和研究目标，再改一版出来”. The prior manuscript and all PDF deliverables are preserved in `493ffe20f`. This is an author-directed revision using the ARS writing guidance, not a formal ARS full-pipeline certification.

## What was read

The initially supplied `PDF/main.pdf` (8 pages) and original Overleaf source/PDF (7 pages, commit `121a6182b`) are different versions. Their full text was read separately. Both organize the study around (1) whether an artifact carries behavioral improvement and how far it extends, and (2) what stages or decisions explain observed gains. The Overleaf version emphasizes an audit framework; the initial PDF explicitly treats reporting implications as consequences of empirical identification.

## Revision

- Restored the identification question in the abstract and introduction. The central finding is the separation of recurring source-task benefit from useful behavior after task changes.
- Restored two research objectives: existence/scope and attribution. The performed experiments address them through completed-skill utility, controlled variations, and artifact/trace interpretation.
- Distinguished completed-skill/no-skill utility from parent-to-final revision in the formulation. The two standard runs are not described as repeated deployments of an identical frozen artifact.
- Reframed P1/P2/P3 in terms of remapping inputs, recomputing decisions, and accommodating changed correctness requirements. SkillEvolver's observed advantages remain reported with all original values.
- Reconnected cases to decisions expressed in skills and enforced in execution. CoEvoSkills' existing checks remain acknowledged. Feedback explanations remain interpretations of published construction procedures, not claimed interventions.
- Rewrote the synthesis and conclusion around persistent decision guidance, behavioral scope and gain interpretation. No SkillRevise/Hone/Opt experiments or unperformed causal ablations were restored.

The two complete table environments are byte-identical to `493ffe20f`; 500 standard pairs and 664 variant pairs were checked. Both tables are single-column and follow complete paragraphs. Four body pages are followed by a separate fifth references page. No experiment was started, modified, or stopped, and Overleaf was not edited.

A separate native read-only review found one potentially ambiguous “skills arise across runs” phrase. It was replaced with “recurring source-task utility.” This is shared-model research assistance, not an independence or submission-readiness certification.

`scoped-patches.json` records the main anchored edits; `revision.patch` records the complete final source difference. `theme-evidence-map.json` preserves source identities and the interpretation boundary. Red highlights compare cumulative changes against original Overleaf commit `121a6182b`.

## Final deliverables and Zotero

Compiled clean, cumulative red comparison, and plugin-generated English/Chinese comparison PDFs each contain five pages. The bilingual English text is canonically identical to the clean PDF; all 55 red annotations match the cumulative comparison. Observed Chinese translation and table-layout defects were corrected on the Chinese half only (`chinese-repairs.json`), and all pages were visually inspected. The bibliography retains original citation spelling on both sides.

Imported and visually verified Zotero attachment `LUKZUDRG`. Original baseline `RTB7QH9K` remains; superseded `DYD9FMCX` was moved to Zotero trash only after verifying the new attachment. The trash was not emptied. All final hashes are in `bilingual-zotero.json`.
