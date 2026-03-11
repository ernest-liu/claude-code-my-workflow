---
name: deploy
description: Compile slides and copy output artifacts for deployment. Use when deploying lecture slides after making changes.
argument-hint: "[LectureN or 'all']"
allowed-tools: ["Read", "Bash"]
---

# Deploy Slides

Compile slides and copy output artifacts to `output/` for deployment.

## Steps

1. **Compile the source files:**
   - For `.tex` files: run the 3-pass XeLaTeX compilation (see `/compile-latex`)
   - For other source formats: render using the appropriate tool

2. **Copy compiled artifacts to `output/`:**
   - Copy compiled PDFs from `slides/` to `output/`
   - Copy any generated HTML and associated asset directories to `output/`

3. **Verify deployment:**
   - Check that output files exist in `output/`
   - Check that `figures/` assets are accessible from output

4. **Verify interactive charts** (if applicable):
   - Grep rendered HTML for interactive widget count
   - Confirm count matches expected

5. **Verify TikZ SVGs** (if applicable):
   - Check that all referenced SVG files exist in `figures/LectureN/`

6. **Open output** for visual verification:
   - `open output/LectureX_Name.pdf`            # macOS
   - `# xdg-open output/LectureX_Name.pdf`      # Linux
   - Confirm slides render, images display correctly

7. **Report results** to the user
