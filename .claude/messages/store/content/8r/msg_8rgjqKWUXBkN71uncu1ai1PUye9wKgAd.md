---
id: msg_8rgjqKWUXBkN71uncu1ai1PUye9wKgAd
kind: 103
account_id: claude
created_at: 1765929260230
imported_at: 1766005511863
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

5-8 sentences would be quite long for a statusline (it's a single line in the terminal). That would overflow and wrap awkwardly.

Did you mean:
- **5-8 words** (fits on statusline): `"Statusline model & summary features"`
- **5-8 sentences** (needs different display): A paragraph stored somewhere, maybe shown on hover or in a separate view?

If you want longer summaries, I could:
1. **Truncate on statusline** — Show first ~50 chars, store full summary in file
2. **Separate command** — `/statusline:instances` shows full summaries in a table
3. **Different location** — Store in registry JSON, display via command not statusline

What's your preference?
