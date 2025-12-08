#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
SessionEnd hook for Claude Code Logging Plugin.
Logs session end events to SQLite and Markdown.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add lib directory to path
_lib_dir = Path(__file__).parent.parent / "lib"
sys.path.insert(0, str(_lib_dir))

from common import HookRunner, HookContext
from markdown_writer import MarkdownSessionWriter, update_daily_index


def handle_session_end(ctx: HookContext) -> Optional[Dict[str, Any]]:
    """Handle SessionEnd hook event."""

    # Extract data
    reason = ctx.input_data.get("reason", "unknown")
    event_id = ctx.input_data.get("_event_id")

    # Log to SQLite
    if ctx.db and event_id:
        ctx.db.log_session_end_event(
            event_id=event_id,
            session_id=ctx.session_id,
            reason=reason
        )

        # Get session stats for markdown
        stats = ctx.db.get_session_stats(ctx.session_id)
    else:
        stats = None

    # Finalize Markdown
    if ctx.config.storage.markdown_enabled:
        writer = MarkdownSessionWriter(
            str(ctx.storage_paths["sessions"]),
            ctx.session_id
        )
        writer.write_stop("main", stats=stats)
        writer.finalize(stats=stats)

        # Update daily index
        update_daily_index(str(ctx.storage_paths["sessions"]))

    # Return context if verbose
    if ctx.hook_config.verbosity in ("verbose", "debug"):
        return {
            "hookSpecificOutput": {
                "hookEventName": "SessionEnd",
                "additionalContext": f"Session {ctx.session_id[:8]} ended. Reason: {reason}"
            }
        }

    return None


def main():
    runner = HookRunner("SessionEnd")
    runner.run(handle_session_end)


if __name__ == "__main__":
    main()
