---
id: 2025-12-16-1732
title: "Headless Debugging Victory: Three Bugs, One Working System"
type: atomic
created: 2025-12-16T17:32:51-08:00
author: Phoenix
description: "Debugging journey from 'it doesn't work' to working headless auto-summary with three distinct bug fixes"
tags: [debugging, hooks, stdin, uv-run, recursion, headless-claude, victory]
parent_daily: [[2025-12-16]]
related:
  - [[17-03-engineering-tradeoffs-headless-vs-api]]
---

# Headless Debugging Victory: Three Bugs, One Working System

Following the [[17-03-engineering-tradeoffs-headless-vs-api|earlier engineering analysis]], I switched the auto-summary system to use headless Claude. It immediately broke. What followed was a debugging journey that uncovered three distinct bugs, each masquerading as the others.

## The Symptom

User: "It didn't work."

New Claude sessions showed "Awaiting instructions." in their summary, even after exchanging messages. The system that worked perfectly with the API backend was completely non-functional with headless.

## Bug #1: Recursive Hook Triggering

**Discovery**: Log files showed sessions like `d5e3b80a` with suspicious content—their "user prompt" was our summary generation prompt. The headless Claude subprocess was triggering the same hooks as the parent session.

**Evidence**:
```json
{"type": "UserPromptSubmit", "prompt": "You are Phoenix. Based on this recent conversation, write a 5-10 word first-person summary..."}
```

This wasn't a user session—it was our headless subprocess getting logged!

**Fix**: Added `--setting-sources ""` to the headless Claude call:
```python
subprocess.run([
    "claude", "-p", prompt,
    "--setting-sources", "",  # Disables ALL settings = no hooks, no plugins
    ...
])
```

This completely isolates the subprocess from the plugin ecosystem.

## Bug #2: uv run Swallows stdin

**Discovery**: After fixing recursion, the hook still didn't work. Manual testing revealed `uv run` doesn't pass stdin through to scripts.

**Evidence**:
```bash
echo '{"test": "data"}' | python3 -c "import sys; print(sys.stdin.read())"
# Output: {"test": "data"}

echo '{"test": "data"}' | uv run python3 -c "import sys; print(sys.stdin.read())"
# Output: (empty)
```

This is a known limitation of `uv run`—it's designed for running scripts, not processing piped data.

**Fix**: Created `auto-summary-wrapper.sh` that captures stdin first:
```bash
INPUT=$(cat)
export HOOK_INPUT="$INPUT"
uv run "${SCRIPT_DIR}/auto-summary.py"
```

And modified the Python script to check both stdin and the environment variable.

## Bug #3: Plugin Cache Staleness

**Discovery**: Even after code fixes, new sessions weren't seeing the changes. The plugin cache at `~/.claude/plugins/cache/` was serving old versions.

**Fix**: `rm -rf ~/.claude/plugins/cache/linuxiscool-claude-plugins/statusline/`

New sessions now load directly from the source plugin directory.

## The Debugging Process

What made this hard was **bug masking**:
- Bug #1 created fake sessions that polluted my analysis
- Bug #2 only manifested in production (hooks), not in manual testing with `python3`
- Bug #3 made fixes appear ineffective

The breakthrough came from **layered verification**:
1. Test the script manually → Works? Then hook execution is the problem
2. Check if hooks run at all → Count file updated? Then stdin is the problem
3. Check log contents → Recursive prompts? Then subprocess isolation is the problem

## Key Insight

> **Production environments have different stdin behavior than manual testing.**

When I ran `echo '...' | python3 script.py`, it worked. When Claude Code ran the hook, it didn't. The difference was `uv run` in the hook command.

This is why "works on my machine" is a meme. The execution context matters as much as the code.

## Technical Artifacts

- `auto-summary-wrapper.sh` - stdin capture wrapper
- `--setting-sources ""` - subprocess isolation flag
- `HOOK_INPUT` environment variable - stdin bypass mechanism

## The Victory

```
User: "OK it worked!"
```

Three bugs. Three fixes. One working headless auto-summary system that:
- Uses Max subscription (free)
- Doesn't create recursive sessions
- Properly receives hook data
- Updates summaries in new instances

Sometimes debugging is archaeology—you dig through layers of symptoms to find the actual bugs buried underneath.

---

*Parent: [[2025-12-16]] → [[2025-12]] → [[2025]]*
