# Open Rebellion — Rust/WASM reimplementation of Star Wars Rebellion (1998 4X), one dev + "multiple agentic harnesses" (Claude Code, Codex)

- Repo: https://github.com/tdimino/open-rebellion  (Ghidra RE docs site: https://tdimino.github.io/open-rebellion/)
- Stars: 10. 462 commits, 2026-03-12 → 2026-09-28. README footer: "Built by Tom di Mino and Claudius, Artifex Maximus [Claude Code]"; Codex co-authored commits; "Fable" workflows mentioned.
- Genre: galactic grand strategy 4X (200 systems, 15 sim systems, space+ground combat, missions, AI, mods), macroquad/egui, native macOS + browser WASM.
- Result evidence: 706 workspace tests + 84-case tactical browser gate passing (2026-09-18). BUT the project's own CLAUDE.md says "the project is not yet 100% functional. Do not repeat historical parity percentages as verified results." Honest partial — include as a harness case, not a finished-game case.
- Spec: again **ground truth artifacts** rather than prose — the original game's 51 DAT files (parsed with byte-level round-trip), 5,127 Ghidra-decompiled functions from REBEXE.EXE, 111 mapped GNPRTB parameters, original manual. Agent docs: game-domain.md, dat-formats.md, ghidra-re.md, main-menu-parity.md (acceptance matrix vs original screens).
- Notable process practices (some of the strictest in the set):
  - progress.json = live recovery record, read first; one audit feature at a time; commit+push after each passes gates; "Never mark a partial or inferred result complete."
  - Provenance enforcement: every sim rule carries a source tag (Ghidra `FUN_`, GNPRTB, DAT) or explicit `port:`/`hyp:` tag; `provenance-scan --check` must pass; "the baseline of uncited items may only shrink". Tests asserting original behavior must cite source.
  - `cargo mutants` on touched files before commit; close/explain each surviving mutant.
  - "Never delete, weaken, or broaden an assertion to make code pass"; "show the test fails without the change before calling it done"; regenerate goldens only for a named cause.
  - Visual claims: "Do not claim bitmap correctness from decode or HTTP success alone. Require a resource mapping, cache hit, and inspected screenshot on each claimed platform." Browser acceptance with retained screenshots/network/console logs/artifact hashes.
  - Deterministic replay gate across native and WASM; headless campaign runner crate (rebellion-playtest) with JSONL telemetry.
  - A dated full-functionality audit (docs/qa/2026-09-08-...) with evidence contract + definition of done supersedes earlier self-reported percentages — explicit correction of earlier agent over-claiming.

---
## Verbatim: CLAUDE.md
---
title: "Open Rebellion"
description: "Claude Code instructions for the Open Rebellion Rust reimplementation"
updated: 2026-09-08
---

# Open Rebellion

Open Rebellion is a Rust, macroquad, and egui reimplementation of Star Wars
Rebellion (1998). It runs natively and as WebAssembly/WebGL in the browser.

The September 2026 audit is the source of truth: the project is not yet 100%
functional. Do not repeat historical parity percentages as verified results.

## Current Workflow

- Read `progress.json` first. It is the ignored live recovery record; the older
  native-video record is `archive/progress.archived-2026-04-07-native-video.json`.
- Work one audit feature at a time and keep its JSON, Markdown, roadmap, and
  progress evidence synchronized.
- After a feature passes its required gates, commit and push it before starting
  the next feature. Never mark a partial or inferred result complete.
- Work directly on `main`; the repository intentionally carries no other local
  or origin branches during this audit.
- Run browser acceptance yourself with `agent-browser`, or through
  `codex-orchestrator` with Astra at medium effort. Either way, retain
  screenshots, network logs, console logs, and artifact hashes.
- v1.0 is the complete browser build deployed through password-protected
  Cloudflare Pages; credentials belong in encrypted secrets, never in Git.
- GitHub Actions workflow definitions are intentionally local and untracked as
  of 2026-09-08. Until M5 restores a reviewed provider, verification is manual.

## Commands

`~/.local/bin/cc` is not a C compiler. Use the sanitized PATH for Cargo:

