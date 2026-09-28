# The Long Silence (Anshu Chimala, @anshuc) — "vibe + verifiable bar" seed prompt, then a 24-hour /goal with an un-relaxable judge

- **Source URL:** https://x.com/anshuc/status/2081801966158811506 (2026-07-27). The prompts are verbatim in the author's self-reply https://x.com/anshuc/status/2081801979131818412
- **Model/tool:** Claude Opus 5 in Claude Code (seed prompt at high effort, /goal at max effort), with parallel subagents, Blender MCP, and a self-authored "blender-hardsurface" skill
- **Genre:** Space exploration (Outer Wilds / Starfield-like): walkable ship interior, cockpit piloting, procedural universe with planets and derelicts, a mystery narrative ("The Choir", 7 Resonators)
- **Result evidence:** Playable at https://longsilence.anshu.dev ; code at https://github.com/achimala/TheLongSilence (README has verification tools: levels.mjs clip/percentile metrics, survey/play/probe/sheet scripts)
- **Quality signal:** ~662k views / 3.7k likes (fxtwitter). Covered by 36kr, vc.ru ("Claude Opus 5 built its own Starfield in 24 hours"). README refuses mobile: "Phones are turned away at the door... a bad first impression is worse than none."
- **One-shot vs iterative:** The author says "This took a few steps, not one-shot. But the process was simple and almost entirely hands-off." Steps: (0) set up Blender MCP, iterate on a spaceship model by hand, and dump the learnings into a skill; (1) seed prompt; (2) 24h /goal run; (3) the judge was never satisfied, so he stopped it manually; he steered a few times from his phone (e.g. refocus from planets to ship interior); (4) separate sessions fixed rendering glitches, cleanup, deploy.
- **Failure/limit note:** "Claude did not actually finish the goal. The judge kept critiquing and it kept going overnight, then I manually stopped it." An un-satisfiable judge turns the run into "run until the human stops it".

## Verbatim author thread (includes both prompts)

Play it yourself: https://longsilence.anshu.dev

Code: https://github.com/achimala/TheLongSilence

This took a few steps, not one-shot. But the process was simple and almost entirely hands-off.

Two main ideas:
1) Adversarial subagent, based on @mattshumer_'s Claude of Duty prompt: Have an independent agent critique screenshots of the game compared to AAA space games like Starfield. Claude is not allowed to stop till the critic says it looks just as good.
2) Blender MCP so Claude can model its own assets

How I set it up:
- Just told Claude Code to install Blender MCP, and it found it and did it
- Asked Claude to use it to model a spaceship
- Went back and forth giving it feedback until the model looked great
- Had Claude dump all its learnings to a skill

The skill is "blender-hardsurface". You can find it in GitHub above.

---

This prompt built the first version of the game (high effort):

This is an empty repo. I want you to build a space exploration game using Three.js. Don't ask me questions, just build whatever game mechanics you think would be cool to evoke a sense of exploration. The primary non-negotiable thing is that it needs to look absolutely mind-blowing, AAA game studio quality, unlike anything anyone's ever seen from a web game. I want a photorealistic aesthetic here, not low-res/low-poly or the usual plasticky/shiny artificial look that games often have.

I want the game to have the player piloting a ship through space. They should be able to walk around the ship and interact with various elements and controls, but also sit down at the cockpit and pilot the ship around space. Sweat all the details to a AAA game quality bar: graphics, storyline, sound, even menus and HUD elements. Build everything yourself, don't download external assets or code (beyond three.js)

Build a core game loop around this idea. User should fly the ship, discover things, learn, build towards some goal, have a reason to go to the next place and keep exploring. Make it easy to understand and guide the player through the game (without just force-feeding them a bunch of tutorials/popups - show, don't tell). I want the immense scale of space to really come through, but you need to balance that with not making flying around tedious.

You must verify everything yourself in browser and make sure the game works correctly end to end at smooth 60fps. When you think you're done, take a screenshot. If it doesn't look like a AAA game or a literal photo of space, you're not done, improve the graphics.

---

The massive goal session that overhauled the visuals over 24 hours (max effort):

/goal I want you to make this game absolutely mind blowing visually - review in browser and pull out all the stops. Keep everything procedurally generated but push as hard as possible on the visuals, do everything custom if you need to. Delegate work to parallel subagents to work efficiently.

The universe should feel alive, with tons of things to do. You should be able to fly anywhere, meet other ships, and land on the planets. Everything should have gorgeous cutscenes and feel fluid, with no abrupt cuts.

You have access to Blender, running on this laptop. Read the Blender skill and have a subagent use it to model high-quality assets. I think you cannot parallelize this so you will need to queue it up for that agent. Right now many assets look blocky and obviously procedural. I don't want to see anything like this; I want to see intentional, beautiful 3d models.

There are various artifacts: z-fighting, weird banding, etc. You need to dump sheets of frames across cutscenes and gameplay, look for these, and fix them.

Goal verification: Set up an independent, impartial judge subagent. This should literally look at screenshots of AAA space games like Starfield, compare to screenshots of our games, and provide specific criticism, then you must address it. Your goal is to reach that level of visual fidelity at 60fps in browser. You cannot mark the goal done until the judge says our game actually looks as good as the AAA games. The judge must consider meshes, textures, lighting, shader effects, menus, transitions, etc. in its assessment. Every aspect of the visuals, in detail. You cannot alter the judge's prompt to try to relax this condition. You are capable of reaching this bar - try your hardest and don't give up.

---

Claude did not actually finish the goal. The judge kept critiquing and it kept going overnight, then I manually stopped it.

Claude mostly ran autonomously, but I watched from my phone and steered a few times to change its priorities (it was spending a lot of time on space/planets and I wanted it to focus on the ship interior, for example). But the vast majority of the work happened while I was AFK or asleep.

After I stopped the big goal run I had a couple separate Claudes fix a few rendering glitches so I could record the demo, then handle cleanup and deployment.