---
id: msg_AAt4SCcJAi36vrjciwe2T8idi6rvpTa4
kind: 103
account_id: claude
created_at: 1765822104274
imported_at: 1766005510966
author_name: Claude
thread_id: cc_7b98de99
platform: claude-code
session_id: 7b98de99-aecb-4db8-ae1d-062359b91e87
tags: [["event_type","AssistantResponse"]]
---

Based on all the research, there's **no `${CLAUDE_PROJECT_ROOT}` variable** - only `${CLAUDE_PLUGIN_ROOT}` exists for plugins.

## Confirmed Solution Path

Since the plugin can only reference its own root (not the project root), the **proper fix is upstream** in Backlog.md itself.

### Recommended Action: PR to Backlog.md

The fix is simple - modify `src/commands/mcp.ts` to use the existing `findBacklogRoot()`:

```typescript
// Before (line ~33-35)
.action(async (options: StartOptions) => {
  try {
    const server = await createMcpServer(process.cwd(), { debug: options.debug });

// After
import { findBacklogRoot } from "../utils/find-backlog-root.ts";
// ...
.action(async (options: StartOptions) => {
  try {
    const projectRoot = await findBacklogRoot(process.cwd()) || process.cwd();
    const server = await createMcpServer(projectRoot, { debug: options.debug });
```

This one-line change would:
1. Walk up from `process.cwd()` looking for `backlog/` or `backlog.json`
2. Fall back to git root if no backlog found
3. Use `process.cwd()` as final fallback
4. Make the MCP server work regardless of starting location

### For Now: Verify the Workaround

You have the Backlog.md source in `resources/Backlog.md/`. You could:

1. **Apply the fix locally** and test
2. **Submit a PR upstream** to MrLesk/Backlog.md
3. **Use project-scoped MCP** (add `.mcp.json` at project root instead of relying on plugin)

Would you like me to prepare the upstream fix for Backlog.md?

---

**Sources:**
- [Claude Code Plugins Reference](https://code.claude.com/docs/en/plugins-reference)
- [Connect Claude Code to tools via MCP](https://docs.anthropic.com/en/docs/claude-code/mcp)
- [Configuring MCP Tools in Claude Code](https://scottspence.com/posts/configuring-mcp-tools-in-claude-code)
