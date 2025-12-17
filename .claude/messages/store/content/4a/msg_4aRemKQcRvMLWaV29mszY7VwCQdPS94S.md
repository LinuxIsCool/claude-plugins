---
id: msg_4aRemKQcRvMLWaV29mszY7VwCQdPS94S
kind: 103
account_id: claude
created_at: 1765934639659
imported_at: 1766005520582
author_name: Claude
thread_id: cc_282a7ce9
platform: claude-code
session_id: 282a7ce9-2da3-4abe-b125-c94509967b13
tags: [["event_type","AssistantResponse"]]
---

Here's what the research found:

## `current_usage` Fields Explained

| Field | Meaning |
|-------|---------|
| `input_tokens` | Tokens **after the last cache breakpoint** - NOT all input tokens. Just the new, uncached portion. |
| `cache_creation_input_tokens` | Tokens being **written to cache** for the first time |
| `cache_read_input_tokens` | Tokens **retrieved from existing cache** (reused) |
| `output_tokens` | Tokens in the model's response |

## The Math

**Total input tokens for a request:**
```
total = cache_read + cache_creation + input_tokens
```

Your current statusline calculation is **correct** for this.

## Why It Doesn't Match /context

The gap exists because:
- **`current_usage`** = tokens sent to API for **this request** (conversation/cache)
- **`/context`** = **full context window** including system prompt, tool definitions, MCP tools, agents, memory files

The `current_usage` is essentially just the **Messages** portion from `/context`, not the entire context window.

## Bottom Line

The statusline shows **cache/conversation tokens** (~50-60% of context), while `/context` shows **everything** (~92%). Both are accurate for what they measure - they're just measuring different things.

If you want the statusline to match `/context`, you'd need Claude Code to expose the full context calculation (system + tools + conversation), which isn't currently in the statusline JSON.
