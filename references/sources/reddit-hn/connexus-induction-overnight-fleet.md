# Connexus + Induction — two shipped mobile puzzle games; Induction built overnight by an orchestrated Claude Code fleet from a plan folder

- Reddit: https://www.reddit.com/r/ClaudeGameDev/comments/1wc25xu/ (r/ClaudeGameDev, 7 upvotes, 2026-09) — low engagement, self-reported
- Play Induction (browser): https://connexuspuzzles.com/induction/play ; iOS/Android links in post
- Model/tool: Claude Code (Opus, later "Fable"), multi-agent orchestration (coordinator + per-story workers on branches/PRs); Codex as adversarial PR reviewer; Flutter/Supabase
- Genre: daily puzzle collection (Connexus, 8 months) and Black-Box-style deduction puzzle (Induction, ~1 week)
- Outcome: SUCCESS (shipped on both stores). Induction: "By morning: 15 stories done as 14 reviewed PRs, ~900 tests, playable. A week of polish and store wiring later it was live on both stores." No independent quality evidence.
- Session style: overnight autonomous multi-agent run from a pre-written plan folder, then a week of human-directed polish

## Spec/process (verbatim)
> "I wrote a plan folder (stories, a decisions file, a 'discoveries' file for gotchas), then ran an orchestrated fleet of Claude Code agents against it overnight."
> "Workers had to read a decisions file and a discoveries file before touching code as well as write back findings and downstream effects for the Orchestrator agent to react to."
> "It works from an md per directory that states architectural invariants (server-authoritative writes, encrypted local cache, 'never compute coin deltas client-side') and a TDD rule: write the failing test first, then the code."
> Content pipeline: "every puzzle runs through a deterministic solver so it can't ship unless a machine proves it has exactly one solution."

What worked:
> "A plan-of-record folder agents must read first. The decisions file ('streaks only count completions', 'never mention another app in-game') stopped agents from re-litigating settled calls."
> "Test-pinning every ruling. If a rule matters, there's a test that fails when an agent 'helpfully' changes it."
> "A second model reviewing the first. Claude and Codex disagree in useful ways."

What didn't:
> "Agents love flipping flags they don't understand. I had to write 'NEVER re-enable retired puzzle types' in caps after the third time."
> "'All tests green' on a fresh branch means nothing when the baseline has ~60 chronic failures. Always get a baseline first."

## Relevance
Puzzle games have a mechanically verifiable notion of "correct content" (unique-solution solver) — a content-quality gate that is machine-checkable. Decision log + test-pinned rulings are the antidote to agents re-litigating/undoing accepted behavior.
