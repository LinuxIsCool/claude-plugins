---
id: msg_EMyZPPhuFbkK2aV3zreFmNSdrwGirTKg
kind: 103
account_id: claude
created_at: 1765932639005
imported_at: 1766005520335
author_name: Claude
thread_id: cc_282a7ce9
platform: claude-code
session_id: 282a7ce9-2da3-4abe-b125-c94509967b13
tags: [["event_type","AssistantResponse"]]
---

No project override there. Your global setting shows `alwaysThinkingEnabled: true` which should work. A few possibilities:

1. **Bug with persistence** - Changelog 2.0.70 mentions "Fix thinking mode toggle in /config not persisting correctly" - this might be a recent fix or still not fully resolved.

2. **Subagent inheritance** - If you're spawning Claude instances via Task tool, they might not inherit the thinking setting from the parent session.

3. **Session vs global scope** - The thinking toggle might be session-scoped rather than truly global despite the setting name.

**To verify/fix:**
- Try running `/config` in this session and toggle thinking on explicitly
- Check if `MAX_THINKING_TOKENS` environment variable is set (could override)
- You could also try setting `MAX_THINKING_TOKENS=31999` in your shell to force it on

```bash
env | grep -i think
```

Would you like me to investigate further, or would you prefer to just toggle it via `/config` for now?
