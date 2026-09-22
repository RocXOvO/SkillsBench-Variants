# Skill utility and reuse revision

Author request: rewrite and expand the added experiment section around whether evolved skills remain useful when tasks change; reference yesterday's SAGE paper and add editable PPT logic figures. This is a user-directed local manuscript revision, not an ARS full-pipeline or formal reviewer-roadmap run.

## Argument and sources

The original manuscript separates effect existence/scope from lifecycle attribution. The new section addresses completed-skill utility and scope of reuse. It preserves the final-versus-no-skill comparison and does not substitute it for parent-to-final revision effects.

Writing reference: Wang et al., *Reinforcement Learning for Self-Improving Agent with Skill Library*, ACL 2026, https://aclanthology.org/2026.acl-long.69.pdf. Re-read main results (§4.2), usage analysis (§4.3), ablations (§4.4), and Figure 1. Adopted the progression from results to usage analysis and then complementary interventions. No result, causal conclusion, or graphic was copied.

Numerical authority: `../full-variant-records-20260922/statistics.json`, existing six-run table and its source audits. Qualitative authority: `case-evidence.json`, frozen skill texts and execution excerpts. Historical/recovery aggregation remains descriptive; no experiments or selections changed.

## Changes

- Rename added section to Skill Utility and Reuse on SkillsBench.
- Organize three questions: source-task utility, usefulness under task changes, preserved content during reuse.
- Explain the P1/P2/P3 probes and their different roles rather than treating them as ordered difficulty levels.
- Expand analysis of paired mean changes, improved/regressed counts, category profiles, and ties.
- Extend the variant table with category-specific N and delta, preserving aggregate rows.
- Expand inspected-case interpretation around diagnostic rules, correctness constraints, and adapted execution; avoid detailed period/schedule logs.
- Explicitly identify later component interventions as complementary studies of SkillRevise/SkillHone/SkillOpt, not causal validation of these three methods' aggregate differences.
- Add two PPT-authored vector figures, with native editable source retained.
- Replace the original artifact-mediation table's forced H placement with !t, and use raggedbottom to remove stretched gaps. No font or margin reductions. Final manuscript is nine pages.

## Review and verification

A separate same-family subagent read the rewrite and the raw source evidence. Its two substantive findings (aggregate mechanism extrapolation; cross-method attribution ambiguity) were corrected. Its suggestion to reduce repeated table values was applied. This was a focused check, not an independent formal peer-review panel or calibrated validity certificate.

Final LaTeX log has no warnings or undefined references. All nine pages reviewed as rendered images; new figures checked separately and in the paper. Baseline comparison remains original Overleaf commit `121a6182b`. Red text highlights mark substantive additions; red outline annotations mark the two new colored figures without recoloring their contents.

Approximate prose counts: {"before": 722, "after": 1320, "method": "Whitespace words in experiment and variant source after removing figures/tables/equation/comments; approximate."}
