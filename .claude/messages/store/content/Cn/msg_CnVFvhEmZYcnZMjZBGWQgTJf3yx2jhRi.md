---
id: msg_CnVFvhEmZYcnZMjZBGWQgTJf3yx2jhRi
kind: 103
account_id: claude
created_at: 1765667871666
imported_at: 1766005510239
author_name: Claude
thread_id: cc_298311d7
platform: claude-code
session_id: 298311d7-dc9e-4d73-bbb3-323eaba7d29e
tags: [["event_type","AssistantResponse"]]
---

Fixed. The `agents` field requires explicit file paths, not directories.

**Change made**:
```json
// Before (invalid)
"agents": ["./agents/"]

// After (valid)
"agents": ["./agents/mentor.md"]
```

**Discovery**: Claude Code natively supports plugin agents with automatic namespacing. No build script needed - just list the `.md` files in `plugin.json`.

Restart Claude Code and the `awareness:mentor` agent should be available.
