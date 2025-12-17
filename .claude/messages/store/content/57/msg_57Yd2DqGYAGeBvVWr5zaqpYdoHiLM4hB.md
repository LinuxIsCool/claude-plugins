---
id: msg_57Yd2DqGYAGeBvVWr5zaqpYdoHiLM4hB
kind: 103
account_id: claude
created_at: 1765935516245
imported_at: 1766005512246
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

Done. Summary now updates on:

| Hook | When | Why |
|------|------|-----|
| **UserPromptSubmit** | User sends message | Capture user intent early |
| **Stop** | Claude finishes responding | Capture completed work |

Cache cleared. New sessions will pick up the change.

Note: This means ~2 summary generations per exchange (with headless, that's ~10s total). If latency bothers you, you could remove the UserPromptSubmit one and only keep Stop—that way it updates once after Claude finishes.
