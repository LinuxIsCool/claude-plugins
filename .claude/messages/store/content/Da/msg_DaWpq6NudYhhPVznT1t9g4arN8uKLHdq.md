---
id: msg_DaWpq6NudYhhPVznT1t9g4arN8uKLHdq
kind: 103
account_id: claude
created_at: 1765937454289
imported_at: 1766005512484
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

It's working now - I just tested it and got **10h26m**. The cache might not have updated for your running session yet.

Regarding the 10h25m being "wrong" - that's actually when session `e05dab22` was **first created**. Even with context continuation/compaction, the session_id stays the same, so duration tracks from original creation.

If you want duration to reset on context continuation, we'd need to detect the "compact" or "resume" source in SessionStart and update the `created` timestamp. Want me to add that behavior?
