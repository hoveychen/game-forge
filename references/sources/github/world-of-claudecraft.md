# World of ClaudeCraft — classic-WoW-style browser MMO + headless RL env, seeded in ~48h by "Claude Fable 5", now community-built

- Repo: https://github.com/levy-street/world-of-claudecraft  (live: https://worldofclaudecraft.com ; ModDB page; YouTube "Claude Built an MMO. I Had to See It."; press release GlobeNewswire 2026-06-22; write-up https://www.thesidequest.biz/p/world-of-claudecraft-an-mmo-for-1000)
- Stars: 2,268 / 718 forks (by far the biggest in this set). 19,669 commits 2026-06-10 → 2026-09-28 (community + many agent subagents, e.g. author "Codex Dev Subagent").
- Tool/model: Claude Code with Claude Fable 5 for the initial 2-day build (first commit "Co-Authored-By: Claude Fable 5"); ~$1,000 metered compute; two devs (Reuben Horne, Max Polaczuk, Levy Street). Later Codex + Gemini agents too (AGENTS.md, GEMINI.md, .codex/agents/*.toml).
- Genre: persistent multiplayer classic-era MMORPG (9 classes, talents, dungeons, raids, PvP, professions, market), Three.js, authoritative WS server + Postgres, desktop/mobile apps, Gym RL env.
- Result evidence: live public world with players, thousands of Reddit upvotes, 2.2k★, 700 forks, press coverage. Strongest real-world traction of any case.
- Spec: **no verbatim prompt published.** Per the write-up, the brief was essentially "generate a faithful MMO sandbox [classic WoW] to train [RL agents] inside." The implicit spec = the enormously well-documented vanilla WoW rule set ("Real vanilla formulas: rage conversion, spell-hit table, armor DR, XP curve and gray bands ..."). CLAUDE.md still says: "Gameplay math follows real classic-era MMO formulas ... Don't invent balance numbers." The first commit message (below) is the best available statement of the day-2 scope.
- One-shot vs multi-session: initial 2-day sprint (4 feature commits on day 1 incl. AWS deploy, then "level-20 expansion", "graphics overhaul stage 1–3", "judge fixes", "21 verified review findings"); then months of multi-agent/community development.
- Notable process practices:
  - Day-1 test harness was part of the first commit: 52 unit tests, 26-check integration suite, browser E2E, and **a 5-bot raid that clears the dungeon end-to-end**.
  - Architecture built for agent verification: one deterministic 20 Hz sim core runs in browser, server and headless RL env; `IWorld` single seam; invariants guarded by tests/architecture.test.ts (no DOM imports in sim, no Math.random/Date.now).
  - Hierarchical CLAUDE.md: lean root (~200 lines, "anchor guidance on stable paths, symbols, pinned tests, never on counts that rot") + ~20 per-directory CLAUDE.md loaded on demand.
  - Default task workflow in CLAUDE.md: worktree per task, base off release branch, review existing impl first, preserve behavior, tests for every sim/server change, before/after screenshots for visual changes, deliver a mergeable PR that passes the gate (`node scripts/gate_select.mjs`).
  - Hooks: qa-stop.sh (Stop hook runs QA), deny-generated-edit.sh (blocks editing generated files).
  - 13 specialized reviewer subagents (.claude/agents/: gate-integrity-reviewer, content-obligations-reviewer, render-performance-reviewer, server-hot-path-reviewer, test-coverage-auditor, migration-safety, privacy-security...).
  - Monte-Carlo balance analyses as docs (healing, class balance, rift rank) instead of vibes.
  - Post-launch: an agent listens to Discord, writes and tests code end-to-end against vibe-coded bot players.

---
## Verbatim: first commit message (2026-06-10, the 2-day build's first snapshot)
Eastbrook Vale: WoW-Classic-style MMO + RL training environment

A vanilla-flavored micro-MMO with three faces sharing one deterministic
20Hz sim core: a playable Three.js client (offline or online), an
authoritative multiplayer server (WebSocket + Postgres accounts and
character persistence), and a headless gymnasium environment for
training agents at thousands of steps/sec.

- Real vanilla formulas: rage conversion, spell-hit table, armor DR,
  stat rules, XP curve and gray bands, group XP bonuses
- All nine classes with vanilla learn levels and rank values, including
  hunter ranged auto-shot, heals/HoTs/absorbs, seals and judgements,
  combo points, polymorph, channels, and bear form
- Parties, atomic trading, duels, tap rights, chat
- The Hollow Crypt: a party-instanced 5-player elite dungeon with a
  storyline chain, vanilla elite scaling, and a pulse-mechanic boss
- Procedural everything: terrain, models, textures, audio; no assets
- docker compose up -d --build deploys postgres + game server
- 52 unit tests, 26-check integration suite, browser E2E, and a 5-bot
  raid that clears the dungeon end-to-end

Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>

## First-day commit log (oldest last)
```
2026-06-11T11:05 feat: lookdev overhaul — PBR terrain splat, HDRI sky dome + IBL API, real water normals, N8AO, Kenney sprite VFX
2026-06-11T11:05 fix: props polish from probe review — mine mound, hut/tent kits, beached rowboat, stepped pier
2026-06-11T11:04 feat: foliage overhaul — Quaternius Stylized Nature MegaKit replaces procedural trees/rocks
2026-06-11T10:42 feat: settlement props from real CC0 assets — village buildings, Kenney kits, instanced camps
2026-06-11T10:39 feat: dungeon interiors rebuilt from KayKit Dungeon Remastered kit, colliders derived from shared layout data
2026-06-11T09:52 feat: await asset preload in startGame with failure overlay
2026-06-11T09:50 chore: preload registry + worktree-friendly asset script (absolute src paths)
2026-06-11T09:48 feat: asset pipeline + first shipped asset set (characters, creatures, weapons, HDRIs, terrain PBR)
2026-06-11T09:36 chore: asset-pipeline groundwork — dungeon.ts extraction, asset MIME/404, Dockerfile public/, .dockerignore
2026-06-11T08:30 Merge feature/expansion-levels-1-20: the level-20 expansion
2026-06-11T06:14 feat: de-Roblox remodel — organic geometry for characters, buildings, and terrain props
2026-06-11T02:23 fix: 21 verified review findings — boss resets, exclusive epic drops, shadows, leaks, guards
2026-06-11T01:14 feat: graphics polish pass — judge fixes for shadows, water, foliage, dungeons
2026-06-11T00:03 feat: graphics overhaul stage 3 — foliage wind/variation, rig+prop PBR merge, VFX bloom
2026-06-10T22:35 feat: graphics overhaul stage 2 — chunked splat terrain, shader water, biome sky/fog
2026-06-10T21:46 feat: graphics overhaul stage 1 — gfx tiers, post pipeline, lighting+IBL, PBR map generators
2026-06-10T21:21 test/docs: new-dungeon + boss-mechanic tests, README for the expansion, RL env horizon
2026-06-10T20:40 feat: full 1-20 expansion content — Mirefen Marsh, Thornpeak Heights, two dungeons, spell ranks, icons
2026-06-10T15:41 feat: expansion foundation — level cap 20, 3-zone world, dual eat+drink, generalized dungeons
2026-06-10T10:02 feat: combat VFX, soundtrack, collision/swimming, walk-in dungeon doors, fixes
2026-06-10T08:21 docs: note Ansible (eastbrook_game role) is the canonical prod deploy
2026-06-10T07:57 feat: AWS deployment — first-boot script, DEPLOY.md, loopback-only ports
2026-06-10T07:39 feat: vanilla spell pushback — hits delay casts instead of cancelling
2026-06-10T07:39 fix: make browser E2E scripts cross-platform and deflake timing races
2026-06-10T05:57 Eastbrook Vale: WoW-Classic-style MMO + RL training environment
```


---
## Verbatim: CLAUDE.md (root)
<!-- World of ClaudeCraft, project-root CLAUDE.md. Keep this lean (about 200 lines)
     and strictly repo-wide. Area-specific guidance lives in each subdirectory's own
     CLAUDE.md (src/sim/, src/render/, server/, ...), which load on demand when you
     open files there, so do NOT duplicate them here. Anchor guidance on stable paths,
     symbols, and pinned tests, never on counts that rot. HTML comments like this are
     stripped before load (zero tokens). No em dashes, en dashes, or emojis. -->

# World of ClaudeCraft

A classic-style micro-MMO **and** a headless reinforcement-learning
environment, both driven by one deterministic TypeScript simulation core.
Stack: TypeScript (ESM, `strict`) · Three.js renderer · `ws` WebSockets ·
Postgres (`pg`) · Vite + esbuild · Vitest. No UI framework in the game client; tiny
dependency set. The one sanctioned exception is the standalone admin dashboard
(`src/admin/`), which is built with Svelte 5 (it never touches the game client bundle).

## Repo map
| Path | What it is |
|---|---|
| `src/sim/` | **Deterministic game core, the source of truth.** No DOM/Three deps; runs in browser, server, and headless. |
| `src/sim/content/` | Data-as-code: classes, abilities, talents, zones, dungeons, items, professions, mounts, deeds, Reliquary pages. |
| `src/render/` | Three.js renderer (procedural geometry/textures/VFX + curated GLBs). Reads the world; never mutates it. |
| `src/game/` | Local input, camera, keybinds, gamepad, mobile controls, sampled WebAudio SFX, and procedural music. |
| `src/ui/` | Classic HUD (frames, windows, tooltips, map, FCT), procedural icons, i18n. |
| `src/styles/` | Extracted HUD CSS under one `@layer` order, imported once via `src/main.ts`. See `src/styles/CLAUDE.md`. |
| `src/net/` | Online client: REST auth + WebSocket world mirror (`ClientWorld`), reconnect, native-app glue, wallet glue. |
| `src/admin/` | Admin dashboard SPA (separate `admin.html` entry). |
| `src/guide/` | Public guide/wiki SPA (separate `guide.html` entry, served at `/wiki`); spoiler-safe content generated from `src/sim/`. |
| `src/editor/` | World editor SPA (separate root-level `editor.html` entry); its 3D viewport composes the real `Sim` + `Renderer`. |
| `src/world_api.ts` + `src/world_api/` | `IWorld`, the seam render/ui depend on: one facet interface per domain file under `src/world_api/`, re-aggregated by the barrel (see Architecture). |
| `src/main.ts` | Client entry; fixes the world seed. |
| `server/` | Authoritative game server: HTTP+WS, world loop, Postgres, auth, social, moderation. |
| `server/http/` | The REST request pipeline spine: table router, middleware onion, per-domain `RouteDef` tables, typed schemas, stable error codes. |
| `server/epic/` · `server/steam/` · `server/parse/` · `server/email/` | Store/platform glue, combat-parse ingest, transactional email; each has its own `CLAUDE.md`. |
| `headless/` + `python/` | RL env server (`env_server.ts`) + Python Gym bindings. |
| `bot/` | Discord bot (role sync, relay, activity feed; own `CLAUDE.md`). |
| `electron/` (+ `build/`) | Desktop (Steam) shell + packaging assets; see `docs/desktop-release.md`. |
| `android/` + `ios/` | Capacitor native shells (`npm run native:*`). |
| `tests/` | Vitest suite (subdirectory map in `tests/CLAUDE.md`). |
| `scripts/` | Asset/build/i18n/SFX tooling + browser E2E / screenshot scripts. |
| `patches/` + `data/` | pnpm-patched dependencies (Three.js is patched; check before bumping it) + checked-in map data. |
| `public/` · `docs/` | Static assets, **deployed verbatim to the live site** · design + PRD + ops docs. |
| `mediawiki/` + `deploy/` | Player-wiki container + production first-boot assets (see `DEPLOY.md`). |

Most directories above have their own `CLAUDE.md` with local conventions; read it when you work there.

## Commands
Install once per clone/worktree with **pnpm** (pinned via `packageManager` in
`package.json`; Corepack not required): `npm install -g pnpm@<the pinned version>`, then
`pnpm install --frozen-lockfile`. Same on macOS, Linux, and Windows; the shared store
makes multi-worktree installs cheap. Never commit `package-lock.json`. Full policy:
CONTRIBUTING.md. After install, `pnpm run <script>` and `npm run <script>` both work;
the nested `npm run` forms below are the package.json script names.

- `npm run dev`: Vite client on :5173 (proxies `/api`, `/admin/api`, `/ws` to :8787).
- `npm run server`: esbuild-bundle + run the authoritative server on :8787.
- `npm test`: Vitest. **Prefer a single file while iterating:** `npx vitest run tests/sim.test.ts`.
- `node scripts/gate_select.mjs`: **the pre-merge gate.** Same step list as `npm run gate`
  (nothing dropped) with one substitution: the full vitest run becomes ONE merged
  `vitest related` invocation (the always-run floor rides it as self-selecting seeds,
  same form as the CI shards). Roughly 3x faster; falls back to the full suite for any change it
  cannot reason about. See `docs/qa-gate.md`.
- `npm run gate`: the full CI-equivalent gate, still the deeper check (i18n gen + freshness, malware scan,
  changed-files biome, SFX conformance, full tests with bounded workers, the real-browser
  regression suite, `tsc`, all builds;
  release-tier automatically on a `release/**` branch; FFmpeg/ffprobe come from the bundled
  ffmpeg-static/ffprobe-static packages, PATH is the fallback). Exit-code-safe;
  use it instead of an ad-hoc `&&` chain before calling a change done (piping `npm test` through
  `tail` masks its exit code, and an unbounded run flakes heavy suites under core contention).
- `npm run gate:fast`: the high-signal day-loop subset while iterating; never the merge
  bar (`docs/qa-gate.md` owns the tier detail).
- `npm run build`: regen all generated artifacts (i18n, wiki content, sitemap, SFX + media
  manifests), then `vite build` (the entry list lives in `vite.config.ts`).
- `npm run env` / `npm run bench`: build + run the headless RL env server.
- `npm run db:up` / `npm run db:down`: Postgres 16 in Docker (dev DB on :5433).
- `npm run realms`: run multiple realm processes locally.
- `node scripts/release_mint.mjs vX.Y.Z`: THE settings step when a new `release/**`
  branch is minted (re-points the merge-queue ruleset, with an audit dump; run it
  every mint or the queue goes silently dormant, see `docs/merge-queue.md`,
  "Minting a release branch"). Merging on the queue-protected branches: `gh pr merge`
  does not work there; use the `enqueuePullRequest` GraphQL mutation (exact command
  in `docs/merge-queue.md`).

See `README.md` for the full host/develop/play guide and the classic-fidelity checklist; `DEPLOY.md` for production.

## Default task workflow
Unless the request says otherwise, the default for any task is to accomplish the stated
objective, and to deliver it this way. This is the baseline for every contribution.

Before making changes:
- **Base your work off the latest release branch** (and its tracking issue), not `main`. The
  release branch is the active integration base; `main` trails it.
- **Create and use a separate git worktree for the task**, so unrelated working-tree WIP never
  contaminates the branch and parallel tasks stay isolated.
- **Review the existing implementation before modifying anything.** Read the code paths, tests,
  and the local `CLAUDE.md` for the area you are touching first.
- **Preserve existing behavior unless the goal explicitly requires changing it.**

Implementation requirements:
- Make **all** the changes the objective needs: code, data, validation, UI, and tests.
- **Avoid unrelated refactors.** Keep the diff scoped to the task.
- **Add or update automated tests** covering the new behavior (`sim/` and `server/` changes
  always get a test).
- Keep the solution maintainable and extensible: follow the module-first seams below, do not grow
  a monolith.
- **If the change is visual, add before/after screenshots to the PR** (desktop and mobile where
  relevant), committed under `docs/screenshots` and referenced from the PR body (the
  `pr-screenshots` skill has the capture recipe).

Deliverable: a PR based off the latest release branch, following
`.github/PULL_REQUEST_TEMPLATE.md`, that is **fully mergeable and passes CI**. Gate it locally
with `node scripts/gate_select.mjs` (above) before calling it done; `npm run gate` remains
the deeper check when you want the whole suite locally.

## Architecture (the load-bearing ideas)
- **One sim, three hosts.** The exact same `src/sim/` code runs the offline
  browser world, the online server, and the RL env. Behavior must be identical
  everywhere; that is the whole point.
- **`IWorld` is the only seam.** `IWorld` is split into per-domain facet interfaces
  (`src/world_api/<domain>.ts`); the barrel `src/world_api.ts` re-aggregates them and
  stays count-free. The offline `Sim` satisfies it structurally and the online
  `ClientWorld` implements it by mirroring server snapshots. **`src/render/` and
  `src/ui/` talk only to `IWorld`**, never to `Sim`/`ClientWorld` concretely.
  New feature: add the member to the matching facet file (never the barrel), implement
  it in BOTH worlds, and update the pinned member list in `tests/world_api_parity.test.ts`
  in the same change (see `src/world_api/CLAUDE.md`).
- **The server is authoritative.** Clients stream movement intent + commands at
  20 Hz; the server runs the one shared `Sim` and returns interest-scoped
  (~120 yd) snapshots + per-player events. All combat, loot, quest credit, and
  economy resolve server-side. The client is a renderer; it never decides outcomes.
  REST requests run through the in-house pipeline seam (`server/http/`): a new endpoint is a
  `RouteDef` module behind the registry, never an inline route in `main.ts` (see `server/http/CLAUDE.md`).

## Invariants, YOU MUST keep these
- **`src/sim/` has zero DOM/browser/Three.js imports** and never imports from
  `render/`, `ui/`, `game/`, or `net/`. It must run unchanged in Node and the
  browser. (Guarded by `tests/architecture.test.ts`, which scans every sim file.)
- **Determinism.** The sim is a fixed **20 Hz** tick (`DT = 1/20`). All randomness
  goes through `Rng` (`src/sim/rng.ts`): **never `Math.random`**, `Date.now`, or
  `performance.now` in sim logic. Same seed gives the same world. (Also guarded by
  `tests/architecture.test.ts`.)
- **Gameplay math follows real classic-era MMO formulas** (rage, hit tables, armor DR,
  XP curves; see `README.md` and `docs/design/`). Don't invent balance numbers.
- **Graphics and performance settings are gameplay-neutral.** A preset or tier knob may shed
  cosmetic richness but NEVER actionable information a player reacts to (own debuffs, party/raid
  HP, cast bars, target HP granularity, enemy positions). Tier knobs read the STATIC preset via
  `src/game/ui_effects_profile.ts`, never the FPS governor. Rule of thumb: if it hides or delays
  something a player acts on, it is not allowed. Exemplars + fairness tests: `src/ui/CLAUDE.md`
  and `docs/design/graphics-settings-fairness.md`.
- **Don't hand-edit generated files** (`*.generated.ts`, the `i18n.resolved.generated`
  bundles, the SFX manifest + runtime pack): regenerate via the owning build step
  (`npm run build` chains them all; SFX tuning edits `scripts/sfx/sfx_gain_map.json` /
  `sfx_speed_map.json`, then `npm run sfx:manifest`). A `PreToolUse` hook blocks direct
  edits to the `*.generated.ts` and resolved-i18n artifact classes; the rest of the rule
  is on you.
- **i18n: every player-visible string is a `t()` key**, classified by render sink, not
  statement type: labels, tooltips, placeholders, aria/alt, toasts, dialogs, validation and
  connection errors, static HTML, `document.title`, server-sent player text, and the whole
  admin dashboard (operators are users). Rendered text always comes from `t()`: never concat,
  `?? 'English'` fallbacks, default params, or `setAttribute('aria-label'|'title'|...)`.
  Dev-channel text (`console.*`, assertions, a `throw` no catch surfaces) stays English; if one
  string feeds both a log and the UI, split it. Numbers, money, dates, percents go through
  `formatNumber`/`formatMoney`/`formatDateTime`/`Intl`.
  - **Contributors add ENGLISH only** to the matching `src/ui/i18n.catalog/<domain>.ts` module;
    the maintainer fills every locale at release. Never edit the `src/ui/i18n.locales/` overlays.
    The PR-tier gate permits English-only (one exception, M16: a new wordy English value also
    needs its non-Latin fills in the same change); the release-tier gate (`I18N_RELEASE_TIER=1`)
    hard-fails on any `pending` row.
  - **`src/sim/` and `server/` stay language-agnostic** (no `t()`, no DOM) but their player text
    is in scope: emit a stable key plus values, or English re-localized via the client matcher,
    in the SAME change. The S3 guard (`tests/localization_fixes.test.ts`) enforces it.
  - Full model (catalog layout, matcher rules, formatters, exceptions): `src/ui/CLAUDE.md` and
    `docs/i18n-scaling/translation-workflow.md`.
- **Every player tooltip follows `docs/design/tooltip-writing.md`.** Write from the live mechanic,
  use resolved values for scaling effects, state important triggers and limits, and change the
  English source first. Use the `write-game-tooltips` skill for any tooltip authoring or audit.
- **Never set `ALLOW_DEV_COMMANDS=1` in production** (it enables the full `/dev` cheat set:
  level/teleport/item cheats, mob spawns, instance teleports, and the dev command GUI).
- **Never commit `.env` or secrets.**

## Conventions
- **ESM + TypeScript `strict`** everywhere. 2-space indent; match the surrounding file.
- **TypeScript toolchain:** `tsc` is the TypeScript 7 native binary (installed as the
  `@typescript/native` alias); a full-repo `npx tsc --noEmit` takes about 2 seconds, so run it
  liberally as a check while working. `require('typescript')` deliberately resolves a
  TypeScript 6 JS API wrapper because svelte-check needs that API; never collapse the dual
  alias yourself (the collapse triggers live in CONTRIBUTING.md, "TypeScript toolchain", and
  `tests/server/new_endpoint.test.ts` pins both arms).
- **Keep the dependency set tiny.** Don't add packages without a clear need. (Svelte
  and `@sveltejs/vite-plugin-svelte` are the one sanctioned exception, scoped to the
  `src/admin/` dashboard bundle; the game/guide/play entries stay framework-free.)
- **No em dashes, en dashes, or emojis** anywhere: code, comments, docs, commits, PR
  text, or player-facing copy. Use commas, colons, parentheses, or "to" for ranges.
  (An emoji that stands in for a real label still needs its real `t()` text.)
- **Commits:** Conventional Commits with a scope (`feat(talents): ...`, `fix(net): ...`,
  `test(sim): ...`), and every commit carries a BODY, never a title alone: after a
  blank line, 1 to 4 plain sentences or short bullet lines saying what changed and
  why (the intent or finding behind it, not a file list), wrapped near 72 columns.
  Branches: `feature/<slug>`, `fix/<slug>`.
- **Docs follow the anchor rule:** cite stable paths, exported symbols, and pinned tests;
  never literal counts or line numbers that rot (see `docs/qa-gate.md`).

## Modularity: module-first is the default for ALL new code
The default, stated explicitly: **every piece of new logic lands as its own small, reusable,
tested module behind an existing seam, imported where needed. Never append it to an existing
big file.** The deciding question is one: **does this code need the coordinator's private
mutable state** (the live `Sim` loop, the `Hud` DOM and per-frame buffers, the renderer's
scene graph)? If no, it is a sibling module, every time. If only partly, extract the pure
part (math, formatting, id/state resolution) into a host-agnostic module a Vitest imports
directly and leave the coordinator a thin consumer.
- **The monolith ratchet.** The known-large logic files (the four sanctioned coordinators
  `src/ui/hud.ts`, `src/sim/sim.ts`, `src/main.ts`, `src/render/renderer.ts`, plus the
  monoliths that formed since: `server/game.ts`, `src/sim/world.ts`, `src/net/online.ts`,
  `src/game/music.ts`, `src/render/foliage.ts`, `src/sim/colliders.ts`, `server/db.ts`)
  are ACTIVE extraction targets: never GROW one, and do not split one just to hit a line
  count. `tests/monolith_budget.test.ts` pins a line-count ceiling per file and fails any
  change that grows one past it; the fix is extraction behind the file's seam, and after
  extracting you LOWER the ceiling. Raising a ceiling is a maintainer decision.
- **`src/main.ts` is a firewall, not a home.** Client-bootstrap helpers (mobile, fullscreen,
  shell, loading, analytics, graphics detection) belong in `src/game/` or `src/ui/` sibling
  modules; never add a top-level function here when a sibling module will do.
- **Data-as-code is exempt.** Large declarative tables (`src/sim/content/*`,
  `src/ui/i18n.catalog/*`, `talent_i18n.ts`, `sim_i18n.ts`) are correctly big; module-first is
  about LOGIC, never data. Do not "modularize" a data table.

Use the seams this repo already has, do not invent new ones:
- New render/ui data or action: add it to the matching `IWorld` facet
  (`src/world_api/<domain>.ts`), implement in BOTH `Sim` and `ClientWorld`, update the
  parity pin (`tests/world_api_parity.test.ts`), then consume via `IWorld` only.
- New HUD component (a window OR a per-frame frame/bar): its own module the HUD composes,
  never a new banner section in `hud.ts`: a pure DOM-free view-core plus a thin painter on
  the `PainterHost` seam; HUD-domain components land in `src/ui/hud/<domain>/` behind its
  `index.ts` barrel. Reuse a FAMILY before bespoke. Full recipe + the perf/window
  contracts: `src/ui/CLAUDE.md`, `src/ui/hud/CLAUDE.md`, and `src/styles/CLAUDE.md`.
- New visual system: a new `src/render/<thing>.ts` the renderer calls, not a method bank on
  `renderer.ts` (pure logic goes in a `RENDER_PURE_CORES` core; see `src/render/CLAUDE.md`).
- New GPU producer (a material, a light, a GL context, a group added to the scene after
  boot): it is a client of the preparation scheduler, never a free draw. Give it a prewarm
  home or a gate, and see `src/render/CLAUDE.md` "GPU work: every new producer is a client
  of the scheduler"; dispatch `render-performance-reviewer` on any such diff.
- New world GLB prop or building from a reference image: the `image-to-glb` skill owns the
  whole pipeline (exporter, optimizer, fingerprint pins, adapter); do not improvise one.
- New sim SYSTEM behavior (a combat/mob/social/economy mechanic, not just a data record):
  its own module behind the `SimContext` seam (`src/sim/sim_context.ts`), with backing
  state kept on `Sim` as a live `ctx` view, never a new method cluster on the `sim.ts`
  coordinator. See `src/sim/CLAUDE.md`.
- New game content (mob/quest/item/ability/zone/dungeon/mount): a declarative record in
  `src/sim/content/`, merged by `data.ts`, never a content table inline in `sim.ts`. Every
  content change carries ALL of its same-change obligations: wiki regen
  (`npm run wiki:content`, freshness-gated by `tests/guide.test.ts`) plus any new `guide.*`
  prose keys; Book of Deeds records in `src/sim/content/deeds.ts` for every new piece of
  conquerable content (`docs/design/deeds.md`, pinned by `tests/deeds_content.test.ts`;
  deeds are cosmetic-only, never power); Reliquary pages for new conquerable unique loot
  (`docs/design/reliquary.md`, pinned by `tests/reliquary_content.test.ts`); committed WebP
  art for every new item id, plus non-Latin name fills when the English name is wordy
  (M16); `src/ui/world_entity_i18n.ts` names for new named entities. The
  `content-obligations-reviewer` agent audits exactly this list; dispatch it on any
  content diff.
  **Every new player-visible proper noun is IP-checked BEFORE it ships, in the same
  change that authors it**: web-verify the name (exact-phrase plus coined-token
  searches against the major game wikis) and never reuse a coined term or a full
  name distinctive to another game; shared generic fantasy English is fine. Protocol
  and worked verdicts: `src/sim/content/CLAUDE.md` "Naming originality" and
  `docs/design/naming-audit.md`. A collision found after shipping is
  fixed display-only (ids are frozen) and pinned in `tests/originality_renames.test.ts`.
- New server REST endpoint: a `RouteDef` module (`server/<domain>.ts` `export const routes`)
  registered in `server/http/registry.ts`, never an inline handler in `main.ts`. Scaffold with
  `npm run new:endpoint` (see `server/http/CLAUDE.md`).
- New server hot-path work (a shared read, a per-tick self-path read, a recurring
  autosave or sweep job, a table or in-memory collection that grows, a broadcast
  payload): use the performance seams in `server/CLAUDE.md` "Hot paths": cached reads
  with single-flight and moderation busts, the retention sweep for every table that grows
  without bound, build-once realm readouts and serialize-once events, and the revision
  plus cadence gate for any per-tick read of a collection that grows with realm age. An
  uncached viewer-identical read, a new unbounded table without a retention story, a
  per-tick read with no named bound, or a recurring job or durability write whose cost
  scales with a whole book instead of what changed is a defect, not a style choice; and a
  fresh world or a
  fresh-bot fleet is never evidence that such a read is cheap. The
  `server-hot-path-reviewer` agent audits exactly these seams; dispatch it on any server
  hot-path diff, including a `src/sim/` change to a read `selfWireJson` consumes.
- New multi-file subsystem: a directory with an `index.ts` barrel exposing only its
  public surface, plus a local `CLAUDE.md` (template: `src/render/characters/`).

Extract on the rule of three, not before: leave two similar blocks alone; a third copy,
or one block with a single nameable responsibility, earns its own module. Never abstract
for one use or a hypothetical future need (the pure-core + thin-consumer reference is
`src/ui/unit_portrait.ts` + `unit_portrait_painter.ts`). **Fix bugs test-first, in
isolation:** reproduce the bug with a failing test that exercises the real code path
(if the buggy logic is buried in a coordinator, that is the signal to extract the unit
under test into its own module first), then make the smallest change that turns it green.
Detailed heuristics and the bug-fix workflow live in the `extract-and-test` skill
(`.claude/skills/extract-and-test/`).

## Testing & verification
- Logic/unit: Vitest (`tests/`). Add or update tests when you change sim or server behavior.
  Real-browser suite: `npm run test:browser` (`tests/browser/`); part of the full gate,
  runnable standalone.
- E2E/visual: `scripts/*.mjs` drive real browsers via `puppeteer-core` and need
  `npm run dev` (often `npm run server` too) running. Bot raids / E2E that teleport
  or level need `ALLOW_DEV_COMMANDS=1` (dev only).
- **QA gate before a change is done.** Run `/qa` (or invoke the `qa-checklist` agent) over your
  diff: it checks every invariant in play, names the domain reviewers to dispatch, and ends with
  an adversarial "what is missing" pass. Checked-in hooks enforce the cheap floor so it is
  never skipped: a `Stop` hook (`.claude/hooks/qa-stop.sh`) blocks instantly on an em/en dash,
  emoji, stray `.only(`, leftover `debugger`, or a wall-clock/`Math.random` call added under
  `src/sim/`; a `PreToolUse` hook blocks edits to the `*.generated.ts` and resolved-i18n
  artifacts; the `.githooks/pre-push`
  floor runs `tsc`, the guard tests, biome, and the copy scan at push time. See
  `docs/qa-gate.md` and `.claude/hooks/README.md`.
- **Biome / formatting / CI.** Biome (version pinned in `package.json`; `biome.json`: 2-space,
  lineWidth 100, single quotes, trailing commas). CI and the pre-push floor gate CHANGED FILES
  ONLY (`npm run ci:changed`) and fail on errors and format diffs, NOT on lint warnings.
  Whole-repo `biome check .` is
  intentionally RED (pre-existing debt): a DEFERRED chore, not your regression, do not fix it.
  NEVER run a whole-repo `--write`; format only the files you changed:
  `npx @biomejs/biome check --write <changed-file.ts>`.

## Working style by model capability
This whole file is the baseline for **any** model: obey all of it. The block below changes
only how much you take on at once and at what effort, never what is correct. Pick a tier
from what your model and harness can actually do, not from the model name alone (names go
stale and new models appear): if you can plan multi-step work end to end, sustain a
long-horizon task, and spawn parallel subagents reliably, use the frontier tier; when
unsure, or on a smaller or unfamiliar model, use the baseline.
- **Baseline (the default, and always safe):** take small, verifiable steps; checkpoint
  with the user before large multi-file changes; use one investigation subagent for a
  broad search rather than fanning out widely. If your runtime has a reasoning-effort
  knob: medium by default, low for latency-sensitive trivia, high for hard reasoning.
- **Frontier (the Claude 5 family, Opus 4.8 and newer, and comparable models):** work
  autonomously. Plan multi-step work end to end and carry long-horizon tasks (migrations,
  multi-file refactors) to completion without pausing after each step, as long as the
  build and tests stay green. Front-load the spec: state the task, intent, constraints,
  and the acceptance check in one turn rather than revealing them piecemeal. Fan out
  parallel subagents across independent files, subsystems, or batch items (these models
  under-spawn by default); do not spawn for work doable in one response. Before declaring
  done, have a FRESH subagent review your diff: its job is COVERAGE (report every
  correctness or requirement gap with confidence and severity), not filtering, which
  happens in a later pass. Effort knob, where available: high or above for coding and
  agentic work; reserve the top tier for genuinely frontier problems and measure, since
  it overthinks structured tasks. The operator can push further with ultracode.
- **Use the repo's reviewers, not ad-hoc subagents.** Purpose-built read-only reviewers
  live in `.claude/agents/` and dispatch via `/qa`; the canonical concern-to-reviewer
  table is in `docs/qa-gate.md`. Highlights: `qa-checklist` (the end-of-contribution
  gate), `content-obligations-reviewer` (any game-content diff), `gate-integrity-reviewer`
  (any change to the gate/CI selection pipeline), `render-performance-reviewer` (any diff
  that produces GPU work: a material, a light, a GL context, a scene attach), plus the
  domain reviewers for sim, parity, database, security, frontend, and tests. Skills cover the repeated workflows:
  `extract-and-test`, `feature-plan`, `review-pr`, `release-merge-audit`,
  `i18n-locale-fill`, `pr-screenshots`, `ci-triage`, `image-to-glb`, `asset-pipeline`.
- **State rule scope literally.** Models follow instructions literally and will not
  generalize a rule across cases unless told. When an invariant covers every case (every
  player string is a `t()` key; all sim randomness goes through `Rng`), say "every" or
  "all"; do not rely on generalization by analogy.
- **Never gate the Invariants, safety (`ALLOW_DEV_COMMANDS`, secrets), or correctness on
  which model you are:** the model named in your system prompt can be stale or wrong, so
  when in doubt use the baseline. Anchor every autonomous step on a check you can actually run (`npx vitest run
  <file>`, `npm test`, `npm run build`, `tests/architecture.test.ts`, the S3 i18n guard
  `tests/localization_fixes.test.ts`), never on "looks done."

## Pointers
`README.md` (host/develop/play + fidelity checklist) · `DESIGN.md` (the adopted interface
design-language standard; interface changes land through its rollout phases) ·
`DEPLOY.md` (production) · `CREDITS.md` (asset licenses) · `docs/design/` (design docs) ·
`docs/prd/` (feature specs) · `docs/qa-gate.md` (the layered QA gate) ·
`docs/merge-queue.md` (the merge queue + required-check contract on protected branches).


---
## Verbatim: AGENTS.md
# Codex entry point

This file owns Codex runtime behavior for World of ClaudeCraft. The root and
directory-local `CLAUDE.md` files remain canonical for repository facts, architecture,
hard invariants, conventions, commands, the default task workflow and deliverable
contract, and the QA contract. Claude-specific model,
memory, Workflow, slash-command, and agent-runtime instructions do not apply to Codex.
Do not edit or replace the Claude setup unless the user explicitly asks for that work.

## Start safely

1. Run `git status --short` before edits and preserve unrelated user work.
2. Follow the default task workflow in `CLAUDE.md`: base the work on the latest
   `release/**` branch, never `main`, and create a separate worktree for the task.
3. Read the root `CLAUDE.md` in full. Before reading or changing files in a directory,
   read that directory's `CLAUDE.md` if it exists. Codex builds its instruction chain at
   session start, so opening a nested file does not load local guidance automatically.
4. Use `rg` and targeted reads to discover the current shape. Follow existing code and
   tests instead of relying on remembered inventories or line numbers.

Never revert, discard, stage, commit, push, file an issue, post a review, or mutate a
remote system unless the user authorized that action. If a commit is requested, stage
only this task's files and follow the scoped Conventional Commit rule in `CLAUDE.md`.

## Work effectively

- Keep the main thread responsible for integration and final verification.
- Parallelize bounded exploration, log analysis, and read-only reviews when useful.
  Give overlapping files one implementation owner and wait for every delegated task
  before reporting completion.
- Treat subagent results as evidence to verify, not verdicts to relay unchanged.
- Use the active session model and reasoning setting. Do not weaken acceptance criteria,
  tests, or review depth for a faster model. Route by task shape, not a hardcoded model:
  clear mechanical work can run fast, while ambiguous architecture and security work
  needs deeper reasoning.
- Fetch current official documentation for external APIs and libraries. Do not write
  unstable interfaces from memory.
- Prefer small modules, decisive tests, and existing seams. Do not add frameworks or
  abstractions without a concrete repository need.

## Codex workflows

Repository skills live in `.agents/skills/` and are invoked as `$skill-name`:

- `$woc-qa`: scope and run the contribution gate, then dispatch relevant reviewers.
- `$woc-extract-and-test`: extract a module behind behavior-pinning tests.
- `$woc-feature-plan`: produce an implementation-ready plan for cross-cutting work.
- `$woc-review-pr`: verify a pull request without posting unless explicitly requested.
- `$woc-file-issue`: draft an issue, and file it only with explicit authorization.
- `$woc-write-game-tooltips`: write or audit plain English tooltips against live combat values and
  scaling.
- `$woc-image-to-glb`: build a shipping GLB asset from a reference image through the
  repo pipeline.
- `$woc-release-merge-audit`: find semantic damage after release integration.
- `$woc-release-malware-audit`: scan and judge malicious-code risk.
- `$woc-codex-audit`: compare the checked-in Codex architecture with current official
  guidance.

Read-only specialist agents live in `.codex/agents/`. Use only the roles matching the
changed surface: sim architecture, cross-platform parity, persistence, database
performance, server hot-path performance, security, test coverage, frontend, release
malware, and official documentation research. The parent runs deterministic commands once; reviewers inspect
evidence instead of duplicating the full gate.

For SQL, database call sites, schema or indexes, query cadence/cardinality, pool or lock
behavior, timeout policy, background work, database driver/dependency versions, PostgreSQL engine
or resource/configuration/topology changes, or stored-data growth, invoke
`woc_database_performance` before implementation decisions and again on the finished diff.
Pair it with persistence or security review when those concerns also apply.

For server work that runs per tick, per request, per broadcast, per session, or on a
recurring main-thread job (a shared read or cache, a growing collection, a snapshot or event
payload, a `selfWireJson` key or the `src/sim/` read it calls, an autosave or sweep job, a
`world_state` blob write), invoke `woc_server_hot_path`; it owns the non-SQL server budget
and the grown-collection rules in `server/CLAUDE.md` "Hot paths".

## Completion contract

Run checks proportional to the change while iterating. Before calling an implementation
complete, use `$woc-qa` or follow `docs/qa-gate.md`, including the pre-merge bar
`node scripts/gate_select.mjs` (or the deeper `npm run gate`) when the canonical gate
requires it. Report the exact commands and outcomes, remaining risks, and
any checks you could not run. A hook or subagent report never substitutes for the shared
test, typecheck, build, i18n, and security gates.


---
## Verbatim: .claude/settings.json
```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/deny-generated-edit.sh",
            "timeout": 10
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/ensure-hooks.sh",
            "timeout": 10
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/qa-stop.sh",
            "timeout": 30,
            "statusMessage": "QA stop-gate: scanning the diff for forbidden characters and test debris"
          }
        ]
      }
    ]
  }
}
```


---
## Verbatim: .claude/hooks/qa-stop.sh
```bash
#!/usr/bin/env bash
# QA stop-gate for World of ClaudeCraft.
#
# Runs at the end of EVERY Claude Code turn (the Stop hook). It deliberately does only
# instant, near-zero-cost checks on the working tree's uncommitted added lines (the
# tracked diff against HEAD, staged AND unstaged, plus untracked text files), so it never
# slows the edit loop. It NEVER runs tsc, vitest, biome, or the LLM review:
#   - a Stop hook fires on every turn, so heavy checks here would tax every iteration;
#   - a hook is a shell command and cannot spawn the QA agent anyway.
# The heavier deterministic floor (tsc, guard tests, biome) runs once per push in
# .githooks/pre-push; the full multi-agent review is the /qa skill and the qa-checklist
# agent.
#
# What it blocks on (all hard project invariants from CLAUDE.md, all detectable instantly):
#   - em dash, en dash, or emoji anywhere in code, comments, or docs;
#   - a stray ".only(" in a test, which silently disables the rest of that suite;
#   - a leftover "debugger" statement;
#   - a Math.random / Date.now / performance.now call added under src/sim/ (the
#     determinism invariant; tests/architecture.test.ts is the deep guard, this is the
#     instant tripwire; lines that START as comments are skipped).
# On a hit it asks Claude to fix those exact lines before finishing. Otherwise it is silent.
#
# This script is checked in and runs on every contributor's machine. It is intentionally
# small, dependency-light (bash + git + perl, all already required to work on this repo),
# reads only `git diff`, the untracked files git reports, and its own stdin; writes
# nothing, and makes no network calls. See .claude/hooks/README.md.
set -uo pipefail

input=$(cat)

# Loop guard: if we already blocked once this turn, let Claude finish. Tolerant of spacing.
if printf '%s' "$input" | grep -Eq '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
  exit 0
fi

dir="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$dir" 2>/dev/null || exit 0
command -v git >/dev/null 2>&1 || exit 0
command -v perl >/dev/null 2>&1 || exit 0
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

# Added lines in this working tree, across source and docs, excluding locale overlays
# and the Russian doc mirrors (native punctuation such as a real em dash is legitimate
# there; keep this set identical to the copy-scan exclusions in .githooks/pre-push) and
# generated bundles.
pathspec=(
  .
  ':(exclude)src/ui/i18n.locales'
  ':(exclude)tests/fixtures/guide_wiki_audit_fills.ts'
  ':(exclude)src/ui/i18n.resolved.generated'
  ':(exclude)src/admin/i18n.resolved.generated'
  ':(exclude)docs/i18n/*.ru_RU.md'
  ':(exclude)*.lock'
  ':(exclude)package-lock.json'
)

# Tracked modifications (git diff) plus untracked, non-ignored files synthesized as
# all-added, so a brand-new file is scanned too. Untracked files are limited to text
# extensions to skip binaries.
stream=$(
  git diff HEAD -U0 --no-color -- "${pathspec[@]}" 2>/dev/null
  git ls-files --others --exclude-standard -- "${pathspec[@]}" 2>/dev/null \
    | grep -Ei '\.(ts|tsx|mts|cts|js|mjs|cjs|json|md|css|html|ya?ml|sh|svelte|toml|txt)$' \
    | while IFS= read -r f; do
        [ -f "$f" ] || continue
        printf '+++ b/%s\n' "$f"
        sed 's/^/+/' "$f" 2>/dev/null
      done
)
[ -n "$stream" ] || exit 0

out=$(printf '%s' "$stream" | perl -CSD -e '
  my @hits; my $file = "";
  while (my $line = <STDIN>) {
    if ($line =~ m{^\+\+\+\s+b/(.+)$}) { $file = $1; $file =~ s/\s+$//; next; }
    next unless $line =~ /^\+/;
    next if $line =~ /^\+\+\+/;
    my $c = substr($line, 1);
    chomp $c;
    my $cat = "";
    if ($c =~ /[\x{2013}\x{2014}\x{2015}]/) {
      $cat = "em or en dash";
    } elsif ($c =~ /[\x{1F000}-\x{1FAFF}\x{1F1E6}-\x{1F1FF}\x{2600}-\x{27BF}\x{FE0F}]/) {
      $cat = "emoji";
    } elsif (($file =~ /\.test\.(ts|tsx|js|mjs|cjs)$/ || $file =~ m{(^|/)tests/})
             && $c =~ /\b(?:it|test|describe|bench|suite)\.only\s*\(/) {
      $cat = "stray .only( disables the suite";
    } elsif ($file =~ /\.(ts|tsx|js|mjs|cjs)$/ && $c =~ /^\s*debugger\s*;?\s*$/) {
      $cat = "leftover debugger";
    } elsif ($file =~ m{^src/sim/.*\.ts$} && $c !~ m{^\s*(?://|\*|/\*)}
             && $c =~ /\b(?:Math\.random|Date\.now|performance\.now)\s*\(/) {
      $cat = "wall-clock or Math.random in sim code (use Rng and sim time)";
    }
    next unless $cat;
    my $snip = $c; $snip =~ s/^\s+//; $snip =~ s/\s+$//; $snip = substr($snip, 0, 80);
    push @hits, "$file [$cat]: $snip";
    last if @hits >= 20;
  }
  exit 0 unless @hits;
  my $n = scalar @hits;
  my $body = "QA stop-gate blocked: $n line(s) this change added violate a hard project invariant. "
    . "Fix every one before finishing (no em dashes, en dashes, or emojis anywhere; no stray .only() that "
    . "disables a test suite; no leftover debugger statement; no Math.random/Date.now/performance.now "
    . "in src/sim, use Rng and sim time):";
  $body .= "\n- $_" for @hits;
  $body =~ s/([\\"])/\\$1/g;
  $body =~ s/([\x00-\x1f])/sprintf("\\u%04x", ord($1))/ge;
  print "{\"decision\":\"block\",\"reason\":\"$body\"}";
')

if [ -n "$out" ]; then
  printf '%s' "$out"
fi
exit 0
```


---
## Verbatim: .claude/agents/gate-integrity-reviewer.md
---
name: gate-integrity-reviewer
description: >
  QA-gate pipeline reviewer for World of ClaudeCraft. Use on any diff that touches the gate or
  CI plumbing: `scripts/gate*.mjs`, `scripts/lib/gate_*.mjs`, `scripts/lib/ci_*.mjs`,
  `scripts/ci_shard_test.mjs`, `.github/workflows/`, or their pin tests. The selective gate is
  the merge bar, so a selection-semantics bug silently skips tests repo-wide; every check here
  verifies a change fails TOWARD MORE TESTS, never fewer. Read-only - analyzes and reports but
  never modifies files.
tools: Read, Grep, Glob, Bash
model: opus
maxTurns: 20
---

You are the gate-integrity reviewer for World of ClaudeCraft. `node scripts/gate_select.mjs` is
THE pre-merge merge bar (model: `docs/qa-gate.md`; steps: `scripts/lib/gate_steps.mjs`), so a
bug in its selection semantics does not fail a build, it silently stops running tests for the
whole repo. The core principle for every check: when a gate change is ambiguous, it must FAIL
TOWARD MORE TESTS. A change that could only ever run extra tests is safe; a change that could
skip one is the defect class you exist to catch.

**You are read-only. Never edit files or suggest edit commands. Only analyze and report.**

## Scope gate - run this FIRST

1. Get the changed files (cheap): `git diff --name-only` (working tree), else
   `git diff --name-only "$(git merge-base HEAD "$(git rev-parse --abbrev-ref '@{upstream}' 2>/dev/null || echo origin/main)")"..HEAD`.
2. You are IN SCOPE if any changed path matches `scripts/gate*.mjs`, `scripts/lib/gate_*.mjs`,
   `scripts/lib/ci_*.mjs`, `scripts/lib/test_visibility.mjs`, `scripts/ci_shard_test.mjs`,
   anything under `.github/workflows/`, or the pin tests (`tests/ci_workflow.test.ts`,
   `tests/ci_shard_plan.test.ts`, `tests/gate_select_plan.test.ts`,
   `tests/ci_test_select.test.ts`, `tests/nightly_plan.test.ts`).
3. EARLY EXIT: if nothing matched, output exactly this and STOP:

   > **Gate integrity review - out of scope.** No gate or CI pipeline surface in this diff.
   > Nothing to review.

## Checks - apply each, cite file:line

### Check 1 - Visibility classification stays computed, never listed (CRITICAL)

The blind/partial classification in `scripts/lib/test_visibility.mjs` decides which tests are
ALWAYS run because the import graph cannot see their dependencies. Flag any weakening: a test
moved out of the always-run set without a graph-visible replacement, or the classification
turned from recomputed-from-source into a committed list (a list rots toward skipping).

### Check 2 - Widen-to-full triggers preserved (CRITICAL)

The local planner (`scripts/lib/gate_select_plan.mjs`) drops the WHOLE plan to the full suite
for any change it cannot classify: lockfile and `package.json` edits, vitest/vite/tsconfig and
other config, shared test helpers and global setup. The CI arm carries two triggers the local
planner does NOT have: a selection-pipeline self-edit (`SELECTION_PIPELINE_FILES` in
`scripts/lib/ci_test_select.mjs`) and any removed or renamed source/test path both force full
there, while locally a planner self-edit classifies as an ordinary related source and
`scripts/gate_select.mjs` filters deleted paths out of the argv without widening. Know which
arm owns which trigger before flagging; a change that weakens a CI-only trigger is not excused
by the local behavior. Flag any removed or narrowed trigger, any new file class that lands in
a narrow bucket without its own freshness-equivalent argument, and any change that grows the
local arm's silent-drop surface.

### Check 3 - Partitions stay provably complete (CRITICAL)

Shard and lane partitions must cover every test exactly once; the pins in
`tests/ci_shard_plan.test.ts` (and the other pin tests in scope) are updated in the SAME
change as the partition logic. Run the pin tests yourself and report real results:
`npx vitest run tests/gate_select_plan.test.ts tests/ci_shard_plan.test.ts tests/ci_test_select.test.ts tests/ci_workflow.test.ts tests/nightly_plan.test.ts`
(drop files the diff cannot affect).

### Check 4 - Exit codes propagate (CRITICAL)

No test run piped through `tail`/`head` (that masks the exit code), no swallowed subprocess
status, no `process.exit()` that truncates a still-draining log where the existing code
deliberately uses `process.exitCode`. A carried-forward red must stop the gate or be loudly
reported, never averaged away.

### Check 5 - The known-flake retry stays narrow (WARNING)

The ONE sanctioned auto-retry lives in `scripts/lib/ci_leg_runner.mjs`: a leg that exits 1
with the exact teardown-rpc signature (`isTeardownRpcFlake`, `scripts/lib/teardown_rpc_flake.mjs`:
every test passed, failure only in environment teardown) reruns ONCE, loudly. Flag any widened
signature, extra retry budget, retry applied to a leg with real test failures, or a retry that
does not print itself into the job log.

### Check 6 - Silent caps and skips must speak (WARNING)

Every place the pipeline decides to skip, cap, or substitute work (selective vitest step,
artifact-cache hits, worker caps, plan fallbacks) must print that decision in the job log so a
human can audit what did NOT run. Flag any new silent skip path.

## How to work

- Start from the diff; read `docs/qa-gate.md` for the current gate model before judging intent.
- For any selection change, construct the adversarial case: what diff would this change cause
  to run FEWER tests than before? If you can name one, that is a finding.
- Do not run the full gate or `npm test`; targeted pin tests only.

## Output format

Open with a one-line summary and the pin-test results. Then findings, highest severity first:
`[CRITICAL|WARNING|INFO] file:line - what could skip tests -> the adversarial diff that shows
it -> the concrete fix`. End with an explicit per-check PASS/FAIL/N-A line for each of the six
checks so coverage is auditable.

## Delivering your report

The review only counts once the report is DELIVERED. End with the complete report as your final
message, never a status line or a promise to report later. If a SendMessage tool is available
(it is injected when you run as a background teammate), ALSO send the full report (never a
one-line summary) to `main` as your FINAL action; going idle without sending it is a failed
review that costs the orchestrator a nudge round-trip.


---
## Excerpt: docs/qa-gate.md (first 150 lines)
# The QA gate

World of ClaudeCraft uses multiple coding-agent runtimes, but one repository QA
contract. Every layer does one job at the cheapest useful boundary. Claude Code and
Codex have different entry points and share the same deterministic scripts and commands.

## Layers

| Layer | What runs | When | Blocks? |
|---|---|---|---|
| Instant copy gate | `.claude/hooks/qa-stop.sh` through each runtime's Stop hook | End of an agent turn | Yes, on a hard-invariant hit |
| Deterministic floor | `.githooks/pre-push` | Before a push | Yes |
| Day-loop fast path | `npm run gate:fast` through `scripts/gate_fast.mjs` | While iterating (agents and mid/low-tier machines) | No (local only; not merge) |
| **Selective gate** | `node scripts/gate_select.mjs` | **Before implementation is called ready / pre-merge** | **Yes (the merge bar)** |
| Full local gate | `npm run gate` through `scripts/gate.mjs` | When you want the whole suite locally, or the planner falls back | Yes (deeper check) |
| Selective PR-tier CI | ci.yml `pr-gate` shards through `scripts/ci_shard_test.mjs` (same selection semantics, sharded; full suite on any unprovable diff) | Every pull request | Yes (required checks) |
| Merge queue | ci.yml on the `merge_group` event: the full PR tier over the exact merge result about to become the branch tip (see `docs/merge-queue.md`, including rollout status: `release/**` first, `main` at the next release-to-main merge) | Every queued merge into a queue-protected branch | Yes (required checks on the merge group) |
| Nightly full gate | `.github/workflows/nightly.yml`: full suite + checks + browser over the tips of main and the active `release/**` branch | Scheduled nightly (04:47 UTC) | No (alerting: files and closes one tracking issue) |
| Judgment review | Claude `/qa` or Codex `$woc-qa`, plus scoped reviewers | End of a contribution | Advisory locally |

### Instant copy gate

The Stop gate scans the uncommitted added lines (the tracked diff against HEAD, staged
and unstaged, plus untracked text files) for an em dash, en dash, emoji, focused
`.only(` test, leftover `debugger`, or a `Math.random`/`Date.now`/`performance.now`
call added under `src/sim/` (the determinism invariant's instant tripwire). The locale
overlays and `docs/i18n/*.ru_RU.md` are excluded, matching the pre-push copy scan. It
takes milliseconds and never runs TypeScript, Vitest, Biome, browser work, or an agent.
`.claude/settings.json` and `.codex/hooks.json` share the Claude implementation; the
Codex adapter (`.codex/hooks/qa-stop.sh`) delegates to it, then re-scans TOML and
`.mts`/`.cts` module files (the shared filter now covers those itself, so the adapter's
extra pass is a harmless belt). A companion `PreToolUse` hook
(`.claude/hooks/deny-generated-edit.sh`) blocks direct agent edits to generated
artifacts (`*.generated.ts`, the `i18n.resolved.generated/` bundles) at the tool-call
boundary.

### Deterministic floor

`.githooks/pre-push` runs the heavier fast checks at the push boundary: TypeScript,
determinism and purity guards, i18n matcher guards, Biome on changed files, and copy
checks over the push diff. The shared `.claude/hooks/ensure-hooks.sh` idempotently points
`core.hooksPath` at `.githooks`; both agent runtimes call it at session start.

`git push --no-verify` remains an emergency bypass, not a substitute for reporting and
fixing a red gate.

### Day-loop fast path (`gate:fast`)

`npm run gate:fast` is a **high-signal subset** for agent and day-to-day loops. It is
**not** the merge contract and does **not** replace `npm run gate`.

It runs, in order:

1. Malware gate (`security:gate`, typically a few seconds)
2. Biome on changed files (`ci:changed`)
3. Determinism / purity and i18n-matcher guards (`tests/architecture.test.ts`,
   `tests/localization_fixes.test.ts`)
4. Incremental TypeScript check (`check:ts` only; not admin `svelte-check`)
5. Vitest for changed code: `vitest related` on working-tree source files plus any
   changed test files (`--passWithNoTests`). `package.json` / vite config dirtiness is
   **not** expanded through `vitest --changed` (that would re-run nearly the full suite).

It deliberately skips full unsharded vitest, browser regressions, SFX conformance,
i18n generate/freshness, wiki content, and env/server/client builds. Those stay on the
full gate. Vitest workers still use `computeGateWorkers` (CPU/2 and available-memory clamp;
the sensor is `scripts/lib/gate_memory.mjs`, which reads `vm_stat` on macOS because
`os.freemem()` under-reports availability there).
Optional `GATE_WORKER_TIER=low|medium|high` caps workers after that clamp; see
[`docs/local-gate-perf/tier-workers.md`](local-gate-perf/tier-workers.md). Opt in to
branch-wide `vitest --changed <ref>` with `GATE_FAST_BASE=<ref>` when you deliberately
want that broader (and slower) selection. **Which command for your tier / agent vs
human:** [`docs/local-gate-perf/platform-matrix.md`](local-gate-perf/platform-matrix.md)
(macOS verified; Linux smoke via CI; Windows smoke until a host fills the matrix).

For a narrower loop without malware/biome/types, use the thin wrappers (same Vitest CLI;
not a merge bar):

```bash
npm run test:related -- path/to/changed.ts   # vitest related --run --passWithNoTests
npm run test:changed                         # vitest run --changed (uncommitted)
npm run test:changed -- origin/release/v0.34.0
```

`test:changed` expands almost to the full suite when `package.json` or `vite.config.ts`
is dirty (same reason `gate:fast` skips those paths for related expansion). Prefer
`test:related` with explicit sources, or `gate:fast`, for day-to-day work. Vitest
`experimental.fsModuleCache` is on in `vite.config.ts` so warm re-runs reuse module
transforms under `node_modules/.experimental-vitest-cache` (clear with
`npx vitest --clearCache` if a warm run looks wrong). The same store is persisted
across CI runs since Phase 4 of the CI/CD performance packet: the pr-gate and
release-gate shard jobs carry an `actions/cache` step for it, keyed per shard, and the
two long-sims lane jobs carry the same step keyed per lane half (Phase 6, the recorded
Phase 4 rider), all over the node_modules-layout inputs (lockfile, vite config, `.npmrc`,
`package.json`), with the design constraints written on the pr-gate copy of the step in
`.github/workflows/ci.yml` and pinned by `tests/ci_workflow.test.ts`. The nightly gate deliberately stays cold: it is the
uncached full replay. Most DOM-environment unit
tests use `// @vitest-environment happy-dom`; a short exception list still pins
`jsdom` where happy-dom API gaps bite (see `docs/local-gate-perf/baselines.md`
Phase 5). Default environment remains `node`.

### Full local gate

`npm run gate` (or `pnpm run gate`) is the **full CI mirror, the deeper check behind the
selective merge bar** (`gate:select`, below, is the bar itself). It mirrors CI:
generated i18n and build-manifest freshness, malware scanning, changed-file formatting, the SFX conformance
check, the full test suite, the browser regression suite (`npm run test:browser`, which
drives Chromium through Playwright), the typecheck, and env, server, bot, and client
builds. Release branches use the release i18n tier. It stops at the first failure and
bounds Vitest workers to avoid load flakes on shared machines. It resolves FFmpeg
(`ffmpeg` and `ffprobe`) from the bundled `ffmpeg-static`/`ffprobe-static` npm packages,
falling back to PATH, and refuses to run when neither source yields a working binary.

**Full-suite lock across concurrent gates (issue #2808):** per-process worker sizing
protects a gate run from itself, but does nothing when a second `npm run gate` is
running in a sibling worktree, which this repo's own per-task-worktree workflow makes
routine; two gates that each correctly claim half the cores still request the whole
machine between them. `gate.mjs` acquires an advisory lock (`scripts/lib/gate_lock.mjs`,
an exclusive loopback listener shared by every worktree on the host) around the
`vitest (full suite)` step only, never the rest of the run. The kernel's atomic listener
ownership admits one gate at a time and disappears with its process, so recovery never
deletes a raced lock file or trusts a reusable pid. A gate that finds the listener held
waits and prints who holds it; a non-gate service on the reserved port is identified and
bypassed rather than blocking local work. The locked npm/Vitest step runs in a managed
child process group, so handled termination tears down the active workload before
releasing ownership. `GATE_NO_LOCK=1` restores fully concurrent behavior for a user who
deliberately wants two full suites running at once.
`gate_select.mjs`/`gate_fast.mjs` never touch this lock; it exists for the one step
that is actually the shared-host bottleneck.

**Task cache (Turborepo):** pure artifact steps (`i18n:gen`, `wiki:content`, `sfx:check`,
`check:types`, `build:env`, `build:server`, `build:bot`, `build:bundle`) run through `turbo run`
(the gate spawns the `node_modules/.bin/turbo` binary directly)
with inputs/outputs in root `turbo.json`. A warm second gate on an unchanged tree
replays those steps from `.turbo/` (often under a second). Full vitest, browser tests,
malware, changed-file Biome, and the i18n freshness `git diff` always run (they are not
cached as "passed"). Catalog edits under `src/ui/i18n.catalog/**` invalidate `i18n:gen`.
Contributor detail: [`docs/local-gate-perf/task-cache.md`](local-gate-perf/task-cache.md).

Use this command instead of an ad hoc shell pipeline whenever you want the whole suite
locally; the pre-merge bar itself is the selective gate (next section). Piping a test
run can hide its exit status, and unconstrained full-suite parallelism can make healthy
heavy sim tests flake. Day-loop iteration may use `npm run gate:fast`; a green fast path
alone is never enough to claim done.

### Selective gate (`gate:select`)

`node scripts/gate_select.mjs` is **the merge bar** (owner decision, 2026-08-05; recorded in
`docs/local-gate-perf/state.md`). `npm run gate` remains the deeper check. The one-line
difference from the other paths:

