# Voxel Velocity (OpenAI, Codex app launch demo) — dense one-paragraph spec + generic re-prompt loop

- **Source URL:** https://openai.com/index/introducing-the-codex-app/ (section "Go beyond code generation with skills"); sequel in https://openai.com/index/introducing-gpt-5-3-codex/ ("version two of the racing game" + new diving game "Dive In", again driven by "preselected, generic follow-up prompts like 'fix the bug' or 'improve the game'")
- **Model/tool:** Codex app (GPT-5.x-Codex, early 2026) with `develop-web-game` skill + `imagegen` skill (GPT Image). The skill was at github.com/openai/skills/.../develop-web-game/SKILL.md; it is no longer in the repo tree as of Sept 2026.
- **Genre:** 3D voxel kart racer (Three.js), 8 tracks, 8 characters, 8 items, CPU AI
- **Result evidence:** Playable build embedded on the OpenAI page, which also let you "try out earlier iterations to see how Codex improved it as it worked for longer"; YouTube re-creations exist (e.g. https://www.youtube.com/watch?v=E8yDhj0pIBY)
- **Quality signal:** Vendor launch demo, so treat it as marketing. ">7 million tokens with just one initial user prompt"; the agent "took on the roles of designer, game developer, and QA tester to validate its work by actually playing the game."
- **One-shot vs iterative:** One substantive human prompt, then continuous automatic re-prompting from a random list of 10 generic prompts (no human design input).
- **Caveat:** OpenAI says the prompt below is "summarized for clarity", so the real prompt was longer. It references "the 8 characters with their given stats", which implies a stat table that was not published.

## Prompt (as published, "summarized for clarity")

```
Implement Voxel Velocity as a 3D voxel kart racer using Three.js, with exactly one mode: Single Race (always 3 laps, 1 human vs 7 CPU, and all 8 tracks available immediately with no progression). Build a minimal pre-race flow with only: Track (8), Character (8), Difficulty (Chill/Standard/Mean), optional Mirror Mode, optional Allow Clones, and Start Race, plus an Options menu and an in-race pause menu (Resume / Restart / Quit). Create an arcade driving model with responsive handling, forgiving glancing wall hits, meaningful drifting as the main skill, and a drift-charge system that produces exact boost tiers (Tier 1 0.7s, Tier 2 1.1s, Tier 3 1.5s) while keeping baseline speed "fast-but-readable" and pack passing constant on wide roads. Implement exactly 8 items with one-item capacity, subtle position-weighted distribution, and mild effects (max loss of control ≤1.2s, max steering disabled ≤0.6s) that create goofy chaos without hard stuns, plus off-road slowdowns that are reduced by 50% during boosts. Define the 8 characters with their given stats and AI tendencies, implement CPU difficulty presets and track-authored racing/variation splines, drift zones, and hazard avoidance so AI uses multi-lane width for clean overtakes, and ship HUD/audio essentials (position, lap/final lap banner, minimap, item slot, timer/splits, readable SFX, and one music loop per track).
```

## Example generic continuation prompt (1 of 10, randomly rotated)

```
Your job is to add new features so the game matches the original more closely. First, play the game and identify what's missing vs. the original. Then pick a few missing features and implement them. After each feature, thoroughly test it by playing the game and confirm it works. If you notice any bugs while playing, prioritize fixing them too.
```

Notable spec traits: hard scope caps ("exactly one mode", "exactly 8 items", "only:" menu list, "no progression"); numeric feel parameters (boost tier durations, stun caps ≤1.2s/≤0.6s, off-road -50% during boost); design intent stated as feel ("goofy chaos without hard stuns", "fast-but-readable"); names the core skill loop ("meaningful drifting as the main skill").
