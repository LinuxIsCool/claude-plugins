#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Claude Code logging hook. Logs to JSONL + live Markdown."""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

EMOJIS = {
    "SessionStart": "💫",
    "SessionEnd": "⭐",
    "UserPromptSubmit": "🍄",
    "PreToolUse": "🔨",
    "PostToolUse": "🏰",
    "PermissionRequest": "🔑",
    "Notification": "🟡",
    "PreCompact": "♻",
    "Stop": "🟢",
    "SubagentStop": "🔵",
    "AssistantResponse": "🌲",
}


def get_info(event, data, jsonl):
    if event == "SessionStart":
        return data.get("source", "")
    if event == "UserPromptSubmit":
        return data.get("prompt", "")
    if event == "PreToolUse":
        return f"{data.get('tool_name', '?')} {preview(data)}"
    if event == "PostToolUse":
        return data.get("tool_name", "?")
    if event == "Notification":
        return data.get("message", "")
    if event == "SubagentStop":
        return data.get("agent_id", "?")
    if event == "Stop":
        return stats(jsonl)
    if event == "AssistantResponse":
        return data.get("response", "")
    return ""


def preview(data):
    inp = data.get("tool_input", {})
    if isinstance(inp, str):
        return f"`{inp}`"
    for k in ("file_path", "pattern", "query", "command"):
        if k in inp:
            return f"`{str(inp[k])}`"
    return ""


def stats(path):
    try:
        lines = path.read_text().strip().split("\n") if path.exists() else []
        events = [json.loads(l) for l in lines if l]
        p = sum(1 for e in events if e["type"] == "UserPromptSubmit")
        t = sum(1 for e in events if e["type"] == "PostToolUse")
        return f"{p} prompt{'s'*(p!=1)}, {t} tool{'s'*(t!=1)}" if p or t else ""
    except:
        return ""


def get_last_response(transcript_path):
    """Extract the last assistant response from Claude's transcript."""
    try:
        lines = Path(transcript_path).read_text().strip().split("\n")
        for line in reversed(lines):
            if not line.strip():
                continue
            entry = json.loads(line)
            if entry.get("type") == "assistant":
                content = entry.get("message", {}).get("content", [])
                for block in content:
                    if block.get("type") == "text":
                        return block.get("text", "")
        return ""
    except:
        return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", required=True)
    event = ap.parse_args().e

    data = json.loads(sys.stdin.read() or "{}") if sys.stdin else {}
    if not data:
        return

    cwd = data.get("cwd") or "."
    sid = data.get("session_id", "unknown")
    ts = datetime.now()

    base = Path(cwd) / ".claude/logging" / ts.strftime("%Y/%m/%d")
    base.mkdir(parents=True, exist_ok=True)

    # Find existing files for this session, or create new ones with timestamp prefix
    existing = list(base.glob(f"*-{sid[:8]}.jsonl"))
    if existing:
        prefix = existing[0].stem.rsplit("-", 1)[0]  # Extract timestamp prefix
    else:
        prefix = ts.strftime("%H-%M-%S")

    jsonl, md = base / f"{prefix}-{sid[:8]}.jsonl", base / f"{prefix}-{sid[:8]}.md"

    # JSONL
    with open(jsonl, "a") as f:
        json.dump(
            {"ts": ts.isoformat(), "type": event, "session_id": sid, "data": data},
            f,
            default=str,
        )
        f.write("\n")

    # Markdown header
    if not md.exists():
        md.write_text(
            f"# Session {sid[:8]}\n**ID:** `{sid}`\n**Started:** {ts:%Y-%m-%d %H:%M:%S}\n\n---\n\n"
        )

    # Log the event
    emoji = EMOJIS.get(event, "•")
    info = get_info(event, data, jsonl)
    with open(md, "a") as f:
        f.write(f"`{ts:%H:%M:%S}` {emoji} {event} {info}\n".rstrip() + "\n")

    # On Stop, also capture and log the assistant's response
    if event == "Stop" and data.get("transcript_path"):
        response = get_last_response(data["transcript_path"])
        if response:
            # Log to JSONL
            with open(jsonl, "a") as f:
                json.dump(
                    {
                        "ts": ts.isoformat(),
                        "type": "AssistantResponse",
                        "session_id": sid,
                        "data": {"response": response},
                    },
                    f,
                    default=str,
                )
                f.write("\n")
            # Log to Markdown
            with open(md, "a") as f:
                f.write(f"`{ts:%H:%M:%S}` 🌲 AssistantResponse {response}\n")


if __name__ == "__main__":
    try:
        main()
    except:
        pass
