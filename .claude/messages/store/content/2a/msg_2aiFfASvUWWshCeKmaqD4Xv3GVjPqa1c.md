---
id: msg_2aiFfASvUWWshCeKmaqD4Xv3GVjPqa1c
kind: 103
account_id: claude
created_at: 1765937094791
imported_at: 1766005512444
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

All entries now have `created` timestamps. Duration should work for these sessions.

**What was happening:**
1. Statusline.sh backfills `model` when it runs (creates partial entry)
2. Session-start hook should create full entry, but for some sessions it never ran
3. Result: partial entries with only `model`, no `created` for duration

The hook is working correctly now - new sessions will get proper registration. The 8 sessions in the registry are fixed.
