---
name: task-workflow
description: Guide task-driven development with Backlog.md. Use when the user asks to work on a task, implement a feature, fix a bug, or when structured work tracking would help. Handles task creation, progress tracking, acceptance criteria management, and completion workflows.
allowed-tools: task_create, task_list, task_view, task_edit, task_search, task_archive, backlog_init, backlog_overview, Read, Glob, Grep, Edit, Write, Bash
---

# Task Workflow Skill

Guide users through structured, task-driven development using Backlog.md.

## When to Use

Invoke this skill when:
- User asks to "work on task X" or "implement feature Y"
- User wants to track progress on multi-step work
- User asks about current tasks or project status
- Work would benefit from acceptance criteria and progress tracking
- User mentions "backlog", "task", or "ticket"

## Workflow Phases

### Phase 1: Task Discovery

Before starting work, understand the context:

1. **Check for existing task**:
   ```
   task_search query="[feature/bug description]"
   ```

2. **If task exists**: Load it and review
   ```
   task_view id="task-42"
   ```

3. **If no task exists**: Decide if one should be created
   - Multi-step work? Create task
   - Clear deliverables? Create task
   - Quick fix? Maybe skip

### Phase 2: Task Setup

When creating or preparing a task:

1. **Create with clear scope**:
   ```
   task_create
     title="Implement OAuth authentication"
     description="Add OAuth 2.0 support for Google and GitHub providers"
     acceptanceCriteria=[
       "User can sign in with Google",
       "User can sign in with GitHub",
       "Tokens refresh automatically",
       "Logout clears all sessions"
     ]
     labels=["auth", "feature"]
     priority="high"
   ```

2. **Mark as in-progress**:
   ```
   task_edit id="task-42" status="In Progress" assignee=["@claude"]
   ```

### Phase 3: Implementation

During implementation:

1. **Work incrementally**: Focus on one acceptance criterion at a time

2. **Check off progress**: As criteria are met
   ```
   task_edit id="task-42" checkAc=[1]
   ```

3. **Add implementation notes**: Document decisions
   ```
   task_edit id="task-42" implementationNotes="Using passport.js with Redis session store. Tokens have 24h TTL."
   ```

4. **Handle blockers**: If stuck, update notes with blocker info

### Phase 4: Completion

When finishing a task:

1. **Verify all AC complete**: Review acceptance criteria
   ```
   task_view id="task-42"
   ```

2. **Add final notes**: Summarize implementation
   ```
   task_edit id="task-42"
     status="Done"
     implementationNotes="Completed OAuth implementation. Used passport.js with strategies for Google and GitHub. Sessions stored in Redis."
   ```

3. **Archive if appropriate**:
   ```
   task_archive id="task-42"
   ```

## Breaking Down Large Tasks

For complex work, create subtasks:

1. **Create parent task**:
   ```
   task_create title="Major Feature X" ...
   ```

2. **Create subtasks with parent reference**:
   ```
   task_create
     title="Backend API for Feature X"
     parentTaskId="task-100"
     ...
   ```

Subtasks get IDs like `task-100.1`, `task-100.2`.

## Handling Dependencies

When tasks depend on others:

1. **Declare dependencies**:
   ```
   task_create
     title="Frontend UI"
     dependencies=["task-101", "task-102"]
     ...
   ```

2. **Check dependency status before starting**:
   ```
   task_view id="task-101"
   task_view id="task-102"
   ```

## Session Management

### Starting a Session

1. Check for in-progress tasks:
   ```
   task_list status="In Progress"
   ```

2. Review context from implementation notes

3. Continue from last checkpoint

### Ending a Session

1. Update task with current state:
   ```
   task_edit id="task-42"
     implementationNotes="[Previous notes]\n\nSession update: Completed steps 1-3. Next: implement token refresh."
   ```

2. Note any blockers or questions

## Best Practices

1. **Search before creating** - Avoid duplicate tasks

2. **Write testable AC** - Each criterion should be verifiable

3. **Update status promptly** - Keep the backlog accurate

4. **Document as you go** - Future sessions depend on notes

5. **Keep tasks focused** - One clear deliverable per task

6. **Use labels consistently** - Enables filtering and organization

## Example Conversations

**User**: "Let's implement user authentication"

**Response**:
1. Search for existing auth tasks
2. If none, propose creating a task with AC
3. Get user approval on scope
4. Create task and mark in-progress
5. Begin implementation, checking off AC as completed

**User**: "What am I working on?"

**Response**:
1. List in-progress tasks
2. Show acceptance criteria progress
3. Summarize implementation notes
4. Suggest next steps

**User**: "Mark the auth task as done"

**Response**:
1. View task to confirm all AC complete
2. If incomplete, highlight remaining items
3. If complete, update status and add final notes
4. Offer to archive
