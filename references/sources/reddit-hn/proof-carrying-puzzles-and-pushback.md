# Two small shipped cases: FALLMATCH (solver-proven levels) and Echo Abyss (Claude pushes back on playtest-driven tuning)

## FALLMATCH — zen block puzzle, 300 levels, designer who can't code (r/ClaudeCode 1vyy3x1, 0 upvotes, 3 comments, 2026-08)
- https://www.reddit.com/r/ClaudeCode/comments/1vyy3x1/ ; iOS https://apps.apple.com/app/fallmatch/id6791134651
- Claude Code, React Native/Expo. Outcome: shipped iOS/Android. Evidence: self-reported only.
Verbatim:
> "The division of labor was strict: I design levels, playtest on device, and make every final call; Claude Code writes all the code ... AND runs a verification pipeline we built together."
> "A solver proves the minimum move count for every level — that proof is the 3-star target players see. Every 'this mechanic is required' badge in the HUD is solver-verified. The 10 difficulty tiers are computed from measurements (search depth, narrow-path ratio, fatal-move ratio), not from my gut."
> "House rule: if the prover can't certify a claim, the level doesn't ship."
> "every design decision, every 'this feels wrong' call, every reject came from playtesting. My job was mostly saying no, demanding proof, and catching things the pipeline missed ... 'No claim without proof' turned out to be a better project rule than any prompt trick."

## Echo Abyss — deep-sea sonar stealth game in 2 days (r/aigamedev 1u47xcb, 22 upvotes, 18 comments, 2026-06)
- Play: https://www.aigameshare.com/games/echo-abyss
- Claude (+ GPT design review). Hook: "your sonar ping is the only way to see — but every hunter down there is blind and comes for sound. Seeing = being seen."
Verbatim:
> "My job was playtesting and complaining — 'I don't know why I died', 'the white eel should show up earlier', 'can share work on iOS?' Claude's job was everything else, including the part I didn't expect: it maintains its own test harness."
> "I also pasted GPT's design review of the game into Claude and asked what it thought. Claude agreed with most of it, but rejected one suggestion (adding a mobile ping button)"
> "When I said 'all eels +20 speed', it shipped it but warned me the base player can now never outrun even the weakest hunter, and told me which number to revert first if early-game deaths spike."

## Relevance
Both: the human supplies one crisp design hook and the "feels wrong" veto; the agent supplies verification. Echo Abyss is a positive counterexample to failure mode (3): the agent reasoned about the systemic consequence of a feedback-driven tweak rather than just applying it.
