---
id: msg_JAspL9pXQfQXpcxT1XbpMztDAzP6Xp39
kind: 103
account_id: claude
created_at: 1765505183190
imported_at: 1766005508920
author_name: Claude
thread_id: cc_42b02dc6
platform: claude-code
session_id: 42b02dc6-2ff1-46f3-a100-df68b705d414
tags: [["event_type","AssistantResponse"]]
---

**Root cause identified.** The awareness plugin's `plugin-studier` skill helped me understand the discovery mechanism.

## The Answer

**Only 2 plugins are registered in `.claude-plugin/marketplace.json`:**

```json
"plugins": [
  {"name": "brainstorm", "source": "./plugins/brainstorm/"},
  {"name": "logging", "source": "./plugins/logging/"}
]
```

**Missing from marketplace.json:**
- `awareness` - exists at `./plugins/awareness/` but not registered
- `Schedule.md` - exists at `./plugins/Schedule.md/` but not registered

## How Plugin Discovery Works

According to the awareness plugin's documentation:

1. Claude Code reads `marketplace.json` to find registered plugins
2. For each registered plugin, it reads the plugin's `.claude-plugin/plugin.json`
3. Discovers and loads skills, commands, hooks, and MCP servers from declared paths
4. **Plugins not in marketplace.json are invisible to the loader**

## The Fix

Add the missing plugins to `.claude-plugin/marketplace.json`:

```json
"plugins": [
  {"name": "brainstorm", "source": "./plugins/brainstorm/"},
  {"name": "logging", "source": "./plugins/logging/"},
  {"name": "awareness", "source": "./plugins/awareness/"},
  {"name": "schedule", "source": "./plugins/Schedule.md/"}
]
```

Would you like me to update the marketplace.json to register all 4 plugins?
