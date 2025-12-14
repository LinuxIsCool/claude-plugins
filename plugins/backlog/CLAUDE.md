# Backlog.md - Agent Instructions

You have access to Backlog.md, a markdown-native task management system designed for AI-assisted development.

## Getting Started

**CRITICAL**: Before creating tasks or managing work, read the workflow overview:

```
Read MCP resource: backlog://workflow/overview
```

This resource contains:
- Decision framework for when to create tasks
- Search-first workflow to avoid duplicates
- Task creation, execution, and completion guides
- Complete MCP tools reference

## Quick Reference

### When to Create Tasks

Create tasks when work:
- Takes more than a few minutes
- Has clear deliverables or acceptance criteria
- Needs to be tracked across sessions
- Benefits from structured planning

**Don't create tasks for**:
- Quick fixes or one-liners
- Exploratory research
- Simple questions

### Core Workflow

1. **Search First**: Before creating, search for existing tasks
   ```
   task_search query="feature name"
   ```

2. **Create with Context**: Include description and acceptance criteria
   ```
   task_create title="Implement feature X" description="..." acceptanceCriteria=["Criterion 1", "Criterion 2"]
   ```

3. **Track Progress**: Update status as you work
   ```
   task_edit id="task-42" status="In Progress"
   ```

4. **Complete with Notes**: Add implementation notes before closing
   ```
   task_edit id="task-42" status="Done" implementationNotes="Implemented using..."
   ```

## Available MCP Tools

### Task Management
| Tool | Purpose |
|------|---------|
| `task_create` | Create a new task with title, description, AC |
| `task_list` | List tasks with filters (status, assignee, labels) |
| `task_view` | View full task details |
| `task_edit` | Update task fields (status, description, AC, notes) |
| `task_archive` | Move completed task to archive |
| `task_search` | Full-text search across all tasks |

### Documents & Decisions
| Tool | Purpose |
|------|---------|
| `document_create` | Create documentation |
| `document_list` | List all documents |
| `decision_create` | Create ADR-style decision record |
| `decision_list` | List all decisions |

### Project Management
| Tool | Purpose |
|------|---------|
| `backlog_init` | Initialize backlog in current project |
| `backlog_overview` | Get project statistics and summary |

### Workflow Guidance Tools
| Tool | Purpose |
|------|---------|
| `get_workflow_overview` | Overview of when/how to use Backlog.md |
| `get_task_creation_guide` | Scope assessment, acceptance criteria patterns |
| `get_task_execution_guide` | Planning, execution discipline, scope changes |
| `get_task_completion_guide` | Definition of Done, completion workflow |

## Task Edit Operations (Complete Reference)

The `task_edit` tool supports extensive field operations:

### Basic Fields
```
task_edit id="task-42"
  title="New title"
  description="New description"
  status="In Progress"
  priority="high"
  labels=["bug", "urgent"]
  assignee=["@claude"]
  dependencies=["task-40", "task-41"]
```

### Acceptance Criteria Management
```
# Replace all AC
task_edit id="task-42" acceptanceCriteriaSet=["AC 1", "AC 2", "AC 3"]

# Add new AC items
task_edit id="task-42" acceptanceCriteriaAdd=["New criterion"]

# Remove AC by index (1-based)
task_edit id="task-42" acceptanceCriteriaRemove=[2]

# Check/uncheck AC items (1-based indices)
task_edit id="task-42" acceptanceCriteriaCheck=[1, 3]
task_edit id="task-42" acceptanceCriteriaUncheck=[2]
```

### Implementation Plan
```
# Set entire plan (replaces all)
task_edit id="task-42" planSet="1. Research\n2. Implement\n3. Test"

# Append lines to plan
task_edit id="task-42" planAppend=["4. Deploy", "5. Monitor"]

# Clear plan entirely
task_edit id="task-42" planClear=true
```

### Implementation Notes
```
# Set notes (replaces all)
task_edit id="task-42" notesSet="Started implementation..."

# Append to notes (preserves existing)
task_edit id="task-42" notesAppend=["Session 2: Completed auth flow", "Session 3: Added tests"]

# Clear notes
task_edit id="task-42" notesClear=true
```

## MCP Resources

Read-only guides available via MCP resources:

| Resource URI | Content |
|-------------|---------|
| `backlog://workflow/overview` | Complete workflow guide |
| `backlog://workflow/task-creation` | Task creation patterns |
| `backlog://workflow/task-execution` | Implementation workflow |
| `backlog://init-required` | Setup instructions |

## Task Data Model

Tasks are stored as markdown files with YAML frontmatter:

```markdown
---
id: task-42
title: "Implement OAuth"
status: "In Progress"
assignee: ["@claude"]
labels: ["auth", "backend"]
priority: "high"
dependencies: ["task-41"]
---

## Description
Implement OAuth 2.0 authentication...

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 OAuth provider configured
- [ ] #2 Token refresh working
- [x] #3 Tests written
<!-- AC:END -->

## Implementation Notes
Started with provider setup...
```

### Status Values
Default statuses: `To Do`, `In Progress`, `Done`
(Configurable per project in `backlog/config.yml`)

### Task Hierarchies
- Parent tasks: `task-100`
- Subtasks: `task-100.1`, `task-100.2`

Use `parentTaskId` when creating subtasks to establish hierarchy.

## Best Practices

### 1. Always Search First
Before creating a task, search to avoid duplicates:
```
task_search query="oauth implementation"
```

### 2. Write Clear Acceptance Criteria
Good AC is:
- Specific and measurable
- Testable
- Independent of implementation details

```
acceptanceCriteria=[
  "User can login with Google OAuth",
  "Refresh tokens persist across sessions",
  "Invalid tokens show appropriate error"
]
```

### 3. Update Status Promptly
Mark tasks `In Progress` when starting:
```
task_edit id="task-42" status="In Progress" assignee=["@claude"]
```

### 4. Add Implementation Notes
Document decisions and approach as you work:
```
task_edit id="task-42" implementationNotes="Used passport.js for OAuth. Tokens stored in Redis with 24h TTL."
```

### 5. Check Off Acceptance Criteria
Mark AC items as you complete them:
```
task_edit id="task-42" checkAc=[1, 3]
```

### 6. Archive When Done
Move completed tasks to keep the active list clean:
```
task_archive id="task-42"
```

## Integration with Claude Code

### Starting a Session
1. Check for in-progress tasks: `task_list status="In Progress"`
2. Review task details before resuming work
3. Update notes with session context

### Ending a Session
1. Update task status and notes
2. List remaining acceptance criteria
3. Note any blockers or next steps

### Multi-Session Work
For work spanning multiple sessions:
- Use implementation notes to maintain context
- Check acceptance criteria for progress
- Update status to reflect current state

## File Structure

When initialized, creates:
```
backlog/
├── config.yml          # Project configuration
├── tasks/              # Active tasks
├── drafts/             # Work-in-progress tasks
├── completed/          # Archived tasks
├── docs/               # Documentation
├── decisions/          # Decision records
└── milestones/         # Milestone organization
```

## CLI Fallback

If MCP tools are unavailable, use CLI commands:
```bash
npx backlog.md task list
npx backlog.md task create "Title"
npx backlog.md task edit 42 --status "In Progress"
npx backlog.md board  # Interactive Kanban board
npx backlog.md browser  # Web UI at localhost:6420
```

## Initialization

To initialize backlog in a new project:
```
backlog_init projectName="My Project"
```

Or via CLI:
```bash
npx backlog.md init "My Project"
```
