#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
SubagentStop hook for Claude Code Logging Plugin.
Logs when Claude subagents (Task tool) finish responding.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add lib directory to path
_lib_dir = Path(__file__).parent.parent / "lib"
sys.path.insert(0, str(_lib_dir))

from common import HookRunner, HookContext
from markdown_writer import MarkdownSessionWriter


def handle_subagent_stop(ctx: HookContext) -> Optional[Dict[str, Any]]:
    """Handle SubagentStop hook event."""

    # Extract data
    stop_hook_active = ctx.input_data.get("stop_hook_active", False)
    transcript_path = ctx.get_transcript_path()
    event_id = ctx.input_data.get("_event_id")

    # Log to SQLite
    if ctx.db and event_id:
        ctx.db.log_stop(
            event_id=event_id,
            session_id=ctx.session_id,
            stop_type="subagent",
            stop_hook_active=stop_hook_active,
            transcript_path=transcript_path,
        )

    # Log to Markdown (brief note)
    if ctx.config.storage.markdown_enabled:
        writer = MarkdownSessionWriter(
            str(ctx.storage_paths["sessions"]),
            ctx.session_id
        )
        writer.write_stop(
            stop_type="subagent",
            timestamp=ctx.timestamp,
        )

    # Return context if verbose
    if ctx.hook_config.verbosity in ("verbose", "debug"):
        return {
            "hookSpecificOutput": {
                "hookEventName": "SubagentStop",
                "additionalContext": "Subagent stop logged"
            }
        }

    return None


def main():
    runner = HookRunner("SubagentStop")
    runner.run(handle_subagent_stop)


if __name__ == "__main__":
    main()
