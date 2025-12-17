---
id: msg_259jzBNXBCdUgZ1XymfohUjezumSjxot
kind: 103
account_id: claude
created_at: 1765561275659
imported_at: 1766005509110
author_name: Claude
thread_id: cc_f25ad4cb
platform: claude-code
session_id: f25ad4cb-9080-4661-ad54-5ea7c078599d
tags: [["event_type","AssistantResponse"]]
---

This clarifies it. **The backlog plugin could bundle the MCP server directly** - it's a design choice, not a limitation.

## Two Patterns in Your Plugins

### Schedule.md Plugin (Bundled)
```json
{
  "schedule": {
    "command": "bun",
    "args": ["run", "${CLAUDE_PLUGIN_ROOT}/src/mcp/server.ts"]
  }
}
```
- MCP server code lives **inside** the plugin at `src/mcp/server.ts`
- Uses `${CLAUDE_PLUGIN_ROOT}` to reference plugin files
- Full control, no external dependencies at runtime

### Backlog Plugin (External)
```json
{
  "backlog": {
    "command": "npx",
    "args": ["backlog.md", "mcp", "start"]
  }
}
```
- MCP server fetched from npm at runtime
- Plugin is just a thin wrapper
- Depends on network/npm availability

## Why Backlog Uses External

Looking at the backlog.md package - it's a substantial project with CLI, web UI, MCP server, etc. The plugin author likely chose the external approach to:
1. Avoid duplicating/maintaining that code
2. Get automatic updates from upstream
3. Keep the plugin simple

## The Alternative

The plugin **could** bundle the MCP server by:
1. Copying or vendoring the backlog.md MCP server code into `src/mcp/`
2. Changing `.mcp.json` to:
   ```json
   {
     "command": "node",
     "args": ["${CLAUDE_PLUGIN_ROOT}/src/mcp/server.js"]
   }
   ```

This would make it self-contained like Schedule.md, but requires maintaining that code.

**Bottom line**: It's an architectural trade-off. The current approach prioritizes simplicity over self-containment. Want me to refactor it to bundle the MCP server?
