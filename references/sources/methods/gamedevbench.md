# GameDevBench: Evaluating Agentic Capabilities Through Game Development

- URL: https://arxiv.org/abs/2602.11103
- Authors: Wayne Chi, Yixiong Fang, Arnav Yayavaram, Siddharth Yayavaram, Seth Karten, Qiuhong Anna Wei, Runkun Chen, Alexander Wang, Valerie Chen, Ameet Talwalkar, Chris Donahue (CMU et al.)
- Date: 2026-02-11 (rev. 2026-06-30)
- Why it matters: agents are markedly worse on visual/multimodal game tasks, and giving them visual (image/video) feedback of the running game gives a large lift -- evidence that "look at the running game" must be in the loop.

## Key facts (verbatim where quoted)
- 333 game-dev tasks (Godot); "Agents struggle with game development, with the best agent and method solving only 53.8% of tasks."
- "dropping from 51.4% on gameplay-oriented tasks to 33.0% on 2D graphics tasks"
- "strong correlation between perceived task difficulty and multimodal complexity."
- Tasks need >3x the code changes of prior benchmarks.
- Visual feedback mechanisms (image/video) improved one model "from 41.1% to 52.0%" (fetcher reported model as GPT-4-family; verify in paper before citing the model name).
