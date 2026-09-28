# Effective context engineering for AI agents (Anthropic Engineering)

- URL: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Org: Anthropic Applied AI team, 2025-09-29
- Why it matters: explains WHY relayed sessions drift -- context rot, and what to persist across sessions (notes, not transcripts). Secondary relevance.

## Verbatim quotes
- "as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases." (context rot; "attention budget")
- Guiding principle: find the "smallest set of high-signal tokens that maximize the likelihood of your desired outcome."
- "Compaction distills the contents of a context window in a high-fidelity manner, enabling the agent to continue with minimal performance degradation." Claude Code keeps architectural decisions and unresolved bugs, discards redundant tool output.
- Structured note-taking: "Claude playing Pokémon demonstrates how memory transforms agent capabilities" -- maintaining "precise tallies across thousands of game steps" and "maps of explored regions".
- Sub-agents return "only a condensed, distilled summary of its work (often 1,000-2,000 tokens)."
- Just-in-time: keep "lightweight identifiers" and load data at runtime via tools.

## Mapping
Handoff notes should carry: current core-loop status (pass/fail of golden path), open blocking bug, last playtest verdict -- not a narrative of polish done.