```bash
env PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/Users/tomdimino/.cargo/bin cargo check --workspace
env PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/Users/tomdimino/.cargo/bin cargo test --workspace
env PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/Users/tomdimino/.cargo/bin cargo run -p rebellion-app -- data/base
./scripts/build-wasm.sh
./scripts/package-web.sh dev
```

Formatting and strict Clippy currently have audited baseline failures. Run
scoped checks for touched code and do not describe those workspace gates as
green until their dedicated findings close.

## Architecture

- `crates/rebellion-core` — headless runtime types and simulation; no rendering.
- `crates/rebellion-data` — DAT loading, seeding, and persistence.
- `crates/rebellion-render` — macroquad/egui rendering and interaction panels.
- `crates/rebellion-app` — native/WASM entry point and interactive loop.
- `crates/rebellion-playtest` — headless campaign runner and JSONL telemetry.
- `tools/dat-dumper` — DAT codecs and TEXTSTRA extraction.
- `web` and `scripts` — browser shell, WASM build, packaging, and asset staging.

## Invariants

- Keep binary-layout `dat` types separate from runtime `world` types.
- Preserve original `DatId` identity; never persist slotmap keys directly.
- Every DAT parser must round-trip the original bytes through `DatRecord`.
- Keep `rebellion-core` free of rendering and platform I/O dependencies.
- Route simulation mutations through ordered `GameEffect` values and the
  authoritative integrator; economy precedes manufacturing.
- Do not claim bitmap correctness from decode or HTTP success alone. Require a
  resource mapping, cache hit, and inspected screenshot on each claimed platform.
- Preserve user changes and unrelated untracked files. Do not stage broad paths.

## Testing

- Name each test as a behavior sentence, such as
  `pause_finishes_the_current_day_then_holds`.
- A test that asserts original-game behavior cites its source in a comment or
  constant: a Ghidra function, a resource ID, or a manual page. Tests of our
  own helpers and layout need no citation.
- Never delete, weaken, or broaden an assertion to make code pass. Change an
  expectation only with evidence that it was wrong.
- Regenerate replay goldens or fixtures only for a named cause, such as a save
  format change or recovered original behavior, and name it in the commit.
- When one change writes both code and its test, show the test fails without
  the change before calling it done.
- Before committing, run `cargo mutants` on the touched files and close or
  explain each surviving mutant. See `agent_docs/agent-tooling.md`.
- Before committing simulation code, run `cargo run -q -p provenance-scan --
  check`. New rules carry a source (`FUN_`, GNPRTB, DAT) or a `port:`/`hyp:`
  tag; the baseline of uncited items may only shrink.

## Git and Dependencies

- Use conventional, atomic commits and stage explicit files.
- Never run `gh auth setup-git` or switch the active `gh` account to fix a push.
  Git pushes use the macOS keychain and the repository-scoped credential user.
- Ask before adding production dependencies, changing architecture, or breaking
  save/data/network formats.
- Never commit original game data, generated bitmap packs, secrets, or tokens.

## Detailed Guides

- `docs/qa/2026-09-08-full-functionality-audit/index.md` — audit entry point,
  evidence contract, feature ledger, and definition of done. Read for all work.
- `agent_docs/roadmap.md` — active milestones and v1.0 release sequence. Read when
  choosing or checking off work.
- `agent_docs/architecture.md` — crate graph and data flow. Read before structural
  changes.
- `agent_docs/simulation.md` — tick order and system patterns. Read for game logic.
- `agent_docs/save-load.md` — save schema and migration notes. Read for persistence.
- `agent_docs/assets.md` — bitmap and HD pipeline. Read for visual asset work.
- `agent_docs/dat-formats.md` — binary formats and codec rules. Read for DAT work.
- `agent_docs/agent-tooling.md` — Codex, Fable, Ghidra, QA, asset, and deployment
  skill routing. Read before delegating or selecting a specialized workflow.


---
## Verbatim: AGENTS.md
# Open Rebellion

Open Rebellion is a Rust reimplementation of Star Wars Rebellion (1998), with
native macroquad/egui and browser WebAssembly/WebGL targets.

