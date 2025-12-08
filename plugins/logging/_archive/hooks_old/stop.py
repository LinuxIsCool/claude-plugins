#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Stop hook for Claude Code Logging Plugin.
Logs when main Claude agent finishes responding.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add lib directory to path
_lib_dir = Path(__file__).parent.parent / "lib"
sys.path.insert(0, str(_lib_dir))

from common import HookRunner, HookContext
from markdown_writer import MarkdownSessionWriter


def handle_stop(ctx: HookContext) -> Optional[Dict[str, Any]]:
    """Handle Stop hook event."""

    # Extract data
    stop_hook_active = ctx.input_data.get("stop_hook_active", False)
    transcript_path = ctx.get_transcript_path()
    event_id = ctx.input_data.get("_event_id")

    # Log to SQLite
    if ctx.db and event_id:
        ctx.db.log_stop(
            event_id=event_id,
            session_id=ctx.session_id,
            stop_type="main",
            stop_hook_active=stop_hook_active,
            transcript_path=transcript_path,
        )

    # Note: We don't write to markdown here for every stop.
    # Markdown session file is finalized by SessionEnd hook.
    # This keeps the markdown cleaner.

    # Return context if verbose
    if ctx.hook_config.verbosity in ("verbose", "debug"):
        return {
            "hookSpecificOutput": {
                "hookEventName": "Stop",
                "additionalContext": "Stop event logged"
            }
        }

    return None


def main():
    runner = HookRunner("Stop")
    runner.run(handle_stop)


if __name__ == "__main__":
    main()
