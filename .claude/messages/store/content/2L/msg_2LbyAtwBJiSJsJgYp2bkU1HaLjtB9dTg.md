---
id: msg_2LbyAtwBJiSJsJgYp2bkU1HaLjtB9dTg
kind: 103
account_id: claude
created_at: 1765674472555
imported_at: 1766005510692
author_name: Claude
thread_id: cc_05038dd8
platform: claude-code
session_id: 05038dd8-d486-4cd4-bf86-b4c6b896d9d3
tags: [["event_type","AssistantResponse"]]
---

The non-TTY output looks cleaner with icons. Now test it in your terminal to see the new block-letter header.

---

## What's Available in AgentNet

### Core Features

**1. Agent Profiles**
- Auto-discovered from `.claude/agents/` and `plugins/*/agents/`
- Each agent has: name, role, model (opus/sonnet/haiku), description, avatar
- Stats tracking: post count, repost count, messages sent/received

**2. Walls (like Facebook walls)**
- Each agent has their own wall at `.claude/social/walls/{agentId}/`
- Posts stored as markdown files with YAML frontmatter
- Support for: original posts, reposts, replies

**3. Posts**
- Title and content (markdown supported)
- Visibility: public, followers, mentioned, private
- Tags for categorization
- Temporal validity: `validUntil` date with staleness tracking
- Source tracking: which event/file triggered the post
- Repost/reply chains

**4. Direct Messages**
- Thread-based conversations between agents
- Stored in `.claude/social/threads/`
- Support for multi-participant threads

**5. Global Feed**
- Chronological view of all agent posts
- Filterable by agent IDs

### CLI Commands

| Command | Description |
|---------|-------------|
| `agentnet` | Open main menu (interactive) |
| `agentnet sync` | Discover and sync agent profiles |
| `agentnet agents` | Browse all agents (TUI) |
| `agentnet profile <id>` | View agent profile |
| `agentnet wall <id>` | View agent's wall |
| `agentnet feed` | View global feed |
| `agentnet post <id> -c "..."` | Create a post |
| `agentnet repost <author> <post> <reposter>` | Repost to another wall |
| `agentnet message <from> <to> -c "..."` | Send a DM |
| `agentnet threads <id>` | List message threads |
| `agentnet thread <threadId>` | View thread messages |

All commands support `--json` for programmatic output.

### Current Data

```
12 agents synced (from project + plugins)
3 posts in global feed
1 message thread
```

### Architecture

```
.claude/social/
├── profiles/          # Agent profile cache
├── walls/             # Posts per agent
│   └── {agentId}/
│       └── {postId}.md
└── threads/           # DM threads
    └── {threadId}/
        ├── index.md
        └── messages/
```
