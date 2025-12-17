#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic"]
# ///
"""Auto-generate session summary using Claude.

Supports two backends:
1. "api" - Direct Anthropic API (fast, costs API credits)
2. "headless" - Headless Claude CLI (slower, uses Max subscription)

Configure via:
- Environment: SUMMARY_BACKEND=api|headless
- Config file: ~/.claude/statusline.conf or .claude/statusline.conf
  Format: BACKEND=api or BACKEND=headless

Default: "headless" (free with Max subscription)

Requires for API backend:
- ANTHROPIC_API_KEY environment variable, or
- ~/.claude/anthropic_api_key file

=== ENGINEERING TRADEOFFS ===

| Metric            | API Direct    | Headless Claude |
|-------------------|---------------|-----------------|
| Latency (avg)     | ~1.5s         | ~5.2s           |
| Cost              | ~$0.00024/req | $0 (Max sub)    |
| Memory overhead   | ~10 MB        | ~450 MB         |
| Startup overhead  | Minimal       | Process spawn   |
| Reliability       | High          | Medium          |
| Requires          | API key       | Max subscription|

Monthly cost projection (API):
- 10 summaries/day:  $0.07/month
- 100 summaries/day: $0.72/month
- 500 summaries/day: $3.60/month

Recommendation:
- Use "headless" if you have Max subscription and don't mind latency
- Use "api" if you need fast updates and have API credits
"""

import json
import os
import subprocess
import sys
from pathlib import Path

DEBUG = os.environ.get("DEBUG_SUMMARY", "").lower() in ("1", "true", "yes")


def debug(msg: str):
    """Print debug message if DEBUG is enabled."""
    if DEBUG:
        print(f"[auto-summary] {msg}", file=sys.stderr)


def get_config(cwd: str) -> dict:
    """Load configuration from files or environment."""
    config = {"backend": "headless"}  # Default to free option

    # Check config files (project takes precedence)
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

    # Environment overrides
    if os.environ.get("SUMMARY_BACKEND"):
        config["backend"] = os.environ["SUMMARY_BACKEND"].lower()
        debug(f"Backend from environment: {config['backend']}")

    return config


def get_api_key(cwd: str) -> str:
    """Find API key from multiple sources."""
    # 1. Environment variable (highest priority)
    key = os.environ.get("ANTHROPIC_API_KEY", "")
    if key:
        debug("API key found in environment")
        return key

    # 2. Project-local config
    project_key = Path(cwd) / ".claude" / "anthropic_api_key"
    if project_key.exists():
        key = project_key.read_text().strip()
        if key:
            debug(f"API key found in {project_key}")
            return key

    # 3. User home config
    home_key = Path.home() / ".claude" / "anthropic_api_key"
    if home_key.exists():
        key = home_key.read_text().strip()
        if key:
            debug(f"API key found in {home_key}")
            return key

    debug("No API key found")
    return ""


def get_instances_dir(cwd: str) -> Path:
    """Find instances directory."""
    for loc in [Path(cwd) / ".claude/instances", Path.home() / ".claude/instances"]:
        if loc.exists():
            return loc
    return Path.home() / ".claude/instances"


def get_agent_name(instances_dir: Path, session_id: str) -> str:
    """Get agent name from registry."""
    registry = instances_dir / "registry.json"
    if registry.exists():
        try:
            data = json.loads(registry.read_text())
            return data.get(session_id, {}).get("name", "Claude")
        except:
            pass
    return "Claude"


def get_recent_context(cwd: str, session_id: str) -> str:
    """Extract recent user/assistant messages from logs."""
    log_dir = Path(cwd) / ".claude/logging"
    if not log_dir.exists():
        log_dir = Path.home() / ".claude/logging"

    # Find log file for this session
    short_id = session_id[:8]
    log_files = list(log_dir.rglob(f"*{short_id}*.jsonl"))
    if not log_files:
        return ""

    log_file = log_files[0]

    # Extract recent messages
    messages = []
    try:
        for line in log_file.read_text().strip().split("\n"):
            if not line:
                continue
            entry = json.loads(line)
            if entry.get("type") == "UserPromptSubmit":
                prompt = entry.get("data", {}).get("prompt", "")
                if prompt:
                    messages.append(f"User: {prompt[:150]}")
            elif entry.get("type") == "AssistantResponse":
                response = entry.get("data", {}).get("response", "")
                if response:
                    messages.append(f"Assistant: {response[:150]}")
    except:
        pass

    # Return last 6 messages
    return "\n".join(messages[-6:])


def get_previous_summaries(instances_dir: Path, session_id: str) -> str:
    """Get previous summaries for continuity."""
    history_file = instances_dir / "summaries" / f"{session_id}.history"
    if history_file.exists():
        try:
            lines = history_file.read_text().strip().split("\n")
            return "\n".join(lines[-3:])
        except:
            pass
    return ""


