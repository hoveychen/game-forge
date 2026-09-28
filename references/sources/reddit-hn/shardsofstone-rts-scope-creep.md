# Shards of Stone — vibe-coded WC2/WC3-inspired RTS that sprawled into 4 games; players can't build/chop wood (FAILURE MODE: polishing irrelevant details over a broken core loop)

- Reddit (Part 3): https://www.reddit.com/r/vibecoding/comments/1wh47qo/ (r/vibecoding, 76 upvotes, 92 comments, 2026-09); Part 1: https://www.reddit.com/r/vibecoding/comments/1s8w5ib/
- Play: https://shardsofstone.com/ ; tools: https://www.shardsofstone.com/tools
- Model/tool: Claude Code initially, then Claude + Gemini + Codex (incl. "Astra"), parallel sub-agent teams
- Genre: browser RTS (9 factions, 200+ units) + MOBA + TCG + dungeon crawler sharing one world
- Outcome: FAILURE on playability/fun per playtesters despite enormous feature list; ~6 months spare-time, non-gamedev owner who directs by "feeding in ideas and requests".
- Session style: MULTI-SESSION, many parallel agents, owner does "twenty minutes here and there"

## What the agents built (excerpt of the owner's changelog, verbatim bullets)
"Persistent tracks through snow, gradually filling back in." / "Snowfall fills those tracks faster." / "Wakes fitted to each ship's hull, rather than every vessel producing the same trail." / "Submarine diving and surfacing effects" / "Trees that react to chopping and actually topple over when harvested." / "Forest optimisation - one documented zoomed-out jungle scene dropped from roughly 113 million triangles to 7 million" / "Islands drift and temporarily connect into land bridges" / "An importer reads WC2 and WC3 map files ..." / "Roughly 10× faster simulation in an eight-player stress benchmark"

Owner's role (verbatim): "the agents are doing the coding and implementation. I'm feeding in ideas and requests, directing things, playing it, giving feedback and asking them to fix whatever I've broken or don't like." "The scope creep is getting insane."

## Playtester reports in the same thread (verbatim)
- RepulsiveRaisin7 (17): "Tried the RTS and there was no way to build anything. TBH you're building stuff for the sake of building stuff? Scope creep is not something to be proud of. What is the vision? Why 4 games instead of one that players will actually want to play?"
- sirjonathan: "I tried the RTS and was impressed that I got to a playable screen. In my case, when I got to the wood chopping part it appears there was no wood to chop?"
- delinger90: "Some of the villagers would get stuck in a T-pose while walking back and forth carrying resources. The terrain layout was also difficult to understand unless I viewed it from a spe[cific angle]"
- Any_Economics6283: "I cannot determine the difference between these units and the leaves on the ground. ... This would be abysmal to play because it is too hard to tell at a glance what is going on, which is essential for an RTS"
- _Wilbraham: "The fact that the units are so hard to see against the floor should have been something you realized _needed_ fixing before you came here to brag about this."
- Smart_Opportunity209 (after ~1 hour): "pick a destination and arrive there. You have 4 half baked games instead of one polished. Units do not have idle animation ... game itself is so laggy it makes units difficult to control. ... graphic style seems all over the place"
- ruiyanglol2: "doing so many things at the same time just make it seem like none of it is very good / polished."
- vile-style: "nobody in their right mind would play this over just playing warcraft III."
- waypostmaster: "240 units may like a restaurant with too big a menu"

## Relevance
Closest public analogue to failure mode (1): the core economy loop (build, harvest wood) fails for new players in the first minute, while agent effort goes to snow tracks, hull-fitted wakes, triangle budgets and map importers. No acceptance gate on "a new player can complete the first 3 steps"; readability (unit vs ground contrast) never checked. Also (2): no articulated vision/differentiator ("What is the vision?").
