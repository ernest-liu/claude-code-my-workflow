# CLAUDE.MD -- Academic Project Development with Claude Code

<!-- HOW TO USE: Replace [BRACKETED PLACEHOLDERS] with your project info.
     Keep this file under ~150 lines — Claude loads it every session. -->

**Project:** [YOUR PROJECT NAME]
**Institution:** [YOUR INSTITUTION]
**Branch:** main

---

## Session Startup Protocol

At the start of every session, before doing anything else:

1. Read `PLAN.md` if it exists. This is your task list for the session.
2. Read `CONTEXT.md` if it exists. This is the state handoff from the previous session.
3. Briefly confirm to the user: what tasks you see in PLAN.md, and any critical context from CONTEXT.md.
4. Ask if the user wants to proceed, modify scope, or reprioritize.

## Executing PLAN.md

- Work through tasks in the order listed unless the user says otherwise.
- Each task specifies: description, file paths, function/variable names, and success criteria. Use these precisely — do not infer file locations or function names.
- After completing each task, mark it `[DONE]` in PLAN.md and report completion before moving on.
- If a task is blocked, mark it `[BLOCKED: reason]` in PLAN.md and surface it immediately.

## Session End Protocol

When the user says "wrap up", "end session", or "update context", write a fresh `CONTEXT.md`:

```
# Session Context — [DATE]
## What Was Done
[Bullet list of completed tasks with file paths affected]
## Current State
[What works, what's been built]
## Pending
[Uncompleted tasks from PLAN.md with notes on partial progress]
## Open Questions
[Unresolved decisions or ambiguities needing user input]
## Warnings / Gotchas
[Fragile logic, naming conventions, dependencies, workarounds]
```

---

## Core Principles

- **Plan first** -- use `PLAN.md` for non-trivial tasks; enter plan mode for complex ones
- **Verify after** -- compile/render and confirm output at the end of every task
- **Quality gates** -- nothing ships below 80/100
- **[LEARN] tags** -- when corrected, save `[LEARN:category] wrong → right` to MEMORY.md
- **No silent changes** -- never rename or restructure files outside PLAN.md without asking

---

## Writing Style

When writing academic papers, lead with narrative and economic intuition — open with the core question or puzzle, ground abstract ideas in concrete examples and analogies, and build a clear story arc so the reader understands the big idea within the first page. Use running examples and real-world illustrations to anchor theoretical results. Keep sentences as concise as clarity allows, and weave literature references into the argument rather than cataloging them in separate enumerated sections. At the same time, be thorough: systematically enumerate distinct mechanisms and channels when presenting model results, preview key findings in the introduction, and address potential concerns and caveats upfront. When these two impulses conflict — concise narrative versus exhaustive coverage — favor the narrative. Completeness should serve the story, not bury it.

---

## Folder Structure

```
[YOUR-PROJECT]/
├── CLAUDE.md                    # This file (loaded every session)
├── PLAN.md                      # Task list for current session
├── CONTEXT.md                   # State handoff from previous session
├── .claude/                     # Rules, skills, agents, hooks
├── bibliography_base.bib        # Centralized bibliography
└── raw/                         # Reference papers, data, supporting materials
```

**On-demand folders** — create only when needed:
- `figures/` — when the project has figures or images
- `slides/` — when the project has Beamer/Quarto slides
- `output/` — when compiled PDFs or artifacts are generated
- `tools/` — when the project has helper scripts

---

## Overleaf Integration

If this project syncs with Overleaf, **only push files needed for compilation**.
Claude infrastructure stays local via `.gitignore`.

**What goes to Overleaf:** `.tex`, `.bib`, `.sty`, `.cls`, `figures/`, `.bst`
**What stays local:** `.claude/`, `CLAUDE.md`, `PLAN.md`, `CONTEXT.md`, `MEMORY.md`, `raw/`, `*_proposed.tex`, `*_diff.*`

**Setup:** Uncomment the "Overleaf Integration" block in `.gitignore`.

**Workflow with `/paper-revise`:**
1. Pull latest from Overleaf: `git pull overleaf main`
2. Run `/paper-revise draft.tex` — edits stay local until accepted
3. Accepted changes go into `draft.tex`
4. Push to Overleaf: `git push overleaf main`
5. Coauthor sees only the final `.tex` changes — no Claude artifacts

---

## Commands

