---
id: msg_FunPCBWMeYoUAsZs7FBUWVHU7Fj9VieN
kind: 103
account_id: claude
created_at: 1765509805407
imported_at: 1766005509037
author_name: Claude
thread_id: cc_5fa98c28
platform: claude-code
session_id: 5fa98c28-a3c8-49b3-965a-8f9e399efb65
tags: [["event_type","AssistantResponse"]]
---

You're right - that's a much cleaner approach. The Backlog.md package is already a complete, production-ready system with built-in MCP support. The plugin should just integrate it, not reimplement it.

Let me revise the prerequisites:

---

## Revised: Backlog.md Plugin as Integration Layer

### What the Plugin Actually Needs

The plugin becomes a **thin integration layer** that:

1. **Declares backlog.md as a dependency** (`bun add backlog.md`)
2. **Configures the MCP server** (points to `backlog mcp start`)
3. **Adds Claude Code-specific enhancements**:
   - Commands for common workflows
   - Skills for task-driven development
   - CLAUDE.md with agent instructions

### Minimal Plugin Structure

```
plugins/backlog/
├── .claude-plugin/
│   └── plugin.json
├── .mcp.json              # Points to backlog mcp start
├── CLAUDE.md              # Instructions for using backlog tools
├── package.json           # Depends on backlog.md
├── commands/
│   └── backlog.md         # Slash command for quick access
└── skills/
    └── task-workflow/
        └── SKILL.md       # Skill for AI-guided task execution
```

### Key Configuration Files

**`.mcp.json`**:
```json
{
  "mcpServers": {
    "backlog": {
      "command": "npx",
      "args": ["backlog.md", "mcp", "start"],
      "env": {}
    }
  }
}
```

**`package.json`**:
```json
{
  "name": "backlog-plugin",
  "version": "0.1.0",
  "dependencies": {
    "backlog.md": "^1.27.0"
  }
}
```

### Prerequisites Simplified

| Prerequisite | Status |
|-------------|--------|
| Backlog.md package | Already exists (`npm i -g backlog.md`) |
| MCP server | Built into backlog.md (`backlog mcp start`) |
| Task tools | Already implemented in backlog.md |
| Data model | Already defined (markdown + YAML frontmatter) |

### What Actually Needs to Be Built

1. **Plugin manifest** - Register with marketplace
2. **MCP configuration** - Point to backlog CLI
3. **CLAUDE.md** - Detailed agent instructions for using backlog tools effectively
4. **Commands** - Slash commands for common operations (`/backlog`, `/task`)
5. **Skills** - Task-driven development workflow, planning patterns
6. **Hooks** (optional) - Auto-log task progress, session awareness

### Value-Add from Plugin Layer

The plugin adds Claude Code-specific intelligence:

- **Workflow guidance** - When to create tasks vs subtasks
- **Status conventions** - How to progress tasks through workflow
- **AC management** - Best practices for acceptance criteria
- **Integration patterns** - Using backlog with other plugins (logging, schedule)
- **Slash commands** - Quick access without remembering tool names

This approach is cleaner, more maintainable, and leverages the existing well-tested implementation.
