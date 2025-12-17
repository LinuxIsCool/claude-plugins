---
id: msg_EbGcNKeHdD5SCg4rMUh7ocxDwK3ikuNb
kind: 103
account_id: claude
created_at: 1765822013423
imported_at: 1766005510955
author_name: Claude
thread_id: cc_7b98de99
platform: claude-code
session_id: 7b98de99-aecb-4db8-ae1d-062359b91e87
tags: [["event_type","AssistantResponse"]]
---

I now have comprehensive findings. Let me synthesize everything:

## Root Cause Analysis: Backlog MCP Server Not Finding Project Root

### The Problem

The backlog MCP server reports "not initialized" even though `backlog/` exists at the project root because:

1. **MCP servers don't inherit the project working directory** - According to Claude Code docs, plugin MCP servers start in an unpredictable location (could be plugin dir, cache, or elsewhere)

2. **The backlog plugin doesn't set `cwd`** - Compare:

   **Schedule.md** (working):
   ```json
   "env": {
     "SCHEDULE_ROOT": "${CLAUDE_PLUGIN_ROOT}"
   }
   ```

   **Backlog** (broken):
   ```json
   "env": {}
   ```

3. **Backlog.md CLI uses `process.cwd()` directly** instead of using its own `findBacklogRoot()` function:

   ```typescript
   // src/commands/mcp.ts:35
   const server = await createMcpServer(process.cwd(), ...);
   ```

   The `findBacklogRoot()` function (which walks UP directories looking for `backlog/`) exists but **isn't called** by the MCP startup.

### Why This Is Happening

```
Claude Code starts MCP server
    ↓
cwd = ??? (NOT project root)
    ↓
Backlog.md uses process.cwd()
    ↓
Looks for backlog/ in wrong location
    ↓
"Not initialized"
```

### Verification

The `findBacklogRoot()` at `resources/Backlog.md/src/utils/find-backlog-root.ts` shows the intended behavior:
- Walk up from startDir looking for `backlog/` or `backlog.json`
- Fall back to git root
- This would work if it were used

### Fix Options

**Option 1: Plugin-side fix** (immediate)

Update `plugins/backlog/.mcp.json`:
```json
{
  "mcpServers": {
    "backlog": {
      "command": "npx",
      "args": ["backlog.md", "mcp", "start"],
      "cwd": "${CLAUDE_PROJECT_ROOT}",
      "env": {}
    }
  }
}
```

Note: Need to verify if `${CLAUDE_PROJECT_ROOT}` is a valid variable.

**Option 2: Upstream fix** (proper)

The Backlog.md CLI should use `findBacklogRoot()` in `src/commands/mcp.ts`:
```typescript
const projectRoot = await findBacklogRoot(process.cwd()) || process.cwd();
const server = await createMcpServer(projectRoot, { debug: options.debug });
```

This would make it work regardless of where the MCP server is started.

---

**Would you like me to:**
1. Test what `cwd` options are available for Claude Code plugin MCP servers?
2. File an issue/PR for the upstream Backlog.md fix?
3. Implement a plugin-side workaround?
