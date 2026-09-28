# Mall Hell — first-person Three.js arcade shooter (kid in shopping cart w/ slingshot), Claude Code (Opus) + Codex

- Repo: https://github.com/okohub/mall-hell  (Play: https://okohub.github.io/mall-hell/)
- Stars: 1. Weak popularity evidence; but 151 commits over ~2 weeks (2026-01-23 → 02-05), versions v1.2 → v5.10, README feature list, working GH Pages build claimed.
- Tool/model: "An experimental game written by Claude Code and Opus Model"; CODEX.md shows Codex also used later (with "session learnings").
- Genre: FPS arcade score-chaser, room grid, 4 weapons, enemies, power-ups, 3-minute session.
- One-shot vs multi-session: multi-session incremental versioning; original first prompt NOT preserved (initial commit is "Cart Chaos v1.2"). Spec here is the *living* GAME_DESIGN.md (tables for stats) rather than an up-front GDD.
- Notable process practices:
  - Custom Puppeteer-driven test runner with --failed/--domain/--group/--test filters; "Full suite only when asked" (keeps agent loops fast).
  - Development rules incl. "Fix code, not tests — if tests fail, implementation is wrong"; "Integration tests use manualUpdate — stop the game loop and step dt deterministically".
  - "Before Claiming Done" checklist: related tests pass, no console errors, manual 30-sec smoke test.
  - Domain/orchestrator architecture with "single source of truth" constants per domain; balance table in CLAUDE.md.
  - Feature work via superpowers-style design + implementation plan pairs in docs/plans/ (e.g. speed-boost-powerup-design.md + speed-boost-powerup.md).
  - CODEX.md delegates to CLAUDE.md and appends session learnings; progress.md scratchpad git-ignored.

---
## Verbatim: CLAUDE.md
# Mall Hell

**Version 5.9** | First-person arcade shooter | Clear the mall of enemies

## Quick Commands

| Task | Command |
|------|---------|
| Run failed tests | `bun run-tests.js --failed` |
| Test domain | `bun run-tests.js --domain=enemy` |
| Test group | `bun run-tests.js --group=weapon` |
| Test single | `bun run-tests.js --test=<id>` |
| Integration tests | `bun run-tests.js --suite=integration` |
| Full suite | `bun run test` (only when asked) |
| Rerun flaky test | Run failed test in isolation to verify if timing issue |

## Documentation

| Need to... | Read |
|------------|------|
| Understand codebase structure | [Architecture](docs/ARCHITECTURE.md) |
| Know game mechanics/enemies/weapons | [Game Design](docs/GAME_DESIGN.md) |
| Add enemy, weapon, UI, fix bug | [Workflows](docs/WORKFLOWS.md) |
| Write or run tests | [Testing](docs/TESTING.md) |

## Development Rules

1. **Read before write** - Never modify code you haven't read
2. **Fix code, not tests** - If tests fail, implementation is wrong
3. **Domain boundaries** - Each domain is self-contained
4. **Single source of truth** - Use constants from `<domain>.js` files
5. **Orchestrators over instances** - Use `WeaponOrchestrator`, `EnemyOrchestrator`, etc.
6. **Stateless helpers** - Mesh/animation modules receive all data as parameters
7. **Integration tests use manualUpdate** - Call `LoopOrchestrator.stop()` then use `manualUpdate(dt)` for deterministic control
8. **Test isolation** - Framework stops game loop before each test; reset weapon state between tests
9. **Valid room positions** - Default start is (45, 75) in room (1,2); position (0,0) is invalid
10. **Damage calculations in domain files** - collision-orchestrator reads damage from userData, never calculates it
11. **Weapon fire() returns damage** - Must pass through createMesh options chain to projectile userData
12. **Status effects use userData timestamps** - Store `slowedUntil`, check `Date.now() < timestamp`, auto-expire
13. **Projectile registry pattern** - Each projectile type is a folder; its type file is the public API and must register `createMesh` + `animate`

## Domain Quick Reference

