---
id: msg_HzZ83WpHAvLfJUKjf4ZL4UBshh3VpT8Q
kind: 103
account_id: claude
created_at: 1765561147093
imported_at: 1766005509099
author_name: Claude
thread_id: cc_f25ad4cb
platform: claude-code
session_id: f25ad4cb-9080-4661-ad54-5ea7c078599d
tags: [["event_type","AssistantResponse"]]
---

No, the plugin **does not bundle** the MCP server. It depends on the external `backlog.md` npm package:

```json
// package.json
"dependencies": {
  "backlog.md": "^1.27.0"
}
```

```json
// .mcp.json
"command": "npx",
"args": ["backlog.md", "mcp", "start"]
```

### How It Works

1. User installs the plugin
2. Plugin declares dependency on `backlog.md@^1.27.0`
3. MCP server runs via `npx backlog.md mcp start`
4. Plugin provides the Claude Code layer (CLAUDE.md, commands, skills)

### Trade-offs

**Pros:**
- Always gets latest backlog.md updates
- Smaller plugin size
- No code duplication

**Cons:**
- Requires npm/npx at runtime
- Network fetch on first use
- Version drift possible

This is a common pattern for plugins wrapping existing MCP servers. The alternative would be vendoring the backlog.md code directly into the plugin.
