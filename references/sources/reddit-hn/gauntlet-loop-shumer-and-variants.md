# The "Gauntlet Loop" (Matt Shumer) — 152-word reference-bar prompt + builder/harsh-critic subagent loop; Claude of Duty and Reddit variants

- Origin repo (verbatim prompt + honest assessment): https://github.com/mshumer/Claude-of-Duty (prompt.md, README.md, ARCHITECTURE.md); HN: https://news.ycombinator.com/item?id=49063108 (4 points)
- X origin (3.8M views claimed): https://x.com/mattshumer_/status/2081857631254372509 ; press: https://decrypt.co/374560/dumbest-ai-prompt-claude-beat-careful-game-design
- Skill packaging: https://github.com/duolahypercho/gauntlet-loop
- Reddit variants: r/aigamedev 1v9mbbe "Claude Bandicoot" (118 upvotes, 59 comments); 1vjv3z8 "I left Claude Code running for 24h — 3D roguelite + own trailer" (690 upvotes, 250 comments); 1vixpx2 "Gauntlet Loop with a reference image" (59 upvotes); 1ve7xt5 "GTA 6 first attempt" (38 upvotes, 49 comments); 1vadv6u Roblox cab port (71); 1v9whng cost complaint
- Model/tool: Claude Code, Opus 5 + "ultracode" (multi-agent), /loop, /goal; Codex variants
- Genre: FPS (CoD), 3D platformer (Crash), roguelite, Shenmue-like town, open-world (GTA)
- Outcome: VISUALLY IMPRESSIVE, GAME-WEAK. Shumer's own README: "The goal was to match a modern Call of Duty. It does not." Critics' scores 3.59 -> 4.14 -> 4.05 -> 5.05/10; "In a blind A/B, every critic in every round picked the real Call of Duty frame."
- Session style: one prompt, many hours of autonomous looping (Bandicoot: 3x 5h windows; GTA: 22 h, 86 agents; roguelite: 3 prompts over 24 h)

## VERBATIM: the entire Claude of Duty prompt (prompt.md)
```
I want you to build a first-person shooter at the level of the most recent Call of Duty games. It should be utterly perfect, visually beautiful, with every single thing done at AAA quality—from textures to physics to anything you could think of.

Fan out sub-agents and have sub-agents tackle each one individually so that the game is utterly perfect. You should /loop on each item and have a separate sub-agent check it visually to ensure it looks triple A. That separate sub-agent should be a really harsh critic, and if it doesn't look triple A, it should keep going.

Don't stop until each sub-agent is utterly wowed with the quality when compared with the actual Call of Duty game. It should literally compare them side by side blind and say which one looks better. Do this in ThreeJS. /loop until it's utterly perfect. Fan out sub-agents and ultracode.
```
Note: every acceptance check in this prompt is VISUAL ("check it visually", "looks triple A", "which one looks better"). Nothing checks controls, loop, difficulty, or fun.

## Shumer's README — the most valuable process findings (verbatim)
> "Median frame time hides the actual problem. A static-camera benchmark reported 94 fps while the game was unplayable. Real gameplay at Retina DPR ... ran 12–17 fps with 728–1236 ms stalls caused by 34+ WebGL programs compiling lazily mid-frame."
> "Captures were not reproducible. shotset.mjs reuses one page across all 11 shots, so particle age, decal buffers and exposure state leak forward — two identical runs differed on 10 of 11 shots."
> "Process note: Sequential single-owner passes beat parallel fan-out decisively. Three rounds of six agents each owning one directory moved the score +0.46 and left frame-ruining defects *higher* than they started (60 → 47 → 66), because tonemapping, sky and indirect light are one coupled system and isolated agents kept breaking each other's assumptions. One sequential pass with a single owner per coupled concern moved it +1.00 and cut defects 66 → 26."
> "The most valuable single result came from an agent contradicting its own brief. Every critic for three rounds reported the weapon as 'untextured'. It wasn't — it was specular-dominated, with the diffuse term measured at L=26 against a shipped L=67. Prior rounds had been crushing albedos to fight bright-part complaints, which killed diffuse and made it worse. The fix was the opposite of what was asked for."
> "ARCHITECTURE.md is the contract the agents worked against: subsystem interface, directory ownership, the cross-subsystem event vocabulary, and shared surface types."

## Variant: Claude Bandicoot (r/aigamedev 1v9mbbe) — prompt verbatim (same template, reference = Crash Bandicoot)
"/goal I want you to build a 3D platformer Claude Bandicoot at the level of the Crash Bandicoot game. It should be utterly perfect, visually beautiful, with every single thing done at AAA quality—from textures to physics to anything you could think of. Fan out sub-agents ... /loop on each item and have a separate sub-agent check it visually to ensure it looks triple A. ... compared with the actual Crash Bandicoot game ... Do this in ThreeJS. /loop until it's utterly perfect. Fan out sub-agents and ultracode."
Comments: superkickstart: "The loop method is works for generating these small scenes that try to mimic a very small portion of the game using brute force methods and workarounds. It's pretty impressive as is but not very good at producing actual games." EC36339: "'AAA quality' is the new 'make no mistakes'".

