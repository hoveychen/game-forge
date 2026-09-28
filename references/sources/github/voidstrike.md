# VOIDSTRIKE — browser 3D RTS (StarCraft-like), Claude Code (web) + later Codex

- Repo: https://github.com/braedonsaunders/voidstrike  (demo: https://voidstrike-five.vercel.app)
- Stars: 26 (Sep 2026); 3,540 commits, 2026-01-06 → 2026-04-28
- Tool/model: Claude Code on the web (branches `claude/<task>-XXXX`, author "Claude", merged via PRs; CLAUDE.md says "ALWAYS LAUNCH OPUS 4.5 SUBAGENTS"). Later progress.md entries follow OpenAI Codex `develop-web-game` skill format ("Original prompt: ..."), so Codex was also used.
- Genre: 3-faction sci-fi RTS, WebGPU, lockstep P2P multiplayer, map editor, AI opponents
- Result evidence: README screenshots, live Vercel demo, 2,547 tests across 72 files (per progress.md), very ambitious feature list (GTAO/SSR/volumetric fog, Recast WASM navmesh, Merkle desync search). Stars modest; quality claims are the author's own.
- One-shot vs multi-session: heavily multi-session (hundreds of PRs, one per task branch).
- Notable process practices:
  - CLAUDE.md = "documentation index" table: which doc to load for which task ("Don't load everything—be selective").
  - "After EVERY code change you MUST update relevant documentation" — GAME_DESIGN.md is a living spec updated as units/mechanics are added.
  - Plan-before-code gate: "NEVER CODE UNLESS EXPLICITLY ASKED ... present a plan ... wait for approval".
  - "NEVER LEAVE THINGS INCOMPLETE, CREATE STUBS" ; tests required on every change/bugfix (regression tests).
  - Critical non-standard convention (coordinate system) called out at top of CLAUDE.md with a table.
  - Templates for new ECS system/component/feature in .claude/templates/.
  - progress.md as running handoff log: root cause, fix, tests run, what is still unverified ("Browser-level visual verification ... blocked because no playwright runtime"), TODOs.

---
## Verbatim: .claude/CLAUDE.md
# Claude Code Instructions for VOIDSTRIKE

## Project Overview

VOIDSTRIKE is a browser-based RTS game built with Next.js 14, Three.js r182, and TypeScript.

**Tech Stack:** Next.js 16 | Three.js (WebGPU/TSL) | TypeScript | ECS Architecture | P2P Multiplayer

### ⚠️ Coordinate System (Non-Standard)

This codebase uses a **non-standard coordinate convention** that differs from Three.js:

| Axis | This Codebase | Three.js Standard |
|------|---------------|-------------------|
| `transform.x` | Horizontal (east-west) | Horizontal (east-west) |
| `transform.y` | **Depth (north-south)** | Vertical (up-down) |
| `transform.z` | **Altitude (up-down)** | Depth (forward-back) |

**Ground plane = X-Y** (not X-Z as in standard Three.js)

This affects:
- Vision/fog of war calculations
- Minimap rendering
- Any 2D map logic

See `src/rendering/vision/VisionCoordinates.ts` for shared coordinate utilities.

---

DO NOT CREATE MD FILES UNLESS EXPLICITLY TOLD TO DO SO.

NEVER CODE UNLESS EXPLICITLY ASKED. Before writing any code:
1. Demonstrate understanding of the problem/request
2. Present a clear plan with specific files/changes
3. Offer alternatives or tradeoffs if applicable
4. Wait for approval before implementing

Only after user confirms should you begin coding. This prevents wasted effort and ensures alignment.

ALWAYS WRITE REFERENCE QUALITY PRODUCTION READY CODE. NEVER LEAVE THINGS INCOMPLETE, CREATE STUBS, ETC.

UPDATE TESTS WHEN APPROPRIATE:
- When modifying existing functionality → update related tests
- When adding new features → add tests for the new code
- When fixing bugs → add regression tests to prevent recurrence
- Run `npm test` to verify tests pass before committing

IF YOU NEED MORE CONTEXT, DO NOT CODE UNTIL YOU FIND IT. DO FREQUENT RESEARCH FOR THE LATEST TECHNIQUES

