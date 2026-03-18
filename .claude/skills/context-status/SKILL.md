---
name: context-status
description: |
  Show current context status and session health.
  Use to check how much context has been used, whether auto-compact is
  approaching, and what state will be preserved.
author: Claude Code Academic Workflow
version: 2.0.0
allowed-tools: ["Read", "Bash", "Glob"]
---

# /context-status — Check Session Health

Show the current session status including context usage estimate, active plan,
and preservation state.

## Context Window

Claude Code Opus has a **1,000,000 token** context window. Auto-compaction triggers
when usage approaches this limit. There is no reliable way to query exact token
usage from within a session — estimates below are rough approximations based on
conversation length and tool calls.

## Workflow

### Step 1: Estimate Context Usage

Provide a qualitative estimate based on session activity:
- **Low** (<25%): Short session, few tool calls, minimal file reads
- **Moderate** (25-50%): Medium session, several file reads and edits
- **High** (50-75%): Long session, many large file reads, extensive tool use
- **Critical** (>75%): Very long session, should save state soon

Note: This is a rough heuristic. If you've read many large files or had extensive
back-and-forth, bias toward higher estimates.

### Step 2: Find Active Plan

```bash
ls -lt PLAN.md 2>/dev/null
```

Read PLAN.md and report:
- How many tasks total
- How many marked [DONE]
- How many remaining
- Any [BLOCKED] items

### Step 3: Check Context Handoff Files

```bash
ls -lt CONTEXT.md 2>/dev/null
ls -lt MEMORY.md 2>/dev/null
```

### Step 4: Report Status

Format the output:

```
Session Status
─────────────────────────────────
Context Window:  1,000,000 tokens (Opus)
Usage Estimate:  [Low / Moderate / High / Critical]

Active Plan
File:   PLAN.md [exists / missing]
Tasks:  X total, Y done, Z remaining, W blocked

Session Handoff
CONTEXT.md:  [exists (date) / missing]
MEMORY.md:   [exists / missing]

Recommendation
[If High/Critical: "Consider wrapping up — run 'update context' to save state"]
[If Low/Moderate: "Plenty of room — continue working"]
```

## Notes

- Context window is 1,000,000 tokens for Claude Opus 4.6
- Auto-compaction is handled by Claude Code automatically — no user action needed
- All important state should be saved to disk (PLAN.md, CONTEXT.md, MEMORY.md)
- If approaching limits, prioritize saving CONTEXT.md before compaction hits
