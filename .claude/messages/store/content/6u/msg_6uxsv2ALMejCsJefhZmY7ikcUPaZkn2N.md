---
id: msg_6uxsv2ALMejCsJefhZmY7ikcUPaZkn2N
kind: 103
account_id: claude
created_at: 1765561456309
imported_at: 1766005509116
author_name: Claude
thread_id: cc_f25ad4cb
platform: claude-code
session_id: f25ad4cb-9080-4661-ad54-5ea7c078599d
tags: [["event_type","AssistantResponse"]]
---

## Summary

**Why I don't have backlog MCP tools right now:**
- Plugin IS installed and registered ✓
- MCP config exists ✓  
- `npx backlog.md mcp start` works ✓
- **But**: Claude Code loads MCP servers at startup. You likely need to **restart Claude Code** to pick up the new plugin's MCP server.

**Back to your original question** - "why don't we include the MCP in the plugin":

The plugin *does* include the MCP config. The issue is it runs the MCP server via `npx backlog.md mcp start` (external package) instead of bundling the server code like Schedule.md does with `${CLAUDE_PLUGIN_ROOT}/src/mcp/server.ts`.

Both approaches are valid:

| Aspect | Backlog (External) | Schedule.md (Bundled) |
|--------|-------------------|----------------------|
| Server code | Fetched via npx | Lives in plugin |
| Offline use | ❌ Needs network | ✓ Works offline |
| Updates | Auto from npm | Manual |
| Complexity | Simple wrapper | Full implementation |

**To make backlog self-contained**, we'd need to vendor the backlog.md MCP server code into the plugin. Want me to do that, or shall we first restart Claude Code to test if the current setup works?
