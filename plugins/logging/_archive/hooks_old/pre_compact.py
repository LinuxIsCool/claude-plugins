#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
PreCompact hook for Claude Code Logging Plugin.
Logs pre-compaction events to SQLite and Markdown.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add lib directory to path
_lib_dir = Path(__file__).parent.parent / "lib"
sys.path.insert(0, str(_lib_dir))

from common import HookRunner, HookContext
from markdown_writer import MarkdownSessionWriter


def handle_pre_compact(ctx: HookContext) -> Optional[Dict[str, Any]]:
    """Handle PreCompact hook event."""

    # Extract data
    trigger = ctx.get_trigger()
    custom_instructions = ctx.input_data.get("custom_instructions")
    transcript_path = ctx.get_transcript_path()
    event_id = ctx.input_data.get("_event_id")

    # Log to SQLite
    if ctx.db and event_id:
        ctx.db.log_compaction(
            event_id=event_id,
            session_id=ctx.session_id,
            trigger=trigger,
            custom_instructions=custom_instructions,
            transcript_path=transcript_path,
        )

    # Log to Markdown
    if ctx.config.storage.markdown_enabled:
        writer = MarkdownSessionWriter(
            str(ctx.storage_paths["sessions"]),
            ctx.session_id
        )
        writer.write_compaction(
            trigger=trigger,
            custom_instructions=custom_instructions,
            timestamp=ctx.timestamp,
        )

    # Return context if verbose
    if ctx.hook_config.verbosity in ("verbose", "debug"):
        return {
            "hookSpecificOutput": {
                "hookEventName": "PreCompact",
                "additionalContext": f"Compaction logged: trigger={trigger}"
            }
        }

    return None


def main():
    runner = HookRunner("PreCompact")
    runner.run(handle_pre_compact)


if __name__ == "__main__":
    main()
