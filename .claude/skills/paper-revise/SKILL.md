---
name: paper-revise
description: "Iterative paper revision with visual diff review. Makes proposed changes to a copy, generates a latexdiff PDF for review, then accepts/rejects items per user feedback. Loops until no further changes. Use when user says \"revise draft\", \"edit paper iteratively\", \"propose changes\", or wants a review-accept-reject workflow on a LaTeX file."
argument-hint: "[path/to/draft.tex] [optional: revision instructions]"
allowed-tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Agent"]
---

# Paper Revise: Iterative Diff-Based Editing

Interactive loop: propose changes → visual diff → user accepts/rejects → apply → repeat.

## Context: $ARGUMENTS

## Constants

- REVISION_LOG: `REVISION_LOG.md` in the same directory as the draft
- Max rounds: unlimited (user controls termination)

## Phase 1: Setup

### 1a. Identify the draft

Parse $ARGUMENTS to find the .tex file path. Strip `.tex` if needed:

```bash
DRAFT="${ARGUMENTS%.tex}"
```

Verify `${DRAFT}.tex` exists. If not, search for likely candidates and ask.

### 1b. Read the draft

Read `${DRAFT}.tex` in full. Understand:
- Document structure (sections, subsections)
- Writing style and notation conventions
- Any TODO/FIXME markers

### 1c. Determine revision goals

If $ARGUMENTS includes revision instructions beyond the filename, use those.
Otherwise, ask the user what kind of revisions they want:
- General polish (clarity, flow, tightness)
- Specific section rewrites
- Responding to referee comments
- Notation consistency
- Adding/removing content

### 1d. Create initial proposed copy

```bash
cp "${DRAFT}.tex" "${DRAFT}_proposed.tex"
```

### 1e. Initialize revision log

Create `REVISION_LOG.md` with header and timestamp.

## Phase 2: Propose Changes (start of each round)

### 2a. Make changes to the proposed file

Edit `${DRAFT}_proposed.tex` with your proposed revisions. For each change:
- Number it sequentially (Item 1, Item 2, ...)
- Keep a mental list of what each numbered item is

**Rules for proposing changes:**
- Make each change atomic and independently accept/rejectable
- Don't make changes that depend on other changes being accepted (when possible)
- Prefer targeted surgical edits over wholesale rewrites
- Preserve the author's voice — improve, don't replace

### 2b. Generate numbered change summary

Before generating the diff, write a summary of all proposed changes:

```
Proposed Changes (Round N):
  1. [Section X.X] Tightened opening paragraph — removed redundant clause
  2. [Section X.X] Replaced "it is clear that" with direct statement
  3. [Eq. (5)] Fixed notation: \beta_i → \beta_{i,t} for consistency
  4. [Section X.X] Added transition sentence between paragraphs
  5. [Table 2] Clarified column header
  ...
```

Present this summary to the user BEFORE generating the diff PDF, so they know
what each numbered item refers to when reviewing the diff.

### 2c. Generate visual diff

```bash
gitdiff "${DRAFT}" "${DRAFT}_proposed" "${DRAFT}_diff"
```

This runs `latexdiff` and compiles to PDF. After each diff compilation, clean aux files:

```bash
find . -maxdepth 1 -type f \( -name "${DRAFT}_diff.aux" -o -name "${DRAFT}_diff.log" -o -name "${DRAFT}_diff.out" -o -name "${DRAFT}_diff.nav" -o -name "${DRAFT}_diff.snm" -o -name "${DRAFT}_diff.toc" -o -name "${DRAFT}_diff.synctex.gz" -o -name "${DRAFT}_diff.bbl" -o -name "${DRAFT}_diff.blg" -o -name "${DRAFT}_diff.fls" -o -name "${DRAFT}_diff.fdb_latexmk" \) -delete
```

If `gitdiff` fails:
1. Check for latexdiff compatibility issues (e.g., math mode changes)
2. Try with `--math-markup=0` flag if math causes problems:
   ```bash
   latexdiff --math-markup=0 "${DRAFT}.tex" "${DRAFT}_proposed.tex" > "${DRAFT}_diff.tex"
   pdflatex -interaction=nonstopmode "${DRAFT}_diff.tex"
   pdflatex -interaction=nonstopmode "${DRAFT}_diff.tex"
   open "${DRAFT}_diff.pdf"
   ```
3. If still failing, fall back to showing a text-based diff

### 2d. Present to user

Tell the user:
```
Round N: X changes proposed. Diff PDF opened.

[Numbered change summary from 2b]

Review the diff and tell me which to accept/reject/modify.
Example: "accept 1,2,3, reject 4, change 5 to use 'furthermore' instead"
Or: "accept all" / "reject all" / "looks good, we're done"
```

## Phase 3: Process User Feedback

Parse the user's response. They may say:

### "accept all" or "looks good"
- Copy `${DRAFT}_proposed.tex` → `${DRAFT}.tex`
- Ask if they want another round of changes or are done

### "accept X,Y,Z — reject A,B,C — change D,E,F"
Apply in this order:

**Step 1: Start from current draft.tex**
Read `${DRAFT}.tex` as the base.

**Step 2: Apply accepted items**
For each accepted item number, apply that specific change from `_proposed.tex` to `${DRAFT}.tex`.

**Step 3: Skip rejected items**
These stay as-is in `${DRAFT}.tex` (no change needed — they were only in `_proposed`).

**Step 4: Apply modified items**
For items the user wants changed differently, apply the user's version (not the original proposal and not the draft original).

**Step 5: Save updated draft**
Write the result to `${DRAFT}.tex`.

**Step 6: Prepare next round**
```bash
cp "${DRAFT}.tex" "${DRAFT}_proposed.tex"
```

→ Go back to Phase 2 for the next round of proposals.

### "done" / "no more changes" / "that's it"
→ Go to Phase 4.

## Phase 4: Finalize

### 4a. Ensure draft and proposed are identical

```bash
diff "${DRAFT}.tex" "${DRAFT}_proposed.tex"
```

If they differ, copy draft to proposed:
```bash
cp "${DRAFT}.tex" "${DRAFT}_proposed.tex"
```

### 4b. Clean up diff artifacts

```bash
rm -f "${DRAFT}_diff.tex" "${DRAFT}_diff.pdf"
find . -maxdepth 1 -type f \( -name "${DRAFT}_diff.*" \) -delete
# Clean aux files from diff compilation
find . -maxdepth 1 -type f \( -name "*.aux" -o -name "*.log" -o -name "*.out" -o -name "*.synctex.gz" \) -delete
```

### 4c. Update revision log

Append final summary to `REVISION_LOG.md`:
```markdown
## Final Summary
- Total rounds: N
- Total changes proposed: X
- Accepted: Y
- Rejected: Z
- Modified: W
```

### 4d. Report to user

```
Revision complete after N rounds.
- X changes accepted, Z rejected, W modified
- ${DRAFT}.tex is updated
- ${DRAFT}_proposed.tex matches draft (clean state)
- Diff artifacts cleaned up
```

## Key Rules

- NEVER edit `${DRAFT}.tex` directly during Phase 2 — only edit `_proposed.tex`
- Number every change so the user can reference them precisely
- Present the numbered summary BEFORE the diff PDF — the PDF shows visual changes but the numbers are your shared vocabulary
- Each change should be independently accept/rejectable — avoid entangled edits
- If latexdiff fails on complex math, use `--math-markup=0` or `--math-markup=3`
- Always clean up aux files after compilation
- Keep `_proposed.tex` as a working copy — it gets overwritten each round
- The user's word is final — if they reject a change, don't re-propose it next round unless they ask