IF YOU SEE DEAD CODE, DUPLICATE IMPLEMENTATIONS, ETC -> SPEAK UP ABOUT IT NO MATTER IF IT IS RELATED TO YOUR CURRENT TASK.

LAUNCH SUBAGENTS FREQUENTLY, ALWAYS LAUNCH OPUS 4.5 SUBAGENTS

## Documentation Index

Load relevant documentation based on your current task. Don't load everything—be selective.

### Core Documentation (in `docs/`)

| Document | Path | Load When |
|----------|------|-----------|
| **Architecture Overview** | `docs/architecture/OVERVIEW.md` | Starting new features, understanding codebase structure, working with ECS |
| **Networking** | `docs/architecture/networking.md` | Multiplayer features, P2P, netcode, synchronization |
| **Rendering** | `docs/architecture/rendering.md` | Graphics, shaders, post-processing, visual effects |
| **Game Design** | `docs/design/GAME_DESIGN.md` | Units, buildings, factions, game mechanics, balance |
| **Audio Design** | `docs/design/audio.md` | Sound effects, music, audio systems |
| **Schema** | `docs/reference/schema.md` | Database changes, data persistence, entity schemas |
| **Models** | `docs/reference/models.md` | 3D models, GLTF specs, model requirements |
| **Textures** | `docs/reference/textures.md` | Texture specs, UV mapping, material setup |
| **Testing** | `docs/TESTING.md` | Test framework, coverage reports, testing patterns |

### Project Management (in `.claude/`)

| Document | Path | Purpose |
|----------|------|---------|
| **Templates** | `.claude/templates/` | Templates for new systems, components, tools, features |

### Tools Documentation (in `docs/tools/`)

| Tool | Path | Purpose |
|------|------|---------|
| **Blender Scripts** | `docs/tools/blender/` | Retopology, animation extraction, mesh processing |
| **Asset Pipeline** | `docs/tools/asset-pipeline/` | Meshy AI extraction, asset conversion |
| **Debug Tools** | `docs/tools/debug/` | Effect placement, visual debugging |

---

## Critical Rules

### After EVERY code change, you MUST update relevant documentation:

1. **`docs/reference/schema.md`** - When changing database tables, data structures, or entity schemas

2. **`docs/design/GAME_DESIGN.md`** - When adding units, buildings, abilities, or game mechanics

3. **`docs/architecture/OVERVIEW.md`** - When adding systems, modules, or changing architecture

4. **`docs/architecture/rendering.md`** - When adding shaders, effects, or graphics features

5. **`docs/architecture/networking.md`** - When changing multiplayer or networking code

6. **`tests/`** - Update or add tests for any modified or new functionality

### Use templates for consistency:
- New ECS system → `.claude/templates/system.md`
- New component → `.claude/templates/component.md`
- New tool/script → `.claude/templates/tool.md`
- New feature → `.claude/templates/feature.md`

---

## Code Standards

### TypeScript
- Strict TypeScript—no `any` unless absolutely necessary
- Prefer interfaces over types for object shapes
- Use enums for finite sets of values

### React Components
- Functional components with hooks
- Single-purpose, focused components
- `'use client'` directive only when needed

### Game Engine (ECS)
- All game state must be deterministic for multiplayer
- Logic in Systems, data in Components
- Use EventBus for cross-system communication
- Use `SeededRandom` from `utils/math.ts` for any randomness

### Singleton Pattern
Use class-based singletons with static methods for global managers:

```ts
export class MySingleton {
  private static instance: MySingleton | null = null;
  private static initPromise: Promise<MySingleton> | null = null;

  private constructor() { /* private constructor */ }

  // Async access (initializes on first call)
  public static async getInstance(): Promise<MySingleton> {
    if (MySingleton.initPromise) return MySingleton.initPromise;
    if (MySingleton.instance) return MySingleton.instance;
    MySingleton.initPromise = (async () => {
      const instance = new MySingleton();
      await instance.initialize();
      MySingleton.instance = instance;
      return instance;
    })();
    return MySingleton.initPromise;
  }

  // Sync access (returns null if not initialized)
  public static getInstanceSync(): MySingleton | null {
    return MySingleton.instance;
  }

  // Reset for game restart
  public static resetInstance(): void {
    MySingleton.instance = null;
    MySingleton.initPromise = null;
  }
}

// Convenience helpers for backward compatibility
export async function getMySingleton(): Promise<MySingleton> {
  return MySingleton.getInstance();
}
export function getMySingletonSync(): MySingleton | null {
  return MySingleton.getInstanceSync();
}
```

