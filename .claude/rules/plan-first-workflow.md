# Plan-First Workflow

**For any non-trivial task, enter plan mode before writing code.**

## The Protocol

1. **Enter Plan Mode** — use `EnterPlanMode`
2. **Check MEMORY.md** — read any `[LEARN]` entries relevant to this task
3. **Requirements Specification (for complex/ambiguous tasks)** — see below
4. **Draft the plan** — what changes, which files, in what order
5. **Write PLAN.md** — save the plan to `PLAN.md` at project root (see template)
6. **Present to user** — wait for approval
7. **Exit plan mode** — only after approval
8. **Implement via orchestrator** — see `orchestrator-protocol.md`

## PLAN.md Structure

Every plan must include for each task:
- **Description** — what needs to be done
- **Files** — exact paths and what to change in each
- **Functions / Variables** — specific names to touch
- **Success Criteria** — how to know the task is complete

Also include:
- **Out of Scope** — what NOT to touch this session
- **Dependencies / Assumptions** — what must be true for the plan to work

Mark tasks `[DONE]` or `[BLOCKED: reason]` as you work through them.

## Step 3: Requirements Specification (For Complex/Ambiguous Tasks)

**When to use:**
- Task is high-level or vague ("improve the lecture", "analyze the data")
- Multiple valid interpretations exist
- Significant effort required (>1 hour or >3 files)

**When to skip:**
- Task is clear and specific ("fix typo in line 42")
- Simple single-file edit
- User has already provided detailed requirements

**Protocol:**
1. Use AskUserQuestion to clarify ambiguities (max 3-5 questions)
2. Mark each requirement:
   - **MUST** (non-negotiable)
   - **SHOULD** (preferred)
   - **MAY** (optional)
3. Declare clarity status for each major aspect:
   - **CLEAR:** Fully specified
   - **ASSUMED:** Reasonable assumption (user can override)
   - **BLOCKED:** Cannot proceed until answered
4. Get user approval on spec
5. THEN proceed to Step 4 (draft the plan) with spec as input

## Context Management

### General Principles
- Prefer auto-compression over `/clear`
- Save important context to disk before it's lost
- `/clear` only when context is genuinely polluted

### Context Survival Strategy

**Before Auto-Compression:**
When approaching context limits, ensure:
1. MEMORY.md has all `[LEARN]` entries from this session
2. `CONTEXT.md` is up to date
3. `PLAN.md` reflects current task status ([DONE] / [BLOCKED] markers)

The pre-compact hook will remind you of this checklist.

**After Compression:**
First message should be: "Resuming after compression." Then read `PLAN.md` + `CONTEXT.md` + `git log --oneline -10`.

## Session Recovery

After compression or new session:
1. Read `PLAN.md` and `CONTEXT.md`
2. Check `git log --oneline -10` and `git diff`
3. State what you understand the current task to be
