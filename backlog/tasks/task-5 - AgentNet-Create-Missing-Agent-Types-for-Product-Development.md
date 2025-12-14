---
id: task-5
title: 'AgentNet: Create Missing Agent Types for Product Development'
status: To Do
assignee: []
created_date: '2025-12-14 01:14'
updated_date: '2025-12-14 01:23'
labels:
  - agentnet
  - agents
  - infrastructure
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Context
From agent-architect's gap analysis, we need specialized agents for sustainable product development.

## Missing Agent Categories

### Engineering Team (Priority)
- `frontend-engineer` - UI/UX implementation
- `api-designer` - Contract design
- `tui-specialist` - Terminal UI expertise (blessed/neo-bblessed)

### Design Team
- `ux-designer` - User flows, interaction design
- `product-designer` - Feature scoping, design thinking

### Testing Team (Critical)
- `qa-engineer` - Manual testing, bug reproduction
- `test-strategist` - Test planning, coverage analysis
- `tui-tester` - TUI-specific testing patterns

### Product Team
- `product-manager` - Roadmap, prioritization
- `tech-writer` - Documentation

## Agent Team Pattern
Create `.claude/agents/teams/` with team coordination:
- engineering:team-context.md
- testing:team-context.md
- design:team-context.md

## Priority Order
1. qa-engineer (catch bugs before users)
2. tui-specialist (blessed expertise)
3. product-designer (feature direction)

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 qa-engineer agent created
- [ ] #2 tui-specialist agent created
- [ ] #3 Agent team pattern documented
<!-- SECTION:DESCRIPTION:END -->

<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2025-12-14: Created qa-engineer agent at .claude/agents/qa-engineer.md. Agent includes TUI-specific testing guidance and explicit instruction to avoid time estimates. Note: Requires session restart to be discoverable via Task tool.

2025-12-14: Created agentnet:engineer plugin agent at plugins/agentnet/agents/engineer.md. Agent is responsible for developing and maintaining AgentNet on behalf of all agents. Includes TUI best practices, known issues, and explicit 'no time estimates' guidance. Updated plugin.json to include the agent.
<!-- SECTION:NOTES:END -->
