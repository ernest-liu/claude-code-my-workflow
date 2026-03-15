---
name: verify-task
description: "Cross-agent task verification loop. After completing work, generates an eval prompt from the task context (PLAN.md, git diff, success criteria), sends it to a second agent via Codex MCP for independent review, then iterates fixes until quality passes. Use when user says \"verify\", \"double check\", \"cross-check\", \"have another agent review\", or wants independent QA on completed work."
argument-hint: "[task-description or 'last task' to auto-detect from PLAN.md]"
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit, Agent, mcp__codex__codex, mcp__codex__codex-reply
---

# Verify Task: Cross-Agent Quality Assurance Loop

After work is completed by the primary agent, this skill:
1. Generates an evaluation prompt from the task context
2. Sends it + all changed files to a second agent (Codex MCP) for independent review
3. Implements fixes based on the review
4. Re-reviews until quality threshold is met or max rounds reached

## Context: $ARGUMENTS

## Constants

- MAX_ROUNDS = 3
- PASS_THRESHOLD = 8/10
- REVIEW_LOG: `VERIFY_LOG.md` in project root (cumulative, overwritten each invocation)
- REVIEWER_MODEL = `gpt-5.4` via Codex MCP (must be an OpenAI model)

## Phase 1: Gather Task Context

Collect everything the reviewer needs to evaluate the work:

### 1a. Identify what was done

Check these sources **in order** (use the first that provides clear context):

1. **$ARGUMENTS** — if user specified a task description, use it
2. **PLAN.md** — read tasks marked `[DONE]` in current session (most recent)
3. **CONTEXT.md** — read "What Was Done" section
4. **git log + git diff** — fall back to recent commits

Produce a **task summary**: 2-5 sentences describing the goal and approach.

### 1b. Collect changed files

```bash
# Get list of files changed (staged + unstaged + recent commits)
git diff --name-only HEAD~3..HEAD 2>/dev/null
git diff --name-only
git diff --cached --name-only
```

Read each changed file in full. For large files (>500 lines), read the relevant sections using git diff to identify changed regions.

### 1c. Identify success criteria

Check these sources:

1. **PLAN.md** — look for "Success Criteria" fields on completed tasks
2. **CLAUDE.md** — look for project-specific quality standards
3. **$ARGUMENTS** — any criteria the user specified

If no explicit criteria exist, infer reasonable ones from the task type:
- **Code changes**: runs without errors, handles edge cases, follows project conventions
- **LaTeX edits**: compiles cleanly, no broken references, consistent notation
- **Config/infrastructure**: no broken paths, all references valid, idempotent
- **Content edits**: accurate, complete, consistent with surrounding material

### 1d. Collect source/reference material

If the task involved transforming or editing existing content:
- Read the **original source** (pre-edit version via `git show HEAD~1:path/to/file`)
- Read any **reference materials** mentioned in PLAN.md or CONTEXT.md

## Phase 2: Generate Eval Prompt

Compose a structured evaluation prompt. This is the key step — the quality of the review depends entirely on how well you frame what the reviewer should check.

**Template:**

```
You are an independent quality reviewer. Your job is to verify that a task
was completed correctly and completely. Be thorough and critical.

## Task Description
[task summary from Phase 1a]

## Success Criteria
[criteria from Phase 1c, numbered]

## Files Changed
[for each file: path, what was changed, and the FULL current content]

## Source/Reference Material (if applicable)
[original content or reference docs, so reviewer can verify accuracy]

## Review Instructions

For each success criterion, evaluate:
1. Is it MET, PARTIALLY MET, or NOT MET?
2. If not fully met, what specifically is wrong or missing?

Additionally check for:
- Errors introduced (typos, bugs, broken references, wrong values)
- Omissions (tasks that were supposed to be done but weren't)
- Inconsistencies (changes that contradict other parts of the project)
- Regressions (things that worked before but are now broken)

## Output Format

1. **Overall Score**: X/10
2. **Verdict**: PASS (score >= 8) / NEEDS FIXES / FAIL
3. **Criteria Assessment**: [numbered list matching success criteria]
4. **Issues Found**: [ranked by severity: CRITICAL > MAJOR > MINOR]
5. **Specific Fixes Required**: [exact file, line, what to change]
```

## Phase 3: Send to Reviewer

```
mcp__codex__codex:
  config: {"model_reasoning_effort": "xhigh"}
  prompt: [eval prompt from Phase 2]
```

Save the threadId for follow-up rounds.

## Phase 4: Parse Review

Extract from the response:
- **Score** (numeric 1-10)
- **Verdict** (PASS / NEEDS FIXES / FAIL)
- **Issues** (list with severity)
- **Specific fixes** (file + what to change)

**STOP CONDITION**: Score >= 8 AND verdict is PASS → skip to Phase 7.

## Phase 5: Implement Fixes (if not passing)

For each issue, highest severity first:

1. **CRITICAL**: Must fix. These are errors, broken functionality, wrong outputs.
2. **MAJOR**: Should fix. Missing items, incomplete work, significant quality gaps.
3. **MINOR**: Fix if straightforward. Style issues, small improvements.

Rules:
- Fix the actual files, don't just acknowledge the issue
- After fixing, verify the fix works (compile, run, check output)
- If a fix requires clarification from the user, note it but don't block on it

## Phase 6: Re-Review

Send updated context to the reviewer:

```
mcp__codex__codex-reply:
  threadId: [saved from Phase 3]
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    [Round N re-review]

    Fixes implemented since your last review:
    1. [Issue]: [What was fixed, how]
    2. [Issue]: [What was fixed, how]

    Updated file contents:
    [full content of fixed files]

    Please re-score. Same format: Score, Verdict, Remaining Issues, Fixes.
```

Parse response → if passing, go to Phase 7. If not, back to Phase 5.

Repeat up to MAX_ROUNDS total.

## Phase 7: Document Results

Write `VERIFY_LOG.md`:

```markdown
# Task Verification Log — [DATE]

## Task
[task summary]

## Success Criteria
[numbered list]

## Review Rounds

### Round 1
- **Score**: X/10
- **Verdict**: [PASS/NEEDS FIXES/FAIL]
- **Issues**: [list]
- **Fixes Applied**: [list]

### Round N (if applicable)
...

## Final Result
- **Score**: X/10 — **[PASS/FAIL]**
- **Rounds**: N of MAX_ROUNDS
- **Remaining Issues** (if any): [list]

## Reviewer Raw Responses

<details>
<summary>Round 1</summary>

[verbatim response]

</details>
```

## Phase 8: Report to User

Present a concise summary:
- Pass/fail with score
- Number of rounds needed
- What was fixed (if anything)
- Any remaining issues that need human judgment

## Key Rules

- ALWAYS read the actual changed files — don't rely on memory of what you wrote
- ALWAYS include full file contents in the eval prompt — the reviewer has no context
- Include source/reference material when the task involves accuracy verification
- Be honest in the eval prompt — don't frame things favorably
- Fix real issues, don't argue with the reviewer
- If the reviewer flags something you disagree with, fix it anyway (trust the second opinion)
- If MAX_ROUNDS exhausted without passing, present remaining issues honestly
