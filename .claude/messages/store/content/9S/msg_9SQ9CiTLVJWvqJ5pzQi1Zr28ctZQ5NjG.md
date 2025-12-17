---
id: msg_9SQ9CiTLVJWvqJ5pzQi1Zr28ctZQ5NjG
kind: 103
account_id: claude
created_at: 1765585452302
imported_at: 1766005509392
author_name: Claude
thread_id: cc_0a8bf3f1
platform: claude-code
session_id: 0a8bf3f1-1bed-40e7-8abd-689400f702b9
tags: [["event_type","AssistantResponse"]]
---

Found it. To apply our changes, you need to **refresh the plugin cache**:

```bash
# Option 1: Remove the cache and restart Claude Code
rm -rf ~/.claude/plugins/cache/linuxiscool-claude-plugins/

# Option 2: Or use the plugin command to reinstall
# In Claude Code:
/plugin uninstall linuxiscool-claude-plugins
/plugin install /path/to/marketplace.json
```

After clearing the cache and restarting Claude Code:
- The cache will be rebuilt from your updated source files
- Only the 10 master skills should appear
- No more truncation

Would you like me to clear the cache for you?
