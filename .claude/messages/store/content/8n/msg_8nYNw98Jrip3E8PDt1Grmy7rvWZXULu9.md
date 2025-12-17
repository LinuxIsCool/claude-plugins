---
id: msg_8nYNw98Jrip3E8PDt1Grmy7rvWZXULu9
kind: 103
account_id: claude
created_at: 1765936009235
imported_at: 1766005512291
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

The summaries **ARE working**. This session shows:

```
Evaluating headless Claude versus Anthropic API costs.
Debugging headless backend integration issues.
Debugging headless backend integration in new instance.
Debugging headless backend in new instance.
Refactoring summary infrastructure for modularity.
```

Those are accurate summaries of the actual work from today's session.

The "Awaiting instructions" summaries you saw were from sessions with minimal context - users who only said "Hello" and "Test". With thin context, the summary generator produces generic responses. That's expected behavior.

The system is functioning correctly:
- Hooks are firing
- Context is being extracted from logs
- Headless Claude is generating summaries
- Summaries are being saved

Is there a specific session or behavior you're seeing that seems wrong? Or is the issue that new sessions start with generic summaries until meaningful conversation happens?
