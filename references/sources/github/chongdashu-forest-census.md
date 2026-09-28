# Forest Census — Three.js voxel counting minigame (Mario Party-style), Codex CLI + Three.js agent skill

- Repo: https://github.com/chongdashu/threejs-forest-census  (live: https://forestcensus.aioriented.dev)
- Stars: 35
- Tool/model: OpenAI Codex CLI + custom `threejs-builder` skill (.codex/skills/threejs-builder/SKILL.md)
- Genre: single-scene 3D minigame (count yellow chicks in 20 s, submit guess)
- Result evidence: live deployed build, concept art in repo, companion YouTube video. Small scope.
- One-shot vs multi-session: PRD (412 lines, written with TinyPRD) + TDD (290 lines) → Codex build, largely one pass (repo is 1 squashed commit).
- Notable practices: PRD states Three.js version, single-file constraint, unit system (1 unit = 1 m, player 1.6 u), *allowed* materials/lights/geometries, hex palette, camera pitch, and a rule that "V1 must be playable with procedural voxel primitives even if external textures fail to load" (fallback-first). Asset manifest (assets.json) is single source of truth for model paths.

---
## Verbatim: public/forest/PRD.md (full)
# Cube Census: Forest Edition — Game Design Document

## 1. Summary
A 3D voxel “dollhouse” counting minigame where the player has **20 seconds** to **count all Yellow Chicks** wandering a cluttered forest clearing, then **submit a guessed number**; you win only if it matches the **exact spawned chick count**.

---

## 2. Technical Requirements
- **Rendering:** Three.js **r160**
- **Single HTML file** (one `index.html`) with inline CSS + JS
- **Unit system:** **World units** where **1 unit ≈ 1 meter** (reference: player height ≈ **1.6 units**)
- **Three.js allowed materials:** MeshStandardMaterial (primary), MeshBasicMaterial (UI planes)
- **Three.js allowed lights:** HemisphereLight + DirectionalLight (primary), optional AmbientLight (very low)
- **Geometries:** BoxGeometry (dominant voxel look), CylinderGeometry (optional trunks), PlaneGeometry (ground/UI)

**Assets**
- The provided atlas/mockup are **visual references**. V1 must be playable with **procedural voxel primitives** (boxes/planes) even if external textures fail to load.
- Optional: use a single **texture atlas image** as a ground/detail texture; must have a clean fallback to flat colors.

---

## 3. Canvas & Viewport
- **Internal render size:** 960×540 (16:9)
- **Responsive behavior:** scale-to-fit window with **letterboxing** (preserve aspect ratio)
- **Background:** vertical sky gradient (top → horizon) plus light fog feel via color haze:
  - Sky top: `#BFE8FF`
  - Horizon: `#E9FFF2`

---

## 4. Visual Style & Art Direction
**Look:** Low-poly voxel diorama (Quaternius-like), chunky silhouettes, soft lighting, bright readable colors.

### Palette (minimum set)
- Grass base: `#6CC04A`
- Grass shadow: `#4E9A33`
- Dirt path: `#B9855A`
- Trunk brown: `#8B5A3C`
- Leaf green A: `#8DDC4C`
- Leaf green B: `#A6F05A`
- Rock gray: `#9AA0A6`
- Bush green: `#63B84A`
- Chick yellow: `#FFD33D`
- Chicken white: `#F2F2F2`
- Pig pink: `#F3A0B4`
- Sheep wool: `#D9D9D9`
- UI ink dark: `#2A1B1B`
- UI accent red: `#B84A4A`

### Camera (dollhouse side-scroll)
- **Style:** Fixed elevated “toybox” view with shallow perspective.
- **Angle:** camera looks downward at ~35–45° pitch, slightly from front (so **depth/Z** is visible).
- **Behavior:** camera is mostly fixed but **pans left/right** when the player approaches screen edges (details in Section 6).
- **Goal:** keep counting readable; NPCs can be partially occluded by trees/bushes.

### Lighting mood
- Bright, soft daylight:
  - HemisphereLight: cool sky / warm ground
  - DirectionalLight: gentle sun; soft, non-dramatic shadows (if shadows are implemented, keep them subtle).

---

## 5. Player Specifications
### Appearance
- Voxel child-like character (block head/body/limbs), flat-shaded.
- A small “floating counter UI” hovers above the head (always visible).

### Size
- Height: **1.6 units**
- Width: **0.7 units**
- Depth: **0.45 units**

### Colors
- Shirt: `#C94C3A`
- Shorts: `#2E78C7`
- Skin: `#F2C9A0`
- Hair: `#E7C04B`

### Starting position
- World position: **X = 0, Z = 0**, centered horizontally, slightly front-middle depth.