## Variant: Shenmue-like town with a reference image (r/aigamedev 1vixpx2) — prompt verbatim
```
I want you to build a beautiful, cosy first-person Three.js world filled with living NPCs. The attached image is the hard visual quality bar: warm Mediterranean architecture, sunlit stone streets, blue shutters, terracotta roofs, lush flowers, rich vegetation, charming shops, atmospheric lighting, and a handcrafted premium-game feel.

The town should be delightful to explore, with distinctive NPCs who navigate reliably, follow believable routines, work, socialise, converse, remember recent interactions, and react naturally to the player. There should be no combat.

Divide the goal into the smallest pieces that can be improved and judged independently; you decide the exact decomposition. For every important piece, fan out a builder and a separate harsh critic with fresh context. The critic must inspect the actual running game and rendered pixels—not the builder's description—and compare them directly with the attached reference, using a blind side-by-side comparison whenever possible. If ours loses, identify the biggest remaining gap, send it back to the builder, and repeat.

Keep /looping until our result wins or I stop the run. After each major wave, use a fresh agent to smooth the complete experience into one cohesive world. Maintain a simple live progress page showing screenshots, videos, test results, and improvements over time.

Do not stop at a greybox or technical demo. Continue until the town is beautiful, polished, densely detailed, alive, cohesive, and genuinely delightful to explore. Use Three.js, sub-agents, /loop, and ultracode.
```
Outcome (author, verbatim): "By wave 7 I started to give it some basic feedback as it kept iterating on the environments and I thought they already look ok, but NPCs looked trash (spoiler: they still do)." ... "dialog are currently not great and there is no goal or real story." ... "on the other end, the world feels alive, the time passes, npc move, talk, sit, sun goes down, lights turn on etc..."

KEY COMMENT (win-win-win-win_win, verbatim): "This exposes a useful failure mode: the critic can only optimize what the reference image makes measurable, so visual cohesion converged while NPC identity and dialogue stayed undefined. For the next wave I'd replace one 'harsh critic' with three behavioral checks: the same NPC is recognizable at three times of day, one remembered fact changes a later line, and a player can predict one routine after observing it. Otherwise more agents will mostly spend compute polishing the surface that already has the clearest judge."

## Variant: GTA attempt (r/aigamedev 1ve7xt5), 22 h / 86 agents (verbatim)
> "The first attempt failed spectacularly. It got stuck after generating little more than a basic 3D world."
> "The key seems to be giving the agent much richer debugging information. Claude Code can't natively understand gameplay videos, so it extracts frames and reasons over those. That's somewhat useful, but exporting structured JSON describing the game state works *far* better because it can directly understand what's happening in the world."
> Comment (Infamous-Bed-7535): "LLMs and AI in general makes it very easy to reach a 70-80% functional prototype which looks great ... The remaining 15-20% that is required to reach the business requirements contains the hard work."

## Variant: 24h roguelite "Marcha de Ferro" (r/aigamedev 1vjv3z8, 690 upvotes) (verbatim)
> "three prompts, one every ~8 hours, each one a 'gauntlet' prompt that hands the agent a goal and lets it run. No intervention inside a session. Prompt 1 built the base game, prompt 2 followed up after the first real playtest, prompt 3 closed the round." ... "60k lines of TypeScript across 130 files, plus ~8.5k lines of design and architecture docs it wrote for itself to hand off between sessions." Assets from Kenney/KayKit packs.
Comments: Heroic_Platinum: "the gameplay looks to be almost a 1:1 ripoff of the excellent indie game Monsters Are Coming." JikkaThesorus: "it's become great at making a good first pass but iterating on details is very iffy". return_of_valensky (months-long project): "I have had to build so many mechanical gates to stop claude from just completely making shit up, not reading rules ... having to create a 'constitution' doc that specifies all the font sizes, colors, widgets because without it every menu page is an island with no consitency". Prompts not published (build-only repo https://github.com/victorrseloy/marcha-de-ferro).

## Relevance (analysis)
- The loop is a strong optimizer for whatever the critic can measure. With a visual reference, it converges on visuals; gameplay, NPC identity, dialogue and fun — which have no judge — stay weak. This is the mechanism behind failure modes (1)/(2): agents "polish" what is checkable.
- Shumer's own data: parallel isolated owners of coupled systems made defects WORSE; critics' surface complaints ("untextured") drove counterproductive fixes until an agent measured the actual cause — direct evidence for failure mode (3), and for the remedy: measure root cause, single owner per coupled concern.
- Named reference games serve as the de facto GDD (feel, content, layout come from the model's memory of Crash/CoD/Monsters Are Coming) — not a path to novel design.
