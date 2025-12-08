#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Generate Markdown reports from JSONL session logs.

Usage:
    uv run report.py                    # Today's sessions
    uv run report.py --session abc123   # Specific session
    uv run report.py --date 2025-01-15  # Specific date
    uv run report.py --all              # All sessions
"""

import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def find_log_dir(start: Path = None) -> Path:
    """Find .claude/logging directory walking up from start."""
    current = start or Path.cwd()
    while current != current.parent:
        log_dir = current / ".claude" / "logging"
        if log_dir.exists():
            return log_dir
        current = current.parent
    return Path.cwd() / ".claude" / "logging"


def read_jsonl(path: Path) -> list[dict]:
    """Read all events from a JSONL file."""
    events = []
    if path.exists():
        with open(path) as f:
            for line in f:
                if line.strip():
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    return events


def format_event(event: dict) -> str:
    """Format a single event for Markdown output."""
    ts = event.get("ts", "")[:19].replace("T", " ")
    event_type = event.get("type", "Unknown")
    data = event.get("data", {})

    lines = [f"### {ts} — {event_type}"]

    if event_type == "UserPromptSubmit":
        prompt = data.get("prompt", "")
        if prompt:
            lines.append(f"\n> {prompt[:500]}{'...' if len(prompt) > 500 else ''}")

    elif event_type in ("PreToolUse", "PostToolUse"):
        tool = data.get("tool_name", "unknown")
        lines.append(f"\n**Tool:** `{tool}`")
        if event_type == "PostToolUse" and data.get("tool_output"):
            output = str(data["tool_output"])[:300]
            lines.append(f"\n```\n{output}{'...' if len(str(data['tool_output'])) > 300 else ''}\n```")

    elif event_type == "SessionStart":
        lines.append(f"\n**Session ID:** `{data.get('session_id', 'unknown')}`")

    elif event_type == "SessionEnd":
        lines.append("\n*Session ended*")

    elif event_type == "Notification":
        msg = data.get("message", "")
        lines.append(f"\n{msg}")

    elif event_type == "PermissionRequest":
        msg = data.get("message", "")
        lines.append(f"\n**Permission:** {msg[:200]}")

    elif event_type == "PreCompact":
        lines.append("\n*Context compaction triggered*")

    elif event_type in ("Stop", "SubagentStop"):
        lines.append(f"\n*{'Subagent' if 'Subagent' in event_type else 'Agent'} stopped*")

    return "\n".join(lines)


def generate_session_report(events: list[dict], session_id: str) -> str:
    """Generate Markdown report for a single session."""
    lines = [
        f"# Session: {session_id[:8]}",
        "",
        f"**Full ID:** `{session_id}`",
        f"**Events:** {len(events)}",
        "",
        "---",
        ""
    ]

    for event in events:
        lines.append(format_event(event))
        lines.append("")

    return "\n".join(lines)


def generate_daily_report(log_dir: Path, date_str: str) -> str:
    """Generate report for all sessions on a given date."""
    date_path = log_dir / date_str.replace("-", "/")

    if not date_path.exists():
        return f"No logs found for {date_str}"

    lines = [
        f"# Daily Report: {date_str}",
        "",
    ]

    sessions = defaultdict(list)
    for jsonl_file in sorted(date_path.glob("*.jsonl")):
        session_id = jsonl_file.stem
        events = read_jsonl(jsonl_file)
        sessions[session_id] = events

    lines.append(f"**Sessions:** {len(sessions)}")
    lines.append(f"**Total Events:** {sum(len(e) for e in sessions.values())}")
    lines.append("")
    lines.append("---")
    lines.append("")

    for session_id, events in sessions.items():
        lines.append(f"## Session: {session_id}")
        lines.append(f"**Events:** {len(events)}")
        lines.append("")

        # Summarize key events
        prompts = [e for e in events if e.get("type") == "UserPromptSubmit"]
        tools = [e for e in events if e.get("type") in ("PreToolUse", "PostToolUse")]

        if prompts:
            lines.append("### User Prompts")
            for p in prompts[:5]:
                prompt = p.get("data", {}).get("prompt", "")[:100]
                lines.append(f"- {prompt}...")
            lines.append("")

        if tools:
            tool_names = set(t.get("data", {}).get("tool_name", "") for t in tools)
            lines.append(f"### Tools Used: {', '.join(sorted(tool_names))}")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Markdown reports from session logs")
    parser.add_argument("--session", "-s", help="Specific session ID")
    parser.add_argument("--date", "-d", help="Date (YYYY-MM-DD)")
    parser.add_argument("--all", "-a", action="store_true", help="All sessions")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    args = parser.parse_args()

    log_dir = find_log_dir()

    if not log_dir.exists():
        print(f"No logging directory found at {log_dir}")
        return

    if args.session:
        # Find session file
        for jsonl_file in log_dir.rglob("*.jsonl"):
            if jsonl_file.stem.startswith(args.session[:8]):
                events = read_jsonl(jsonl_file)
                report = generate_session_report(events, jsonl_file.stem)
                break
        else:
            report = f"Session {args.session} not found"

    elif args.date:
        report = generate_daily_report(log_dir, args.date)

    elif args.all:
        lines = ["# All Sessions", ""]
        for date_dir in sorted(log_dir.glob("*/*/*/*")):
            if date_dir.is_dir():
                date_str = "/".join(date_dir.parts[-3:])
                lines.append(f"## {date_str}")
                for jsonl_file in sorted(date_dir.glob("*.jsonl")):
                    events = read_jsonl(jsonl_file)
                    lines.append(f"- {jsonl_file.stem}: {len(events)} events")
                lines.append("")
        report = "\n".join(lines)

    else:
        # Default: today
        today = datetime.now().strftime("%Y-%m-%d")
        report = generate_daily_report(log_dir, today)

    if args.output:
        Path(args.output).write_text(report)
        print(f"Report written to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