### Movement constraints
- Player moves in **X (left/right)** and **Z (forward/back)** on a flat plane.
- Player cannot leave the clearing bounds and cannot pass through trees/rocks/bushes.

### Animation states (voxel-style, simple but expressive)
- **Idle:** gentle breathing bob + tiny head sway.
- **Walk:** bouncy step (slight vertical bob) with arm swing.
- **Counter change:** quick “nod” + UI pulse.
- **Submit:** brief “raise hands” / celebratory pose lock for 0.4s.
- **Result:** win bounce vs. lose slump.

(Animations can be done via simple transforms on voxel parts; no skeletal requirement.)

---

## 6. Physics & Movement
**Axis conventions**
- X = left/right
- Z = depth (forward/back)
- Y = up
- Up is **+Y**

### Core movement (top-down-ish but perspective)
| Property | Value | Unit |
|---|---:|---|
| Player max walk speed | 4.2 | units/sec |
| Player acceleration | 18 | units/sec² |
| Player deceleration | 22 | units/sec² |
| NPC max walk speed (varies by species) | 1.5–2.8 | units/sec |
| NPC turn smoothing | 0.18 | sec (time constant feel) |
| World bounds (half extents) | X: 12, Z: 6 | units |
| Camera pan speed (tracking) | 6.5 | units/sec |
| Camera edge-pan threshold | 12% | screen width (from left/right edges) |

### Camera pan rule (side-scroll feel)
- The camera has a **target X** that follows the player only when the player enters an edge zone:
  - If player screen-space X < 12% from left edge → camera target X decreases
  - If player screen-space X > 88% from left edge → camera target X increases
  - Otherwise camera target X holds (player can move within the “safe zone” without camera drift)
- Camera Z and Y remain constant (fixed dollhouse depth framing).

---

## 7. Obstacles / NPCs

## 7.1 Forest obstacles (occluders)
Purpose: create counting chaos by breaking line-of-sight and forcing repositioning.

### Trees
- **Shape:** trunk (box/cylinder) + cubic leafy canopy clusters (2–3 stacked boxes)
- **Footprint collider:** ~1.2×1.2 units
- **Height:** 4.5–6.0 units
- **Placement:** scattered with intentional “lanes” so the player can weave through.

### Bushes
- **Shape:** low blob of voxel cubes
- **Footprint:** ~1.4×1.0 units
- **Height:** ~0.9 units
- **Occlusion:** can hide chicks partially; should not fully block tall animals.

### Rocks
- **Shape:** irregular stacked boxes
- **Footprint:** ~1.2×1.2 units
- **Height:** ~0.7 units

**Obstacle density target**
- Trees: 12–18
- Bushes: 10–16
- Rocks: 6–10  
(All within bounds; keep a clear central “playable weave” region.)

---

## 7.2 NPCs (targets + distractions)

### Shared NPC rules (symmetry & fairness)
- All NPCs move using the same constraints as the player: **X/Z plane**, within world bounds.
- All NPCs **avoid obstacles** and do not overlap each other too tightly (keep readable clusters).
- NPCs can pass behind trees/bushes (visual occlusion), but must remain reachable/visible by repositioning.

### Target: Yellow Chicks
- **Count range (spawned per round):** 6–14 (uniform random)
- **Size:** 0.45(W) × 0.45(D) × 0.55(H) units
- **Color:** body `#FFD33D`, beak `#E88B2D`, comb `#C94C3A`
- **Movement:** erratic wander with frequent micro-turns
  - Speed: **2.2–2.8 units/sec**
  - Direction change: every **0.35–0.9 sec** (random)
  - Occasional “pause peck”: 0.2–0.5 sec (still counts as present)

### Distraction: White Chickens (look-alike)
- **Count range:** 3–10
- **Size:** slightly larger than chicks: 0.55×0.55×0.7
- **Color:** body `#F2F2F2` with red comb
- **Movement:** steadier than chicks
  - Speed: 1.8–2.2 units/sec
  - Direction change: 0.7–1.5 sec

### Distraction: Pigs
- **Count range:** 2–6
- **Size:** 0.9×0.5×0.6
- **Color:** `#F3A0B4`
- **Movement:** slow roam
  - Speed: 1.5–1.9 units/sec

### Distraction: Sheep
- **Count range:** 2–6
- **Size:** 0.95×0.6×0.8
- **Color:** wool `#D9D9D9`, face `#3A3A3A`
- **Movement:** medium roam + occasional stop
  - Speed: 1.6–2.0 units/sec
  - Rest: 0.4–0.9 sec occasionally

### Spawn rules
- Spawn all NPCs at round start (no mid-round spawns in V1).
- Spawn positions must:
  - Be within bounds
  - Not overlap obstacles (minimum 0.6 units clearance from tree trunks)
  - Avoid spawning too close to the player (minimum 2.5 units)

