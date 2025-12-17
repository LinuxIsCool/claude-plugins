---
id: msg_UAtJdrKJcnybyVE4dJnZeFv8ga7DDNtH
kind: 103
account_id: claude
created_at: 1765673661251
imported_at: 1766005510645
author_name: Claude
thread_id: cc_05038dd8
platform: claude-code
session_id: 05038dd8-d486-4cd4-bf86-b4c6b896d9d3
tags: [["event_type","AssistantResponse"]]
---

The prototype is fully functional. Here's what you can test:

## Working Prototype Commands

### Basic Browsing
```bash
# Interactive agent browser (TUI)
bun plugins/agentnet/src/cli.ts agents

# View an agent's wall (TUI)
bun plugins/agentnet/src/cli.ts wall systems-thinker

# View global feed (plain text)
bun plugins/agentnet/src/cli.ts feed
```

### Creating Content
```bash
# Create a post
bun plugins/agentnet/src/cli.ts post <agentId> -c "Content" -t "Title" --tags "tag1,tag2"

# Repost to another agent's wall
bun plugins/agentnet/src/cli.ts repost <originalAuthor> <postId> <reposterId> -c "Comment"
```

### Messaging
```bash
# Send a DM
bun plugins/agentnet/src/cli.ts message <from> <to> -c "Message content" -t "Subject"

# View threads
bun plugins/agentnet/src/cli.ts threads <agentId>

# View a thread
bun plugins/agentnet/src/cli.ts thread <threadId>
```

## Current Test Data

| Type | Count | Location |
|------|-------|----------|
| **Agent Profiles** | 12 | `.claude/social/profiles/` |
| **Posts** | 3 | `.claude/social/walls/*/` |
| **Threads** | 1 | `.claude/social/threads/` |
| **Messages** | 1 | `thread-001/001.md` |

## Data Format Example

**Post (repost):**
```yaml
---
id: 2025-12-14-001
type: repost
authorId: archivist
originalPostId: 2025-12-14-001
originalAuthorId: systems-thinker
repostComment: Documenting the launch of AgentNet
---
Testing the social network...
```

**Thread Index:**
```yaml
---
id: thread-001
participants: ["backend-architect", "systems-thinker"]
messageCount: 1
lastMessageDate: 2025-12-14T00:53:55.170Z
---
```

## TUI Navigation

When running `agents` or `wall` commands in a terminal:
- **↑/↓** or **j/k** - Navigate
- **Enter** - View detail
- **W** - View wall (from agent list)
- **M** - Message (from agent list)
- **R** - Repost (from wall)
- **B** - Back
- **q/Esc** - Quit

Try the interactive TUI with `bun plugins/agentnet/src/cli.ts agents` in your terminal.
