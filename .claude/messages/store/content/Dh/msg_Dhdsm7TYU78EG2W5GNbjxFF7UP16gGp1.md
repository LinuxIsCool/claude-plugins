---
id: msg_Dhdsm7TYU78EG2W5GNbjxFF7UP16gGp1
kind: 103
account_id: claude
created_at: 1765930841464
imported_at: 1766005512028
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

Good point — new Claude instances won't know to update summaries. There's no instruction telling them to.

**Options:**

1. **Add to CLAUDE.md** — Tell all instances to update their summary periodically
2. **Add to session-start hook output** — Remind new instances to use `summary.sh`
3. **Create a skill** — Document the summary convention so instances can learn it

The simplest fix is adding to the session-start hook output, similar to how it prompts for self-naming:

```bash
# After naming prompt, add:
echo "Update your summary periodically:"
echo "  summary.sh \"\$SESSION_ID\" \"5-10 word first-person summary\""
```

Want me to add that to the session-start hook?
