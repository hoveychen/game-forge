# Opus roguelike after multiple pivots — GDD bloats to 4000+ lines of MD, stale decisions poison new work (FAILURE MODE: context rot)

- Reddit: https://www.reddit.com/r/aigamedev/comments/1vgrarx/ (r/aigamedev, 9 upvotes, 25 comments, 2026-08)
- Model/tool: Claude Opus (then Opus 5), vanilla HTML5
- Genre: roguelike (pivoted: Rodent's Revenge-like puzzle -> action roguelike -> turn-based)
- Outcome: STALLED / frustrating; map gen, tiles, player mechanics OK; enemies/items "polluted" by previous versions
- Session style: MULTI-SESSION, fresh session daily

## Author (verbatim)
> "In the design phase I asked it to write a game design doc, but it started adding all the session context to that file, so it grew to a massive size. So we split the file into the GDD, a roadmap file, ideas file, and decision file. But now i have probably 4000+ lines of text in MD files for storing context. (And this seemed to have gotten worse when Opus 5 took over...)"
> "most of the enemy types, enemy behavior, and items and equipment ideas feel polluted still by the previous 2 versions. I'm providing ideas too, and it always 'flags' something as conflicting with some random decision that I no longer care about. It's started to just become frustrating, not that it cant write the features but that its like pulling teeth to do so."

## Useful replies (verbatim)
- Miserable-Dot8544: "the move that tends to work is deleting the narrative history and keeping only the current state"
- Mauseleum: "Context and documentation is not the same. ... Slice to more .md's enemy.md, mechanics.md, skills.md etc."
- Novel-Lifeguard6491: "worth keeping a separate archive file that you don't feed into context, in case you ever want to know why something was built a certain way"
- Laicbeias: "the llm can not make decisions for you. ... every time you design something, if you do not exactly know what you want, the llm will shit the bed. take a piece of paper. draw out each system ... usually people prototype for weeks, till they have a core loop that clicks. with ai people just seem to generate content and skip the exploration part."
- davidslv: "A fresh AI session with a good spec has better chances to get the feature done correctly than a session with too much context"

## Relevance
Letting the agent author/grow the GDD as a session log turns it into accumulated, contradictory history. A GDD should be the current-state spec (rewritten, not appended), with history archived out of context.
