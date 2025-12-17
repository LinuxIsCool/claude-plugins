---
id: msg_3GaqenHLxzirmt28HrUon44YKMzGoyAy
kind: 103
account_id: claude
created_at: 1765930216520
imported_at: 1766005511937
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

Done. New statusline format:

```
[Phoenix:e05da] Opus | claude | ctx:N% | $X.XX | #13 25m | main +159/-14
Recovered from crash, enhanced statusline with model, message count, session duration, git branch status (blue=clean, red=dirty), and diff stats showing lines changed.
```

**Added:**
- **Duration** (`25m`) — time since session start, after message count
- **Branch name** (`main`) — blue if clean, red if dirty (currently red)
- **Diff stats** (`+159/-14`) — unstaged insertions/deletions
