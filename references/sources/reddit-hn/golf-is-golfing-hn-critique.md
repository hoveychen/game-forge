# the-golf-is-golfing.com — golf game built "last night" with Claude Code (HN critique of weekend AI games)

- HN: https://news.ycombinator.com/item?id=47014704 (36 points, 30 comments, 2026-02; flagged)
- Play: https://www.the-golf-is-golfing.com
- Model/tool: Claude Code, Svelte, Three.js (Threlte + Rapier)
- Genre: 3D mini golf
- Outcome: WEAK/FAILURE as a game per commenters (~6–7 h build): ball rolls without friction, hole-in didn't end the game for some players, single straight course, "no personality".
- Session style: short multi-prompt weekend build; no writeup

## Commenter evidence (verbatim)
- parallax_error: "I sunk the ball, but the game didn't end so I happily hit it back out of the hole!!"
- Spacemolte: "One hit and then the ball kept rolling, very slowly, seemingly without any friction."
- cluckindan: "Strictly speaking, this is not yet a game, as the main goal cannot be completed: getting the ball in the hole does nothing."
- pawelwentpawel: "I've been working with physics engine (cannon then rapier) + three js recently using Claude and found that AI was struggling quite when it came to fine tuning physics constants (friction, weights etc.) quite a lot. A human touch was needed - ended up vibe coding a small debug / admin panel where I could adjust those manually."
- boca_honey: "the game has no personality. It looks like something you would find in a shovelware demo CD 20 years ago. No art direction, no sound direction, nothing to talk about. Games made by individuals (indie games) are interesting and fun because you can almost see the person that made it."
- sublinear: "the controls are floaty and imprecise. The camera is at a strange angle ... There's only one course: a straight. ... The remaining work is the most time consuming, and even when finished the result will just be mediocre. Mediocrity isn't mere incompetence, but being asleep at the wheel when the ideas that are foundational to a project are being made."
- In same thread, jaggs' Sonnet-built golf https://gerry7.itch.io/fairwayfun was called "the winner by a large margin".

## Relevance
Win condition (ball-in-hole -> end state) not verified end-to-end; physics constants unset for feel; no design intent beyond "golf". Direct evidence of "game breaks within the first 3 steps" when no loop-completion check exists.
