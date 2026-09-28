# FAILURE: Pitfall! (winterspeak Substack, "Day 5 with Claude") — historical-reference prompt, no agent loop, 4 attempts, never playable

- **Source URL:** https://winterspeak.substack.com/p/day-5-with-claude-pitfall (2025-04-15)
- **Model/tool:** Claude (claude.ai chat; the model isn't stated, likely Claude 3.7 Sonnet given the date). Single-page HTML output, no agent, no tests, no self-verification.
- **Genre:** Side-scrolling platformer (Atari 2600 Pitfall! remake)
- **Result evidence:** Screenshots in the post of all 4 attempts
- **Quality signal:** Author's verdict: "tl;dr — it could not get it working." Attempt 1: looked promising (scorpions, crocodiles in code) but the "Start Game" button did nothing. Attempt 2 ("it did not work, fix it"): "messed up the entire codebase". Attempt 3 (simplified to 3 levels): "Once more, failed to start." Attempt 4 (one mechanic: cross a pond on 3 alligators): "It got the name right, but there was no game and it instantly reached the win state."
- **Contrast from the same author:** Pong and Space Invaders were one-shot successes with the same method (Days 3-4 of the series).
- **One-shot vs iterative:** 4 turns, all failed
- **Author's diagnosis:** Claude "can one-shot simple popular games that are common in the training data, but struggles with titles that aren't as well documented"; and for non-coders, "debugging is really hard. Since you didn't set anything up yourself, you don't know why things don't work, or even where to look."

## Prompt 1 (verbatim, as quoted by the author)

```
Make a game of Pitfall! that I can share via a URL. Pitfall! was originally made for Atari in 1982 and is a side scrolling platformer with a jungle adventure theme. Please make it as a single page html app.
```

## Prompt 3 (verbatim, recovered from a mis-pasted hyperlink in the post, so the original capitalization is lost)

```
make a game of pitfall! that i can share via a url. pitfall! was originally made for atari in 1982 and is a side scrolling platformer with a jungle adventure theme. please make it as a single page html app. it should work on web and mobile. start with just 3 levels with different obstacles to keep things simple.
```

## Prompts 2 and 4 (paraphrased by the author)

2. told Claude it did not work and asked it to fix it
4. "a game where Harry needs to cross a pond by jumping on three alligators while their mouths are closed to win"

Why it's a useful contrast: the prompt names a reference game, but (a) the reference is thin in training data, (b) it states no mechanics, controls, or win/lose rules, (c) there is no verification step or instruction to test, and (d) the harness can't run the game, so "doesn't start" bugs are invisible to the model. Compare RocketLeagueBench, which spells out mechanics, controls, and verification checklist items like "The scene renders", "Take at least one screenshot... to confirm the canvas is nonblank".
