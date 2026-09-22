# Paper manuscript

The editable LaTeX project is in `paper/maintext-20260921/`.

```bash
cd paper/maintext-20260921
make
```

The current compiled paper is `output/pdf/main.pdf`.

The PDFs were regenerated at the author's request on 2026-09-22, incorporating the complete variant records and an expanded diagnostic narrative about utility, behavioral scope, and lifecycle attribution. The clean and bilingual manuscripts both have nine pages. Full variant-record statistics and source choices are documented in `paper/audits/full-variant-records-20260922/`.

`output/pdf/main-revision-highlighted.pdf` marks substantive additions and replacements relative to the original Overleaf baseline (`121a6182b`) in red, with Chinese annotation comments. The nine-page English/Chinese reading copy is `output/pdf/main-bilingual-en-zh.pdf`; its English side carries the same 37 highlights. The comparison includes the abstract, introduction, new experiments and tables, skill-reuse analysis, conclusion, and two added references. Layout-only moves and automatic numbering changes are documented separately in the comparison audit. Zotero retains the original Overleaf baseline (`output/pdf/main-overleaf-original-20260921.pdf`, seven pages) and the latest bilingual red-highlighted comparison. Superseded revision attachments are moved to its trash; local files and Git history preserve prior versions.

Git history preserves each completed revision. Experiment directories and credentials are excluded from version control. Use a new restore or revert commit to return to an earlier version without deleting subsequent history.

The latest diagnostic rewrite is documented in `paper/audits/variant-maintext-20260921/diagnostic-theme-revision-20260922.md`, with the exact English prose in `diagnostic-rewrite-original-text-20260922.md`. The two provisional flow figures were withdrawn from the manuscript; their source files are retained as rejected drafts only.
