# Effective harnesses for long-running agents (Anthropic Engineering)

- URL: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Author/org: Justin Young, Anthropic
- Date: 2025-11-26
- Companion code: https://github.com/anthropics/claude-quickstarts (autonomous-coding quickstart), also https://github.com/anthropics/cwc-long-running-agents

## Architecture
- "The very first agent session uses a specialized prompt that asks the model to set up the initial environment: an `init.sh` script, a claude-progress.txt file that keeps a log of what agents have done, and an initial git commit that shows what files were added."
- "Every subsequent session asks the model to make incremental progress, then leave structured updates."
- "Given this initial environment scaffolding, the next iteration of the coding agent was then asked to work on only one feature at a time."

## Feature list (anti "declare victory early")
- Initializer writes a comprehensive feature list, all initially failing. "In the claude.ai clone example, this meant over 200 features, such as 'a user can open a new chat, type in a query, press enter, and see an AI response.'"
- "We prompt coding agents to edit this file only by changing the status of a passes field."
- Strong wording: "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."
- "We landed on using JSON for this, as the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files."

Example entry (verbatim):
```json
{
    "category": "functional",
    "description": "New chat button creates a fresh conversation",
    "steps": [
      "Navigate to main interface",
      "Click the 'New Chat' button",
      "Verify a new conversation is created",
      "Check that chat area shows welcome state",
      "Verify conversation appears in sidebar"
    ],
    "passes": false
  }
```

## Session start: smoke-test before new work (directly relevant to "breaks in first 3 steps")
- "Start the session by reading the progress notes file and git commit logs, and run a basic test on the development server to catch any undocumented bugs."
- Session checklist: run `pwd`; "Read the git logs and progress files to get up to speed on what was recently worked on"; "Read the features list file and choose the highest-priority feature that's not yet done"; run init.sh and verify basic functionality before implementing new features.
- Transcript line: "Excellent! Now let me navigate to the application and verify that some fundamental features are still working."
- "If the agent had instead started implementing a new feature, it would likely make the problem worse."

## Testing as a user
- "Claude mostly did well at verifying features end-to-end once explicitly prompted to use browser automation tools and do all testing as a human user would."
- Failure-mode table: "Marking features done without testing" -> require self-verification and explicit testing before marking complete. "Declaring victory prematurely" -> comprehensive feature list read at session start.

## Clean state
- Ask the model to "commit its progress to git with descriptive commit messages and to write summaries of its progress in a progress file."

## Stated limitations / future work
- "Claude can't see browser-native alert modals through the Puppeteer MCP, and features relying on these modals tended to be buggier."
- "Some issues remain, like limitations to Claude's vision and to browser automation tools making it difficult to identify every kind of bug."
- "It seems reasonable that specialized agents like a testing agent, a quality assurance agent, or a code cleanup agent, could do an even better job at sub-tasks."
