---
id: msg_Fo6DjBLoefsPnj21GQY479kQvLLhJVeL
kind: 103
account_id: claude
created_at: 1765933216987
imported_at: 1766005520423
author_name: Claude
thread_id: cc_282a7ce9
platform: claude-code
session_id: 282a7ce9-2da3-4abe-b125-c94509967b13
tags: [["event_type","AssistantResponse"]]
---

The script uses `current_usage` from Claude Code's JSON input directly - it's a pre-calculated percentage. If it shows 226%, that's what Claude Code is reporting.

This happens because:
1. **Total tokens exceed the context window** - The session has accumulated more tokens than the 200K window
2. **Auto-compaction is pending** - Claude Code auto-compacts, but there can be a lag

At 226%, that session is way over budget. The other Claude should either:
- Run `/compact` to manually trigger compaction
- Or just keep working - auto-compaction will kick in soon

If you want the statusline to cap at 100%, I can add that, but honestly >100% is useful information - it tells you compaction is imminent or overdue.
