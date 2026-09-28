# Gothicvania Codex Demo — 2D Castlevania-style platformer, Codex CLI + agent skills, zero human code

- HN: https://news.ycombinator.com/item?id=47034752 (Show HN, 10 points, 10 comments, 2026-02-16)
- Repo (GDD + skills + PROGRESS.md): https://github.com/acatovic/gothicvania-codex-demo ; Play: https://acatovic.github.io/gothicvania-codex-demo/ ; HN Arcade: https://hnarcade.com/games/games/gothicvania
- Model/tool: OpenAI Codex CLI (GPT-5.3-Codex listed as co-author of design doc), agent skills with progressive disclosure, playwright-cli
- Genre: single-level side-scrolling melee platformer (Phaser)
- Outcome: SUCCESS (small scope): playable level, title/pause, 2 enemy types, SFX/music, win screen. Human-made assets (ansimuz pack) and human-made level in Tiled.
- Session style: MULTI-PROMPT (~10 prompts over "a couple of hours"); author states one-shot is NOT sufficient for this scope.

## Key claims (author, verbatim)
> "One-shot prompt/game dev agent will basically get the game up and running, with some basic level and player mechanics. Codex is currently unable to (even on the highest setting) perform a fully valid game creation using all the skills, the design document, and the full game development harness - at least not for a game such as this ("snake game" should be ok!)."

> "Essentially, without this implement() -> evaluate() cycle, you are simply feeling around in the dark."

> "It was absolutely magical watching Codex implement a feature then automatically open a web browser window and speed-play the game to validate the said feature. The best part was when it found problems - such as when it found one of the enemies floating in the air, so it went back to implement proper gravity controls."

> Progressive prompting order: "1. Get the game up and running with background and full player mechanics 2. Add the tiles/level map into the game 3. Add the enemies/NPCs with player->NPC dynamics, i.e. 'hurt', 'die', 'destroy enemy', 'reset level' 4. Add the title and pause menu as well as help/instructions 5. Add the sfx and music. In between I had to take some screenshots and feed it to Codex to implement fixes, i.e. collision detection errors, give more 'intelligence' to NPCs, etc."

> (HN reply on Playwright checks) "I just told codex to use playwright cli, told it what to check (in plain English), and it did its thing. Looking at its log I can see that it was 'playing' the game and defining its own test conditions ... it uses CLI to read all the x,y coordinates, speed, timing, it took screenshots, and combined those together. My learning from this is - just let the agent do it. Actually trying to interfere with specific conditions and checks lowers the agent's performance. Simply give it a guide."

> On taste: "I don't have any professional experience ... Also I've been playing games all my life so have a feeling for what's important - collision detection, walkable/collidable areas, speed/timing, some basic NPC logic etc."

Assets: "I tried different models (GPT-5.2, Gemini, Flux) to create sprites - we are not there yet."

NOTE: WORKFLOW.md/TESTING.md closely mirror OpenAI's published "develop-web-game" Codex skill (render_game_to_text hook, "implement -> act -> pause -> observe -> adjust").

## VERBATIM: DESIGN-DOCUMENT.md, SKILL.md, WORKFLOW.md, TESTING.md
#### DESIGN-DOCUMENT.md
---
title: Gothicvania Codex Demo
project: gothicvania-codex
document: DESIGN-DOCUMENT.md
version: 0.1.0
status: active
last_updated: 2026-02-14
authors: Armin Catovic, GPT-5.3-Codex
---

# Gothicvania Design Specification

## Table of Contents

```
1. Purpose and Scope
2. Technical Foundation
3. Story
4. Game Composition
4.1 Main Menu
4.2 Level Composition
5. Game Mechanics
```

## 1. Purpose and Scope

This document defines the target structure and behavior of the current gothic side-scrolling combat platformer implemented in Phaser game engine.

Primary scope:
- One sandbox scene with a long horizontal level.
- A controllable melee player with jump and action states.
- Two enemy archetypes (wizard and burning ghoul) plus projectile threat.
- Layered gothic environment with explicit foreground/mid/far depth composition.
- Tile-based walkable and non-walkable foreground, including elevated reachable routes.
- Start menu / title screen as well as a pause screen; control indicators
- Action sound effects

