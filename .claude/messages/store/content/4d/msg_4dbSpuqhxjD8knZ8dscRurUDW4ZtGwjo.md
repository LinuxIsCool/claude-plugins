---
id: msg_4dbSpuqhxjD8knZ8dscRurUDW4ZtGwjo
kind: 103
account_id: claude
created_at: 1765673727617
imported_at: 1766005510656
author_name: Claude
thread_id: cc_05038dd8
platform: claude-code
session_id: 05038dd8-d486-4cd4-bf86-b4c6b896d9d3
tags: [["event_type","AssistantResponse"]]
---

The CLI is working. You can try the interactive views:

```bash
# Interactive agent browser with TUI
bun plugins/agentnet/src/cli.ts agents

# View systems-thinker's wall
bun plugins/agentnet/src/cli.ts wall systems-thinker

# Check the global feed
bun plugins/agentnet/src/cli.ts feed
```

The TUI uses blessed/neo-neo-bblessed following the Backlog.md pattern you liked. Keyboard navigation: **↑↓/jk** to navigate, **Enter** to view details, **q/Esc** to quit.
