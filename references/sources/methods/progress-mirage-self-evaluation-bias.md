# When Do Agent Loops Mistake Stagnation for Progress? Self-Evaluation Bias and Externally Grounded Verification in Long-Running Autonomous LLM Agent Loops

- URL: https://arxiv.org/abs/2607.25152 (pdf https://arxiv.org/pdf/2607.25152)
- Authors: Hyundoo Park, Byungho Choi
- Date: 2026-07-27 (arXiv preprint; not peer-reviewed as far as fetched)
- Why it matters: a controlled measurement of exactly our failure mode 1 -- "sessions keep reporting progress while the product doesn't improve" ("progress mirage").

## Findings (fetcher-extracted from abstract/body)
- Agents accepted their own claimed improvements 100% of the time across 54 cycles, yet 56% of those cycles showed zero or negative real-world progress.
- Strong in-band judges given artifact text and diff history still decided poorly: of accepted changes "44 percent were real-world regressions", and they "rejected 38 percent of real improvements."
- The self-verdict gate ended up "eroding the best deployed state it had reached by 19 percent."
- With verifiable, externally grounded success signals the mirage disappeared; a sign-only verdict (just better/worse from the real world) matched full feedback (110.0 vs 113.0) -> grounding matters more than feedback richness.
- Recommendation: prioritize "out-of-band evaluation with real-world access" over scaling up internal judges.

## Mapping
Even a one-bit external signal per session ("golden-path replay passed: yes/no"; "playtester preferred build N over N-1: yes/no") beats a rich self-report. Keep best-known-good build and revert on regression.
