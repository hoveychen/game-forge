# Pocket Bomber — Love2D Bomberman (desktop + iOS), Claude Code + Love2D agent skill

- Repo: https://github.com/chongdashu/love2d-pocket-bomber-game  (YouTube build: https://www.youtube.com/watch?v=B8cRapWSGeI)
- Stars: 17 (author Chong-U / "AI Oriented", whose other vibe-coded game repos have 30–150 stars)
- Tool/model: Claude Code + custom Love2D gamedev skill + iOS build skill
- Genre: grid action (Bomberman clone), 5 handcrafted levels, 3 enemy types, touch controls, high score
- Result evidence: README gameplay GIF, full video of build, shipped to iOS in video. Repo squashed to 2 commits (so no commit-level history).
- One-shot vs multi-session: spec-first pipeline: GDD (420 lines, generated with TinyPRD-style template) → TDD (1,937 lines incl. pseudocode, implementation order, testing checklist) → Claude plan-mode plan (plans/sleepy-herding-garden.md, 5 phases, file-by-file) → implementation in one or a few sessions.
- Notable process practices:
  - GDD has an explicit "Assumptions" block up top that kills scope ambiguity (engine version, shapes-only visuals, no procedural gen, no powerups, restart rules, save file name).
  - Everything numeric: tile 48 px, 960x540 logical res, safe margins, touch zone coords, 8+ hex palette, fuse 2.0s, 0.12s explosion grace window, speeds.
  - TDD ends with "Implementation Order" phases (Foundation → Core Gameplay → Enemies & Progression → Polish & Mobile → Juice) and a "Testing Checklist" (desktop/touch/gameplay).
  - Agent-written CLAUDE.md after the build documents architecture for future sessions.

---
## Verbatim: docs/gdd.md (full)
# Pocket Bomber Demo - Game Design Document

## 1. Summary
A Bomberman-style grid action game where you clear enemies per level using timed bombs with cross-shaped blast propagation; you win by defeating all enemies across 5 fixed levels, and you lose by being caught in any explosion damage tick.

- Assumptions:
  - Built in **LÖVE (Love2D) 11.5** (not HTML/Canvas); desktop-first with optional touch support where available.
  - Shapes-only visuals using LÖVE drawing primitives (no external sprites/audio in V1).
  - 5 handcrafted levels, played sequentially; restart from Level 1 on game over.
  - Deterministic level layout (no procedural generation in V1).
  - “Demo” scope prioritizes tight feel + readable UX (no items/powerups).
  - Save data (high score) stored locally via LÖVE filesystem (no browser localStorage).

## 2. Technical Requirements
- Rendering: **LÖVE (Love2D) 11.5** using built-in 2D drawing (`love.graphics`)
- Packaging: Standard LÖVE project (`main.lua` + optional modules/assets), runnable via Love2D 11.5
- Unit system: **pixels**
  - Grid-based gameplay: 1 tile = **48×48 px** (authoritative for collisions, placement, explosions)
- Persistence:
  - High score saved using **`love.filesystem.read` / `love.filesystem.write`**
  - Deterministic save filename: **`pocket_bomber_demo_highscore.txt`** (plain text integer)
- Input support:
  - Keyboard (required)
  - Gamepad (optional nice-to-have, not required)
  - Touch (supported if running on touch-enabled platforms supported by LÖVE; virtual controls drawn in-game)

## 3. Canvas & Viewport
- Logical resolution (authoritative simulation space): **960×540**
- Window behavior:
  - The game scales up/down to fit the actual window while preserving aspect ratio
  - Aspect ratio behavior: **letterboxed** to preserve 16:9; black bars as needed
- Background: dark desaturated vertical gradient (top slightly lighter than bottom) to keep tiles readable
- Safe UI margins:
  - Reserve **top 60 px** for UI bar
  - Reserve **bottom 120 px** for touch controls when touch is active; on non-touch platforms, bottom area may remain mostly empty except for small control hints
- Touch zones (when touch is active):
  - Left side: virtual joystick area (bottom-left quadrant), centered at ~**(160, 440)** in logical space
  - Right side: action buttons area (bottom-right quadrant), never overlapped by joystick visuals
  - Touch controls are always visible during gameplay on touch devices

