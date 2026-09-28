# Tower of Time — AI-coded tower defense (Beginner's Jam Summer 2025), full prompt log published

- HN: https://news.ycombinator.com/item?id=44463967 (Show HN, 319 points, 152 comments, 2025-07-04)
- Repo (code + PROMPTS.md): https://github.com/maciej-trebacz/tower-of-time-game
- Play: https://m4v3k.itch.io/tower-of-time ; 5h stream of final stretch: https://www.twitch.tv/videos/2503428478
- Model/tool: Claude Sonnet 4 (main), occasional Claude Opus 4 (Cursor MAX) and OpenAI o3; via Augment Code + Cursor Agent mode. Phaser 3 + Phaser Editor (level/prefabs placed by human in editor).
- Genre: tower defense with time-rewind core mechanic
- Outcome: SUCCESS — complete, shipped jam entry, playable in browser; HN commenters played and found it fun (some confusion on early-wave energy economy). ~25–30 hours; ~95% AI-written; 7,667 lines of accepted agent edits in Cursor, 105 prompts in Augment.
- Session style: MULTI-SESSION, ~50 separate short conversations, each one feature (headings in PROMPTS.md = one conversation). NOT one-shot, and no upfront GDD — the "spec" was the author's head + incremental feature prompts.

## Process highlights (author, verbatim)

> "Each heading here is one conversation with an AI Agent ... and each code block is a separate prompt in that conversation."

> (HN reply) "If you'll look at my prompt history for the game from OP you'll see it was created with a dozens of separate conversations. This is crucial for non-trivial projects, otherwise the agent will run out of context and start to hallucinate."

> Rewindable Sprite (core mechanic) NOTE: "Since this was the core game mechanic I spent some time carefully crafting the prompt and then I've executed it using three different LLMs and picked the result that looked the best to me (Claude Sonnet 4 won)."

> Player inertia NOTE: "This failed the first time I tried it with Augment Code (the ship was randomly spinning around when moving), and the agent could not recover from it. I switched to Cursor with Claude Opus 4 in MAX mode for this feature and it worked."

> (HN) "The tutorial system in general proved to be challenging and if I had to make it again I would be more specific in how exactly it should be architected."

README lessons (verbatim):
- "It is entirely possible to develop a game with AI, but you need to know what you're doing"
- "AI makes prototyping super fast, but as you transition from prototype to final game you need to be careful"
- "AIs like to write *a lot* of code, this project could probably have two times less code"
- "Claude Sonnet 4 knows Phaser.js pretty well but for key areas I've given it a URL to the docs for the specific feature I was working on and it helped"
- "If the AI gets stuck on something ask it to add debug/console logs and share them with the agent"
- "If after that it still gets stuck don't fight it, roll back everything and try rephrasing the prompt or giving it more context"

## Build order (conversation headings, in order) — note: playable core loop first, polish last
Player -> Player Menu -> Building System -> Enemy walking -> Rewindable Sprite -> Enemy pathfinding -> Spawning enemies -> Tower shooting -> Enemy health/hit -> Issues with Rewind -> Energy system -> Enemies attacking Goal + game restart -> Enemy types + Wave system -> Title screen -> Config system -> Different tower types -> Splash/Slowdown tweaks -> Tutorial system -> (fixes) -> Tutorial dialogue critique -> skipTutorial -> explosions/glow -> Player inertia -> Music w/ reverse music during rewind -> perf cleanup -> HP bars -> drop rates -> sound system -> boss -> title bg / dialog bg / shadow / game over styling -> pause during dialogs.

## Representative verbatim prompts

Core mechanic (carefully crafted, run on 3 LLMs):
```
I want to create a new generic Phaser game object called RewindableSprite that will be the base to all further game objects that can move around and perform actions. The idea is that this object holds all of its state in a special serializable object that gets stored every n update ticks (configurable), updates `timeOffset` to the latest state entry index and then also has a `timeMode` variable that can be set to FORWARD or REWIND. When FORWARD is set the sprite works as usual - it fires its update logic normally, advances towards its target position etc. and stores its state after an update. When REWIND is set (by a public `setTimeMode` method) the object does not advance its state (and does not record it) but instead it just renders itself using the recorded state at current timeOffset. It also has a public method for rewinding the time by decreasing the timeOffset by a certain amount.
```

Systemic, forward-looking prompt:
```
I want to introduce a building system to the game. ... Player can only build on empty non-path tiles. Make sure the building system is robust and extendable because we will later have more building types, upgrades, etc.
```

Energy system with concrete numbers (economy tuned via numbers in prompt, later moved to a Config System):
```
I want to implement an Energy subsystem where the player has a set amount of energy (with max being 100 by default but changeable). ... the Rewind power should cost 1 energy for every update tick of it being used. Also placing a BasicTower should cost 50 energy ... the energy should slowly increase with time (1 energy every 5 frames) until ot hits its max value (unless we're in Rewind mode).
```

Bug report style — precise observed behavior + expected behavior, then logs loop:
```
There's an issue, when I hold REWIND for long enough the enemies stop animating and then when I release it they never start moving forward again.
```
```
This still doesn't work quite right. Now the issue of triggering the menu action many times per second is gone but pressing A on the gamepad still does not hide the menu. Add debug console logs to the code so we can debug this issue
```
```
Ok I've cleared the console, pressed A gamepad button to open the menu, then pressed it again to select a menu item. Here are the logs: <pasted console logs here>
```

Tutorial as a numbered script (+ "Think hard ... plug into already existing functionality"):
```
I want to implement a cutscene / tutorial system. ... The script is as follows:
0. Disable player menu
1. Show dialog box with dialogs ...
...
10. Spawn two Basic enemies at the spawner
There will be more, but let's focus on implementing this. Think hard about what changes are required to implement this. Try not to rewrite everything we have but instead plug into already existing functionality.
```

Content/fun: human did art curation, balancing was done by a human teammate ("Balancing, menu music & testing: death_unites_us"); the AI was asked to critique the tutorial dialogue ("Do not overdo it, keep it concise").

## Why it worked (analysis)
- Fun came from a single, human-chosen design hook (rewind costs the same energy that builds towers) specified precisely; the agent implemented it, didn't invent it.
- Human playtested every prompt; every bug report is a concrete observation.
- Core loop (move/build/enemies/shoot/damage/lose/restart) existed before any title screen, music, or styling.
- Human owned level layout (Phaser Editor) and balancing; AI owned code.
