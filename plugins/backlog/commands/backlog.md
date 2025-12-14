---
description: Show backlog overview and help manage tasks
---

# Backlog Command

Show the project's task backlog status and help the user manage their tasks.

## Instructions

1. **Check Initialization**: First, try to list tasks using `task_list`. If this fails with an init error, guide the user to initialize with `backlog_init`.

2. **Show Overview**: If initialized, provide a summary:
   - Count of tasks by status (To Do, In Progress, Done)
   - Any tasks currently assigned or in progress
   - Recent activity if available

3. **In-Progress Tasks**: Highlight any tasks marked "In Progress" - these are the current focus.

4. **Offer Actions**: Based on the state, offer to help with:
   - **If tasks exist**: View details, update status, search tasks
   - **If no tasks**: Create first task, explain the workflow
   - **If many completed**: Suggest archiving old tasks

5. **Quick Commands**: Remind the user of common operations:
   - Create task: "Create a task for [description]"
   - View task: "Show me task 42"
   - Update status: "Mark task 42 as done"
   - Search: "Find tasks about authentication"

## Output Format

Present information clearly with:
- Task counts by status
- List of in-progress tasks (if any)
- Suggested next actions

If the backlog is not initialized, explain what Backlog.md is and offer to set it up.
