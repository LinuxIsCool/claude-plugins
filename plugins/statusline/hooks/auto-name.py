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
import subprocess
import sys
from pathlib import Path

DEBUG = os.environ.get("DEBUG_NAME", "").lower() in ("1", "true", "yes")


def debug(msg: str):
    """Print debug message if DEBUG is enabled."""
    if DEBUG:
        print(f"[auto-name] {msg}", file=sys.stderr)


def get_config(cwd: str) -> dict:
    """Load configuration from files or environment."""
    config = {"backend": "headless"}  # Default to free option

    for loc in [Path(cwd) / ".claude/statusline.conf", Path.home() / ".claude/statusline.conf"]:
        if loc.exists():
            try:
                for line in loc.read_text().strip().split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip().upper()
                        value = value.strip().strip('"').strip("'")
                        if key == "BACKEND":
                            config["backend"] = value.lower()
                debug(f"Config loaded from {loc}")
                break
            except Exception as e:
                debug(f"Failed to load config from {loc}: {e}")

    if os.environ.get("SUMMARY_BACKEND"):
        config["backend"] = os.environ["SUMMARY_BACKEND"].lower()

    return config


def get_api_key(cwd: str) -> str:
    """Find API key from multiple sources."""
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if key:
        return key

    for loc in [Path(cwd) / ".claude" / "anthropic_api_key", Path.home() / ".claude" / "anthropic_api_key"]:
        if loc.exists():
            key = loc.read_text().strip()
            if key:
                return key
    return ""


def get_instances_dir(cwd: str) -> Path:
    """Find instances directory."""
    for loc in [Path(cwd) / ".claude/instances", Path.home() / ".claude/instances"]:
        if loc.exists():
            return loc
    return Path.home() / ".claude/instances"


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
    """Update the session name in registry.json."""
    registry = instances_dir / "registry.json"
    if not registry.exists():
        debug("Registry not found")
        return False

    try:
        data = json.loads(registry.read_text())
        if session_id in data:
            data[session_id]["name"] = name
            registry.write_text(json.dumps(data, indent=2))
            debug(f"Updated registry: {session_id} -> {name}")
            return True
        else:
            debug(f"Session {session_id} not in registry")
            return False
    except Exception as e:
        debug(f"Registry update failed: {e}")
        return False


def load_prompt_template() -> str:
    """Load name generation prompt template."""
    script_dir = Path(__file__).parent
    locations = [
        script_dir / "name-prompt.txt",
        Path.home() / ".claude" / "name-prompt.txt",
    ]

    for loc in locations:
        if loc.exists():
            try:
                template = loc.read_text().strip()
                if template:
                    debug(f"Loaded prompt template from {loc}")
                    return template
            except:
                pass

    # Default prompt
    return """Based on this user's first message, generate a creative 1-2 word name for this Claude session.

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


def build_prompt(user_prompt: str) -> str:
    """Build the name generation prompt."""
    template = load_prompt_template()
    return template.format(user_prompt=user_prompt[:500])  # Limit context


def generate_name_api(prompt: str, api_key: str) -> str:
    """Generate name using Anthropic API directly."""
    debug("Using API backend")
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=20,
            temperature=0.7,  # Slightly higher for creativity
            messages=[{"role": "user", "content": prompt}],
        )

        name = msg.content[0].text.strip()
        # Clean up: remove quotes, take first word(s), capitalize
        name = name.strip('"').strip("'").split("\n")[0].strip()
        # Limit to 2 words max
        words = name.split()[:2]
        name = " ".join(w.capitalize() for w in words)
        debug(f"API response: {name}")
        return name
    except Exception as e:
        debug(f"API error: {e}")
        return ""


def generate_name_headless(prompt: str) -> str:
    """Generate name using headless Claude CLI."""
    debug("Using headless backend")
    try:
        env = os.environ.copy()
        env.pop("ANTHROPIC_API_KEY", None)  # Force Max subscription

        result = subprocess.run(
            [
                "claude",
                "-p",
                prompt,
                "--model",
                "haiku",
                "--no-session-persistence",
                "--tools",
                "",
                "--setting-sources",
                "",  # Disable all settings = no hooks, no plugins
            ],
            input="",
            capture_output=True,
            text=True,
            timeout=30,
            env=env,
        )

        if result.returncode != 0:
            debug(f"Headless error: {result.stderr}")
            return ""

        name = result.stdout.strip()
        name = name.strip('"').strip("'").split("\n")[0].strip()
        words = name.split()[:2]
        name = " ".join(w.capitalize() for w in words)
        debug(f"Headless response: {name}")
        return name
    except subprocess.TimeoutExpired:
        debug("Headless timeout (30s)")
        return ""
    except Exception as e:
        debug(f"Headless error: {e}")
        return ""


def generate_name(user_prompt: str, config: dict, api_key: str) -> str:
    """Generate name using configured backend."""
    if not user_prompt:
        debug("No user prompt - skipping name generation")
        return ""

    prompt = build_prompt(user_prompt)
    backend = config.get("backend", "headless")

    if backend == "api":
        if not api_key:
            debug("API backend selected but no API key - falling back to headless")
            return generate_name_headless(prompt)
        return generate_name_api(prompt, api_key)
    else:
        return generate_name_headless(prompt)


def main():
    debug("Starting auto-name hook")

    # Read hook input
    raw_input = ""
    try:
        if not sys.stdin.isatty():
            raw_input = sys.stdin.read()
        if not raw_input:
            raw_input = os.environ.get("HOOK_INPUT", "")
        data = json.loads(raw_input or "{}")
    except Exception as e:
        debug(f"Failed to parse input: {e}")
        data = {}

    if not data:
        debug("No input data")
        return

    session_id = data.get("session_id", "")
    cwd = data.get("cwd", ".")
    user_prompt = data.get("prompt", "")

    debug(f"Session: {session_id[:8] if session_id else 'none'}")

    if not session_id:
        debug("No session_id")
        return

    instances_dir = get_instances_dir(cwd)

    # Check if this is the first prompt
    count = get_prompt_count(instances_dir, session_id)
    debug(f"Prompt count: {count}")

    # Only trigger on first prompt (count should be 1 after increment)
    if count != 1:
        debug(f"Not first prompt (count={count}), skipping")
        return

    if not user_prompt:
        debug("No user prompt in hook data")
        return

    # Load configuration
    config = get_config(cwd)
    api_key = get_api_key(cwd)

    # Generate name
    name = generate_name(user_prompt, config, api_key)

    if name:
        debug(f"Generated name: {name}")
        if update_registry_name(instances_dir, session_id, name):
            debug("Name saved to registry")
        else:
            debug("Failed to save name")
    else:
        debug("No name generated")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if DEBUG:
            print(f"[auto-name] Fatal error: {e}", file=sys.stderr)
        pass
