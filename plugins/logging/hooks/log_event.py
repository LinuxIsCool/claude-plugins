#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Claude Code logging hook. Logs to JSONL, generates Markdown reports."""

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

EMOJIS = {
    "SessionStart": "💫", "SessionEnd": "⭐", "UserPromptSubmit": "🍄",
    "PreToolUse": "🔨", "PostToolUse": "🏰", "PermissionRequest": "🔑",
    "Notification": "🟡", "PreCompact": "♻", "Stop": "🟢",
    "SubagentStop": "🔵", "AssistantResponse": "🌲",
}


def get_paths(cwd, sid, ts):
    """Get log file paths, reusing existing timestamp prefix or creating new."""
    base = Path(cwd) / ".claude/logging" / ts.strftime("%Y/%m/%d")
    base.mkdir(parents=True, exist_ok=True)
    existing = list(base.glob(f"*-{sid[:8]}.jsonl"))
    prefix = existing[0].stem.rsplit("-", 1)[0] if existing else ts.strftime("%H-%M-%S")
    return base / f"{prefix}-{sid[:8]}.jsonl", base / f"{prefix}-{sid[:8]}.md"


def get_response(transcript_path):
    """Extract last assistant response from Claude's transcript."""
    try:
        for line in reversed(Path(transcript_path).read_text().strip().split("\n")):
            if line.strip():
                entry = json.loads(line)
                if entry.get("type") == "assistant":
                    for block in entry.get("message", {}).get("content", []):
                        if block.get("type") == "text":
                            return block.get("text", "")
    except:
        pass
    return ""


def get_subagent_info(transcript_path):
    """Extract model, tools, and response from subagent transcript."""
    try:
        data = json.loads(Path(transcript_path).read_text())
        model = data.get("message", {}).get("model", "")
        # Shorten model name (claude-opus-4-5-20251101 -> opus-4-5)
        if "opus" in model:
            model = "opus"
        elif "sonnet" in model:
            model = "sonnet"
        elif "haiku" in model:
            model = "haiku"

        tools, response = [], ""
        for block in data.get("message", {}).get("content", []):
            if block.get("type") == "tool_use":
                name = block.get("name", "?")
                inp = block.get("input", {})
                preview = ""
                for k in ("file_path", "pattern", "query", "command"):
                    if k in inp:
                        preview = str(inp[k])
                        break
                tools.append(f"- {name} `{preview}`" if preview else f"- {name}")
            elif block.get("type") == "text":
                response = block.get("text", "")

        return {"model": model, "tools": tools, "response": response}
    except:
        return {"model": "", "tools": [], "response": ""}


def tool_preview(data):
    """Extract preview string from tool input."""
    inp = data.get("tool_input", {})
    if isinstance(inp, str):
        return inp
    for k in ("file_path", "pattern", "query", "command"):
        if k in inp:
            return str(inp[k])
    return ""


def quote(text):
    """Convert text to markdown blockquote."""
    return "\n".join(f"> {line}" for line in text.split("\n"))


