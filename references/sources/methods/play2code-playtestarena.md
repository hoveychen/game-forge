# GUI Agents for Continual Game Generation (PlaytestArena + Play2Code)

- URL: https://arxiv.org/abs/2605.28258 (html https://arxiv.org/html/2605.28258v1); code https://github.com/RunRiotComeOn/gui-agents-for-continual-game-generation
- Authors: Yixu Huang, Bo Li, Na Li, Zhe Wang, Kaijie Chen, Haonan Ge, Qingyi Si, Yuanzhe Shen, Ruihan Yang, Guangjing Wang, Hongcheng Guo (Fudan, Xiaohongshu, Tongji, UCSB, JD.COM)
- Date: 2026-05-27
- Why it matters: the closest published analogue to a "coder + playtester relay". A GUI agent PLAYS every build and hands back a fixed-format play report; this loop beats agentic-coding baselines by 14.6 pts. Ablation: the play-feedback agent matters more than any memory layer.

## Results
- Play2Code: 66.8% rubric pass-rate, "+37.1 and 14.6 points" over single-pass and agentic-coding baselines.
- Ablation: removing the GUI agent caused larger drops than removing any memory layer; "its grounded, execution-based feedback surfaces runtime failures and interaction-layer bugs that the Game Agent systematically misses."
- Memory ablation (GPT-5.4): No Memory 64.1% / Episode only 69.3% / Episode+Skill 71.8% / Full 72.3%. "Episode Memory accounting for the largest share and World Memory providing genre-transfer benefits."

## Play report format (verbatim)
- "At the end of each session, the GUI Agent emits a single Markdown report with a fixed structure: run outcome and confidence, probe signals considered, chronological interaction log, per-dimension gameplay assessment, severity-tagged findings, the most blocking issue, and a recommended fix direction."
- Two artifacts: "The first is a summary describing events and interaction behaviors during play. The second is a list of actionable fixes that map observed failures to concrete code-level changes, for example, enemies remain stationary when they should patrol."

## Memory schema (verbatim)
- Episode Memory: "accumulating summaries, fixes, and attempts across rounds in a shared subspace between agents"
- Skill Memory: "holding each agent's accumulated know-how, recurring code patterns for the game agent and interaction strategies for the GUI agent"
- World Memory: "recording general game rules, common archetypes, and universal design principles"
- Entries "tagged with layer (episode-shared, skill, or world), owner (game-agent, gui-player, or shared), kind (pitfall, fix_pattern, decision, interaction_pattern, false_positive, observation), and archetype."

## Rubric authoring rule (verbatim)
- "every criterion describes a single observable behavior in concrete, observable terms (e.g., 'the spawn rate increases each wave' is accepted; 'the difficulty curve feels right' is not)."
- Sample criteria: "the spawned enemies move toward the player's position"; "the game loads and renders without errors".

## Prompt/spec requirements (verbatim)
Task prompts must include "the stateful gameplay loop; win and loss conditions; the set of valid player inputs (keys, mouse actions); expected feedback behavior on input (visual, auditory, or state-change cues); any progression structure (levels, waves, rounds)." 200 expert-written prompts, mean 131 tokens.

## Failure modes (verbatim)
- "failures such as unresponsive controls, missing state transitions, or win conditions that never trigger are invisible to code- and compilation-level inspection, and only surface during play."
- Real-time genres: GUI agents struggle with "precise timing of jumps" -- a limitation of play-based testing.

## Appendix details (fetcher-extracted)
- Five rubric dimensions: Mechanics, Controls, Progression, Interface, Visual Feedback.
- GUI agent inputs: "screenshots of the current game frame, captured at 1280×720 resolution"; "the GAME_GUIDE.md produced by the Game Agent, which specifies the intended controls, objectives, mechanics, and success conditions"; a "fixed system prompt defining its role as a playtester, its interaction conventions, and its stopping criteria". (Full prompt text not reproduced in paper; project repo is a demo site only.)
- Note the GAME_GUIDE.md handoff: the coder must write down how to play (controls, objective, success conditions) so the tester can check intent vs. behavior.
