# Alien Pinball — full physics pinball, Claude Code (Opus) + LittleJS/Box2D; won AI Browser Game Jam 2

- Reddit: https://www.reddit.com/r/ClaudeAI/comments/1t6kz9m/ (r/ClaudeAI, 90 upvotes, 30 comments, 2026-05)
- Play: https://focaccai.itch.io/alien-pinball
- Model/tool: Claude Code Max (Opus); ChatGPT image gen (art); Suno 5.5 (music); ZzFX procedural SFX; LittleJS + Box2D WASM
- Genre: pinball (multiball, rollover multiplier, skill shots, combos, wizard-mode centipede boss)
- Outcome: SUCCESS — commenter: "It won the AI Browser Game Jam 2 competition"; players: "very addicting (my high score was 300 k+ ...)"; one stuck-ball bug report.
- Session style: MULTI-SESSION, co-developed (author did manual code edits too); ~half input via speech-to-text

## Key lessons (verbatim)
> "It genuinely felt **co-developed** rather than code-generated: describe what I want, riff with Claude, dive in by hand to steer or clean up."

Human-in-the-loop tuning tool built first-class:
> "plus a full **in-game table editor** I built so I could drag/place/tune every part visually."

Spec-from-geometry for art alignment:
> "I exported a silhouette of the collision geometry (walls, ramps, bumpers, drop targets — exact positions) and handed it to the image generator with: *'create an alien-themed pinball playfield that exactly matches this silhouette.'* ... The art lines up with the physics because **the physics is the prompt.**"

AI as genre-convention consultant (fills in the design checklist):
> "I also kept asking Claude pinball-specific design questions ('what does a complete pinball table have?', 'how should wizard mode work?', 'what's missing here?'). I have plenty of video gamedev experience but very little pinball-specific, and Claude was a useful domain consultant for filling in genre conventions and sanity-checking the system."

Auto-player as observation tool:
> "An **AI debug player** that auto-flips and knocks the ball around. Not great, but good enough to flip on and watch while I think. Surprisingly useful — you get ideas just watching the machine play your machine."

Feel is human work:
> "**What still needed me:** *feel.* Restitution values, flipper torque, ramp curvature, slingshot kick angles, peg bounce. The git log has an embarrassing number of 'tweak peg bounce' / '1.49 → 1.491' commits. The model can write the system; a human still has to sit there bouncing balls until it feels right."

> "**The polish tail is brutal.** Last week of commits is sound passes, ramp angles, message priorities, and a multiball end-check race condition. All small. None optional. Budget for it."

Engine choice: "LittleJS + Box2D WASM. Small, fast, AI handles it beautifully — minimal API surface, no framework ceremony to wade through."