```bash
# LaTeX (3-pass, XeLaTeX only)
cd slides && xelatex -interaction=nonstopmode file.tex
BIBINPUTS=..:$BIBINPUTS bibtex file
xelatex -interaction=nonstopmode file.tex
xelatex -interaction=nonstopmode file.tex

# MANDATORY: Clean aux files after EVERY compilation (no auto-hook exists)
find . -maxdepth 1 -type f \( -name "*.aux" -o -name "*.log" -o -name "*.nav" \
  -o -name "*.out" -o -name "*.snm" -o -name "*.toc" -o -name "*.vrb" \
  -o -name "*.bbl" -o -name "*.blg" -o -name "*.bcf" -o -name "*.run.xml" \
  -o -name "*.synctex.gz" -o -name "*.fls" -o -name "*.fdb_latexmk" \
  -o -name "*-blx.bib" \) -delete
```

---

## Quality Thresholds

| Score | Gate | Meaning |
|-------|------|---------|
| 80 | Commit | Good enough to save |
| 90 | PR | Ready for deployment |
| 95 | Excellence | Aspirational |

---

## Skills Quick Reference

### Slides & LaTeX

| Command | What It Does |
|---------|-------------|
| `/compile-latex [file]` | 3-pass XeLaTeX + bibtex |
| `/deploy [LectureN]` | Render + deploy output |
| `/extract-tikz [LectureN]` | TikZ → PDF → SVG |
| `/create-lecture` | Full lecture creation |
| `/translate-to-quarto [file]` | Beamer → Quarto translation |

### Review & QA

| Command | What It Does |
|---------|-------------|
| `/proofread [file]` | Grammar/typo/overflow review |
| `/visual-audit [file]` | Slide layout audit |
| `/pedagogy-review [file]` | Narrative, notation, pacing review |
| `/review-r [file]` | R code quality review |
| `/qa-quarto [LectureN]` | Adversarial QA review |
| `/slide-excellence [file]` | Combined multi-agent review |
| `/validate-bib` | Cross-reference citations |
| `/devils-advocate` | Challenge slide design |
| `/review-paper [file]` | Manuscript review |

### Research Pipeline *(requires Codex MCP)*

| Command | What It Does |
|---------|-------------|
| `/research-pipeline [topic]` | Full end-to-end: idea → implement → review |
| `/idea-discovery [topic]` | Lit search → brainstorm → novelty check → review |
| `/research-lit [topic]` | Multi-source literature search + synthesis |
| `/idea-creator [topic]` | Brainstorm 8-12 ideas via GPT, filter, pilot top 3 |
| `/novelty-check [idea]` | Multi-source novelty verification |
| `/research-review [file]` | Multi-round critical review via Codex MCP |
| `/auto-review-loop` | Autonomous review loop until score ≥ 6/10 |
| `/verify-task [desc]` | Cross-agent QA: generates eval prompt → Codex reviews → fix loop |
| `/arxiv [query]` | Search, download, summarize arXiv papers |

### Paper Writing *(requires Codex MCP)*

| Command | What It Does |
|---------|-------------|
| `/paper-writing` | Full pipeline: plan → figure → write → compile → polish |
| `/paper-plan` | Claims-evidence matrix + section structure |
| `/paper-figure` | matplotlib/seaborn plots + LaTeX tables |
| `/paper-write` | Section-by-section LaTeX with de-AI polish |
| `/paper-compile` | latexmk build + auto-fix + page verification |
| `/auto-paper-improvement-loop` | 2-round GPT review → fix → recompile |
| `/paper-revise [draft.tex]` | Iterative diff-based editing: propose → latexdiff → accept/reject → loop |

### Utilities

| Command | What It Does |
|---------|-------------|
| `/commit [msg]` | Stage, commit, PR, merge |
| `/interview-me [topic]` | Interactive research interview |
| `/data-analysis [dataset]` | End-to-end R analysis |
| `/learn [skill-name]` | Extract discovery into persistent skill |
| `/context-status` | Show session health + context usage |
| `/deep-audit` | Repository-wide consistency audit |

---

<!-- CUSTOMIZE: Replace the example entries below with your own
     Beamer environments and CSS classes. Delete and add yours. -->

## Beamer Custom Environments

| Environment       | Effect        | Use Case       |
|-------------------|---------------|----------------|
| `[your-env]`      | [Description] | [When to use]  |

## Quarto CSS Classes

| Class              | Effect        | Use Case       |
|--------------------|---------------|----------------|
| `[.your-class]`    | [Description] | [When to use]  |

---

## Current Project State

| Lecture | Source | Output | Key Content |
|---------|--------|--------|-------------|
| 1: [Topic] | `slides/Lecture01.tex` | `output/Lecture01.pdf` | [Brief description] |
| 2: [Topic] | `slides/Lecture02.tex` | -- | [Brief description] |

---

## Key Files

<!-- CUSTOMIZE: List the most important files in your project so Claude
     knows where to find things. Delete the placeholders and add yours. -->

| File | Description |
|------|-------------|
| `[path/to/main-file]` | [Main document or entry point] |
| `[path/to/data-or-code]` | [Key script, dataset, or computation] |
