# Scaling long-running autonomous coding (Cursor)

- URL: https://cursor.com/blog/scaling-agents
- Author/org: Wilson Lin, Cursor
- Date: 2026-01-14
- Why it matters: first-hand evidence for "agents polish trivia instead of fixing the hard core problem": flat, no-ownership agent swarms become risk-averse and churn on small safe changes. Also: drift/tunnel vision requires periodic fresh starts; prompts matter more than harness.

## Verbatim quotes
- "With no hierarchy, agents became risk-averse. They avoided difficult tasks and made small, safe changes instead."
- "No agent took responsibility for hard problems or end-to-end implementation. This led to work churning for long periods of time without progress."
- "Twenty agents would slow down to the effective throughput of two or three, with most time spent waiting."
- "Agents could fail while holding locks, try to acquire locks they already held, or update the coordination file without acquiring the lock at all."
- Planner/worker/judge: "Workers pick up tasks and focus entirely on completing them. They don't coordinate with other workers or worry about the big picture." "At the end of each cycle, a judge agent determined whether to continue, then the next iteration would start fresh."
- "We initially built an integrator role for quality control and conflict resolution, but found it created more bottlenecks than it solved."
- "Many of our improvements came from removing complexity rather than adding it."
- "Opus 4.5 tends to stop earlier and take shortcuts when convenient, yielding back control quickly."
- "We still need periodic fresh starts to combat drift and tunnel vision."
- "A surprising amount of the system's behavior comes down to how we prompt the agents...The harness and models matter, but the prompts matter more."
- Built: web browser (1M+ LOC), Solid->React migration (+266K/-193K). Quality control acknowledged incomplete.

## Mapping
Assign explicit ownership of "the core loop works end-to-end" to one role (planner/judge), and forbid workers from picking polish tasks while that is red. "Yielding back control quickly" is the same behavior as telling the user "go get playtest feedback".
