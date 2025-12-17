---
id: msg_8ggERCbqvYHZ5bFPyQY2jV9Z5VWqqhnn
kind: 103
account_id: claude
created_at: 1765933588975
imported_at: 1766005520474
author_name: Claude
thread_id: cc_282a7ce9
platform: claude-code
session_id: 282a7ce9-2da3-4abe-b125-c94509967b13
tags: [["event_type","AssistantResponse"]]
---

Based on the debug data:
- `cache_read_input_tokens: 88,838` + `cache_creation_input_tokens: 4,874` + `input_tokens: 10` = **93,722 tokens**
- 93,722 / 200,000 = **~47%**

But `/context` shows **76%** (153k/200k).

The gap is because the statusline's `current_usage` only includes message/cache tokens - it **doesn't include** the system overhead:
- System prompt: 3.7k
- System tools: 20.7k
- MCP tools: 29.8k
- Custom agents: 1.0k
- Memory files: 1.6k

That's ~57k tokens of overhead not reflected in `current_usage`.

**Options:**
1. **Add fixed overhead estimate** (~57k for your setup) - hacky but closer
2. **Live with the approximation** - shows message growth accurately, just offset
3. **Remove ctx% entirely** - if it's not accurate, don't show it

What's your preference?
