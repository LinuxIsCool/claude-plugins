---
id: msg_2e3DVn8nQTNAWxYrwp9kuTPwZhbJ2jRy
kind: 103
account_id: claude
created_at: 1765904400990
imported_at: 1766005511515
author_name: Claude
thread_id: cc_0a8bf3f1
platform: claude-code
session_id: 0a8bf3f1-1bed-40e7-8abd-689400f702b9
tags: [["event_type","AssistantResponse"]]
---

Done. The temporal plugin now injects full date+time in all timestamps:

**New format:**
```
[2025-12-16 08:59:25 PDT] SessionStart - Tuesday (morning)
[2025-12-16 08:59:25 PDT] UserPromptSubmit
[2025-12-16 08:59:26 PDT] Stop
```

**Changes made:**
1. `inject_timestamp.py` - Uses `ctx["timestamp"]` (full date+time) instead of `ctx["time"]` (time only)
2. `README.md` - Updated examples and documentation to reflect new format

**Benefits:**
- Self-contained timestamps (don't rely on SessionStart for date context)
- Handles midnight crossings gracefully
- Works correctly when conversation is continued after summarization
- Full temporal grounding at every interaction point
