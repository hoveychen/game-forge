# GameXpert-Bench: How Far Are Coding Agents from Expert Game Development?

- URL: https://arxiv.org/html/2608.21833 (arXiv:2608.21833v1)
- Authors: Kun Chen, Haorong Hong, Peizhong Gao, Jianfeng Lin, Tongxu Luo, Yuxuan Xie, Chenxu Liu, Jieling He, Zhongyuan Liu, Zeno Zeng (Tencent Hunyuan + collaborators)
- Date: 2026-08-22
- Why it matters: most recent, largest-scale evidence that agent-built games fail at INTEGRATION (code exists but isn't wired into the running path), that agents regress core loops across iterative turns, and that self-discovering bugs is far harder than fixing listed ones.

## Rubric (four dimensions, verbatim fragments)
1. Completeness (automated): "fulfillment of the core events...including the fundamental mechanics, interactive UI behaviors, and level logic required by the game"
2. Richness (automated): "supplementary mechanics, interactive content, level variety, and other functional extensions beyond the core game"
3. Visual Quality (human): "aesthetic and spatial properties" -- UI positioning, overlaps, occlusion, overflow, 3D interpenetration
4. Player Experience (human): "holistic playability...including the responsiveness of interaction flows"; moment-to-moment feel.
- Evaluation combines "static source-code analysis with dynamic runtime validation"; intended effects "validated during execution."

## Findings (verbatim)
- "most implementation gaps arise not because the relevant code is entirely absent, but because it is not integrated into a robust end-to-end execution path."
  - 43,081 assessed events; 2,293 (5.32%) marked implemented but failed at runtime. Of those: load/crash 56%, incorrect state transitions 16%, missing feedback 13.1%, missing visual responses 11.9%.
- "a single structural omission—the closing </style> tag—changes how the browser parses the entire document." (Feature code present; whole body failed to render.)
- "Richness is lower than completeness for every model, revealing a persistent gap between constructing the essential playable core and extending it with diverse bonus mechanics"
- GameOpt (six optimization turns): models struggled to preserve the core game loop across successive changes and to avoid regressions; 97 regression checks tracked previously-correct behaviors broken by later edits.
- GameFix: Explicit-issue mode (bugs listed) scores compressed into ~13-pt span; Self-Discovery mode (bugs hidden) ~38-pt span. Strongest model cliff 7.6 pts, weaker 32.8 pts.
- Human evaluation remains necessary for qualities that "emerge only through actual play."

## Actionable takeaways
- Gate every session on a runtime regression suite of core-loop events (not code review).
- Separate "is it wired into the live path" checks from "does code exist" checks.
- Give the agent an explicit bug list from a tester rather than asking it to self-discover.
