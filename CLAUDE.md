# CLAUDE.MD -- Academic Project Development with Claude Code

<!-- HOW TO USE: Replace [BRACKETED PLACEHOLDERS] with your project info.
     Keep this file under ~150 lines — Claude loads it every session. -->

**Project:** [YOUR PROJECT NAME]
**Institution:** [YOUR INSTITUTION]
**Branch:** main

---

## Core Principles

- **Plan first** -- enter plan mode before non-trivial tasks
- **Verify after** -- compile/render and confirm output at the end of every task
- **Quality gates** -- nothing ships below 80/100
- **[LEARN] tags** -- when corrected, save `[LEARN:category] wrong → right` to MEMORY.md

---

## Writing Style

<!-- CUSTOMIZE: Define your prose and LaTeX conventions so Claude
     writes in your voice. Delete the placeholders and add yours. -->

- [Prose tone, e.g., "Formal propositions followed by interpretive discussion"]
- [Interpretation phrases, e.g., "Use 'Intuitively,...', 'This implies...'"]
- [LaTeX conventions, e.g., "`\bm{}` for vectors/matrices, `\left( \right)` for delimiters"]
- [Document format, e.g., "12pt font, 1in margins, onehalfspacing"]
- [Edit display convention, e.g., "Highlight changes with **bold** insertions and ~~strikethrough~~ deletions"]

---

## Folder Structure

```
[YOUR-PROJECT]/
├── CLAUDE.md                    # This file
├── .claude/                     # Rules, skills, agents, hooks
├── bibliography_base.bib        # Centralized bibliography
├── figures/                     # Figures and images
├── slides/                      # Source .tex / .md files
├── output/                      # Compiled PDFs and generated artifacts
└── raw/                         # Reference papers, data, supporting materials
```

---

## Commands

```bash
# LaTeX (3-pass, XeLaTeX only)
cd slides && xelatex -interaction=nonstopmode file.tex
BIBINPUTS=..:$BIBINPUTS bibtex file
xelatex -interaction=nonstopmode file.tex
xelatex -interaction=nonstopmode file.tex
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

| Command | What It Does |
|---------|-------------|
| `/compile-latex [file]` | 3-pass XeLaTeX + bibtex |
| `/deploy [LectureN]` | Render + deploy output |
| `/extract-tikz [LectureN]` | TikZ → PDF → SVG |
| `/proofread [file]` | Grammar/typo/overflow review |
| `/visual-audit [file]` | Slide layout audit |
| `/pedagogy-review [file]` | Narrative, notation, pacing review |
| `/review-r [file]` | R code quality review |
| `/qa-quarto [LectureN]` | Adversarial QA review |
| `/slide-excellence [file]` | Combined multi-agent review |
| `/translate-to-quarto [file]` | Beamer → Quarto translation |
| `/validate-bib` | Cross-reference citations |
| `/devils-advocate` | Challenge slide design |
| `/create-lecture` | Full lecture creation |
| `/commit [msg]` | Stage, commit, PR, merge |
| `/lit-review [topic]` | Literature search + synthesis |
| `/research-ideation [topic]` | Research questions + strategies |
| `/interview-me [topic]` | Interactive research interview |
| `/review-paper [file]` | Manuscript review |
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
