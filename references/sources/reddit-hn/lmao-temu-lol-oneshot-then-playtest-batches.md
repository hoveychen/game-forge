# LMAO — "Temu League of Legends" MOBA: one-shot then playtest-batch iteration (Opus 4.8)

- HN: https://news.ycombinator.com/item?id=48376337 (Show HN, 4 points, 2026-06); related Reddit r/ClaudeAI 1tucsfe ("I had Opus 4.8 build temu league of legends in...") and 1tuopn2 "Temu Anno 1602" one-prompt (198 upvotes)
- Play: https://lmaomoba.com
- Model/tool: Claude Code, Opus 4.8, subagents, "Ultracode Workflows", /goal; React/Canvas/PartyKit
- Genre: web MOBA, room-based online multiplayer with bots
- Outcome: playable (self-reported "fully functional in one shot"); no independent quality evidence. ~4–6 h hands-on over 1.5 days.
- Session style: ONE-SHOT seed + multi-prompt iteration

## Verbatim
Seed prompt: "build a temu league of legends, web-only with online, room-based multiplayer"
> "It built it... fully functional in one shot! Then I went kinda ham and started iterating on every aspect little by little. I made it spin up subagents to each focus on designing a character. Spun up subagents to focus on designing abilities and their SFX/VFX. Did a few passes over the map, mobs, minions, etc. ... had it optimize performance, balance, and a variety of other things."
> "I'd sit and play and make note of like 10-15 tweaks, bug fixes, etc at a time and just let it go to town."

## Relevance
"Temu <famous game>" framing = a reference-game spec: the model fills in the whole design from a well-known template. Works for a demo; says nothing about novelty/fun (cf. r/ClaudeAI commenter: "it feels like we're entering some kind of fast fashion era for apps").
