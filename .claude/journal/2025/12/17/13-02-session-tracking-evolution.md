---
id: 2025-12-17-1302
title: "Session Tracking Evolution"
type: atomic
created: 2025-12-17T13:02:06
author: claude-opus-4
description: "Evolved statusline session tracking from emojis to clean ID:A#N format"
tags: [statusline, logging, session-tracking, debugging, feature-development]
parent_daily: [[2025-12-17]]
related: []
---

# Session Tracking Evolution

Today's session began with a bug investigation and evolved into a feature redesign. The user noticed that long sessions sometimes showed prompt numbers like "1", suspecting the counter reset during context compaction.

## The Investigation

Initial research revealed key insights about Claude Code's session lifecycle:

1. **Session ID persists across compaction** - The `source` field in SessionStart distinguishes:
   - `startup` - Truly new session
   - `compact` - Context compaction (same session continues)
   - `resume` - Session resumed
   - `clear` - Context cleared

2. **Bug found in `user-prompt-submit.sh`** - Used relative path `.claude/instances` instead of absolute `$CWD/.claude/instances`, causing counter lookup failures when working directory changed.

## The Evolution

The session tracking format went through several iterations:

| Version | Format | Rationale |
|---------|--------|-----------|
| Original | `#15` | Just prompt count |
| v1 | `P:A#N` with emojis | Project/agent/prompt tracking |
| v2 | `6:0#15` | Numbers only, colon separator |
| Final | `abc12:0#15` | Short ID + agent session + prompt |

The final format `<short_id>:<agent>#<prompt>`:
- **short_id**: 5-char UUID prefix (unique session identifier)
- **agent**: Context reset counter (0=fresh, increments on compact/clear)
- **prompt**: Prompt count (persists across compaction)

## Implementation Details

Files modified:
- `plugins/logging/hooks/log_event.py` - Agent session counter with state file
- `plugins/statusline/tools/statusline.sh` - Display format
- `plugins/statusline/hooks/user-prompt-submit.sh` - Fixed relative path bug

State persisted in `.claude/logging/session-state.json`:
```json
{"agent_session": 0}
```

## Insights

- **Simplicity won**: The project-level counter added complexity without clear value
- **Agent session IS valuable**: Knowing how many compactions occurred helps debug context issues
- **Relative paths are subtle bugs**: They work in most cases, fail in edge cases
- **Iterative refinement**: Four format iterations in one session shows the value of rapid prototyping

## Context

User was building observability into the Claude Code plugin ecosystem. Session tracking feeds into logging, journaling, and statusline plugins - creating a unified view of Claude's operational state.

---

*Parent: [[2025-12-17]]*