Examples: `RecastNavigation`, `WasmBoids`, `PerformanceMonitor`

### Naming Conventions
- Components: `PascalCase.tsx`
- Utilities: `camelCase.ts`
- Constants: `SCREAMING_SNAKE_CASE`
- Interfaces/Types: `PascalCase`

### Comments
Professional, understated. Explain WHY, not WHAT.

```ts
// Bad: "World-Class Particle System"
// Good: "GPU Particle System"

// Bad: "// Get the player entity"
// Good: (no comment needed)

// Bad: "// This elegant solution handles the edge case"
// Good: "// Edge case: entity may be destroyed mid-frame"
```

Acceptable: `// CRITICAL:`, `// Note:`, `// TODO:`, brief JSDoc

---

## Common Tasks Quick Reference

### Adding a New Unit
1. Add to `src/data/units/{faction}.ts`
2. Update `docs/design/GAME_DESIGN.md`
3. Update `.claude/TODO.md`
4. Test in `gameSetup.ts`

### Adding a New Building
1. Add to `src/data/buildings/{faction}.ts`
2. Update `docs/design/GAME_DESIGN.md`
3. Update `docs/reference/schema.md` if new data fields
4. Update `.claude/TODO.md`

### Adding a New System
1. Create in `src/engine/systems/`
2. Register in `Game.ts` → `initializeSystems()`
3. Document in `docs/architecture/OVERVIEW.md` (use `.claude/templates/system.md`)
4. Update `.claude/TODO.md`

### Adding Visual Effects
1. Read `docs/architecture/rendering.md` first
2. Create shader/effect code
3. Update `docs/architecture/rendering.md`
4. Update `.claude/TODO.md`

### Adding Multiplayer Features
1. Read `docs/architecture/networking.md` first
2. Ensure deterministic logic
3. Update `docs/architecture/networking.md`
4. Update `.claude/TODO.md`

---

## Testing

**Always run tests before committing:**
```bash
npm run type-check  # TypeScript validation
npm run lint        # Code style
npm test            # Run test suite
npm run dev         # Browser test
```

**When to update tests:**
- Modified a system/component → Update its corresponding test file in `tests/`
- Added new functionality → Create tests covering the new code paths
- Fixed a bug → Add a regression test that would have caught it
- Changed public API → Update tests to match new signatures

**Test file locations mirror source:**
- `src/engine/systems/CombatSystem.ts` → `tests/engine/systems/CombatSystem.test.ts`
- `src/engine/ai/BehaviorTree.ts` → `tests/engine/ai/BehaviorTree.test.ts`

See `docs/TESTING.md` for detailed testing patterns and coverage requirements.

## Commits

Use conventional commits: `feat:`, `fix:`, `docs:`, `refactor:`, `style:`, `test:`, `chore:`

---

## File Structure Overview

```
.claude/
├── CLAUDE.md           # This file (always loaded)
├── TODO.md             # Task tracking (update frequently)
└── templates/          # Doc templates for consistency
    ├── system.md
    ├── component.md
    ├── tool.md
    └── feature.md

docs/
├── README.md           # Documentation overview
├── architecture/       # Technical architecture
│   ├── OVERVIEW.md     # System architecture (2600 lines)
│   ├── networking.md   # P2P multiplayer (1500 lines)
│   └── rendering.md    # Graphics pipeline (1100 lines)
├── design/             # Game design
│   ├── GAME_DESIGN.md  # Core design doc
│   └── audio.md        # Audio system
├── reference/          # Technical specs
│   ├── schema.md       # Database schema
│   ├── models.md       # 3D model specs
│   └── textures.md     # Texture specs
└── tools/              # Development tools
    ├── blender/        # Blender scripts
    ├── asset-pipeline/ # Asset processing
    └── debug/          # Debug utilities
```

---

## Remember

**Documentation is the source of truth.** Always update docs when making changes. Load only the docs you need for your current task to preserve context.


