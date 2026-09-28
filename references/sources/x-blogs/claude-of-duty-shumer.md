# Claude of Duty (Matt Shumer) — "Gauntlet Loop" 3-paragraph prompt

- **Source URL (prompt):** https://x.com/mattshumer_/status/2081100592689324502 (reply "Prompt:"), also https://github.com/mshumer/Claude-of-Duty/blob/main/prompt.md
- **Demo post:** https://x.com/mattshumer_/status/2081054356405731740 (2026-07-25) — "Claude Opus 5 one-shotted this game. EVERYTHING you see in this demo is custom code... not a single external asset was used."
- **Method write-up:** https://somethingbig.ai/gauntlet-loop ("Gauntlet Loop")
- **Model/tool:** Claude Opus 5 in Claude Code, with subagents, `/loop`, "ultracode"
- **Genre:** First-person shooter (CoD-style, single market-street map), Three.js/WebGL2, all assets procedural
- **Result evidence:** Repo https://github.com/mshumer/Claude-of-Duty (~3.4k stars, ~520 forks as of Sept 2026); ~55k LOC over 11 subsystems; video in demo tweet
- **Quality signal:** Demo tweet ~5.05M views / 7.8k likes (fxtwitter, Sept 2026); prompt reply ~725k views. README is candid: "The goal was to match a modern Call of Duty. It does not." Internal critic scored frames ~5.05/10 ("AMATEUR"); 28–30 fps at Retina after optimization. Defects dropped 66 -> 26 across rounds; README notes sequential single-owner passes on coupled systems (lighting/tone/sky) beat parallel fan-out.
- **One-shot vs iterative:** One human prompt; "many hours" of autonomous agent looping ("I did not sit there steering it, at all"). README describes 3 rounds of 6 agents + a final sequential pass, and an ARCHITECTURE.md contract the agent wrote itself. So: one human turn, heavily iterative agent run.
- **Notes:** Spawned a copycat wave reusing the prompt verbatim (James Altucher "Operation Blackout" ~10h/1.3M tokens, https://operation-blackout-green.vercel.app/; @atomtanstudio ran it on "Sol 5.6 Ultra", https://x.com/atomtanstudio/status/2081475447037321695, 52k views). Decrypt/Yahoo framed it as "The Dumbest-Looking AI Prompt Just Beat Months of Careful Game-Design Prompt Engineering" (https://decrypt.co/374560/dumbest-ai-prompt-claude-beat-careful-game-design) and flagged training-data contamination risk (FPS code is heavily represented).

## Verbatim prompt

```
I want you to build a first-person shooter at the level of the most recent Call of Duty games. It should be utterly perfect, visually beautiful, with every single thing done at AAA quality—from textures to physics to anything you could think of.

Fan out sub-agents and have sub-agents tackle each one individually so that the game is utterly perfect. You should /loop on each item and have a separate sub-agent check it visually to ensure it looks triple A. That separate sub-agent should be a really harsh critic, and if it doesn't look triple A, it should keep going.

Don't stop until each sub-agent is utterly wowed with the quality when compared with the actual Call of Duty game. It should literally compare them side by side blind and say which one looks better. Do this in ThreeJS. /loop until it's utterly perfect. Fan out sub-agents and ultracode.
```

## Gauntlet Loop meta-prompt template (from somethingbig.ai/gauntlet-loop, excerpt)

```
I want to run a Gauntlet Loop for this goal: [GOAL]. Choose the strongest concrete bar that an agent can actually inspect and compare its work against.
```
(The page then asks the model to write the final Claude Code/Codex prompt itself; principles: real agents not chat, goals not implementation details, an inspectable reference bar, independent decomposition, builder separate from critic.)

## Independent replication + analysis (Ziwen, @ziwenxu_, X Article "How to Vibe Your First Game With One Prompt")

- URL: https://x.com/ziwenxu_/status/2081579558675853424 (~104k views)
- Ran the prompt "exactly as written, no edits, no skills, no MCP" on Claude Code / Opus 5 and "got a playable shooter out of it for 20-30% of a week's usage on Max 20x after 12 hours."
- Warned about variance: "Same model, same budget, same twelve hours: one prompt produces a shooter and the next produces a grey box."
- Reports Shumer's own logs: 11 judges over 4 rounds, final score about 5/10, and "every judge in every round picked the real Call of Duty frame". So the loop never met its own stop condition: "Just don't expect the thing to tell you it's done. It won't. You stop it."
- Breaks the prompt into brief / orchestrator (a "staffing plan") / QC (a blind pairwise comparison rather than a score). He argues the unreachable bar is deliberate ("quality is simply a function of how long you let it run"), which is the opposite of Kart Royale's conclusion that a calibrated rubric made the loop work.
