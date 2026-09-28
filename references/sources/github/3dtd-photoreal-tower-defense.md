# 3DTD — tower defense on real streets (Google Photorealistic 3D Tiles), co-op lockstep, Claude Code-assisted (mixed authorship)

- Repo: https://github.com/ingel81/3dtd  (project page https://3dtd.sgeht.net, browser build /play/, Windows/Linux desktop releases, YouTube co-op best-of 15 min + walkthrough)
- Stars: 9. 2,579 commits, 2026-01-09 → 2026-09-27 (ongoing, ~9 months).
- Tool/model: Claude Code (CLAUDE.md, .claude/commands/*, plans in ~/.claude/plans, "Claude-Designer", "Review-Agent", "Code Review ... (12 Agenten)", branch `claude/3d-engine-performance-analysis-*`). Handover doc states authors are "partly ingel81 (by hand), partly Claude". So: AI-heavy but NOT 100% AI.
- Genre: 3D tower defense on photoreal city tiles (OSM roads as enemy routes), heroes, research tree, adaptive wave director, 2–4 player co-op lockstep with relay, Electron desktop app with auto-update.
- Result evidence: strongest "real game" evidence in the set — shipping installers, CI badges, public videos of 38-wave co-op match. README: "It runs, it's playable, and it is nowhere near finished."
- One-shot vs multi-session: very long multi-session. No up-front GDD preserved; spec lives as docs/game-design/MASTER_GAME_DESIGN.md + ~40 subsystem docs indexed by docs/INDEX.md.
- Notable process practices:
  - CLAUDE.md "mandatory reading per task" table (task → doc) + docs/INDEX.md with status of every doc.
  - TODO.md = the ONLY backlog, stable IDs (A1, C16, E27…), plus "Decided" and "Rejected" sections; DONE.md = dated changelog. Items move TODO→DONE **only on human say-so**.
  - docs/PLAYTEST.md = queue of "re-tests awaiting human eyes": each fix built by the agent gets a numbered playtest item with explicit expectation; human replies "K2.1 ok, K3.4 broken" and result is appended. Division of labor stated explicitly: "Logic is checked by the lead via scenario tests; this list is only for eyes, ears and real maps. What a browser can check, the E2E tests check."
  - Bot playtesting at scale: Python bot-server + dashboard + N headless Chrome tabs running a StrategyBot vs the wave director in a seeded offline "DevWorld" (loads <1 s, no network), JSONL logs, run-report.html. `/bots` slash command starts/monitors the whole stack; balance changes are measured on bot runs, "feel" on human runs.
  - DevWorld: deterministic seeded offline test world — key enabler for fast agent iteration without paid tile API.
  - Guardrails: no `npm start` / no commits without command, no Co-Authored-By, never commit API keys.
  - Slash commands: /addnewtodo (dedupe into right category), /readdocsandtodos (propose next step as a wizard), /buildlint (build+lint, report only errors), /bots, /release, /commit.

---
## Verbatim: CLAUDE.md
# CLAUDE.md - 3DTD

## Projekt

3DTD - Standalone Tower Defense auf Google Photorealistic 3D Tiles (über Cesium Ion oder die Google Maps API)

## Befehle

```bash
npm start       # Development Server (http://localhost:4200)
npm run build   # Production Build
npm test        # vitest
npm run lint
npm run e2e     # End-to-End-Tests im Browser (Dev-Server muss laufen, docs/E2E.md)
npm run coop-server  # Coop-Relay (:3003), docs/COOP_PLAN.md
```

## Architektur

- Angular 22 Standalone Components (nur UI)
- Three.js + 3DTilesRendererJS für 3D-Rendering
- **Event-driven Game Engine** - Manager kommunizieren via GameEventBus
- **Signal Store** - 6 Sub-Stores als Single Source of Truth (Game, UI, Engine, Location, Research, Debug)
- Kein Backend im Spiel-Client - komplett clientseitig (`bot-server/` nur für Bot-Läufe)
- **Wellenquellen sind austauschbar** (`director/wave-source.ts`, ein Unterordner je Variante unter
  `director/sources/`, Standard in `configs/director.config.ts`). Der adaptive Source ist regelbasiert und
  läuft ohne Server und ohne Modell, der Tabellen-Source spielt eine editierbare Liste. Rahmen in
  [WAVE_SOURCE_PLAN.md](docs/WAVE_SOURCE_PLAN.md), der adaptive in
  [WAVE_DIRECTOR.md](docs/WAVE_DIRECTOR.md), Umbau in [BALANCING_PLAN.md](docs/BALANCING_PLAN.md)
- Tile-Zugang: Cesium-Ion-Token (Standard) oder Google-Maps-Key. `ConfigService` liest ihn aus drei Quellen, die
  spätere gewinnt: `environment.ts` (Vorlage `environment.template.ts`), `public/runtime-config.json`, Token-Dialog
  (localStorage `3dtd-tile-credentials`)

## Projektstruktur

```
src/app/
├── app.ts                      # Root Component (AppComponent)
├── app.config.ts               # Provider Config
├── app.routes.ts               # Routing
├── tower-defense.component.*   # Haupt-Spielkomponente (.ts, .html, .scss)
├── bots/                       # Bot System (Strategy Pattern), Bot-Session, WebSocket-Client
│   ├── bots/                   # StrategyBot, Factory
│   └── strategies/             # Placement, Upgrade, Wave, Research, Ability, Hero Strategies
├── director/                   # Wellenquellen: Vertrag (wave-source.ts), WaveDirector, Templates,
│                               # Snapshot, Verteidigungsanalyse; sources/adaptive + sources/table
├── game-engine/                # Event Bus, VFX/Audio/BackgroundMusic/ScreenShake Services (Three.js-coupled, Angular-frei)
├── coop/                       # Coop: Lockstep, Relay-Protokoll, Weltpaket, Prüfsummen, Raum-Optionen (docs/COOP_PLAN.md)
├── components/                 # UI Components (compass, game-header, game-sidebar, etc.)
├── configs/                    # Tower/Enemy/Projectile/Combat/Research/Audio + Kampagne (campaign.config.ts)
├── core/                       # GameObject/Component-Basis, ConfigService
├── devworld/                   # DevWorld Offline-Entwicklungsumgebung
├── entities/                   # Enemy, Tower, Projectile (+ tower-targeting.util, enemy-rush)
├── game-components/            # ECS Components (transform, health, movement, combat, etc.)
├── integration/                # Cross-System Integration-Tests
├── interfaces/                 # Provider-Interfaces (StreetNetwork, Terrain)
├── managers/                   # Manager (Enemy, Tower, Wave, Research, Ability, Hero usw., event-driven), game-state/ (Ledger, Lifecycle, Clock), worm/, audio/ (Spatial Audio)
├── models/                     # Type Definitions (game.types, location.types, status-effects)
├── replay/                     # Replay-Leiste: Marken, Zeitformat (docs/REPLAY.md)
├── run-log/                    # Run-Log: Sammler, Speicher, Export, Game-Over-Zahlen (docs/RUN_LOG.md)
├── simulator/                  # Snapshot, Prüfsumme, Neu-Simulation, Replay-Session, Replay-Datei (docs/SIMULATOR_PLAN.md)
├── services/                   # Angular Services (Subfolders: combat/, debug/, facade/, infrastructure/, location/, onboarding/, world/)
├── store/                      # Signal Stores (Game, UI, Engine, Location, Research, Debug)
├── styles/                     # Theme-Tokens (td-theme.ts)
├── three-engine/               # 3D Rendering: Engine, CameraRig, Tiles, renderers/ (inkl. Shader), post-processing/
├── utils/                      # Shared Utilities (geo-utils, damage-calculator, global-route-grid, route-corridor, game-rng)
└── workers/                    # Web Worker: Heartbeat für den Loop im versteckten Tab

bot-server/                     # Python Bot-Server (nur für Bot-Läufe, plant keine Wellen)
├── server.py                   # WebSocket Server (:3001): Clients, Wellen-Log, Fernbedienung
├── manage_server.py            # Start/Stop/Status als Hintergrundprozess
├── config.py                   # Ports, Bot-Gewichte
├── utils/logger.py             # Console + JSONL-Logging (logs/bots_*.jsonl)
├── dashboard/                  # Web Dashboard (:3002): wer läuft, Knöpfe, Fehler
├── analyze_runs.py, analysis/  # Auswertung der Läufe (run-report.html)
├── tests/                      # pytest (Analyse, Bot-Log)
├── requirements.txt            # Python-Abhängigkeiten
└── start.bat / start.sh        # Start-Skripte (Windows, Unix)

coop-server/                    # Node-Relay für Coop (npm run coop-server, :3003), Einstieg der Desktop-App (desktop.ts)
desktop/                        # Electron-App: Installer, Auto-Update, LAN-Relay und LAN-Suche (docs/ELECTRON_DESKTOP_PLAN.md)
e2e/                            # Playwright-Tests des Dev-Spiels (docs/E2E.md)
tools/                          # Charts, Modell-Budget, Shader-Check, Blender-Skripte, Build-Info, Relay-Last
landing/                        # Projektseite
```

## Wichtig

- **Kein `npm start` ohne Befehl**
- **Keine Commits ohne Befehl**
- **Keine Co-Authored-By Zeile in Commits**
- **API Keys nie committen** (environment.ts ist in .gitignore)

## Dokumentation

**Pflichtlektüre je nach Aufgabe!** Alle weiteren Dokumente (Features wie Fähigkeiten, Held, Replay, Audio,
Partikel; Game Design und Balance; Berichte und Sprint-Handover; Pläne; Archiv) listet
[docs/INDEX.md](docs/INDEX.md) mit Status und Schnellnavigation.

| Aufgabe | Pflichtlektüre |
|---------|----------------|
| Einstieg, Gesamtarchitektur | [ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Manager und Events | [EVENT_SYSTEM.md](docs/EVENT_SYSTEM.md) |
| State, Stores, Facades | [SIGNAL-STORE-ARCHITECTURE.md](docs/SIGNAL-STORE-ARCHITECTURE.md) |
| UI und Styling | [DESIGN_SYSTEM.md](docs/DESIGN_SYSTEM.md) |
| Tower, Turrets, Placement | [TOWER_CREATION.md](docs/TOWER_CREATION.md) |
| Gegner, Animationen, Gegner-Audio | [ENEMY_CREATION.md](docs/ENEMY_CREATION.md) |
| Schaden, Rüstung, Balance | [MASTER_GAME_DESIGN.md](docs/game-design/MASTER_GAME_DESIGN.md) |
| Route, Korridor, Zellen | [ROUTE_CORRIDOR.md](docs/ROUTE_CORRIDOR.md) |
| Sichtlinien der Tower | [LOS_PIPELINE.md](docs/LOS_PIPELINE.md) |
| Wellen: Quellen, Vertrag, Wellenliste | [WAVE_SOURCE_PLAN.md](docs/WAVE_SOURCE_PLAN.md) (Einstieg) |
| Wellen: Regeln, Deckel, Spawning | [WAVE_DIRECTOR.md](docs/WAVE_DIRECTOR.md), [WAVE_SYSTEM.md](docs/WAVE_SYSTEM.md) |
| Daten eines Laufs, Export | [RUN_LOG.md](docs/RUN_LOG.md) |
| Offene Nachtests im Spiel | [PLAYTEST.md](docs/PLAYTEST.md) |
| End-to-End-Tests im Browser | [E2E.md](docs/E2E.md) |
| Coop, Relay, Lockstep, LAN | [COOP_PLAN.md](docs/COOP_PLAN.md), [SIMULATOR_PLAN.md](docs/SIMULATOR_PLAN.md) |
| Desktop-App, Release | [ELECTRON_DESKTOP_PLAN.md](docs/ELECTRON_DESKTOP_PLAN.md) |
| Offene Arbeit und Entscheidungen, Changelog | [TODO.md](TODO.md), [DONE.md](DONE.md) |

**Hinweis zu TODO/DONE:**
- **TODO.md** ist die einzige Liste offener Arbeit: ein Backlog mit stabilen Kennungen (A1, C16, E27 …), dazu
  „Entschieden“ und „Verworfen“; Handover und Berichte führen keine eigenen Listen
- **DONE.md** ist ein chronologischer Changelog mit Datumsabschnitten (neueste zuerst)
- Einträge werden **nur auf menschlichen Zuruf** von TODO nach DONE verschoben
- Bei neuen Einträgen in DONE.md immer das aktuelle Datum als Section verwenden

## Tech Stack

| Teil | Technologie |
|------|-------------|
| Framework | Angular 22 (Node >= 22.22.3 bzw. 24.15, npm 11) |
| 3D Engine | Three.js 0.186 |
| 3D Tiles | 3DTilesRendererJS 0.5.2 |
| UI | Angular Material 22 |
| Maps | Google Photorealistic 3D Tiles über Cesium Ion (Standard) oder die Google Maps API |
| Straßen | OpenStreetMap über Overpass |
| Geocoding | OpenStreetMap Nominatim |
| Bot-Server | Python 3.9+ (venv: 3.11) + WebSockets |
| Bot-Dashboard | FastAPI (http://localhost:3002) |
| Bot System | TypeScript Strategy Pattern (Browser) |
| Coop-Relay | Node + ws (coop-server/), im Lockstep |
| Desktop | Electron 44 (desktop/), NSIS (Windows), AppImage (Linux) |
| E2E | Playwright (e2e/) |


---
## Verbatim: .claude/commands/bots.md
Starte, überwache und steuere Bot-Läufe (Wave-Director gegen einen Bot in DevWorld).

Argumente (optional, `$ARGUMENTS`):
- `start`     — kompletten Stack hochfahren und Läufe starten (Default)
- `start N`   — mit N Bot-Tabs (Default 4, sinnvoll 1-8)
- `status`    — nur Zustand berichten, nichts starten
- `watch`     — Status berichten und in Intervallen weiter beobachten
- `stop`      — Läufe pausieren (Bot aus, Tempo 1)
- `render on|off` — 3D-Rendering in allen Bot-Tabs zu-/abschalten
- `speed N`   — Spieltempo setzen (1/4/10/25/50/75)

## Stack

| Teil | Kommando | Port |
|---|---|---|
| Angular Dev-Server | `npm start` | 4200 |
| Bot-Server (WS) | `bot-server/venv/Scripts/python.exe manage_server.py start` | 3001 |
| Dashboard (FastAPI) | läuft im selben Prozess wie der Server | 3002 |
| Bot-Tab | `http://localhost:4200/?devworld` | — |

Der Server startet **paused**. Clients verbinden sich, gehen automatisch
headless (`renderingEnabled=false`) und warten auf `start`.

Der Server plant keine Wellen. Das macht der Wave Director im Client
([WAVE_DIRECTOR.md](../../docs/WAVE_DIRECTOR.md)); der Server ist Transport,
Log und Fernbedienung.

## Ablauf `start`

1. Zustand prüfen: läuft schon was auf 3001/3002/4200? (`manage_server.py status`)
   Bereits laufende Teile nicht doppelt starten.
2. Bot-Server starten (Hintergrund), auf Port 3001 warten.
3. Angular-Dev-Server starten (Hintergrund), auf Port 4200 warten.
4. N Chrome-Tabs auf `http://localhost:4200/?devworld` öffnen
   (Chrome-Automation-Tools, `tabs_create_mcp`). Der User soll die Tabs sehen —
   nicht minimieren, nicht schließen.
5. Dashboard-Tab auf `http://localhost:3002` öffnen und dem User den Link nennen.
6. Warten bis alle Clients verbunden sind (`GET http://localhost:3002/api/status`
   → `clientCount`).
7. Läufe starten: `POST http://localhost:3002/api/control/start`.
8. Bestätigen: `clientCount`, `runState`, Tempo.

## Überwachung

Datenquellen (keine Log-Datei tailen, die Transkripte sind riesig):
- `GET http://localhost:3002/api/status` — `runState`, `clientCount`,
  `runsFinished`, `runsPerHour`, `wavesPerHour`, je Client Welle, lebende
  Gegner, Phase, beste Welle, dazu `errors` und der Pfad der JSONL-Datei.

Bericht an den User pro Check (kurz halten):
- Läufe je Stunde und Wellen je Stunde, Änderung seit dem letzten Check
- je Client: Welle, Phase, beste Welle
- Auffälligkeiten: Clients weg oder `stale`, Fehler in `errors`

Ein Fehlerbild, das von außen wie ein gesunder Lauf aussieht:

**Eingefrorene Tabs.** Chrome friert `requestAnimationFrame` in unsichtbaren
Tabs komplett ein. Der Status-Push läuft auf `setInterval` und meldet die
Clients weiter als gesund, während nichts mehr passiert. Symptom: Die Welle
steht still oder die Clients bleiben in `phase: setup`. Ein Heartbeat-Worker
treibt die Loop inzwischen auch versteckt (`three-tiles-engine.ts`), aber wenn
die Zähler stillstehen, ist das die erste Vermutung. Das Dashboard markiert
einen Client als `stale`, wenn länger als fünf Sekunden kein Status kam.

Wenn `watch`: nach jedem Bericht ein sinnvolles Intervall wählen (ein Lauf
dauert Minuten, nicht Sekunden) und weiter beobachten.

## Regeln

- Bot-Tabs bleiben sichtbar; Rendering nur auf Zuruf einschalten
  (`POST /api/control/set_rendering` mit `value=true`), da es die Laufrate
  stark drückt.
- `reload` schießt alle Tabs neu — nur wenn Clients hängen.
- Logs nicht ungefragt löschen.
- Keine Commits ohne Zuruf.


---
## Verbatim: .claude/commands/readdocsandtodos.md
lies unsere docs und die TODO.md und mache einen Vorschlag wie wir sinnvoll weitermachen könnten.
Biete dem User einen Wizard an wo er wählen kann wie es weitergeht.

---
## Verbatim: .claude/commands/addnewtodo.md
FÜge das übergebene TODO in der richtigen Kategorie in die TODO.md ein und prüfe auf Dubletten.

---
## Verbatim: .claude/commands/buildlint.md
Führe einen schnellen Build und Lint Check durch um Fehler zu finden.

1. Führe `npm run build` aus
2. Führe `npm run lint -- --quiet` aus
3. Fasse nur die Fehler zusammen (keine Erfolgsmeldungen)
4. Bei Fehlern: Zeige nur die relevanten Zeilen

Halte die Ausgabe minimal und konzentriert auf Probleme.


---
## Excerpt: docs/PLAYTEST.md (first 80 lines)
# Playtest: offene Nachtests

Stand 2026-09-26, Code-Stand `coop`. Hier stehen nur Nachtests: Fixes, die gebaut sind und auf das Ergebnis im Spiel
warten. Offene Arbeit, Bugs und Entscheidungen stehen in [TODO.md](../TODO.md). Die erledigten Punkte samt Ergebnissen
(bis 748, dazu M, Q, R, T bis 2026-09-26) liegen in [archive/PLAYTEST_2026-09.md](archive/PLAYTEST_2026-09.md), ältere Listen in `archive/REVIEW_*.md`.

**So wird ein Punkt abgeschlossen:**
- Antworten reicht so: "K2.1 ok, K3.4 kaputt", bei kaputt ein Satz oder ein Screenshot.
- Das Ergebnis kommt als eine Zeile unter den Punkt (`**ok (Datum)**` oder der Befund).
- Ist ein Paket durch, wandert es ins Archiv; ein Befund wird ein Eintrag in TODO.md.
- Logik prüft der Lead per Szenario-Test, hier stehen nur Augen, Ohren und echte Karten.
- Was ein Browser prüfen kann, prüfen die End-to-End-Tests (`npm run e2e`, [E2E.md](E2E.md)); welcher Punkt dort
  abgedeckt ist, steht in den Testnamen (T.., M..).

## Vorab

- Konsole (F12) offen, Filter leer. Jede Zeile mit `Shader Error` oder `Uncaught` melden.
- **Quick Actions** unten rechts, Namen im Tooltip. "Layers" (drei gestapelte Ebenen) klappt weitere Knöpfe auf:
  "Route Grid Overlay" (vier Quadrate, oberster), "Show streets" (Weg mit zwei Punkten). Ganz rechts "T": "Developer
  options".
- **Developer options:** Kachel "Credits" unter "Cheats" (Klick +1000). Unter "Waves & Inspect": "Waves" öffnet
  "Wave Debug", "Enemies" öffnet "Enemy Debug", "Snapshot" lädt den Korridor als JSON herunter.
- **Custom Wave:** Wave Debug, Knopf "Single", bei "Type" den Gegner, bei "Count" die Anzahl, "Start Custom Wave".
- **Gegner setzen:** Enemy Debug, unter "Placement" den Typ wählen, Stecknadel-Knopf, Klick auf die Route; in "Debug
  Enemies" anklicken, unter "Movement" "Start".
- Orte immer per URL mit F5 kalt laden (`http://localhost:4200/` plus die Parameter unten), keine Tower, keine Welle,
  wenn nicht anders gesagt.

## M Druck-Regler und HP-Budget (2026-09-22)

Gemessen ist der Regler an Bot-Läufen; was Bots nicht prüfen können, ist wie es sich anfühlt. Genau darum geht
es hier. Ein Lauf bis mindestens Welle 30, am Ende über "Runs" speichern.

- **M4 "Why this wave"**: Im Wave-Debug-Fenster steht jetzt "Pressure loop: waves cost X % of HP on average,
  ... so it opened/closed to ×Y" statt der alten Leck-Zeile. Erwartung: Die Zahlen passen zu dem, was man
  gerade erlebt hat.

## Q Balance-Runde nach dem New-York-Lauf (2026-09-23)

Aus M2/M3 und der Gold-Auswertung (beide im Archiv). Ein Lauf bis mindestens W31, am Ende über "Runs" speichern.

- **Q1 Keine Wand in W15**: Golem Squad bleibt beim Überlebbarkeits-Deckel. Erwartung: keine Welle, die auf einen
  Schlag den Großteil der HP nimmt. Im Wave Debug steht bei W15 keine Anzahl über dem Deckel.
- **Q4 Gold**: Ein Herbert, Mammut oder Golem bringt sichtbar mehr als ein Zombie derselben Welle (Kopfgeld nach
  Wurzel der Basis-HP). W21 bis W30 wachsen je Welle um ×1,2, nach W30 fällt das Einkommen je Welle nur noch
  um ×0,85 statt ×0,5. Die Auswertung macht der Lead aus der Datei.

## T Coop: Tower bemannen, Spieler-Leiste, Gold, Lobby (2026-09-24, Branch `coop`)

Relay neu starten (`npm run coop-server`), zwei Fenster, beide neu laden. Nach dem Lauf reicht das Relay-Log
(`logs/coop_*.log`). Kommt ein `DESYNC`, das Log melden.

- **T13 Relay per LAN (R6)**: `npm start -- --host 0.0.0.0`, der Host öffnet das Spiel selbst über `http://<IP>:4200`
  (nicht localhost, sonst zeigt der Einladungslink auf localhost), zweiter Rechner nimmt den Einladungslink. Erwartung: Der Gast findet den Relay unter `ws://<IP>:3003` von selbst; im Dialog steht
  „Server <IP>:3003“.

- **T68 Squad-Box springt nicht mehr** (User, 2026-09-25): Im Coop-Spiel die Welle abwarten, bereit setzen, die nächste
  starten. Erwartung: Der Fuß der Squad-Box („Ready up for the next wave“, „Waiting for …“) bleibt als Zeile stehen,
  auch leer; Box und Chat darunter verschieben sich nicht mehr. Dazu (User, 2026-09-26): die Spielerzeilen wachsen mit Name und
  Tags, die Spawn-Zeile liegt in der Zeile, der Lane-Strich läuft bündig über die ganze Höhe.
  Vorab per Probe (2026-09-26, zwei Browser, echte Karte): die Box bleibt 208,6 px hoch über Bereit, Welle und Wellenende; sie rückt je Chat-Zeile (Systemzeilen wie „Bob is ready“) um eine Zeile höher, bis der Chat voll ist. Offen: ob das stört.
- **T69 Tastenleiste unter dem Chat lesbar** (User, 2026-09-25): „Enter chat · X mark · Tab room“ auf heller Karte.
  Erwartung: eigene dunkle Fläche, gut lesbar.
- **T70 Beitreten ohne eigenen Ort und das neue Dock (E30, E31 Schritt 1)**: App frisch starten (Standortdialog).
  Reiter „Coop“: Umschalter „Same network“ mit Liste und „Online“ mit Code. Auf dem anderen Rechner „Same network“ und „Host a room“, hier in
  der Liste „Join“. Erwartung: der Dialog schließt, der Ort des Hosts lädt einmal, danach geht das Dock mit der Lobby
  auf. Im Dock: keine Server-Adresse mehr, Raumkopf „LAN“; die Lobby steht als Auswahl über „Open rooms“. Geprüft per
  Skript (Browser hostet online, App tritt per Code bei). Bekannt: der Ortsname kann beim Gast anders lauten
  (Rückwärtssuche), gleicher Ort.
- **T71 Öffentliche Raumliste (D62, D63)**: Ein Spieler hostet online, ein anderer öffnet Coop. Erwartung: unter
  „Online“ steht „Open rooms“ mit dem Raum (Titel, Host, Stadt ohne Straße, 1/4, „Lobby“, Ping); der Host sieht im
  Raum „In the public list“ mit Titel und dem Hinweis zum Ort; schaltet er auf privat oder sperrt den Raum,
  verschwindet er aus der Liste. Nach dem Start steht er grau als „In game · Wave n“. Geprüft im Dev-Spiel mit zwei
  Browsern über „This machine“; über die echte Lobby offen, bis sie läuft.
- **T72 Tower bemannen in der Desktop-App** (User, 2026-09-25, Online-Test): Im bemannten Tower stand nur „Click
  the map to aim“, Zielen und Schießen gingen nicht. Ursache: die App erlaubte Webseiten-Berechtigungen nur für die
  Zwischenablage und lehnte den Pointer Lock ab (`SecurityError`, im Electron-Test belegt); betrifft auch den
  Einzelspieler in der App und damit v0.4.0. Gebaut: `pointerLock` erlaubt (`desktop/src/security.js`). Nachtest mit
  neuem Installer: Tower bemannen, klicken, Maus zielt, Linksklick schießt; allein und im Coop.
- **T67 Held des Partners (R15)**: Im Coop-Spiel heuern beide ihren Helden an. Erwartung: jeder sieht auch den Helden


---
## Excerpt: docs/game-design/MASTER_GAME_DESIGN.md (first 200 lines)
# 3DTD: Master Game Design Document

**Stand:** 2026-09-15, gegen die Configs geprüft.

> **Wie dieses Dokument zu lesen ist.** §1 bis §11 beschreiben, was gebaut ist;
> die Quelle der Wahrheit ist jeweils die genannte Config. Wo ein Punkt der
> früheren Fassung nicht gebaut ist, steht an seiner Stelle ein Verweis nach
> §12. §12 sammelt diese Design-Absicht, jeweils mit dem Abschnitt, aus dem sie
> kam. Gestrichen wurde nichts.
>
> Die Balance-Zahlen geben wieder, was die Configs heute sagen. Eine Bewertung
> steht hier nicht.
>
> **Erweitert seit 2026-05-11:** Der **Lightning Tower** mit eigenem `damageType: 'lightning'`
> (8. Schadenstyp im Code, `DAMAGE_TYPES` in `configs/combat/combat.types.ts`) ist
> ausgeliefert und in §2.1 / §2.3 / §3.12 integriert.
>
> **Erweitert 2026-09-12:** Schadenstyp **Chaos** (9. Typ, 1,0 gegen jede
> Rüstung) und der **Chaos Tower** als teurer Generalist, §2.1 / §2.3 / §3.13.
>
> **Erweitert 2026-09-17:** das **Missile Silo** als zweites Gebäude, von dem
> der Nuklearschlag startet, und das Einmal-Flag `unique`, §6.1b.

## 1. Design-Philosophie
- **Einfach zu lernen, schwer zu meistern**: klare Basisregeln + Veteranen-Tiefe (Matrix, Status, Flags).
- **Fairness vor Überraschung**: neue Mechaniken werden **geteasert**, harte Checks nur nach Verfügbarkeit von Countern.
- **Strategische Vielfalt**: mehrere gültige Antworten auf jede Bedrohung (kein Ein-Turm-Meta).
- **Lesbarkeit**: Icons, Farben, Damage-Feedback, Wave-Preview.
- **Progressive Komplexität**: neue Armor-Typen, Flags und Air werden schrittweise eingeführt.

---

## 2. Damage & Armor System (Matrix + Status + Flags)

### 2.1 Schadenstypen (9)
- **Physical (⚔️)**: solider Allrounder ohne Stärke, prallt an Panzerung ab.
- **Pierce (🎯)**: hohe Feuerrate, Schwarm- und Flinkkiller, gegen Stein und Stahl nutzlos.
- **Siege (💥)**: langsame AoE, reiner Panzerknacker, gegen weiche Ziele und Geister schwach.
- **Magic (✨)**: bester Ethereal-Counter, zweiter Konter gegen Fortified, flinke Ziele weichen aus.
- **Fire (🔥)**: DoT/Burn, verbrennt Fleisch, gegen Stein und Geister wirkungslos.
- **Ice (❄️)**: Low-DPS, starker Slow/CC, Ethereal-Counter.
- **Poison (☠️)**: DoT-Spezialist gegen Lebendes, eigenständiger Schadenstyp.
- **Lightning (⚡)**: Hitscan-Chain (Primary + Jumps mit Falloff), stark gegen Light und Ethereal, gut gegen Heavy (Metall leitet), gegen Stein wirkungslos.
- **Chaos (🌀)**: voller Schaden gegen jede Rüstung, keine Schwäche und keine Stärke. Der Generalist, teuer und spät erforschbar.

### 2.2 Rüstungstypen (5)
- **Unarmored**
- **Light**
- **Heavy**
- **Fortified**
- **Ethereal**

### 2.3 Schadensmatrix (Stand 2026-09)
> **Änderung 2026-09:** Spreizung pro Rüstung von 1,5× bis 11,7× auf 3× bis 20×
> erweitert. Vorher hatten sechs von acht Schadensarten keine Paarung unter 0,5,
> die Cannon keine unter 0,7. Ethereal bleibt **nicht** immun gegen
> Physical/Pierce/Fire, sondern **stark reduziert (0.1×)**.

```
                  Unarmored   Light    Heavy    Fortified   Ethereal
                  ─────────  ──────   ──────   ─────────   ────────
Physical  ⚔️       1.0×      1.0×     0.5×     0.3×        0.1×
Pierce    🎯       1.25×     1.6×     0.35×    0.25×       0.1×
Siege     💥       0.5×      0.5×     1.75×    1.6×        0.3×
Magic     ✨       0.9×      0.5×     0.9×     1.3×        2.0×
Fire      🔥       1.5×      1.2×     0.6×     0.25×       0.1×
Ice       ❄️       1.0×      1.3×     0.8×     0.5×        1.5×
Poison    ☠️       1.4×      1.2×     0.4×     0.3×        0.2×
Lightning ⚡       1.0×      1.5×     1.2×     0.3×        1.5×
Chaos     🌀       1.0×      1.0×     1.0×     1.0×        1.0×
```

Spreizung: unarmored 3,0×, light 3,2×, heavy 5,0×, fortified 6,4×, ethereal 20×.
Die Chaos-Zeile liegt in jeder Spalte innerhalb dieser Spannen und ändert sie nicht.

> **Quelle der Wahrheit:** `src/app/configs/combat/damage-matrix.config.ts`. Bei
> Anpassungen dort gilt es, diese Tabelle synchron zu halten; die TypeScript-
> Mapped-Types erzwingen Vollständigkeit auf Code-Seite, nicht in der Doku.

**Regeln** (als Test in `damage-calculator.spec.ts`):
1. Jede Schadensart hat mindestens eine Paarung ≤ 0,5: dort beißt sich der Tower die Zähne aus.
2. Jede Schadensart außer Physical hat mindestens eine Paarung ≥ 1,3. Physical bleibt der Allrounder ohne Stärke, er ist der Starttower.
3. Jede Rüstungsart hat mindestens zwei Konter ≥ 1,2, beide erforschbar, bevor die Kampagne die Rüstung zum ersten Mal schickt.

**Ausnahme Chaos** (seit 2026-09-12): Chaos bricht Regel 1 und 2 bewusst, die
Zeile steht überall auf 1,0. Der Generalist bezahlt nicht mit einer
Matrix-Lücke, sondern mit Preis (Tower 200, Forschung 1.000 hinter Siege
Engineering und Storm Mastery, §3.13) und damit, dass er in keiner Spalte der
beste Konter ist. Auch gegen Ethereal 1,0 statt einer Abwertung: Magic (2,0),
Ice und Lightning (1,5) bleiben deutlich besser, und weil die Chaos-Forschung
Arcane Studies voraussetzt, gibt es Chaos nie vor dem ersten echten
Ethereal-Konter. Chaos zählt damit als Anti-Ethereal-Tower
(`isAntiEtherealTower`, Schwelle 1,0), das Mechanik-Gate aus §6.5 bleibt
unverändert. Der Test prüft beides (`damage-calculator.spec.ts`).

| Rüstung | Konter ≥ 1,2 |
|---|---|
| Unarmored | Fire 1,5 · Poison 1,4 · Pierce 1,25 |
| Light | Pierce 1,6 · Lightning 1,5 · Ice 1,3 · Fire 1,2 · Poison 1,2 |
| Heavy | Siege 1,75 · Lightning 1,2 |
| Fortified | Siege 1,6 · Magic 1,3 |
| Ethereal | Magic 2,0 · Ice 1,5 · Lightning 1,5 |

**Interpretation:**
- **Ethereal** ist **hart, aber nicht unbesiegbar**. Magic/Ice/Lightning bleiben beste Konter, aber Notlösungen existieren.
- **Luft:** Light-Flieger (Fledermaus, Hornisse) kontern Gatling mit AA Retrofit (1,6), Lightning (1,5) und Ice (1,3). Heavy-Flieger (Drache) kontern Rocket (1,75) und Lightning (1,2). Die Rocket ist damit der Anti-Drachen-Tower und gegen Schwärme schwach (0,5).
- **Überlebbarkeits-Deckel:** Der Wave-Director würde eine schlechte Paarung sonst mit einer kleineren Welle beantworten. Deshalb zählt er gegen Boden-Gegner (außer Ethereal) jeden Tower mit mindestens 0,6 (`FAIRNESS_MATCHUP_FLOOR`), siehe §6.5.

### 2.4 Status-Effekte (Schicht 2)

Gebaut sind fünf Effekte (`StatusEffectType` in `models/status-effects.ts`,
Mechanik in [STATUS_EFFECTS.md](../STATUS_EFFECTS.md)):

| Effekt | Quelle | Wirkung | Dauer |
|---|---|---|---|
| **Slow** | Ice Tower | -50 % Tempo | 3 s |
| **Burn** | Fire Tower | 20 % der Beam-DPS als DoT, Tick 500 ms, pro Turm ein Eintrag | 3 s, im Kegel erneuert |
| **Poison** | Poison Tower | 8 DPS | 4 s |
| **Freeze** | Frostbombe | Halt | 3 s, Bosse 1 s |
| **Stun** | EMP | Halt | 1,5 s, Maschinen 6 s, Bosse 0,75 s |

Werte aus `game-balance.config.ts` (`effects`), `combat-tuning.config.ts`
(`burnTickIntervalMs`) und `abilities.config.ts`. Beim Burn bleibt die Summe im
Kegel gleich: der Fire Tower gibt 20 % seines Schadens als Burn aus statt
direkt. Details in [STATUS_EFFECTS.md](../STATUS_EFFECTS.md#burn-effect-dot),
die Fähigkeiten in [ABILITIES.md](../ABILITIES.md).

Nicht gebaut: Armor Break, Mark, ein Stun als Tower-Effekt, die Gegenmittel
`immuneToSlow` und `immuneToBurn` sowie Regen, gegen den Burn helfen sollte.
Die Design-Werte stehen in §12.1.

### 2.5 Gegner-Eigenschaften (Schicht 3)

Gebaut sind diese Eigenschaften je Gegnertyp (`EnemyTypeConfig` in
`enemy-types.config.ts`):

| Eigenschaft | Feld | Wirkung | Typen |
|---|---|---|---|
| Luft | `isAirUnit` | nur von Towern mit Luftziel zu treffen | Bat, Hornet, Dragon |
| Boss | `isBoss` | Boss-Leiste, Boss-Intro, Fähigkeiten wirken schwächer | Herbert, Skarnax, Ooze |
| Maschine | `mechanical` | das EMP hält sie 6 statt 1,5 s | Tank, Mech |
| Split | `splitOnDeath` | ein Kill (kein Leck) teilt den Gegner | Skeleton (2 Minions), Ooze (bis zu 10 Slime Clumps) |
| Kette | `chain` | ein Spawn bringt einen Wurm aus Segmenten | Skarnax |

`immunityPercent: 100` steht bei Herbert in der Config, gelesen wird es im
Spiel nicht (nur ein Spec prüft, dass das Feld nicht negativ ist).

Die geplanten Flags Shielded, Camo, Regen, Phasing und Aura sind nicht gebaut,
siehe §12.2.

---

## 3. Tower-Katalog (Stats + Upgrade-Bäume)

### 3.1 Basis-Tower
> Werte aus `tower-types.config.ts` (Quelle der Wahrheit), Stand 2026-09.

| Tower | Typ | Base Stats | Kosten | Air? |
|---|---|---|---:|---|
| **Archer** | Physical | 25 dmg, 1.0/s, Range 30 | 45 | **Air + Ground** |
| **Dual-Gatling** | Pierce | 10 dmg, 5.0/s, Range 50 | 90 | per Forschung (AA Retrofit) |
| **Cannon** | Siege | 55 dmg, 0.5/s, Range 70, Splash 6 m (max. 8 Ziele) | 150 | nein |
| **Rocket** | Siege | 40 dmg, 0.5/s, Range 100 | 120 | **Air-only** |
| **Magic** | Magic | 40 dmg, 1.5/s, Range 70 | 140 | nein |
| **Ice** | Ice | 5 dmg, 0.33/s, Range 60, Slow 50 % 3 s, Splash 8 m | 90 | **Air + Ground** |
| **Fire** | Fire | 35 DPS Beam, Range 20 (= Flammenlänge) | 110 | nein |
| **Tentacle** | Physical | 30 dmg, 1.5/s, Range 25 | 80 | nein |
| **Poison** | Poison | 5 dmg + DoT 8/s für 4 s, 1.0/s, Range 55, Splash 8 m | 100 | nein |
| **Lightning** | Lightning | 35 dmg primary, Chain ×0.7/Jump, 2 Jumps, 0.8/s, Range 65 | 130 | **Air + Ground** |
| **Chaos** | Chaos | 50 dmg, 1.2/s, Range 60, 1,0 gegen jede Rüstung | 200 | **Air + Ground** |

### 3.2 Upgrade-Regeln (Stand 2026-09)
- **Kosten:** `50 × 1,25^Stufe` pro Stufe und Track, für alle Tower gleich.
- **Damage und Fire Rate:** 25 Stufen. Stufe 1–15 wirkt der tower-eigene
  Multiplikator `m`, Stufe 16–25 nur noch `1 + 0,4 × (m − 1)`. L25 liefert das
  5,3- bis 6,4-Fache der Basis-DPS (vorher 14,5 mit ×1,05/×1,06 für alle).
- **Range:** 10 Stufen × 1,03 (max. ×1,34), für alle Tower gleich (vorher 25 Stufen
  × 1,04, also ×2,67; Archer ×1,02). Beim Fire Tower verlängert Range die Flamme,
  Beam Width ist ebenfalls ein 10-Stufen-Track × 1,03.
- **Tier-Gating:** 5er-Bänder hinter Forschung (T2 Advanced Weaponry … T5
  Transcendent Tech). Der Range-Track endet in Tier 2.
- Der Tower wächst über Schaden oder über Tempo:

| Tower | Damage `m` | Fire Rate `m` | Idee |
|---|---:|---:|---|
| Archer | 1,05 | 1,04 | Starttower, im Endausbau kein Dauerfeuer |
| Dual-Gatling | 1,04 | 1,06 | Feuerrate ist der Kill-Durchsatz gegen Schwärme |
| Cannon | 1,07 | 1,02 | schwere Einzelschüsse, Splash-Durchsatz bleibt klein |
| Magic | 1,05 | 1,05 | ausgewogen |
| Rocket | 1,07 | 1,03 | wenige schwere Treffer gegen Drachen |
| Ice | 1,04 | 1,05 | Rate bestimmt die Slow-Abdeckung |
| Fire | 1,06 | (Beam Width 1,03) | Kegel trifft viele Ziele |
| Tentacle | 1,07 | 1,03 | Nahkampf, wenige harte Schläge |
| Poison | 1,05 | 1,04 | DoT skaliert mit dem Damage-Track |
| Lightning | 1,05 | 1,04 | Kette vervielfacht ohnehin |
| Chaos | 1,05 | 1,04 | Generalist, soll die Spezialisten auch im Endausbau nicht überholen |

Andere Upgrade-Pfade als diese Tracks gibt es nicht. Die früher je Tower
geplanten Pfade (Air-Pfade, Armor Break, Luftflamme, Spezialisierungen) stehen
in §12.3.


---
## Excerpt: TODO.md (first 60 lines)
# TODO

**Offene Arbeit steht nur hier.** Handover, Berichte und Playtest-Listen führen keine eigenen Listen, sie verweisen
hierher. Offene Nachtests stehen in [docs/PLAYTEST.md](docs/PLAYTEST.md), Erledigtes und getroffene Entscheidungen in
[DONE.md](DONE.md) (nur auf Zuruf), Überholtes in `docs/archive/` und in der Git-Historie.

- Ein Eintrag hat eine bis drei Zeilen: was, Status, Beleg nur wo nötig.
- Die Kennungen (A1, C4, ...) bleiben stabil. Ein erledigter Eintrag geht nach DONE.md, seine Nummer wird nicht neu
  vergeben. Neues kommt ans Ende des Backlogs.
- Konzepte und Pläne bekommen ein eigenes Dokument, hier steht nur der Verweis.

Stand 2026-09-25, gearbeitet wird auf `coop`. Offene Nachtests stehen in [docs/PLAYTEST.md](docs/PLAYTEST.md), vor
allem unter T (Coop).

---

## Später (Backlog)

- [ ] **C16 Zufalls-Spawn-Portal noch schräg** (User, 2026-09-17, Amsterdam "Westerstraat", nicht reproduziert): Trotz
      Verschieben auf ein gerades Stück (`cbdec4e5`) stand ein Portal schräg. Vermutungen: gerades Stück zu kurz (nur
      bis zur Ebene geprüft, Mindestlänge etwa 25 bis 30 m fehlt) oder die Gegnerlinie schwenkt am Start vom OSM-Punkt
      zur Bandmitte. Erst mit URL oder Snapshot eines neuen Falls debuggen.
- [ ] **C17 Zoom rutscht nahe der Route zurück und nach Norden** (User, 2026-09-23, nur hier reproduziert):
      `?l=52.55000,19.70000&s=52.54690,19.69225` (Płock). Wer aufs Portal oder daneben zoomt, wird am Limit
      zurückgesetzt, die Kamera rutscht nach Norden. Mit weit versetztem Spawn ist dieselbe Stelle unauffällig.
      Kein `cameraCorrection` im Log; der Korridor-Aufbau lief dort als "unmeasured freeze" (452/452 Stationen,
      Fallback). Vermutung, unbelegt: die Korridor-Region hält grobe Tiles, der Abstands-Raycast der GlobeControls
      trifft zu hoch. Messen: Raycast-Treffer, Höhe, Tile-Tiefe am Limit, mit und ohne Region.
- [ ] **C19 Tower bemannen wirkt kaputt** (bis 2026-09-25 als C18 geführt, die Nummer hat schon DONE) (User, 2026-09-24, Coop, im Einzelspieler ungeprüft; **gebaut 2026-09-24**,
      Nachtest T1 ok im Coop, archiviert; offen: Einzelspieler und die Desktop-App, PLAYTEST T72): Fadenkreuz kommt,
      Sidebar verschwindet, aber die Kamera bleibt, Zielen und Schießen gehen nicht. Ursache im Coop, aus dem Code:
      `TowerControlService.enter()` prüft direkt nach `command:man-tower` mit `getMannedTower()`, ob man drin
      sitzt; im Lockstep wirkt der Befehl erst am Tick, also bricht `enter()` ab (keine Kamera, kein Pointer-Lock,
      kein Zielen). Das spätere `tower:manned` setzt den Store trotzdem, daher Fadenkreuz und leere Sidebar. Lösung:
      Kamera und Eingabe erst auf das eigene `tower:manned` hin anschließen. Einzelspieler nachprüfen. So gebaut:
      `takeSeat` beim eigenen `tower:manned`; die Kamera folgt dem lokalen Ziel, das Maus-Ziel rechnet nicht mehr vom
      nachlaufenden Tower-Ziel aus, im Coop geht das Ziel höchstens einmal je Tick raus (D12).
- [ ] **A1 Herkunft von 5 Gegnermodellen** (Ghost, Hornet, Mech, Wraith, zombie_v2), Einträge in
      `attributions.config.ts` nachtragen. Der User sucht die Quellen, low prio; Stone Golem und Herbert sind eigene
      Modelle.
- [ ] **A2 Tentacle-Sound ersetzen** (Security-Review 2026-09-27, User: ersetzen): `tentacle-01.mp3` trägt ID3-Tags
      aus „The Odyssey Collection: Expanded“ (Liquid FX), eine Lizenz ist nicht belegt. Neu mit ElevenLabs über die
      Sound-Auswahlseite (`tmp/sound-audition`), User wählt, alte Datei raus.
- [ ] **A3 Spielmenü mit Zahnrad und Esc** (User, 2026-09-27): Zahnrad unten rechts im Sidebar-Fuß, Esc öffnet es,
      wenn Esc sonst nichts zu tun hat (kein Dialog, kein bemannter Turm). Einträge: Vollbild (F11), Lautstärke (M),
      What's new, Attributions; nur in der Desktop-App „Quit 3DTD“, im laufenden Spiel mit Rückfrage (im Coop: der Raum
      verliert dich). Im Browser Vollbild über die Fullscreen-API, ohne Quit.
- [ ] **A4 Update-Hinweis über modalen Dialogen** (Test 2026-09-27, **gebaut**): 0.5.0-beta.2 bot 0.5.0 an, aber der
      Standortdialog des ersten Starts schluckte den Klick auf „Restart now“. Der Hinweis hängt jetzt im CDK-Overlay über
      allen Dialogen (`update-hint.component.ts`, Spec). Geht mit dem nächsten Release raus.
- [ ] **E1 Balancing aufrollen**: Phase 1 und 2 sind gebaut, die Baseline steht (354 Läufe, 2026-09-21), sechs
      Tuning-Runden sind gelaufen. Offen sind die Zielbänder (3b) und das Kampagnenende (3a),
      [docs/BALANCING_PLAN.md](docs/BALANCING_PLAN.md).
- [ ] **E12 Heilung oder kürzere Kampagne?** (User, 2026-09-26: vertagt bis zu eigenen langen Läufen, Tendenz "so
      lassen"): Der Könner verliert in W24-29 je 8 bis 14 HP und nichts heilt; die drei Antworten stehen in
      [docs/BALANCING_PLAN.md](docs/BALANCING_PLAN.md), "Was das Tuning nicht lösen kann". Hängt an D10.
- [ ] **E14 Luftwellen kosten doppelt so viel wie der Deckel verspricht** (gemessen 2026-09-21, 5085 Bot-Wellen
      plus ein Menschenlauf): In Wellen, in denen der Deckel Spielraum versprach (Deckel x1,6 über der
      Wellengröße), töten Bodenverteidigungen **100 %** der Welle, Luftverteidigungen **50 %**, bei 10,9 statt
      4,2 HP Verlust. Im Menschenlauf sagte der Deckel bei W8 Hornet Strike "645, not binding", getötet wurden 68
