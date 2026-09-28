# Harness design for long-running application development (Anthropic Engineering)

- URL: https://www.anthropic.com/engineering/harness-design-long-running-apps
- Author/org: Prithvi Rajasekaran, Anthropic
- Date: 2026-03-24
- Why it matters: the headline example is literally a GAME (2D retro game maker with playable test mode). Solo run produced a game where nothing responded to input; planner+generator+evaluator harness produced a playable one.

## Test prompt (verbatim)
> "Create a 2D retro game maker with features including a level editor, sprite editor, entity behaviors, and a playable test mode."

## Solo-run failure (same as our failure mode 1)
- "The layout wasted space, with fixed-height panels leaving most of the viewport empty."
- "the actual game was broken. My entities appeared on screen but nothing responded to input."
- "the wiring between entity definitions and the game runtime was broken, with no surface indication of where."

## Full harness result
- "I was actually able to move my entity and play the game. The physics had some rough edges—my character jumped onto a platform but ended up overlapping with it, which felt intuitively wrong—but the core thing worked, which the solo run did not manage."
- Remaining UX gap: workflow "didn't make it clear that you should build sprites and entities before trying to populate a level."
- Cost: Solo 20 min / $9 vs Full harness 6 hr / $200. "The harness was over 20x more expensive, but the difference in output quality was immediately apparent."

## Planner
- Instructed to "be ambitious about scope and to stay focused on product context and high level technical design rather than detailed technical implementation."
- "the planner step expanded that prompt into a 16-feature spec spread across ten sprints" including "sprite animation system, behavior templates, sound effects and music, an AI-assisted sprite generator and level designer, and game export."

## Evaluator (separate agent, skeptical, uses the app like a user)
- Uses "the Playwright MCP to click through the running application the way a user would, testing UI features, API endpoints, and database states."
- Hard thresholds: "if any one fell below it, the sprint failed."
- Self-evaluation bias: "When asked to evaluate work they've produced, agents tend to respond by confidently praising the work—even when, to a human observer, the quality is obviously mediocre." / "agents reliably skew positive when grading their own work"
- "tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work."
- Caveat: "the evaluator is still an LLM that is inclined to be generous towards LLM-generated outputs."
- Tuning loop: "The tuning loop was to read the evaluator's logs, find examples where its judgment diverged from mine, and update the QAs prompt." Calibrated with "few-shot examples with detailed score breakdowns".
- Example evaluator findings (verbatim, from the game maker run):
  - "Rectangle fill tool allows click-drag to fill a rectangular area with selected tile — FAIL — Tool only places tiles at drag start/end points instead of filling the region."
  - "User can select and delete placed entity spawn points — FAIL — Delete key handler requires both `selection` and `selectedEntityId` to be set, but clicking an entity only sets `selectedEntityId`."
- Catching display-only / stubbed features (DAW run): "The main failure point is Feature Completeness — while the app looks impressive and the AI integration works well, several core DAW features are display-only without interactive depth: clips can't be dragged/moved on the timeline, there are no instrument UI panels (synth knobs, drum pads), and no visual effect editors (EQ curves, compressor meters)." / "Audio recording is still stub-only (button toggles but no mic capture)."

## Sprint contracts
- "the generator and evaluator negotiated a sprint contract: agreeing on what 'done' looked like for that chunk of work before any code was written."
- "The generator proposed what it would build and how success would be verified, and the evaluator reviewed that proposal to make sure the generator was building the right thing."
- "Communication was handled via files: one agent would write a file, another agent would read it and respond either within that file or with a new file."

## Subjective-quality rubric (frontend design; template for "fun" rubric)
- Design quality: "Does the design feel like a coherent whole rather than a collection of parts?"
- Originality: "Is there evidence of custom decisions, or is this template layouts, library defaults, and AI-generated patterns?"
- Craft: "Technical execution: typography hierarchy, spacing consistency, color harmony, contrast ratios."
- Functionality: "Usability independent of aesthetics. Can users understand what the interface does?"
- Criteria language like "the best designs are museum quality"; penalized "telltale signs of AI generation like purple gradients over white cards"; originality and design quality weighted more heavily.
- Iteration effect: "By the ninth iteration, it had produced a clean, dark-themed landing page ... Then, on the tenth cycle, it scrapped the approach entirely and reimagined the site as a spatial experience" (the skeptical grader drove a non-incremental rethink rather than polish).

## Meta
- Evaluator "is worth the cost when the task sits beyond what the current model does reliably solo."
- "When a new model lands, it is generally good practice to re-examine a harness, stripping away pieces that are no longer load-bearing to performance."
