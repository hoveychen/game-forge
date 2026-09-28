# Godogen — Claude Code/Codex skills pipeline that builds complete Godot (later Bevy/Babylon) games from a text prompt, with visual QA loop

- HN: https://news.ycombinator.com/item?id=47400868 (Show HN, 337 points, 2026-03)
- Repo: https://github.com/htdt/godogen ; demo video: https://youtu.be/eUz19GROIpY ; demo prompts: docs/demo_prompts.md
- Model/tool: Claude Code (Max) / Codex; Gemini/Grok images, Tripo3D 3D; Gemini Flash for visual QA
- Genre: generator (demos: top-down rally, 2D side-scrolling cyclist dodger, 3D snowboarding, nature scene)
- Outcome: PARTIAL SUCCESS — produces playable projects end-to-end; author concedes "these demos are essentially raw single-run output, not cherry-picked or polished. The goal was showing the pipeline works end-to-end, not producing a finished game." ~1 year, 4 major rewrites.
- Session style: autonomous pipeline (one prompt -> decomposition -> forked-context tasks -> visual QA)

## Author on what made it work (verbatim, HN)
> "Getting LLMs to reliably generate functional games required solving three specific engineering bottlenecks: 1. The Training Data Scarcity: LLMs barely know GDScript ... I built a custom reference system: a hand-written language spec, full API docs converted from Godot's XML source, and a quirks database for engine behaviors you can't learn from docs alone ... the agent lazy-loads only the specific APIs it needs at runtime. 2. The Build-Time vs. Runtime State ... 3. The Evaluation Loop: A coding agent is inherently biased toward its own [work] ..." (OP truncated in API)

> (reply to a failed RPG attempt) "That's exactly the failure mode this project exists to solve. The core issue is Claude Code has no way to see what it's producing — code compiles fine but assets are floating, paths lead nowhere, layouts are garbage. It even told you as much. Godogen closes that loop: after writing code, it captures screenshots from the running engine and a vision model evaluates them. That's the difference between 'compiles but broken' and 'actually playable.' And yes — providing design docs helps a lot. The pipeline generates those automatically (visual reference, architecture, task plan)"

> "That was actually my starting point — generating Three.js output that looked okay-ish but broke the moment you touched anything. Godot gives you a real engine with physics, scene trees, which is why the output is more robust even if it's far from polished."

> "the decomposer identifies genuinely hard elements (custom physics, procedural generation) and those get dedicated testing. Routine stuff like movement or UI doesn't, since the visual QA already catches most breakage there."

> "each task runs in a forked context, a bad lookup doesn't cascade beyond that task."

Cost: "~$1–3 for a full game generation run if you were paying API rates" + assets; "snowboarding game ... roughly $5–8 all-in".

## The failure it was answering (HN commenter andreagrandi, verbatim)
> "I tried using Claude Code to build an RPG game with Godot and GDScript, using free to use assets: a total failure :/ ... I asked Claude to first produce a one area demo, so I could test the assets ... First it produced some garbage using the assets randomly. Then it tried to copy from an existing demo but it had not idea where a door or a path were and at a certain point it even admitted it with something like: 'I can't design an usable and nice area: I either make it functional and ugly or I copy and adapt the existing demo but I will have no clue about what is what'"

Other commenters: vblanco (Daggerfall-like procedural RPG, 60k LOC): "you dont do one prompt to do the entire game, but 'decent' style vibecoding where you do things little by little ... make some documentation about the axis systems and core classes ... set your claude.md to point at the godot source code so that the bot can doublecheck things." Ariarule: "just a CLAUDE.md file, the project itself, and going through plan mode before each change. I did start from a playable project with a fair amount of hand-written scaffolding already in place".

## Note on spec style of the demo prompts
Each demo prompt is ~150–300 words, written as a player-experience description: named "core feel" section, concrete numbers (max 25 km/h, 4 lanes, ~250px sprites), explicit exclusions ("No coins or power-ups — just survival"), explicit "pure eye candy, no interaction" labels, one core risk/reward named ("moving into oncoming lanes risks hitting approaching cyclists — the core risk/reward"), and the lose/restart loop specified.

## VERBATIM: prompts/runtime.md (runtime manifest)
# Build ${ENGINE_NAME} game from a description

- Keep durable project status in `README.md`: what is built, what is left, and an asset table.
- Generate visual assets with `${ASSET_SKILL_COMMAND}`. Confirm the spend with the user before the first paid generation.
- Read `${ENGINE_GUIDE_FILE}` for engine guidance: stack, project layout, how to run, and how to capture.

## Delivery

Judge progress from the running game, never from a clean build: verify the structural things yourself (it loads, no errors, assets present) and let what you see drive the next iteration.

Decide from how the task is framed how to work. A task that invites collaboration — open-ended, exploratory, phrased as a direction rather than a spec — gets the live game early: checkpoint at decisions of taste, scope, or cost, and build freely in between. A task handed over as a finished brief to execute gets reasonable calls and steady progress, no blocking. Either way the result is proven, not claimed — if the user hasn't seen it running, finish with a 15–20s video of the game in action, and watch it back before you call the work done.

## VERBATIM: docs/demo_prompts.md
# Demo Prompts

## CartoRally

