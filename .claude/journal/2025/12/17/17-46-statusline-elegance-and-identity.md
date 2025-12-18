---
id: 2025-12-17-1746
title: "Statusline Elegance and Identity"
type: atomic
created: 2025-12-17T17:46:38
author: claude-opus-4
description: "Redesigned statusline with JSONL-derived state and Claude process numbers"
tags: [statusline, logging, architecture, event-sourcing, identity]
parent_daily: [[2025-12-17]]
related: [[2025-12-17-1302-session-tracking-evolution]]
---

# Statusline Elegance and Identity

Today's session was a masterclass in architectural refinement. What started as debugging a broken feature evolved into a complete rethinking of how state should be managed.

## The Elegant Redesign

The original agent session tracking used a state file (`session-state.json`) that the logging plugin wrote and the statusline plugin read. This created:
- Cross-plugin coordination complexity
- Cache invalidation issues (edits didn't take effect)
- A separate source of truth from the actual logs

**The insight**: The JSONL log file already contains all SessionStart events with their `source` field ("startup", "compact", "clear", "resume"). Instead of maintaining state, just count what's in the log.

```python
# Before: 45 lines of state file management
def get_agent_session(cwd, source):
    state = load_session_state(cwd)
    if source == "startup":
        state["agent_session"] = 0
    elif source in ("compact", "clear"):
        state["agent_session"] += 1
    save_session_state(cwd, state)
    return state["agent_session"]

# After: 28 lines of derivation
def get_agent_session_from_jsonl(jsonl_path, source):
    count = content.count('"source": "compact"') + content.count('"source": "clear"')
    if source in ("compact", "clear"):
        count += 1  # Current event not logged yet
    return count
```

This is **event sourcing** in miniature: the log is the source of truth, derived values are computed on demand.

## A Subtle Bug: grep -c Exit Codes

Discovered a bash gotcha that caused the statusline to show `0\n0` (two lines):

```bash
# BUG: grep -c outputs "0" but exits with code 1 for no matches
# The || echo "0" then ALSO outputs "0"
AGENT_SESSION=$(grep -cE 'pattern' file || echo "0")
# Result: "0\n0"

# FIX: Capture first, check if empty
AGENT_SESSION=$(grep -cE 'pattern' file 2>/dev/null)
[ -z "$AGENT_SESSION" ] && AGENT_SESSION="0"
```

This is unusual behavior - most commands exit 0 on success regardless of output. grep -c is a special case.

## Claude Process Numbers

Added a new identity feature: **spawn order numbering** (C1, C2, C3...).

Format evolution:
```
abc12:0#5  → redundant (abc12 already in [Name:abc12])
C39:0#5    → meaningful (39th Claude spawned on this machine)
```

Implementation:
- Counter file: `.claude/instances/process_counter.txt`
- On new session: read → increment → write → store in registry
- Monotonic: never resets, always increases
- Total ordering of all Claude instances across time

## Visual Polish

Made key elements bold for scannability:
- Agent name (what am I?)
- Last directory (where am I?)
- Branch name (what state is the code in?)
- Summary line (what was I doing?)

## Architecture Principles Reinforced

1. **Single source of truth**: Don't maintain state if you can derive it from existing data
2. **Event sourcing works**: Append-only logs are inherently robust
3. **Self-healing systems**: Derived state can't get corrupted - just re-derive
4. **Monotonic counters**: Simple, reliable, information-rich

The statusline plugin went from v0.3.0 to v0.4.0 today. Created a proper CHANGELOG to track the evolution.

---

*Parent: [[2025-12-17]] -> [[2025-12]] -> [[2025]]*
