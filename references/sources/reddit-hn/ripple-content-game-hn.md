# Ripple — daily 2nd/3rd-order-effects puzzle (content-driven game), vibe-coded; HN front page; content-quality critique

- HN: https://news.ycombinator.com/item?id=46490323 (155 points, 41 comments, 2026-01-04)
- Author writeup: https://katecatlin.substack.com/p/i-vibe-coded-a-game-to-the-front ; HN of writeup: https://news.ycombinator.com/item?id=46979908
- Play: https://ripplegame.app/
- Model/tool: Lovable (MVP from an AI-written spec), GitHub Copilot + Copilot Coding Agent; Gemini/Claude/ChatGPT for ideation, design critique; ChatGPT agent mode as simulated playtesters
- Genre: daily cause-and-effect prediction puzzle (see a historical event, pick what happened next from 4 options, 3 steps deep)
- Outcome: MIXED — traffic SUCCESS (40,500 visitors; HN #9, ~13,000 visitors) but HN players critiqued content depth (too easy, obviously-wrong distractors, "smells LLM", "a history quiz, not a puzzle") and the 1-per-day limit.
- Session style: multi-tool, multi-session

## Author lessons (verbatim from writeup, as extracted)
Spec: "The AI-generated-AI-prompt went far more in depth than I would have: Full details on mechanics, tone, color-scheme, and user experience" -> prototype with "30 puzzle chains, ocean-themed animations, streak tracking, shareable results, and a 'How to Play' modal."

What-not-how:
> "When prompting agentic coding AIs, describe the what, not the how. Tell them what the user should see and do."
> (archive feature broke the app) "The initial 'how-to' instructions clashed with their instincts, and the result was chaos." ... "I deleted all the implementation details and kept only what I wanted the user to experience - what the archive should look like and how it should behave." ... "It worked on the first try!"

Content — the AI's weak spot:
> "Ripple puzzles came from two places: my brain and AI...AI knows a lot of cool facts! But the question flow it generated was often shallow."
> "Many of its suggestions felt like straight trivia rather than real cause-and-effect shifts someone could predict."
> Re-prompting loop: "'Wait is step two actually true? Please search and verify.'"

Simulated playtest (ChatGPT agent mode, 20 player types) found real UX issues:
> "AI players couldn't find the 'Next Event' button because it was below the fold." / "The sign-in form on the results page made AI players think registration was required to see their score, so they just left." / "The AI players didn't understand the hint button...It said '50/50' with no explanation and they didn't get it."

## HN player critique of the content (verbatim)
- jrowen: "it felt too easy or even heavy-handed. Three of the four options in each round sound like 'and everyone lived happily ever after.' Only one sounds like something that would happen in real life and continue the story."
- noduerme: "it only works because the wrong answers are very obviously wrong (and virtually impossible). But that forces you into answering along the path which is clearly not as wrong, even though it's full of vague sweeping generalizations."
- nialv7: "This kind of smells LLM, which is fine. But I do want to see the facts backed by citations."
- mrgoldenbrown: "I would call this a history quiz, not a puzzle. The 'ripples' are not deducible from the info given."
- TuringTest: "The game tastes as too little with just one question; when you get the gist of how it works, it's over."
- dzink: "the questions are too easy ... I would do this as a tree of possible consequences instead"

## Relevance
Failure mode (2) for content-driven games: code/UX was easy to fix via agents and simulated playtesters, but the fun lives in the content (distractor quality, deducibility), where LLM output defaulted to shallow trivia with implausible distractors. AI playtesters found UX friction, not content boredom — real players found the latter.
