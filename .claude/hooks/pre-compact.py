#!/usr/bin/env python3
"""
Pre-Compact State Capture Hook

Fires before context compaction to capture the current state from
PLAN.md and CONTEXT.md at project root.

Hook Event: PreCompact
Returns: Exit code 0 (message printed to stderr for visibility)
"""

from __future__ import annotations

import json
import os
import sys
import re
from pathlib import Path
from datetime import datetime
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


def read_plan_status(project_dir: str) -> dict | None:
    """Read PLAN.md and extract current task status."""
    plan_file = Path(project_dir) / "PLAN.md"
    if not plan_file.exists():
        return None

    content = plan_file.read_text()

    # Skip if it's just the template
    if "[PROJECT NAME]" in content or "[Short title]" in content:
        return None

    # Find current task (first task not marked [DONE] or [BLOCKED])
    current_task = None
    for line in content.split("\n"):
        if line.strip().startswith("### Task") and "[DONE]" not in line and "[BLOCKED" not in line:
            current_task = line.strip().replace("### ", "")
            break

    # Count done vs total
    tasks = [l for l in content.split("\n") if l.strip().startswith("### Task")]
    done = sum(1 for t in tasks if "[DONE]" in t)

    return {
        "plan_path": "PLAN.md",
        "current_task": current_task,
        "tasks_done": done,
        "tasks_total": len(tasks),
    }


def extract_recent_decisions(project_dir: str, limit: int = 3) -> list[str]:
    """Extract recent decisions from CONTEXT.md."""
    context_file = Path(project_dir) / "CONTEXT.md"
    if not context_file.exists():
        return []

    content = context_file.read_text()
    decisions = []

    patterns = [
        r"Decision:\s*(.+)",
        r"Decided:\s*(.+)",
        r"Chose:\s*(.+)",
        r"→\s*(.+)",
        r"•\s*(.+)"
    ]

    for line in content.split("\n")[-50:]:
        for pattern in patterns:
            match = re.search(pattern, line.strip())
            if match and len(match.group(1)) > 10:
                decisions.append(match.group(1)[:100])
                if len(decisions) >= limit:
                    return decisions

    return decisions


def save_state(state: dict) -> None:
    """Save state to the session directory."""
    state_file = get_session_dir() / "pre-compact-state.json"
    state["timestamp"] = datetime.now().isoformat()

    try:
        state_file.write_text(json.dumps(state, indent=2))
    except IOError as e:
        print(f"Warning: Could not save pre-compact state: {e}", file=sys.stderr)


def append_compaction_note(project_dir: str, trigger: str) -> None:
    """Append compaction note to CONTEXT.md."""
    context_file = Path(project_dir) / "CONTEXT.md"
    if not context_file.exists():
        return

    try:
        with open(context_file, "a") as f:
            f.write(f"\n\n---\n")
            f.write(f"**Context compaction ({trigger}) at {datetime.now().strftime('%H:%M')}**\n")
            f.write(f"Read PLAN.md and CONTEXT.md to restore state.\n")
    except IOError:
        pass


def format_compaction_message(plan_info: dict | None, decisions: list[str]) -> str:
    """Format the pre-compaction message."""
    lines = []
    lines.append(f"\n{YELLOW}⚡ Context compaction starting{NC}")
    lines.append("")

    if plan_info:
        lines.append(f"{GREEN}Current state saved:{NC}")
        lines.append(f"  Plan: PLAN.md ({plan_info['tasks_done']}/{plan_info['tasks_total']} tasks done)")
        if plan_info.get("current_task"):
            lines.append(f"  Next task: {plan_info['current_task']}")

    if decisions:
        lines.append("")
        lines.append(f"{GREEN}Recent decisions captured:{NC}")
        for d in decisions:
            lines.append(f"  • {d[:80]}...")

    lines.append("")
    lines.append(f"{CYAN}State will be restored after compaction.{NC}")
    lines.append("")

    return "\n".join(lines)


def main() -> int:
    """Main hook entry point."""
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, IOError):
        hook_input = {}

    trigger = hook_input.get("trigger", "auto")
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", "")

    if not project_dir:
        return 0

    # Gather state
    plan_info = read_plan_status(project_dir)
    decisions = extract_recent_decisions(project_dir)

    # Build state object
    state = {
        "trigger": trigger,
        "plan_path": "PLAN.md" if plan_info else None,
        "current_task": plan_info.get("current_task") if plan_info else None,
        "tasks_done": plan_info.get("tasks_done") if plan_info else None,
        "tasks_total": plan_info.get("tasks_total") if plan_info else None,
        "decisions": decisions
    }

    # Save state for restoration
    save_state(state)

    # Append note to CONTEXT.md
    append_compaction_note(project_dir, trigger)

    # Print to stderr
    print(format_compaction_message(plan_info, decisions), file=sys.stderr)

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        # Fail open — never block Claude due to a hook bug
        sys.exit(0)