The September 2026 audit is authoritative. The project is not yet 100%
functional; historical parity percentages are estimates, not acceptance proof.

## Active Work

- Start with `progress.json`, the ignored live recovery record.
- Use `docs/qa/2026-09-08-full-functionality-audit/README.md` for the audit index,
  feature ledger, evidence contract, and definition of done.
- Use `agent_docs/roadmap.md` for milestone order, including the protected
  Cloudflare Pages v1.0 release.
- Use `agent_docs/agent-tooling.md` to select Codex, Fable, Ghidra, QA, asset,
  and deployment workflows without loading unrelated skills.
- Complete one feature at a time. Update progress JSON, audit JSON, audit
  Markdown, and roadmap evidence together.
- Once a feature passes its stated gates, commit and push it before starting the
  next feature. Never check off a partial or inferred result.
- Work directly on `main`; do not create or retain side branches unless the
  user explicitly changes the main-only policy.
- Use Astra only for live browser or computer-use acceptance through
  `codex-orchestrator`: low effort for routine checks, medium for complex or
  release-significant journeys. Do not assign Astra source, implementation,
  reverse-engineering, or documentation reviews. Retain its inspected
  screenshots, console/network logs, and artifact hashes.
- Use Codex Sol through `codex-orchestrator`, at high or extra-high effort,
  when risk warrants independent code, reverse-engineering, architecture,
  persistence/network, security, or documentation review. Routine, well-tested
  feature slices do not require a Sol review.
- Launch every Open Rebellion browser-test session with Chromium
  `--mute-audio`, and keep the in-game music control muted unless the test
  explicitly verifies audio. Close the test browser and local server when the
  run finishes.
- GitHub Actions workflow definitions are intentionally local and untracked as
  of 2026-09-08. Verification is manual until M5 restores a reviewed CI provider.

## Commands

`~/.local/bin/cc` shadows Apple clang. Use this sanitized PATH for Cargo:

```bash
env PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/Users/tomdimino/.cargo/bin cargo check --workspace
env PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/Users/tomdimino/.cargo/bin cargo test --workspace
env PATH=/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/Users/tomdimino/.cargo/bin cargo run -p rebellion-app -- data/base
./scripts/build-wasm.sh
./scripts/package-web.sh dev
```

Formatting and strict Clippy have known audited baseline failures. Run scoped
checks for touched code; do not report the workspace gates as green until their
dedicated findings close.

## Structure

- `crates/rebellion-core` — headless runtime types and simulation.
- `crates/rebellion-data` — DAT loading, seeding, and persistence.
- `crates/rebellion-render` — macroquad/egui rendering and interaction.
- `crates/rebellion-app` — native/WASM entry point and interactive loop.
- `crates/rebellion-playtest` — headless campaigns and JSONL telemetry.
- `tools/dat-dumper` — DAT codecs and TEXTSTRA extraction.
- `web` and `scripts` — browser shell, WASM builds, packaging, asset staging.
- `agent_docs` and `docs` — architecture, plans, mechanics, and QA evidence.

## Conventions

- Keep binary-layout `dat` types separate from runtime `world` types.
- Preserve original `DatId` identity; never persist slotmap keys directly.
- Require every DAT parser to round-trip original bytes through `DatRecord`.
- Keep `rebellion-core` free of rendering and platform I/O dependencies.
- Express simulation mutations as ordered `GameEffect` values applied by the
  authoritative integrator; economy runs before manufacturing.
- Prove bitmap display with a resource mapping, cache hit, and inspected runtime
  screenshot. Decode or HTTP success alone is insufficient.
- Keep password/session material in encrypted Cloudflare secrets. Never commit
  credentials, original game data, or generated proprietary asset packs.
- Follow the testing rules in `CLAUDE.md`: behavior-sentence test names, cited
  sources for original behavior, no weakened assertions, goldens regenerated
  only for a named cause, new tests shown to fail, and a scoped `cargo mutants`
  run before committing.

## Boundaries

- Always: Preserve unrelated user changes and stage explicit paths only.
- Always: Verify in proportion to risk and record exact commands/results.
- Always: Use conventional, atomic commit messages and push every verified item.
- Ask: Before adding production dependencies, changing architecture, or breaking
  save, DAT, or network formats.
