---
id: msg_2mebdqowufgSAKa9rDoYQkBfwN6SzZpE
kind: 103
account_id: claude
created_at: 1765935658997
imported_at: 1766005521341
author_name: Claude
thread_id: cc_f280e0d0
platform: claude-code
session_id: f280e0d0-e4a3-4d44-a458-de741d55c168
tags: [["event_type","AssistantResponse"]]
---

Based on the hooks configuration in `plugins/statusline/.claude-plugin/plugin.json`:

**Currently updating on:**
- `SessionStart` - instance registration
- `UserPromptSubmit` - counter + auto-summary
- `Stop` - auto-summary

**NOT updating on response** - there's no `AssistantResponse` hook configured.

So to directly answer: **Submit only, not response.**

Would you like to add an `AssistantResponse` hook to update status after I respond as well?
