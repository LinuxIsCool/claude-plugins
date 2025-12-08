#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Universal logging hook for Claude Code.
Single script handles all 10 hook types via --event-type argument.

Usage in settings.json:
  "command": "uv run log_event.py --event-type SessionStart"
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime


def get_log_file(cwd: str, session_id: str) -> Path:
    """Get session log file path organized by date."""
    now = datetime.now()
    base = Path(cwd) / ".claude" / "logging" / now.strftime("%Y/%m/%d")
    base.mkdir(parents=True, exist_ok=True)
    short_id = session_id[:8] if len(session_id) > 8 else session_id
    return base / f"{short_id}.jsonl"


def log_event(cwd: str, session_id: str, event_type: str, payload: dict) -> Path:
    """Append event to session JSONL file. Stores FULL payload, never truncates."""
    log_file = get_log_file(cwd, session_id)
    event = {
        "ts": datetime.now().isoformat(),
        "type": event_type,
        "session_id": session_id,
        "data": payload
    }
    with open(log_file, 'a') as f:
        f.write(json.dumps(event, default=str) + '\n')
    return log_file


def read_input() -> dict:
    """Read and parse JSON from stdin. Returns empty dict on failure."""
    try:
        text = sys.stdin.read()
        return json.loads(text) if text.strip() else {}
    except (json.JSONDecodeError, Exception):
        return {}


def get_cwd(data: dict) -> str:
    """Extract working directory from hook input."""
    return data.get("cwd") or data.get("working_directory") or str(Path.cwd())


def get_session_id(data: dict) -> str:
    """Extract session ID from hook input."""
    return data.get("session_id", "unknown")


def main():
    parser = argparse.ArgumentParser(description="Log Claude Code hook events")
    parser.add_argument(
        "--event-type", "-e",
        required=True,
        help="Hook event type (SessionStart, PreToolUse, etc.)"
    )
    args = parser.parse_args()

    data = read_input()
    if not data:
        sys.exit(0)

    try:
        log_event(
            cwd=get_cwd(data),
            session_id=get_session_id(data),
            event_type=args.event_type,
            payload=data
        )
    except Exception:
        pass  # Never block Claude Code

    sys.exit(0)


if __name__ == "__main__":
    main()