- Never: Run `gh auth setup-git` or switch the active `gh` account to repair a
  push; use the macOS keychain and repository-scoped credential username.
- Never: Claim 100% functionality until every supported P00–P40 pass is green
  and all P0/P1 findings are closed with release-artifact evidence.

## Troubleshooting

- Linker invokes a Claude/tmux launcher: rerun Cargo with the sanitized PATH.
- Browser boots black: wait for the bitmap manifest and all staged assets, then
  inspect console/network logs before assigning a visual result.
- Push omits `main`: run `git push origin main` and compare `HEAD` with upstream.
- Pages/Jekyll reports a missing local path: inspect tracked symlinks; local
  scratch links must remain ignored.


---
## Verbatim: agent_docs/INDEX.md
---
title: "Agent Docs Index"
description: "Master index of AI agent reference documentation for Open Rebellion"
category: agent-docs
created: 2026-03-22
updated: 2026-03-22
tags: [index, agent-docs]
---

# Agent Docs Index

Reference documentation for AI agents working on the Open Rebellion codebase. Read `CLAUDE.md` at project root for which doc to load when.

## Architecture & Design

| Document | Description |
|----------|-------------|
| [architecture.md](architecture.md) | Crate graph, type system, entity identity, data flow, render architecture |
| [roadmap.md](roadmap.md) | Phase breakdown with status, addon plans, AI parity gaps |
| [simulation.md](simulation.md) | 15 simulation systems, advance() contract, integration order |
| [deterministic-replay.md](deterministic-replay.md) | Replay format, exact native/WASM artifact gate, DAT/config identity, checkpoints, and open engine-convergence work |
| [agent-tooling.md](agent-tooling.md) | Claude Code Minoan and Codex skill routing, including browser acceptance, Fable, and Ghidra |

## Game Knowledge

| Document | Description |
|----------|-------------|
| [game-domain.md](game-domain.md) | Galaxy, factions, units, missions, combat — game mechanics overview |
| [dat-formats.md](dat-formats.md) | DAT binary format reference, 3 structural patterns, 51 files |
| [ghidra-re.md](ghidra-re.md) | Ghidra RE summary: 5,207 decompiled functions, combat formulas, GNPRTB params |
| [main-menu-parity.md](main-menu-parity.md) | Original shuttle-cockpit geometry, resources, settings, actions, and browser acceptance matrix |

## Subsystems

| Document | Description |
|----------|-------------|
| [save-load.md](save-load.md) | Save format v4, migration, mod metadata hash |
| [mod-runtime.md](mod-runtime.md) | ModRuntime, ModConfig, enable/disable, hot reload |
| [modding.md](modding.md) | Mod loader: TOML manifest, RFC 7396, semver, load order |

## Assets & Media

| Document | Description |
|----------|-------------|
| [assets.md](assets.md) | 6 asset pipelines, 11 reference collections, 4 3D providers |
| [game-media.md](game-media.md) | 18 DLLs, Smacker videos, WAV soundtrack |
| [dll-resource-catalog.md](dll-resource-catalog.md) | 2,441 BMPs + 3,223 data files across 11 DLLs |

## Per-System Detail (systems/)

| Document | System |
|----------|--------|
| [systems/ai-parity-tracker.md](systems/ai-parity-tracker.md) | AI function-by-function parity mapping — 6/6 core pipeline DONE |
| [systems/combat.md](systems/combat.md) | Space + ground combat resolution |
| [systems/blockade.md](systems/blockade.md) | Fleet-presence blockade mechanics |
| [systems/uprising.md](systems/uprising.md) | Incite/subdue uprising |
| [systems/death-star.md](systems/death-star.md) | Construction, fire, planet destruction |
| [systems/research.md](systems/research.md) | 3 tech trees, skill-based progression |
| [systems/jedi.md](systems/jedi.md) | Force tier progression, detection |
| [systems/victory.md](systems/victory.md) | HQ capture, Death Star, terminal conditions |
| [systems/betrayal.md](systems/betrayal.md) | Loyalty-driven faction defection |


