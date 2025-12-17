#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Intelligent version control that commits based on human-agent collaboration signals.

This hook runs on UserPromptSubmit and analyzes the user's message to determine
if it signals approval of previous work. If so, it uses headless Claude Haiku
to generate a rich, insightful commit message that captures the "third mind" -
the collaborative understanding that emerges from human-agent interaction.

Key features:
- Sentiment analysis: "looks good" → commit, "still broken" → skip
- Safety checks: Never commit secrets, warn on large files
- Rich commit messages: Context, insights, third mind notes
- .gitignore suggestions: Proactive guidance for common pitfalls

Based on proven patterns from statusline plugin's auto-name.py and auto-summary.py.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

DEBUG = os.environ.get("DEBUG_AUTOCOMMIT", "").lower() in ("1", "true", "yes")

# =============================================================================
# OPTIONAL INTEGRATIONS
# =============================================================================
# This plugin works standalone but is enhanced by other ecosystem plugins:
#
# - statusline: Provides human-readable agent names (otherwise uses session ID)
# - logging: Provides conversation context (otherwise decides from prompt + diff)
#
# These are detected at runtime and used if available.
# =============================================================================

# Safety patterns - never commit these
# Note: Patterns are matched with re.IGNORECASE
SENSITIVE_PATTERNS = [
    # .env files EXCEPT .env.example, .env.sample, .env.template (those are templates)
    r"\.env($|\.(?!example|sample|template))",
    r"secret",
    r"credential",
    r"\.pem$",
    r"\.key$",
    r"password",
    r"token",
    r"api[_-]?key",
]

# Large file threshold (5MB)
LARGE_FILE_THRESHOLD = 5 * 1024 * 1024

# Patterns that suggest .gitignore additions
GITIGNORE_SUGGESTIONS = {
    r"node_modules/": "node_modules/ - npm dependencies should be in .gitignore",
    r"__pycache__/": "__pycache__/ - Python bytecode should be in .gitignore",
    r"\.pyc$": "*.pyc - Python bytecode should be in .gitignore",
    r"\.DS_Store$": ".DS_Store - macOS metadata should be in .gitignore",
    r"\.venv/": ".venv/ - Virtual environments should be in .gitignore",
    r"venv/": "venv/ - Virtual environments should be in .gitignore",
    r"\.idea/": ".idea/ - IDE settings should typically be in .gitignore",
    r"\.vscode/": ".vscode/ - VS Code settings should typically be in .gitignore",
    r"dist/": "dist/ - Build artifacts should typically be in .gitignore",
    r"build/": "build/ - Build artifacts should typically be in .gitignore",
}


def debug(msg: str):
    """Print debug message if DEBUG is enabled."""
    if DEBUG:
        print(f"[autocommit] {msg}", file=sys.stderr)


def get_config(cwd: str) -> dict:
    """Load configuration from files or environment."""
    config = {
        "enabled": True,
        "backend": "headless",
        "never_commit": list(SENSITIVE_PATTERNS),
        "log_decisions": True,
    }

    # Check config files (project takes precedence)
    for loc in [Path(cwd) / ".claude/autocommit.conf", Path.home() / ".claude/autocommit.conf"]:
        if loc.exists():
            try:
                for line in loc.read_text().strip().split("\n"):
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        key = key.strip().upper()
                        value = value.strip().strip('"').strip("'")
                        if key == "ENABLED":
                            config["enabled"] = value.lower() in ("true", "1", "yes")
                        elif key == "BACKEND":
                            config["backend"] = value.lower()
                        elif key == "NEVER_COMMIT":
                            config["never_commit"].extend(value.split(","))
                        elif key == "LOG_DECISIONS":
                            config["log_decisions"] = value.lower() in ("true", "1", "yes")
                debug(f"Config loaded from {loc}")
                break
            except Exception as e:
                debug(f"Failed to load config from {loc}: {e}")

    # Environment overrides
    if os.environ.get("AUTOCOMMIT_ENABLED"):
        config["enabled"] = os.environ["AUTOCOMMIT_ENABLED"].lower() in ("true", "1", "yes")
    if os.environ.get("AUTOCOMMIT_BACKEND"):
        config["backend"] = os.environ["AUTOCOMMIT_BACKEND"].lower()

    return config


