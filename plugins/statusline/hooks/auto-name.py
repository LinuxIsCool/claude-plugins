#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic"]
# ///
"""Auto-generate creative session name using Claude on first user prompt.

Triggers only once per session - on the first user prompt (count == 1).
Uses the user's initial prompt as context to generate a meaningful 1-2 word name.

Supports two backends (same as auto-summary.py):
1. "api" - Direct Anthropic API (fast, costs API credits)
2. "headless" - Headless Claude CLI (slower, uses Max subscription)

Configure via:
- Environment: SUMMARY_BACKEND=api|headless
- Config file: ~/.claude/statusline.conf or .claude/statusline.conf

Default: "headless" (free with Max subscription)
"""

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
)

DEBUG_PREFIX = "name"


def log(msg: str):
    """Debug helper using our prefix."""
    debug(msg, DEBUG_PREFIX)


def get_prompt_count(instances_dir: Path, session_id: str) -> int:
    """Get current prompt count for session."""
    count_file = instances_dir / "counts" / f"{session_id}.txt"
    if count_file.exists():
        try:
            return int(count_file.read_text().strip())
        except:
            pass
    return 0


def update_registry_name(instances_dir: Path, session_id: str, name: str) -> bool:
    """Update the session name in registry.json with file locking to prevent race conditions."""
    import fcntl

    registry = instances_dir / "registry.json"
    if not registry.exists():
        log("Registry not found")
        return False

    try:
        # Use file locking to prevent race conditions from concurrent hooks
        with open(registry, "r+") as f:
            # Acquire exclusive lock (blocks until available)
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                data = json.load(f)
                if session_id in data:
                    data[session_id]["name"] = name
                    # Rewind and truncate before writing
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent=2)
                    log(f"Updated registry: {session_id} -> {name}")
                    return True
                else:
                    log(f"Session {session_id} not in registry")
                    return False
            finally:
                # Lock is released when file is closed, but explicit unlock is cleaner
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except Exception as e:
        log(f"Registry update failed: {e}")
        return False


DEFAULT_PROMPT_TEMPLATE = """Based on this user's first message, generate a creative 1-2 word name for this Claude session.

The name should be evocative and memorable - like a codename or callsign that hints at the session's purpose.

Examples of good names:
- "Navigator" (for navigation/exploration tasks)
- "Architect" (for design/planning tasks)
- "Debugger" (for fixing issues)
- "Scribe" (for documentation)
- "Refactor" (for code cleanup)
- "Phoenix" (for resurrection/restart tasks)
- "Sentinel" (for monitoring/security)
- "Catalyst" (for transformation tasks)

User's first message:
{user_prompt}

Respond with ONLY the 1-2 word name, nothing else:"""


def clean_name(raw_name: str) -> str:
    """Clean up generated name: capitalize, limit to 2 words."""
    name = raw_name.strip().strip('"').strip("'").split("\n")[0].strip()
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

    instances_dir = get_instances_dir(cwd)

    # Check if this is the first prompt
    count = get_prompt_count(instances_dir, session_id)
    log(f"Prompt count: {count}")

    # Only trigger on first prompt (count should be 1 after increment)
    if count != 1:
        log(f"Not first prompt (count={count}), skipping")
        return

    if not user_prompt:
        log("No user prompt in hook data")
        return

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
        if update_registry_name(instances_dir, session_id, name):
            log("Name saved to registry")
        else:
            log("Failed to save name")
    else:
        log("No name generated")


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