Out of scope:
- Save system, multi-level progression, music soundtrack and narrative flow.

## 2. Technical Foundation

- Engine: Phaser
- Runtime: Single page app (`index.html`) with one Phaser game instance
- Size and Positioning: 336 x 224 pixels, centered in the middle of the screen/page
- Other: pixel graphics without antialiasing but with round pixels; game is centered in the middle of the screen
  and can be maximized to full screen - Phaser takes care of proper scaling so all the proportions remain the same

## 3. Story

Single level Castlevania-style no-narrative game where the player is a monk with nifty martial arts skills
who punches and kicks his way through gothic monsters (ghouls and flame throwing wizards). When the player reaches the
last (right-most) pixels of the level, the game is over. The player is presented with a small "Well Done" screen.

## 4. Game Composition

### 4.1 Main Menu

When the game starts, the user is presented with a title screen and slowly flashing "press enter" text below it.
In the background/behind the title screen there is a slow but smooth moving (repeated) background imagery, consisting
of the far background images and columns super-imposed. All these images should be used from the images folder.

When the user hits the ENTER key the game begins - the level is generated with all the sprites and the player
presumes control.

When the user hits ESC kep the game is paused with "PAUSED" message written in small pixel font, in the dead center
of the screen.

### 4.2 Level Composition

The level is a long level going from left to right. The player starts on the far left hand side.
There are no visible enemies until the player starts moving to the right after some time.

The level is layed out in three layers with a strong sense of depth and parallax effects:

- Far background layer that is repeating left-right
- Mid background layer with large columns superimposed on the far background layer, also repeating left-right
- Foreground layer with the tiles, the player and the enemies/NPCs

When it comes to the tiles follow the tilemap configuration and the relevant tiles png.

In the top right hand corner of the screen is the player health. There will be four pixel-graphics style red hearts
representing the player's health.

Enemies will be scattered randomly throughout the level, but at sufficient distance and always placed on top
of the collidable tiles.

## Game Mechanics

There is overall very smooth mechanics to both the player and the enemies.

The player controls are:

- W: jump
- S: crouch
- A: move left (and face left)
- D: move right (and face right)
- J: action key - it will randomly select punch or kick
- Combos: player can jump and kick

When enemies fire or attack the player, it is at slow-to-medium speed. The fireballs should be at
player's head height.

The enemies are always facing the player and attacking in his direction. If the player jumps over them, they turn
to face him.

The player should always be grounded on blocks/tiles - he should never be "floating" in mid air. If he jumps on the blocks
he should land on them properly and with conviction.

When the player jumps or attacks there should be a sfx, and similarly when he is hurt, or when an enemy is destroyed.

When the player gets hit, he will lose one of his health hearts.

When it comes to the actual collision with the player, it should be basically right into him, i.e. it shouldn't be that it's
"near him", but really it should be entering into his frame.

#### .agents/skills/game-dev/SKILL.md
---
name: "game-dev"
description: "Used when building or iterating during a game development process."
---

# Instructions

This document serves as a high-level map for executing game development skills.
Each set of skills is described in a dedicated `*.md` file as listed below:

* `PREREQUISITES.md` specifies the environment configuration and any pre-requisites that need to be met; this is the first place we need to look at.
* `WORKFLOW.md` describes the general game development workflow and should be referred to periodically as needed.
* `GAME-ENGINE.md` documents the game engine and APIs; it may also simply refer to external documentation.
* `ASSETS.md` describes how the various game assets and config should be used, i.e. sprites/atlas, tiles, backgrounds, sounds.
* `TESTING.md` describes how the game shall be run/tested/evaluated.

#### .agents/skills/game-dev/WORKFLOW.md
# Workflow

Build a game in small steps and validate every change. Treat each iteration as: implement -> act -> pause -> observe -> adjust.

Keep referring to `$GAME_ROOT/DESIGN-DOCUMENT.md` since this specifies the implementation details, the story, the logic, and the overall
look and feel of the game.

Initialize and keep up to date a development log inside `$GAME_ROOT/PROGRESS.md`; this should contain what works, what doesn't, TODOs, and key
implementation decisions.

The general workflow sequence should be as follows:

