---
id: msg_3kdq6AEqSZXBsBiGpdHKA4ZFRhduvusL
kind: 103
account_id: claude
created_at: 1765934312709
imported_at: 1766005520537
author_name: Claude
thread_id: cc_282a7ce9
platform: claude-code
session_id: 282a7ce9-2da3-4abe-b125-c94509967b13
tags: [["event_type","AssistantResponse"]]
---

Done. Unfortunately, `/context` is TUI-only and can't be run headless.

**Summary of changes:**

1. **Statusline now shows**: `ctx:31+53=84%` format (fixed + messages = total)
2. **Reads overhead from**: `~/.claude/overhead_pct.txt`
3. **Calibration tool**: `~/.claude/compute-overhead.sh`

**To calibrate with your actual overhead:**

From your `/context` output:
- System prompt: 1.9%
- System tools: 10.3%
- MCP tools: 14.9%
- Custom agents: 0.5%
- Memory files: 0.8%
- **Total: ~28%**

Run:
```bash
~/.claude/compute-overhead.sh 28
```

This will make your statusline more accurate. The overhead only changes when you enable/disable plugins, so you rarely need to recalibrate.
