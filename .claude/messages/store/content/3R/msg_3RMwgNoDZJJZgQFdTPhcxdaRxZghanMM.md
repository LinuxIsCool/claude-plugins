---
id: msg_3RMwgNoDZJJZgQFdTPhcxdaRxZghanMM
kind: 103
account_id: claude
created_at: 1765937975676
imported_at: 1766005521822
author_name: Claude
thread_id: cc_62e5188c
platform: claude-code
session_id: 62e5188c-281b-4909-9d8f-996705bfb665
tags: [["event_type","AssistantResponse"]]
---

Done. Implemented and committed as `b207ccf`.

**How it works:**

1. **Trigger**: `UserPromptSubmit` hook fires
2. **Count check**: `user-prompt-submit.sh` increments count (0 → 1)
3. **Name generation**: `auto-name.py` checks `count == 1`, generates name via headless Haiku
4. **Registry update**: New name written to `registry.json`

**Files added:**
- `auto-name.py` - Main logic (same dual-backend pattern as auto-summary)
- `auto-name-wrapper.sh` - stdin capture for uv run
- `name-prompt.txt` - Customizable prompt template

**Plugin cache cleared.** Start a new session to test - the first prompt you send will trigger name generation. You can enable debug output with `DEBUG_NAME=1` to see what's happening.
