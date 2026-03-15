#!/usr/bin/env python3
"""
Post-Compact Context Restoration Hook

Fires after compaction to restore context from PLAN.md and CONTEXT.md.

Hook Event: SessionStart (matcher: "compact|resume")
Returns: Exit code 0 (output to stdout)
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
import hashlib

# Colors for terminal output
CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
NC = "\033[0m"  # No color


def get_session_dir() -> Path:
    """Get the session directory for storing state files."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return Path.home() / ".claude" / "sessions" / "default"

    project_hash = hashlib.md5(project_dir.encode()).hexdigest()[:8]
    session_dir = Path.home() / ".claude" / "sessions" / project_hash
    session_dir.mkdir(parents=True, exist_ok=True)
    return session_dir


def read_pre_compact_state() -> dict | None:
    """Read and delete the pre-compact state file."""
    session_dir = get_session_dir()
    state_file = session_dir / "pre-compact-state.json"

    if not state_file.exists():
        return None

    try:
        state = json.loads(state_file.read_text())
        state_file.unlink()  # Clean up after restore
        return state
    except (json.JSONDecodeError, IOError):
        return None


def check_files_exist(project_dir: str) -> dict:
    """Check which handoff files exist."""
    return {
        "plan": (Path(project_dir) / "PLAN.md").exists(),
        "context": (Path(project_dir) / "CONTEXT.md").exists(),
    }


def format_restoration_message(
    pre_compact_state: dict | None,
    files: dict,
) -> str:
    """Format the context restoration message for Claude."""
    lines = []
    lines.append(f"\n{CYAN}[Context Restored After Compaction]{NC}")
    lines.append("")

    if pre_compact_state:
        lines.append(f"{GREEN}Pre-Compaction State:{NC}")
        if pre_compact_state.get("current_task"):
            lines.append(f"  Current task: {pre_compact_state['current_task']}")
        if pre_compact_state.get("tasks_done") is not None:
            lines.append(f"  Progress: {pre_compact_state['tasks_done']}/{pre_compact_state['tasks_total']} tasks done")
        if pre_compact_state.get("decisions"):
            lines.append("  Recent decisions:")
            for decision in pre_compact_state["decisions"][-3:]:
                lines.append(f"    - {decision}")
        lines.append("")

    lines.append(f"{YELLOW}Recovery Actions:{NC}")
    if files["plan"]:
        lines.append("  1. Read PLAN.md for current task list and progress")
    if files["context"]:
        lines.append("  2. Read CONTEXT.md for session state and open questions")
    lines.append("  3. Check git status/diff for uncommitted changes")
    lines.append("  4. Continue from where you left off")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    """Main hook entry point."""
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        hook_input = {}

    # Only run on compact/resume sessions
    session_source = hook_input.get("source", "")
    if session_source not in ("compact", "resume"):
        return 0

    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if not project_dir:
        return 0

    # Gather context
    pre_compact_state = read_pre_compact_state()
    files = check_files_exist(project_dir)

    if pre_compact_state or files["plan"] or files["context"]:
        message = format_restoration_message(pre_compact_state, files)
        print(message)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # Fail open — never block Claude due to a hook bug
        sys.exit(0)