### Despawn condition
- None in V1 (all remain in scene until submission/time end).

---

## 8. World & Environment
### Ground
- One main ground plane with subtle tile variation (either via atlas texture or procedural color noise).
- Add faint “grid seams” or path strips to enhance depth reading.

### Layering / depth readability
- Back layer: denser tree line silhouettes (non-colliding set dressing) for forest feel.
- Mid layer: colliding trees/bushes/rocks (gameplay occluders).
- Foreground: a few bushes/flowers near camera edges to reinforce parallax (optional).

### If external asset loading fails
- All objects render as colored voxel primitives with the palette above.
- UI remains readable and fully functional.

---

## 9. Collision & Scoring
### Collision detection approach
- **Player vs. obstacles:** axis-aligned box collision (AABB) on X/Z footprints.
- **NPC vs. obstacles:** same AABB footprint rules (simple avoidance is fine; must not get stuck).
- **Player vs. NPC:** no hard collision required; allow passing through NPCs (prevents frustration while counting).

### Forgiving hitboxes (for movement smoothness)
- Obstacle colliders are **shrunk by 0.12 units** per side compared to the visible mesh footprint (player-friendly navigation).

### Win / lose logic
- Player’s submitted counter must equal **exact number of Yellow Chicks spawned** at round start.
- If time expires without manual submission: auto-submit current counter at **0.00** remaining.

### Score / progression (arcade framing)
- Track **streak**: consecutive correct rounds.
- Track **best streak** in localStorage: key `voxelCensus_bestStreak`
- Track last round result breakdown (for results screen):
  - Actual chicks
  - Player submitted
  - Difference (absolute)

(No points math needed; the “puzzle” is correctness under pressure.)

---

## 10. Controls
| Input | Action | Condition |
|---|---|---|
| W | Move forward (increase Z) | Playing |
| S | Move backward (decrease Z) | Playing |
| A | Move left (decrease X) | Playing |
| D | Move right (increase X) | Playing |
| ↑ Arrow | Increase counter by +1 | Playing (clamped) |
| ↓ Arrow | Decrease counter by -1 | Playing (clamped) |
| Space | Submit count immediately | Playing (once) |
| P or Escape | Pause / Resume | Playing / Paused |
| Enter | Start / Restart | Menu / Game Over |

**Counter clamp**
- Minimum: **0**
- Maximum: **24** (comfortably above max possible chicks to prevent “cap loss” confusion)

---

## 11. Game States

### 11.1 Menu
**Displayed**
- Title: Cube Census: Forest Edition”
- One-paragraph objective: “Count ONLY the Yellow Chicks.”
- **Controls list visible** (keyboard diagram style)
- “Press Enter to Start”
- Best streak display (from localStorage)

**Background**
- Live scene running slowly (NPCs wander at 35% speed) to show gameplay vibe.

---

### 11.2 Playing
**Active**
- Timer countdown (top-center)
- Best streak + current streak (top-left)
- Controls hint (top-right, compact)
- Floating counter UI above player (always)

**End triggers**
- Space submission OR timer hits 0.00 → lock input and transition to Results.

---

### 11.3 Paused
**Trigger:** P or Escape
- Overlay: semi-transparent dark veil + “PAUSED”
- Controls: “P/Esc to Resume, Enter to Restart, M to Menu (optional)”
- Everything frozen: timer, NPCs, camera.

---

### 11.4 Results (Game Over / Round Over)
**Displayed**
- “Correct!” or “Wrong!”
- Actual chick count
- Your submitted number
- Difference
- Current streak + best streak
- “Enter: Play Again” and “Backspace: Menu” (controls visible)

**Persistence**
- If correct: streak++
- If wrong: streak resets to 0
- Update best streak in `voxelCensus_bestStreak`

---

## 12. Game Feel & Juice (REQUIRED)

## 12.1 Input Response (same-frame acknowledgment)
- **Movement keys (WASD):**
  - Player immediately leans slightly into direction (max tilt 6°) even before reaching top speed.
- **Counter up/down:**
  - Floating UI number pops (scale up then settle) on every change.
  - Player does a quick “count nod” (head dips 6° then returns).
- **Denied counter input (trying to go below 0 or above max):**
  - UI ring flashes `#B84A4A` for 0.12s + tiny shake (2px screen-space equivalent).

## 12.2 Animation Timing (durations & easing targets)
- **UI pop on counter change:** 0.14s up, 0.18s settle (ease-out then ease-in)
  - Scale: 1.0 → 1.18 → 1.0
- **Player walk bob:** ~2.2 steps/sec at max speed (bouncy but not floaty)
- **Submit “lock-in”:** 0.08s freeze-frame + 0.25s zoom pulse (see screen effects)

