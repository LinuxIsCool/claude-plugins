---
id: msg_9k78BtG6i3BdWESSuMib33wxWp5oMJxG
kind: 103
account_id: claude
created_at: 1765936729585
imported_at: 1766005512393
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

Fixed. The entry now has all fields including `created: 2025-12-16T15:43:45Z` for duration calculation.

**What happened:**
1. This session started ~2+ hours ago
2. When context was summarized/restored, the registry entry got overwritten or was incomplete
3. The `model` field was backfilled by statusline.sh, but other fields were missing
4. When I added `name: Phoenix`, I didn't restore the other fields

Next refresh should show the full statusline with duration (~2h14m), message count (#17), etc.
