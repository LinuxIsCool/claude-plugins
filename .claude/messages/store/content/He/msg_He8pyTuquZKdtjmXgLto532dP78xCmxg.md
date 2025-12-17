---
id: msg_He8pyTuquZKdtjmXgLto532dP78xCmxg
kind: 103
account_id: claude
created_at: 1765934700585
imported_at: 1766005512174
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

Fixed. The issue was **recursive hook triggering** - headless Claude was spawning its own session which triggered the same hooks again.

**The fix**: Added `--setting-sources ""` to the headless call, which disables all settings/hooks/plugins for that subprocess.

Now the headless backend:
- ✅ Uses Max subscription (free)
- ✅ No recursive sessions
- ✅ No log pollution from summary subprocesses
- ⏱️ Still ~5s latency (inherent to process spawn)

Try it in a new instance now - it should work correctly.
