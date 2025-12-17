---
id: msg_2TYeyfhNPP5tmr4Wy6rJNvaqBmy2t59P
kind: 103
account_id: claude
created_at: 1765667956739
imported_at: 1766005510250
author_name: Claude
thread_id: cc_298311d7
platform: claude-code
session_id: 298311d7-dc9e-4d73-bbb3-323eaba7d29e
tags: [["event_type","AssistantResponse"]]
---

## How Plugin Agents Work

### The Setup

```
plugins/awareness/
├── .claude-plugin/
│   └── plugin.json      ← Lists agents here
└── agents/
    └── mentor.md        ← Agent definition
```

**plugin.json**:
```json
{
  "agents": ["./agents/mentor.md"]
}
```

### What Happens

1. **Claude Code starts** → reads all installed plugins
2. **Finds `agents` field** → loads each `.md` file listed
3. **Namespaces it** → `mentor.md` in `awareness` plugin becomes `awareness:mentor`
4. **Adds to Task tool** → now available as a subagent_type

### The Result

You can now spawn the agent:

```
Task tool → subagent_type: "awareness:mentor"
```

Or via the command:

```
/awareness:mentor how do hooks work
```

### The Agent File

The `.md` file has two parts:

```markdown
---
name: mentor
description: Shows up in Task tool description
tools: Read, Glob, Grep, Skill
model: sonnet
---

# The actual prompt/identity
This content becomes the agent's system context...
```

### Summary

| What | Where | Becomes |
|------|-------|---------|
| Project agent | `.claude/agents/foo.md` | `foo` |
| Plugin agent | `plugins/bar/agents/baz.md` | `bar:baz` |

That's it. Plugins can now ship their own agents with automatic namespacing.
