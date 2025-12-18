#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic"]
# ///
"""Auto-generate session summary using Claude.

Creates a 5-10 word action-oriented summary of what the agent is currently
working on. Updates every user prompt to reflect current focus.

Supports two backends:
1. "api" - Direct Anthropic API (fast, costs API credits)
2. "headless" - Headless Claude CLI (slower, uses Max subscription)

Configure via:
- Environment: SUMMARY_BACKEND=api|headless
- Config file: ~/.claude/statusline.conf or .claude/statusline.conf
  Format: BACKEND=api or BACKEND=headless

Default: "headless" (free with Max subscription)

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
    get_recent_messages,
    get_previous_summaries,
    format_messages_for_prompt,
    generate_with_backend,
    write_with_history,
    load_prompt_template,
    parse_hook_input,
)

DEBUG_PREFIX = "summary"


def log(msg: str):
    """Debug helper using our prefix."""
    debug(msg, DEBUG_PREFIX)


DEFAULT_PROMPT_TEMPLATE = """You are {agent_name}. Based on this recent conversation, write a 5-10 word first-person summary of what you're working on. Be concise and natural.

Previous summaries for continuity:
{prev_summaries}

Recent conversation:
{context}

Write ONLY the summary (5-10 words, first person), nothing else:"""


def main():
    log("Starting auto-summary hook")

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

    # Get context
    agent_name = get_agent_name(instances_dir, session_id)
    recent_messages = get_recent_messages(cwd, session_id, limit=6, prefix=DEBUG_PREFIX)
    context = format_messages_for_prompt(recent_messages)
    prev_summaries = get_previous_summaries(instances_dir, session_id, limit=3)

    log(f"Agent: {agent_name}, Context length: {len(context)}, Prev summaries: {len(prev_summaries)}")

    if not context:
        log("No context found in logs")
        return

    # Load and build prompt
    script_dir = Path(__file__).parent
    template = load_prompt_template(script_dir, "summary-prompt.txt", DEFAULT_PROMPT_TEMPLATE)

    prompt = template.format(
        agent_name=agent_name,
        prev_summaries=prev_summaries or "(None yet)",
        context=context,
    )

    # Generate summary
    summary = generate_with_backend(
        prompt=prompt,
        config=config,
        api_key=api_key,
        max_tokens=50,
        temperature=0.3,
        prefix=DEBUG_PREFIX,
    )

    if summary:
        log(f"Generated summary: {summary}")
        if write_with_history(instances_dir, session_id, "summaries", summary, DEBUG_PREFIX):
            log("Summary saved")
        else:
            log("Failed to save summary")
    else:
        log("No summary generated")


if __name__ == "__main__":
    # Enable debug with DEBUG_SUMMARY=1
    os.environ.setdefault("DEBUG_SUMMARY", os.environ.get("DEBUG_SUMMARY", ""))

    try:
        main()
    except Exception as e:
        if os.environ.get("DEBUG_SUMMARY", "").lower() in ("1", "true", "yes"):
            print(f"[summary] Fatal error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
        # Fail silently in production - summary is enhancement, not critical
        pass
