---
id: msg_HzZsRhEVCKY5zt3GHmcBGvUXb7dn3Myd
kind: 103
account_id: claude
created_at: 1765933385105
imported_at: 1766005520439
author_name: Claude
thread_id: cc_282a7ce9
platform: claude-code
session_id: 282a7ce9-2da3-4abe-b125-c94509967b13
tags: [["event_type","AssistantResponse"]]
---

Updated. The script now correctly reads from `.context_window.current_usage.input_tokens` and `.context_window.current_usage.output_tokens` to calculate the percentage.

Your next prompt should show a more accurate context percentage. If it's still off, we may need to dump the actual JSON to see what Claude Code is sending. Let me know if the percentage looks right on the next statusline update.