def detect_integrations(cwd: str) -> dict:
    """Detect available ecosystem integrations at runtime.

    This plugin works standalone but is enhanced by:
    - statusline: Human-readable agent names from registry.json
    - logging: Conversation context from JSONL logs

    Returns dict with availability status and paths for each integration.
    """
    integrations = {
        "statusline": {
            "available": False,
            "registry_path": None,
        },
        "logging": {
            "available": False,
            "log_dir": None,
        },
    }

    # Check for statusline plugin (instances registry)
    for loc in [Path(cwd) / ".claude/instances", Path.home() / ".claude/instances"]:
        registry = loc / "registry.json"
        if registry.exists():
            integrations["statusline"]["available"] = True
            integrations["statusline"]["registry_path"] = registry
            debug("✓ Statusline integration: agent names available")
            break
    else:
        debug("○ Statusline not found: using session ID for attribution")

    # Check for logging plugin (JSONL logs)
    for loc in [Path(cwd) / ".claude/logging", Path.home() / ".claude/logging"]:
        if loc.exists():
            # Check if there are actually log files
            jsonl_files = list(loc.rglob("*.jsonl"))
            if jsonl_files:
                integrations["logging"]["available"] = True
                integrations["logging"]["log_dir"] = loc
                debug("✓ Logging integration: conversation context available")
                break
    else:
        debug("○ Logging not found: decisions based on user prompt + diff only")

    return integrations


def get_git_status(cwd: str) -> tuple[list[dict], str]:
    """Get uncommitted changes with file info."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=10,
        )
        if result.returncode != 0:
            return [], ""

        files = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            status = line[:2].strip()
            filepath = line[3:].strip()

            # Get file size if it exists
            full_path = Path(cwd) / filepath
            size = 0
            if full_path.exists():
                try:
                    size = full_path.stat().st_size
                except:
                    pass

            files.append({
                "status": status,
                "path": filepath,
                "size": size,
                "size_human": format_size(size),
            })

        return files, result.stdout.strip()
    except Exception as e:
        debug(f"git status failed: {e}")
        return [], ""


def format_size(size: int) -> str:
    """Format file size in human-readable form."""
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f}KB"
    else:
        return f"{size / (1024 * 1024):.1f}MB"


def get_git_diff_stat(cwd: str) -> str:
    """Get diff statistics."""
    try:
        result = subprocess.run(
            ["git", "diff", "--stat", "HEAD"],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=30,
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except:
        return ""


def get_git_diff(cwd: str, max_chars: int = 4000) -> str:
    """Get actual diff content, truncated."""
    try:
        result = subprocess.run(
            ["git", "diff", "HEAD"],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=30,
        )
        diff = result.stdout.strip() if result.returncode == 0 else ""
        if len(diff) > max_chars:
            diff = diff[:max_chars] + "\n... [truncated]"
        return diff
    except:
        return ""


def get_agent_name(integrations: dict, session_id: str) -> str:
    """Get agent name, using statusline registry if available.

    Falls back to session ID prefix if statusline plugin not installed.
    """
    if integrations["statusline"]["available"]:
        registry_path = integrations["statusline"]["registry_path"]
        try:
            data = json.loads(registry_path.read_text())
            name = data.get(session_id, {}).get("name")
            if name:
                return name
        except Exception as e:
            debug(f"Failed to read statusline registry: {e}")

    # Fallback: use session ID prefix for traceability
    if session_id:
        return f"Session-{session_id[:8]}"
    return "Claude"


def get_recent_assistant_response(integrations: dict, session_id: str) -> str:
    """Get the most recent assistant response from logs if logging plugin available.

    Returns empty string if logging plugin not installed - Haiku will decide
    based on user prompt and diff alone (still functional, just less context).
    """
    if not integrations["logging"]["available"]:
        return ""

    log_dir = integrations["logging"]["log_dir"]

    # Find log file for this session
    short_id = session_id[:8]
    try:
        log_files = list(log_dir.rglob(f"*{short_id}*.jsonl"))
        if not log_files:
            debug(f"No log files found for session {short_id}")
            return ""

        log_file = sorted(log_files, key=lambda p: p.stat().st_mtime, reverse=True)[0]

        # Get most recent assistant response
        last_response = ""
        for line in log_file.read_text().strip().split("\n"):
            if not line:
                continue
            try:
                entry = json.loads(line)
                if entry.get("type") == "AssistantResponse":
                    response = entry.get("data", {}).get("response", "")
                    if response:
                        last_response = response
            except:
                continue

        return last_response
    except Exception as e:
        debug(f"Failed to read logs: {e}")
        return ""


def analyze_safety(files: list[dict], config: dict) -> dict:
    """Analyze files for safety concerns."""
    result = {
        "sensitive": [],
        "large": [],
        "gitignore_suggestions": [],
        "safe_to_commit": [],
    }

    never_patterns = [re.compile(p, re.IGNORECASE) for p in config["never_commit"]]
    gitignore_patterns = [(re.compile(p), msg) for p, msg in GITIGNORE_SUGGESTIONS.items()]

    for f in files:
        path = f["path"]

        # Check for sensitive files
        is_sensitive = any(p.search(path) for p in never_patterns)
        if is_sensitive:
            result["sensitive"].append(path)
            continue

        # Check for large files
        if f["size"] > LARGE_FILE_THRESHOLD:
            result["large"].append(f"{path} ({f['size_human']})")
            continue

        # Check for gitignore suggestions
        for pattern, msg in gitignore_patterns:
            if pattern.search(path):
                if msg not in result["gitignore_suggestions"]:
                    result["gitignore_suggestions"].append(msg)

        result["safe_to_commit"].append(path)

    return result


def infer_scope(files: list[dict]) -> str:
    """Infer the most likely scope from changed files."""
    paths = [f["path"] for f in files]

    # Check for plugin patterns
    for p in paths:
        if p.startswith("plugins/"):
            parts = p.split("/")
            if len(parts) >= 2:
                return f"plugin:{parts[1]}"

    # Check for journal
    if any(".claude/journal/" in p for p in paths):
        return "journal"

    # Check for planning
    if any(".claude/planning/" in p for p in paths):
        return "planning"

    # Check for agents
    if any(".claude/agents/" in p for p in paths):
        return "agent"

    # Check for system files
    if any(p.startswith(".claude/") for p in paths):
        return "system"

    # Check for config
    if any(p in [".gitignore", "package.json", "tsconfig.json"] for p in paths):
        return "config"

    return "update"


def build_haiku_prompt(
    user_prompt: str,
    assistant_response: str,
    files: list[dict],
    diff_stat: str,
    diff_content: str,
    safety: dict,
    agent_name: str,
    session_id: str,
) -> str:
    """Build a strict classifier prompt for Haiku.

    Key design principles:
    1. Classifier framing FIRST - not an assistant
    2. Output format before context
    3. Few-shot examples
    4. Minimal context to reduce confusion
    """

    # Minimal file list (max 10 files shown)
    file_count = len(files)
    file_preview = "\n".join(f"  {f['status']} {f['path']}" for f in files[:10])
    if file_count > 10:
        file_preview += f"\n  ... +{file_count - 10} more"

    # Truncate user prompt aggressively
    user_short = user_prompt[:400] if len(user_prompt) > 400 else user_prompt

    # Infer scope for the example
    scope = infer_scope(files)

    # Safety checks
    if safety["sensitive"]:
        return f"""CLASSIFIER: Decide COMMIT or SKIP.

