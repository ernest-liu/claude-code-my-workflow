# Test Coverage Analysis

**Status:** COMPLETED
**Date:** 2026-03-10

---

## Current State: Zero Test Coverage

The codebase has **no automated tests** — no test files, no test framework configuration (`pytest.ini`, `pyproject.toml`, etc.), and no CI/CD pipelines. Quality assurance is currently handled through:
- Heuristic scoring (`quality_score.py`)
- Agent-based adversarial review (critic/fixer loops)
- Hook-based reminders (verify, log, context)

While the agent-based approach is valuable for subjective review, the **core Python infrastructure** (1,050+ lines across 6 files) has no regression safety net.

---

## Testable Code Inventory

| File | Lines | Complexity | Test Priority |
|------|-------|------------|---------------|
| `scripts/quality_score.py` | 760 | High (regex, file I/O, scoring logic) | **P0 — Critical** |
| `.claude/hooks/context-monitor.py` | 225 | Medium (heuristics, caching, throttling) | P1 |
| `.claude/hooks/pre-compact.py` | 216 | Medium (file discovery, regex extraction) | P1 |
| `.claude/hooks/post-compact-restore.py` | 191 | Medium (state restore, file discovery) | P1 |
| `.claude/hooks/log-reminder.py` | 147 | Medium (state machine, counter logic) | P2 |
| `.claude/hooks/verify-reminder.py` | 182 | Low (filtering logic, caching) | P2 |
| `scripts/sync_to_docs.sh` | 92 | Low (file copying) | P3 |

---

## Proposed Test Areas (by priority)

### P0: `quality_score.py` — IssueDetector (Unit Tests)

This is the most critical code. Bugs here silently pass bad content or block good content. Every static method on `IssueDetector` is a pure function (content in, issues out) and trivially testable.

#### 1. `check_equation_overflow(content)` — 8-10 tests
- Short equation inside `$$...$$` → no overflow
- Single long line (>120 chars) inside `$$...$$` → flagged
- Multi-line equation with short lines inside `\begin{align}...\end{align}` → no overflow
- Single-line `$$ long_equation $$` (both delimiters on same line) → flagged
- Nested environments (`align` inside `equation`) → correct handling
- Lines with LaTeX comments (`%`) stripped before measuring
- Empty math blocks → no crash
- `\begin{gather}`, `\begin{multline}` variants → detected

#### 2. `check_broken_citations(content, bib_file)` — 6-8 tests
- `\cite{key}` with key in bib → empty result
- `\cite{key}` with key NOT in bib → key returned
- `\citep{a,b,c}` with mixed hits → only missing keys returned
- `\citeauthor{key}` → recognized
- Missing bib file → all keys returned as broken
- No citations in content → empty result

#### 3. `check_quarto_citations(content, bib_file)` — 6-8 tests
- `@key` standalone → detected
- `[@key]` bracket form → detected
- `[@key1; @key2]` multi-citation → both detected
- Email addresses (`user@domain.com`) → NOT treated as citation
- Quarto cross-refs (`@fig-xxx`, `@tbl-xxx`) → skipped
- Keys present in bib → not flagged

#### 4. `check_latex_syntax(content)` — 6-8 tests
- Matched `\begin{itemize}...\end{itemize}` → no issues
- Unclosed `\begin{frame}` → reported with line number
- Mismatched `\begin{itemize}...\end{enumerate}` → reported
- `\end{env}` without `\begin` → reported
- Nested environments (properly matched) → clean
- Environments inside comments → ideally skipped (potential bug to test)

#### 5. `check_hardcoded_paths(content)` — 5-6 tests
- `"/Users/foo/data.csv"` → flagged
- `"C:\Users\data.csv"` → flagged
- `"https://example.com"` → NOT flagged
- `"/tmp/scratch"` → NOT flagged
- Relative paths → NOT flagged
- `here::here("data/file.csv")` → NOT flagged

#### 6. `check_overfull_hbox_risk(content)` — 4-5 tests
- Short line inside `\begin{frame}...\end{frame}` → no issue
- Long line (>120 chars) inside frame → flagged
- Long line outside frame → NOT flagged
- `\includegraphics` long path → skipped
- Comment-only long lines → skipped

### P0: `quality_score.py` — QualityScorer (Integration Tests)

#### 7. Score calculation and thresholds — 6-8 tests
- Clean file with no issues → score 100, status EXCELLENCE
- File with 1 equation overflow → score 80, status COMMIT_READY
- File with auto-fail (compilation) → score 0, status FAIL
- File with multiple issues → correct cumulative deduction
- Score floor at 0 (never negative)
- `_generate_report()` → correct status mapping for each threshold band

