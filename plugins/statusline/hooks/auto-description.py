#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic"]
# ///
"""Auto-generate agent description using Claude.

Creates a 2-5 word "lifetime arc" description that captures WHO the agent is
and WHAT journey they've been on. Unlike the Summary (current focus), the
Description encodes the full trajectory through sophisticated context composition.

Context includes:
- First 5 user prompts (origin anchor - where we started)
- Most recent 20 user prompts (current trajectory)
- 10 most recent descriptions (arc continuity)
- 10 most recent summaries (activity log)
- Most recent Claude response (current state)

Triggers on every user prompt (like Summary) but evolves more slowly due to
the historical context weighting.

Configure via:
- Environment: SUMMARY_BACKEND=api|headless
- Config file: ~/.claude/statusline.conf or .claude/statusline.conf

Default: "headless" (free with Max subscription)
"""

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
    get_agent_name,
    get_first_messages,
    get_recent_user_prompts,
    get_latest_response,
    get_previous_summaries,
    get_previous_descriptions,
    format_messages_for_prompt,
    generate_with_backend,
    write_with_history,
    load_prompt_template,
    parse_hook_input,
    log_statusline_event,
)

DEBUG_PREFIX = "description"

# Debug helper that uses our prefix
def log(msg: str):
    debug(msg, DEBUG_PREFIX)


DEFAULT_PROMPT_TEMPLATE = """You are {agent_name}. Based on this conversation history, write a 2-5 word description of WHO you are in this session - your role, identity, or mission.

This should capture your lifetime arc: where you started and what journey you've been on. Think of it as a title or callsign that describes your purpose.

Examples of good descriptions:
- "Plugin infrastructure architect"
- "Debugging database migrations"
- "Feature dev workflow guide"
- "Statusline enhancement engineer"
- "Yoga schedule optimizer"

Session origin (first prompts show initial intent):
{first_prompts}

Recent trajectory (shows current work):
{recent_prompts}

Previous descriptions (your arc so far):
{prev_descriptions}

Recent activity summaries:
{prev_summaries}

Your most recent response:
{recent_response}

Write ONLY the description (2-5 words, describes your role/mission), nothing else:"""


def main():
    log("Starting auto-description hook")

    # Parse hook input
    data = parse_hook_input(DEBUG_PREFIX)
    if not data:
        log("No input data")
        return

    session_id = data.get("session_id", "")
    cwd = data.get("cwd", ".")

    log(f"Session: {session_id[:8] if session_id else 'none'}, CWD: {cwd}")

    if not session_id:
        log("No session_id")
        return

    # Load configuration
    config = get_config(cwd, DEBUG_PREFIX)
    log(f"Backend: {config['backend']}")

    api_key = get_api_key(cwd, DEBUG_PREFIX)
    instances_dir = get_instances_dir(cwd)

    # Build enhanced context
    agent_name = get_agent_name(instances_dir, session_id)

    # First 5 prompts (origin anchor)
    first_messages = get_first_messages(cwd, session_id, limit=5, prefix=DEBUG_PREFIX)
    first_prompts = format_messages_for_prompt(first_messages, "User")

    # Recent 20 prompts (current trajectory)
    recent_messages = get_recent_user_prompts(cwd, session_id, limit=20, prefix=DEBUG_PREFIX)
    recent_prompts = format_messages_for_prompt(recent_messages, "User")

    # History for continuity
    prev_descriptions = get_previous_descriptions(instances_dir, session_id, limit=10)
    prev_summaries = get_previous_summaries(instances_dir, session_id, limit=10)

    # Most recent Claude response
    recent_response = get_latest_response(cwd, session_id, prefix=DEBUG_PREFIX)

    log(f"Agent: {agent_name}, First prompts: {len(first_messages)}, Recent: {len(recent_messages)}")
    log(f"Prev descriptions: {len(prev_descriptions.split(chr(10))) if prev_descriptions else 0}")
    log(f"Prev summaries: {len(prev_summaries.split(chr(10))) if prev_summaries else 0}")

    # Need at least some context to generate
    if not recent_prompts and not first_prompts:
        log("No context found in logs")
        return

    # Load and build prompt
    script_dir = Path(__file__).parent
    template = load_prompt_template(script_dir, "description-prompt.txt", DEFAULT_PROMPT_TEMPLATE)

    prompt = template.format(
        agent_name=agent_name,
        first_prompts=first_prompts or "(No earlier prompts)",
        recent_prompts=recent_prompts or "(No recent prompts)",
        prev_descriptions=prev_descriptions or "(First description)",
        prev_summaries=prev_summaries or "(No summaries yet)",
        recent_response=recent_response[:500] if recent_response else "(No response yet)",
    )

    # Generate description
    description = generate_with_backend(
        prompt=prompt,
        config=config,
        api_key=api_key,
        max_tokens=30,
        temperature=0.3,
        prefix=DEBUG_PREFIX,
    )

    if description:
        log(f"Generated description: {description}")
        if write_with_history(instances_dir, session_id, "descriptions", description, DEBUG_PREFIX):
            log("Description saved")
        else:
            log("Failed to save description")
        log_statusline_event("description", session_id, description, True, DEBUG_PREFIX)
    else:
        log("No description generated")
        log_statusline_event("description", session_id, "", False, DEBUG_PREFIX)


if __name__ == "__main__":
    # Enable debug with DEBUG_DESCRIPTION=1
    os.environ.setdefault("DEBUG_DESCRIPTION", os.environ.get("DEBUG_DESCRIPTION", ""))

    try:
        main()
    except Exception as e:
        if os.environ.get("DEBUG_DESCRIPTION", "").lower() in ("1", "true", "yes"):
            print(f"[description] Fatal error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
        # Fail silently in production - description is enhancement, not critical
        pass
