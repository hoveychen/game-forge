# Demystifying evals for AI agents (Anthropic Engineering)

- URL: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Org: Anthropic, 2026-01-09
- Why it matters (secondary): guidance for building the game-quality grader itself -- mix code graders (deterministic playthrough checks) with calibrated model graders (fun/feel rubric) and periodic human grading.

## Verbatim quotes
- "it's often better to grade what the agent produced, not the path it took."
- Code-based graders: "Fast, Cheap, Objective, Reproducible, Easy to debug" but "Brittle to valid variations."
- Model-based graders: "Flexible, Scalable, Captures nuance" but "Non-deterministic" and "More expensive than code."
- Human graders: "Gold standard quality" but "Expensive, Slow".
- Example subjective assertions: "Agent showed empathy for customer's frustration"; "Resolution was clearly explained."
- "LLM-based rubrics should be frequently calibrated against expert human judgment to grade these agents effectively."
- "You won't know if your graders are working well unless you read the transcripts and grades from many trials."
- "Eval saturation occurs when an agent passes all of the solvable tasks, leaving no room for improvement."
