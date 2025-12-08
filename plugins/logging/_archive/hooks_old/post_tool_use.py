#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
PostToolUse hook for Claude Code Logging Plugin.
Logs tool completion to SQLite. Updates tool_usage entry created by PreToolUse.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add lib directory to path
_lib_dir = Path(__file__).parent.parent / "lib"
sys.path.insert(0, str(_lib_dir))

from common import HookRunner, HookContext
from summarizer import ResponseSummarizer


def handle_post_tool_use(ctx: HookContext) -> Optional[Dict[str, Any]]:
    """Handle PostToolUse hook event."""

    # Extract data
    tool_name = ctx.get_tool_name()
    tool_input = ctx.get_tool_input()
    tool_response = ctx.get_tool_response()
    event_id = ctx.input_data.get("_event_id")

    if not tool_name:
        return None

    # Log to SQLite (links to PreToolUse entry)
    if ctx.db and event_id:
        ctx.db.log_tool_post(
            event_id=event_id,
            session_id=ctx.session_id,
            tool_name=tool_name,
            tool_input=tool_input,
            tool_output=tool_response,
        )

    # Note: We don't write to markdown here because PreToolUse already
    # created an entry. The markdown is intentionally simpler - showing
    # tool invocations without full response details.
    # Full details are in SQLite.

    # Return context if verbose
    if ctx.hook_config.verbosity in ("verbose", "debug"):
        summarizer = ResponseSummarizer(ctx.config.summarization.max_length)
        output_summary = summarizer.summarize_tool_output(tool_name, tool_response)
        return {
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": f"Tool {tool_name} completed: {output_summary}"
            }
        }

    return None


def main():
    runner = HookRunner("PostToolUse")
    runner.run(handle_post_tool_use)


if __name__ == "__main__":
    main()
