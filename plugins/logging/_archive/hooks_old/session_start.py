#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
SessionStart hook for Claude Code Logging Plugin.
Logs session start events to SQLite and Markdown.
"""

import sys
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

# Add lib directory to path
_lib_dir = Path(__file__).parent.parent / "lib"
sys.path.insert(0, str(_lib_dir))

from common import HookRunner, HookContext
from markdown_writer import MarkdownSessionWriter


def get_git_branch() -> Optional[str]:
    """Get current git branch name."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def handle_session_start(ctx: HookContext) -> Optional[Dict[str, Any]]:
    """Handle SessionStart hook event."""

    # Extract session data
    source = ctx.get_source()
    cwd = ctx.cwd
    git_branch = get_git_branch()

    # Log to SQLite
    if ctx.db:
        ctx.db.log_session_start(
            session_id=ctx.session_id,
            source=source,
            working_directory=cwd,
            git_branch=git_branch,
            metadata={
                "permission_mode": ctx.input_data.get("permission_mode"),
                "transcript_path": ctx.get_transcript_path(),
            }
        )

    # Log to Markdown
    if ctx.config.storage.markdown_enabled:
        writer = MarkdownSessionWriter(
            str(ctx.storage_paths["sessions"]),
            ctx.session_id
        )
        writer.write_session_start(
            source=source,
            working_directory=cwd,
            git_branch=git_branch,
        )

    # Return context if verbose
    if ctx.hook_config.verbosity in ("verbose", "debug"):
        return {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": f"Session {ctx.session_id[:8]} logged. Source: {source}"
            }
        }

    return None


def main():
    runner = HookRunner("SessionStart")
    runner.run(handle_session_start)


if __name__ == "__main__":
    main()
