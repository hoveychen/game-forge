# Claude of Tanks — multiplayer Three.js tank game, 100+ vehicles, long-running multi-agent pipeline with visual critic

- Reddit: https://www.reddit.com/r/ClaudeGameDev/comments/1vz74j8/ (21 upvotes, 13 comments, 2026-08); cross-post r/vibecoding 1vu0p6q (175 upvotes, 43 comments)
- Play: https://cot.kevinliu.studio ; Repo (AGENTS.md + subsystem instruction files): https://github.com/Kevin-Liu-01/Claude-of-Tanks
- Model/tool: Claude Code + Codex, orchestrator + per-vehicle-family agents + separate critic agent, git worktrees
- Genre: World-of-Tanks-Blitz-like multiplayer arena
- Outcome: SUCCESS-ish (playable, multiplayer; commenters positive; complaints: graphics, reversed minimap, "vehicles aren't procedural")
- Session style: MULTI-SESSION, long-running parallel agents

## Key lessons (verbatim)
> "The repository contains an AGENTS.md file and smaller subsystem instruction files covering simulation, vehicles, networking, UI, audio, effects, and world generation. These record the rules that agents need across sessions. Units are meters, seconds, and radians, and changes enforce a fixed 60 Hz. Authoritative logic must be deterministic. Vehicle changes have specific geometry, armor, module, and release gates that evaluate models visually and geometrically."
> "One agent would own a specific vehicle profile or family file, implement the geometry, run the relevant checks, and generate screenshots. A separate critic reviewed the rendered tank for proportions, clipping, missing surfaces, running gear, and recognizable details. The orchestrator reran the checks and committed only the verified files."
> "For visual quality, the only thing that worked was a proper render loop with visual comparison; tests don't really work for this. The cycle I fell into was change, render, inspect, measure, and rerun the gates. Text-only reviews missed warped proportions and camera problems that would just plainly be obvious in one screenshot."
> "Claude Code became much more reliable once every system had concrete invariants and executable failure conditions. But visual quality is another beast."
> "Parallel agents need strict ownership. Separate files and isolated Git worktrees prevented concurrent sessions from overwriting each other"

Commenter: "Did you hand create the particles? I've found Claude only made really basic ones despite how confident it sounds about the effects it will be adding."