SENSITIVE FILES DETECTED - MUST SKIP:
{chr(10).join(safety["sensitive"])}

Output exactly:
SKIP: Sensitive files detected ({', '.join(safety["sensitive"][:3])})"""

    return f"""CLASSIFIER FUNCTION - NOT AN ASSISTANT

You are a commit decision classifier. You output EXACTLY one of two formats. Nothing else.
Do NOT explain. Do NOT use tools. Do NOT ask questions. Just output the format.

═══════════════════════════════════════════════════════════════════════════════
OUTPUT FORMAT (copy exactly)
═══════════════════════════════════════════════════════════════════════════════

IF COMMIT:
COMMIT
[scope] action: summary under 50 chars

Brief description of what changed and why.

---
Agent: {agent_name}
🤖 Generated with Claude Code
Co-Authored-By: {agent_name} <agent@claude-ecosystem>

IF SKIP:
SKIP: reason in under 15 words

═══════════════════════════════════════════════════════════════════════════════
EXAMPLES (follow these exactly)
═══════════════════════════════════════════════════════════════════════════════

User: "looks good!"
Files: 3 changed
COMMIT
[auth] add: email validation

Added format validation for email inputs on login form.

---
Agent: Phoenix
🤖 Generated with Claude Code
Co-Authored-By: Phoenix <agent@claude-ecosystem>

