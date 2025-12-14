# Backlog Plugin for Claude Code

A Claude Code plugin that integrates [Backlog.md](https://github.com/MrLesk/Backlog.md) for AI-assisted task management.

## Overview

This plugin provides:
- **MCP Tools**: Full access to Backlog.md's task management tools
- **Slash Command**: `/backlog` for quick project overview
- **Task Workflow Skill**: AI-guided task-driven development

## Installation

1. Install the plugin in your Claude Code marketplace
2. The MCP server starts automatically via npx (no manual install needed)
3. Initialize backlog in your project: `npx backlog.md init "Project Name"`

Or via npm scripts:
```bash
npm run init    # Initialize backlog
npm run serve   # Start web UI at localhost:6420
npm run mcp     # Start MCP server manually
```

## Usage

### Via MCP Tools

The plugin exposes Backlog.md's MCP server with tools for:
- `task_create`, `task_list`, `task_view`, `task_edit`, `task_search`, `task_archive`
- `document_create`, `document_list`, `decision_create`, `decision_list`
- `backlog_init`, `backlog_overview`

### Via Slash Command

```
/backlog
```

Shows project overview with task counts and in-progress work.

### Via Skill (Auto-Invoked)

The `task-workflow` skill activates when you:
- Ask to work on a task or implement a feature
- Request progress tracking
- Mention "backlog", "task", or "ticket"

## Features

- **Markdown-native**: Tasks stored as readable markdown files
- **Acceptance Criteria**: Track completion with checkboxes
- **Task Hierarchies**: Parent tasks with subtasks
- **Dependencies**: Declare task dependencies
- **Labels & Priorities**: Organize and filter tasks
- **Web UI**: Visual Kanban board at localhost:6420

## File Structure

When initialized, creates:
```
backlog/
├── config.yml     # Project settings
├── tasks/         # Active tasks
├── drafts/        # Work-in-progress
├── completed/     # Archived tasks
├── docs/          # Documentation
└── decisions/     # Decision records
```

## Configuration

Edit `backlog/config.yml` to customize:
- Status values (default: To Do, In Progress, Done)
- Labels and milestones
- Date format
- Auto-commit behavior

## Links

- [Backlog.md Documentation](https://github.com/MrLesk/Backlog.md)
- [MCP Tools Reference](https://github.com/MrLesk/Backlog.md#mcp-integration)
