---
id: msg_8SrUHLTXRZHKSsHamPPyhVeTbg9NkGxT
kind: 103
account_id: claude
created_at: 1765931670496
imported_at: 1766005512075
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

The new sessions don't have summaries. This confirms **Claude Code needs a full restart** to load the new hooks from settings.json.

The many summary files you see (16:28-16:33) were likely generated from other test sessions, not from the new instances.

**To enable auto-summaries:**
1. Quit ALL Claude Code instances (including this one)
2. Start fresh

The hooks in `~/.claude/settings.json` will then be active for new sessions.

Want me to check if there's another way to reload hooks without restart?
