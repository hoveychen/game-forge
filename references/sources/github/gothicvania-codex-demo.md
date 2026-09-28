# GothicVania Codex Demo — Phaser 2D gothic platformer, Codex CLI + custom `game-dev` agent skill, ~10 prompts

- Repo: https://github.com/acatovic/gothicvania-codex-demo  (play: https://acatovic.github.io/gothicvania-codex-demo/ ; featured on HN Arcade https://hnarcade.com/games/games/gothicvania)
- Stars: 24. 9 commits. Few hours total ("sandbox level in under 30 minutes", then a couple more hours polish).
- Tool/model: OpenAI Codex CLI (GPT-5.x-codex, "even on the highest setting"), agent skills in .agents/skills/game-dev/.
- Genre: side-scrolling action platformer, one level (Tiled map), enemies, title/pause menus, sfx + music.
- Result evidence: live playable GH Pages build, gameplay video in README, HN Arcade feature. Art/audio/level map human-made (ansimuz asset pack, Tiled) — AI wrote all code.
- One-shot vs multi-session: ~10 prompts of "progressive prompting". Author explicitly: "One-shot ... will basically get the game up and running with some basic level and player mechanics. Codex is currently unable ... to perform a fully valid game creation using all the skills, the design document, and the full harness — at least not for a game such as this ('snake game' should be ok!)."
- Progressive prompt sequence (author's): 1) background + full player mechanics → 2) tiles/level map → 3) enemies/NPCs with hurt/die/destroy/reset → 4) title + pause menu + help → 5) sfx + music. Plus screenshot-fed fix prompts (collision errors, NPC intelligence).
- Notable process practices:
  - "Harness engineering + progressive disclosure": SKILL.md is only a table of contents → PREREQUISITES / WORKFLOW / ASSETS / GAME-ENGINE / TESTING ("CRITICAL!").
  - Living PROGRESS.md as memory "so it doesn't consume context with things that don't work".
  - implement() → evaluate() loop with Playwright speed-playing the game; found a floating enemy and went back to add gravity. "Without this cycle, you are simply feeling around in the dark."

---
## Verbatim: DESIGN-DOCUMENT.md
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


---
## Verbatim: .agents/skills/game-dev/SKILL.md
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


---
## Verbatim: .agents/skills/game-dev/WORKFLOW.md
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


---
## Verbatim: .agents/skills/game-dev/TESTING.md
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


---
## Verbatim: .agents/skills/game-dev/ASSETS.md
# Assets

The assets generally fall into the following structure:

```
assets/
  images/
    backgrounds/
    misc/
  tilemaps/
    tiles/
    maps/
  spritesheets/
  audio/
    sfx/
    music/
  fonts/
```

If the assets structure within `$GAME_ROOT/` directory does not follow the above then try
to infer it on your own.

## Images and Backgrounds

These are typically `.png` files and are used as-is without any extraction.
Backgrounds are typically just joined/repeated together left-to-right. There may be "far" backgrounds, and backgrounds closer to the player
(e.g. columns or walls) that are overlayed on top of the far backgrounds. These may require different scaling and parallax effects.
Backgrounds should **NOT** be joined/repeated vertically (up-down).

Misc images contain menus, pause screens, instruction screens, game over screens, etc.
Similar to backgrounds, these are used as-is, i.e. no specific extraction nor configuration is required.

## Tilemaps and Tilesets

Tilemaps consist of both `.png` files (in the `tiles/` folder) as well as corresponding JSON configuration files
(in the `maps/` folder). The JSON configuration is a map export from Tiled Map Editor. It specifies the metadata
in terms of the width and height of a level (in number of tiles), and tile size. It also provides an array of
tile placements and various properties associated with the tiles, such as whether they are collidable (e.g. whether
the player/NPCs can stand on them, or collide with them). This map should be used for level layout (superimposed on
the backgrounds) and for guiding the placement of NPCs and player movement.

- X-position
- Y-position
- Width (in pixels)
- Height (in pixels)
- Whether the tile is "collidable", i.e. whether the player, enemies and NPCs can "stand" on the tile, or
  bump into the tile
- Description specifying any other details important to consider during the game implementation


## Spritesheets

Spritesheets consist of both `.png` files as well as corresponding JSON configuration files.
The JSON configuration specifies different sprite movements/frames and their properties. The properties include:

- X-position
- Y-position
- Width (in pixels)
- Height (in pixels)

The sprite frame name identifies the type of sprite, the movement, and the sequence number. E.g. "player-jump-0" means
it's a player jump sequence, first frame.

Example:

```json
...
  "player-flying-kick-0": { "x": 328, "y": 0, "w": 82, "h": 60 },
  "player-flying-kick-1": { "x": 410, "y": 0, "w": 82, "h": 60 },
...
```

## Fonts

Use the fonts in the `assets/fonts` folder.

## Audio

Audio is split into sound effects (`sfx/` directory) and music (`music/` directory).
The sfx should be named accordingly (e.g. "hurt", "kill", "jump", etc), if not try to infer based on `DESIGN-DOCUMENT.md` or
developer instructions.


---
## Verbatim: .agents/skills/game-dev/PREREQUISITES.md
# Pre-Requisites

## Phaser Game Engine Installation

We use Phaser JS game engine.

To install Phaser simply add *either* of the following to index.html:

```html
<script src="//cdn.jsdelivr.net/npm/phaser@3.86.0/dist/phaser.js"></script>
```

or

```html
<script src="//cdn.jsdelivr.net/npm/phaser@3.86.0/dist/phaser.min.js"></script>
```

## Node and Playwright Installation.

1. Ensure Node.js + npm are installed:

```
node --version
npm --version
```

2. Install Playwright in this project. From the project root:

```
npm install -D @playwright/cli
npx playwright install
```

3. Create a Playwright config

```
npx playwright init
```


---
## Verbatim: .agents/skills/game-dev/GAME-ENGINE.md
# Game Engine

We use Phaser JS game engine.

Refer to https://docs.phaser.io/phaser/getting-started/making-your-first-phaser-game to get an overview
on all the different pieces required to put a game together.

For more detailed documentation on animations, actions, input, physics, etc, refer to https://docs.phaser.io/ and
perform a rigorous search.

For loading tilemaps/tilesets in Phaser, use `load.image('tiles' ...)` and `load.tilemapTiledJSON('map', ...)`.


---
## Excerpt: PROGRESS.md (first 120 of 463 lines)
Original prompt: Implement a single level according to the DESIGN-DOCUMENT and $game-dev skills. For now focus only on the level setup (backgrounds and tiles) and the correct player mechanics. No enemies.

## 2026-02-15

- Created a runnable Phaser SPA with centered 336x224 canvas, pixel-art settings, and scaling.
- Added a title scene with moving background/columns and Enter-to-start flow.
- Implemented one gameplay level scene with:
  - Repeating far/mid parallax backgrounds.
  - Tilemap foreground loaded from `assets/tilemaps/maps/map.json`.
  - Collision enabled from tile `collides` properties.
- Implemented player mechanics only (no enemies):
  - Move left/right (`A`/`D`) with facing direction.
  - Jump (`W`) with jump SFX.
  - Crouch (`S`) on ground.
  - Attack (`J`) randomly picks punch/kick on ground, flying kick in air, with attack SFX.
  - Combo behavior support: jump + attack triggers air kick animation.
  - Pause toggle (`ESC`) with centered `PAUSED` text.
- Added top-right heart HUD (4 hearts) and debug hooks:
  - `window.render_game_to_text()`
  - `window.advanceTime(ms)`
- Validation done:
  - `node --check main.js` passed.

### Follow-up Prompt

- Add wizard enemies with fireballs, hurt/destroy mechanisms, and game-over/restart behavior.

### Follow-up Updates

- Added wizard + fireball + enemy-death asset loading and animation setup.
- Spawned wizard enemies across the level on collidable tile surfaces.
- Implemented wizard AI casting loop:
  - Wizards face the player.
  - Wizards periodically cast and spawn head-height fireballs toward the player.
- Implemented enemy hurt/destroy flow:
  - Player attacks now damage wizards.
  - Wizards flash on hit, die at 0 HP, and play death animation + kill SFX.
- Implemented player hurt flow:
  - Fireballs and direct wizard contact damage player hearts.
  - Added invulnerability window and hurt reaction.
- Implemented full game-over flow:
  - Triggered when hearts reach 0.
  - Triggered when player falls below the level (through floating gaps).
  - Displays `GAME OVER` and `PRESS ENTER TO RESTART`.
  - ENTER restarts the level scene.
- Validation done:
  - `node --check main.js` passed.

### TODO

- Tune collision body and movement feel against full gameplay expectations after visual/interactive playtesting.
- Add remaining design elements in a later step (additional enemy archetypes, end-of-level/win state, polish pass).

### Follow-up Prompt

- Fix enemies/fighting sequence so enemies always face player direction, player hits trigger enemy death sequence, and enemy hits trigger player hurt sequence.

### Follow-up Updates

- Combat flow updates in `main.js`:
  - Enemies now consistently sync facing direction against player position every frame (`syncWizardFacing`), including overlap/tie fallback behavior.
  - Wizard health was reduced to `1` so a successful player strike immediately starts enemy death sequence/animation.
  - Player hurt handling now has an explicit hurt-sequence window (`playerHurtUntil`) so enemy/fireball impacts force hurt animation reliably.
  - Enemy overlap logic now only skips player hurt when the current overlap is a valid player hit; otherwise enemy contact damages player.
  - Player hurt now clears current attack state to ensure hurt sequence is not suppressed by attack animation state.
- Validation done:
  - `node --check main.js` passed.
  - Playwright runtime checks passed for:
    - Enemy facing flip behavior when moving player from left side to right side of enemy (`wizardFlipX: true -> false`).
    - Player hit reducing active wizard count from `2` to `1` and starting death sequence sprite.
    - Enemy overlap reducing player health (`4 -> 3`) and forcing `player-hurt` animation with active hurt-sequence timer.

### Follow-up Prompt

- Fix visual scaling so player and enemies are larger and closer to reference proportions.

### Follow-up Updates

- Increased character scales in `main.js`:
  - `PLAYER_SCALE`: `0.58 -> 0.9`
  - `WIZARD_SCALE`: `0.62 -> 0.92`
- Increased wizard foot placement offset to keep enemy grounding correct with larger scale:
  - `WIZARD_FOOT_OFFSET`: `21 -> 31`
- Validation done:
  - `node --check main.js` passed.
  - Playwright screenshot captured for visual verification: `output/playwright/scale-fix-side-by-side.png`.

### Follow-up Prompt

- Enemy sprite is scaled correctly now, but still facing away from player while attacking.

### Follow-up Updates

- Corrected wizard visual facing rule in `syncWizardFacing` to match sprite authoring direction.
  - Wizards now face toward the player while still firing in the player's direction.
- Validation done:
  - `node --check main.js` passed.
  - Playwright screenshots verify both directions:
    - `output/playwright/enemy-facing-fixed-left.png`
    - `output/playwright/enemy-facing-fixed-right.png`

### Follow-up Prompt

- Hearts disappear after player death/restart; reset HUD to initial 4 hearts state on restart.

### Follow-up Updates

- Fixed heart HUD lifecycle on scene restart:
  - Reset `heartGraphics` reference at scene `create()` start so restart never reuses stale graphics instance.
  - Hardened `drawHearts()` creation guard to recreate graphics when the existing reference is not attached to the active scene.
- Validation done:
  - `node --check main.js` passed.
  - Playwright restart-cycle check confirms post-restart state includes `health: 4` and visible heart HUD:
    - `output/playwright/hearts-initial.png`
    - `output/playwright/hearts-after-restart.png`

### Follow-up Prompt

- While crouching, player should remain in crouch mode and not start kick/punch attack.

