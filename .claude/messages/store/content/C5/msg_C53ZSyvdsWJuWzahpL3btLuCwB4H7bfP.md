---
id: msg_C53ZSyvdsWJuWzahpL3btLuCwB4H7bfP
kind: 103
account_id: claude
created_at: 1765932543834
imported_at: 1766005520318
author_name: Claude
thread_id: cc_282a7ce9
platform: claude-code
session_id: 282a7ce9-2da3-4abe-b125-c94509967b13
tags: [["event_type","AssistantResponse"]]
---

Extended thinking is off by default for most models primarily for **cost and efficiency reasons**:

1. **Token costs** - You're charged for all thinking tokens, even though only a summary is shown. Keeping it off prevents unexpected token consumption.

2. **Prompt caching** - Extended thinking impacts prompt caching efficiency, which can slow down repeated operations.

3. **Not always needed** - Many tasks (simple edits, quick questions) don't benefit from deep reasoning.

**Exceptions**: Sonnet 4.5 and Opus 4.5 have thinking enabled by default since they're designed for complex reasoning.

**To enable it**:
- `/config` → toggle thinking on globally
- Use `ultrathink` keyword in a message for a single request
- Set `MAX_THINKING_TOKENS` environment variable

You can press **Ctrl+O** to toggle verbose mode and see the thinking output when it's enabled.
