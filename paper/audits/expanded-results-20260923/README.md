# Expanded results and aggregate diagnosis — 2026-09-23

## Author instructions

Replace the unhelpful “Locating Successful and Failed Reuse” section and add a substantial results table. The author subsequently allowed this table to span both columns, then requested omission of “all variants”; the table therefore omits the three aggregate variant rows and retains six source runs and nine P1/P2/P3 rows. No red annotations.

## Changes

- Replaced the two-case narrative with within-task agreement across standard runs, exact gain/loss decomposition, and baseline-conditioned outcomes across the variant record.
- Combined prior results tables into a large table, adding full per-change means/counts, positive and negative contributions, and endpoint counts.
- Aligned abstract, research questions, formulation, discussion, related work, and conclusion with the analyses actually presented. Retained method-construction context without claiming a feedback ablation.
- Removed redundant prose while expanding the reported diagnostics. Preserved official ICASSP typography. Four body pages plus a separate references page.

## Reproduction

Run `python3 paper/audits/expanded-results-20260923/derive.py`, then `python3 paper/audits/expanded-results-20260923/build-wide-table.py`, then `make -C paper/maintext-20260921`. The statistics include the overall variant rows used in the prose, although those aggregate rows are omitted from the table by author request.

Input hashes are in statistics.json. An independent read-only agent recomputed endpoint transitions, gain/loss contributions, and the complete repeated-task sign cross-tabs with tolerance 1e-9; all match. The source records were not modified and no experiment was started, stopped, or changed.

## Interpretation

G and L are accounting terms, not separate experimental effects. Both use all evaluated tasks as denominator. Endpoint counts exclude ten intermediate-baseline variants per method. Same-task direction across runs does not mean repeated evaluation of identical frozen artifacts. Variant statistics remain a descriptive historical/recovery summary; no new unified-protocol causal estimate is claimed.

## Layout and delivery

The large table begins page 3 after a complete paragraph on page 2, and is followed by the section 4 heading and opening paragraph. All five English pages were visually inspected. No overfull/underfull boxes were reported. English/bilingual copies must have zero annotations. Zotero getApp timed out (-10005) in this turn; no library mutation was attempted after that failure. Preserve the baseline and old attachment until the new bilingual import can be verified.

The final bilingual file uses the final compiled English pages verbatim. Chinese ratio/direction/terminology errors were manually corrected; the references are preserved in their original form. Every repair fits without font shrinking. All five bilingual pages were visually inspected and both PDFs contain zero annotations.