```text
Top-down racing game with a stylized topographic map aesthetic. Terrain rendered with visible contour lines following elevation changes, spaced tighter on steep slopes and wider on flat areas. Muted earthy color palette: cream/parchment base, sage green for lowlands, tan/brown for mid-elevation, grey-white for peaks. The racing track is a bold saturated line (burnt orange or red) cutting through the terrain, with subtle road markings. Trees represented as simplified symbolic markers — small clustered circles in dark green, like map legend symbols. Mountain border walls rendered as dense contour bundles with hatch shading. Subtle paper texture overlay across the entire scene. Elevation communicated through both 3D geometry and contour line density. Clean, minimal, highly readable. Visual references: topographic hiking maps, ordnance survey maps, vintage cartography with a modern minimal twist.
Terrain is a heightmap with distinct elevation changes — rolling hills create natural ramps where the car launches into the air and lands with impact. Track conforms to the terrain surface, following contours over hills and through valleys. Car physics emphasize verticality: visible airtime on crests, shadow separation from ground during jumps, suspension compression on landing. High mountain walls enclose the scene as natural borders. Closed-loop circuit with a natural winding layout through varied elevation.
```

## Ultra Realistic Nature Scene

```text
Generate a serene riverbank nature scene combining HQ 3D models with procedural shaders.
Scene elements:
River with shader-based water (reflection, refraction, flow, edge foam)
Riverbank with shader-blended ground (grass/dirt/mud transition)
Procedural grass with wind-animated vertex shaders
One tree — modeled trunk/branches, shader-driven leaf cards with wind sway and translucency
Forest backdrop behind the river (simple tree silhouettes or billboard impostors)
Old small wooden boat (3D model, weathered look)
Fallen log on the bank (3D model)
Technical split:
Models: boat, log, tree trunk/branches, rocks
Shaders: water surface, grass, leaves, ground blending, wind animation
Visual targets: Natural lighting (directional sun + ambient), soft shadows, subtle fog/atmosphere for depth.
```

## Amsterdam Cyclist

```text
A 2D side-scrolling cyclist game, left to right, with lane switching, slow and relaxed in pace. You ride through Amsterdam on a red bike lane — 4 horizontal lanes stacked vertically: two bottom lanes for your direction, two top lanes with oncoming traffic. Tourists jump onto the bike lane from gray sidewalks (top and bottom edges) as obstacles; three caricature types: the Selfie Walker (phone up, completely oblivious), the Lost Map Reader (spinning confused, giant map unfolded), and the Tulip Hauler (struggling to see past a comically huge bouquet of tulips, drifting blindly). You dodge by switching lanes vertically; moving into oncoming lanes risks hitting approaching cyclists — the core risk/reward. Lane switching is discrete with smooth lerp, max speed caps at 25 km/h — the vibe is chill Amsterdam cruising that slowly gets chaotic.
Three-layer parallax: canal water at the bottom scrolls fastest, road/bike lanes at medium speed, townhouse facades along the top slowest. The canal is visually rich — animated dark water with ripple highlights, and varied boats drifting past: classic sloepen with passengers, houseboats with rooftop plants, tourist canal boats, an occasional rower. Boats vary in size and speed, some overlapping — pure eye candy, no interaction. Road markings (dashed center line, bike symbols, arrows) are baked into the road tile texture, not separate objects. Sidewalks have a subtle brick pattern. All sprites stay small (~250px) with bold simple shapes, thick outlines, flat filled colors — chunky and iconic, readable at a glance.
The cyclist has a pedaling animation loop. Each tourist type has a distinct animation: Selfie Walker shuffling with phone raised, Map Reader spinning in place, Tulip Hauler swaying with the bouquet bobbing. Art style: flat colored sprite illustrations, clean and cartoony. HUD shows distance and speed; game over screen with final score and restart. Controls: W/S or Up/Down to switch lanes. No coins or power-ups — just survival as tourist density gradually increases.
```

## 3D Alpine Snowboard Simulator

```text
A downhill snowboarding game set in an Alpine ski resort.
World: A long slope descending with gentle undulations. A curvy groomed track winds down the center, flanked by powder snow zones on both sides — visually distinct, and entering them heavily dampens speed. Scattered along the track are ramp-shaped kickers that launch the rider airborne when hit with speed.
Obstacles: Slow-moving skiers (simple figures) drift downhill on the track. Snowy pine trees with white snow caps line the edges and occasionally encroach onto the track. Collision with either means crash and game over with restart option.
Snowboard physics — the core feel: The rider stands sideways on a board. Left/Right input carves by tilting onto the heel edge or toe edge — lean the whole model into the turn and gradually arc the heading. Turns should feel carved with angular momentum, not instant snaps. Sharper carves scrub more speed. No input means neutral glide with gravity acceleration. Airborne means preserve momentum plus gravity.
Snow spray: Sharp carves spawn a burst of white particles fanning out from the board's outside edge, rising slightly and fading quickly. Harder carve means bigger spray. This should feel satisfying and punchy.
Camera: Third-person chase cam behind and above the rider, smooth-following with slight lag, gently swinging on turns.
Scenery: Panorama image. At the bottom of the slope, a charming Alpine village — clustered wooden chalets with snowy roofs, a small church steeple. Behind it, jagged snow-capped mountain peaks on the horizon. Clear winter blue sky with warm sun glow on one side. Directional sunlight with soft shadows.
HUD: Speed, run timer. Minimal, not intrusive.
```
