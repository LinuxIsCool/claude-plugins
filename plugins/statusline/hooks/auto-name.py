#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic"]
# ///
"""Auto-generate creative session name using Claude on first user prompt.

Triggers only once per session using the registry's `auto_named` flag with file locking.
Uses the user's initial prompt as context to generate a meaningful 1-2 word name.

NOTE: Since Claude Code runs all hooks in parallel, we use fcntl file locking on
registry.json to atomically check-and-set the `auto_named` flag. This ensures
exactly one naming attempt per session without needing separate lock files.

Supports two backends (same as auto-summary.py):
1. "api" - Direct Anthropic API (fast, costs API credits)
2. "headless" - Headless Claude CLI (slower, uses Max subscription)

Configure via:
- Environment: SUMMARY_BACKEND=api|headless
- Config file: ~/.claude/statusline.conf or .claude/statusline.conf

Default: "headless" (free with Max subscription)
"""

import fcntl
import json
import os
import sys
from pathlib import Path

# Add lib to path for shared infrastructure
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from claude_backend import (
    debug,
    get_config,
    get_api_key,
    get_instances_dir,
    generate_with_backend,
    load_prompt_template,
    parse_hook_input,
    log_statusline_event,
)

DEBUG_PREFIX = "name"


def log(msg: str):
    """Debug helper using our prefix."""
    debug(msg, DEBUG_PREFIX)


def try_claim_and_update_name(instances_dir: Path, session_id: str, name: str) -> bool:
    """Atomically claim naming rights and update name in one transaction.

    Uses fcntl file locking on registry.json to ensure only one process can
    claim naming rights per session. This replaces the separate lock file approach
    with a single source of truth.

    The function:
    1. Acquires exclusive lock on registry
    2. Checks if session exists and hasn't been auto-named yet
    3. If claimable, sets both `auto_named=True` and the new name atomically
    4. Releases lock

    Returns:
        True if we claimed naming rights and updated the name
        False if already claimed, session missing, or error occurred
    """
    registry = instances_dir / "registry.json"
    if not registry.exists():
        log("Registry not found")
        return False

    try:
        with open(registry, "r+") as f:
            # Acquire exclusive lock (blocks until available)
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                data = json.load(f)

                if session_id not in data:
                    log(f"Session {session_id} not in registry")
                    return False

                # Check if already auto-named (atomic check)
                if data[session_id].get("auto_named", False):
                    log("Already auto-named, skipping")
                    return False

                # Claim naming rights and update name atomically
                data[session_id]["auto_named"] = True
                data[session_id]["name"] = name

                # Rewind and truncate before writing
                f.seek(0)
                f.truncate()
                json.dump(data, f, indent=2)
                log(f"Claimed and named: {session_id} -> {name}")
                return True
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except Exception as e:
        log(f"Registry operation failed: {e}")
        return False


DEFAULT_PROMPT_TEMPLATE = """Generate a creative 1-2 word name for an AI assistant session based on the user's first message.

CRITICAL RULES:
- NEVER use "Claude" or "Assistant" as the name
- NEVER use the exact command name (e.g., don't output "Status" for "/status")
- For minimal prompts like "Hello" or "Test", infer purpose from context or use evocative general names

The name should be a codename/callsign that captures the session's likely purpose or energy.

Good name patterns:
- Task-based: "Architect", "Debugger", "Scribe", "Refactor"
- Evocative: "Phoenix", "Sentinel", "Catalyst", "Navigator"
- Mission-style: "Silent Keeper", "Thread Hunter", "Code Whisperer"

For greetings/minimal prompts, use evocative names like:
- "Companion" (friendly greeting)
- "Explorer" (unclear/open-ended)
- "Seeker" (curious/questioning)

User's first message:
{user_prompt}

One creative name (1-2 words only):"""


def clean_name(raw_name: str) -> str:
    """Clean up generated name: capitalize, limit to 2 words."""
    name = raw_name.strip()
    # Strip common formatting artifacts
    name = name.strip('"').strip("'").strip("`").strip("*")
    # Take first line only
    name = name.split("\n")[0].strip()
    # Remove any remaining markdown bold
    name = name.replace("**", "").replace("__", "")
    # Limit to 2 words, capitalize
    words = name.split()[:2]
    return " ".join(w.capitalize() for w in words)


def main():
    log("Starting auto-name hook")

    # Parse hook input
    data = parse_hook_input(DEBUG_PREFIX)
    if not data:
        log("No input data")
        return

    session_id = data.get("session_id", "")
    cwd = data.get("cwd", ".")
    user_prompt = data.get("prompt", "")

    log(f"Session: {session_id[:8] if session_id else 'none'}")

    if not session_id:
        log("No session_id")
        return

    if not user_prompt:
        log("No user prompt in hook data")
        return

    instances_dir = get_instances_dir(cwd)

    # Load configuration
    config = get_config(cwd, DEBUG_PREFIX)
    api_key = get_api_key(cwd, DEBUG_PREFIX)

    # Load and build prompt
    script_dir = Path(__file__).parent
    template = load_prompt_template(script_dir, "name-prompt.txt", DEFAULT_PROMPT_TEMPLATE)

    prompt = template.format(user_prompt=user_prompt[:500])

    # Generate name with higher temperature for creativity
    raw_name = generate_with_backend(
        prompt=prompt,
        config=config,
        api_key=api_key,
        max_tokens=20,
        temperature=0.7,  # Higher for creativity
        prefix=DEBUG_PREFIX,
    )

    if raw_name:
        name = clean_name(raw_name)
        log(f"Generated name: {name}")
        # Atomically claim naming rights and update - only first caller wins
        if try_claim_and_update_name(instances_dir, session_id, name):
            log("Name saved to registry")
            log_statusline_event("name", session_id, name, True, DEBUG_PREFIX)
        # If claim failed, another hook instance already named this session
    else:
        log("No name generated")
        log_statusline_event("name", session_id, "", False, DEBUG_PREFIX)


if __name__ == "__main__":
    # Enable debug with DEBUG_NAME=1
    os.environ.setdefault("DEBUG_NAME", os.environ.get("DEBUG_NAME", ""))

    try:
        main()
    except Exception as e:
        if os.environ.get("DEBUG_NAME", "").lower() in ("1", "true", "yes"):
            print(f"[name] Fatal error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
        pass