## 12.3 Near-Miss Rewards (counting equivalent: “Confirmed Sighting”)
Purpose: reward the act of *visually verifying* a chick, not just mashing the counter.

- **Detection:** A Yellow Chick is within **3.2 units** of the player AND within a **60° forward view cone** AND is not heavily occluded (i.e., line between player and chick is not intersecting a tree trunk collider).
- **Reward (once per chick per round):**
  - Small floating text near chick: “CONFIRMED +1” (does not change the counter automatically)
  - Brief golden sparkle burst (simple quads/points) around chick for 0.35s
  - Micro time-dilation: 0.92× for 0.25s (subtle, just a “moment”)
- **Intent:** players learn to *move to get clean views* and mentally tally.

## 12.4 Screen Effects
| Effect | Trigger | Feel |
|---|---|---|
| Zoom pulse | Counter change, Submit | 1.00→1.03 scale, 0.18s |
| Flash vignette | Confirmed sighting | soft yellow vignette `#FFD33D` at 18% opacity, 0.20s |
| Screen shake | Wrong result reveal | 0.25s, small horizontal jitter (feels “uh-oh”) |
| Freeze frame | Submit | 0.08s dramatic lock-in |

## 12.5 Progressive Intensity (as time runs out)
- At **10s remaining:** timer text shifts to warmer color, subtle tick emphasis.
- At **5s remaining:** timer pulses every second; ambient scene slightly increases contrast.
- At **2s remaining:** stronger pulse + soft red vignette (opacity 12%) to raise urgency.

## 12.6 Idle Life (scene never feels static)
- Player idle: breathing bob 0.06 units amplitude, 2.5s cycle.
- Trees: ultra-subtle canopy sway (just enough to feel alive).
- NPCs: occasional peck / head-bob even while paused in place.
- UI: counter ring slowly rotates (very slowly) when not changing.

## 12.7 Milestone Celebrations
- Every time the player reaches a **new best streak**, show a small banner:
  - “NEW BEST STREAK!” slides in (0.22s) and out (0.22s), with gold accent.

## 12.8 Result / Failure Sequence
- **On submit:** freeze-frame 0.08s → camera zoom pulse 0.25s → fade to Results overlay 0.25s.
- **On wrong:** add 0.25s shake and briefly desaturate scene (0.35s) behind the overlay.
- **On correct:** player does a quick hop-in-place animation (no physics jump needed; just pose + bob) and a green-tinted flash (`#8DDC4C`, 12% opacity, 0.2s).

---

## 13. UX Requirements
- Controls must be **visible on Menu** and **during gameplay**.
- Timer must be large and readable; never hidden by the 3D scene.
- Counter UI must be readable at all times:
  - Use high-contrast outline and a stable screen-facing orientation (billboard feel).
- Forgiving navigation:
  - Obstacle colliders shrunk by **0.12 units** per side.
  - No player collision with NPCs.
- Accessibility-lite:
  - Color distinction: Yellow Chicks must be clearly more saturated than White Chickens; add a tiny signature (e.g., chick has a brighter beak or a slightly different head proportion).

---

## 14. Out of Scope (V1)
1. Sound effects / music
2. Multiple levels/biomes (only Forest clearing)
3. Online leaderboards
4. Power-ups (slow time, highlight chicks, etc.)
5. Complex flocking AI or advanced pathfinding
6. Mouse/touch controls (keyboard only in V1; can be added later)
7. Shadow-mapping quality settings

---

## 15. Success Criteria
- [ ] Runs from a **single HTML file** without errors
- [ ] Uses **Three.js r160**
- [ ] Controls visible on **menu** and **in-game**
- [ ] Timer defaults to **20 seconds** (configurable constant)
- [ ] Player moves in **X/Z** with clear camera edge-panning behavior
- [ ] Yellow Chicks + distractor NPCs spawn within defined ranges and wander
- [ ] Submit locks answer; auto-submit at time-out
- [ ] Win only if submitted count equals actual spawned Yellow Chick count
- [ ] Counter change has immediate feedback (pop + nod) and denied-input feedback
- [ ] “Confirmed sighting” near-miss equivalent triggers once per chick per round
- [ ] Pause freezes timer/NPCs/camera; resume restores cleanly
- [ ] Best streak persists via `localStorage` key `voxelCensus_bestStreak`
- [ ] Scene has idle life (breathing, subtle sway) even when player stands still

---

---
## Verbatim: public/forest/TDD.md (full)
# Cube Census: Forest Edition — Technical Design Document
_Last updated: 2025-12-30_

