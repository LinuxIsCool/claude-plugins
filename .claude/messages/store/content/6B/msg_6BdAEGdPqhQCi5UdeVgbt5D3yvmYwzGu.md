---
id: msg_6BdAEGdPqhQCi5UdeVgbt5D3yvmYwzGu
kind: 103
account_id: claude
created_at: 1766004684454
imported_at: 1766005523473
author_name: Claude
thread_id: cc_e3079ff0
platform: claude-code
session_id: e3079ff0-7670-4e37-9b80-9a4cb0eb1cc6
tags: [["event_type","AssistantResponse"]]
---

---

## Summary

`★ Insight ─────────────────────────────────────`
**The fix worked because of three key changes:**

1. **Framing shift**: Changed from "intelligent version control assistant" to "CLASSIFIER FUNCTION - NOT AN ASSISTANT". This fundamentally changes how Haiku interprets its role.

2. **Output format BEFORE context**: The original prompt put format requirements at the END after ~2000 chars of context. Haiku would "forget" them. Now format is shown first, with 5 concrete examples.

3. **`--max-turns 1`**: Even if Haiku tries to call tools, this flag prevents any follow-up turns. Combined with `--tools ""`, it's now truly single-shot.

**The difference in behavior**: Before, Haiku would start reasoning ("I need to examine...") and try actions. Now it outputs exactly `SKIP: reason` or `COMMIT` with the message format.
`─────────────────────────────────────────────────`

---

**One note**: The `.env.example` file is being flagged as sensitive due to the `\.env($|\.)` pattern. This is arguably too aggressive - `.env.example` files are templates, not secrets. Want me to refine that pattern to exclude `.example` and `.sample` suffixes?
