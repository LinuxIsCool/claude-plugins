---
id: msg_D14sUfhrkH3ERPwEgao7WDYqd69uTewn
kind: 103
account_id: claude
created_at: 1765937149565
imported_at: 1766005512458
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

That fixes the count (initializes to 0). 

But for **duration** - if the statusline renders *before* the SessionStart hook completes, there's no registry entry yet to read `created` from. This would be a Claude Code timing issue we can't fully fix from hooks.

New sessions should now show:
- **#0** immediately (instead of nothing)
- **Duration** after first render cycle (once registry entry exists)

Want me to test with a new session to verify?
