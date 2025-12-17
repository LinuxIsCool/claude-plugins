---
id: msg_4btmNwVD2nC68PRX12SYQmeT5JNoqkfh
kind: 103
account_id: claude
created_at: 1765509743017
imported_at: 1766005509030
author_name: Claude
thread_id: cc_5fa98c28
platform: claude-code
session_id: 5fa98c28-a3c8-49b3-965a-8f9e399efb65
tags: [["event_type","AssistantResponse"]]
---

## Synthesis: Prerequisites for Backlog.md Plugin Implementation

All three research agents have completed their analysis. Here's the synthesized findings:

---

### Repository Overview

This is a **Claude Code Plugin Marketplace** with these implemented plugins:
- **brainstorm** - Commands-focused (slash command for capturing brainstorms)
- **logging** - Hooks-focused (full-fidelity session logging with 10+ hook events)
- **Schedule.md** - MCP server-focused (weekly schedule manager with web UI)
- **awareness** - Skills-focused (self-reflection and learning system)
- **agents/llms** - Reference frameworks for agent development

---

### Key Findings by Agent

#### Agent 1: Backlog.md Reference Implementation

The Backlog.md codebase (`resources/Backlog.md/`) is a **production-ready task management system** with:

| Component | Details |
|-----------|---------|
| **Data Model** | Tasks as markdown files with YAML frontmatter (id, title, status, assignee, labels, dependencies, AC) |
| **Task Hierarchies** | Parent-child relationships (`task-100` → `task-100.1`) |
| **Acceptance Criteria** | Structured checkboxes with `<!-- AC:BEGIN/END -->` markers |
| **MCP Server** | Full tool suite: `task_create`, `task_list`, `task_view`, `task_edit`, `task_archive`, `task_search` |
| **MCP Resources** | Read-only guides: `backlog://workflow/overview`, `backlog://task-creation` |
| **Web UI** | React + Bun.serve + WebSocket for real-time Kanban board |
| **CLI** | Commander.js with 20+ commands (init, task CRUD, board, search) |
| **Tech Stack** | Bun, TypeScript, gray-matter, neo-neo-bblessed (TUI) |

#### Agent 2: Schedule.md Plugin Architecture

The Schedule.md plugin provides a **reusable template** for MCP-based plugins:

```
.claude-plugin/plugin.json    # Manifest with mcpServers reference
.mcp.json                     # MCP server configuration
src/
├── core/schedule.ts          # Business logic class
├── mcp/server.ts             # MCP stdio server
├── mcp/tools/blocks/         # Tool schemas & handlers
├── markdown/parser.ts        # YAML frontmatter parsing
├── server/index.ts           # HTTP + WebSocket server
└── web/App.tsx               # React components
```

**Key Patterns**:
- Plugin.json references `.mcp.json` for server config
- `${CLAUDE_PLUGIN_ROOT}` variable expansion
- Handlers wrap core class methods
- Output formatted as markdown for Claude readability
- File watcher broadcasts WebSocket updates

#### Agent 3: Plugin Ecosystem Patterns

Comprehensive analysis of the plugin system:

| Pattern | Implementation |
|---------|---------------|
| **Commands** | Markdown files with YAML frontmatter, `/command` invocation |
| **Skills** | `SKILL.md` with description triggers, `allowed-tools` restrictions |
| **Hooks** | Python scripts receiving JSON on stdin, 10+ event types |
| **MCP Servers** | `.mcp.json` with command/args/env configuration |

**Plugin Manifest Fields**:
```json
{
  "name": "plugin-name",
  "version": "1.0.0", 
  "description": "What it does",
  "commands": ["./commands/"],
  "skills": ["./skills/"],
  "hooks": { "SessionStart": [...] },
  "mcpServers": "./.mcp.json"
}
```

---

### Prerequisites for Backlog Plugin

Based on the research, implementing a Backlog.md plugin requires:

#### 1. **Core Architecture**
- TypeScript project with Bun runtime
- Shared `Core` class for task CRUD operations
- Markdown parser/serializer using `gray-matter`
- Content store with file watchers

#### 2. **MCP Server**
- StdioServerTransport from `@modelcontextprotocol/sdk`
- Tool schemas with Zod validation
- Resources for workflow guides
- Handler classes wrapping Core methods

#### 3. **Data Model**
```yaml
# Task file format
---
id: task-42
title: "Feature Implementation"
status: "In Progress"
assignee: ["@user"]
labels: ["feature"]
dependencies: ["task-41"]
---

## Description
...

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Criterion text
<!-- AC:END -->
```

#### 4. **Plugin Structure**
```
plugins/backlog/
├── .claude-plugin/plugin.json
├── .mcp.json
├── CLAUDE.md
├── src/
│   ├── core/backlog.ts
│   ├── mcp/server.ts
│   ├── mcp/tools/tasks/
│   ├── markdown/parser.ts
│   └── types/index.ts
├── commands/backlog.md
└── skills/task-workflow/SKILL.md
```

#### 5. **MCP Tools to Implement**
- `task_create` - Create new task
- `task_list` - List with filters (status, assignee, labels)
- `task_view` - Get task details
- `task_edit` - Update task fields
- `task_archive` - Move to completed
- `task_search` - Full-text search
- `backlog_init` - Initialize project

#### 6. **Key Dependencies**
```json
{
  "@modelcontextprotocol/sdk": "^1.0.0",
  "commander": "^14.0.0",
  "gray-matter": "^4.0.3",
  "zod": "^3.23.0"
}
```

---

### Recommended Next Steps

1. **Create plugin scaffold** with `.claude-plugin/plugin.json` and `.mcp.json`
2. **Port Core class** from Backlog.md reference (simplified version)
3. **Implement MCP server** with basic task tools
4. **Add markdown parsing** for task files
5. **Create slash command** for quick task operations
6. **Add skill** for AI-guided task workflow
