---
id: msg_BrLe16Gv7Vf4F7nZD2P7jMKtXbQYo3kR
kind: 103
account_id: claude
created_at: 1765902496923
imported_at: 1766005511522
author_name: Claude
thread_id: cc_fadb45f5
platform: claude-code
session_id: fadb45f5-d424-4fb5-848d-b6e1a9503da8
tags: [["event_type","AssistantResponse"]]
---

The git protocols are documented in two places:

## Primary Documentation

**`.claude/conventions/coordination.md`** (514 lines)
- Complete coordination conventions
- Commit message format and scopes
- Namespace ownership rules
- Observation patterns
- Conflict prevention
- Information flow patterns
- Bootstrap protocol
- Proactive commit discipline
- Agent ID traceability
- Commit plan template

## Summary in CLAUDE.md

**`CLAUDE.md`** (lines 7-19)
```markdown
# Coordination

**Git is the inter-agent coordination layer.** Agents coordinate 
through observable file changes, not complex protocols.

- **Write** to your designated namespace
- **Read** from anywhere
- **Commit** with structured messages: `[scope] action: description`
- **Include agent ID** when known: `[agent:type/hexid] action: description`
- **Observe** git log for ecosystem activity

**Agent ID traceability**: After spawning a subagent, include its 
hex ID (from Task output) in commits to enable direct transcript 
lookup. Use `.claude/tools/correlate_commits.py` for retroactive 
correlation.

See `.claude/conventions/coordination.md` for full patterns.
```

## Supporting Tools

**`.claude/tools/correlate_commits.py`**
- Retroactively links commits to agent executions
- Matches by timestamp proximity (120-second window)
- Referenced in documentation but rarely used
