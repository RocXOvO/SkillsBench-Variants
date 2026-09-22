# Editable logic figures, 2026-09-22

The two original diagrams were authored as native PowerPoint text, shapes and connected arrows using `@oai/artifact-tool`. The final deck is `output/pptx/skill-transfer-logic-20260922.pptx`. It contains two 12.5 × 4.1667 inch slides. A muted blue / purple / amber / green palette distinguishes stages and variant types; a muted red path denotes the observed failure pattern in the inspected cases.

## Figure scope

1. `variant-evaluation-logic.pdf`: source-task skill generation/evolution, frozen final artifact, three kinds of task changes, and a matched no-skill evaluation. The contrast is final skill versus no skill, measuring the scope of utility. It does not depict a pre-evolution / post-evolution ablation.
2. `skill-reuse-logic.pdf`: interpretation of inspected artifacts and traces. Diagnostic rules and output constraints guide adaptive execution; corresponding failure cases omit a needed decision or constraint. The paths do not assign a universal mechanism to a method. This diagram is conceptual, not a causal intervention result.

Design inspiration: Figure 1 in Wang et al., *Reinforcement Learning for Self-Improving Agent with Skill Library*, ACL 2026, <https://aclanthology.org/2026.acl-long.69.pdf>. The diagrams are new compositions. No graphics or phrasing were copied from that figure.

## Build and export

`build-logic-figures.mjs` contains the complete native slide authoring source. It was run from `tmp/ppt-logic-20260922/` with a `node_modules` symlink to the bundled runtime packages. Set `RUNTIME_NODE_MODULES` to `/Users/duchongyang/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules`, and use the bundled Node executable. The finalizer intentionally refuses to overwrite its output and receipt; select a new output filename and receipt filename for a future revision.

The checked r3 PPTX was copied unchanged to the final filename. The local bundled LibreOffice `soffice` converted it to PDF using `impress_pdf_Export`. PyMuPDF split the two pages with `insert_pdf`, without rasterizing text or vector shapes. The manuscript uses those single-page PDFs. The source PPTX SHA-256, vector drawing counts and zero-image checks are in `logic-figures-20260922.json`.

## Verification

The deck passed the supplied package, dimensions, font, heading-fit and first-party import checks; the retained receipt is `logic-figures-validation-20260922.json`. Both Artifact Tool previews and the exported PDF pages were inspected visually. The inspection corrected arrowhead direction and one text overlap before final export. Final figures have no visible overlap or clipping. PowerPoint itself was not opened, so native PowerPoint rendering is not claimed.
