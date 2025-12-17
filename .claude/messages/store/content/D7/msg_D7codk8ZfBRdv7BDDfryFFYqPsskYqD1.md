---
id: msg_D7codk8ZfBRdv7BDDfryFFYqPsskYqD1
kind: 103
account_id: claude
created_at: 1765929546498
imported_at: 1766005511887
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

## Done

**New statusline format:**
```
[Phoenix:e05da] Opus | claude | ctx:N% | $0.XX | #9 | Added count and summary history tracking
```

**What was added:**

1. **Message counter** (`#N` in magenta)
   - Hook: `plugins/statusline/hooks/user-prompt-submit.sh` → symlinked to `~/.claude/hooks/`
   - Increments on each user message
   - Stored in `.claude/instances/counts/{session_id}.txt`

2. **Summary history**
   - History file: `.claude/instances/summaries/{session_id}.history`
   - When updating summary, previous 2 are shown for context:
   ```
   Previous summaries (use for context when generating next summary):
   Statusline model & summary features
   Crash recovery, statusline model and summary
   ```

3. **Usage:**
   ```bash
   # Update summary (shows previous for context)
   summary.sh "$SESSION_ID" "New 5-8 word summary"
   
   # View history
   summary.sh "$SESSION_ID" --history
   ```

The counter will increment starting next message. Current count: **9**
