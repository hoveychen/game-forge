# Supplementary short quotes (weaker evidence, used for cross-checking observations)

## r/gamedev 1wo5asm "AI models have caught up with Unity dev" (2466 upvotes, 1255 comments, 2026-09) https://www.reddit.com/r/gamedev/comments/1wo5asm/
- OP (30 yrs software, studio owner): "Quality has not gone down because we're all experienced devs and we're careful how we use AI and we don't let it make decisions regarding project structure or design patterns."
- name_was_taken (writing a MUD server in Rust with Claude): "the vast majority of its decisions are correct, technically. It's the *game* that it's been wrong about for the most part."

## r/gamedev 1vbxk1u "3 Things I have learned making a game with Claude Code" (surf game, 52 comments, heavily downvoted by sub) https://www.reddit.com/r/gamedev/comments/1vbxk1u/
- "When I first sat down I gave Claude a very general description of what I wanted. ... It included features I didn't want, left out features I did want, the UI looked horrible, and the character looked awful. It felt like a completely different game."
- "to this day I haven't been happy with the first version of any major feature. One trick I've learned is to tell Claude not to write any code and instead create a mockup."
- "At the beginning I gave Claude Code my entire vision which was way too much for a single prompt ... I was trying to cram a month of work into one prompt. Now ... I ask it to create an MD file, read through it, make edits or give it more context, then tell Claude Code to read the MD file and execute it. Breaking every big feature into its own MD file helps"

## r/ClaudeGameDev 1wc6hra "Shipped a game with Claude after learning many lessons on context management" (43 upvotes; DeepFury: Idle Berserker, Godot 4, Play Store) https://www.reddit.com/r/ClaudeGameDev/comments/1wc6hra/
- Think -> Design -> Build modes: "The think mode or session is a raw ideation with Claude on core loops and mechanics. Zero lines of code or drawing just ping-ponging ideas. Next, is the design mode where Claude switches roles entirely to build the GDD, palette, assets, and screens ... And finally the build mode where Claude turns the design into an ordered backlog and implements tasks sequentially."
- "ensuring that decisions made on session 1 stay respected on session 20 because they live in a written spec and are traced by a worklog completed at the end of each task." (spec-driven development + EARS requirement syntax)
- "I never run past 30 or maybe 40% of the context window."
- "Don't ask LLMs directly for assets. Ask your agent (which knows your style, palette, and context) to write structured and detailed prompts for the LLM that you use for asset generation instead"

## r/ClaudeCode 1wd01tk same open prompt, two models (382 upvotes, 83 comments, 2026-09) https://www.reddit.com/r/ClaudeCode/comments/1wd01tk/
- Prompt (verbatim): "a game where a fish follows my cursor, super creative and majestic." No follow-ups.
- OP: "Codex did amazing on the design and detail ... Claude did amazing on the mechanics and gameplay. It feels more like an actual game and is more fun to play."
- daaain (220): "the Fable one looks basic on the screenshot, but the animation and the whole thing is more alive, and the Astra one is fancy, but the fish hardly animates and moves completely unnaturally."
- Mikefacts: "Although Astra did better in term of UI, the gameplay experience wasn't good and it was boring."
- Note: a vague prompt lets each model's default priority (visual polish vs motion/feel) decide what the game is.

## r/ClaudeAI 1wnzcbg "I gave Opus 5.5 one prompt and one hour ... then actually played the thing" (2026-09) https://www.reddit.com/r/ClaudeAI/comments/1wnzcbg/
- "Everyone posts the first thirty seconds of their AI-made game and calls it a win. I wanted to know what happens at minute four." Review: https://youtu.be/56oLTK1Jseo (not transcribed). Top comment: "It looks pretty good, but what's the game?"

## r/aigamedev 1uf08jm "I'm tired, man" (91 comments) — 3-year solo MMO/cRPG, "iterated this entire project six times", "1500 pages worth of notes", GDD + spec notes for Claude. Reply _BreakingGood_: "You're in planning hell. 1500 pages is insane." (over-specification + over-scope failure) https://www.reddit.com/r/aigamedev/comments/1uf08jm/

## HN 46548947 "Ask HN: Why isn't AI spawning profitable indie games?" https://news.ycombinator.com/item?id=46548947
- falloutx: "During the vibe coding jam, there were so many games build by AI, but none of them were any good, AI was making three.js games mostly and it was placing objects so stupidly ... in a car came it was placing objects on the road. You can see https://geminimakesrally.vercel.app/"
- amadeuswoo: "The tech isn't the bottleneck, the taste is."

## Godot Forum post-mortem (not Reddit/HN, but canonical failure) https://forum.godotengine.org/t/post-mortem-of-my-failed-attempt-to-vibe-code-a-metroidvania-game/137567
- Gemini/Replit/Cursor/Cline, ~40 hours: player controller in 3–4 hours, then enemy/combat "consistently failed across multiple prompts"; state-machine refactor was "purely cosmetic; actual logic remained unrefactored"; "Fixing one system broke others".

## HN 44463967 (Tower of Time) commenter mgdev: "the leverage you get out of it is exponentially proportional to the quality of your instructions, the structure of your interactions, and the amount of attention you pay to the outputs"

## hydrogen18 Gemini vehicle sandbox (HN 46765599) https://www.hydrogen18.com/blog/google-gemini-3d-game-generation.html
- Success for 2h15m on physics/terrain; asset-loading request derailed: referenced non-existent Kenney files, wrote unneeded loaders, "Removed existing game functionality while attempting model loading", end result "completely unusable" — regression while chasing a peripheral feature.

## r/aigamedev 1v1kt7j "Spent this year fixing 'AI-built' games for indie devs" (153 upvotes, 67 comments; commenters suspect a repost of a generic vibe-coding post) https://www.reddit.com/r/aigamedev/comments/1v1kt7j/
- "The AI specific one: it'll quietly touch systems you weren't even asking about while it's fixing something else. Your movement code was fine last night, you didn't go near it, now it's acting weird. Keep one test scene you click through after any big AI assisted change, catches this fast."
- Vivid_Gas_5755: "mid-session the model rewrote our event queue handling while it was supposed to be fixing a dialogue bug. Nothing broke immediately, which is actually the worst outcome because we shipped it. Found it two weeks later when world state started desynchronizing ... We now have a smoke test that hits every major system after anything AI-assisted"

## r/vibecoding Hormuz Trail (HN 47781289) — Oregon Trail parody, 3 weekends, ~$150 Cursor
- "I can't tell you how often I'd have Sonnet do something, and then find an extra paragraph or two of UI text on a screen where Sonnet thought maybe we needed to tell the user exactly how scoring works." (unrequested additions)
