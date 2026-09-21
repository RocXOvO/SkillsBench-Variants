# Paper revision history

- The user requires every completed paper revision to be recorded in Git and pushed to this project's private GitHub repository. Use a separate descriptive commit for each coherent revision and report its short hash and concrete changes.
- Before replacing or reverting manuscript content, preserve the current version in a commit. Prefer a new restoration/revert commit; do not erase history with reset or force-push.
- Active manuscript: `paper/maintext-20260921/main.tex`. Current compiled deliverable: `output/pdf/main.pdf`.
- The original Overleaf source snapshot is preserved locally in `paper/overleaf-original-20260921/`. The initially supplied `PDF/main.pdf` is a different version; do not conflate the two.
- Track only the allowlisted manuscript source, build instructions, current PDF, and derived audit records under `paper/audits/`. Do not stage experiment workspaces, credentials, raw run logs, or caches.
- Manuscript work does not authorize starting, modifying, or stopping experiments, or editing the online Overleaf project.
- After a manuscript edit, compile and inspect the PDF, copy it to `output/pdf/main.pdf`, commit both source and PDF, and push. If pushing fails, preserve the local commit and clearly report the unsynced status.
- Zotero should retain only the latest bilingual PDF attachment for this manuscript. After importing and verifying each new bilingual version, move older bilingual, English, and Chinese-only PDF attachments under this manuscript to Zotero's trash. Keep the parent item, local files, and Git history; do not empty the trash.
