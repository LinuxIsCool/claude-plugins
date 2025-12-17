---
id: msg_ANhT3dU5oBLEkLEBafZTrA4CC9MpKwQQ
kind: 103
account_id: claude
created_at: 1765935720217
imported_at: 1766005512272
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

Done. Now updates on:

| Hook | When |
|------|------|
| **SessionStart** | Instance registered |
| **UserPromptSubmit** | User sends message |
| **Stop** | Claude finishes turn |
| **AssistantResponse** | Response generated |

That's potentially 3 summary updates per exchange (submit + stop + response). All background, all free.

The other instance you showed needs to restart to pick up the new hooks - it loaded the old cached config.
