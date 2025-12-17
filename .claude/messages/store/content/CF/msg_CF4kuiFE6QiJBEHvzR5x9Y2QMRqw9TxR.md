---
id: msg_CF4kuiFE6QiJBEHvzR5x9Y2QMRqw9TxR
kind: 103
account_id: claude
created_at: 1765933255861
imported_at: 1766005512123
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

## Engineering Analysis Complete

### Quantitative Tradeoffs

| Metric | API Direct | Headless Claude |
|--------|------------|-----------------|
| **Latency** | **~1.5s** | ~5.2s |
| **Cost** | ~$0.00024/req | **$0 (Max sub)** |
| **Memory** | **~10 MB** | ~450 MB |
| **Startup** | **Minimal** | Process spawn |
| **Reliability** | **High** | Medium |
| **Requires** | API key | Max subscription |

### Monthly Cost Projection (API)
- 10 summaries/day: **$0.07/month**
- 50 summaries/day: **$0.36/month**
- 100 summaries/day: **$0.72/month**
- 500 summaries/day: **$3.60/month**

### Modular Solution Implemented

The `auto-summary.py` hook now supports both backends:

**Configure via:**
1. **Config file**: `.claude/statusline.conf` or `~/.claude/statusline.conf`
   ```
   BACKEND=api      # or headless
   ```
2. **Environment variable**: `SUMMARY_BACKEND=api` or `SUMMARY_BACKEND=headless`

**Current setting**: Your project is now configured to use **API** (fast) in `.claude/statusline.conf`

**Key implementation details:**
- Headless requires `input=""` to avoid hanging
- Headless strips `ANTHROPIC_API_KEY` to force Max subscription
- API falls back to headless if no key available
- Both backends clean and normalize output identically

**To switch to headless (free):**
```bash
echo "BACKEND=headless" > .claude/statusline.conf
```
