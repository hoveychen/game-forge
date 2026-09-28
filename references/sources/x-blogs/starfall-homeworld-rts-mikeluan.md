# Starfall — Homeworld-style space RTS (@mikeluan123), Shumer template retargeted

- **Source URL:** https://x.com/mikeluan123/status/2081716631986983093 (2026-07-27)
- **Prompt transcription:** https://explainx.ai/blog/opus-5-homeworld-space-rts-mikeluan-july-2026 (prompt shared alongside the post; the tweet body itself shows only the cost breakdown, so treat the text below as second-hand transcription, ellipses are the transcriber's)
- **Model/tool:** Claude Opus 5 (Claude Code-style agent workflow with subagents + /loop)
- **Genre:** Universe-scale space RTS (Homeworld-like), Three.js, 13 ship classes, procedural hulls/planets, zero image files
- **Result evidence:** 57-second video in tweet; a live demo appears at https://e01.ai/starfall/ (attribution to this author not independently verified); no public repo
- **Quality signal:** ~223k views / 2.5k likes (fxtwitter, Sept 2026). Author: "Besides minor game play issues, watching model cook this is beyond my imagination." Cost $632.65 (68.6k input, 4.6M output, 837.2M cache read, 13.6M cache write). Skeptic (Samir Alibabic) questioned whether token totals add up.
- **One-shot vs iterative:** Claimed one continuous prompt session.

## Prompt (as transcribed; ellipses in source)

```
I want you to build a homeworld style universe scale RTS at the level of most recent space RTS games. It should be utterly perfect, visually beautiful, stunning in detail, with every single thing done at AAA quality—from textures to physics to anything you could think of, with the sense of massiveness and scale.

Fan out sub-agents and have sub-agents tackle each one individually so that the game is utterly perfect. You should /loop on each item and have a separate sub-agent check it visually to ensure it looks triple A. That separate sub-agent should be a really harsh critic, and if it doesn't look triple A, it should keep going.

Don't stop until each sub-agent is utterly wowed with the quality when compared with the actual Homeworld game... Do this in ThreeJS. /loop until it's utterly perfect... Only need random mode, not mission, create multiple ship types, great UI, HUD, and game mechanics, and fluent control, max quality. For ship models, and effects, AAA, max detail needed, use shaders, generative textures, and instancing to ensure best performance.
```

Note the additions vs. Shumer's original: explicit scope cuts ("Only need random mode, not mission"), feature list (ship types, UI/HUD, controls), and technique hints (shaders, generative textures, instancing).
