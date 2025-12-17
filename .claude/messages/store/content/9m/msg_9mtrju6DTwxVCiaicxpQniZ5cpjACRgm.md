---
id: msg_9mtrju6DTwxVCiaicxpQniZ5cpjACRgm
kind: 103
account_id: claude
created_at: 1765935122415
imported_at: 1766005512205
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

Excellent! 🎉

**Summary of fixes applied:**

1. **`--setting-sources ""`** - Prevents recursive hook triggering in headless subprocess
2. **Wrapper script** - Captures stdin before `uv run` (which swallows stdin)
3. **HOOK_INPUT env var** - Passes data to Python script when stdin isn't available

Now the headless backend:
- ✅ Uses Max subscription (free)
- ✅ No recursive sessions
- ✅ Works in new instances
- ⏱️ ~5s latency per update

To switch back to API (faster, ~$0.72/month at 100/day):
```bash
echo "BACKEND=api" > .claude/statusline.conf
```