---
## Verbatim: docs/design/GAME_DESIGN.md (first 300 of 641 lines)
# VOIDSTRIKE - Design Document

## Overview

VOIDSTRIKE is a browser-based real-time strategy game built with modern web technologies. It features 3D graphics, competitive multiplayer, and deep strategic gameplay.

## Core Vision

**"Zero-friction competitive RTS"** - Click and play from any browser, no downloads required.

## Technical Architecture

### Frontend Stack

- **Three.js / React Three Fiber** - 3D rendering engine
- **Next.js 14** - App Router, Server Components
- **TypeScript** - Full type safety
- **Zustand** - Game state management
- **Web Workers** - Pathfinding, AI, simulation offloading
- **WebGPU** (WebGL fallback) - Graphics performance
- **Howler.js** - Spatial audio

### Backend Stack (Supabase + Vercel)

- **Supabase Realtime** - WebSocket multiplayer
- **Supabase Database** - Player data, matches, rankings
- **Supabase Auth** - OAuth authentication
- **Supabase Edge Functions** - Game server logic
- **Vercel Edge Functions** - Matchmaking
- **Vercel KV** - Session state caching

## Game Architecture

### Entity Component System (ECS)

The game uses an ECS architecture for maximum performance and flexibility:

```
Entity: Unique ID
Components: Data containers (Position, Health, Selectable, etc.)
Systems: Logic processors (MovementSystem, CombatSystem, etc.)
```

### Game Loop

```
1. Process Inputs (player commands)
2. Run Systems (physics, AI, combat)
3. Update State (ECS world)
4. Render Frame (Three.js)
5. Sync Network (multiplayer only)
```

### Lockstep Simulation

For multiplayer, we use deterministic lockstep:

- All clients run identical simulations
- Only inputs are transmitted (not state)
- Periodic checksums detect desync
- Enables replay system for free

## Faction Design

### The Dominion (Humans)

- **Theme**: Military industrial complex
- **Playstyle**: Versatile, defensive, siege warfare
- **Unique Mechanics**:
  - Siege modes (units transform)
  - Bunkers and fortifications
  - Healing/repair units

### The Synthesis (Machine Consciousness)

- **Theme**: Transcendent AI collective
- **Playstyle**: Powerful but expensive, shield-based
- **Unique Mechanics**:
  - Warp-in (instant unit deployment)
  - Shield regeneration
  - Psionic abilities

### The Swarm (Organic Hive)

- **Theme**: Adaptive biological horror
- **Playstyle**: Cheap, fast, overwhelming
- **Unique Mechanics**:
  - Creep spread (terrain control)
  - Unit morphing/evolution
  - Passive regeneration

## Resource System

### Primary Resources

1. **Minerals** - Basic resource, abundant
2. **Plasma** - Advanced resource, limited

### Economy Flow

```
Workers -> Resource Nodes -> Storage -> Production
```

### Worker Saturation

Each resource node displays worker assignment status with floating labels showing "X/Y" (current/optimal):

| Resource Type | Optimal Workers | Max Useful Workers | Label Color                             |
| ------------- | --------------- | ------------------ | --------------------------------------- |
| **Minerals**  | 2 per patch     | 3 per patch        | Green when saturated, Yellow when under |
| **Plasma**    | 3 per geyser    | 3 per geyser       | Green when saturated, Yellow when under |

- **Green (X/Y)**: Optimal saturation reached - maximum efficiency
- **Yellow (X/Y)**: Undersaturated - workers needed for optimal income
- **Gray (0/Y)**: No workers assigned

AI prioritizes filling extractors to 3 workers first, then distributes workers evenly across mineral patches (2 per patch optimal, 3 maximum).

## Combat System

### Auto-Attack Behavior

Units automatically engage enemies based on their state:

| Unit State        | Target Acquisition            | Notes                               |
| ----------------- | ----------------------------- | ----------------------------------- |
| **Idle**          | Immediate within attack range | Instant response, no throttle delay |
| **Hold Position** | Within attack range only      | Won't move to engage                |
| **Patrolling**    | Within sight range            | Engages then resumes patrol         |
| **Attack-Moving** | Within sight range            | Engages then resumes move           |

**Targeting Priority** (higher = attacked first):