def generate_markdown(jsonl_path, md_path, sid):
    """Generate markdown report from JSONL source."""
    try:
        events = [json.loads(l) for l in jsonl_path.read_text().strip().split("\n") if l]
    except:
        return
    if not events:
        return

    lines = [
        f"# Session {sid[:8]}",
        f"**ID:** `{sid}`",
        f"**Started:** {events[0]['ts'][:19].replace('T', ' ')}",
        "", "---", ""
    ]

    # Process events into exchanges (prompt → stop cycles)
    prompt = tools = tool_details = subagents = None

    for e in events:
        t, d, ts = e["type"], e.get("data", {}), e["ts"][11:19]

        if t == "UserPromptSubmit":
            # Start new exchange
            prompt, tools, tool_details, subagents = (ts, d.get("prompt", "")), Counter(), [], []

        elif t == "PreToolUse" and prompt:
            name, preview = d.get("tool_name", "?"), tool_preview(d)
            tool_details.append(f"- {name} `{preview}`" if preview else f"- {name}")

        elif t == "PostToolUse" and prompt:
            tools[d.get("tool_name", "?")] += 1

        elif t == "SubagentStop" and prompt is not None:
            # Collect subagent info for this exchange
            agent_id = d.get("agent_id", "?")
            transcript = d.get("agent_transcript_path", "")
            info = get_subagent_info(transcript) if transcript else {}
            subagents.append({"ts": ts, "id": agent_id, **info})

        elif t == "AssistantResponse":
            # Complete the exchange
            if prompt:
                ts_prompt, text = prompt
                lines.extend(["", "---", f"### {ts_prompt}", "", "🍄 **User**", quote(text), ""])

                if tools:
                    summary = ", ".join(f"{n} ({c})" for n, c in tools.most_common())
                    lines.extend([
                        "<details>",
                        f"<summary>📦 {sum(tools.values())} tools: {summary}</summary>",
                        "", *tool_details, "",
                        "</details>", ""
                    ])

                if subagents:
                    for sa in subagents:
                        model_tag = f" ({sa['model']})" if sa.get("model") else ""
                        lines.extend([
                            "<details>",
                            f"<summary>🔵 Subagent {sa['id']}{model_tag}</summary>",
                            ""
                        ])
                        if sa.get("tools"):
                            lines.append(f"**Tools:** {len(sa['tools'])}")
                            lines.extend(sa["tools"])
                            lines.append("")
                        if sa.get("response"):
                            lines.extend(["**Response:**", quote(sa["response"]), ""])
                        lines.extend(["</details>", ""])

                prompt = None

            lines.extend(["🌲 **Claude**", quote(d.get("response", "")), ""])

        elif t == "SubagentStop" and prompt is None:
            # Subagent outside of an exchange (e.g., session startup)
            agent_id = d.get("agent_id", "?")
            transcript = d.get("agent_transcript_path", "")
            info = get_subagent_info(transcript) if transcript else {}
            model_tag = f" ({info['model']})" if info.get("model") else ""

            if info.get("tools") or info.get("response"):
                lines.extend([
                    "<details>",
                    f"<summary>`{ts}` 🔵 Subagent {agent_id}{model_tag}</summary>",
                    ""
                ])
                if info.get("tools"):
                    lines.append(f"**Tools:** {len(info['tools'])}")
                    lines.extend(info["tools"])
                    lines.append("")
                if info.get("response"):
                    lines.extend(["**Response:**", quote(info["response"]), ""])
                lines.extend(["</details>", ""])
            else:
                lines.append(f"`{ts}` 🔵 Subagent {agent_id}{model_tag}")

        elif t in ("SessionStart", "SessionEnd", "Notification"):
            info = d.get("source") or d.get("message") or ""
            lines.append(f"`{ts}` {EMOJIS.get(t, '•')} {t} {info}".rstrip())

    md_path.write_text("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-e", required=True)
    event = ap.parse_args().e

    data = json.loads(sys.stdin.read() or "{}") if sys.stdin else {}
    if not data:
        return

    cwd, sid, ts = data.get("cwd") or ".", data.get("session_id", "unknown"), datetime.now()
    jsonl, md = get_paths(cwd, sid, ts)

    # Append to JSONL (source of truth)
    with open(jsonl, "a") as f:
        json.dump({"ts": ts.isoformat(), "type": event, "session_id": sid, "data": data}, f, default=str)
        f.write("\n")

        # Capture assistant response on Stop (append before closing file)
        if event == "Stop" and data.get("transcript_path"):
            response = get_response(data["transcript_path"])
            if response:
                json.dump({"ts": ts.isoformat(), "type": "AssistantResponse", "session_id": sid, "data": {"response": response}}, f, default=str)
                f.write("\n")

    # Regenerate markdown on key events
    if event in ("SessionStart", "Stop", "SessionEnd", "SubagentStop"):
        generate_markdown(jsonl, md, sid)


if __name__ == "__main__":
    try:
        main()
    except:
        pass
