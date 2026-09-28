# Legends of Future Past — 1992 commercial MUD resurrected from surviving scripts/manuals with Claude Code ("a weekend")

- Repo: https://github.com/jonradoff/lofp  (live: https://lofp.metavert.io ; write-up: https://meditations.metavert.io/p/resurrecting-a-1992-mud-with-agentic)
- Stars: 180. 118 commits, 2026-04-03 → 2026-05-17. Author: Jon Radoff (original 1992 creator).
- Tool/model: Claude Code.
- Genre: multiplayer text MUD (2,000+ rooms, 8 races, 5 magic schools, psionics, crafting, alchemy), Go + MongoDB backend, React frontend, multi-machine Fly.io deploy, bot agents spec.
- Result evidence: live public server; README: original took 6 months to code, "came back to life in a weekend of agentic engineering"; listed in awesome-ai-built-games. Author is a credible industry figure.
- One-shot vs multi-session: multi-session ("iterative archaeological dig"), core in a weekend, then ~6 weeks of refinement.
- WHY IT MATTERS: the "spec" is not a GDD but **ground-truth artifacts**: 333 original .SCR content scripts (every room/item/monster), GM manual, GM scripting guide, player manual, and a **1996 session capture log** used as golden output for combat message format and formulas. Mechanics were inferred by cross-referencing monster stat ranges with the capture. Same pattern as archer-wars' research dossier: executable-grade reference beats prose description.
- Notable process practices:
  - CLAUDE.md "Reference Documentation" table with a rule: "When implementing new features, always cross-reference these documents and the session capture to match original behavior." Original scripts are read-only reference.
  - Per-unit CLAUDE.md files (engine/, frontend/, original/) + orchestrator CLAUDE.md at root; "Read VIBECTL.md for current project status ... before starting work" (external status/handoff file managed by vibectl tool).
  - Invariant rules learned from incidents: all mutable world state must go through the MongoDB hub or multi-machine players desync; exact deploy command pattern with explanation of why the naive one silently fails (Bash tool doesn't persist env vars) + a post-deploy verification command.
  - Failure anecdotes in README useful for research: misreading MLIST third field as max count → 3,000+ monsters spawned; DOS case-insensitive filenames broke room 592 silently on Linux.

---
## Verbatim: README "How We Brought It Back"
## How We Brought It Back

The source code for the game engine is gone — lost over the years across many computer changes and projects. But several former gamemasters, especially David Goodman, had kept copies of the game's script files. This is important: while the engine code is lost, these script files *are* the actual game content. Every room, item, monster, spell, quest trigger, and NPC interaction in the original game was defined in these scripts using a custom scripting language. The world data is authentic — this isn't a reimagining or a recreation from memory, it's the same content players experienced in the 1990s, now running on a new engine. Along with the scripts, we had the GM manual, player documentation, a scripting reference guide, and — crucially — a session capture log from 1996 that recorded actual gameplay with full combat output.

I used [Claude Code](https://claude.ai/claude-code) to reconstruct the game from these artifacts. The process was genuinely collaborative — not just "write me a game," but an iterative archaeological dig through decades-old files. Here's what that looked like:

**Reverse-engineering the script language.** The game world is defined in hundreds of `.SCR` files using a custom language with commands like `IFVAR`, `IFPREVERB`, `ECHO`, `MOVE`, and `CLEARVERB`. There's no formal specification — just a GM scripting guide written in 1998 and the scripts themselves. Claude Code parsed the language by reading the documentation, examining real script files, and handling edge cases like implicit `ENDIF` blocks and the `ELSE` keyword (which turned out to be critical for temple doorway puzzles).

**Matching original combat output.** The 1996 session capture was invaluable. It showed the exact format of combat messages: `[ToHit: 5, Roll: 31] Hit!` followed by `Puny slash to head. [14 Damage]`. From this, we could determine that ToHit is a d100 threshold (low = easy to hit), that damage has severity tiers (Puny through Dazzling), and that weapon types determine the attack verb (swings for swords, thrusts for polearms, slashes for claws). We also discovered weapon clash mechanics (`[Strength: 57, 2d100 Roll: 26]`) and the `[Round: 5 sec]` roundtime format.

**Reconstructing game mechanics from monster stats.** The script files define monster attributes like `ATTACK1 280`, `DEFENSE 200`, `BODY 250`, `STRATEGY 501`, and `SPEED 2`. By looking at the ranges across hundreds of monsters and cross-referencing with the combat capture, we could infer the formulas connecting attack ratings to hit chances and damage output. The `STRATEGY` field turned out to encode seven distinct AI behaviors, from "non-hostile, flee when attacked" (1-100) to "hostile, fight to the death" (501-700).

**Discovering systems from documentation fragments.** The alchemy system came from a file called `alchemy.bin` that turned out to be a plain-text recipe grid written by a player in 1995. The skill build-point costs came from `skills.txt`. The XP progression table came from the last page of the GM manual. Monster spawning rules were reverse-engineered from `MLIST` entries in the scripts — we initially misinterpreted the format as min/max counts, which caused 3,000+ monsters to spawn at once, before realizing the third field was a probability percentage.

**Handling DOS-era quirks.** The original game ran on MS-DOS, which is case-insensitive. Some script filenames were stored in git with different case than the `LEGENDS.CFG` references. This worked fine on macOS but broke silently on Linux Docker builds — the Temple of Amilor (room 592) was missing in production for this reason. We added case-insensitive file resolution to the script loader.

## Why Release This?


---
## Verbatim: CLAUDE.md (root orchestrator)
Read VIBECTL.md for current project status, deployment details, and issue context before starting work.

# LoFP — Legends of Future Past

Resurrecting a 1990s MUD from original script files. The original game engine source code is lost; only the content scripts and documentation survive. We reverse-engineer a working game from those.

## Architecture

- **Backend**: Go + gorilla/mux + MongoDB at `engine/`
- **Frontend**: React 19 + TypeScript + Vite + Tailwind 4 at `frontend/`
- **Original Scripts**: `original/scripts/` (read-only reference, 333 .SCR files)
- Frontend dev server: port 4992, Backend server: port 4993
- Start both: `./start.sh`

## Build Check

```sh
cd engine && go build ./...
cd frontend && npx tsc --noEmit
```

## Reference Documentation

These original documents are the primary sources for game mechanics and world data:

| Document | Path | Description |
|----------|------|-------------|
| GM Manual | `original/GM Pages/MANUAL.DOC` | Comprehensive GM reference: combat, stats, items, monsters, skills, XP tables, all GM commands |
| GM Script Guide | `original/GMSCRIPT.DOC` | Script language reference: room/item/monster definitions, IFVERB/IFENTRY/IFSAY blocks, variables |
| Player Manual | `original/legends/LEGENDS.DOC` | Player-facing docs: commands, spells, psionics, skills, races, crafting |
| Session Capture | `original/legends/shirla.cap` | 1996 gameplay session capture — invaluable for combat output format, spell interactions, original message text |
| Script Config | `original/scripts/LEGENDS.CFG` | Master config listing all .SCR files to load in order |
| GM Pages | `original/GM Pages/` | Additional GM reference materials (various .DOC files) |

When implementing new features, always cross-reference these documents and the session capture to match original behavior.

## Multi-Machine Coordination

Production runs multiple Fly.io machines. ALL mutable world state must be coordinated via the MongoDB-backed hub (`engine/internal/hub/`):

- **Messages**: broadcasts, whispers, global announcements → published to `events` collection, delivered via Change Streams
- **Player presence**: WHO list, room occupancy → `presence` collection with TTL heartbeat
- **Room state changes**: item open/close/lock, item drops/pickups, script mutations (vals, itembits) → `room_state_change` events via hub
- **Any new mutable state** added to rooms, items, or global data MUST call `notifyRoomChange()` or publish through the hub, or players on different machines will see inconsistent worlds

## After Server Changes

After making changes to the backend (engine/), restart the Go server:
```sh
kill $(lsof -ti:4993) 2>/dev/null; sleep 1; cd engine && go run cmd/lofp/main.go &
```
Load .env first if needed: `source .env`

## Deploying to Production

**CRITICAL: The Google Client ID MUST be passed as a build arg or Google login will break.**

The frontend uses `VITE_GOOGLE_CLIENT_ID` at build time (baked into the JS bundle by Vite). If it's missing, the "Sign in with Google" button disappears and users see "Authentication Not Configured".

### Deploy command (always use this exact pattern):
```sh
GCID=$(grep GOOGLE_CLIENT_ID .env | cut -d= -f2) && fly deploy --build-arg "VITE_GOOGLE_CLIENT_ID=$GCID"
```

**Why this specific pattern?** The Bash tool's shell does not persist exported variables between commands. `source .env && fly deploy --build-arg VITE_GOOGLE_CLIENT_ID=$GOOGLE_CLIENT_ID` silently passes an empty string because `source` sets but does not export the variable, and the Bash tool may run commands in separate shell contexts. Using `grep | cut` directly extracts the value inline, which is reliable.

If using `--no-cache` to force a fresh build, append it:
```sh
GCID=$(grep GOOGLE_CLIENT_ID .env | cut -d= -f2) && fly deploy --build-arg "VITE_GOOGLE_CLIENT_ID=$GCID" --no-cache
```

### After deploying, verify Google login:
```sh
fly ssh console -a lofp -C "grep -c 718491 /app/static/assets/index-*.js"
```
This should return `1`. If it returns `0`, the build arg was not passed correctly.

### Local dev vs. production:
- **Local**: `.env` file at project root contains `GOOGLE_CLIENT_ID=...` (among other secrets). Vite reads `VITE_GOOGLE_CLIENT_ID` from the environment when running `npm run dev`.
- **Production**: Fly.io secrets store `MONGODB_URI`, `JWT_SECRET`, `RESEND_API_KEY`, `SSH_HOST_KEY` (set via `fly secrets set`). The Google Client ID is NOT a Fly secret — it's a **build arg** because Vite needs it at build time, not runtime.
- **Never commit `.env`** — it contains production secrets. It is in `.gitignore`.

## MUD Client Protocols

Reference: https://wiki.mudlet.org/w/Manual:Supported_Protocols

Telnet server (`engine/internal/api/telnet.go`) implements these protocols:

### GMCP (option 201)
- **Core.Hello** — sent on connect: `{"client":"LoFP","version":"11.5.0"}`
- **Core.Supports.Set** — handled from client to track subscribed packages
- **Char.Vitals** — sent after every command: `bp`, `maxbp`, `mana`, `maxmana`, `psi`, `maxpsi`, `fatigue`, `maxfatigue`, `position`, `conditions`
- **Char.Status** — sent on login: `name`, `fullname`, `race`, `gender`, `level`, `experience`, `gold`, `silver`, `copper`
- **Char.Stats** — sent on login: `strength`, `agility`, `quickness`, `constitution`, `perception`, `willpower`, `empathy`
- **Room.Info** — sent on every room change (powers Mudlet automapper): `num` (int), `name` (string), `area` (string), `environment` (string), `exits` (map direction→room number)

### MXP (option 91)
- Line mode `\033[1z` = secure line (allows `<send>` tags until newline). NOT `\033[4z`.
- Used for clickable exits: `\033[1z<send href="north">north</send>, <send href="east">east</send>`
- `<send>` is a SECURE tag — only works in secure line mode (`\033[1z`)
- MXP output is gated on `tc.mxpEnabled` — plain clients see normal text

### MCCP2 (option 86)
- After negotiation, sends `IAC SB 86 IAC SE` uncompressed, then ALL subsequent output goes through zlib
- **IMPORTANT**: When MCCP2 is active, ALL data including IAC sequences (like WILL ECHO for password mode) MUST go through `t.write()` (the compressor), NOT `t.conn.Write()` (raw). Sending raw bytes corrupts the zlib stream and causes Mudlet to disconnect.

### MSSP (option 70)
- Sends game metadata (name, player count, website, genre, etc.) for MUD directory crawlers

### MSDP (option 69)
- Variable reporting for TinTin++ compatibility
- Handles REPORT subscriptions, pushes CHARACTER_NAME, HEALTH, MANA, ROOM, etc.

### Password Echo Suppression
- `WILL ECHO` / `WONT ECHO` toggle for password fields
- Must be sent through the compressor when MCCP2 is active
- `enterPasswordMode()` before prompt, `exitPasswordMode()` after reading

### NAWS (option 31)
- Window size negotiation, updates `t.width` for `wordWrap()`

## Script Language

The game world is defined in a custom scripting language (documented in `original/GMSCRIPT.DOC`):
- **Rooms**: `NUMBER`, `NAME`, `*DESCRIPTION_START/END`, `EXIT`, `ITEM`, terrain, lighting
- **Items**: `INUMBER`, `NAME` (noun ref), type, weight, volume, substance, worn slots
- **Monsters**: `MNUMBER`, body parts, stats, AI strategy, weapons, spells
- **Events**: `IFVERB/IFPREVERB/IFSAY/IFENTRY/IFVAR...ENDIF` conditional blocks
- **Variables**: Named variables + internal vars (stats, time, flags, item vals)
- Config file: `original/scripts/LEGENDS.CFG` lists all scripts to load in order

## Current State (v11.5)

- Script parser loads 2273+ rooms, 1990+ items, 297 monsters with case-insensitive file loading
- Full combat system: original [ToHit/Roll] format, weapon crits/slayers, fatigue, weapon clash
- 60+ spells across 5 schools, 30+ psionic disciplines
- Complete crafting: mining, smelting, forging, weaving, dyeing, foraging, alchemy (32 recipes)
- 36 skills with build point costs, prerequisites, and mechanical effects
- Treasure system: coin drops, weapon/armor/scroll/chest drops scaled by monster TREASURE level
- Monster AI: hostile aggro, flee behavior, special attacks, guard, demand-based spawning
- ELSE branches in script conditionals, all portal types supported
- 150+ emotes, race-specific, submit-gated interactions
- Character soft-delete with admin recovery, unique first names
- Security: rate limiting, connection caps, chat flood protection, HTML sanitization
- WebSocket-based real-time multiplayer
- Admin panel for rooms/items/monsters/players/logs
- Feedback pipeline: REPORT command forwards to VibeCtl for triage and issue tracking
- Production: Fly.io (1 machine, ord region) at lofp.metavert.io
  - Single machine to avoid multi-machine state desync (monsters, combat, player visibility)
  - Scale to 2+ machines only after implementing full hub-based monster/combat coordination

## Units

| Unit | Code | Path | Description |
|------|------|------|-------------|
| Engine | ENG | `engine` | Go backend: script parser, game engine, command interpreter, MongoDB persistence |
| Frontend | FRONT | `frontend` | React + Tailwind: player UI (text client) and admin interface |
| Scripts | SCR | `original` | Original game script files and documentation (read-only reference) |


---
## Verbatim: engine/CLAUDE.md
Read VIBECTL.md for current project status, deployment details, and issue context before starting work.

# Engine

Go backend: script parser, game engine, command interpreter, MongoDB persistence

This is a unit of the **LoFP** project.

## Sibling Units

- **Frontend** (`frontend`) — React + Tailwind: player UI (text client) and admin interface
- **Scripts** (`original`) — Original game script files and documentation (read-only reference)

The orchestrator CLAUDE.md at the project root (`/Users/jonradoff/lofp/CLAUDE.md`) coordinates cross-unit concerns.


---
## Verbatim: frontend/public/bot-agent-spec.md
# Legends of Future Past — Bot Agent Specification

> Machine-readable specification for AI agents connecting to the game.

## Endpoint

```
wss://lofp.metavert.io/ws/game
```

## Authentication

Send after WebSocket connection opens:

```json
{"type": "auth_apikey", "data": {"key": "<your_api_key>"}}
```

Response:
```json
{"type": "auth_result", "data": {"success": true, "character": "CharacterName"}}
```

On failure: `{"type": "auth_result", "data": {"success": false, "error": "invalid API key"}}`

## Sending Commands

```json
{"type": "command", "data": {"input": "<game_command>"}}
```

Examples:
- `{"type": "command", "data": {"input": "look"}}` — examine surroundings
- `{"type": "command", "data": {"input": "go north"}}` — move north
- `{"type": "command", "data": {"input": "attack skeleton"}}` — attack a monster
- `{"type": "command", "data": {"input": "say Hello!"}}` — speak in room
- `{"type": "command", "data": {"input": "inventory"}}` — list carried items
- `{"type": "command", "data": {"input": "status"}}` — show character stats
- `{"type": "command", "data": {"input": "skills"}}` — show trained skills
- `{"type": "command", "data": {"input": "exp"}}` — show experience progress

## Receiving Messages

### type: "result"
Response to your command. Fields:

| Field | Type | Description |
|-------|------|-------------|
| messages | string[] | Lines of text output |
| roomName | string | Room name (e.g., "[City Gate]") |
| roomDesc | string | Room description text |
| exits | string[] | Available exit directions |
| items | string[] | Visible items in room |
| error | string | Error message if any |
| quit | boolean | True if session ended |
| promptIndicators | string | Status codes (see below) |
| playerState | object | Character state (see below) |

### type: "broadcast"
Messages from other players, monsters, or world events in your room.

| Field | Type | Description |
|-------|------|-------------|
| messages | string[] | Lines of broadcast text |

## Player State Object

Included in results when state changes:

```json
{
  "firstName": "BotName",
  "lastName": "LastName",
  "race": 1,
  "level": 5,
  "bodyPoints": 42,
  "maxBodyPoints": 50,
  "mana": 10,
  "maxMana": 15,
  "psi": 8,
  "maxPsi": 10,
  "fatigue": 30,
  "maxFatigue": 35,
  "experience": 5000,
  "gold": 10,
  "silver": 5,
  "copper": 23,
  "position": 0,
  "dead": false,
  "bleeding": false,
  "stunned": false,
  "poisoned": false
}
```

Position values: 0=standing, 1=sitting, 2=laying, 3=kneeling

## Prompt Indicators

The `promptIndicators` string contains single-character status codes:

| Char | Meaning |
|------|---------|
| ! | Bleeding |
| s | Sitting |
| S | Stunned |
| D | Diseased |
| P | Poisoned |
| J | In combat (joined) |
| K | Kneeling |
| L | Laying down |
| R | Roundtime active |
| H | Hidden |
| U | Unconscious |
| I | Immobilized |
| DEAD | Dead |

## Common Commands

### Navigation
- `look` — describe current room
- `go <direction>` — move (north, south, east, west, up, down, out, or portal name)
- `n`, `s`, `e`, `w`, `ne`, `nw`, `se`, `sw`, `u`, `d`, `o` — direction shortcuts

### Combat
- `attack <target>` or `kill <target>` — attack a monster
- `flee` — escape combat
- `offensive` / `defensive` / `wary` / `normal` — change combat stance

### Magic
- `prepare <spell>` — prepare a spell
- `cast [target]` — release prepared spell

### Psionics
- `psi <discipline>` — prepare a discipline
- `project [target]` — project prepared discipline

### Items
- `get <item>` — pick up item
- `drop <item>` — drop item
- `inventory` — list carried items
- `wield <weapon>` — equip weapon
- `wear <armor>` — put on armor

### Information
- `status` — full character stats
- `health` — body point summary
- `skills` — trained skills list
- `exp` — experience and level progress
- `who` — list online players
- `wealth` — currency summary

### Communication
- `say <message>` or `'<message>` — speak in room
- `yell <message>` — shout
- `whisper <player> <message>` — private message
- `think <message>` — telepathy broadcast

### Crafting
- `mine` — mine ore (in mine rooms)
- `forage` — forage materials (outdoor)
- `smelt` — refine ore at forge
- `craft <item>` — craft at workshop
- `brew <reagent> in <flask>` — alchemy

## Rate Limits

- Burst: maximum 4 commands per second
- Sustained: maximum 10 commands per 10 seconds
- Maximum 5 broadcast messages (say/yell/act) per 10 seconds
- Exceeding limits returns: `[Slow down! Too many commands.]`

## Bot Identification

- Bots appear on the WHO list with `[Bot]` suffix
- Bots follow all normal game rules (combat, death, roundtime, etc.)
- GM commands require explicit permission set during API key generation
