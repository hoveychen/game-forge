# Super Mario Galaxy fan game — Claude Code (Opus), 53 days, 76K LOC TS

- HN: https://news.ycombinator.com/item?id=47600002 (Show HN, 7 points, 14 comments, 2026-04-01) — low HN points but went viral on X
- Game: https://supertommy.com/games/super-mario-galaxy-movie-game/ ; three.js forum: https://discourse.threejs.org/t/super-mario-galaxy-movie-game/90783
- Model/tool: Claude Code (Opus), $200 Max plan; custom skills; blender-mcp
- Genre: 3D platformer with spherical/multi-field gravity (Three.js + Rapier3D WASM + custom SoA ECS)
- Outcome: SUCCESS on mechanics/tech (playable, mobile+gamepad, polished movement, Yoshi, spin attack); explicit FAILURE on level design ("failed completely"). Commenter noted fixed jump height (no variable jump) — game-feel detail missed until shipping.
- Session style: MULTI-SESSION, 735 commits, 87 plans, 36 AI code reviews, 11 retrospectives.

## Process (author, verbatim)
> "Claude Code (Opus) wrote ~95% of the code. I provided architecture, constraints, and direction; looked at some but not much of what it wrote."

> "My process for every feature: braindump what I want, relevant technical details, and 'does this make sense?' into the chat. Largely unorganized. I built custom Claude Code skills like /lets-build:plan that spawns sub-agents to research the codebase first, then asks me clarifying questions. We go back and forth until it sounds right, then Claude writes plan documents split into phases so the app stays runnable after each one."

> "As we got closer to ship date, I started having Claude review its own plans. This mostly catches the main issues. Built dedicated skills for that too: /review-plan, /code-review, /retrospective, /ecs-review."

> "87 plans total, averaging 2-3 pages each. The CLAUDE.md project file is 164 lines of hard constraints learned from debugging sessions. Every constraint has a token massacre behind it."

> "The constraints were built up over time as we did the project; claude.md also got pruned several times to move things around so it references other files as claude finds it needs that information"

> "One of the biggest 'wins' is having Claude create tools that you would probably never do for a project with a deadline in ~50 days." (debug editor via Tweakpane: place objects, visualize colliders)

Research-first on hard feel problems (three.js forum): "I had claude research and write me a report and then I read it and checked some of the research and then picked which other camera types would be needed" ... "part of the research claude found was from an Iwata Asks or something similar where they discussed how some of Mario Galaxy did the gravity"

## Where Claude struggled (verbatim)
> "It defaulted to OOP in TypeScript even though the project is data-oriented ECS. Took a lot of steering to overcome. Built /ecs-plan and /ecs-review skills specifically to catch and fix this."

> "Level design failed completely. I tried making a CLI tool so Claude could help place objects in 3D space where 'down' could be anywhere. Tried elevation maps, architectural diagrams; didn't help."

> "At one point it had an index.ts that was thousands of lines long so ensuring a fast first paint was a disaster ... So I had Claude map the dependency tree and do the refactor which was a piece of cake for it."

> "The hardest problems were the camera and the gravity shadows. Both work but still have edge cases."

Commenter (silbercue): "mine [CLAUDE.md] kept growing until I'm pretty sure claude was just skipping half of it. ended up doing the same... moved verbose stuff into separate files and only kept the absolute hard rules in claude.md."

## Takeaways
- "Phases so the app stays runnable after each one" is the explicit guard against the never-playable failure mode.
- Well-known reference design (Mario Galaxy) = a ready-made spec for feel; AI research of the reference (Iwata Asks) fed the plans.
- Spatial content (level design) is where the agent failed even with custom tools — content creation remained human/borrowed (models from Hello Mario Framework).