1. **Read the DESIGN-DOCUMENT.md.**. Understand what the game is trying to achieve and ensure the current implementation adheres to the design spec.
2. **Pick a goal.** Define a single feature or behavior to implement.
3. **Implement small.** Make the smallest change that moves the game forward.
4. **Udate PROGRESS.md.** If `PROGRESS.md` exists, read it first and confirm the original user prompt is recorded at the top (prefix with `Original prompt:`). Also note any TODOs and suggestions left by the previous agent. If missing, create it and write `Original prompt: <prompt>` at the top before appending updates.
5. **Dry-run the game loop.** Use any necessary tools to run or simulate the game loop with the latest implementation changes.
6. **Inspect state.** Capture the state (logs, screenshots, outputs) during the dry-run.
7. **Verify controls and state (multi-step focus).** Exhaustively exercise all important interactions. For each, think through the full multi-step sequence it implies (cause → intermediate states → outcome) and verify the entire chain works end-to-end. If anything is off, fix and rerun. Examples of important interactions: move, jump, shoot/attack, interact/use, select/confirm/cancel in menus, pause/resume, restart, and any special abilities or puzzle actions defined by the request. Multi-step examples: shooting an enemy should reduce its health; when health reaches 0 it should disappear and update the score; collecting a key should unlock a door and allow level progression.
8. **Check errors.** Review console errors and fix the first new issue before continuing.
9. **Reset between scenarios.** Avoid cross-test state when validating distinct features.
10. **Iterate with small deltas.** Change one variable at a time (frames, inputs, timing, positions), then repeat steps 3-9 until stable.

#### .agents/skills/game-dev/TESTING.md
# Testing / Running

3) Run the game locally
- Start a local web server from the project root:
  python3 -m http.server 8000
- Game URL:
  http://127.0.0.1:8000

4) Open a Playwright browser session
- Use a named session so you can run multiple commands against the same browser:
  npx playwright-cli -s=gothic open http://127.0.0.1:8000 --headed

5) Basic game-loop test flow
- Capture a screenshot:
  npx playwright-cli -s=gothic screenshot --filename output/playwright/smoke-1.png
- Press keys for menu/game start:
  npx playwright-cli -s=gothic press Enter
  npx playwright-cli -s=gothic press Enter
- Check in-game state text hook:
  npx playwright-cli -s=gothic eval "() => window.render_game_to_text()"
- Move player for a short interval:
  npx playwright-cli -s=gothic keydown d
  npx playwright-cli -s=gothic eval "async () => { await new Promise((r) => setTimeout(r, 600)); return window.render_game_to_text(); }"
  npx playwright-cli -s=gothic keyup d
- Test jump / attacks:
  npx playwright-cli -s=gothic press w
  npx playwright-cli -s=gothic press j
  npx playwright-cli -s=gothic press k
- Capture another screenshot:
  npx playwright-cli -s=gothic screenshot --filename output/playwright/smoke-2.png

6) Useful checks for this project
- Current scene + status:
  npx playwright-cli -s=gothic eval "() => window.render_game_to_text()"
- Pause/resume:
  npx playwright-cli -s=gothic press Escape
  npx playwright-cli -s=gothic press Escape
- Force a scripted probe:
  npx playwright-cli -s=gothic run-code "(async (page) => { return await page.evaluate(() => window.render_game_to_text()); })"

7) Clean up
- Close Playwright session:
  npx playwright-cli -s=gothic close
- Stop local server (Ctrl+C in server terminal)

Notes
- Keep screenshots under:
  output/playwright/
- If element refs become stale, run:
  npx playwright-cli -s=gothic snapshot
- If a browser session is stuck:
  npx playwright-cli kill-all

## Test Checklist

Test any new features added for the request and any areas your logic changes could affect.
Identify issues, fix them, and re-run the tests to confirm they’re resolved.

Examples of things to test:

- Primary movement/interaction inputs (e.g., move, jump, shoot, confirm/select).
- Win/lose or success/fail transitions.
- Score/health/resource changes.
- Boundary conditions (collisions, walls, screen edges).
- Menu/pause/start flow if present.
- Any special actions tied to the request (powerups, combos, abilities, puzzles, timers).

