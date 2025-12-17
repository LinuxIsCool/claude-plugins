---
id: msg_GGMh6CwXmYpj4eE7iVCgwuuh3bctBdqg
kind: 103
account_id: claude
created_at: 1765936104529
imported_at: 1766005512306
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

I see the timing issue. Here's what's happening:

**Sequence:**
1. User submits prompt → `UserPromptSubmit` hook fires → summary generates (in background)
2. Claude processes your message
3. Claude responds → statusline refreshes → displays updated summary

The statusline only refreshes when **Claude Code renders it** - which happens after Claude responds, not immediately when you submit a prompt. By the time the statusline refreshes, you see the new summary.

**The summary IS being generated on UserPromptSubmit** - but the display won't update until the next statusline render cycle.

This is architectural - hooks can update files, but they can't force a statusline refresh. The statusline is a Claude Code feature that polls/renders at specific intervals.

**Options:**
1. Accept the ~1-2 second delay (summary updates, display catches up on next render)
2. Remove the UserPromptSubmit summary update and only update on Stop - simpler, less work for same visible result
3. The headless backend adds ~5s latency anyway, so the display would be stale regardless

Want me to simplify and only update on Stop? Since the statusline only refreshes after Claude responds anyway, updating on UserPromptSubmit is redundant work.
