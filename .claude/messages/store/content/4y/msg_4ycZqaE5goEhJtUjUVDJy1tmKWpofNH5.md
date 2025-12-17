---
id: msg_4ycZqaE5goEhJtUjUVDJy1tmKWpofNH5
kind: 103
account_id: claude
created_at: 1765586179794
imported_at: 1766005509589
author_name: Claude
thread_id: cc_7f5d9f72
platform: claude-code
session_id: 7f5d9f72-5703-4425-bba7-ac6313ba2ba2
tags: [["event_type","AssistantResponse"]]
---

Yes, each agent spawned via the Task tool has a unique ID. When an agent completes, it returns its agent ID along with its result. You can use this ID to resume the agent later via the `resume` parameter, which continues the agent with its full previous context preserved.

This is useful for:
- Follow-up questions on the same topic
- Continuing work that was interrupted
- Adding to previous research or exploration
