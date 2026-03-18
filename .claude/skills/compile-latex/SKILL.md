---
name: compile-latex
description: Compile a Beamer LaTeX slide deck with XeLaTeX (3 passes + bibtex). Use when compiling lecture slides.
argument-hint: "[filename, e.g. lecture01 or lecture01.tex]"
allowed-tools: ["Read", "Bash", "Glob"]
---

# Compile Beamer LaTeX Slides

Compile a Beamer slide deck using XeLaTeX with full citation resolution.

## Step 0: Normalize filename — CRITICAL, DO NOT SKIP

**⚠️ The argument may or may not include `.tex`. Strip it unconditionally so you never get `file.tex.tex`:**

```bash
BASENAME="${ARGUMENTS%.tex}"
```

**From this point forward, ONLY use `$BASENAME` — NEVER use `$ARGUMENTS` directly.**

Verify: `echo "$BASENAME"` should print something like `lecture01`, NOT `lecture01.tex`.

## Step 1: Compile

Navigate to `slides/` and run the 3-pass sequence:

```bash
cd slides
xelatex -interaction=nonstopmode "$BASENAME.tex"
BIBINPUTS=..:$BIBINPUTS bibtex "$BASENAME"
xelatex -interaction=nonstopmode "$BASENAME.tex"
xelatex -interaction=nonstopmode "$BASENAME.tex"
```

**Alternative (latexmk):**
```bash
cd slides
BIBINPUTS=..:$BIBINPUTS latexmk -xelatex -interaction=nonstopmode "$BASENAME.tex"
```

## Step 2: Check for warnings

- Grep output for `Overfull \\hbox` warnings
- Grep for `undefined citations` or `Label(s) may have changed`
- Report any issues found

## Step 3: Open the PDF

```bash
open slides/$BASENAME.pdf          # macOS
# xdg-open slides/$BASENAME.pdf    # Linux
```

## Step 4: Clean up auxiliary files — MANDATORY, NO HOOK EXISTS

**There is NO automatic cleanup hook. You MUST run this step every time, no exceptions.**

```bash
cd slides && find . -maxdepth 1 -type f \( -name "*.aux" -o -name "*.log" -o -name "*.nav" -o -name "*.out" -o -name "*.snm" -o -name "*.toc" -o -name "*.vrb" -o -name "*.bbl" -o -name "*.blg" -o -name "*.bcf" -o -name "*.run.xml" -o -name "*.synctex.gz" -o -name "*.fls" -o -name "*.fdb_latexmk" -o -name "*-blx.bib" \) -delete
```

**Why `find` instead of `rm -f *.ext`?** zsh's `nomatch` option errors when a glob has no matches. `find` handles missing extensions silently.

## Step 5: Report results

- Compilation success/failure
- Number of overfull hbox warnings
- Any undefined citations
- PDF page count

## Why 3 passes?
1. First xelatex: Creates `.aux` file with citation keys
2. bibtex: Reads `.aux`, generates `.bbl` with formatted references
3. Second xelatex: Incorporates bibliography
4. Third xelatex: Resolves all cross-references with final page numbers

## Important
- **Always use XeLaTeX**, never pdflatex
- **BIBINPUTS** is required: your `.bib` file lives in the repo root
- If your Beamer theme or preamble files are in a separate directory, add it to `TEXINPUTS`
- **Step 0 is non-negotiable** — double-check BASENAME before compiling
- **Step 4 is manual** — no hook will do it for you
