# OpenGame: Open Agentic Coding for Games

- URL: https://arxiv.org/abs/2604.18394 ; code https://github.com/leigest519/OpenGame
- Authors: Yilei Jiang, Jinyuan Hu, Qianyin Xiao, et al.
- Date: April 2026
- Why it matters: identifies the recurring CROSS-FILE WIRING failures that make agent-built web games break on load/first interaction, and uses a "living debugging protocol" (error signature -> root cause -> verified fix) to stop whack-a-mole.

## Key quotes
- Game Skill = Template Skill + Debug Skill, which "stabilizes project scaffolding and resolves recurrent cross-file failures."
- Template Skill: "an evolving template library ... into a compact set of specialized template families" -- gravity-based side view, top-down continuous motion, discrete grid logic, path-and-wave dynamics, UI-driven gameplay.
- Debug Skill: "living debugging protocol ... updated from observed build, test, and runtime outcomes"; entries contain error signatures, root causes, and verified fixes.
- Recurring cross-file failures: mismatched asset keys, missing configuration fields, invalid scene transitions, broken scene wiring, initialization order problems.
- Failure taxonomy: (1) Logical Incoherence -- losing track of global state across game loops; (2) Engine-Specific Knowledge Gaps; (3) Cross-File Inconsistencies.

## OpenGame-Bench metrics
- Build Health: "whether the project compiles, loads, and renders without critical errors."
- Visual Usability: "pixel-level heuristic (frame entropy and motion detection) with a Vision-Language Model judge score." (frame entropy/motion = cheap automatic "is anything happening on screen" check)
- Intent Alignment: "a weighted pass rate from per-requirement verdicts produced by a VLM judge against a structured requirement specification."

## Workflow
Six phases: initialization and classification, scaffolding, design generation, asset synthesis, code implementation, verification/self-correction.

## Actionable takeaway
Start from a known-good template for the genre; keep a persistent "bug signature -> root cause -> fix" log that every session reads, so the same class of wiring bug is fixed at the root once.