## 4. Visual Style & Art Direction
- Art style: clean, chunky “toy-like” flat shapes with strong outlines and high contrast
- Mood/atmosphere: playful arcade tension; readable hazards, minimal clutter

**Color palette (purposeful, 8+ hex):**
- Background deep: `#101826`
- Background mid: `#18263A`
- Floor tile A: `#2A3B55`
- Floor tile B: `#24344C`
- Indestructible wall: `#6B7A8F`
- Indestructible wall shadow: `#4E5B6C`
- Destructible block: `#B07A3A`
- Destructible highlight: `#D39B5A`
- Player primary: `#3ED2FF`
- Player accent: `#EAF8FF`
- Enemy primary: `#FF4D5A`
- Enemy outline: `#9E1F2D`
- Bomb: `#1B1B1B`
- Bomb highlight: `#3A3A3A`
- Explosion core: `#FFF2A6`
- Explosion edge: `#FF9B42`
- UI text: `#F2F5FF`
- “Danger” flash overlay: `#FF4D5A`

## 5. Player Specifications
- Appearance: rounded-square “chibi bomber” silhouette with a small visor stripe; subtle 2-tone shading; thick outline
- Size: **36×36 px** body (fits within a 48 px tile with margin)
- Colors:
  - Primary: `#3ED2FF`
  - Accent/visor: `#EAF8FF`
- Starting position: per-level fixed spawn tile (always a safe **2×2 open pocket**)
- Movement constraints: **4-directional only (cardinal)**, tile-collision based
  - Player may change direction instantly at tile boundaries; no diagonal movement
  - Movement is continuous in pixels but governed by tile passability

**Animation states (feel):**
- Idle: subtle bob + breathing squash (friendly, alive)
- Walk: snappy step-bob synced to speed (arcade)
- Place bomb: micro “tap” squash + quick lean (instant feedback)
- Death: quick freeze-frame + pop/flatten + fade (impactful, clear)

## 6. Physics & Movement
Up direction: **negative Y** (screen coordinates)

| Property | Value | Unit |
|----------|-------|------|
| Gravity | 0 | px/sec² |
| Jump velocity | 0 | px/sec |
| Move speed | 180 | px/sec |
| Max fall speed | 0 | px/sec |
| Ground position | N/A (top-down) | px |

Additional movement rules (authoritative “Bomberman feel”):
- Tile collision:
  - Player cannot enter tiles marked as blocked (indestructible or destructible blocks, bombs if configured as blocking—see Bomb Rules below)
- Cornering assist (lane magnet):
  - If moving toward an open corridor and within **10 px** of tile-center on the perpendicular axis, gently bias the player toward center to reduce joystick frustration
- Turn buffering:
  - If the player is holding a new direction while blocked, execute the turn automatically as soon as the adjacent tile becomes open
- Bomb pass rule (fairness standard):
  - After placing a bomb, the player may still move off that tile even if bombs are otherwise blocking
  - Once the player leaves the bomb tile, that bomb becomes solid (blocks re-entry) until it explodes

## 7. Obstacles/Enemies
### 7.1 Tiles (Obstacles)
- Indestructible walls:
  - Appearance: solid beveled blocks, thicker outline, darker bottom edge
  - Size: **48×48 px**
  - Behavior: blocks movement and blocks explosion propagation
- Destructible blocks:
  - Appearance: cracked crate/brick look with highlight corner
  - Size: **48×48 px**
  - Behavior:
    - Blocks movement
    - Destroyed by explosions
    - Stops explosion propagation at that tile (explosion includes the tile, then halts)

### 7.2 Enemies
- Count per level:
  - Level 1: **2**
  - Level 2: **3**
  - Level 3: **4**
  - Level 4: **5**
  - Level 5: **6**
- Appearance: rounded diamond blob with angry eyes; simple wobble
- Size: **34×34 px**
- Color: `#FF4D5A` with darker outline `#9E1F2D`
- Spawn: pre-authored spawn tiles away from player pocket (minimum **5 tiles Manhattan distance**)
- Movement behavior:
  - **Cardinal-only movement** (symmetry with player constraint)
  - Roam AI:
    - At intersections (2+ valid forward options), choose direction with weighted preference:
      - 60% continue forward if possible
      - 30% turn left/right (split evenly)
      - 10% reverse (only if not blocked)
    - If next tile is blocked, re-roll immediately
  - Bomb awareness (simple, readable):
    - If an enemy is within **2 tiles** (Manhattan) of a bomb that will detonate within **0.6 sec**, it will try to choose a direction that increases distance (still cardinal-only; if none, it may reverse)