| Domain | Data | Orchestrator | Purpose |
|--------|------|--------------|---------|
| enemy | `enemy.js` | `enemy-orchestrator.js` | Enemy types, AI, spawning |
| weapon | `weapon.js` | `weapon-orchestrator.js` | Weapons, ammo, firing |
| room | `room.js` | `room-orchestrator.js` | Room grid, themes |
| environment | `obstacle.js` | `spawn-orchestrator.js` | Obstacles, lazy loading |
| ui | `ui.js` | `ui-orchestrator.js` | HUD, menus, minimap |
| player | `player.js` | `player-orchestrator.js` | Movement, health |
| projectile | `projectile.js` | `projectile-orchestrator.js` | Projectile physics |
| powerup | `powerup.js` | `powerup-orchestrator.js` | Power-ups, effects, timers |
| engine | - | `state-orchestrator.js`, etc. | Core game systems |

## File Ownership

| File | Purpose |
|------|---------|
| `index.html` | Orchestration only (game loop, glue code) |
| `src/<domain>/` | Domain logic (self-contained) |
| `tests/` | Test runners and test files |

## Common Patterns

**Weapon config access:** `weapon.config.projectile.speed.min` (not speedMin)
**Enemy visual effects:** Traverse `enemy.mesh.userData.cart`, set `child.material.emissive`
**Test helpers in index.html:** `startFiring()` → `startCharging()`, `stopFiring()` → `releaseAndFire()`
**Weapon spawn offsets:** Each weapon has `spawnOffset: { forward, down, right }` for projectile origin

## Weapon Balance (v5.8)

| Weapon | Damage | Ammo | Charge Time | Notes |
|--------|--------|------|-------------|-------|
| Slingshot | 1 base, +3 per charge<br>Quick: 1, Half: 2, Full: 4 | 25 | 2.0s to full charge<br>minTension: 0.05 | Skill-based workhorse, rewards patience |
| Nerf Gun | 3 flat | 12 | N/A | Reliable sidearm, 20% faster projectiles (120 speed) |
| Water Gun | 2 direct, 3 splash | 30 | N/A | Crowd control, 50% stronger AOE |
| Laser Gun | 1 per shot | 75 | N/A | Power weapon, melts 18 skeletons per magazine |

## Before Claiming Done

```
[ ] Related tests pass
[ ] No console errors
[ ] Manual smoke test (30 sec)
```


---
## Verbatim: CODEX.md
# CODEX.md

This repo uses `CLAUDE.md` as the primary project guide. Read it first:
- `CLAUDE.md`

## Codex Notes (session learnings)
- Integration tests should follow the game-boot pattern: `resetGame()` → click `#start-btn` → stop loop → use `manualUpdate()` for deterministic steps.
- The shared helper `IntegrationHelpers.bootGameForIntegration()` mirrors this flow.
- Unit/UI/integration tests are browser-driven via Puppeteer; in restricted environments, browser launch may fail.
- `progress.md` is a local scratchpad and is ignored in `.gitignore`.


---
## Verbatim: docs/GAME_DESIGN.md
# Game Design

## Overview

| Attribute | Value |
|-----------|-------|
| **Title** | Mall Hell |
| **Version** | 5.9 |
| **Genre** | Arcade Score-Chaser / Hell Crawler |
| **Session** | 3 minutes |
| **Objective** | Clear Mall Hell of all enemies before time expires |

## Core Loop

```
EXPLORE → HUNT → KILL → SCORE → REPEAT
    ↑                              ↓
    └──────── CLEAR ROOMS ←────────┘
```

## Controls

| Input | Action |
|-------|--------|
| W / ↑ | Drive forward |
| S / ↓ | Reverse |
| A / ← | Turn left (aim) |
| D / → | Turn right (aim) |
| SPACE (hold) | Charge weapon |
| SPACE (release) | Fire |
| ESC | Pause |

---

## Enemies

### Skeleton (Base)

| Stat | Value |
|------|-------|
| Health | 4 hits |
| Speed | 0.30 |
| Damage | 25 HP |
| Score (hit) | +150 |
| Score (destroy) | +400 |

- 2-3 per room at game start
- Never respawn when killed

### Dinosaur (Boss)

| Stat | Value |
|------|-------|
| Health | 10 hits |
| Speed | 0.25 |
| Damage | 40 HP |
| Score (hit) | +250 |
| Score (destroy) | +1500 |

- First spawn at 5000 points
- Additional every 5000 points
- Shows "DINO BOSS!" warning

---

## Weapons