DEFAULT_PROMPT_TEMPLATE = """You are {agent_name}. Based on this recent conversation, write a 5-10 word first-person summary of what you're working on. Be concise and natural.

Previous summaries for continuity:
{prev_summaries}

Recent conversation:
{context}

Write ONLY the summary (5-10 words, first person), nothing else:"""


def load_prompt_template() -> str:
    """Load prompt template from file or use default."""
    # Check multiple locations for custom prompt
    script_dir = Path(__file__).parent
    locations = [
        script_dir / "summary-prompt.txt",  # Same dir as script
        Path.home() / ".claude" / "summary-prompt.txt",  # User config
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

    debug("Using default prompt template")
    return DEFAULT_PROMPT_TEMPLATE


def build_prompt(agent_name: str, context: str, prev_summaries: str) -> str:
    """Build the summary generation prompt from template."""
    template = load_prompt_template()
    return template.format(
        agent_name=agent_name,
        context=context,
        prev_summaries=prev_summaries
    )


def generate_summary_api(prompt: str, api_key: str) -> str:
    """Generate summary using Anthropic API directly."""
    debug("Using API backend")
    try:
        import anthropic

        client = anthropic.Anthropic(api_key=api_key)

        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=50,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}],
        )

        summary = msg.content[0].text.strip()
        summary = summary.strip('"').strip("'").split("\n")[0].strip()
        debug(f"API response: {summary}")
        return summary
    except Exception as e:
        debug(f"API error: {e}")
        return ""


def generate_summary_headless(prompt: str) -> str:
    """Generate summary using headless Claude CLI."""
    debug("Using headless backend")
    try:
        # Unset ANTHROPIC_API_KEY to force Max subscription usage
        env = os.environ.copy()
        env.pop("ANTHROPIC_API_KEY", None)

        # Run headless Claude with:
        # - stdin input to avoid hanging
        # - no tools (simple text response)
        # - no session persistence
        # - no setting sources (disables ALL hooks/plugins - prevents recursion)
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

        summary = result.stdout.strip()
        summary = summary.strip('"').strip("'").split("\n")[0].strip()
        debug(f"Headless response: {summary}")
        return summary
    except subprocess.TimeoutExpired:
        debug("Headless timeout (30s)")
        return ""
    except Exception as e:
        debug(f"Headless error: {e}")
        return ""


def generate_summary(agent_name: str, context: str, prev_summaries: str, config: dict, api_key: str) -> str:
    """Generate summary using configured backend."""
    if not context:
        debug("No context - skipping summary generation")
        return ""

    prompt = build_prompt(agent_name, context, prev_summaries)
    backend = config.get("backend", "headless")

    if backend == "api":
        if not api_key:
            debug("API backend selected but no API key - falling back to headless")
            return generate_summary_headless(prompt)
        return generate_summary_api(prompt, api_key)
    else:
        return generate_summary_headless(prompt)


def main():
    debug("Starting auto-summary hook")

    # Read hook input from stdin or HOOK_INPUT env var (for uv run compatibility)
    raw_input = ""
    try:
        # First try stdin
        if not sys.stdin.isatty():
            raw_input = sys.stdin.read()
        # Fall back to environment variable (set by wrapper script)
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

    debug(f"Session: {session_id[:8] if session_id else 'none'}, CWD: {cwd}")

    if not session_id:
        debug("No session_id")
        return

    # Load configuration
    config = get_config(cwd)
    debug(f"Backend: {config['backend']}")

    # Get API key (needed for API backend, optional for headless)
    api_key = get_api_key(cwd)

    instances_dir = get_instances_dir(cwd)
    summaries_dir = instances_dir / "summaries"
    summaries_dir.mkdir(parents=True, exist_ok=True)

    # Get context
    agent_name = get_agent_name(instances_dir, session_id)
    context = get_recent_context(cwd, session_id)
    prev_summaries = get_previous_summaries(instances_dir, session_id)

    debug(f"Agent: {agent_name}, Context length: {len(context)}, Prev summaries: {len(prev_summaries)}")

    if not context:
        debug("No context found in logs")
        return

    # Generate summary
    summary = generate_summary(agent_name, context, prev_summaries, config, api_key)

    if summary:
        debug(f"Generated summary: {summary}")
        # Write to files
        summary_file = summaries_dir / f"{session_id}.txt"
        history_file = summaries_dir / f"{session_id}.history"

        summary_file.write_text(summary)
        with open(history_file, "a") as f:
            f.write(summary + "\n")
        debug("Summary saved")
    else:
        debug("No summary generated")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if DEBUG:
            print(f"[auto-summary] Fatal error: {e}", file=sys.stderr)
        # Fail silently in production - summary is enhancement, not critical
        pass