1. Devastators, Dreadnoughts, Colossus (90-100) - High threat units
2. Specters, Operatives, Breachers (70-85) - Tactical threats
3. Troopers, Scorchers, Valkyries (50-60) - Standard combat
4. Vanguards, Lifters (40-45) - Support units
5. Buildings (30) - Structures
6. Workers (10) - Lowest priority

Target scoring also considers:

- **Distance** - Closer enemies are prioritized
- **Health** - Damaged enemies are prioritized

### Attack Targeting Types

Units have restrictions on what they can attack based on air/ground targeting:

| Target Type      | Can Attack Ground | Can Attack Air | Example Units                                                        |
| ---------------- | ----------------- | -------------- | -------------------------------------------------------------------- |
| **Ground & Air** | ✅                | ✅             | Trooper, Breacher, Colossus, Specter, Dreadnought (continuous laser) |
| **Ground Only**  | ✅                | ❌             | Fabricator, Scorcher, Devastator, Valkyrie (Assault Mode)            |
| **Air Only**     | ❌                | ✅             | Valkyrie (Fighter Mode)                                              |
| **No Attack**    | ❌                | ❌             | Lifter, Overseer                                                     |

**Transform Mode Targeting**: Some units change targeting when transforming:

- **Valkyrie Fighter Mode** (flying): Air only - anti-air specialist
- **Valkyrie Assault Mode** (ground): Ground only - ground assault
- **Devastator/Scorcher**: Ground only in all modes (artillery/flamethrower)

**AI Transform Intelligence**: AI-controlled units intelligently transform based on nearby enemy composition:

- **Valkyrie**: Transforms to Fighter Mode when air enemies present (no ground), Assault Mode when ground enemies present (no air). Uses threat scores for mixed situations.
- **Scorcher**: Transforms to Inferno mode (area-of-effect) when 2+ enemies are nearby, reverts to Scorcher mode (mobile) when no enemies in range.

**AI Counter-Building**: When AI units are attacked by enemies they cannot hit (e.g., air units attacking ground-only troops), the AI urgently prioritizes building anti-air capable units.

### AI Air Unit Control

The AI manages air units as an independent tactical arm:

**Air Combat Units** (Valkyrie, Specter, Dreadnought):
- Separated from ground army during attacks
- Execute flanking maneuvers perpendicular to the main ground attack
- Perform hit-and-run micro (reposition after attacking)
- Disengage automatically when health drops below 30%
- Used for worker harassment between major attacks

**Air Support Units** (Lifter, Overseer):
- Follow the main army at a safe distance behind the centroid
- Provide healing (Lifter) and detection (Overseer) support
- Not included in combat formations

**Valkyrie Transform Intelligence**:
- Switches to Fighter mode when air threats dominate (1.5x threshold)
- Switches to Assault mode when ground threats dominate (1.5x threshold)
- More aggressive mode-switching than previous 2x threshold

**Air Production Priority**:
- Valkyrie: priority 54 (primary air unit)
- Specter: priority 52 (cloaked strike)
- Dreadnought: priority 58 (capital ship)
- Air Superiority response: priority 75 when enemy has air
- Emergency anti-air: priority 95 on all difficulties

### AI Personality System

Each AI player is assigned a personality that determines its strategic behavior, army composition, and build order selection. In multi-AI games, personalities are varied so no two AIs play identically.

| Personality    | Style            | Early Game                             | Late Game                             |
| -------------- | ---------------- | -------------------------------------- | ------------------------------------- |
| **Balanced**   | Well-rounded     | Trooper/Breacher/Vanguard mix          | Diverse army with all unit types      |
| **Aggressive** | Fast pressure    | Scorcher/Vanguard heavy, early attacks | Valkyrie/Specter focused              |
| **Defensive**  | Fortify & tech   | Trooper/Breacher/Devastator            | Colossus/Dreadnought deathball        |
| **Economic**   | Greedy expansion | Light defense, fast expand             | Colossus/Dreadnought/Operative heavy  |
| **Cheese**     | All-in rush      | Scorcher/Vanguard rush                 | Pivots to Valkyrie/Devastator if held |
| **Turtle**     | Slow & steady    | Trooper/Devastator behind defenses     | Colossus/Dreadnought siege force      |

