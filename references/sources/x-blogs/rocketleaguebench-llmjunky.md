# RocketLeagueBench (am.will, @LLMJunky) — one fixed structured spec, run against many models

- **Source URL (prompt, verbatim):** https://x.com/LLMJunky/status/2068932673838387280 (reply in the thread under https://x.com/LLMJunky/status/2068932670696952075, 2026-06-22)
- **Model/tool:** The same prompt was used as a personal benchmark ("RocketLeagueBench") across models, all in agentic coding harnesses (Codex / Claude Code):
  | Date | Model | Result (author's words) | Link |
  |---|---|---|---|
  | 2026-06-22 | Sakana "Fugu Ultra" | **FAIL**: "The game was pretty bad... Even after multiple fixes, it took 7-8 back and forth with Codex just to get it an almost playable condition. Prior to these fixes, the game was not playable." Also burned the 5-hour limit in under 1 prompt. | https://x.com/LLMJunky/status/2068932670696952075 (595k views) |
  | 2026-06-22 | GPT 5.5 xHigh | "one shot a perfectly playable game... It even nailed ball cam." Only change was a more intense boost animation. | same thread |
  | 2026-07-01 | Fable | "Fable one shot this Rocket League clone"; praised the small details (ball momentum smoke, slow-mo goal replay, tire smoke, boost pad placement, ball cam) | https://x.com/LLMJunky/status/2072441245259923884 (594k views) |
  | 2026-07-24 | Claude Opus 5 | "the best Rocket League clone i've ever seen", 27% of a Max 5x sub; follow-up prompts added practice mode, infinite boost, steering tweaks, audio | https://x.com/LLMJunky/status/2080740121398120655 (342k views, 1.9k likes); playable https://rl-opus5.vercel.app ; code https://github.com/am-will/rl-opus |
  | 2026-09-01 | Fable 5.1 | "a 2 shot prompt"; "pretty flawed on the first few passes. But it reviewed itself... 98% of the bugs that I saw earlier in the process were gone" | https://x.com/LLMJunky/status/2094894000524156946 (147k views) |
  | 2026-09-05 | GPT-6 Astra | "GAMING = SOLVED... Is RocketLeagueBench saturated? I honestly think so" | https://x.com/LLMJunky/status/2096028790925488452 (1.25M views) |
  Caveat: later posts say "Per usual, RocketLeagueBench", which implies the same prompt, but I did not confirm it was byte-identical on every run.
- **Genre:** 3D car-soccer (Rocket League-like), Three.js + Rapier
- **Quality signal:** See table. This is the closest thing to a controlled experiment in this set (fixed spec, varying model), though scoring is one person's subjective judgment.
- **One-shot vs iterative:** It is designed as a one-shot prompt; the results ranged from one-shot playable to 7-8 fix turns.
- **Related:** "Slopet League" (https://x.com/LLMJunky/status/2082173640431346058) is the same author's later build: Opus 5 + GPT 5.6 Sol, about 25 prompts over 1.5 days, in a real game engine.

## Verbatim prompt

```
Build a polished browser-based 3D Rocket League-style game using Three.js.

Goal:
Create a fully playable local web game that runs in the browser. The first screen should be the actual game, not a landing page.

Tech requirements:
- Use Three.js for rendering.
- Use a real physics engine, preferably Rapier.js, for car, ball, arena, wall, and goal physics.
- Use TypeScript if the project already supports it, otherwise plain modern JavaScript is fine.
- Use Vite for the dev server unless another stack already exists.
- Keep the architecture clean: separate rendering, physics, controls, game state, UI/HUD, and assets.

Core gameplay:
- Third-person controllable rocket car.
- Large soccer ball with believable bouncy physics.
- Enclosed arena with side walls, back walls, ceiling or high invisible bounds, and two goals.
- Score detection when the ball crosses fully into a goal.
- Reset after each goal with a countdown.
- Match timer and score display.
- Boost system:
  - Boost meter from 0-100.
  - Hold boost key to accelerate with flame/trail effect.
  - Boost drains while active.
  - Boost pads around the arena refill boost.
- Jump system:
  - Single jump.
  - Optional second jump / flip if feasible.
  - Air control with pitch, yaw, and roll.
- Car should feel responsive and arcade-like, not like a slow simulator.

Controls:
- WASD or arrow keys: drive / steer.
- Space: jump.
- Shift: boost.
- R: reset car.
- C: toggle camera mode.
- Esc or P: pause.

Camera:
- Smooth chase camera behind the car.
- Camera should follow car rotation and velocity while remaining readable.
- Optional ball-cam toggle that keeps the ball in view.

Visual design:
- Recreate a Rocket League-inspired feel, including branded-style presentation if desired.
- Add a futuristic indoor stadium, colored goals, boost pads, arena trim, and energetic UI.
- Add lighting, shadows, bloom or subtle postprocessing if performance allows.
- Add clear team colors, goal colors, boost pad glow, trail effects, ball highlight, and simple particle effects.
- Use generated, procedural, or available assets as appropriate.
- Add a readable HUD with score, timer, boost meter, countdown, and goal celebration text.
- Ensure the game works on common laptop screens and resizes correctly.

Physics feel:
- Prioritize fun over realism.
- The ball should be heavy but responsive.
- Cars should have strong acceleration, drift-friendly turning, and stable recovery.
- Avoid cars flipping uncontrollably from minor bumps.
- Tune gravity, friction, restitution, angular damping, and impulses until gameplay feels good.

AI / opponent:
- If time permits, add a simple bot opponent:
  - Bot chases the ball.
  - Bot aims roughly toward the player goal.
  - Bot can boost occasionally.
  - Bot should be beatable, not perfect.
- If bot is too risky, create a solo practice mode with two goals and a working scoreboard.

Implementation expectations:
- Build the complete working game, not just a prototype shell.
- Include all source files.
- Add brief comments only where the logic is non-obvious.
- Avoid overengineering.
- Do not create a marketing homepage.

Verification:
- Start the dev server.
- Test the game in the browser.
- Verify:
  - The scene renders.
  - The car moves, turns, jumps, and boosts.
  - The ball collides with the car and arena.
  - Goals are detected correctly.
  - Score and timer update.
  - Reset after goal works.
  - Boost pads refill boost.
  - The camera does not clip badly or lose the car.
  - No major console errors.
- Take at least one screenshot or use browser automation to confirm the canvas is nonblank.

Deliverable:
- A local runnable browser game.
- Provide the dev server URL.
- Summarize controls and what was implemented.

Quality bar:
Make it feel like an arcade sports game people would actually want to play for five minutes. Spend extra effort tuning car handling, camera smoothing, ball impact, boost feel, and goal feedback. A technically complete but boring physics demo is not acceptable.
```
