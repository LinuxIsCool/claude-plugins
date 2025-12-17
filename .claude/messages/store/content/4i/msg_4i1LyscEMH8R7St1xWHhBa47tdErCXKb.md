---
id: msg_4i1LyscEMH8R7St1xWHhBa47tdErCXKb
kind: 103
account_id: claude
created_at: 1765669799242
imported_at: 1766005510061
author_name: Claude
thread_id: cc_538cc19c
platform: claude-code
session_id: 538cc19c-9468-465c-ac4e-003ec46676d9
tags: [["event_type","AssistantResponse"]]
---

Done. I added `"showHiddenFolders": true` to `.obsidian/app.json`.

**Reload Obsidian** (Cmd/Ctrl+R or close and reopen) to apply the changes.

If `.claude/` still doesn't appear, Obsidian may be hardcoded to ignore dotfolders. In that case, the symlink workaround:

```bash
ln -s .claude claude
```

Then open `claude/journal/` in Obsidian — all the wikilinks will still work since they're relative, and the graph will render the DNA spiral.

Let me know if the setting worked or if you need the symlink.
