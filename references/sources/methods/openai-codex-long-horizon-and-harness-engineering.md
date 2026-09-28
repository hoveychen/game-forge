# OpenAI: "Run long horizon tasks with Codex" + "Harness engineering: leveraging Codex in an agent-first world"

## A. Run long horizon tasks with Codex
- URL: https://developers.openai.com/blog/run-long-horizon-tasks-with-codex
- Org: OpenAI Developers blog (author reported by search as Derrick Choi; page itself did not show a byline), Feb 2026
- Run: ~25 hours uninterrupted, ~13M tokens, ~30k LOC, built a design tool from a blank repo.

Four durable files (verbatim purposes):
- Prompt.md (spec): "Purpose: Freeze the target so the agent doesn't 'build something impressive but wrong.'" Sections: goals, non-goals, hard constraints, deliverables, "Done when" checks.
- Plans.md (milestones): "Purpose: Turn open-ended work into a sequence of checkpoints the agent can finish and verify." Milestones sized for one loop, acceptance criteria, validation commands, decision notes.
- Implement.md (runbook): "Purpose: This is the runbook. It tells Codex exactly how to operate: follow the plan, keep diffs scoped, run validations, update docs."
- Documentation.md (audit log): "Purpose: This is the shared memory and audit log. It's how I can step away for hours and still understand what happened."
Rules: "Run validation after each milestone (fix failures immediately)" and "Keep diffs scoped (don't expand scope)."

## B. Harness engineering (Ryan Lopopolo, OpenAI, 2026-02-11)
- URL: https://openai.com/index/harness-engineering/ (403 to fetcher; quotes below via mirror https://businessdatasolutions.github.io/ai-wiki/sources/2026-02-11-lopopolo-codex-harness-engineering -- treat as secondary)
- ~1M LOC product, zero human-written lines, 5 months. "Humans steer. Agents execute."
- App legibility: "Codex can launch one app instance per git worktree, take DOM snapshots, take screenshots, navigate, and reason about UI behaviour directly."
- Bug loop: "select target → snapshot before → trigger UI path → snapshot after → apply fix → re-run validation until clean."
- End-to-end: "Given a single prompt, the agent can now: validate the current state of the codebase; reproduce a reported bug; record a video demonstrating the failure; implement a fix; validate the fix by driving the application; record a second video demonstrating the resolution; open a pull request; respond to agent and human feedback; detect and remediate build failures; escalate to a human only when judgment is required; merge the change."
- AGENTS.md: one big file "failed in four predictable ways"; replaced with "progressive disclosure: a ~100-line top-level AGENTS.md that maps to deeper sources".
- Continuous cleanup: "Technical debt is like a high-interest loan: it's almost always better to pay it down continuously in small increments than to let it compound."

## Mapping to games
- "Reproduce before fix, with a before/after recording" is the direct antidote to whack-a-mole: a fix without a reproduced failure is not accepted.
- Prompt.md "non-goals" + "Done when" is the mechanism to stop polishing irrelevant details.
