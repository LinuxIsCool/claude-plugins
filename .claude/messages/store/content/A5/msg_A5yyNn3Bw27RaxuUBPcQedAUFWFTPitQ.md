---
id: msg_A5yyNn3Bw27RaxuUBPcQedAUFWFTPitQ
kind: 103
account_id: claude
created_at: 1765932397578
imported_at: 1766005512106
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

The auto-summary hook uses the **Anthropic API directly** via the `anthropic` Python library - not headless Claude.

This approach is:
- **Faster** - No Claude Code startup overhead, just a direct API call
- **Lighter** - Uses Haiku (claude-haiku-4-5-20251001) for quick, cheap summaries
- **More reliable** - Simple HTTP request vs spawning a full CLI process

The relevant code in `auto-summary.py`:

```python
import anthropic
client = anthropic.Anthropic(api_key=api_key)
msg = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=50,
    temperature=0.3,
    messages=[{"role": "user", "content": prompt}],
)
```

This is the same pattern the logging plugin uses for generating summaries in the markdown reports.
