# Building a C compiler with a team of parallel Claudes (Anthropic Engineering)

- URL: https://www.anthropic.com/engineering/building-c-compiler
- Author/org: Nicholas Carlini, Anthropic
- Date: 2026-02-05
- Why it matters: longest published autonomous multi-session run (~100k LOC) and its lessons are all about the VERIFIER: a weak verifier makes agents "solve the wrong problem"; regressions were rampant until CI enforcement; agents are time-blind and burn hours on low-value work.

## Verbatim quotes
- "Claude will work autonomously to solve whatever problem I give it. So it's important that the task verifier is nearly perfect, otherwise Claude will solve the wrong problem."
- Environment designed for Claude: "extensive READMEs and progress files that should be updated frequently with the current status."
- Context pollution: "The test harness should not print thousands of useless bytes. At most, it should print a few lines of output and log all important information to a file."
- "If there are errors, Claude should write ERROR and put the reason on the same line so grep will find it."
- Time blindness: Claude "can't tell time and, left alone, will happily spend hours running tests instead of making progress." Fix: a `--fast` option using "a 1% or 10% random sample" that is "deterministic per-agent but random across VMs."
- "New features and bugfixes frequently broke existing functionality." -> "built a continuous integration pipeline and implemented stricter enforcement that allowed Claude to better test its work."
- Task locking: "Claude takes a 'lock' on a task by writing a text file to current_tasks/"
- When parallel agents all hit the same bug, used "GCC as an online known-good compiler oracle" to isolate failing files so agents could work on different parts.
- Role specialization: "I tasked one agent with coalescing any duplicate code it found. I put another in charge of improving the performance of the compiler itself, and a third I made responsible for outputting efficient compiled code."
- "When a human sits with Claude during development, they can ensure consistent quality and catch errors in real time. For autonomous systems, it is easy to see tests pass and assume the job is done, when this is rarely the case."

## Mapping to games
- A game has no GCC oracle; the nearest equivalents are (a) a scripted "golden path" replay of the first N minutes, (b) spec-derived keypoint tests, (c) a human/agent playtest report. Without one, agents optimize whatever is measurable (polish, refactors).
