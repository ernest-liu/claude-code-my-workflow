# Session Logging

**Use `CONTEXT.md` at project root as the session state handoff file.**

## Session Start

1. Read `PLAN.md` — your task list
2. Read `CONTEXT.md` — state from previous session
3. Confirm scope with user before starting

## During Session

Append 1-3 lines to `CONTEXT.md` whenever:
- A design decision is made
- A problem is solved
- The user corrects something
- The approach changes

Do not batch — log incrementally.

## Session End

When the user says "wrap up", "end session", or "update context":

Write a fresh `CONTEXT.md` with:
- **What Was Done** — completed tasks with file paths
- **Current State** — what works, what's built
- **Pending** — uncompleted tasks from PLAN.md
- **Open Questions** — unresolved decisions needing user input
- **Warnings / Gotchas** — fragile logic, dependencies, workarounds

Also update `PLAN.md` — mark all completed tasks `[DONE]`.
