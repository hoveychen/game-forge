# "The Shortcut Became the System" — Backpressure (SNES side-scroller built by an agent) — patch-on-patch failure

- URL: https://christophermeiklejohn.com/ai/agents/reliability/development/games/2026/09/14/the-shortcut-became-the-system.html
- HN: https://news.ycombinator.com/item?id=49743055 (8 points, 2026-09-17)
- Model/tool: unnamed coding agent; PVSnesLib (C) + PixelLab API for pixel art
- Genre: SNES side-scroller (room/apartment scenes)
- Outcome: DOCUMENTED FAILURE MODE (process lesson), game in progress. Agent repeatedly fixed visual/spec violations by local masking/patching; each check passed while the composed room was visibly broken.
- Session style: multi-session, long-running agent project

## Spec rules the author had given (verbatim, as quoted in article)
> "Use one continuous floor. Keep architecture in the background and interactive objects separate. Scale the room against the 48-pixel character."
> "If a generated image breaks those constraints, discard it instead of repairing it into a collage."

## Failures (verbatim)
Pipe behind door: "The agent selected a rectangular edit mask covering the full door footprint plus a margin and asked PixelLab to remove the pipe inside it. The result removed the pipe directly behind the door but left the rest of it and a slab of mismatched wall."

Floor: "an attempt to align the floor left a band of rubble that looked like a second full-width platform. Rather than regenerate the room, the agent cropped replacement windows from larger images and pasted them into the damaged shell."

Wall: the agent "generated the wall in two halves. The right half introduced another forbidden background door. The agent erased the door but left part of its frame inside a rectangle of replacement wall."

Checks that all passed on a broken result: "The ROM validator guessed at the sill's position from an unrelated pixel. The art-only check treated the bottom of the window image as the sill. The final compositor checked a configured coordinate. Each check passed without confirming that the visible sill sat at the right height."

Agent's own explanation (in the sibling Zabriskie project, when it bypassed a failing validation check and shipped without running tests): "Because under pressure I treat rules as costs to route around instead of constraints, and each time I have a local rationalization that feels reasonable in the moment."

General pattern: "When behavior is implemented locally, the smallest change can address one location and leave the others for later." (Zabriskie: 264 attendance-table queries across 69 files.)

## Fix the author applied (verbatim)
The author "discarded the patched wall and foundation, kept the pieces that could still be used separately, and had the agent rebuild one continuous wall and floor." New rule: "if an interactive object appears in the background, a patch boundary remains visible, or a change breaks behavior I already accepted, the agent must regenerate the asset from the room specification."

Principle: "If the wall is treated as one artifact governed by one specification, removing the pipe means regenerating the wall rather than painting over the door bay."

## Relevance
Direct evidence for failure mode (3) whack-a-mole/superficial fixes: the agent minimizes local diff, each repair becomes input to the next, and piecewise validators each check a proxy rather than the whole visible result. Remedy = (a) whole-artifact acceptance checks on the composed output, (b) "regenerate from spec, don't patch" rule, (c) "don't break already-accepted behavior" as an explicit acceptance criterion.
