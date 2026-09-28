# WorldBuild Bench — same ~30-line game brief given to 8–9 models through one harness; blind human arena

- Reddit: https://www.reddit.com/r/ClaudeAI/comments/1uwe2id/ (r/ClaudeAI, 194 upvotes, 30 comments, 2026-07)
- HN: https://news.ycombinator.com/item?id=48994848 (Show HN, 2 points, 2026-07)
- Repo: https://github.com/sebnado/worldbuild-bench ; results/arena: https://sandscape.app/worldbuild/rounds/ai-game-benchmark-2026-07-13
- Models: Fable 5, Opus 4.8, GPT-5.6 (Sol), GLM 5.2, Grok 4.5, Kimi K3, etc. "high" thinking; custom harness with sub-agents, Three.js + Rapier + Playwright tools (test_game, play_game)
- Genre: arena combat, physics puzzle, racing (later FPS, dogfight, RTS)
- Outcome: 24–27 browser-playable games; author: "Fable did produce some of the strongest (sometimes quite a lot) games, and 5.6 really did not perform great"; "the difference between Opus and Fable was not that dramatic in some cases, yet the average cost was 68 for opus vs 252 for fable." Fable physics-puzzle run: ~$491, ~9 h.
- Session style: one-shot autonomous per brief (one run per model per brief)

## Why this is useful
It is the cleanest public example of a *pinned-concept* brief: "Task briefs pin the game concept. Each brief fixes the game's name, setting, aesthetic direction, feel, and core loop (alongside the required mechanics), so every model executes the same design ... no brief prescribes technical approach". Plus an explicit quality-bar skill and causal playtest rules.

Playtest rules (prompts/rules-playtest.md, verbatim):
> "Test causally, not just visually: test_game checks overall health; play_game lets you script real gameplay (clicks, drags, key holds, waits) and see the game state after every action. Confirm each required mechanic causes the state change the design intends — a game that looks right in screenshots can still be unplayable."
> "Keep playtesting bounded: it proves a mechanic changes state, not how it feels — real-time control, timing, and responsiveness are not observable here. Confirm each mechanic works once or twice, then stop; don't loop play_game chasing feel."

Known-bug note in playtest skill (verbatim): "Input probe passes but controls are wrong — the probe only proves keys change state, not that directions are right. Left/right inversion relative to the camera is a near-universal bug the probe cannot see: trace the sign yourself from key → rotation → on-screen direction (A moves left)."

## VERBATIM: tasks/arena-combat/TASK.md
# Arena Combat

Build **Last Stand at the Ruin**, a wave-based 3D arena combat game: the player fights
escalating waves of melee enemies inside a closed arena until every wave is cleared or
the player dies.

## Concept

A lone fighter defends a torch-lit ruined courtyard against creatures pouring in from
the dark.

- **Setting**: a crumbling walled courtyard at night — broken columns, rubble piles,
  and a handful of burning torches as landmarks; beyond the walls, darkness.
- **Aesthetic**: high-contrast night scene — warm torch and ember light against cool
  moonlit stone; enemies read as clear dark silhouettes with glowing eyes so the
  player can track a whole crowd at a glance.
- **Feel**: tense but readable crowd control — kite, turn, swing; each wave should feel
  barely survived, with health as the pressure gauge.
- **Core loop**: wave banner → fight and thin the crowd → clear the wave → short
  breather → bigger wave → victory, or a defeat worth avenging via Restart.

The concept is fixed — interpret and execute it well rather than replacing it.

## Objective

Survive and clear **3 waves** of enemies in a walled arena roughly 40×40 units.
The arena must read as a coherent space: floor, boundary walls the player cannot leave,
and enough visual landmarks to orient by.

## Required mechanics

- **Player**: third-person or top-down character moved with WASD, camera following
  smoothly. A visible attack (melee swing or projectile) triggered with Space or
  left-click, with a short cooldown.
- **Enemies**: spawn at the arena edges in 3 waves (suggested 5 / 8 / 12). They pursue
  the player and deal contact damage. Enemies die to a fixed number of player hits and
  visibly disappear (or play a death effect).
- **Health and score**: player health (100, contact damage ~10) and a kill score,
  both always visible on the HUD.
- **Wave flow**: a short banner announces each wave; the next wave starts when the
  current one is cleared.

## Win / lose

- **Win**: all 3 waves cleared → victory screen with final score and a Restart control.
- **Lose**: player health reaches 0 → defeat screen with a Restart control.
- Restart fully resets the game to wave 1 without reloading the page.

## Controls

- `WASD` move, `Space` (and/or left-click) attack.
- Control hints visible on screen at all times.

## Shared constraints (apply to every task)

- The game must run entirely from **static files** in this workspace: open `index.html`
  from a plain static file server, no build step, no server-side code.
- **No external network requests** of any kind. Use only the bundled libraries under
  `./lib/` through the import map in the provided `index.html` — Three.js, and
  optionally the Rapier physics engine (see the `threejs-game` skill).
- Implement the **`window.__bench` telemetry contract** exactly as specified in the
  `bench-telemetry` skill. Scoring is capped without it.
- Target **60 fps** on a mid-range machine; use delta-time-based movement.
- Playable immediately: visible instructions, working restart, reachable win and lose
  states. Validate with the `test_game` tool before finishing.

