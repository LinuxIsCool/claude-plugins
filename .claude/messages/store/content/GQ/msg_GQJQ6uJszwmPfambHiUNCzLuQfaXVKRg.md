---
id: msg_GQJQ6uJszwmPfambHiUNCzLuQfaXVKRg
kind: 103
account_id: claude
created_at: 1765934035746
imported_at: 1766005512150
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

## Current Configuration

**Backend**: `api` (Direct Anthropic API with Haiku)
- Fast (~1.5s latency)
- Costs ~$0.00024 per update

**To switch to headless (free)**:
```bash
echo "BACKEND=headless" > .claude/statusline.conf
```

---

## When It Updates

| Hook | What Runs | Purpose |
|------|-----------|---------|
| **SessionStart** | `session-start.sh` | Registers instance, creates initial summary ("Awaiting instructions.") |
| **UserPromptSubmit** | `user-prompt-submit.sh` | Increments message counter (#N) |
| **UserPromptSubmit** | `auto-summary.py` | Regenerates summary from recent conversation |

So the summary updates **every time you send a message** (UserPromptSubmit hook).

---

## Not Currently Hooked

These hooks could also trigger summary updates but aren't configured:

| Hook | When It Fires |
|------|---------------|
| `Stop` | After Claude finishes responding |
| `AssistantResponse` | When Claude completes a response |
| `SubagentStop` | When a subagent completes |

If you want less frequent updates (to save API costs or reduce latency), we could move the summary generation to `Stop` instead of `UserPromptSubmit` - that way it only updates after Claude finishes responding, not on every user message.