#### 8. CLI interface — 3-4 tests
- Unknown file extension → error message
- Missing file → exit code 1
- `--json` flag → valid JSON output
- `--summary` flag → abbreviated output

### P1: Hook State Management (Unit Tests)

#### 9. `context-monitor.py` — 5-6 tests
- `estimate_context_percentage()` → increments tool call counter
- Throttling: returns True when below threshold and recent check
- Throttling: returns False when at/above threshold
- Threshold tracking: each threshold shown only once per session
- Cache read/write round-trip

#### 10. `pre-compact.py` — 4-5 tests
- `find_active_plan()` → finds most recent non-COMPLETED plan
- `find_active_plan()` → skips COMPLETED plans
- `extract_recent_decisions()` → extracts "Decision: ..." patterns
- `extract_recent_decisions()` → respects limit parameter
- `save_state()` / state round-trip

#### 11. `post-compact-restore.py` — 3-4 tests
- `read_pre_compact_state()` → reads and deletes state file
- `read_pre_compact_state()` → returns None when no state file
- `find_active_plan()` → status extraction (DRAFT/APPROVED/COMPLETED)
- `format_restoration_message()` → handles None inputs gracefully

### P2: Hook Filtering Logic (Unit Tests)

#### 12. `verify-reminder.py` — 4-5 tests
- `should_skip()` → True for `.md`, `.json`, `.yaml` files
- `should_skip()` → True for files in `/docs/`, `/.claude/`
- `should_skip()` → True for `test_*.py` files
- `needs_verification()` → True for `.tex`, `.qmd`, `.R`
- `needs_verification()` → False for `.py`, `.sh`

#### 13. `log-reminder.py` — 4-5 tests
- Counter increments on each call when log unchanged
- Counter resets when log mtime changes
- Block fires at threshold (15) and sets `reminded=True`
- Second call after threshold → no double-block
- `stop_hook_active=True` → immediate exit (loop prevention)

### P3: Shell Script (Smoke Tests)

#### 14. `sync_to_docs.sh` — 2-3 tests
- Script exits with error when no QMD file matches argument
- Script creates expected directory structure
- Script handles missing `rsync` gracefully (falls back to `cp`)

---

## Recommended Test Infrastructure

```
tests/
├── conftest.py                    # Shared fixtures (tmp dirs, sample content)
├── test_quality_score.py          # P0: IssueDetector + QualityScorer
├── test_context_monitor.py        # P1: Context monitor hook
├── test_pre_compact.py            # P1: Pre-compact hook
├── test_post_compact_restore.py   # P1: Post-compact restore hook
├── test_log_reminder.py           # P2: Log reminder hook
├── test_verify_reminder.py        # P2: Verify reminder hook
└── fixtures/
    ├── sample.bib                 # Test bibliography
    ├── clean_slides.qmd           # No-issue Quarto file
    ├── overflow_equation.tex      # Equation overflow examples
    └── bad_citations.tex          # Broken citation examples
```

**Framework:** pytest (standard, no dependencies beyond what's already implicit)

**Configuration (pyproject.toml):**
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["scripts", ".claude/hooks"]
```

---

## Estimated Impact

| Test Suite | Tests | Bugs Likely Caught |
|------------|-------|--------------------|
| IssueDetector unit tests | ~40 | Regex edge cases, off-by-one in line counting, false positives on URLs/emails |
| QualityScorer integration | ~8 | Threshold boundary errors, score floor bugs, report format issues |
| Hook state management | ~15 | Cache corruption, double-fire, missed threshold, state file cleanup |
| Hook filtering | ~10 | Overly aggressive skipping, missed file types |
| **Total** | **~73** | |

---

## Known Risks Without Tests

1. **Regex fragility** — `check_equation_overflow` has complex state machine logic for tracking `$$` vs `\begin{env}` delimiters. A subtle nesting bug could silently miss overflows or flag correct content.

2. **Citation parsing** — Quarto `@key` detection uses negative lookbehind that could break with certain Unicode or punctuation contexts. Email false positives are handled but not tested.

3. **Score arithmetic** — Multiple issues can push score below 0 before `max(0, score)` clamp. No test verifies the cumulative deduction logic is correct.

4. **Hook state races** — All hooks share a session directory with JSON files. Concurrent hook execution could cause cache corruption (read-modify-write without locking).

5. **`check_latex_syntax` comment handling** — The comment stripping (`line.split('%')[0]`) doesn't handle escaped `\%`, so a line containing a literal percent sign in LaTeX would be incorrectly truncated.
