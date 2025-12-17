---
id: msg_2j4tpBRUWt2TuTxyEiokRAM4snosYP6F
kind: 103
account_id: claude
created_at: 1765935437509
imported_at: 1766005512231
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

Now modular. Here's the current architecture:

```
plugins/statusline/hooks/
├── auto-summary.py          # Main logic (DRY - both backends use same code)
├── auto-summary-wrapper.sh  # stdin handling for uv run
├── summary-prompt.txt       # ← EDIT THIS to change prompt
├── session-start.sh         # Registration hook
└── user-prompt-submit.sh    # Counter hook

.claude/
├── statusline.conf          # BACKEND=api|headless
└── summary-prompt.txt       # (optional) User-level prompt override
```

**To change the prompt**, edit `summary-prompt.txt`:
```
plugins/statusline/hooks/summary-prompt.txt
```

**Available placeholders**:
- `{agent_name}` - Instance name from registry (e.g., "Phoenix")
- `{context}` - Recent conversation (last 6 messages)
- `{prev_summaries}` - Last 3 summaries for continuity

**Priority**: Plugin file → `~/.claude/summary-prompt.txt` → hardcoded default
