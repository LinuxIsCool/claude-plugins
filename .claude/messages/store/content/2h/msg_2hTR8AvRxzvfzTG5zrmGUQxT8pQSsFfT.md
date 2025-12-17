---
id: msg_2hTR8AvRxzvfzTG5zrmGUQxT8pQSsFfT
kind: 103
account_id: claude
created_at: 1765581991161
imported_at: 1766005509337
author_name: Claude
thread_id: cc_0a8bf3f1
platform: claude-code
session_id: 0a8bf3f1-1bed-40e7-8abd-689400f702b9
tags: [["event_type","AssistantResponse"]]
---

Based on my research, here's what's happening:

## Skill Truncation Mechanism

**The truncation is internal to Claude Code** - it's part of how the system prompt is assembled at session startup.

### How it works:
1. Claude Code loads all available skills from enabled plugins
2. Each skill's name + description consumes tokens in the system prompt
3. When a token budget is exceeded, the list is cut
4. You see: `<!-- Showing 45 of 84 skills due to token limits -->`

### Prioritization
The exact algorithm isn't documented, but appears to follow:
1. Plugin registration order in `marketplace.json`
2. Skills within each plugin (alphabetical or discovery order)

Looking at your marketplace.json order:
```
brainstorm → logging → awareness → schedule → agents → llms → backlog → journal
```

Yet displayed skills come from: logging, schedule, agents, llms - **skipping awareness, backlog, journal**. This suggests there may be additional prioritization beyond registration order.

### No User Configuration
There's **no documented setting** to control which skills appear in the truncated list. Options to reduce truncation:
- Disable unused plugins in `settings.json`
- Reduce total skill count
- Consolidate skills

### Key Insight
**Skills still work even when not displayed** - as we demonstrated with `awareness:docs-reader`. The truncation only affects the initial display, not functionality.

Would you like me to investigate the Claude Code source or plugin loader to find the exact truncation logic?
