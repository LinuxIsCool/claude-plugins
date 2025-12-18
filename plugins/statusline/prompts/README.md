# Statusline Prompts

This directory contains prompt templates for the statusline plugin's AI generation systems.
Each prompt uses Python `.format()` style variables: `{variable_name}`.

## Quick Start: Testing Prompts

```bash
# Preview filled prompt without API call
./tools/test-prompts.py name --preview --user-prompt "Fix the login bug"

# Test with mock response (no API call)
./tools/test-prompts.py summary --mock "Debugging auth flow"

# Test against real API
./tools/test-prompts.py name --user-prompt "Help me refactor the database layer"
```

---

## name.txt

**Purpose:** Generate creative 1-2 word session names on first prompt.

**Trigger:** First user prompt only (once per session).

**Output:** 1-2 words, capitalized (e.g., "Navigator", "Thread Hunter")

### Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{user_prompt}` | First user message (truncated to 500 chars) | "Help me fix the login bug in auth.py" |

### Quality Guidelines

Good names are:
- Evocative and memorable
- Hint at session purpose
- Feel like codenames or callsigns

---

## summary.txt

**Purpose:** Generate 5-10 word first-person summaries of current work.

**Trigger:** Every user prompt.

**Output:** 5-10 words, first person (e.g., "Fixing race condition in statusline hooks")

### Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{agent_name}` | Current session name | "Navigator" |
| `{prev_summaries}` | Last 3 summaries (newline-separated) | "Debugging auth flow\nRefactoring database" |
| `{context}` | Last 6 user/assistant messages | "User: Fix the bug\nAssistant: I found..." |

### Quality Guidelines

Good summaries are:
- Action-oriented ("Fixing X" not "Looking at X")
- Specific to current work
- Natural first-person voice

---

## description.txt

**Purpose:** Generate 2-5 word "lifetime arc" descriptions capturing WHO the agent is.

**Trigger:** Every user prompt.

**Output:** 2-5 words describing role/mission (e.g., "Plugin infrastructure architect")

### Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `{agent_name}` | Current session name | "Phoenix" |
| `{first_prompts}` | First 5 user prompts (origin anchor) | "User: Help me redesign..." |
| `{recent_prompts}` | Last 20 user prompts (trajectory) | "User: Now fix the tests..." |
| `{prev_descriptions}` | Last 10 descriptions (arc continuity) | "Database migration guide" |
| `{prev_summaries}` | Last 10 summaries (activity log) | "Running test suite..." |
| `{recent_response}` | Latest Claude response (500 chars) | "I've identified the issue..." |

### Quality Guidelines

Good descriptions:
- Capture the journey, not just current task
- Feel like a title or role
- Evolve slowly as work progresses

---

## Iteration Workflow

1. **Edit prompt** in this directory
2. **Preview** with `./tools/test-prompts.py <type> --preview`
3. **Test with mock** to verify parsing: `./tools/test-prompts.py <type> --mock "Expected output"`
4. **Test with API** using synthetic data or real session
5. **Observe in production** via debug mode (see below)

---

## Debug Mode

Enable debug output for any generation system with environment variables:

```bash
# Show full prompts and responses for specific generators
DEBUG_NAME=1 claude        # Name generation debug
DEBUG_SUMMARY=1 claude     # Summary generation debug
DEBUG_DESCRIPTION=1 claude # Description generation debug

# Combine multiple
DEBUG_NAME=1 DEBUG_SUMMARY=1 claude
```

When enabled, you'll see in stderr:
- Full prompt text with all variables filled
- Generation parameters (max_tokens, temperature)
- Backend selection (api/headless)
- Generated response

## File Locations

Prompts are loaded from (in order):
1. `plugins/statusline/prompts/{name}.txt` (this directory)
2. `plugins/statusline/hooks/{name}-prompt.txt` (legacy)
3. `~/.claude/{name}-prompt.txt` (user override)
4. Hardcoded default in hook script (fallback)