---
## Excerpt: agent_docs/game-domain.md (first 120 lines)
---
title: "Game Domain: Star Wars Rebellion"
description: "Game mechanics overview covering galaxy structure, factions, units, missions, and combat"
category: "agent-docs"
created: 2026-03-11
updated: 2026-03-16
tags: [reference, game-mechanics, factions, missions]
---

# Game Domain: Star Wars Rebellion

Star Wars Rebellion (1998, Coolhand/LucasArts) is a 4X galactic strategy game. Alliance vs Empire, controlling systems, building fleets, training characters, running missions.

## Galaxy Structure

- **Galaxy**: 200 star systems across 20 sectors
- **Sector**: Named region with `SectorGroup` (`Core`, `RimInner`, `RimOuter`). Contains multiple systems.
- **System**: Atomic unit of territory. X/Y position (range ~100-840), belongs to one sector. Holds facilities, ground units, orbiting fleets.
- **Popularity**: Each system has Alliance/Empire popularity (0.0-1.0). Shifts via diplomacy, occupation, events.

## Factions

Alliance and Empire only. Each has:
- Headquarters system (Alliance: variable start, Empire: Coruscant)
- Characters, fleets, manufacturing queues, tech tree
- Victory: capture enemy HQ (or destroy Death Star / find Rebel base)

## Characters

- **Major** (6 in base): Luke, Vader, etc. Fixed stats, unique abilities, plot events.
- **Minor** (54): Generic officers. Stats use base+variance: `final = base + rng(0..=variance)` at game start.
- **8 skill pairs**: diplomacy, espionage, ship_design, troop_training, facility_design, combat, leadership, loyalty
- **Jedi**: `jedi_probability` (0-100), `jedi_level` (base+variance). DAT layer also has `is_known_jedi`, `is_jedi_trainer` (not yet promoted to world model)
- **Roles**: `can_be_admiral` (fleet command), `can_be_commander` (missions), `can_be_general` (ground combat)
- **Loyalty**: `loyalty` skill pair + `is_unable_to_betray` flag (Luke, Vader cannot switch sides)

## Military Units

### Capital Ships (30 classes)
Class templates, not instances. Key fields:
- Weapons on 4 arcs (fore/aft/port/starboard) x 3 types (turbolaser/ion/laser)
- Hull, shields (strength + recharge), engines, maneuverability, hyperdrive
- Fighter capacity, troop capacity, tractor beam, gravity well projector
- Detection, bombardment modifier, damage control

### Fighters (8 classes)
Squadron-based (`squadron_size` craft per squadron). Torpedoes for bombing. Same weapon arc structure as capital ships.

### Troops (10 types)
Ground combat: attack_strength, defense_strength, bombardment_defense.

### Special Forces (9 types)
Mission specialists with character-like skill pairs + `mission_id` bitmask for eligible mission types.

## Facilities

Built on system surfaces. Three categories:
- **Defense** (6 types): planetary shields, turbolasers, ion cannons. bombardment_defense, attack_strength, shield_strength.
- **Manufacturing** (6 types): shipyards, training centers. processing_rate determines build speed.
- **Production** (2 types): mines, refineries. Same binary layout as manufacturing.

## Production System

- Every buildable entity has: `refined_material_cost`, `maintenance_cost`, `research_order`, `research_difficulty`
- `production_family` / `next_production_family` -- linked list through the tech tree
- Production facilities generate raw materials; manufacturing facilities convert them to units

## Game Balance Parameters

### GNPRTB (213 entries)
Master balance table. Each parameter has 8 values: Development, Alliance Easy/Med/Hard, Empire Easy/Med/Hard, Multiplayer. Controls travel time, combat recovery, mission rewards, diplomacy effects, events, economy, uprising mechanics, Jedi training. 29% documented, 71% unknown (Ghidra RE target).

### SDPRTB (35 entries)
Per-faction modifiers, same difficulty breakdown as GNPRTB.