| Weapon | Ammo | Damage | Charge Time | Special |
|--------|------|--------|-------------|---------|
| Slingshot | 25 | 1 base, +3 per charge<br>Quick: 1, Half: 2, Full: 4 | 2.0s to full charge<br>minTension: 0.05 | Skill-based workhorse, rewards patience |
| Nerf Gun | 12 | 3 flat | N/A | Reliable sidearm, 20% faster projectiles (120 speed) |
| Water Gun | 30 | 2 direct, 3 splash | N/A | Crowd control, 50% stronger AOE |
| Laser Gun | 75 | 1 per shot | N/A | Power weapon, melts 18 skeletons per magazine |

---

## Power-Ups

### Speed Boost

| Stat | Value |
|------|-------|
| Effect | 2x movement speed |
| Duration | 10 seconds |
| Spawn Chance | 25% per room |
| Visual | Red/yellow energy drink can |

- Temporary speed increase for aggressive room clearing
- Refreshes timer if collected while already boosted (doesn't stack)
- HUD timer shows remaining duration with color warnings

---

## Player

| Stat | Value |
|------|-------|
| Max Health | 100 HP |
| Move Speed | 25 units/sec |
| Dodge Speed | 8 units/sec |
| Invulnerability | 1 sec after hit |

---

## Scoring

| Score Range | Rating |
|-------------|--------|
| 0 - 1,500 | Window Shopper |
| 1,501 - 3,000 | Lost in IKEA |
| 3,001 - 6,000 | Mall Diver |
| 6,001 - 10,000 | Cart Warrior |
| 10,001 - 15,000 | Demon Buster |
| 15,001 - 21,000 | Abyss Hunter |
| 21,001 - 28,000 | Hell's Nightmare |
| 28,001+ | MALL REDEEMER |

**Theme:** You're descending into Mall Hell as a demon-slaying hero. Ratings blend your descent depth with growing fearsome reputation.

---

## HUD Elements

| Element | Position | Purpose |
|---------|----------|---------|
| Score | Top-left | Chaos score |
| Timer | Top-center | Time remaining |
| Status Panel | Top-right | Enemy progress + minimap |
| Health | Bottom-left | Current HP |
| Ammo | Bottom-center | Weapon + ammo count |
| Crosshair | Center | Aiming reticle |

### Minimap Legend

| Visual | Meaning |
|--------|---------|
| Yellow border | Current room |
| Red + number | Enemies in room |
| Orange pulse | Dinosaur in room |
| Subtle green | Cleared room |

---

## Spawn System

### Lazy Room Loading
- All rooms planned at game start (data only)
- Meshes created when player approaches room
- Eliminates game start lag

### Per Room
- Enemies: 2-3 skeletons
- Obstacles: 3-5
- Pickups: 0-1 weapon/ammo

### No Respawning
- Killed enemies stay dead
- "Clear the Mall" design philosophy
- Rooms can be completed

---

## Design Decisions

### Why No Respawning?
Random spawning creates frustration. Permanent progress feels rewarding and lets players strategize.

### Why Score-Based Dinosaurs?
Prevents late-game boredom. Aggressive play is rewarded with harder enemies.


---
## Verbatim: docs/TESTING.md
# Testing Guide

## Important: No Shell Redirects

Never use `2>&1` or other shell redirects with the test runner:
```bash
# WRONG - unnecessary, provides no benefit
bun run-tests.js 2>&1

# CORRECT
bun run-tests.js
```

The test runner captures all output internally and saves to `.test-output/`. Shell redirects are consumed by the shell before the script runs, so they cannot be detected or blocked.

## Quick Reference

| Command | Use When |
|---------|----------|
| `bun run-tests.js --failed` | Re-run only failed tests |
| `bun run-tests.js --domain=<name>` | Changed a specific domain |
| `bun run-tests.js --group=<name>` | Test specific feature group |
| `bun run-tests.js --test=<id>` | Test single test by ID |
| `bun run-tests.js --fail-fast` | Stop on first failure |
| `bun run-tests.js --suite=integration` | Run integration tests |
| `bun run test` | Full suite (only when user asks) |

## Workflow Rules

### Before Running Tests
1. Read `.test-output/latest.json` first
2. Check what failed in the last run
3. Only run tests if you made code changes

### Run Only Related Tests
- Changed enemy code? → `--domain=enemy`
- Changed specific feature? → `--test=<test-id>`
- Re-run failures? → `--failed`

### One Test Run Per Change
- Make your fix
- Run specific test(s) ONCE
- Read the output file
- DO NOT re-run unless you made another change

## Test Output

Results saved to `.test-output/`:
- `latest.json` - Most recent results
- `latest.txt` - Console output
- `run-<timestamp>.json` - History

## Writing Tests

### Unit Tests
- Location: `src/<domain>/<domain>.test.js`
- Register in: `tests/unit-tests.html`

### UI Tests
- Location: `tests/ui/<domain>.tests.js`
- Register in: `tests/ui-tests.html`

### Integration Tests
- Location: `tests/integration/<feature>.tests.js`
- Register in: `tests/integration-tests.html`
- Purpose: Test complete game mechanics end-to-end
- Run: `bun run-tests.js --suite=integration`
- Runtime: ~3-5 minutes for full suite

**Integration test groups:**
- Combat Flow: Weapon firing → projectile → hit → damage → kill
- Enemy Lifecycle: Spawn → AI → attack → death
- Room Progression: Pre-spawning, materialization, movement
- Player Lifecycle: Movement → damage → death, survival mechanics

### Critical Patterns

**Use orchestrators, not specific implementations:**
```javascript
// GOOD - weapon agnostic
WeaponOrchestrator.currentWeapon.state.lastFireTime = 0;

// BAD - couples to specific weapon
Slingshot.state.lastFireTime = 0;
```

**Same principle for all domains:**
- Use `EntityOrchestrator`, not specific entity arrays
- Use `StateOrchestrator`, not direct state manipulation
- Use `EnemyOrchestrator.getSpawnType()`, not hardcoded types

## Test Isolation

The test runner automatically resets game state before and after each test.

**What the runner does:**
1. Stops game loop (`LoopOrchestrator.stop()`)
2. Calls `resetGame()` before each test
3. Waits 100ms for state to settle
4. Runs the test
5. Calls `resetGame()` after test (cleanup)

**What gets reset:**
- Game loop stopped
- Game state → MENU
- Projectiles, enemies, obstacles cleared
- Score reset to 0

## Known Limitation: Keyboard Event Simulation

**Keyboard events (`simulateKeyDown`) are unreliable in the puppeteer/iframe test environment.**

The issue: Events dispatched to `gameDocument` sometimes don't reach `InputOrchestrator` listeners, even though:
- InputOrchestrator is initialized
- Callbacks are registered
- Event format is correct

This is an environment limitation, not a game bug. The actual game keyboard input works fine.

**Workaround: Use direct function calls instead of simulated keys**

```javascript
// UNRELIABLE - may intermittently fail
runner.simulateKeyDown('Escape');
await runner.wait(100);
// State might still be PLAYING!

// RELIABLE - use direct function call
runner.gameWindow.pauseGame();
await runner.wait(100);
// State is guaranteed PAUSED
```

**When to use each approach:**

| Action | Unreliable | Reliable Alternative |
|--------|------------|---------------------|
| Pause game | `simulateKeyDown('Escape')` | `gameWindow.pauseGame()` |
| Resume game | `simulateKeyDown('Escape')` | `gameWindow.resumeGame()` |
| Start firing | `simulateKeyDown(' ')` | `gameWindow.startFiring()` |
| Stop firing | `simulateKeyUp(' ')` | `gameWindow.stopFiring()` |

**Note:** Click simulation (`simulateClick`) works reliably - only keyboard events have this issue.

## Weapon State in Tests

When testing weapon functionality, always call `weapon.reset()` before your test to ensure clean state:

```javascript
const WeaponOrchestrator = runner.gameWindow.WeaponOrchestrator;
WeaponOrchestrator.currentWeapon.reset();  // Clean state

// Now test weapon behavior
weapon.onFireStart(Date.now());
```

**Why:** Previous tests may have fired the weapon, reducing ammo or setting cooldown timers. Without reset, `canFire()` may return false unexpectedly.


---
## Verbatim: docs/plans/2026-01-27-speed-boost-powerup-design.md
# Speed Boost Power-Up Design

**Version**: 5.5+
**Date**: 2026-01-27
**Type**: New Feature - Power-Up System

---

## Overview

Add a speed boost power-up that temporarily doubles player movement speed for 10 seconds. The power-up spawns as an energy drink can pickup in rooms, fitting the mall theme while adding tactical depth to room-clearing gameplay.

---

## Core Mechanics

### Effect
- **Speed Multiplier**: 2x (25 → 50 units/sec)
- **Duration**: 10 seconds
- **Applies to**: Forward, backward, and strafe movement
- **Does NOT affect**: Turn rate (maintains control)

### Spawn Configuration
- **Spawn Chance**: 25% per room
- **Spawn Weight**: 2 (similar rarity to Laser Gun)
- **Max per Room**: 1 (competes with existing weapon/ammo pickups)
- **Placement**: Uses existing PickupOrchestrator collision avoidance

### Stacking Behavior
- Picking up while boosted **refreshes** timer to 10 seconds
- No duration stacking (prevents 30+ second boosts)
- Maintains consistent gameplay tempo

### Visual Identity
- **Mesh**: Cylindrical energy drink can
- **Colors**: Bright red/yellow gradient
- **Glow**: Yellow-orange (0xffaa00)
- **Scale**: 2.0 (similar to weapon pickups)
- **Animation**: Standard float and rotation

---

## Player Feedback

### HUD Timer Display
- **Position**: Top-right corner (near status panel)
- **Format**: "BOOST: 8s" with icon
- **Icon**: Energy drink can sprite
- **Color States**:
  - White/bright: 10-4 seconds
  - Orange: 3 seconds remaining (warning)
  - Red flash: 1 second remaining (imminent expiration)
- **Transitions**: Fades in/out smoothly (0.3s)

### Screen Effects (Primary Feedback)
- **FOV Increase**: +10 degrees (simulates speed perception)
- **Chromatic Aberration**: Subtle edge distortion (motion effect)
- **Vignette Reduction**: Wider peripheral vision (better awareness at speed)
- **Transitions**: All effects lerp in/out over 0.3s

### Audio
- **None** - Keeps implementation simple, relies on visual feedback

### Cart Visual Effects
- **None** - First-person view means player won't see their own cart

---

## Technical Architecture

### New Domain Files

Following the standard domain pattern:

```
src/powerup/
├── powerup.js              # Pure data definitions
├── powerup-orchestrator.js # State management, active effects
└── powerup.test.js         # Unit tests
```

Optional mesh module (if needed):
```
src/powerup/
└── energydrink-mesh.js     # Stateless mesh creation
```

### PowerUp Data Structure

```javascript
// powerup.js
const PowerUp = {
    types: {
        SPEED_BOOST: {
            id: 'speed_boost',
            name: 'Speed Boost',
            isPowerup: true,
            spawnChance: 0.25,
            spawnWeight: 2,
            duration: 10000,        // milliseconds
            speedMultiplier: 2.0,
            visual: {
                color: 0xff3333,     // Red
                glowColor: 0xffaa00, // Yellow-orange
                scale: 2.0
            }
        }
    },

    // Helper methods
    get(typeId) { ... },
    getAll() { ... },
    selectRandom() { ... }
};
```

### PowerUpOrchestrator Responsibilities

```javascript
// powerup-orchestrator.js
const PowerUpOrchestrator = {
    activeEffects: [],  // Currently active power-ups

    // Lifecycle
    init() { ... },
    reset() { ... },

    // Activation
    activate(powerupType, timestamp) { ... },
    deactivate(powerupId) { ... },

    // Queries
    isActive(powerupType) { ... },
    getTimeRemaining(powerupType) { ... },
    getSpeedMultiplier() { ... },  // Returns current multiplier

    // Update
    update(dt, currentTime) { ... }  // Handle expiration
};
```

---

## Integration Points

### 1. PickupOrchestrator (Spawning & Collection)

**Modify spawn selection**:
- Add power-ups to weighted pickup pool
- Power-ups compete with weapons/ammo for room slots
- Use existing collision avoidance logic

**Modify collection**:
- Detect power-up type on collection
- Call `PowerUpOrchestrator.activate()` instead of weapon equip
- Return collection result to game loop for UI updates

**Modify mesh creation**:
- Add power-up mesh creation branch in `_createMesh()`
- Call `EnergyDrinkMesh.create()` or inline mesh creation
- Apply standard glow effect

### 2. PlayerOrchestrator (Movement Speed)

**Add speed multiplier query**:
```javascript
// In movement calculations
const baseSpeed = 25;
const multiplier = PowerUpOrchestrator.getSpeedMultiplier();
const currentSpeed = baseSpeed * multiplier;

// Apply to forward/backward/strafe
velocity.x = direction.x * currentSpeed * dt;
velocity.z = direction.z * currentSpeed * dt;
```

**No changes to**:
- Turn rate (maintains control at high speed)
- Acceleration curves (immediate speed change)

### 3. UIOrchestrator (HUD Timer)

**Add power-up timer display**:
```javascript
updatePowerUpTimer(timeRemaining, powerupType) {
    // Show/hide timer element
    // Update countdown text
    // Apply color transitions (white → orange → red)
    // Flash animation at 1s
}
```

**Position**: Top-right, below or beside status panel

### 4. Camera/Main Loop (FOV Effects)

**Store base FOV**:
```javascript
const BASE_FOV = 75;  // Or current value
```

**Apply FOV boost**:
```javascript
// In update loop
if (PowerUpOrchestrator.isActive('speed_boost')) {
    camera.fov = BASE_FOV + 10;
} else {
    // Lerp back to base FOV over 0.3s
    camera.fov = lerp(camera.fov, BASE_FOV, dt / 0.3);
}
camera.updateProjectionMatrix();
```

**Post-processing** (optional, can defer):
- Add EffectComposer pass for chromatic aberration
- Subtle effect on screen edges only
- Can skip initially and add later if needed

---

## Edge Cases

### Boost Expires Mid-Movement
- Lerp speed multiplier back to 1.0 over 0.2s
- Smooth deceleration, no jarring stops
- Player maintains directional velocity

### Refresh While Active
- Reset timer to 10 seconds
- No visual interruption (FOV stays wide)
- Brief flash on HUD timer to indicate refresh
- Prevents stacking to 20+ seconds

### State Transitions

**Pause Game**:
- Timer pauses (no countdown)
- Effects remain visible
- Resume continues countdown

**Game Over**:
- Clear all active boosts immediately
- Reset FOV and screen effects
- Clean state for next game

**Room Transition**:
- Boost continues (rewards mobility)
- Timer keeps counting down
- No interruption to effect

### Player Death While Boosted
- Clear active boost immediately
- Reset FOV to base value
- Remove HUD timer
- No lingering effects on respawn

---

## Testing Strategy

### Unit Tests (`powerup.test.js`)

Following TESTING.md patterns:

```javascript
// Data structure validation
test('PowerUp.types.SPEED_BOOST has required fields')
test('Duration is 10000ms (10 seconds)')
test('Speed multiplier is 2.0')

// Helper methods
test('PowerUp.get() returns correct config')
test('PowerUp.selectRandom() respects weights')

// Orchestrator logic
test('activate() starts new effect with correct duration')
test('activate() while active refreshes timer')
test('getSpeedMultiplier() returns 2.0 when active')
test('getSpeedMultiplier() returns 1.0 when inactive')
test('update() expires boost after duration')
```

### Integration Tests

```javascript
// Spawning
test('Speed boost spawns in rooms with 25% chance')
test('Speed boost competes with weapon pickups (max 1 per room)')

// Collection & Activation
test('Collecting speed boost activates effect')
test('Player speed increases to 50 units/sec when boosted')
test('Collecting second boost refreshes timer')

// Timer & Expiration
test('Boost expires after 10 seconds')
test('Speed returns to 25 units/sec after expiration')
test('HUD timer counts down accurately')

// FOV Changes
test('FOV increases by 10 when boost active')
test('FOV returns to base when boost expires')

// State Management
test('Pause stops timer countdown')
test('Game over clears active boosts')
test('Player death clears active boosts')
```

### Manual Smoke Test (30 seconds)

```
[ ] Start game, find speed boost pickup
[ ] Collect can → HUD timer appears
[ ] Movement feels noticeably faster (2x)
[ ] FOV wider, screen feels faster
[ ] Timer counts down from 10s
[ ] Timer turns orange at 3s
[ ] Timer flashes red at 1s
[ ] Boost expires smoothly at 0s
[ ] Speed returns to normal
[ ] Find second boost while already boosted
[ ] Timer refreshes to 10s (doesn't stack)
[ ] Pause → timer stops counting
[ ] No console errors
```

---

## Implementation Workflow

Following WORKFLOWS.md - "Add New Feature":

### Step 1: Create Power-Up Domain
1. Create `src/powerup/powerup.js` (data definitions)
2. Create `src/powerup/powerup-orchestrator.js` (state management)
3. Add to `index.html` script loading order (after shared, before engine)

### Step 2: Create Energy Drink Mesh
1. Create `src/powerup/energydrink-mesh.js` (optional, or inline in orchestrator)
2. Use `THREE.CylinderGeometry` for can shape
3. Apply red/yellow gradient materials
4. Return mesh for PickupOrchestrator

### Step 3: Integrate with Pickup System
1. Modify `PickupOrchestrator._createMesh()` to handle power-ups
2. Add power-ups to weighted selection in `WeaponPickup` or create separate pool
3. Modify collection logic to detect and activate power-ups

### Step 4: Player Movement Integration
1. Modify `PlayerOrchestrator` movement calculations
2. Add `getCurrentSpeedMultiplier()` query to PowerUpOrchestrator
3. Apply multiplier to forward/backward/strafe speeds
4. Add lerp for smooth expiration transition

### Step 5: Visual Feedback
1. Add FOV manipulation in main game loop (or CameraOrchestrator)
2. Store base FOV, apply +10 when boost active
3. Extend `UIOrchestrator` with power-up timer display
4. Implement color transitions (white → orange → red)
5. (Optional) Add chromatic aberration post-processing pass

### Step 6: Testing
1. Write unit tests for PowerUp config and orchestrator
2. Write integration tests for spawn → collect → boost → expire
3. Manual smoke test for feel, timing, and edge cases
4. Iterate on speed/duration if balance feels off

---

## Files Affected

### New Files (3)
- `src/powerup/powerup.js`
- `src/powerup/powerup-orchestrator.js`
- `src/powerup/powerup.test.js`

### Modified Files (4-5)
- `src/weapon/pickup-orchestrator.js` (spawn & collection)
- `src/player/player-orchestrator.js` (movement speed)
- `src/ui/ui-orchestrator.js` (HUD timer)
- `index.html` (script loading order)
- Main game loop or camera orchestrator (FOV effects)

### Optional Files (1-2)
- `src/powerup/energydrink-mesh.js` (if extracted)
- Post-processing shader (if adding chromatic aberration)

---

## Future Considerations

### Additional Power-Ups
This design creates a reusable power-up system. Future power-ups could include:
- Damage multiplier (2x or 3x damage for 8 seconds)
- Shield (temporary invulnerability extension)
- Slow-motion (bullet-time effect for precision aiming)
- Infinite ammo (no reload for 15 seconds)

All would use the same domain structure and integration points.

### Balance Tuning
Monitor after implementation:
- Is 2x speed too fast/slow? (adjust multiplier)
- Is 10s too long/short? (adjust duration)
- Is 25% spawn rate too common/rare? (adjust spawn chance)
- Does FOV change feel disorienting? (reduce to +5 degrees)

### Visual Polish
Potential enhancements:
- Particle trail effect when moving at boost speed
- Screen shake on collection (brief impact moment)
- More elaborate can design (label graphics, reflections)
- Pickup "anticipation" (glow pulses faster when player nearby)

---

## Design Rationale

### Why Speed Boost First?
- **Simplest implementation**: Single multiplier, no complex interactions
- **Clear player value**: Speed is universally understood and desired
- **Fits gameplay**: Rewards aggressive room-clearing playstyle
- **Mall theme**: Energy drink fits retail environment perfectly

### Why 2x Speed?
- **Noticeable impact**: 1.5x feels too subtle, 3x too chaotic
- **Maintains control**: Doubling speed is manageable in mall corridors
- **Risk/reward**: Faster movement means faster repositioning but less precision

### Why 10 Seconds?
- **Room-clearing window**: Enough time to clear most rooms aggressively
- **Not overpowered**: Short enough to feel tactical, not dominant
- **Session length**: In 3-minute sessions, 10s is meaningful but not game-warping

### Why Refresh (Not Stack)?
- **Predictable duration**: Player always knows they have 10s, not "10s + X"
- **Prevents runaway**: Stacking could create 30+ second boost chains
- **Rewards finding multiple**: Still valuable to grab second boost mid-effect

### Why Screen Effects?
- **Visceral feedback**: FOV change instantly communicates speed
- **No distraction**: Subtle effects don't obscure enemies or aiming
- **First-person focus**: Can't see cart in FPS, so screen is the canvas

---

## Success Criteria

Power-up is successful if:
- [ ] Collecting boost immediately feels faster (2x speed confirmed)
- [ ] Players use boost tactically (room clearing, repositioning)
- [ ] 10-second duration feels balanced (not too short/long)
- [ ] Visual feedback is clear without being distracting
- [ ] No performance issues (FOV changes, HUD updates)
- [ ] No bugs in edge cases (pause, death, refresh)
- [ ] Fits naturally into existing gameplay loop