---

User: "there's still an error"
Files: 2 changed
SKIP: User reports error, work incomplete

---

User: "perfect, what should we work on next?"
Files: 5 changed
COMMIT
[ui] update: button hover states

Improved interactive feedback on primary action buttons.

---
Agent: Phoenix
🤖 Generated with Claude Code
Co-Authored-By: Phoenix <agent@claude-ecosystem>

---

User: "can you also add dark mode support?"
Files: 1 changed
SKIP: User requesting additional changes

---

User: "yes"
Files: 4 changed
COMMIT
[feature] create: settings panel

New settings panel with user preferences.

---
Agent: Phoenix
🤖 Generated with Claude Code
Co-Authored-By: Phoenix <agent@claude-ecosystem>

═══════════════════════════════════════════════════════════════════════════════
DECISION RULES
═══════════════════════════════════════════════════════════════════════════════

COMMIT when user message contains:
- Approval: good, nice, perfect, works, great, yes, done, ship, approved
- Moving on: next, now let's, what's next, continue, also
- New topic: asking about something unrelated to the diff

SKIP when user message contains:
- Problems: error, bug, wrong, broken, failed, not working, issue
- Requests: fix, change, try again, redo, actually, instead, can you also
- Continuing: follow-up questions about same topic, clarifications

═══════════════════════════════════════════════════════════════════════════════
CURRENT INPUT
═══════════════════════════════════════════════════════════════════════════════

User message:
{user_short}

Changed files ({file_count}):
{file_preview}

Suggested scope: [{scope}]
Agent: {agent_name}

═══════════════════════════════════════════════════════════════════════════════

Output COMMIT or SKIP now. Exact format only. No explanation."""


def call_haiku_headless(prompt: str) -> str:
    """Call headless Claude Haiku as a single-turn classifier."""
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
                "--max-turns",
                "1",  # Single turn only - no tool use, no follow-ups
                "--tools",
                "",
                "--setting-sources",
                "",  # Disable all settings = no hooks, no plugins (prevents recursion!)
            ],
            input="",  # Critical: must provide empty stdin or it hangs
            capture_output=True,
            text=True,
            timeout=60,
            env=env,
        )

        if result.returncode != 0:
            debug(f"Headless error: {result.stderr}")
            return ""

        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        debug("Headless timeout (60s)")
        return ""
    except Exception as e:
        debug(f"Headless error: {e}")
        return ""


def parse_haiku_response(response: str) -> dict:
    """Parse Haiku's response into structured data."""
    result = {
        "decision": None,
        "message": "",
        "reason": "",
        "warnings": [],
        "gitignore_suggestions": [],
    }

    lines = response.strip().split("\n")
    if not lines:
        return result

    first_line = lines[0].strip()

    if first_line == "COMMIT":
        result["decision"] = "COMMIT"
        # Everything after "COMMIT" line is the commit message
        message_lines = []
        for line in lines[1:]:
            if line.startswith("GITIGNORE_SUGGEST:"):
                result["gitignore_suggestions"].append(line[18:].strip())
            elif line.startswith("WARNING:"):
                result["warnings"].append(line[8:].strip())
            else:
                message_lines.append(line)
        result["message"] = "\n".join(message_lines).strip()

    elif first_line.startswith("SKIP:"):
        result["decision"] = "SKIP"
        result["reason"] = first_line[5:].strip()
        # Check for additional warnings/suggestions
        for line in lines[1:]:
            if line.startswith("GITIGNORE_SUGGEST:"):
                result["gitignore_suggestions"].append(line[18:].strip())
            elif line.startswith("WARNING:"):
                result["warnings"].append(line[8:].strip())

    else:
        # Fallback: try to detect COMMIT or SKIP in response
        if "COMMIT" in response[:50]:
            result["decision"] = "COMMIT"
            result["message"] = response
        elif "SKIP" in response[:50]:
            result["decision"] = "SKIP"
            result["reason"] = response

    return result


def execute_commit(cwd: str, files_to_stage: list[str], message: str) -> tuple[bool, str]:
    """Stage files and execute git commit."""
    try:
        # Stage files
        for filepath in files_to_stage:
            result = subprocess.run(
                ["git", "add", filepath],
                capture_output=True,
                text=True,
                cwd=cwd,
                timeout=10,
            )
            if result.returncode != 0:
                debug(f"Failed to stage {filepath}: {result.stderr}")

        # Commit
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=30,
        )

        if result.returncode == 0:
            # Extract commit hash
            hash_result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                cwd=cwd,
            )
            commit_hash = hash_result.stdout.strip() if hash_result.returncode == 0 else "unknown"
            return True, commit_hash
        else:
            return False, result.stderr.strip()

    except Exception as e:
        return False, str(e)


