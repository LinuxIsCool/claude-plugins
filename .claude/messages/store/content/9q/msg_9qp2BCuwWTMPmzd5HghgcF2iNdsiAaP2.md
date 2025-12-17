---
id: msg_9qp2BCuwWTMPmzd5HghgcF2iNdsiAaP2
kind: 103
account_id: claude
created_at: 1765933509748
imported_at: 1766005520457
author_name: Claude
thread_id: cc_282a7ce9
platform: claude-code
session_id: 282a7ce9-2da3-4abe-b125-c94509967b13
tags: [["event_type","AssistantResponse"]]
---

Based on the debug JSON:
- `cache_read_input_tokens: 85150` + `cache_creation_input_tokens: 606` + `input_tokens: 8` = **85,764 tokens**
- 85,764 / 200,000 = **~43%**

This should now show around 43% in your statusline. The gap vs `/context` showing 71% might be because `/context` includes things not reported in `current_usage` (system overhead, tool definitions, etc.) or calculates it differently.

Try sending another message and let me know what percentage you see now.
