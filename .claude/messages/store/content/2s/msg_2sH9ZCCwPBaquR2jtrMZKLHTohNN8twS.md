---
id: msg_2sH9ZCCwPBaquR2jtrMZKLHTohNN8twS
kind: 103
account_id: claude
created_at: 1765930999223
imported_at: 1766005512042
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

Found the issue: `Credit balance is too low` — headless Claude can't run.

The auto-summary hook is set up correctly, but it needs API credits for headless Claude calls. Options:

1. **Add credits** — Then it will work automatically
2. **Use a different approach** — Perhaps a simpler heuristic-based summary (no LLM)
3. **Manual updates** — Keep using `summary.sh` manually

The hook is ready and will work once credits are available. After restart, both the counter and auto-summary will run on each UserPromptSubmit.