Personality affects:

- **Build order selection**: Each personality prefers matching build order styles (e.g., aggressive AI picks aggressive openers)
- **Composition goals**: Per-phase army composition targets that drive production scoring
- **Macro rules**: Personality-filtered rules for extra production buildings, earlier expansions, etc.
- **Attack timing**: More aggressive personalities attack earlier and with smaller armies

### Damage Types

- **Normal** - Standard damage
- **Explosive** - Bonus vs large, reduced vs small
- **Concussive** - Bonus vs small, reduced vs large
- **Psionic** - Ignores armor

### Armor Types

- **Light** - Infantry, workers
- **Armored** - Vehicles, heavy units
- **Massive** - Capital ships, structures
- **Naval** - Ships and submarines
- **Shields** - Synthesis units (regenerates)

## Naval Combat

### Movement Domains

Units have a movement domain that determines where they can move:

| Domain         | Land | Shallow Water   | Deep Water | Air |
| -------------- | ---- | --------------- | ---------- | --- |
| **Ground**     | ✅   | ✅ (0.6x speed) | ❌         | ❌  |
| **Water**      | ❌   | ✅              | ✅         | ❌  |
| **Amphibious** | ✅   | ✅              | ✅         | ❌  |
| **Air**        | ✅   | ✅              | ✅         | ✅  |

### Naval Targeting

| Unit Type        | Can Attack Ground | Can Attack Air | Can Attack Naval |
| ---------------- | ----------------- | -------------- | ---------------- |
| **Ground Units** | ✅ (varies)       | ✅ (varies)    | ❌ (most)        |
| **Naval Units**  | ✅ (varies)       | ✅ (varies)    | ✅               |
| **Air Units**    | ✅ (varies)       | ✅ (varies)    | ✅ (most)        |

### Torpedo Damage Type

New damage type for anti-ship weapons:

| Torpedo vs | Multiplier |
| ---------- | ---------- |
| Light      | 0.5x       |
| Armored    | 0.75x      |
| Massive    | 1.0x       |
| Naval      | 1.5x       |
| Structure  | 1.25x      |

### Submarine Mechanics

Submarines (Hunter) have special submerge mechanics:

- **Surfaced**: Normal speed, can use deck gun, visible
- **Submerged**: Reduced speed (67%), cloaked, torpedo attacks only
- Detected by: Radar Array, Overseer, other submarines (sonar)

### Shore Bombardment

Naval capital ships (Leviathan) can attack land targets:

- Normal attack range applies to coastal targets
- Shore Bombardment ability: Long-range artillery strike (75 energy)
- Yamato Cannon: 150 damage single target (100 energy)

### Dominion Naval Units

| Unit          | Cost      | Supply | HP  | Armor       | Speed | Range | DPS  | Role                 |
| ------------- | --------- | ------ | --- | ----------- | ----- | ----- | ---- | -------------------- |
| **Mariner**   | 75m       | 1      | 60  | 0 (Light)   | 4.5   | 1     | 3.5  | Naval worker         |
| **Stingray**  | 100m      | 2      | 120 | 0 (Light)   | 6.5   | 6     | 7.2  | Fast patrol          |
| **Corsair**   | 150m/75v  | 3      | 200 | 1 (Armored) | 3.5   | 8     | 16.8 | Anti-air frigate     |
| **Leviathan** | 350m/250v | 6      | 500 | 3 (Massive) | 2.25  | 10    | 12.5 | Battlecruiser        |
| **Hunter**    | 200m/150v | 4      | 175 | 1 (Armored) | 3.0   | 7     | 14   | Submarine            |
| **Kraken**    | 200m/100v | 3      | 250 | 2 (Armored) | 3.5   | 6     | 24   | Amphibious transport |

### Dominion Naval Buildings

| Building              | Cost      | Size | HP   | Requirements      | Description                     |
| --------------------- | --------- | ---- | ---- | ----------------- | ------------------------------- |
| **Drydock**           | 200m/100v | 4×4  | 1500 | Forge             | Naval production (coastline)    |
| **Offshore Platform** | 150m      | 3×3  | 800  | Drydock           | Naval supply point (deep water) |
| **Armed Platform**    | +100m/50v | 3×3  | 1000 | Offshore Platform | Defensive upgrade               |