## 1. Intent & References
- **Goal:** Ship the Forest counting minigame described in `forest/PRD.md` and illustrated by `forest/design.png`: a 960×540 fixed-aspect Three.js diorama where the player counts only Yellow Chicks within 20 seconds and submits a guess.
- **Sources consulted:** `forest/PRD.md`, `forest/design.png`, `assets.json`, `ASSET_INDEX.md`, and Three.js execution guidance from `.codex/skills/threejs-builder/SKILL.md`.
- **Clarified decisions (per user):**
  1. Counter UI renders as a DOM overlay anchored to the screen center (not attached to the player mesh).
  2. Use the provided GLTF models “as is” for player, chicks, chickens, pigs, sheep, and foliage (no voxel primitives unless a loader failure occurs).
  3. Lighting spec in the PRD stands; no extra discussion needed.

## 2. Implementation Constraints
- **Single file deliverable:** `forest/index.html` contains HTML, inline CSS, and `<script type="module">` JavaScript.
- **Engine:** Three.js r160 via ES modules (from unpkg). Only use `MeshStandardMaterial` (scene) and `MeshBasicMaterial` (UI planes) as mandated.
- **Performance guardrails (per threejs-builder skill):**
  - Clamp DPR to `Math.min(devicePixelRatio, 2)`.
  - `renderer.outputColorSpace = THREE.SRGBColorSpace` and `renderer.toneMapping = THREE.ACESFilmicToneMapping` for consistent palette.
  - Reuse geometries/materials, avoid per-frame allocations, and keep draw calls low by instancing environment GLTFs.
- **World contract:** 1 Three.js unit ≈ 1 meter. Ground plane at `y = 0`. Characters rest such that their `minY == 0`.
- **States:** `loading → menu → playing → paused/results`, with a latching transition function (`setMode(next)`).
- **Input:** Keyboard only (WASD, arrow keys, Space/Enter/Backspace/P/Esc) per PRD table.
- **Persistence:** localStorage key `voxelCensus_bestStreak`.

## 3. Asset & Content Plan (from assets.json)
### 3.1 Character + NPC models
| Usage | Asset key | Path |
| --- | --- | --- |
| Player avatar | `Character_Male_1` | `assets/Characters/glTF/Character_Male_1.gltf` |
| Target (Yellow Chick) | `Chick` | `assets/Animals/glTF/Chick.gltf` |
| Distraction: Chicken | `Chicken` | `assets/Animals/glTF/Chicken.gltf` |
| Distraction: Pig | `Pig` | `assets/Animals/glTF/Pig.gltf` |
| Distraction: Sheep | `Sheep` | `assets/Animals/glTF/Sheep.gltf` |

### 3.2 Environment dressing
| Usage | Asset key | Path | Notes |
| --- | --- | --- | --- |
| Trees | `Tree_1`, `Tree_2`, `Tree_3` | `assets/Environment/glTF/Tree_*.gltf` | Random mix for variety |
| Bushes | `Bush` | `assets/Environment/glTF/Bush.gltf` | Collidable |
| Tall grass | `Grass_Big`, `Grass_Small` | `assets/Environment/glTF/Grass_*.gltf` | Non-colliding filler |
| Rocks | `Rock1`, `Rock2` | `assets/Environment/glTF/Rock*.gltf` | Collidable |
| Mushrooms | `Mushroom` | `assets/Environment/glTF/Mushroom.gltf` | Foreground parallax |
| Decorative flowers | `Flowers_1`, `Flowers_2` | `assets/Environment/glTF/Flowers_*.gltf` | Non-colliding |

### 3.3 Asset pipeline decisions
- Load `assets.json` via `fetch('../assets.json')`, filter needed keys, and create a `loadGltf(label, path)` helper using `GLTFLoader` (`three/addons/loaders/GLTFLoader.js`).
- After load, wrap each root in `makeAnchoredMesh(root, anchor = 'minY')` so ground contact is consistent.
- Build pooling for chicks/chickens/pigs/sheep to avoid reloading between rounds (clone scene graph per spawn).
- Fallback path (required by PRD but expected rare): if any GLTF fails, instantiate voxel primitives with the palette from PRD section 4.

## 4. Runtime Architecture
### 4.1 File layout (single HTML)
```
<body>
  <div id="hud">
    <div id="timer"></div>
    <div id="streak"></div>
    <div id="controls"></div>
    <div id="counterOverlay"> ... DOM counter ... </div>
    <div id="menu"></div>
    <canvas></canvas>
  </div>
  <script type="module">/* Three.js code */</script>
</body>
```

### 4.2 Module organization inside the script
- **Config constants:** sizes, colors, spawn counts, timings, camera numbers, DOM selectors.
- **State stores:**
  - `const gameState = { mode: 'loading', timer: 20, streak: 0, best: 0, submitted: false, currentCount: 0, actualChicks: 0 }`
  - `const world = { scene, camera, renderer, clock, mixerRegistry: [], npcControllers: [], colliders: [], assetCache: {} }`