## Seed Tables (9 files)
Starting unit/facility deployments for new games:
- CMUNAFTB/CMUNEFTB -- fleet seeds (Alliance/Empire)
- CMUNALTB/CMUNEMTB -- army seeds
- CMUNCRTB -- Empire Coruscant garrison
- CMUNHQTB/CMUNYVTB -- Alliance HQ and Yavin
- FACLCRTB/FACLHQTB -- starting facilities

## Implemented Systems

See `agent_docs/simulation.md` for full API reference on all 15 systems.

### Core Loop (v0.2.0)
- **Tick system** (`tick.rs`): Frame-independent GameClock, GameSpeed (Paused/Normal/Fast/Faster), TickEvent markers
- **Manufacturing** (`manufacturing.rs`): Per-system production queues with overflow propagation; blockade-aware (`advance_with_blockade`)
- **Events** (`events.rs`): Conditional triggers (TickReached, CharacterAtSystem, Random, EventFired), event chaining
- **AI** (`ai.rs`): Rule-based opponent — officer assignment, production priority, fleet deployment, espionage dispatch. Re-evaluates every 7 ticks.
- **Movement** (`movement.rs`): Fleet hyperspace transit with speed from slowest hyperdrive rating
- **Fog of war** (`fog.rs`): Per-faction monotonic visibility with advance intel at 50% transit
- **Mod loader** (`rebellion-data/src/mods.rs`): TOML manifests, RFC 7396 merge patch, semver, hot reload

### War Machine (v0.4.0)
- **9 mission types** (`missions.rs`): Diplomacy, Recruitment, Sabotage, Assassination, Espionage, Rescue, Abduction, InciteUprising, Autoscrap — MSTB probability tables with quadratic fallback
- **Space combat** (`combat.rs`): 7-phase pipeline (weapon fire → shield absorb → hull damage → fighter engage → result), CombatPhaseFlags, per-system 5-tick cooldown
- **Ground combat** (`combat.rs`): Troop-by-troop resolution with regiment_strength comparison
- **Orbital bombardment** (`bombardment.rs`): `damage = sqrt(delta²) / GNPRTB[0x1400]`, minimum 1
- **Blockade** (`blockade.rs`): Hostile fleet without defender halts manufacturing, destroys in-transit troops
- **Uprising** (`uprising.rs`): revolts start on a troop shortfall and never change control; an incident every 30-100 ticks maps its score through UPRIS1TB/UPRIS2TB step lookups to losses; natural disasters erode resources and facilities
- **Death Star** (`death_star.rs`): Construction countdown, superlaser fire (precondition checks from RE), nearby-warning scan
- **Research** (`research.rs`): 3 tech trees (Ship/Troop/Facility) per faction, `research_order` + `research_difficulty`
- **Jedi training** (`jedi.rs`): 4-tier Force progression (None→Aware→Training→Experienced), XP accumulation, detection checks
- **Victory conditions** (`victory.rs`): HQ capture, Death Star fire/destroyed, `resolved` flag prevents re-trigger
- **Save/load** (`rebellion-data/src/save.rs`): Bincode with OPENREB header, v4 format with mod metadata + FNV-1a hash, migration framework, 10 slots. See `agent_docs/save-load.md`.

### Full Parity (v0.5.0)
- **4 scripted story chains** (`story_events.rs`): Luke Dagobah (0x221→0x210), Final Battle (0x220), Bounty Hunters (0x212), Jabba's Palace (0x380-0x383)
- **Han Solo speed bonus** (`movement.rs`): `hyperdrive_modifier` on Character, consulted by `fleet_ticks_per_hop()`
- **Betrayal system** (`betrayal.rs`): loyalty threshold via UPRIS1TB, `is_unable_to_betray` immunity, 50-tick cooldown
- **Decoy system** (`missions.rs`): FDECOYTB consultation during mission resolution
- **Escape system** (`missions.rs`): ESCAPETB per-tick check for captive characters, `check_escapes()` in main loop
- **Mission state flags**: `on_mission`, `on_hidden_mission`, `on_mandatory_mission` tracked on Character; `dispatch_guarded()` prevents double-dispatch
- **6 new EventConditions** + **6 new EventActions** for story event mechanics
- **15 Ghidra RE event ID constants** (0x12c–0x370)

### Mod Workshop (v0.6.0)
