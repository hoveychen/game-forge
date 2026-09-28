# Archer Wars — Dota 2 custom game remake (10-player skillshot FFA), Claude Code, ~10 days

- Repo: https://github.com/carloslibardo/archer-wars  (companion method repo: https://github.com/carloslibardo/dota2-claude-playbook — playbook, template, GPU-VM testrig, long-form article)
- Stars: 3 (Sep 2026) — low star count, but the best-documented harness in this collection.
- Tool/model: Claude Code, with the "superpowers" plugin (brainstorm → spec → plan → implement, ledger in docs/superpowers/) and GitHub Spec Kit templates (.specify/).
- Genre: Dota 2 custom arena; 7 archer classes w/ 6-slot kits, 19-item shop, bot engine (4 difficulties), procedural map generator (Python, rewrites Valve vmap), Convex backend for progression, Panorama UI.
- Result evidence: README "Playable and end-to-end proven — bots run full FFA matches to 20 kills, and every class, skill, and item has been exercised on video." 274 commits / 10 days, 86 fix commits, 306 human prompts → 2,576 agent actions (author's measurements; commit hashes linked in docs/HISTORY.md). Steam Workshop release "upcoming" — not independently verified.
- One-shot vs multi-session: multi-session, many parallel worktrees; ~300 human prompts.
- Notable process practices (very rich):
  - First commit is a design spec + research captures; no code for 3 hours. Every feature thereafter: spec (docs/superpowers/specs) → plan (docs/superpowers/plans) → implementation.
  - A research dossier (docs/research/original-dossier.md, reconstructed from Wayback/YouTube/wiki/WC3 map data tables) is the *design source of truth*; balance numbers must trace to it or be tagged DESIGN-FRESH. "The research wins its first argument ... The dossier won, and kept winning."
  - Tests + CI gate before first gameplay feature; playable core loop in 3 hours.
  - "Architecture invariants (violating these caused real crashes)" section in CLAUDE.md — written from incidents (hero-spawn crisis).
  - Self-playtesting via bots: headless e2e smoke on a Windows GPU VM — bots play FFA to win, console scanned for script errors + `[E2E]` win marker.
  - Publish quality gate: harness buys every item, casts every ability, asserts visible effect, films it; frames extracted as evidence. Standard: "prove it, don't claim it"; "a passing test was never enough". Gate itself needed 9 fixes "to stop it lying in both directions".
  - Human playtest rounds (R3, R9, R10, R11 feedback batch plans) found "three entire subsystems ... never worked" and bots "issuing 39 orders per second while firing nothing" — i.e. unit tests + agent confidence were insufficient; human/visual play loop mattered.
  - Decision records (docs/decisions/, .shippit/decisions/).
  - Big lesson: on a closed engine, main failure mode is hallucinated APIs failing silently ("invented-API tax").

---
## Verbatim: CLAUDE.md
# CLAUDE.md — Archer Wars

Dota 2 custom game remake of "Archer Wars" (original Workshop item `358561265`,
removed by moderation — this is a fresh rebuild). Skillshot-only 10-player FFA,
4 archer classes, 20 kills to win. TypeScript → Lua via TypeScriptToLua.

## Commands

```bash
bun install        # deps + postinstall symlinks game/ + content/ into dota_addons/
bun run build      # TS→Lua (tstl) + panorama (tsc). run-p build:*
bun run dev        # both compilers in --watch
bun run test       # vitest, pure-logic unit tests (run on Mac, no Dota needed)
bun run launch     # start Dota 2 with -tools -addon archer_wars (needs Dota installed)
```

CI (`.github/workflows/ci.yml`) runs typecheck + build + vitest on every push/PR.

## Where code lives

| Path | What |
|------|------|
| `src/vscripts/` | Game logic TS → compiles to `game/scripts/vscripts/*.lua` |
| `src/vscripts/bots/` | Bot engine: perception → agent FSM → kit advisors → executor |
| `src/vscripts/systems/` | Match systems (class select, shop zone, e2e/fill bots, difficulty chat, progression) |
| `src/vscripts/lib/` | Pure helpers (unit-testable; tests in `lib/__tests__/`) |
| `src/panorama/` | UI TS → compiles to `content/panorama/scripts/custom_game/` |
| `game/`, `content/` | Dota addon dirs (KV files, maps). Compiled Lua/JS here is **gitignored** |
| `mapgen/` | Python vmap transformer (radial FFA spawn ring + arena terrain/water painting) |
| `scripts/` | install/launch/publish + GCP VM control (`vm.sh`, `vm-smoke.ps1`) |
| `infra/` | Windows VM startup provisioning |
| `docs/superpowers/` | SDD ledger: design specs + implementation plans per feature |
| `docs/research/` | Recovered dossier of the original 2015 game (design source of truth) |
| `docs/PUBLISHING.md` | Steam Workshop publish runbook + automation ceiling |

## Architecture invariants (violating these caused real crashes)

- **Archers ARE base heroes overridden in place** (OAA pattern): Windrunner=Assault,
  Mirana=Sniper, Drow=Shadow, Clinkz=Demolitionist; tier-locked Hoodwink/Medusa/Sniper.
  `GetUnitName()` returns the BASE name — old `npc_dota_hero_*_custom` names never
  spawn. Any hero-keyed dispatch (e.g. `bots/kits/kitAdvisor.ts`) must key base names.
- **Seat bots with `dota_create_fake_clients`, never `dota_bot_populate`** — populate
  hard-crashes the tools client in this laneless FFA map (no traceback, process dies).
- **Resolve bot heroes via `lib/heroResolve.ts` `heroForPlayer()`**, not
  `PlayerResource.GetSelectedHeroEntity` — fake clients get heroes ASSIGNED
  (`CreateHeroForPlayer`), not selected, so SelectedHeroEntity is nil for them.
- Skillshot-only: heroes have ~0 right-click damage; all damage flows through
  abilities → `lib/arrowHitPipeline.ts` (ults deliberately bypass it).
- Bots are convar-driven: `archer_wars_fill_bots` (auto-fill, default 1),
  `archer_wars_bot_difficulty` (0–3), `archer_wars_e2e` (headless smoke mode).
  Host can type `-difficulty easy|medium|hard|unfair` in all-chat pre-horn.

## Testing strategy

1. **Unit (Mac, fast)**: vitest over pure logic — `bun run test`. Keep game-API-free
   logic in `lib/` / pure kit advisors so it stays testable here.
2. **Headless e2e smoke (Windows GPU VM)**: `scripts/vm-smoke.ps1` — compiles
   resources, launches Dota in tools mode with `archer_wars_e2e 1`, bots play FFA,
   scans console.log for script errors + `[E2E]` win marker. Must run in the VM's
   interactive session (scheduled task), not over SSH. VM control: `scripts/vm.sh
   {start|stop|tunnel|ssh}` (GCP `archer-wars-dev`, project `<gcp-project-id>`).
3. **Manual playtest**: `bun run launch` on any machine with Dota 2 installed.

The VM is only needed for step 2 (and for Workshop publish tooling). Local build
and local play need only Dota 2 + Workshop Tools on the machine you play on.

## Conventions

- Bun is the package manager/runner. Strict TypeScript. English everywhere.
- Compiled artifacts (`game/scripts/vscripts/**/*.lua`, panorama JS) are build
  outputs — never commit them; never edit Lua directly.
- Features follow SDD: design spec in `docs/superpowers/specs/`, plan in
  `docs/superpowers/plans/`, then implementation. Balance numbers trace to the
  research dossier (`docs/research/original-dossier.md`) or are tagged DESIGN-FRESH.
- TSTL truthiness warnings ("Only false and nil evaluate to 'false'") in
  scout_bird/archer_ward/burning_arrow are known and benign.


---
## Verbatim: docs/superpowers/specs/2026-07-04-archer-wars-remake-design.md (the original design spec, first commit)
# Archer Wars Remake — Design Spec

**Date:** 2026-07-04
**Status:** Approved by Carlos (brainstorming session, 2026-07-04)
**Target:** Full-parity reimplementation of the removed Dota 2 custom game "Archer Wars" (Viggzta + Druffe, Workshop ID 358561265) as a new Dota 2 Source 2 custom game.

## Decisions (locked)

| Decision | Choice |
|---|---|
| Platform | Dota 2 custom game (Source 2 Workshop Tools) |
| Scope | Full clone — feature parity with the original in v1 |
| Code architecture | TypeScriptToLua (ModDota `dota-ts-addon-template`), TSX Panorama UI |
| Dev/test environment | Cloud Windows VM with GPU (GCP, Windows Server 2022 + NVIDIA L4) |
| Repo | `~/carlos/projects/archer-wars`, GitHub under `carloslibardo` |

## 1. Game specification

Sources: Fandom wiki (dota2customgame.fandom.com/wiki/Archer_Wars), Wayback snapshot of the Workshop page (2016), Workshop comments. Raw captures in `docs/research/`.

- **Mode:** Free-for-all, 10 players, first to 20 kills wins. A second, smaller 5-player map exists for parity ("multiple maps" — a "forest oasis" variant and a "5 player map" are referenced in comments).
- **Combat:** Skillshot linear-projectile arrows only; no right-click auto-attack damage. Fast, instakill-leaning time-to-kill.
- **Archer classes:** **4 selectable archers** — corrected from the recovered public mirror of the Jun-2015 source (`rmwxiong/Dota-2-Archer-Wars`), which supersedes the earlier "5" estimate: **Assault** (Windrunner), **Sniper** (Mirana), **Shadow** (Drow Ranger), **Demolitionist** (Clinkz). All 480 hp / 100 mana / 290 ms, right-click ≈0 dmg (skillshot-only). Shared kit: Fade (dodge), Locate (reveal-all radar pulse), Holy Arrow/Comet (all but Shadow). The WC3 predecessor "Archer Wars: Legacy" (by cleeezzz) had 6 richer classes and serves as lineage reference. Final post-2016 roster count is DESIGN-FRESH (source is only a 4-month snapshot).
- **Ability progression:** base arrow (Q) → learnable/upgradable second arrow type → cloaked scout bird (map vision tool) → flaming boulder (powerful ult).
- **Innate radar:** every ~10 s cooldown, briefly (~1–2 s) reveals the location of all players. Anti-hide-and-seek mechanic.
- **Economy:** gold from kills; **no gold loss on death**; passive catch-up XP for trailing players (comeback design).
- **Shop:** physical zone at map center, always visible and exposed — deliberate ambush bait. **19 custom items**: wards, special arrow upgrades (e.g., reinforced bow), boots, etc. Exact list is a data gap (§2).

## 2. Data gaps and Phase 0 deep-scrape

The original is removed from the Workshop. Remaining public sources, to be scraped autonomously at the start of implementation:

1. Wayback Machine: Workshop **changelog** page + all snapshots 2015–2018 (patch notes name items/archers/maps).
2. Workshop **discussions** (3 threads existed) via Wayback.
3. YouTube gameplay videos ("Archer Wars dota 2") — HUD, shop layout, item names, archer kits.
4. WC3 `Archer Wars: Legacy` `.w3x` (epicwar.com map 132484) — extract triggers/object data (w3x2lni or MPQ tools) as design reference for classes/items.
5. Output: `docs/research/original-dossier.md` — everything recoverable, organized by system.

**Gap rule:** anything still unknown after the sweep is designed fresh, keeping the original's counts and roles (5 archers, 19 items, 2 maps). This is a clean-room reimplementation of mechanics, not a copy of code/assets.

## 3. Repository and code architecture

Scaffold from ModDota `dota-ts-addon-template`:

```
archer-wars/
├── src/vscripts/           # TypeScript → Lua (game logic)
│   ├── gamemode.ts         # GameRules state machine: setup → hero pick → live → win at 20
│   ├── systems/            # killTracker, respawn, radarPulse, comebackXp, shopZone
│   ├── abilities/          # arrow projectiles, scout bird, flaming boulder (logic side)
│   └── lib/                # timers, projectile helpers, netTable helpers
├── src/panorama/           # TSX Panorama UI: kill counter/leaderboard, HUD, end screen
├── game/dota_addons/archer_wars/scripts/npc/
│   ├── npc_abilities_custom.txt   # KV ability definitions
│   ├── npc_items_custom.txt       # 19 items
│   └── npc_heroes_custom.txt      # 5 archers (reskinned Dota hero bases)
├── content/dota_addons/archer_wars/maps/   # Hammer map sources (VM-side)
├── scripts/                # sync-to-vm.ps1, smoke-test, vm-start/stop
└── docs/                   # research dossier, specs, plans
```

Principles:

- **Typecheck + tstl build is the primary local verification gate.** The agent iterates on Mac/CI without a VM round-trip; runtime testing is the second gate.
- Pure-logic modules (score math, comeback XP curve, radar timing) are engine-independent and unit-tested with vitest on Mac.
- Abilities/items defined declaratively in KV where possible; TS logic only where KV can't express behavior.
- Archers are built on existing Dota hero bases (e.g., Drow Ranger, Windrunner models) with custom kits — no custom model work in v1.

## 4. Windows VM pipeline

- GCP Windows Server 2022 + NVIDIA L4 GPU (~$1/hr while running), region us-central1. Steam + Dota 2 + Dota 2 Workshop Tools installed once (Steam Guard needs Carlos once).
- `scripts/sync-vm.ps1`: push addon files → `dota_addons/archer_wars`, run resourcecompiler, launch `dota2.exe -tools -addon archer_wars`.
- **Smoke test loop:** autoexec cfg launches the map with bot players, executes scripted console commands, dumps the console log; log syncs back and the agent parses it for script errors. This is the closest available approximation to autonomous playtesting.
- Interactive playtests: Carlos joins a hosted lobby from his Mac Dota client, or Parsec/RDP into the VM.
- Cost guard: auto-stop the VM on idle.

## 5. Build phases (end-to-end)

| # | Phase | Verification |
|---|-------|--------------|
| 0 | Deep-scrape → `original-dossier.md` | dossier committed |
| 1 | Scaffold TSTL repo, CI (typecheck + build) | green build |
| 2 | VM provision + tools + sync/smoke pipeline | smoke log round-trip works |
| 3 | Core loop: spawn, arrow skillshot, kill→score, respawn, win at 20 (blockout map) | smoke + manual |
| 4 | 5 archers + ability progression (arrow 2, bird, boulder, radar) | per-archer smoke |
| 5 | 19 items + center shop zone | buy/effect smoke |
| 6 | Comeback XP + polish (Dota VFX/sounds) | manual |
| 7 | Maps: 10-player arena + 5-player small map (Hammer blockout → art pass) | compile + perf check |
| 8 | Panorama UI full pass (killboard, HUD, end screen) | manual |
| 9 | Balance pass: bot lobbies + Carlos playtests | playtest sign-off |
| 10 | Workshop publish (Carlos's Steam auth required) | live Workshop page |

## 6. Error handling

- All event handlers pcall-wrapped with safe defaults; a script error must never hard-crash the lobby.
- Console logs are the debugging surface; the sync pipeline always retrieves them.
- Projectile/kill edge cases: simultaneous kills resolve by event order; kill 20 triggers immediate game-end state, further kills ignored.

## 7. Risks

| Risk | Mitigation |
|---|---|
| VM + Steam + GPU driver setup friction | One-time interactive setup session with Carlos; document as runbook |
| TSTL transpile quirks | Mature ModDota tooling; known workarounds; typecheck gate catches most |
| Original balance values unrecoverable | Own balance via Phase 9 playtests |
| Workshop name collision / takedown concern | New title allowed ("Archer Wars Remake" or fresh name decided at publish); mechanics are not copyrightable; no original code/assets used |

## 8. Legal posture

Clean-room reimplementation of game mechanics — mechanics/ideas are not copyright-protected. No code, scripts, or custom assets from the removed original are copied. Valve Dota 2 assets are used only inside Dota 2, per Workshop Tools terms. Optional courtesy email to the original authors (d2archerwars@gmail.com).


---
## Verbatim: docs/superpowers/specs/2026-07-08-publish-quality-gate-design.md
# Publish Quality Gate — Design

**Date:** 2026-07-08
**Status:** Approved-pending-review (Carlos requested full plan before any execution)
**Driver:** Carlos wants to publish the game. Two rounds of playtest bugs ("W/R don't pull", "ice bow does nothing") passed the existing smoke because it only verifies *cast released* (cooldown started), never the *effect*. Passive shop items are never exercised at all, and no item is ever bought through the real shop flow.

## Goal

One command runs a full automated certification on the Windows VM:
**every class × every ability verified at effect level, every shop item bought through the real shop and verified at effect level, plus a full bot match — all screen-recorded — producing a single PASS/FAIL report.** Publish requires the gate green.

## Evidence: why the current smoke is insufficient

| Escaped bug | Why smoke passed |
|---|---|
| W/R grapple: no pull, no chain (reported broken twice) | `SkillsExercise.verify()` checks only `GetCooldownTimeRemaining() > 0` — the cast released, the *effect* failed |
| Jötnar's Warbow: no cold visual/damage/slow | Passive items are not in `ACTIVE_ITEMS`; never exercised anywhere |
| Any shop/gold regression | Items granted via `AddItemByName`, real `archer_wars_shop_buy_request` path untested end-to-end |

## Scope

1. **Phase A — Ability effect sweep.** One bot per class (all 7, tier gates bypassed — existing `e2eBots` + `ClassSelect` path). Every ability cast in isolation (existing `SkillsExercise` cadence), but each cast now also runs an **effect assertion** from a registry: damage landed, target displaced, modifier applied, unit spawned — per-ability ground truth.
2. **Phase B — Item sweep (buy + effect).** For every entry in the shop catalog (`src/vscripts/lib/itemCatalog.ts` is the source of truth):
   - **Buy check:** teleport the bot into `ShopZone`, grant exact gold, fire the real `archer_wars_shop_buy_request` event, assert gold spent AND item in inventory (covers the 2026-07-06 "buy Ward, nothing appears" class of bug).
   - **Effect check:** actives → cast + effect assertion; passives → fire arrows at a victim until the expected proc/stat shows (attempt cap derived from KV `proc_chance`; 100%-proc items need 1 arrow); stat items (boots, reinforced bow) → assert stat delta after grant.
   - **Coverage is enforced:** a catalog item with no assertion entry is itself a FAIL — the gate can't silently under-cover as the shop grows.
3. **Phase C — Match regression.** Existing bounded e2e bot match (kills → score → win) runs after the sweeps; win screen reached = PASS.
4. **Recording + report.** ffmpeg desktop capture for the whole run (existing pattern). Harness prints `[QGATE] MARK <phase>/<subject> t=<GameTime>` lines; the runner converts them into a chapter index next to the mp4 so any FAIL maps to a video timestamp. Runner writes `aw-qgate-result.txt` with per-check verdicts + summary and exits non-zero on any FAIL or script error.
5. **Fix loop.** Run gate → each FAIL gets root-cause fix (systematic-debugging) → rerun → repeat until green. Seeded known-reds: **W/R grapple pull** and **ice bow frost proc** (both reported broken on retail macOS after confirmed fresh-lua load — they are real bugs, and Phase A/B assertions must reproduce them or the assertions are wrong).

## Non-goals

- Retail-client automation (Steam retail can't be driven headlessly; tools mode only).
- Tooltip/HUD pixel checks (covered by existing `vm-smoke-skills.ps1` hover sweep).
- Balance/tuning judgments — the gate checks "works", not "feels good".
- Mac-native automation. **Known limitation:** the gate runs the Windows tools-mode client. The earlier motion-controller bug was retail-macOS-specific; logic-level assertions (displacement measured server-side) still catch that class, but purely client-side rendering differences on macOS remain a short manual checklist (last section).

## Architecture

New `src/vscripts/systems/qualityGate/` module, engaged by tools-only convar `archer_wars_e2e_quality 1` (composes with existing `archer_wars_e2e 1`):

- `effectChecks.ts` — pure-ish registry: per ability/item name, `snapshot(ctx)` before cast and `assert(ctx, snap)` at verify time. Unit-testable shapes (thresholds, attempt-cap math) in plain functions.
- `qualityGate.ts` — orchestrator: reuses `SkillsExercise`'s cast/verify timer cadence but replaces the cooldown-only verify with cooldown check **AND** effect assertion; then runs the item buy+effect sweep; then hands off to the normal e2e match loop. Emits `[QGATE]` verdict + MARK lines.
- `scripts/vm-qgate.ps1` — VM runner: resourcecompile → ffmpeg record → launch tools mode with `+archer_wars_e2e 1 +archer_wars_e2e_quality 1` → wait → parse console.log into `aw-qgate-result.txt` + `aw-qgate-chapters.txt` → nonzero exit on FAIL.
- `scripts/vm.sh qgate` — Mac-side: start VM if stopped, sync repo, trigger the `aw_qgate` scheduled task (Interactive principal — same session-1 requirement as existing smokes), poll for completion, scp back mp4 + result + chapters + console.log, print summary, stop VM.

### Effect assertion ground truths (Phase A)

| Ability | Assertion (server-side, at verify) |
|---|---|
| archer_arrow / spread_shot / sniper_shot / explosive_arrow (+ variants) | victim HP dropped since snapshot |
| archer_hook / archer_grapple_volley | victim displaced ≥ 250u toward caster since snapshot AND (`modifier_grapple_pull` active OR `modifier_grapple_stun` seen) |
| archer_holy_arrow / archer_detonate | victim HP dropped |
| archer_fade | caster has `modifier_archer_fade` |
| archer_scout_bird | a controllable `npc_archer_scout_bird` owned by caster exists |
| archer_locate | cooldown-only (vision not cheaply assertable) — explicitly tiered as "cast-verified" in the report |

### Item assertions (Phase B, keyed off itemCatalog)

- Actives (ward, swap/sacrificial/burst/pull/vision gems): cast + per-item effect (ward unit exists; pull gem = displacement; burst = HP drop; swap = positions exchanged; vision/sacrificial = cast-verified tier).
- Elemental bows (phoenix/jotnar/raiju/elemental): fire arrows until `modifier_burning_arrow` / `modifier_frost_arrow` (+ HP drop from frost_damage) / `modifier_lightning_arrow` appears; cap = ceil(ln(0.001)/ln(1−proc/100)) attempts.
- Stat passives (reinforced bow, boots family, eagle eye, welling/elven/enchanted boots): stat delta (ideal speed, damage on next arrow, vision) after grant.
- Counter passives (dual arrows, astral compass): fire `hits_needed` arrows, assert extra damage instance / mana gain.
- Sustain passives (lifesteal mask, mana siphon, marksman's luck tiers): sampled — fire N arrows, assert heal event / mana steal / ≥1 crit-sized hit within cap.
- Recipe-only entries (native-shop recipes): buy-path exempt (native flow), effect covered via the final item.

## Gate criteria (publish checklist)

1. `npx tstl --project src/vscripts/tsconfig.json` exit 0; vitest suite green (local — allowed class).
2. VM quality gate: **0 script errors, 0 FAILs** across Phase A (7 classes × full kit), Phase B (full catalog), Phase C (win reached).
3. Video artifacts reviewed once per release candidate (chapters make this minutes, not an hour).
4. Manual Mac sanity pass (15 min, checklist in PUBLISHING.md): launch, pick each of 2–3 classes, one grapple, one ice-bow arrow, one item buy, one full round — catches macOS-client-only rendering issues the VM can't.

## Risks

- **Tools-mode vs retail divergence** — mitigated by server-side logic assertions + manual Mac pass; accepted residual.
- **Flaky sampled assertions (crit/lifesteal)** — caps sized for <0.1% false-fail; retries allowed once per sampled check.
- **Runtime** — ~13 abilities × 7 classes ≈ 50 casts (existing) + ~25 items × (buy + effect ≤ 30 arrows) — bounded to ~15 min wall; runner window sized accordingly.


---
## Verbatim: BUILD-TODO.md
# BUILD-TODO — verification steps NOT run on the scaffolding machine

This branch (`scaffold-code`) was assembled without running any installs or
builds (per repo rule: no local Mac builds). Everything below must be run on
remote infra (coder VM or GitHub Actions CI) before this is trusted to be
correct.

## 1. First-time bootstrap (required before CI's `--frozen-lockfile` will work)

The ModDota template ships an **npm** `package-lock.json`; this scaffold
deleted it because the project uses `bun` (per repo convention) and the
`package.json` `name` field changed (`"" → "archer_wars"`, plus a new
`vitest` devDependency was added). There is **no committed bun lockfile
yet**. `.github/workflows/ci.yml` runs `bun install --frozen-lockfile`,
which will fail on the very first run with no lockfile present.

Run once, then commit the generated lockfile:

```bash
cd archer-wars
bun install                 # generates bun.lock (or bun.lockb)
git add bun.lock             # or bun.lockb, whichever bun emits
git commit -m "chore: commit bun lockfile"
git push
```

After that, CI's `--frozen-lockfile` step will succeed on subsequent pushes
(as long as `package.json` and the lockfile are edited together going
forward).

## 2. Full verification sequence (mirrors `.github/workflows/ci.yml`)

```bash
bun install --frozen-lockfile        # after step 1 above
bunx tsc --noEmit -p src/vscripts/tsconfig.json
bunx tsc --noEmit -p src/panorama/tsconfig.json
bun run build                        # runs both build:panorama + build:vscripts (tstl)
bunx vitest run --passWithNoTests
```

Expected:
- `tsc --noEmit` clean on both projects.
- `bun run build` emits `.lua` files under `game/scripts/vscripts/**` and
  compiled JS under `content/panorama/scripts/custom_game/**`.
- `vitest run` → 4 passing tests in `src/vscripts/lib/__tests__/score.test.ts`.

## 3. Specific things to double-check on first real build

- **`postinstall` addon linking is a no-op here.** `scripts/install.js`
  only symlinks `game/` and `content/` into a real Steam/Dota install if
  one is found (`@moddota/find-steam-app`). On a Mac/Linux CI runner with
  no Dota installed, `postinstall` will just print "No Dota 2 installation
  found. Addon linking is skipped." and do nothing — this is expected and
  fine for typecheck/build/test purposes. Real in-game verification only
  happens on the Windows GPU VM (Plan Tasks 8-10, out of this branch's
  scope).
- **Addon name comes from `package.json`'s `name` field** (`scripts/utils.js:getAddonName()`),
  not from any directory literally named `dota_addons/archer_wars` in this
  repo. It is now set to `"archer_wars"`. Do not rename the `game/`/`content/`
  top-level folders — the template's own tooling relocates them into
  `<dota>/game/dota_addons/archer_wars` and `<dota>/content/dota_addons/archer_wars`
  only at `postinstall` time, on a machine where Dota 2 is actually installed.
- **Verify `@moddota/dota-lua-types` actually exports these exact global
  names** used in `src/vscripts/GameMode.ts` and
  `src/vscripts/abilities/archer_arrow.ts` — I could not run `tsc` to
  confirm: `DotaTeam.CUSTOM_1`..`CUSTOM_8`, `EntityKilledEvent`,
  `GameRules.SetGoldTickTime`, `GameRules.SetDaynightCycleDisabled`,
  `GameRules.GetGameModeEntity().SetCustomGameForceHero`,
  `.SetFixedRespawnTime`, `.SetAnnouncerDisabled`, `.SetBuybackEnabled`,
  `UnitTargetTeam.ENEMY`/`UnitTargetType.HERO`, `DamageTypes.PURE`,
  `ApplyDamage`, `ProjectileManager.CreateLinearProjectile`. These names
  were taken from the plan verbatim and cross-checked against the
  template's own `earthbind_ts_example.ts`, but the plan itself flags that
  the types package is the source of truth — if `tsc` flags any of them,
  fix to the typed name (do not silently `as any` past it).
- **`CustomNetTables.SetTableValue("archer_wars_score", ...)` typing.**
  This scaffold took the plan's "escape hatch" option: declared
  `interface CustomNetTableDeclarations { archer_wars_score: Record<string, { kills: number }> }`
  in `src/vscripts/types.d.ts` instead of using `as never` casts at the
  call site. Confirm `@moddota/dota-lua-types`'s `CustomNetTables` type
  actually keys off a global `CustomNetTableDeclarations` interface with
  this shape (checked against the pattern the plan describes; not
  verified by an actual compile).

## 4. Deviation flagged for a bug in the plan text (already fixed here)

Plan Task 7's code snippet sets `const FORCED_HERO = "npc_dota_hero_drow_ranger";`
— the **vanilla** hero name. But Task 6's KV override creates a **new**
hero entry named `npc_dota_hero_drow_ranger_custom` (via
`"override_hero" "npc_dota_hero_drow_ranger"` inside
`"npc_dota_hero_drow_ranger_custom" { ... }"`), which is what actually
carries the `archer_arrow` ability + the 1/1 attack damage override. If
`GameMode.ts` forces the vanilla hero name, players would spawn as a
stock Drow Ranger with her real kit and real attack damage — the whole
skillshot-only core loop would silently not apply.

This scaffold sets `FORCED_HERO = "npc_dota_hero_drow_ranger_custom"`
(matching the KV override key) instead of copying the plan's literal
string. **Verify this is indeed the correct hero name to force** once
`bun run build` + an actual VM boot (Plan Tasks 8-10) can confirm it,
since this could not be tested here.

## 5. Things intentionally out of scope for this branch

Tasks 1, 2, 8, 9, 10 from the plan were not touched:
- `docs/research/` — owned by another agent, not touched.
- Windows GPU VM provisioning / sync-vm / smoke-test pipeline / blockout
  map — separate plan tasks, need the interactive Steam/Dota install
  checkpoint the plan calls out.


---
## Excerpt: docs/HISTORY.md (first 160 lines)
# How Archer Wars Got Built

Archer Wars is a Dota 2 custom game — a remake of a 2015 Workshop map that was pulled by
moderation and never came back. This document is the story of rebuilding it, told from the
one source that can't be edited after the fact: the commit log.

The whole thing took **274 commits over ten days**, from 2026-07-04 to 2026-07-13. What
follows is the shape of those ten days, twenty commits worth reading, the numbers, and a
note about why this history was left exactly as it happened.

Every number below is measured over that ten-day window and is not restated as `main` moves.
Work has continued since — the elemental-visuals follow-ups, a CI determinism fix, an
adversarial-review batch and the arrow-launch refactors — and it is called out where it
changes the story rather than folded into the counts.

Every commit hash below links to GitHub. You can check any claim here yourself.

---

## The ten days

| Phase | Dates | Commits | What happened |
|-------|-------|---------|---------------|
| **1. Bootstrap and research** | Jul 4, 11:29–14:51 | ~14 | A design spec, then a plan, then the code. A research dossier — reconstructed from Wayback captures and YouTube footage of the deleted original — lands the same afternoon and immediately starts overruling guesses. |
| **2. Content build-out** | Jul 4, 15:43–17:05 | ~23 | Four archer kits, a 19-item shop, modifiers, comeback economy, a Panorama HUD. Then five straight fix commits, because a lot of that code called Dota APIs that don't exist. |
| **3. Test harness and class select** | Jul 4, 23:16 – Jul 5, 02:21 | ~10 | A headless bot harness so matches can run without a human. A Warcraft-3-style in-game class picker, followed by four consecutive attempts to make its overlay actually go away. |
| **4. Progression and tier classes** | Jul 5, 02:42–03:11 | ~18 | A stats backend, a tier/unlock model, three unlockable archers. Built across five parallel branches and merged in a single three-minute burst. |
| **5. The bot engine** | Jul 5, 03:28–05:22 | ~30 | Perception, threat registry, dodge geometry, aim error, target scoring, a shopping brain, a state machine. **This is the busiest stretch in the repo: 121 commits on July 5, 25 of them between 4 and 5 in the morning.** |
| **6. The hero-spawn crisis** | Jul 5, 04:16–12:30 | ~12 | Custom archer heroes would not spawn. At all. Eight hours of precaching, byte-order marks, file encodings and hero lists before the actual answer turned up. Three of the four architecture rules in this repo's `CLAUDE.md` were written during this phase. |
| **7. Terrain as a gameplay layer** | Jul 5, 14:52 – Jul 6, 09:16 | ~25 | River currents that push you, high ground that sees further, cliffs that stop arrows. An arena manifest becomes the single source of truth, with a CI check to stop it drifting. |
| **8. Procedural map generation** | Jul 5, 18:11 – Jul 6, 19:56 | ~20 | A Python tool that rewrites Valve's map format directly. Involved reverse-engineering an undocumented tile-grid schema and a three-commit fight with a single minimap texture. |
| **9. Four features at once** | Jul 6, 09:41–13:36 | ~10 | Terrain traversal, bot aggression, game rules and ability tooltips developed simultaneously in separate worktrees, then merged together. |
| **10. Real playtests** | Jul 6, 21:30 – Jul 8, 15:55 | ~45 | An actual human plays the game and files feedback rounds. This is where three entire subsystems turn out to have never worked, and where the bots are discovered to be issuing 39 orders per second while firing nothing. |
| **11. The quality gate** | Jul 8, 19:00 – Jul 9, 10:42 | ~18 | An automated harness that buys every item, casts every ability, and asserts each one had a visible effect — then films it. Nine consecutive fixes to stop it lying in both directions. |
| **12. Tearing the map down** | Jul 9, 10:05–18:10 | ~16 | Playtesting says the elaborate terrain plays badly. The moat, the plateau, the mounts and the ramps get deleted. This is the only day in the project that removes more than it adds. |
| **13. Proving it on video** | Jul 10 – Jul 13 | 4 (squashed) | Four milestone pull requests that shift the standard from "it runs" to "here is the frame where it worked." |

The last four days show as one commit each because they were squash-merged; roughly 80
commits of detail live on their feature branches. The daily diff sizes are normal — the
work didn't slow down, only the log did.

---

## Twenty commits worth reading

**1. The first commit is a document.**
[`6362ccc`](https://github.com/carloslibardo/archer-wars/commit/6362ccc24126ef4c45dd9baf3e7ebd578b7d26f6)
— a design spec and research captures. No code for another three hours. Every feature in
this repo followed the same order afterwards: spec, plan, then implementation.

**2. Tests before features.**
[`fcb13c9`](https://github.com/carloslibardo/archer-wars/commit/fcb13c953caba56bb000480925fccb410c34890d)
scaffolds the project and
[`90f642d`](https://github.com/carloslibardo/archer-wars/commit/90f642d1a93d6341e280f43c032766867a75c880)
adds the CI gate — same minute, before a single gameplay feature exists.

**3. A playable game, three hours in.**
[`ae66462`](https://github.com/carloslibardo/archer-wars/commit/ae66462825f8baf69f3735b9128799c926d56cfb)
— "FFA core loop — forced archer, linear-projectile arrow, kill scoring, win at 20." Not
pretty, but it's the game.

**4. The research wins its first argument.**
[`a45806e`](https://github.com/carloslibardo/archer-wars/commit/a45806e9fe877d6f97163ef1e8e5652dc098d85a)
— "correct archer count 5→4 (recovered public mirror)." The spec had guessed. Recovered source said
otherwise. The dossier won, and kept winning.

**5. The invented-API tax comes due.**
[`7cde0bd`](https://github.com/carloslibardo/archer-wars/commit/7cde0bdcf74e421e4d4820b00ba81c13e012e6eb)
— "`ModifierState.TRUE_SIGHT` doesn't exist." First of five commits in ten minutes deleting
Dota APIs that were entirely plausible and entirely imaginary.

**6. Sometimes the missing API costs you an architecture.**
[`6d86eca`](https://github.com/carloslibardo/archer-wars/commit/6d86ecae22d1f7c44169610f68d8a6f2385d9975)
— "rewrite shopZone.ts to poll — trigger-touch events don't exist." The shop was built on
trigger volumes. Dota doesn't have them. The shop now checks, sixty times a second, whether
you're standing in it.

**7. Five branches, one merge, three minutes.**
[`e4efeb9`](https://github.com/carloslibardo/archer-wars/commit/e4efeb9e6c3e195a9945187ad6ccf7ea6e42bd34)
through
[`d6cab58`](https://github.com/carloslibardo/archer-wars/commit/d6cab58fc3489341dabbd69caca1f42d918a21e6)
— the progression system was built as five independent workstreams and reassembled at 3:03
in the morning. The parallelism is visible in the commit graph.

**8. The diagnostic tool broke the thing it was diagnosing.**
[`9896635`](https://github.com/carloslibardo/archer-wars/commit/9896635eb20f0d64398bc2b9db8e737aeb188846)
adds a temporary probe to figure out why heroes won't spawn.
[`e355814`](https://github.com/carloslibardo/archer-wars/commit/e355814692bc39d153c9e656dc0ed85b016c4697)
removes it 63 minutes later: "try/catch+continue crashed addon load." The probe was
crashing the game before it could report anything.

**9. Hours lost to three invisible bytes.**
[`3613e2c`](https://github.com/carloslibardo/archer-wars/commit/3613e2c2c07b35fe3fae8275ba8313da03d673f8)
— "pure-ASCII `npc_heroes_custom.txt` so engine encoding sniff stops rejecting the whole
hero file." Dota was silently discarding the entire hero definition file because of a
byte-order mark. No error, no warning, just no heroes.

**10. The breakthrough.**
[`11a9635`](https://github.com/carloslibardo/archer-wars/commit/11a9635c339c0cfbc025e23544bdd1d0d2ec95ad)
and
[`299bbac`](https://github.com/carloslibardo/archer-wars/commit/299bbaccd2e51b7cc495580245d9106fd6c30fe9)
— archers aren't new heroes, they're existing Dota heroes overridden in place. Custom hero
names never spawn in this engine, full stop. Eight hours of debugging collapse into one
architectural rule that the whole codebase now depends on.

**11. The console command that killed the editor.**
[`729aab5`](https://github.com/carloslibardo/archer-wars/commit/729aab554583cfa617486cb18a92679546c2e4a3)
— "seat bots via `dota_create_fake_clients`, not `dota_bot_populate`." The obvious command
hard-crashed the tools client in this map. No traceback, no log line, the process just
died.

**12. Bots don't pick heroes, they're handed them.**
[`d3e1b0f`](https://github.com/carloslibardo/archer-wars/commit/d3e1b0fe499894517063660affe6644762b0b513)
— every "get this player's hero" call had been silently returning nothing for every bot in
the game, because they're assigned heroes rather than selecting them.

**13. It starts looking like a product.**
[`80d333e`](https://github.com/carloslibardo/archer-wars/commit/80d333ee0b991f871477935333d3b0368fc14d13)
— a pre-game panel where the host picks bot count and difficulty. The first commit that
isn't about making something work at all.

**14. macOS ships a smaller Lua.**
[`b2ca13a`](https://github.com/carloslibardo/archer-wars/commit/b2ca13a89acd2b1627b373d385e5ce975a20de89)
— retail Dota on macOS strips the Lua debug library, so the build had to stop emitting
source maps entirely. A platform difference reaching all the way back into the compiler
configuration.

**15. Three commits for one image.**
[`ce7a68d`](https://github.com/carloslibardo/archer-wars/commit/ce7a68dbed1dca9b99896c6bcda06120a02ab375)
(PNG rejected) →
[`5835841`](https://github.com/carloslibardo/archer-wars/commit/58358418becc7806d3476ed74d41df01d3782e4a)
(must reference the *compiled* texture). Two minutes apart. The minimap now works.

**16. The 9:30 PM triple.**
Three commits, same minute, July 6 —
[`e9e408d`](https://github.com/carloslibardo/archer-wars/commit/e9e408d4281622d912ee3996429a24ca2eb1a8bb)
"real-match fill bots never registered,"
[`cc03f21`](https://github.com/carloslibardo/archer-wars/commit/cc03f21b5b06c1c03c8e7d6cb18a340415097455)
"buys silently no-op'd," and
[`b2a6bc6`](https://github.com/carloslibardo/archer-wars/commit/b2a6bc6d64a84702548397fbd61955b0d5a21d51)
"ability tooltips dead — addon localization must be UTF-16 LE, not UTF-8." Three separate
subsystems, all of which had passed their tests, none of which had ever worked in a real
match. Someone playing the game found all three in one sitting.

**17. Thirty-nine orders a second, zero arrows.**
[`38ad88d`](https://github.com/carloslibardo/archer-wars/commit/38ad88d4a10be45a7c7825140a1621ea63c74a13)
— the bot AI was re-issuing its cast order every frame, and each new order cancelled the
previous one's windup. The bots were trying to shoot constantly and had never fired once.

**18. The comedy run.**
[`7cb1ed4`](https://github.com/carloslibardo/archer-wars/commit/7cb1ed46a934e66dbd683d17535d3918e6b8b807)
the ward spawns invisible;
[`11d490e`](https://github.com/carloslibardo/archer-wars/commit/11d490e0a3b21f7933388d39f04edb9d1965d036)
ships a *visible* scout hawk;
[`8c98e43`](https://github.com/carloslibardo/archer-wars/commit/8c98e43b5e1b275ecaf8ee5b6e8cf752bf1c5021)
fixes the grappling hook for the second time by abandoning the engine's motion controller;
[`f2db43c`](https://github.com/carloslibardo/archer-wars/commit/f2db43cc8021fc42c385ed0face55e9c9c138fce)
finally gets "a real Pudge-style hook reel."

**19. Deleting two days of work because it wasn't fun.**
