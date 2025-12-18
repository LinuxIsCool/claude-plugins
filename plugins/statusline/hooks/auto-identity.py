#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic"]
# ///
"""Unified identity generator - generates name, description, and summary in ONE call.

This consolidates auto-name.py, auto-description.py, and auto-summary.py into a single
hook that makes ONE subprocess/API call instead of THREE. This is 3x faster and eliminates
resource contention that was causing system freezes.

Generation logic:
- NAME: Only on first prompt (when auto_named is false)
- DESCRIPTION: On first prompt, then stable unless context significantly changes
- SUMMARY: Every prompt (reflects current work)

Output format requested from Claude:
    NAME: <1-2 word symbolic name>
    DESCRIPTION: <Plugin Role format>
    SUMMARY: <5-10 word first-person summary>

The response is parsed and each value is saved to its respective location.
"""

import fcntl
import json
import os
import re
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
    get_previous_descriptions,
    format_messages_for_prompt,
    generate_with_backend,
    write_with_history,
    update_registry_task,
    load_prompt_template,
    parse_hook_input,
    log_statusline_event,
)

DEBUG_PREFIX = "identity"


def log(msg: str):
    """Debug helper using our prefix."""
    debug(msg, DEBUG_PREFIX)


def check_needs_name(instances_dir: Path, session_id: str) -> bool:
    """Check if session needs a name (hasn't been auto_named yet)."""
    registry = instances_dir / "registry.json"
    if not registry.exists():
        return False

    try:
        with open(registry) as f:
            data = json.load(f)
        session_data = data.get(session_id, {})
        return not session_data.get("auto_named", False)
    except:
        return False


def claim_naming_rights(instances_dir: Path, session_id: str) -> bool:
    """Atomically claim naming rights for this session.

    Returns True if we successfully claimed, False if already claimed.
    """
    registry = instances_dir / "registry.json"
    if not registry.exists():
        return False

    try:
        with open(registry, "r+") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                data = json.load(f)
                session_data = data.get(session_id, {})

                if session_data.get("auto_named", False):
                    log("Already auto_named, skipping name generation")
                    return False

                # Claim it
                session_data["auto_named"] = True
                data[session_id] = session_data

                f.seek(0)
                json.dump(data, f, indent=2)
                f.truncate()

                log("Claimed naming rights")
                return True
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except Exception as e:
        log(f"Error claiming naming rights: {e}")
        return False


def save_name(instances_dir: Path, session_id: str, name: str) -> bool:
    """Save the generated name to registry."""
    registry = instances_dir / "registry.json"
    if not registry.exists():
        return False

    try:
        with open(registry, "r+") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                data = json.load(f)
                if session_id in data:
                    data[session_id]["name"] = name
                    f.seek(0)
                    json.dump(data, f, indent=2)
                    f.truncate()
                    log(f"Saved name: {name}")
                    return True
                return False
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except Exception as e:
        log(f"Error saving name: {e}")
        return False


def save_description(instances_dir: Path, session_id: str, description: str):
    """Save description to file."""
    desc_dir = instances_dir / "descriptions"
    desc_dir.mkdir(parents=True, exist_ok=True)
    desc_file = desc_dir / f"{session_id}.txt"
    desc_file.write_text(description)
    log(f"Saved description: {description}")


def save_summary(instances_dir: Path, session_id: str, summary: str, cwd: str):
    """Save summary to file and registry."""
    write_with_history(instances_dir, session_id, "summaries", summary, DEBUG_PREFIX)
    update_registry_task(instances_dir, session_id, summary, DEBUG_PREFIX)


def build_combined_prompt(
    needs_name: bool,
    user_prompt: str,
    agent_name: str,
    context: str,
    prev_summaries: str,
    prev_descriptions: str,
    first_prompts: str,
    recent_prompts: str,
) -> str:
    """Build a combined prompt for all three generations."""

    sections = []

    sections.append(f"""You are {agent_name}, a Claude Code assistant.

Generate identity information based on the USER'S ACTUAL MESSAGE, not assumptions about the directory or environment.""")

    # Conditional name section
    if needs_name:
        sections.append("""
=== NAME ===
Generate a 1-2 word symbolic name (callsign) for this session.
- Base it on the user's stated intent, NOT the directory path
- Be evocative and memorable
- For greetings/tests: use neutral names like "Spark", "Echo", "Nexus"
- For specific work: capture that domain""")

    sections.append("""
=== DESCRIPTION ===
Generate a 2-word description.
- "Hello" → "General Assistant"
- "Testing" → "General Assistant"
- "Fix the statusline hooks" → "Statusline Engineer"
- Base it ONLY on user's explicit words, NOT directory path""")

    sections.append("""
=== SUMMARY ===
Generate a 5-10 word first-person summary.
- "Hello/Hi/Hey" → "Awaiting task direction"
- "Testing" or "Test" → "Running a test" or "Testing the system"
- Specific task → Describe that task literally
- NEVER infer from directory path - use ONLY what user explicitly stated""")

    # Context section
    sections.append(f"""
=== CONTEXT ===
User's prompt: {user_prompt[:500] if user_prompt else '(none)'}

Previous summaries (for continuity):
{prev_summaries}

Previous descriptions (maintain stability):
{prev_descriptions}

Session origin (first prompts):
{first_prompts}

Recent trajectory:
{recent_prompts}

Recent conversation:
{context}""")

    # Output format - JSON on single line for headless compatibility
    # CRITICAL: headless backend only captures first line, so NO code blocks
    if needs_name:
        sections.append("""
=== OUTPUT ===
CRITICAL: Output ONLY this JSON on ONE line, NO code blocks, NO explanation:
{"name":"NAME","description":"DESCRIPTION","summary":"SUMMARY"}""")
    else:
        sections.append("""
=== OUTPUT ===
CRITICAL: Output ONLY this JSON on ONE line, NO code blocks, NO explanation:
{"description":"DESCRIPTION","summary":"SUMMARY"}""")

    return "\n".join(sections)