---
## Verbatim: .claude/templates/feature.md
# Feature Documentation Template

Use this template when documenting a new game feature in `docs/design/`.

## Template

```markdown
# {Feature Name}

## Overview
{2-3 sentence description of the feature}

## Design Goals
- {Goal 1}
- {Goal 2}
- {Goal 3}

## User Experience
{How players interact with this feature}

## Technical Implementation

### Components
- `{ComponentName}`: {purpose}

### Systems
- `{SystemName}`: {purpose}

### Data Files
- `src/data/{file}`: {purpose}

## Configuration
| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| {setting} | {type} | {value} | {description} |

## Edge Cases
- {Edge case 1}: {how it's handled}
- {Edge case 2}: {how it's handled}

## Future Improvements
- [ ] {Potential improvement 1}
- [ ] {Potential improvement 2}
```


---
## Excerpt: progress.md (first 30 lines)
Original prompt: cant get this app to start locally

- Investigated `npm run build` failure on macOS.
- Root cause: `src/engine/components/Unit.ts` re-exported from `./unit`, which can resolve ambiguously on case-insensitive filesystems because the facade itself is `Unit.ts`.
- Applied fix: changed the facade to re-export from `./unit/index` explicitly.
- Verified `npm run build` succeeds.
- Verified `npm run type-check` succeeds.
- Verified `npm run dev` starts successfully; Next selected `http://localhost:3001` because port `3000` was already in use locally.
- The `develop-web-game` Playwright client could not be used because the `playwright` package is not installed in this environment.
- No further action required for the original startup/build issue.

- Investigated pathfinding regression on elevated maps.
- Reproduced the bug below the game loop: Recast paths on elevated bundled maps were truncating partway up/down ramps, while the flat test map still reached its destination.
- Replaced the flat-per-cell navmesh geometry path with a shared ramp-aware geometry builder and wired editor validation to the same logic.
- Removed the terrain-grid fallback after confirming the root issue was navmesh geometry, not movement execution.
- Added ramp metadata normalization so both bundled ramps and editor-inferred flat ramps derive their direction and endpoint elevations from surrounding walkable terrain before Recast heightfields are built.
- Replaced the fallback-specific tests with Recast connectivity regressions for `contested_frontier`, `crystal_caverns`, `titans_colosseum`, and a synthetic flat-ramp editor map.
- Verified `npm run type-check`, targeted `recastRampConnectivity` and `pathfindingSystem` tests, full `npm test` (72 files / 2547 tests), and `npm run lint` with only pre-existing warnings.
- TODO: Verify full long-haul spawn-to-spawn routes on `scorched_basin` and `void_assault` if we want cross-map regression coverage beyond the local elevated-move cases.

- Updated the PWA install UI so the global bottom-right install prompt no longer renders from the app layout.
- Reworked `src/components/pwa/InstallPrompt.tsx` into a compact `InstallAppButton` that reuses the existing install flow but renders as an icon-only control.
- Added the compact install button beside the existing mute/fullscreen controls on the home page, game setup page, and editor header.
- Verified `npm run type-check` and `npm run build` pass after the UI change.
- Verified targeted ESLint on the touched files reports only two pre-existing warnings: the unused `eslint-disable` in `src/app/game/setup/page.tsx` and the existing custom-font warning in `src/app/layout.tsx`.
- Browser-level visual verification of the install button placement is still blocked here because the repo does not include a usable `playwright` runtime, and the install prompt itself depends on a browser-only `beforeinstallprompt` event.

- Continued investigating the pathfinding stop-after-an-inch bug after gameplay reports showed it also happened on multiple bundled maps near starting bases, not just on ramps.
- Root cause: the nested pathfinding worker could finish loading its navmesh after startup buildings and decoration collisions were already registered on the authoritative main-thread `RecastNavigation` TileCache. In that case the worker never received those existing obstacles, so it planned straight through the starting HQ/decor while movement/collision stopped units almost immediately.
- Applied fix in `src/engine/systems/PathfindingSystem.ts`: retain registered decoration collisions, and whenever the worker reports `navMeshLoaded`, replay all current building and decoration obstacles into the worker so worker-side path queries match the authoritative obstacle state.
