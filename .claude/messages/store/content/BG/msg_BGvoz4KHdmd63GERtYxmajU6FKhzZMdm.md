---
id: msg_BGvoz4KHdmd63GERtYxmajU6FKhzZMdm
kind: 103
account_id: claude
created_at: 1765672606261
imported_at: 1766005509762
author_name: Claude
thread_id: cc_d49e6b0a
platform: claude-code
session_id: d49e6b0a-03db-4ab3-922d-43b820eea0bb
tags: [["event_type","AssistantResponse"]]
---

## Simple Explanation

**The situation:** You have multiple Claude Code sessions running at the same time, each working on different parts of the same project. They're like coworkers who don't share an office.

**The problem we were thinking about:** How do these sessions know what each other did? How do they coordinate without stepping on each other's toes?

**The original plan:** We were designing complicated systems - servers, protocols, databases - to let agents talk to each other.

**What actually happened:** While we were planning all that, we noticed something. Two sessions had been working in parallel. One created agents and a reflection command. The other (ours) was doing strategic planning. Neither knew about the other.

But when we looked at the files and the git history, we could see exactly what the other session did. No special protocol needed.

**The insight:** Git already does this.

- When a session makes changes, it shows up in git
- Any other session can look at git and see what changed
- The files themselves are the messages
- The commit messages explain why

**The analogy:** It's like coworkers who leave notes on a shared whiteboard instead of having meetings. Everyone can see what everyone else wrote. No scheduling required. No complex communication system. Just... the whiteboard.

**Why this matters:** We were over-engineering. The filesystem + git is already a coordination system. We just needed to recognize it and use it deliberately instead of accidentally.

**Bottom line:** Agents can "talk" to each other by:
1. Writing to known locations (like `.claude/perspectives/agent-name/`)
2. Committing their work
3. Other agents reading those locations and checking git history

Simple. Already works. No infrastructure needed.
