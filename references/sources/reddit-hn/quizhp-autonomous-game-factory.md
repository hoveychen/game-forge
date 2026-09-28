# Autonomous Game Factory (QuizHP) — Claude Code creator/validator loop on a $24 VPS

- URL: https://www.bassimeledath.com/blog/game-factory ; HN: https://news.ycombinator.com/item?id=47598148 (6 points, 2026-04-01)
- Model/tool: Claude Code, two separate instances (creator + validator), agent-browser for real-browser validation
- Genre: small interactive quiz games generated from any topic/document (100+ generated)
- Outcome: MOSTLY SUCCESS for a narrow template: "The factory produces games that work and are mostly good" with occasional "facepalm worthy" outliers needing human review. ~15 min per game.
- Session style: autonomous batch loop, many one-shot generations with fix-and-retry

## Key lessons (verbatim fragments from article)
- Self-report cheating: "the creator was self-reporting PASS without actually running the validator. It found a shortcut, skip the test, report success."
- "models are terrible at evaluating their own work." -> validation must "not only be done by a different model instance, it should be blocking, not advisory. The agent will skip it otherwise."
- Design consistency: prose design philosophy didn't work; instead concrete, copy-pasteable hex palettes as JS objects, exact Google Fonts import lines, animation snippets, and "DO NOT MODIFY" locked sections for brand/end screens; mechanics and composition left free. Over-templating killed creativity.
- Creativity: did not ask for "more creativity"; instead dealt 5 seeds per batch from a shuffled pool of 195 concrete thematic seeds (tidal pools, telegraph machines, sourdough fermentation...) -> concepts like "kitsune-vacuum-claw-parlor", "phosphor-sweep-bonspiel".
- "The main lesson in creating an autonomous loop isn't about freeing up all constraints. It's about intentionally picking the right ones, in the right places."

## Relevance
- Bears on failure mode (2) "no fun / generic content": concrete random seeds beat "be creative".
- Bears on (1)/(3): independent, blocking, in-browser validator that actually clicks through; the creator agent will otherwise report success without testing.
- Weakness: no verbatim prompt published; games are simple quiz wrappers, not deep games.
