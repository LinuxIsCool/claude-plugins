---
id: msg_Fts1ieNDwLdiua3ArE4FpQNts7YxPTWK
kind: 103
account_id: claude
created_at: 1765667717015
imported_at: 1766005510217
author_name: Claude
thread_id: cc_298311d7
platform: claude-code
session_id: 298311d7-dc9e-4d73-bbb3-323eaba7d29e
tags: [["event_type","AssistantResponse"]]
---

## Done

Created `/awareness:mentor` command that spawns the agent.

### The Command

**File**: `plugins/awareness/commands/mentor.md`

**Usage**:
```
/awareness:mentor how do I create a plugin
/awareness:mentor          # (will ask what you want to learn)
```

**What it does**: When invoked, the command expands to a prompt that instructs Claude to spawn the `awareness:mentor` subagent via the Task tool with the learning goal passed through.

### Full Flow

```
User types:  /awareness:mentor hooks
                    ↓
Command expands:  "Spawn awareness:mentor with prompt about hooks"
                    ↓
Claude uses:  Task tool → subagent_type: "awareness:mentor"
                    ↓
Mentor agent:  Guides learning session about hooks
```

### Files Created/Modified

| File | Action |
|------|--------|
| `plugins/awareness/agents/mentor.md` | Created - agent definition |
| `plugins/awareness/commands/mentor.md` | Created - slash command |
| `plugins/awareness/.claude-plugin/plugin.json` | Updated - added `agents` field |
| `.claude/agents/awareness:mentor.md` | Generated - by aggregation script |
| `scripts/aggregate-plugin-agents.sh` | Created - build script |
| `CLAUDE.md` | Updated - documented pattern |

### To Activate

Restart Claude Code. Then:
- `/awareness:mentor` will be available as a slash command
- `awareness:mentor` will be available as a Task tool subagent_type