- Speed:
  - Base: **120 px/sec**
  - Level scaling:
    - Level 1–2: 120 px/sec
    - Level 3–4: 130 px/sec
    - Level 5: 140 px/sec
- Spawn timing: all enemies present at level start (no mid-level spawners in V1)
- Despawn condition: removed instantly when hit by explosion damage tick

**Animated enemy feel:**
- Idle/walk: squish-wobble loop
- Danger tell: wobble amplitude increases when near bombs (see Juice section)

## 8. World & Environment
- Game board: **13 columns × 9 rows**
  - Gameplay footprint: 13×9 tiles = **624×432 px**
  - Board is centered horizontally, placed below the top UI bar with comfortable padding
- Layout conventions (per level):
  - Outer border: indestructible walls
  - Interior pillars: indestructible walls in checker pattern typical of Bomberman (maze-like flow)
  - Destructible blocks fill most remaining spaces but always leave:
    - Player spawn pocket: **2×2 open tiles**
    - A minimum of **8** empty traversable tiles across the map (excluding spawn pocket) to avoid “all crates” frustration
- Level transition:
  - After clearing enemies, show a short banner celebration, then load next level
  - After Level 5 clear, show “DEMO CLEAR” and return to menu after celebration; high score updates normally
- UI layout:
  - Top bar (within top 60 px):
    - Left: Score
    - Center: Level X / 5
    - Right: Enemies remaining + Pause indicator/button (depending on platform)
  - Bottom area:
    - Touch devices: joystick left + BOMB/PAUSE buttons right
    - Non-touch: small control hint text centered near bottom (non-intrusive)

## 9. Collision & Scoring
- Collision detection approach:
  - World collision: **tile-blocking** (impassable tiles stop movement)
  - Entity overlap (player/enemy vs explosion): tile membership with a forgiving center check window (see below)
- Forgiving hitboxes:
  - Player collision radius: **14 px**
  - Enemy collision radius: **14 px**
- Explosion damage timing (fairness-critical):
  - Explosion visual lifetime: **0.34 sec** (see timings)
  - Damage tick occurs at **explosion start + 0.12 sec**
  - Grace rule: during the first **0.12 sec**, the player is only harmed if their **center point** is inside an exploding tile; after damage tick, no additional damage ticks occur (single decisive moment)
- Game over triggers:
  - Player center is considered “hit” at the damage tick timing while inside any exploding tile (after grace rules)
- Score:
  - +100 per destructible block destroyed
  - +300 per enemy defeated
  - +200 level clear bonus
  - Combo bonus: if a single bomb defeats multiple enemies, +150 extra per additional enemy after the first
- Near-miss threshold:
  - If player center exits an explosion tile within **0.20 sec before** the damage tick moment, trigger near-miss (max once per bomb)
- High score storage:
  - Save filename: **`pocket_bomber_demo_highscore.txt`**
  - Stored value: integer best score
  - Update rule: if final score > saved best, overwrite file

## 10. Controls
| Input | Action | Condition |
|-------|--------|-----------|
| Keyboard: Arrow keys / WASD | Move (4-direction) | Playing |
| Keyboard: Space / Enter | Place bomb on current tile | Playing; if tile doesn’t already contain a bomb |
| Keyboard: P / Escape | Pause/Resume toggle | Playing/Paused |
| Touch: drag on virtual joystick (left) | Move (4-direction) | Playing only (touch platforms) |
| Touch: tap “BOMB” button (right) | Place bomb | Playing; if tile doesn’t already contain a bomb |
| Touch: tap “PAUSE” button (top-right or right cluster) | Pause | Playing only |
| Touch: tap “RESUME” | Resume | Paused only |
| Touch: tap “RETRY” | Restart from Level 1 | Game Over only |