- **Subsystem namespaces:**
  - `setupRenderer()`, `setupScene()`, `setupLights()`, `setupCamera()`
  - `initAssets()`
  - `createEnvironment()` (builds ground + occluders + background tree line)
  - `createPlayer()` and `updatePlayer(dt)`
  - `spawnNPCs()` / `updateNPCs(dt)`
  - `updateCamera(dt)` (edge pan logic)
  - `updateHud()` (DOM binding)
  - `runFX()` (UI pulses, confirmed sightings)
  - `handleStateTransition(nextMode)`

### 4.3 Game state diagram
`loading → menu → playing ↔ paused → results → (menu | playing)`
- Loading waits for GLTF/manifest fetch then calls `handleStateTransition('menu')`.
- Paused retains snapshot of timers and halts animations by skipping controller updates.

### 4.4 Data flow
1. `bootstrap()` loads manifest & GLTFs.
2. `setupScene()` builds static world + player placeholder.
3. `startRound()` spawns NPCs, resets timer/counter.
4. `setAnimationLoop(loop)` handles dt, updates, state gating.
5. DOM overlay updates mirror `gameState` each frame.

## 5. Rendering & Scene Composition
### 5.1 Reference-frame contract (per threejs-builder skill)
- Axes: +X right, +Y up, +Z toward camera. Gameplay uses X/Z plane.
- Camera: `PerspectiveCamera(45°, 960/540, 0.1, 200)` positioned at `(0, 11.5, 13)` looking at `(0, 0, 0)`; orbit disabled. Downward pitch ≈ 40°.
- Edge-pan: project player world position to NDC via `player.clone().project(camera)`; if x < -0.76 or x > 0.76 (≈12% screen), lerp camera target X.
- Calibration pass: On first load, attach `AxesHelper` + `ArrowHelper` to check GLTF facing; store `yawOffset` per asset (expected default is `-Z` forward, but we log to confirm).
- Units: Player height 1.6 units, ground plane extends `24 × 12` units.

### 5.2 Scene layers (front → back)
1. **Foreground parallax**: Non-collision mushrooms/grass near camera edges.
2. **Gameplay plane**: Ground tile plane, collidable trees/bushes/rocks, player, NPCs, confirmed-sighting particles.
3. **Backdrop**: Extra tree line (scaled/backed) + gradient sky plane (MeshBasicMaterial) + fog (`scene.fog = new THREE.FogExp2('#E9FFF2', 0.035)`).
4. **UI planes**: any in-world signage uses `MeshBasicMaterial`.

### 5.3 Lighting
- HemisphereLight (sky `#BFE8FF`, ground `#E9FFF2`, intensity 0.85).
- DirectionalLight at `(6, 12, 6)` with intensity 1.1, soft shadows (512-map). Optional low AmbientLight 0.15 for fill.
- Lights baked once; only intensity pulsing for urgency cues (timer low).

## 6. Core Subsystems
### 6.1 Asset Loading & Pooling
```js
const manifest = await fetch('../assets.json').then(r => r.json());
const ASSET_PATHS = {
  player: manifest.assets.characters.Male_1,
  chick: manifest.assets.animals.Chick,
  chicken: manifest.assets.animals.Chicken,
  pig: manifest.assets.animals.Pig,
  sheep: manifest.assets.animals.Sheep,
  trees: [manifest.assets.environment.flora.Tree_1, ...],
  bush: manifest.assets.environment.flora.Bush,
  rocks: [manifest.assets.environment.resources.Rock1, Rock2],
  grass: [manifest.assets.environment.flora.Grass_Big, Grass_Small],
  mushrooms: manifest.assets.environment.flora.Mushroom,
};
```
- `loadGltf(key)` caches the `GLTF.scene` root. For repeated use, `SkeletonUtils.clone()` if skinned; otherwise `scene.clone(true)`.
- Pools: maintain arrays of `npcPool.yellow`, `npcPool.chicken`, etc. Spawn by pulling from pool and enabling; return on round reset.

### 6.2 Input & Camera
- Input state object toggled by `keydown/keyup` listeners.
- Movement vectors derived from camera basis per skill instructions:
```js
const forward = new THREE.Vector3();
camera.getWorldDirection(forward);
forward.y = 0; forward.normalize();
const right = new THREE.Vector3().crossVectors(forward, UP); // ensures RH basis
```
- Edge-pan target `cameraRig.targetX`; actual camera position lerps toward target each frame with speed 6.5 units/sec.
- Pause/resume handled by event listeners gating updates.

