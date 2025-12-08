#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
PermissionRequest hook for Claude Code Logging Plugin.
Logs permission dialog events to SQLite.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add lib directory to path
_lib_dir = Path(__file__).parent.parent / "lib"
sys.path.insert(0, str(_lib_dir))

from common import HookRunner, HookContext


def handle_permission_request(ctx: HookContext) -> Optional[Dict[str, Any]]:
    """Handle PermissionRequest hook event."""

    # Extract data
    message = ctx.get_message()
    notification_type = ctx.input_data.get("notification_type")
    event_id = ctx.input_data.get("_event_id")

    # Log to SQLite
    if ctx.db and event_id:
        ctx.db.log_permission_request(
            event_id=event_id,
            session_id=ctx.session_id,
            message=message,
            notification_type=notification_type,
        )

    # Return context if verbose
    if ctx.hook_config.verbosity in ("verbose", "debug"):
        return {
            "hookSpecificOutput": {
                "hookEventName": "PermissionRequest",
                "additionalContext": f"Permission request logged: {notification_type}"
            }
        }

    return None


def main():
    runner = HookRunner("PermissionRequest")
    runner.run(handle_permission_request)


if __name__ == "__main__":
    main()
