# GameGen-Verifier: Parallel Keypoint-Based Verification for LLM-Generated Games via Runtime State Injection

- URL: https://arxiv.org/abs/2605.07442 (html: https://arxiv.org/html/2605.07442v1)
- Authors: Chaobo Jia, Ruipeng Wan, Ting Sun, Weihao Tan, Borui Wan, Yuxuan Tong, Guangming Sheng, Hong Xu
- Date: May 2026 (arXiv)
- Why it matters: shows that "agent plays the game via GUI" is a weak verifier (58.8% agreement with humans) and that spec-derived keypoints + direct state injection is a strong one (92.2%). Directly addresses "game breaks within first 3 steps / agents can't see it".

## Problem (verbatim)
- "Unlike conventional code generation, game correctness is defined over long-horizon interaction: a game may appear correct while violating core mechanics such as state updates, interaction rules, and phase transitions."
- "A generated game may build successfully and appear visually correct while violating core mechanics such as state updates, interaction rules, and phase transitions."

## Method (verbatim from abstract)
- "GameGen-Verifier extracts sparse, specification-derived critical conditions from the specification and formulates them as verifiable keypoints."
- "the verifier constructs a precise game state described by the implementation's parameter structure, injects it into the runtime, executes a bounded interaction sequence, and judges whether the observed outcome satisfies the expected one."
- "This formulation makes verification units self-contained, reducing unreliable gameplay to a finite set of parallelizable short-horizon verifications."

## Why exploratory agent-play fails (paraphrase of paper section)
Coverage-enforced agent-as-verifier hits exponential state space and reachability barriers; late-game states (boss fights, rare rule violations) are slow or impossible to reach through natural play; verification described as "slow, coverage-limited, and misaligned with specification-level judgment."

## Keypoint example (as rendered by the paper's formalism)
Spec: "When the player collides with a boss, health should decrease by 10 points."
- Keypoint phi = (P, a, Q): P = player near boss, health = 100; a = collision sequence; Q = health == 90
- Verification unit u_k = (s_k, i_k, y_k): s_k = inject position+health via runtime state; i_k = bounded collision script; y_k = assert health value.

## Results
- VeriGame: 100 games, seven genres. "up to 92.2% accuracy against human judgments versus 58.8% for the coverage-enforced Agent-as-a-Verifier baseline, while reducing wall-clock time by up to 16.6x."

## Actionable takeaway
Require every game to expose a debug/state-injection hook (e.g. window.__game.setState / getState, seeded RNG) so a verifier can jump to any state and run a short scripted input sequence; write keypoints (P, a, Q) from the GDD, not from the code.