### 6.3 Player Controller & Collision
- Player root is a `Group` containing GLTF plus floating UI anchor.
- Movement: acceleration/deceleration values per PRD table. Velocity clamped in `[-max, max]` each axis.
- Collision: maintain `colliders` array of AABBs. Proposed algorithm: attempt move per axis; for each collider, check overlap using `sweptAABB`. If collision, zero velocity along that axis and clamp position to collider edge ± clearance (0.12).
- Player may pass through NPCs (their colliders flagged `passThrough`).

### 6.4 NPC Controller
- `class Wanderer` holds reference to mesh, species config, `direction` vector, `speed`, `turnTimer`, `pauseTimer`, `sighted` flag.
- Behavior update pseudocode:
```js
turnTimer -= dt;
if (turnTimer <= 0) { pick random heading ± jitter; turnTimer = rand(minTurn, maxTurn); }
if (pauseTimer > 0) { pauseTimer -= dt; return; }
position.addScaledVector(direction, speed * dt);
wrap/clamp within bounds; if hitting collider, steer away by reflecting direction.
if (random < pauseChance) pauseTimer = rand(0.2, 0.5);
```
- Species config table (per PRD) defines `speedRange`, `turnRange`, `pauseRange`.
- Spawn counts: Yellow (6–14), White (3–10), Pigs (2–6), Sheep (2–6). Random seeds logged for reproducibility (use `Math.random()` with optional deterministic seed toggled).

### 6.5 Counting & Confirmed Sightings
- `gameState.currentCount` changed only by arrow keys, clamped 0–24. DOM overlay updates immediately and triggers CSS animation.
- Confirmed-sighting detection each frame for each yellow chick not yet `sighted`:
  1. Check planar distance `< 3.2`.
  2. Compute vector to chick, compare with player forward (dot ≥ cos 60° ≈ 0.5).
  3. Line-of-sight test: cast `Raycaster` from player eye height to chick; ensure no collider intersection before chick distance.
  4. If pass, mark `sighted = true`, emit particle burst (GPU instanced quads or Points), show floating text, slow global timeScale to 0.92 for 0.25s.

### 6.6 Timer, Submission, and Persistence
- Timer stored as float seconds; each loop `gameState.timer = Math.max(0, timer - dt * timeScale)`.
- Low-time cues triggered at 10s, 5s, 2s by toggling CSS classes on `#timer` and adjusting scene post-processing (color shift uniform).
- Submission: Space (or auto when timer hits 0). On submit, freeze movement, evaluate equality vs `gameState.actualChicks`, update streaks, store `best`, and show results overlay.

### 6.7 UI & DOM Overlay
- **Fixed HUD (DOM):**
  - `#counterOverlay`: central circle with number, up/down arrow buttons or key hints (“Press ↑/↓ to adjust”). Receives CSS `@keyframes pop` for changes.
  - `#timer`: top-center, large font with gradient background when urgent.
  - `#streak`: top-left small stack showing current/best.
  - `#controls`: top-right list (WASD, arrows, Space, Enter, P/Esc, Backspace).
  - `#menu` / `#results` overlays for states, toggled via CSS classes.
- DOM uses CSS variables for palette taken from PRD to keep consistent branding.
- `requestAnimationFrame` updates DOM through `updateHud()`; heavy operations (innerHTML) avoided.

### 6.8 Effects & Animation System
- Use a lightweight `FXTimeline` storing active tweens (counter pop, vignette, screen shake). Each entry has `duration`, `onUpdate`, `onComplete`.
- Confirmed sightings spawn GPU particles via `PointsMaterial` tinted `#FFD33D` with additive blending for 0.35s.
- Screen shake implemented by applying offsets to camera rig parent (lerped back).
- DOM overlays use CSS transitions (timer color/pulse, new best banner sliding).

### 6.9 Performance & Debug Hooks
- `renderer.info` logged at dev toggle to ensure draw calls < 120.
- Dev key `H` toggles helpers (AxesHelper, Bounding boxes) for verifying collisions.
- Stats: optional FPS counter hidden in production.

## 7. Game Flow & UI States
### 7.1 State specifics
- **Loading:** Show spinner overlay; background gradient. Once assets ready, transition to menu.
- **Menu:** Live scene at 35% speed; DOM overlay displays title, description, controls, best streak. Enter starts new round.
- **Playing:** Timer visible, DOM counter active, instructions pinned. Pause (P/Esc) overlays translucent layer.
- **Paused:** Freeze `timeScale` and skip updates; DOM overlay with resume controls.
- **Results:** Display actual vs submitted counts, difference, streak updates, instructions for Enter/Backspace.

