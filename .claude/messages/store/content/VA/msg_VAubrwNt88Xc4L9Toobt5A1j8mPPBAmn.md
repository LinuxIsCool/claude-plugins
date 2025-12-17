---
id: msg_VAubrwNt88Xc4L9Toobt5A1j8mPPBAmn
kind: 103
account_id: claude
created_at: 1765935554085
imported_at: 1766005512259
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

Exactly right. The hook runs as a background subprocess - it doesn't block your conversation or consume your context. The ~5s latency is invisible to you.

**Current flow**:
```
User sends message
  → UserPromptSubmit hook fires (background)
    → Summary updates with user intent
  
Claude responds
  → Stop hook fires (background)  
    → Summary updates with completed work
```

Both run in parallel with your conversation. Free updates, no blocking, no token cost.
