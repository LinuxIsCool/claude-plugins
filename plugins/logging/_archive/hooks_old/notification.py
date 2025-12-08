#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Notification hook for Claude Code Logging Plugin.
Logs notification events to SQLite and Markdown.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add lib directory to path
_lib_dir = Path(__file__).parent.parent / "lib"
sys.path.insert(0, str(_lib_dir))

from common import HookRunner, HookContext
from markdown_writer import MarkdownSessionWriter


def handle_notification(ctx: HookContext) -> Optional[Dict[str, Any]]:
    """Handle Notification hook event."""

    # Extract data
    message = ctx.get_message()
    notification_type = ctx.input_data.get("notification_type")
    event_id = ctx.input_data.get("_event_id")

    # Log to SQLite
    if ctx.db and event_id:
        ctx.db.log_notification(
            event_id=event_id,
            session_id=ctx.session_id,
            message=message,
            title=notification_type,
        )

    # Log to Markdown
    if ctx.config.storage.markdown_enabled:
        writer = MarkdownSessionWriter(
            str(ctx.storage_paths["sessions"]),
            ctx.session_id
        )
        writer.write_notification(
            message=message,
            title=notification_type,
            timestamp=ctx.timestamp,
        )

    # Return context if verbose
    if ctx.hook_config.verbosity in ("verbose", "debug"):
        return {
            "hookSpecificOutput": {
                "hookEventName": "Notification",
                "additionalContext": f"Notification logged: {notification_type}"
            }
        }

    return None


def main():
    runner = HookRunner("Notification")
    runner.run(handle_notification)


if __name__ == "__main__":
    main()
