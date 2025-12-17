---
id: msg_6HAZZ6FaBBzPLP7nSmQipWmvu2uaQMR1
kind: 103
account_id: claude
created_at: 1765933840876
imported_at: 1766005520504
author_name: Claude
thread_id: cc_282a7ce9
platform: claude-code
session_id: 282a7ce9-2da3-4abe-b125-c94509967b13
tags: [["event_type","AssistantResponse"]]
---

77% vs 80% - that's only a 3% difference now. That's pretty close and definitely usable. The small gap is likely due to:

1. Overhead being slightly higher than 28% (actual is ~28.4%)
2. Timing differences between statusline and /context updates
3. Some additional tokens not captured in the simple calculation

If you want it even closer, bump `OVERHEAD_PCT` from 28 to 30 or 31. But 77% vs 80% is reasonably accurate for a statusline indicator.
