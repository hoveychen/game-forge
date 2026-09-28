# Kart Royale (Ryan Campbell) — Shumer template retargeted to Mario Kart; bar rewritten as calibrated rubric

- **Source URL:** https://github.com/ryancampbell/kart-royale (README section "The prompt", "Verbatim, typo and all"); tweet https://x.com/Ryancampbell/status/2081750419857133709 (2026-07-27); write-up https://www.ryancampbell.com/kart-royale
- **Model/tool:** Claude Opus 5, Claude Code with subagents / `/loop` / ultracode ("a fleet of Claude agents in four days"; 127 agents / 11 rounds per secondary coverage)
- **Genre:** Kart racer (Mario Kart-style), Three.js, zero art assets (~60.5k LOC, 49 files, 4 runtime deps)
- **Result evidence:** Playable at https://racing.ryancampbell.com ; repo includes ART_DIRECTION.md (art bible), FEEDBACK.md (public/player feedback), 13 test harnesses in tools/
- **Quality signal:** Tweet ~54k views / 362 likes; repo ~64 stars. Author's own honest score: **62/100** vs a shipped-Mario-Kart bar ("It does not have better graphics than Mario Kart World"); drift-to-boost loop 74/100. Author: "Still drops some frames but this is amazing what was completed just yesterday".
- **One-shot vs iterative:** One seed prompt, then nine orchestrated multi-agent rounds over four days, with human playtest feedback folded in (FEEDBACK.md, from X replies).
- **Key lessons the author documents (valuable for spec research):**
  - The prompt's bar ("compare side by side blind against actual Mario Kart") was unusable (copyrighted frames, self-grading). It was replaced by an explicit rubric with calibrated bands in ART_DIRECTION.md §9, and the author calls this "the single change that made the loop work."
  - ART_DIRECTION.md (course layout, exact sun angle, palette hexes, material standards) "is the reason eleven agents working in parallel produced something coherent."
  - Critics judged rendered screenshots from a headless build, not source code.
  - **Failure mode:** "The screenshot critics found none of the gameplay bugs. Inverted steering, missing mobile controls, black frames, a pause menu that suspended the race permanently, a phone crash at ten seconds — every one came from a human playing."
  - The post-FX chain was silently dead for 4 rounds (caught exception, pass disabled); critics noted "no antialiasing" but nobody read that as a crash report.
  - Best design feedback came from a stranger on X: "For a kart racer the whole game lives in the drift into boost loop... Feel first, more tracks later." This matched the lowest internal score (game feel).

## Verbatim prompt (typo "kat" in original)

```
I want you to build a kat racing game at the level of the most recent Mario Kart games. It should be utterly perfect, visually beautiful, with every single thing done at AAA quality—from textures to physics to anything you could think of.

Fan out sub-agents and have sub-agents tackle each one individually so that the game is utterly perfect. You should /loop on each item and have a separate sub-agent check it visually to ensure it looks triple A. That separate sub-agent should be a really harsh critic, and if it doesn't look triple A, it should keep going.

Don't stop until each sub-agent is utterly wowed with the quality when compared with the actual Mario Kart game. It should literally compare them side by side blind and say which one looks better. Do this in ThreeJS. /loop until it's utterly perfect. Fan out sub-agents and ultracode.
```

## Replacement critic rubric (ART_DIRECTION.md §9, as quoted in README)

```
0-40   reads as a programmer-art prototype
40-60  a competent hobby project; obviously not commercial
60-75  a good indie game; still clearly not first-party
75-88  near-professional, but a trained eye spots the tells immediately
88-95  genuinely shipped-AAA quality
```
"Almost nothing deserves 88+ on an early round. If you are inclined to give 85, look harder — you are probably missing something."
