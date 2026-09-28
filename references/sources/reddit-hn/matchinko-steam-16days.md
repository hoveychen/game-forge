# Matchinko — match-3 x pachinko roguelite, engine-free Rust, idea -> Steam upload in 16 days with Claude + Codex

- Reddit: https://www.reddit.com/r/aigamedev/comments/1vs38mh/ (r/aigamedev, 22 upvotes, 2026-08) — low engagement; self-reported
- Steam: https://store.steampowered.com/app/4994610/Matchinko/ (demo in Steam Pins & Pegs Fest 2026)
- Skills (MIT): https://github.com/Data-Oriented-Design-for-Games/data-oriented-design ; https://github.com/nitzangames/procedural-game-art ; https://github.com/nitzangames/headless-game-balance ; https://github.com/nitzangames/steam-demo-release
- Model/tool: Claude and OpenAI Codex interchangeably; Rust (wgpu/winit/egui), procedural woodcut renderer, no AI image assets
- Genre: match-3 + pachinko roguelite deckbuilder-ish
- Outcome: SUCCESS (shipped Steam demo; 900+ tests; seeded headless auto-player). Author is an experienced dev/book author (High Performance Unity Game Development).
- Session style: MULTI-SESSION, ~16 days to first Steam upload, polish through August

## Key points (verbatim)
Constraint-driven ideation instead of "invent a game":
> "The festival constraint helped. Instead of asking AI to 'invent a game,' I could ask a specific question: *How can pins and pegs support a mechanic that is not just another Peggle clone?*"
> "A playable JavaScript/Canvas prototype existed on day one."

Architecture skill as shared rules for both agents:
> "It gave both agents the same persistent rules: static `Balance` data, mutable `GameData` in parallel arrays, pure logic functions, a read-only presentation layer, seeded randomness, and no allocation in hot paths. That separation made the no-engine approach manageable and allowed most of the game to run headlessly without a window, GPU, audio device, or Steam client."

Where AI failed — global consistency:
> "AI was excellent at producing the first complete version of a clearly bounded system. ... The weakness was **global consistency**. We still managed to: Let the JavaScript and Rust implementations drift apart / Upload the wrong older demo once / Show 32 stops in what should have been a 16-stop demo / ... Let item descriptions drift away from their real behavior / Produce capsule art that passed tests but still looked visibly cropped or discontinuous. These were not syntax failures. They were integration, product, and source-of-truth failures."

Structural fixes, not "be careful":
> "We fixed them structurally: retired the duplicate JavaScript game, made the demo a compile-time build flavor, embedded and verified its Steam App ID, scanned binaries before staging them, derived descriptions from live balance data, and added reachability tests for every fairy and tile."
> "The game now has more than 900 tests, plus a seeded headless player that runs hundreds of complete games for balance tuning. Neither replaces human playtesting or visual judgment."
> "The best response to an AI-assisted mistake is not 'be more careful next time.' It is to add a guard that makes the same mistake impossible."
