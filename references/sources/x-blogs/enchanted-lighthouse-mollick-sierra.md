# The Enchanted Lighthouse (Ethan Mollick) — tiny vibe prompt, genre-anchored, with a hard duration and a playtest turn

- **Source URL:** https://x.com/emollick/status/2015512532056764490 (2026-01-25); full prompt posted in Mollick's own reply in the same thread
- **Model/tool:** Claude Code (the model isn't named; Opus 4.5 was the Claude Code default then) plus a custom Claude Code subagent calling GPT-image-1 for illustrations. Mollick posted that subagent's description in the thread.
- **Genre:** Sierra-style point-and-type adventure (EGA-like graphics, text parser), 10-15 min of play
- **Result evidence:** Playable at https://enchanted-lighthouse-game.netlify.app/ (HTTP 200 on 2026-09-28). The thread includes the AI's own spoiler walkthrough: 4+ phases, item combination (oil + shells -> celestial oil), a tide timer ("Tide: Low every 10 moves") that gates a cave, and keys and letters. That is a real puzzle dependency chain.
- **Quality signal:** ~114k views / 1.2k likes. Mollick: "100% designed, tested, and made by Claude Code". Joke about cliché: "And of course the main character's name is Elara."
- **One-shot vs iterative:** "It was a single prompt for the entire game, and then a prompt to playtest and improve the outcome." That makes 2 human turns.

## Verbatim prompt ("Full prompt for the game (yes, this was it)")

```
heres the deal, create me an entirely original old-school Sierra style adventure game with EGA-like graphics. You should use your image agent to generate images (consistent style, etc) and give me a parser. make all puzzles  interesting and solvable. finish the game (it should take 10-15 minutes to play), don't ask any questions. make  it amazing and delightful
```

Second turn (paraphrased by Mollick): playtest the game and deploy it.

Notable traits: a strong genre anchor ("old-school Sierra style", "EGA-like") does the job of a GDD. The only hard constraints are verifiable: a parser, solvable puzzles, and 10-15 minutes of play. It also includes autonomy directives ("finish the game", "don't ask any questions") and names the asset pipeline tool ("use your image agent... consistent style").
