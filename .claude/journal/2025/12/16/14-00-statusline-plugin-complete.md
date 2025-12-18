---
id: 2025-12-16-1400
title: "Statusline Plugin: Instance Identity for Multi-Claude Coordination"
type: atomic
created: 2025-12-16T08:10:00
references_date: 2025-12-15
author: claude-opus-4-5
session_id: continued-from-117ec3ac
description: "Built complete statusline plugin with auto-registration, self-naming, and hook-based session tracking"
tags: [statusline, plugin, identity, multi-instance, hooks, self-naming, registry, coordination]
parent_daily: [[2025-12-16]]
related:
  - [[13-30-exploration-deep-dive]]
  - [[2025-12-15]]
---

# Statusline Plugin: Instance Identity for Multi-Claude Coordination

Completed a full plugin for tracking Claude instance identity across sessions, enabling multi-instance coordination and historical traceability.

## The Problem

When multiple Claude instances run in parallel:
- Which Claude made this commit?
- What was this session working on?
- How do I find context from a previous instance?
- How do instances avoid duplicate work?

Session IDs exist but are opaque UUIDs. Needed: human-readable names, persistent tracking, and visual identity.

## The Solution

Built `plugins/statusline/` with four integrated components:

### 1. SessionStart Hook (`hooks/session-start.sh`)

Fires automatically when Claude Code starts. Receives JSON via stdin:
```json
{
  "session_id": "abc123...",
  "cwd": "/path/to/project",
  "source": "startup|resume|clear|compact"
}
```

The hook:
- Registers session in `~/.claude/instances/registry.json`
- Exports `$SESSION_ID` via `CLAUDE_ENV_FILE` for Claude to use
- Injects context prompting self-naming:
  ```
  [statusline] Session abc12 registered. Statusline shows: [Opus:abc12]
  When you understand the user's task, name yourself:
    python3 plugins/statusline/tools/registry.py register "$SESSION_ID" "Name" --task "description"
  ```

### 2. Statusline Script (`tools/statusline.sh`)

Renders the status display. Receives JSON with model, context, cost. Shows:

| State | Display |
|-------|---------|
| Default | `[Opus:abc12] project | ctx:42% | $0.45` |
| Custom name | `[Explorer:abc12] project | ctx:42% | $0.45` |

Key features:
- Extracts model name (Opus/Sonnet/Haiku) from `model.display_name`
- Uses new `current_usage` field for accurate context percentage
- Falls back to manual calculation for older Claude Code versions
- Looks up custom name from registry, shows model if none set

### 3. Instance Registry (`tools/registry.py`)

Python module for instance tracking:

```python
from statusline.tools.registry import InstanceRegistry

registry = InstanceRegistry()
registry.register(session_id, "Explorer", task="Environmental exploration")
registry.list_active()  # [(session_id, data), ...]
registry.find_by_name("Explorer")  # (session_id, data)
registry.mark_inactive(session_id)
registry.cleanup_stale(hours=24)
```

Registry format:
```json
{
  "abc123...": {
    "name": "Explorer",
    "task": "Environmental exploration",
    "model": "claude-opus-4-5",
    "cwd": "/path/to/project",
    "created": "2025-12-16T14:00:00Z",
    "last_seen": "2025-12-16T15:30:00Z",
    "status": "active"
  }
}
```

### 4. Self-Naming Skill (`skills/statusline-master/`)

Guides Claude on when and how to name itself:

**DO name yourself when:**
- User states a clear task
- Beginning substantive work
- Task changes significantly

**DON'T name yourself when:**
- Just answering a quick question
- Task is still unclear
- Session will be very short

Naming convention by task type:
| Task | Names |
|------|-------|
| Exploration | Explorer, Scout, Cartographer |
| Debugging | Debugger, Detective, Fixer |
| Documentation | Scribe, Writer, Documenter |
| Architecture | Architect, Designer, Builder |

## Architecture Decisions

### Data Storage Pattern
- **Plugin code**: `plugins/statusline/`
- **Runtime data**: `~/.claude/instances/`

This follows the ecosystem pattern where plugins don't store runtime data in their own directories.

### Hook-Based Auto-Registration
SessionStart hook was chosen because:
1. Fires reliably at session start
2. Receives `session_id` via JSON stdin
3. Can export env vars via `CLAUDE_ENV_FILE`
4. Can inject context into Claude's awareness

Alternative considered: Having Claude manually register. Rejected because it requires Claude to "remember" to do it.

### Statusline Format Evolution

Started with: `[Explorer:a1b2c] dir | ctx:45% | $0.12`

Problem: Without custom name, showed `[Claude-a1b2c:a1b2c]` (redundant).

Fixed to: `[Opus:a1b2c]` (model name when no custom name).

User feedback drove this - they saw `[Opus-dbaaa:dbaaa]` and asked "what's with the dbaaa?"

### Context Percentage
Initially calculated manually from `total_input_tokens + total_output_tokens`.

Updated to use new `current_usage` field from Claude Code changelog - more accurate as it accounts for system prompts and tool definitions.

## Files Created

```
plugins/statusline/
├── .claude-plugin/plugin.json
├── README.md
├── commands/
│   ├── install.md          # /statusline:install
│   └── instances.md        # /statusline:instances
├── hooks/
│   └── session-start.sh    # Auto-registration hook
├── skills/
│   └── statusline-master/
│       ├── SKILL.md
│       └── subskills/
│           ├── self-namer.md
│           └── instance-tracker.md
└── tools/
    ├── registry.py         # Python registry module
    └── statusline.sh       # Display script
```

## Installation Flow

```
/statusline:install
    │
    ├── Symlink ~/.claude/statusline.sh → plugin script
    ├── Symlink ~/.claude/hooks/session-start.sh → hook script
    ├── Configure settings.json with statusLine and hooks
    └── Create ~/.claude/instances/ directory
```

After restart:
1. SessionStart hook fires
2. Session registered in registry
3. `$SESSION_ID` available to Claude
4. Statusline shows `[Opus:xxxxx]`
5. Claude can self-name when task is clear

## Integration Points

### Git Commits
```
feat: Add new feature

Session-Id: abc123
Instance-Name: Explorer
```

### Journal Entries
```yaml
session_id: abc123
instance_name: Explorer
author: claude-opus-4-5
```

### Logs
Already named with session ID by Claude Code.

## What's Next

1. **Multi-instance coordination** - Message passing between instances
2. **Historical queries** - "What did Explorer work on last week?"
3. **Automatic task detection** - Name suggestion based on conversation analysis
4. **Session handoff** - Structured transfer of context between instances

## Key Insight

> **Identity enables accountability. Accountability enables coordination.**

Without identity, multiple Claude instances are indistinguishable ghosts. With identity, each becomes a traceable agent with history, purpose, and relationships to other agents.

The statusline is just the visible surface. The registry is the memory. The hooks are the nervous system. Together they give Claude instances persistent identity.

---

*Plugin version: 0.1.0 | Registered as 15th plugin in ecosystem*

---

*Parent: [[2025-12-16]]*
