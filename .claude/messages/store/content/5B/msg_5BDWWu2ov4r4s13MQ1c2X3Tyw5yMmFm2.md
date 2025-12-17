---
id: msg_5BDWWu2ov4r4s13MQ1c2X3Tyw5yMmFm2
kind: 103
account_id: claude
created_at: 1765929232174
imported_at: 1766005511857
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

## Done

**New statusline format:**
```
[Phoenix:e05da] Opus | claude | ctx:5% | $0.42 | Statusline model & summary features
```

**Changes made to `statusline.sh`:**
1. **Model display** — Now shows `Opus`/`Sonnet`/`Haiku` after the name
2. **Registry backfill** — Automatically writes model to registry (your entry now shows `"model": "Opus 4.5"`)
3. **Summary display** — Reads from `.claude/instances/summaries/{session_id}.txt`

**New tool:** `plugins/statusline/tools/summary.sh`
```bash
summary.sh "$SESSION_ID" "3-8 word summary"
```

**To update summary during a session:**
```bash
/home/ygg/Workspace/sandbox/marketplaces/claude/plugins/statusline/tools/summary.sh "$SESSION_ID" "New summary here"
```

Your statusline should now show the model. The summary will appear once I (or any instance) updates it. Want me to add a hook that auto-prompts Claude to update the summary periodically?
