---
id: msg_3b4znroRZzv3a1tuiGY9Rcq42y4VLdnr
kind: 103
account_id: claude
created_at: 1765930413727
imported_at: 1766005511953
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

Done. New format:

```
[Phoenix:e05da] Opus | ~/Workspace/sandbox/marketplaces/claude | ctx:N% | $X.XX | #14 | 28m | main +159/-14
Enhanced statusline with cwd, duration, git status, and diff stats.
```

**Fixed:**
- Full cwd path (with `~` for home)
- Pipe between `#N` and duration
- UserPromptSubmit hook added to `~/.claude/settings.json` — counter will increment starting next message
- Summary back to 5-10 words (70 char limit)
