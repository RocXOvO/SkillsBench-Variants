# Paper revision history

- The user requires every completed paper revision to be recorded in Git and pushed to this project's private GitHub repository. Use a separate descriptive commit for each coherent revision and report its short hash and concrete changes.
- Before replacing or reverting manuscript content, preserve the current version in a commit. Prefer a new restoration/revert commit; do not erase history with reset or force-push.
- Active manuscript: `paper/maintext-20260921/main.tex`. Current compiled deliverable: `output/pdf/main.pdf`.
- The original Overleaf source snapshot is preserved locally in `paper/overleaf-original-20260921/`. The initially supplied `PDF/main.pdf` is a different version; do not conflate the two.
- Track only the allowlisted manuscript source, build instructions, current PDF, and derived audit records under `paper/audits/`. Do not stage experiment workspaces, credentials, raw run logs, or caches.
- Manuscript work does not authorize starting, modifying, or stopping experiments, or editing the online Overleaf project.
- After a manuscript edit, compile and inspect the PDF, copy it to `output/pdf/main.pdf`, commit both source and PDF, and push. If pushing fails, preserve the local commit and clearly report the unsynced status.
- Zotero should retain the original Overleaf baseline PDF plus the latest bilingual red-highlighted comparison for this manuscript. The user explicitly requested the baseline exception on 2026-09-22. After importing and verifying each new bilingual version, move superseded revision attachments to Zotero's trash; preserve the baseline, parent item, local files and Git history. Do not empty the trash.
- On 2026-09-22 the user explicitly requested generation after the source-review edits, ending the temporary rendering deferral. Generate the comparison against original Overleaf commit `121a6182b`, including all accumulated edits.
- Table-placement regression recorded on 2026-09-22: inspect the reading order before and after every table, not only TeX warnings. Keep a table from separating fragments of the same paragraph; keep headings with their opening text and avoid fixing float placement by creating large blank areas.