## VERBATIM: skills/game-quality/SKILL.md
---
name: game-quality
description: The quality bar — what separates a shippable game from a prototype — across lighting, world geometry, VFX, audio, game feel, UI, and performance. Outcomes to hit on every front, with technique families worth exploring; how you hit them is your call.
---

# The Quality Bar

You are not building a tech demo that minimally satisfies a checklist. The bar is a
game a player would voluntarily keep playing: readable at a glance, juicy to interact
with, coherent as a world. Flat-shaded boxes on a green plane do not clear that
bar. Everything runs offline from the
bundled `lib/three/` (the full `examples/jsm/` addons tree is available) and the
WebAudio API. No external assets exist — geometry, materials, and audio are all made
in code, which is a style to embrace (clean, bold, stylized) rather than apologize for.

Each section below sets the bar for one front and names technique families worth
exploring — how you hit the bar is yours to decide. Nothing ships as a placeholder:
every asset the player sees or hears — geometry, materials, music, sound — is a
final product, composed and finished to the best of your ability, not a stand-in.
For the arrangement of the world itself, see the world-design skill.

## Lighting & atmosphere (the cheapest 10x visual upgrade)

The bar: the scene reads as *lit* — a definite light direction, shadows that ground
objects, depth cues receding toward a designed sky, and a deliberate palette that
reads as art direction rather than defaults. Get color management right (output
color space, tone mapping) so the colors that ship are the colors you chose.

Worth exploring: physically-based materials and HDR lighting, image-based /
environment lighting, global-illumination approximations (ambient occlusion, light
probes), screen-space reflections, area lights, shadow mapping, fog matched to the
sky, gradient or procedural skies, emissive accents.

## Geometry & world building

The bar: shapes with designed silhouettes and materials that read as finished art
at gameplay distance — a world that looks authored, not accidental. Repeated
elements vary enough that the repetition doesn't read.

Worth exploring: procedural geometry and procedural texturing (generated color /
normal / roughness maps — made at runtime or baked to files in `assets/` during
the build), composition and sculpting of primitives, signed-distance-field
modeling, instancing and geometry merging, per-instance variation,
level-of-detail.

## VFX, shaders, post-processing

The bar: the picture *moves* — impacts burst, speed leaves traces, the objects that
matter draw the eye. Every effect serves a moment the player cares about; nothing
runs as decoration for its own sake.

Worth exploring: GPU-instanced or pooled particle systems, trails, small targeted
custom shaders where the player actually looks, a restrained post-processing chain.

## Animation & motion

The bar: things that move look alive. Locomotion reads as locomotion — parts that
should articulate do, secondary motion follows — never a statue sliding across the
floor. Motion has weight (acceleration, lean, recoil, follow-through), and births
and deaths are animated events, not object removal.

Worth exploring: procedural animation, skeletal or keyframe animation, inverse
kinematics, physics-driven secondary motion, squash and stretch.

## Audio (WebAudio, all synthesized)

Sound is a design layer, not a checklist. Decide a sonic palette that matches the
world (what does this place sound like?), let intensity follow game state (layers
and tempo rise with the stakes), keep a mix hierarchy (music ducks under SFX, SFX
under stingers), and use silence deliberately. Aim for music and effects that sound
produced — composed, layered, mixed; a player should assume they are hearing
crafted audio, not raw oscillators.

Environment facts: one `AudioContext`, unlocked on the first user input (browsers
block autoplay before a gesture); route everything through a master gain.

Worth exploring: synthesis for SFX (subtractive, FM, physical modeling),
spatial/positional audio, convolution reverb (impulse responses can be generated in
code), generative or adaptive layered music, mapping continuous sounds to game
state, randomized variation so repeated sounds don't fatigue.

## Game feel ("juice") — the difference players actually notice

The bar: every interaction acknowledges the player. Nothing pops into existence
unanimated, nothing important happens without feedback the player can feel, and the
big moments (wins, losses, near-misses) have anticipation and payoff.

Worth exploring: reactive cameras (smoothed follow, speed response, impact shake),
spring-damper motion, tweened transitions, layered hit feedback (visual, camera,
and audio landing together).

## UI/HUD

The bar: every state — menu, countdown, playing, paused, won, lost — is a designed
screen with readable hierarchy, never an `alert()` or raw unstyled text. Values the
player watches visibly react when they change. (A DOM overlay usually out-typesets
canvas text for the same effort — your call.)

## Performance (60 fps is a feature)

The bar: a steady frame rate on a mid-range machine, verified in a playtest —
`renderer.info.render.calls` tells the truth about draw calls.

Known traps: movement must be delta-time-based, with dt clamped so a backgrounded
tab doesn't teleport physics on return; per-frame allocations in hot loops kill
frame pacing — pool and reuse; unbatched repeated geometry multiplies draw calls.

## Scope discipline

If you cannot finish everything well, cut whole features cleanly — fewer things,
finished — instead of shipping everything at prototype quality.

## VERBATIM: prompts/rules-playtest.md
- Test causally, not just visually: test_game checks overall health; play_game lets you script real gameplay (clicks, drags, key holds, waits) and see the game state after every action. Confirm each required mechanic causes the state change the design intends — a game that looks right in screenshots can still be unplayable.
- Keep playtesting bounded: it proves a mechanic changes state, not how it feels — real-time control, timing, and responsiveness are not observable here. Confirm each mechanic works once or twice, then stop; don't loop play_game chasing feel. Spend that time building and polishing the game and its UI/flow.