def log_decision(cwd: str, decision: str, details: str, config: dict):
    """Log decision to autocommit.log."""
    if not config.get("log_decisions", True):
        return

    log_dir = Path(cwd) / ".claude"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "autocommit.log"

    timestamp = datetime.now().isoformat()
    entry = f"[{timestamp}] {decision} - {details}\n"

    try:
        with open(log_file, "a") as f:
            f.write(entry)
    except Exception as e:
        debug(f"Failed to write log: {e}")


def main():
    debug("Starting autocommit hook")

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

    debug(f"Session: {session_id[:8] if session_id else 'none'}, CWD: {cwd}")

    if not session_id:
        debug("No session_id")
        return

    # Load configuration
    config = get_config(cwd)

    if not config["enabled"]:
        debug("Autocommit disabled in config")
        return

    # Check for uncommitted changes
    files, status_output = get_git_status(cwd)

    if not files:
        debug("No uncommitted changes")
        return

    debug(f"Found {len(files)} changed files")

    # Analyze safety
    safety = analyze_safety(files, config)

    # If ALL files are sensitive, skip entirely
    if safety["sensitive"] and not safety["safe_to_commit"]:
        log_decision(cwd, "SKIP", f"All changed files are sensitive: {', '.join(safety['sensitive'])}", config)
        debug("All files sensitive, skipping")
        return

    # Detect available ecosystem integrations
    integrations = detect_integrations(cwd)

    # Get context (using integrations if available)
    agent_name = get_agent_name(integrations, session_id)
    assistant_response = get_recent_assistant_response(integrations, session_id)
    diff_stat = get_git_diff_stat(cwd)
    diff_content = get_git_diff(cwd)

    debug(f"Agent: {agent_name}, Response length: {len(assistant_response)}")

    # Build prompt for Haiku
    prompt = build_haiku_prompt(
        user_prompt=user_prompt,
        assistant_response=assistant_response,
        files=files,
        diff_stat=diff_stat,
        diff_content=diff_content,
        safety=safety,
        agent_name=agent_name,
        session_id=session_id,
    )

    # Call Haiku
    response = call_haiku_headless(prompt)

    if not response:
        debug("No response from Haiku")
        log_decision(cwd, "ERROR", "No response from Haiku", config)
        return

    # Parse response
    parsed = parse_haiku_response(response)
    debug(f"Decision: {parsed['decision']}")

    # Log warnings and suggestions
    for warning in parsed["warnings"]:
        log_decision(cwd, "WARNING", warning, config)
    for suggestion in parsed["gitignore_suggestions"]:
        log_decision(cwd, "GITIGNORE_SUGGEST", suggestion, config)

    # Execute decision
    if parsed["decision"] == "COMMIT":
        if not parsed["message"]:
            debug("COMMIT decision but no message")
            log_decision(cwd, "ERROR", "COMMIT decision but no message generated", config)
            return

        # Only commit safe files
        files_to_commit = safety["safe_to_commit"]
        if not files_to_commit:
            debug("No safe files to commit")
            log_decision(cwd, "SKIP", "No safe files to commit after filtering", config)
            return

        success, result = execute_commit(cwd, files_to_commit, parsed["message"])

        if success:
            # Extract first line of commit message for log
            first_line = parsed["message"].split("\n")[0]
            log_decision(cwd, "COMMIT", f"{result} - {first_line}", config)
            debug(f"Committed: {result}")
        else:
            log_decision(cwd, "COMMIT_FAILED", result, config)
            debug(f"Commit failed: {result}")

    elif parsed["decision"] == "SKIP":
        log_decision(cwd, "SKIP", parsed["reason"], config)
        debug(f"Skipped: {parsed['reason']}")

    else:
        debug(f"Unknown decision: {parsed['decision']}")
        log_decision(cwd, "ERROR", f"Unknown decision from Haiku: {response[:100]}", config)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        if DEBUG:
            print(f"[autocommit] Fatal error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
        # Fail silently in production - autocommit is enhancement, not critical
        pass