### 7.2 Counter overlay behavior
- Always centered; number increments via arrow keys. Buttons for accessibility optional but present (click increments).
- Denied input (clamp) triggers CSS shake (translateX) and color flash (#B84A4A) for 120ms.

## 8. Data Structures & Algorithms
### 8.1 Configuration objects
```js
const SPECIES = {
  yellowChick: { speed: [2.2, 2.8], turn: [0.35, 0.9], pause: [0.2, 0.5], count: [6, 14], color: '#FFD33D' },
  chicken: { speed: [1.8, 2.2], turn: [0.7, 1.5], pause: [0.3, 0.7], count: [3, 10], color: '#F2F2F2' },
  pig: { speed: [1.5, 1.9], turn: [1.2, 2.0], pause: [0.6, 1.1], count: [2, 6], color: '#F3A0B4' },
  sheep: { speed: [1.6, 2.0], turn: [1.0, 1.8], pause: [0.4, 0.9], count: [2, 6], color: '#D9D9D9' },
};
```
- `const WORLD_BOUNDS = { x: [-12, 12], z: [-6, 6] }`.
- `const COLLIDER_SHRINK = 0.12`.

### 8.2 Main loop pseudocode
```js
const clock = new THREE.Clock();
renderer.setAnimationLoop(() => {
  const rawDt = clock.getDelta();
  const dt = rawDt * globalTimeScale;
  if (!state.paused && state.mode === 'playing') {
    updatePlayer(dt);
    updateNPCs(dt);
    updateCamera(dt);
    updateConfirmedSightings(dt);
    updateTimer(dt);
  }
  runFX(dt);
  updateHud();
  renderer.render(scene, camera);
});
```

### 8.3 Confirmed sighting check
```js
function checkSightings() {
  for (const chick of yellowChicks) {
    if (chick.meta.sighted) continue;
    if (!withinRange(player.position, chick.position, 3.2)) continue;
    if (!inViewCone(playerForward, player.position, chick.position, 0.5)) continue;
    if (isOccluded(playerEye, chick.position)) continue;
    markSighted(chick);
  }
}
```
- `isOccluded` uses `Raycaster` against `colliderMeshes`.

## 9. Risks & Mitigations
| Risk | Mitigation |
| --- | --- |
| GLTF scale/orientation mismatch | Run calibration pass per threejs-builder instructions; store `yawOffset` constants. |
| High draw calls due to many GLTF instances | Use instancing for repeated trees/bushes where possible; reuse materials. |
| Collision tunneling at high speeds | Movement speeds are low; still, move axis-by-axis with small dt. |
| DOM overlay desync with canvas | `updateHud` reads from `gameState` immediately after updates. Use CSS `pointer-events: none` for overlays except counter buttons. |
| Counters not readable on small screens | Layout scales using CSS clamp fonts; maintain 16:9 letterboxing by wrapping canvas in container that sets `width: min(100vw, 100vh*16/9)`. |
| Confirmed sighting raycasts expensive | Only evaluate for unsighted chicks (max 14) and reuse single `Raycaster` instance. |

## 10. Implementation Roadmap
1. **Bootstrap & reference frame:** stub `index.html`, renderer setup, gradient background, calibration helpers to verify units/orientation.
2. **Asset loader + manifest filter:** fetch `assets.json`, load required GLTFs, anchor them, build pools.
3. **Environment assembly:** ground plane, gradient sky, occluders, background tree line; register collider volumes.
4. **Player controller:** instantiate avatar, input handling, collision resolution, floating anchor for counter.
5. **NPC system:** config-driven spawner, wander steering, pooling.
6. **Camera rig & edge pan:** implement threshold logic, confirm large-screen letterboxing.
7. **HUD & DOM overlay:** central counter, timer, controls, state overlays; wire to state machine.
8. **Gameplay logic:** timer, submission, state transitions, streak persistence.
9. **Confirmed sighting FX + time pressure cues.**
10. **Polish & QA:** stress test spawn counts, confirm performance, finalize CSS + responsive layout.

## 11. Testing & Debug Checklist
- ✅ Asset load success and fallback log.
- ✅ Player collision edges (can’t exit bounds, can weave between trees).
- ✅ NPCs stay within bounds and avoid obstacles.
- ✅ Counter clamps & denies gracefully.
- ✅ Timer low-warning cues trigger at 10s/5s/2s.
- ✅ Confirmed sighting triggers once per chick and respects occlusion.
- ✅ Pause/resume freeze everything (movement, animations, timers).
- ✅ localStorage best streak persists across refresh.
- ✅ DOM overlays stay centered regardless of window size.

This TDD aligns with the PRD, references the available GLTF assets, and applies the threejs-builder skill guidance (reference-frame contract first, ES-module structure, asset calibration, camera-relative controls). Implementation can now proceed in `forest/index.html` following the roadmap above.
