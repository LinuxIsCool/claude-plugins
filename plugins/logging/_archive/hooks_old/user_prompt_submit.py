#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
UserPromptSubmit hook for Claude Code Logging Plugin.
Logs user prompts to SQLite and Markdown.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add lib directory to path
_lib_dir = Path(__file__).parent.parent / "lib"
sys.path.insert(0, str(_lib_dir))

from common import HookRunner, HookContext, count_words
from markdown_writer import MarkdownSessionWriter


def handle_user_prompt_submit(ctx: HookContext) -> Optional[Dict[str, Any]]:
    """Handle UserPromptSubmit hook event."""

    # Extract data
    prompt = ctx.get_prompt()
    event_id = ctx.input_data.get("_event_id")
    word_count = count_words(prompt)

    # Log to SQLite
    if ctx.db and event_id:
        ctx.db.log_user_prompt(
            event_id=event_id,
            session_id=ctx.session_id,
            prompt=prompt,
            was_blocked=False,
        )

    # Log to Markdown
    if ctx.config.storage.markdown_enabled:
        writer = MarkdownSessionWriter(
            str(ctx.storage_paths["sessions"]),
            ctx.session_id
        )
        writer.write_user_prompt(
            prompt=prompt,
            word_count=word_count,
            timestamp=ctx.timestamp,
        )

    # Return context if verbose
    if ctx.hook_config.verbosity in ("verbose", "debug"):
        return {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": f"Prompt logged ({word_count} words)"
            }
        }

    return None


def main():
    runner = HookRunner("UserPromptSubmit")
    runner.run(handle_user_prompt_submit)


if __name__ == "__main__":
    main()