## 11. Game States
### Menu
- Display:
  - Title: “Pocket Bomber Demo”
  - Big “PLAY” button centered
  - Controls panel (must be visible):
    - Keyboard: “Move: WASD/Arrows • Bomb: Space/Enter • Pause: P/Esc”
    - Touch (if touch is active): “Left thumb: Move • Right thumb: BOMB • PAUSE: button”
  - High score shown (Best: ####)
- Start:
  - Activate PLAY (click/tap) or press Enter/Space

### Playing
- Active:
  - Grid board, player, enemies, bombs, explosions
- UI shown:
  - Top-left: Score
  - Top-center: “Level X / 5”
  - Top-right: Enemies remaining + Pause hint/button
  - Bottom overlay hint (small, non-intrusive):
    - Keyboard: “WASD/Arrows • Space: Bomb • P: Pause”
    - Touch: “Move: joystick • Bomb: button”
- Level complete:
  - When enemies remaining = 0:
    - Show “LEVEL CLEAR” banner
    - Award +200 score immediately with a small floating “+200”
    - Transition to next level after celebration timing (see Juice)

### Paused
- Trigger: P/Escape or Pause button
- Display:
  - Dim overlay (60% opacity)
  - “PAUSED” text + Resume + Restart buttons
  - Controls reminder still visible (small)
- Behavior:
  - Everything frozen: movement, timers, bomb fuses, explosions, enemy AI
  - UI may have subtle pulse (purely visual)

### Game Over
- Trigger: player death
- Display:
  - “GAME OVER”
  - Score + Best score
  - Big “RETRY” button
  - Small “Back to Menu” button
- Retry:
  - Restarts at Level 1, score resets to 0

## 12. Game Feel & Juice (REQUIRED)

### 12.1 Input Response
Every input must acknowledge on the same frame it’s received.

- Movement input:
  - Player immediately leans **6°** toward move direction (same-frame)
  - If input is held into a wall (movement denied):
    - Player does a tiny “bump” nudge: **2 px** toward wall and back over **0.10 sec**
    - Outline flashes `#FF4D5A` for **0.06 sec**
- Joystick engage (touch):
  - On touch start: joystick base fades in within **0.05 sec**
  - Stick follows finger with a slightly elastic feel (visual trails by ~1 frame impression; never delays actual movement once direction is chosen)
- Place bomb:
  - Same-frame feedback:
    - Player squash: scale to **(1.12, 0.90)** for **0.07 sec**
    - Bomb pops in with scale **0.6 → 1.0** over **0.10 sec**
- Denied bomb placement (tile already has a bomb):
  - Player outline flash `#FF4D5A` for **0.08 sec**
  - Small “X” blip over player for **0.20 sec**
  - Micro screen shake: intensity **2 px**, duration **0.10 sec**

### 12.2 Animation Timing
- Player idle bob:
  - Period: **1.2 sec** loop
  - Scale: y **1.00 → 1.04 → 1.00**, ease-in-out
- Player walk bob:
  - Period: **0.35 sec** loop while moving
  - Position bob: ±**2 px** vertical, ease-in-out
- Bomb fuse:
  - Fuse duration: **1.80 sec**
  - Blink rate accelerates:
    - 0.0–1.0 sec: blink every **0.30 sec**
    - 1.0–1.6 sec: blink every **0.18 sec**
    - 1.6–1.8 sec: blink every **0.10 sec**
- Explosion:
  - Expand-in: **0.06 sec**
  - Hold: **0.18 sec**
  - Fade-out: **0.10 sec**
  - Total visible: **0.34 sec**
- UI banner transitions:
  - “LEVEL CLEAR” / “GAME OVER” banner:
    - Slide in from top over **0.18 sec** (ease-out)
    - Hold **0.55 sec**
    - Fade out **0.18 sec**

### 12.3 Near-Miss Rewards
- Detection:
  - If player center exits an explosion tile within **0.20 sec** before the damage tick time, count as near-miss (max **1** per bomb)
- Visual:
  - Brief rim light on player (tint toward `#FFF2A6`) for **0.25 sec**
  - “Whoosh” streak line behind player for **0.20 sec**
  - Floating text: “CLOSE!” above player, rising **18 px** over **0.40 sec**, fading out
- Score:
  - +50 per near-miss (max 1 per bomb)
  - Floating “+50” appears near player

### 12.4 Screen Effects
| Effect | Trigger | Feel |
|--------|---------|------|
| Shake | Explosion hits destructible block | 3 px intensity, 0.12 sec, snappy |
| Shake | Enemy defeated | 2 px intensity, 0.08 sec, crisp |
| Shake | Player death | 10 px intensity, 0.25 sec, heavy |
| Flash | Near-miss | `#FFF2A6` overlay at 18% opacity, 0.10 sec |
| Flash | Level clear | White overlay at 25% opacity, 0.18 sec |
| Zoom pulse (visual-only) | Bomb detonation | Screen scale 1.00 → 1.03 → 1.00 over 0.18 sec |
| Time dilation | Player death | Slowdown to **0.35×** for **0.35 sec**, then transition |

### 12.5 Progressive Intensity
Across the 5 fixed levels:
- Level 1:
  - Bomb blast radius: **2 tiles**
  - Enemy speed: **120 px/sec**
  - Destructible density: medium
- Level 2:
  - Blast radius: **2 tiles**
  - Slightly more destructibles (tighter lanes)
- Level 3:
  - Blast radius: **3 tiles**
  - Enemy speed: **130 px/sec**
- Level 4:
  - Blast radius: **3 tiles**
  - Enemy count increases; danger tells are stronger (enemy wobble increases more near bombs)
- Level 5:
  - Blast radius: **3 tiles**
  - Enemy speed: **140 px/sec**
  - Subtle global tint shift toward warmer danger tones (background lerp 15% toward `#2A1B22`)

### 12.6 Idle Life
- Player:
  - Breathing squash + tiny visor shine sweep every **3.0 sec**
- Enemies:
  - Continuous wobble
  - When a bomb is within **3 tiles** (Manhattan), wobble amplitude increases by **40%** and blink rate increases slightly (readable danger tell)
- Environment:
  - Faint drifting particles (2–4 at a time) moving upward at **12 px/sec**
  - Occasional floor tile glint: one tile highlight sweep every **2.5 sec** (subtle, not distracting)

### 12.7 Milestone Celebrations
- Milestones: every **1000 points**
- Celebration effect:
  - Top-center banner “+1000!” pulse
  - Quick flash: white overlay **12% opacity** for **0.08 sec**
  - Confetti-like squares (shapes-only) burst from top bar: **12 pieces**, lifetime **0.6 sec**
- New high score special treatment:
  - On Game Over, if score > best:
    - “NEW BEST!” text pulses for **0.8 sec**
    - Background briefly shifts tint toward `#3ED2FF` (10% overlay) for **0.15 sec**

### 12.8 Death Sequence
Make failure feel consequential and readable.
- Trigger: player hit at explosion damage tick
- Sequence:
  1. Freeze frame: **0.06 sec** (gameplay stops, but draw one crisp frame)
  2. Screen shake: **10 px**, **0.25 sec**
  3. Player visual:
     - Flatten squash to **(1.30, 0.60)** over **0.10 sec**
     - Fade out to 0 alpha over **0.22 sec**
     - Optional “shatter” pips: 8 small squares pop outward, lifetime **0.35 sec**
  4. Time dilation: **0.35×** for **0.35 sec** (blends through the death moment)
  5. Fade to Game Over overlay over **0.25 sec**

## 13. UX Requirements
- Controls visible on menu screen (required)
- Controls hint during gameplay (required)
- Forgiving collision:
  - Player/enemy radius **14 px**
  - Explosion grace window **0.12 sec** with center-point requirement
- Touch support:
  - If touch is available, show on-screen joystick + buttons
  - Touch controls must not cover the grid play area (remain in bottom reserved zone)
- Readability:
  - Explosions must clearly occupy tiles (cross shape), with brighter core and orange edges
  - Enemy count remaining must be always visible during play
- Pause:
  - Must freeze all gameplay timers and movement
  - Must be obvious visually (dim overlay + “PAUSED”)

## 14. Out of Scope (V1)
- Sound effects and music
- Power-ups/items (extra bombs, flame length, speed boots, etc.)
- Soft walls revealing exit/goal tile (the demo win condition is enemy clear only)
- Online leaderboards or cloud saves
- Procedural level generation
- Advanced enemy types (only one enemy archetype)
- Multiplayer / local co-op
- Settings menu (volume, controls remap, graphics options)

## 15. Success Criteria
- [ ] Runs in **Love2D 11.5** without errors or missing dependencies
- [ ] Controls visible on menu AND during gameplay (keyboard and touch where applicable)
- [ ] Input feels instant (same-frame response for movement and bomb placement)
- [ ] Player movement is strictly cardinal with cornering assist and turn buffering
- [ ] Bomb placement rules prevent self-trap frustration (can leave placed bomb tile; bomb becomes solid after leaving)
- [ ] Jump is not present (top-down); instead, bomb placement and movement have clear anticipation/follow-through
- [ ] Near-misses trigger reward feedback (visual + +50) and are limited to once per bomb
- [ ] Score updates with readable UI and floating point feedback
- [ ] High score persists across sessions via `pocket_bomber_demo_highscore.txt`
- [ ] Pause/resume works and freezes timers (bomb fuses/explosions/enemies)
- [ ] Death feels impactful (freeze + shake + squash + fade + time dilation)
- [ ] Collision feels fair (radius forgiveness + explosion grace timing)
- [ ] Something moves during idle (player breathing, enemy wobble, drifting particles)
- [ ] All 5 levels are completable, with enemy counts per level matching spec and level-clear transitions working

---
## Verbatim: plans/sleepy-herding-garden.md (Claude plan-mode output)
# Pocket Bomber Implementation Plan

## Overview
Implement a Bomberman-style grid action game using LÖVE 11.5 that works on desktop (keyboard) and iOS (touch). The implementation follows the GDD and TDD documents.

## Project Structure
```
pocket-bomber/
├── conf.lua                 # LÖVE configuration
├── main.lua                 # Entry point
├── src/
│   ├── globals.lua          # Constants and shared state
│   ├── colors.lua           # GDD color palette
│   ├── utils.lua            # Math helpers, serialization
│   ├── camera.lua           # 960x540 viewport with scaling
│   ├── save.lua             # High score persistence
│   ├── input.lua            # Keyboard + touch abstraction
│   ├── touch_controls.lua   # Virtual joystick & buttons
│   ├── state_machine.lua    # Game state management
│   ├── grid.lua             # Tile grid (13x9)
│   ├── level_data.lua       # 5 handcrafted levels
│   ├── level.lua            # Level management
│   ├── player.lua           # Player entity with animation
│   ├── enemy.lua            # Enemy AI
│   ├── bomb.lua             # Bomb with fuse timing
│   ├── explosion.lua        # Cross propagation, damage timing
│   ├── particle.lua         # Visual effects system
│   ├── ui.lua               # HUD, menus, banners
│   └── states/
│       ├── menu.lua
│       ├── playing.lua
│       ├── paused.lua
│       └── gameover.lua
```

## Implementation Phases

### Phase 1: Foundation Files
1. **conf.lua** - Window config, identity, module toggles
2. **src/globals.lua** - Game constants (tile size, speeds, timers)
3. **src/colors.lua** - Hex to RGB conversion for all GDD colors
4. **src/camera.lua** - Logical 960x540 resolution with letterboxing
5. **src/utils.lua** - Serialization, math helpers
6. **src/save.lua** - High score file I/O

### Phase 2: Input System
7. **src/input.lua** - Unified keyboard/touch input
8. **src/touch_controls.lua** - Virtual joystick (left), bomb/pause buttons (right)

### Phase 3: Core Game Systems
9. **src/state_machine.lua** - State switching with enter/exit callbacks
10. **src/grid.lua** - Tile grid with collision
11. **src/level_data.lua** - 5 level definitions with enemy spawns
12. **src/level.lua** - Level loading and management

### Phase 4: Entities
13. **src/player.lua** - Movement, cornering assist, bomb pass rule, animations
14. **src/enemy.lua** - Roam AI, bomb avoidance, wobble animation
15. **src/bomb.lua** - Fuse timing with accelerating blink
16. **src/explosion.lua** - Cross propagation, damage timing, near-miss
17. **src/particle.lua** - Floating text, debris effects

### Phase 5: Game States
18. **src/states/menu.lua** - Title, play button, controls, high score
19. **src/states/playing.lua** - Game loop, entity updates, level progression
20. **src/states/paused.lua** - Dim overlay, resume/restart
21. **src/states/gameover.lua** - Death sequence, final score, retry

### Phase 6: UI and Polish
22. **src/ui.lua** - HUD, banners, buttons
23. **main.lua** - Love callbacks, initialization

### Phase 7: Testing & iOS Prep
24. Test all 5 levels
25. Test touch controls
26. Create iOS build script

## Key Technical Requirements
- 60 FPS target with dt-based movement
- Shapes-only rendering (no external assets)
- Keyboard (WASD/Arrows + Space) + Touch (joystick + buttons)
- Persistent high score via love.filesystem
- Grace window (0.12s) for explosions
- Near-miss detection (0.20s before damage)

## Verification Steps
1. Run with `love .` - game starts to menu
2. Press Space/Enter or click PLAY - enters level 1
3. Move with WASD/Arrows - player moves cardinally
4. Press Space - bomb placed, fuse blinks accelerating
5. Explosion destroys blocks and enemies
6. Clear all enemies - "LEVEL CLEAR" banner, advances to next level
7. Die - death sequence, game over screen
8. High score persists between sessions
9. On iOS: touch controls visible, joystick moves player, bomb button works


---
## Excerpt: docs/tdd.md — section outline + sections 11 (Implementation Order) and 13 (Testing Checklist)
## 1. Overview
## 2. Project Structure
## 3. Core Architecture
### 3.1 Game Loop Flow
### 3.2 State Machine Implementation
### 3.3 Game States
## 4. Rendering & Viewport
### 4.1 Camera/Scaling System
### 4.2 Grid Layout
## 5. Input System
### 5.1 Input Abstraction Layer
### 5.2 Touch Controls Module
## 6. Entity Systems
### 6.1 Player Implementation
### 6.2 Enemy AI Implementation
### 6.3 Bomb & Explosion System
## 7. Grid & Level System
### 7.1 Grid Implementation
### 7.2 Level Data
## 8. UI System
## 9. Save System
## 10. iOS Build Configuration
### 10.1 conf.lua
### 10.2 iOS Build Script
#!/bin/bash
# build-ios.sh
### 10.3 iOS Setup Checklist
## 11. Implementation Order
### Phase 1: Foundation
### Phase 2: Core Gameplay
### Phase 3: Enemies & Progression
### Phase 4: Polish & Mobile
### Phase 5: Juice
## 12. Performance Considerations
### Optimization Tips
## 13. Testing Checklist
### Desktop (Keyboard)
### Mobile (Touch)
### Gameplay
## 14. References
## 11. Implementation Order

### Phase 1: Foundation
1. `conf.lua` - Window configuration
2. `src/globals.lua` - Constants, shared state
3. `src/colors.lua` - GDD color palette
4. `src/camera.lua` - Viewport/scaling
5. `main.lua` - Basic structure with state machine

### Phase 2: Core Gameplay
6. `src/grid.lua` - Tile grid system
7. `src/level_data.lua` - 5 level definitions
8. `src/player.lua` - Player movement, animation
9. `src/input.lua` - Keyboard input
10. `src/bomb.lua` - Bomb placement, fuse
11. `src/explosion.lua` - Cross propagation, damage

### Phase 3: Enemies & Progression
12. `src/enemy.lua` - AI, movement
13. `src/level.lua` - Level loading, management
14. State implementations: `menu`, `playing`, `paused`, `gameover`

### Phase 4: Polish & Mobile
15. `src/particle.lua` - Visual effects
16. `src/ui.lua` - HUD, menus, banners
17. `src/touch_controls.lua` - Virtual joystick, buttons
18. `src/save.lua` - High score persistence
19. iOS build testing

### Phase 5: Juice
20. Screen shake, flashes
21. Floating text, animations
22. Near-miss detection
23. Death sequence

---

## 12. Performance Considerations
## 13. Testing Checklist

### Desktop (Keyboard)
- [ ] Movement: WASD and Arrow keys
- [ ] Bomb placement: Space/Enter
- [ ] Pause: P/Escape
- [ ] Window resize maintains aspect ratio
- [ ] Fullscreen toggle works

### Mobile (Touch)
- [ ] Virtual joystick appears on touch
- [ ] Joystick deadzone feels right
- [ ] Bomb button places bomb
- [ ] Pause button works
- [ ] Controls don't obscure gameplay
- [ ] Touch targets >= 44 points

### Gameplay
- [ ] All 5 levels completable
- [ ] Enemy counts match GDD
- [ ] Blast radius progression correct
- [ ] Score tracking accurate
- [ ] High score persists
- [ ] Death sequence plays
- [ ] Near-miss detection works

---

## 14. References


---
## Verbatim: CLAUDE.md
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pocket Bomber is a Bomberman-style grid-based action game built with LÖVE (Love2D) 11.5 in Lua. It targets both desktop (keyboard) and iOS (touch). All visuals use shape-based rendering — no external sprite assets.

## Running the Game

```bash
love .
```

Requires LÖVE 11.5 installed. There is no build step, test suite, or linter — the game runs directly from source.

## Architecture

### Game Loop & State Machine

`main.lua` wires LÖVE callbacks (`load`, `update`, `draw`, `resize`, input events) to three systems: Camera, Input/Touch, and StateMachine. The state machine (`src/state_machine.lua`) manages four states — **menu**, **playing**, **paused**, **gameover** — each with `enter(params)`, `update(dt)`, `draw()`, `exit()`, and input handler methods.

### Camera & Coordinate System

The camera (`src/camera.lua`) scales a logical 960×540 space to the actual window, stretching to fill. Tile size and grid offsets are calculated dynamically from the viewport. All touch/mouse coordinates pass through `Camera.toGame()` before reaching game logic. The top 80 logical pixels are reserved for HUD.

### Grid System

The grid (`src/grid.lua`) is a 13×9 2D array of tile types: `EMPTY` (0), `WALL_PERMANENT` (1), `WALL_BREAKABLE` (2). Coordinate conversions between grid `(col, row)` and world `(x, y)` live in `src/utils.lua`. Collision uses per-corner hitbox checks against grid tiles.

### Entity Model

Entities are plain Lua tables managed in lists on `src/globals.lua` (`G.bombs`, `G.explosions`, `G.enemies`, `G.particles`). The player is a singleton. Each entity type has its own module:

- **Player** (`src/player.lua`) — Cardinal movement at 180px/s, cornering assist (auto-align within 12px), bomb pass rule (can walk through just-placed bomb until leaving its tile), death animation sequence.
- **Enemy** (`src/enemy.lua`) — Three types (basic/fast/tank) with simple roaming AI: continue forward, randomly turn perpendicular, reverse if stuck for 0.5s. Avoids bomb tiles.
- **Bomb** (`src/bomb.lua`) — 2.0s fuse with accelerating blink rate. Returns true on detonation to trigger explosion spawn.
- **Explosion** (`src/explosion.lua`) — Cross-shaped propagation up to 2-3 tiles per direction. Stops at permanent walls, destroys breakable walls. Has a 0.12s grace window before dealing damage (fairness buffer). Total duration 0.5s.
- **Particle** (`src/particle.lua`) — Float text (score popups) and debris (block destruction).

### Level Data

`src/level_data.lua` defines 5 handcrafted levels. Each specifies a grid layout string, breakable wall positions, enemy spawn list, player start position, blast radius, and time limit (120-200s). `src/level.lua` handles loading and progression.

### Input Abstraction

`src/input.lua` normalizes keyboard input into `G.input` (dx/dy direction, bombPressed, pausePressed). `src/touch_controls.lua` provides a floating virtual joystick (left half) and bomb/pause buttons (right side) on mobile. Platform detection chooses which to display.

### Persistence

`src/save.lua` reads/writes high scores via LÖVE's filesystem (identity: "pocket-bomber").

## Key Design Details

- **Globals pattern**: `src/globals.lua` exports a single table `G` holding all constants, shared state, and entity containers. Modules `require("src.globals")` to access it.
- **No external dependencies**: Pure LÖVE APIs only.
- **Modules disabled in `conf.lua`**: joystick, physics, video, thread.
- **dt capped at 0.1s** in the update loop to prevent large frame skips.
- **Color palette**: `src/colors.lua` converts hex to LÖVE RGB (0-1 range).

## Design Documents

- `docs/gdd.md` — Game Design Document with full mechanics specification
- `docs/tdd.md` — Technical Design Document with architecture pseudocode and iOS build details
