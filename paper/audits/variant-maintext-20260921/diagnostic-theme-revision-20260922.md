# Diagnostic-theme revision

## Author direction

Rewrite and expand the added experiments around the manuscript's diagnostic
question, using yesterday's SAGE paper as a writing reference. Preserve data and
avoid turning the manuscript into a method-ranking or proposed-method paper.
This is an author-directed manuscript revision, not a formal peer-review verdict
or a claim of compliance with a particular venue's review criteria.

## Reference and adaptation

Wang et al., *Reinforcement Learning for Self-Improving Agent with Skill Library*,
ACL 2026: https://aclanthology.org/2026.acl-long.69.pdf

Sections 4.2–4.4 connect main results to skill-use analysis and then ablations.
The useful rhetorical pattern is a result followed by a question about the
behavior producing it, followed by a contrast that tests the explanation. Here
that pattern is adapted to a diagnostic audit: source utility → scope under task
changes → decisions observed in traces → retention and lifecycle interventions.
SAGE's data, wording, method, and causal findings are not imported into our paper.

## Changes

- Rename the added section to “Diagnosing the Scope of Skill Utility.”
- Expand source-task analysis: stable paired gains despite shifting absolute
  baselines, and the distinction between mean gain and task-level outcomes.
- Explain P1/P2/P3 as probes of input interpretation, instance-specific
  computation, and coupled requirements.
- Analyze the distinctive P2 profile, the category-specific results, and the
  difference between gain magnitude, gain frequency, and reward ties.
- Organize qualitative evidence around decision criteria and correctness checks.
  Preserve the signal-detection P2 failure and SPARK's scheduling successes so
  the examples characterize behavior rather than selectively illustrating one
  method's favorable results.
- Connect artifact utility and trace observations to the actual-parent/final
  and component-intervention contrasts in the subsequent mechanism studies.
- Rewrite the introduction's study overview and the conclusion's first paragraph
  to follow the same diagnostic argument.
- Withdraw the two provisional flow figures. Retain their draft sources only for
  revision history; do not present the intermediate PPT as a deliverable.
- Preserve all six standard runs, all 886 condition cells, and all table values.

## Evidence mapping and inline review

| Manuscript analysis | Evidence |
|---|---|
| Standard paired means and sign counts | `../six-run-maintext-20260921/six-runs.json` |
| Overall/P1/P2/P3 variant statistics | `../full-variant-records-20260922/statistics.json` |
| Scheduling and signal-detection outcomes | `../full-variant-records-20260922/paired-scores.json` |
| Artifact decision rules and execution excerpts | `case-evidence.json` |
| Retention, surgery, and verifier results | Existing baseline manuscript; unchanged |

The same assistant checked numeric correspondence, terminology, transitions,
case scope, and causal language. This is an inline self-review, not an independent
reviewer or a venue-calibrated assessment. Aggregate variant comparisons remain
explicitly descriptive. No component ablation is inferred from trace inspection;
no final-versus-no-skill difference is called a parent-to-final revision effect.

## Outputs

- Exact revised prose: `diagnostic-rewrite-original-text-20260922.md`.
- Clean manuscript: `../../../output/pdf/main.pdf`.
- Original-baseline comparison: `../../../output/pdf/main-revision-highlighted.pdf`.
- Baseline: original Overleaf commit `121a6182b`, preserved unchanged.
- Pre-rewrite checkpoint: `52f25d6ea`.

No experiment, online Overleaf source, or experiment selection record was changed.
