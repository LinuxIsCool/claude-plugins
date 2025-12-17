---
id: msg_7AmrHv72Hw9vD1mmakgf7nwY4HRvC4Gd
kind: 103
account_id: claude
created_at: 1765903514825
imported_at: 1766005511570
author_name: Claude
thread_id: cc_298311d7
platform: claude-code
session_id: 298311d7-dc9e-4d73-bbb3-323eaba7d29e
tags: [["event_type","AssistantResponse"]]
---

The deprecated agent was **awareness:mentor** at the project level.

**What happened**: There were two identical `mentor` agents:
1. `.claude/agents/awareness:mentor.md` (project-level)
2. `plugins/awareness/agents/mentor.md` (plugin-level)

The project-level one was an exact duplicate that had been created during parallel session work. The plugin version is the authoritative one since mentor is part of the awareness plugin's persona.

**Resolution**: The duplicate was archived to `.claude/archive/agents/awareness-mentor-deprecated.md` with a deprecation header:

```yaml
---
name: mentor
deprecated: 2025-12-15
reason: Exact duplicate of plugins/awareness/agents/mentor.md
replacement: awareness:mentor (plugin version)
original-location: .claude/agents/awareness:mentor.md
---
```

The plugin version (`plugins/awareness/agents/mentor.md`) remains active and is the one synced to AgentNet as `awareness:mentor`.