def parse_response(response: str, needs_name: bool) -> dict:
    """Parse the JSON response into components."""
    result = {"name": None, "description": None, "summary": None}

    # Try to parse as JSON
    try:
        # Clean up response - remove markdown code blocks if present
        cleaned = response.strip()
        if cleaned.startswith("```"):
            # Extract content between code blocks
            lines = cleaned.split("\n")
            cleaned = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

        # Find JSON object in response
        json_match = re.search(r'\{[^{}]+\}', cleaned)
        if json_match:
            data = json.loads(json_match.group())
            result["name"] = data.get("name")
            result["description"] = data.get("description")
            result["summary"] = data.get("summary")

            # Clean up name to max 2 words
            if result["name"]:
                words = result["name"].split()[:2]
                result["name"] = " ".join(words)

            return result
    except json.JSONDecodeError:
        pass

    # Fallback: try line-based parsing
    name_match = re.search(r'NAME:\s*(.+?)(?:\n|$)', response, re.IGNORECASE)
    desc_match = re.search(r'DESCRIPTION:\s*(.+?)(?:\n|$)', response, re.IGNORECASE)
    summary_match = re.search(r'SUMMARY:\s*(.+?)(?:\n|$)', response, re.IGNORECASE)

    if needs_name and name_match:
        name = name_match.group(1).strip().strip('"\'')
        words = name.split()[:2]
        result["name"] = " ".join(words)

    if desc_match:
        result["description"] = desc_match.group(1).strip().strip('"\'')

    if summary_match:
        result["summary"] = summary_match.group(1).strip().strip('"\'')

    return result


def main():
    log("Starting unified identity hook")

    # Parse input
    data = parse_hook_input(DEBUG_PREFIX)
    if not data:
        return

    session_id = data.get("session_id", "")
    cwd = data.get("cwd", ".")
    user_prompt = data.get("prompt", "")
    transcript_path = data.get("transcript_path", "")

    log(f"Session: {session_id[:8] if session_id else 'none'}")

    if not session_id:
        log("No session_id, exiting")
        return

    # Get configuration
    config = get_config(cwd, DEBUG_PREFIX)
    api_key = get_api_key(cwd, DEBUG_PREFIX)
    instances_dir = get_instances_dir(cwd)

    if not instances_dir:
        log("No instances directory found")
        return

    # Determine what we need to generate
    needs_name = check_needs_name(instances_dir, session_id)

    # If we need a name, try to claim naming rights
    if needs_name:
        needs_name = claim_naming_rights(instances_dir, session_id)

    log(f"Needs name: {needs_name}")

    # Gather context
    agent_name = get_agent_name(instances_dir, session_id)
    messages = get_recent_messages(cwd, session_id, limit=10, prefix=DEBUG_PREFIX)
    context = format_messages_for_prompt(messages, DEBUG_PREFIX)
    prev_summaries = get_previous_summaries(instances_dir, session_id, limit=3)
    prev_descriptions = get_previous_descriptions(instances_dir, session_id, limit=3)

    # Get first/recent prompts for description stability
    first_prompts = "\n".join([m.get("content", "")[:200] for m in messages[:2]]) if messages else ""
    recent_prompts = "\n".join([m.get("content", "")[:200] for m in messages[-3:]]) if messages else ""

    # Build combined prompt
    prompt = build_combined_prompt(
        needs_name=needs_name,
        user_prompt=user_prompt,
        agent_name=agent_name,
        context=context,
        prev_summaries=prev_summaries,
        prev_descriptions=prev_descriptions,
        first_prompts=first_prompts,
        recent_prompts=recent_prompts,
    )

    # Generate with single call (multiline=True to get full JSON response)
    log("Generating identity (single call)...")
    response = generate_with_backend(
        prompt=prompt,
        config=config,
        api_key=api_key,
        max_tokens=100,  # Enough for all three
        temperature=0.5,
        prefix=DEBUG_PREFIX,
        multiline=True,  # Need full response for JSON parsing
    )

    if not response:
        log("Generation failed")
        log_statusline_event("identity", session_id, "", False, DEBUG_PREFIX)
        return

    log(f"Response: {response}")

    # Parse response
    result = parse_response(response, needs_name)
    log(f"Parsed: {result}")

    # Save each component
    success = True

    if needs_name and result["name"]:
        if save_name(instances_dir, session_id, result["name"]):
            log_statusline_event("name", session_id, result["name"], True, DEBUG_PREFIX)
        else:
            success = False
            log_statusline_event("name", session_id, "", False, DEBUG_PREFIX)

    if result["description"]:
        save_description(instances_dir, session_id, result["description"])
        log_statusline_event("description", session_id, result["description"], True, DEBUG_PREFIX)
    else:
        log_statusline_event("description", session_id, "", False, DEBUG_PREFIX)
        success = False

    if result["summary"]:
        save_summary(instances_dir, session_id, result["summary"], cwd)
        log_statusline_event("summary", session_id, result["summary"], True, DEBUG_PREFIX)
    else:
        log_statusline_event("summary", session_id, "", False, DEBUG_PREFIX)
        success = False

    log(f"Identity generation complete, success={success}")


if __name__ == "__main__":
    main()
