#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
PreToolUse hook for Claude Code Logging Plugin.
Logs tool invocations before execution to SQLite and Markdown.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add lib directory to path
_lib_dir = Path(__file__).parent.parent / "lib"
sys.path.insert(0, str(_lib_dir))

from common import HookRunner, HookContext
from markdown_writer import MarkdownSessionWriter
from summarizer import ResponseSummarizer


def handle_pre_tool_use(ctx: HookContext) -> Optional[Dict[str, Any]]:
    """Handle PreToolUse hook event."""

    # Extract data
    tool_name = ctx.get_tool_name()
    tool_input = ctx.get_tool_input()
    event_id = ctx.input_data.get("_event_id")

    if not tool_name:
        return None

    # Log to SQLite
    if ctx.db and event_id:
        ctx.db.log_tool_pre(
            event_id=event_id,
            session_id=ctx.session_id,
            tool_name=tool_name,
            tool_input=tool_input,
        )

    # Log to Markdown (brief entry, will be updated by PostToolUse if needed)
    if ctx.config.storage.markdown_enabled:
        summarizer = ResponseSummarizer(ctx.config.summarization.max_length)
        input_summary = summarizer.summarize_tool_input(tool_name, tool_input)

        writer = MarkdownSessionWriter(
            str(ctx.storage_paths["sessions"]),
            ctx.session_id
        )
        writer.write_tool_use(
            tool_name=tool_name,
            input_summary=input_summary,
            timestamp=ctx.timestamp,
        )

    # Return context if verbose
    if ctx.hook_config.verbosity in ("verbose", "debug"):
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": f"Tool {tool_name} logged"
            }
        }

    return None


def main():
    runner = HookRunner("PreToolUse")
    runner.run(handle_pre_tool_use)


if __name__ == "__main__":
    main()
