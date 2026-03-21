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
when usage approaches this limit.

## Workflow

### Step 1: Measure Session Transcript Size

Find and measure the current session's JSONL transcript file:

```bash
# Find the most recently modified .jsonl in the project's Claude sessions dir
# The project path is derived from the current working directory
PROJECT_HASH=$(echo "$PWD" | sed 's|/|-|g; s|^-||')
SESSION_DIR="$HOME/.claude/projects/$PROJECT_HASH"
TRANSCRIPT=$(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -1)
if [ -n "$TRANSCRIPT" ]; then
  BYTES=$(stat -f%z "$TRANSCRIPT" 2>/dev/null || stat -c%s "$TRANSCRIPT" 2>/dev/null)
  MB=$(echo "scale=1; $BYTES / 1048576" | bc)
  echo "Transcript: ${MB}MB ($TRANSCRIPT)"
else
  echo "No transcript found"
fi
```

**Interpreting transcript size** (rough calibration based on observed sessions):
- **< 1 MB**: Early session, plenty of room
- **1-3 MB**: Moderate usage, no concerns
- **3-6 MB**: Substantial session, approaching middle of context
- **6-10 MB**: Heavy session, consider saving state soon
- **> 10 MB**: Likely near compaction — session may have already been compacted

Note: Transcript size in bytes ≠ token count. The JSONL includes tool call metadata,
full file contents from Read calls, and system prompts. A 10MB transcript may use
far more or less than 50% of the 1M token window depending on content. Treat these
thresholds as rough guidance, not precise measurements.

Also check if the session has already been compacted:
```bash
grep -c '"type":"summary"' "$TRANSCRIPT" 2>/dev/null || echo "0"
```
If > 0, the session has been compacted at least once — context was already near-full
at some point.

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
Transcript:      X.X MB  [compacted: N times]
Estimate:        [Early / Moderate / Heavy / Near-limit]

Active Plan
File:   PLAN.md [exists / missing]
Tasks:  X total, Y done, Z remaining, W blocked

Session Handoff
CONTEXT.md:  [exists (date) / missing]
MEMORY.md:   [exists / missing]

Recommendation
[If Heavy/Near-limit: "Consider saving state — run 'update context'"]
[If Early/Moderate: "Plenty of room — continue working"]
```

## Notes

- Context window is 1,000,000 tokens for Claude Opus 4.6
- Auto-compaction is handled by Claude Code automatically — no user action needed
- All important state should be saved to disk (PLAN.md, CONTEXT.md, MEMORY.md)
- If approaching limits, prioritize saving CONTEXT.md before compaction hits
- Transcript size is the best available proxy but is NOT a precise token count
