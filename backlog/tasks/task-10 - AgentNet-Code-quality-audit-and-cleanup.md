---
id: task-10
title: 'AgentNet: Code quality audit and cleanup'
status: To Do
assignee: []
created_date: '2025-12-15 18:54'
labels:
  - agentnet
  - tech-debt
  - quality
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Goals
- Reliable and maintainable codebase
- Clean code with minimal lines
- Maximum feature coverage
- Great user experience

## Areas to Review
1. **DRY violations** - repeated patterns across UI files
2. **Screen lifecycle** - ensure consistent create/destroy/focus patterns
3. **Error handling** - graceful failures, user-friendly messages
4. **Code organization** - clear separation of concerns
5. **Type safety** - proper TypeScript usage

## Potential Refactors
- Extract common TUI patterns to shared utilities
- Consolidate key handler registration
- Standardize popup/fullscreen view patterns
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 No duplicate code patterns across UI files
- [ ] #2 Consistent screen lifecycle management
- [ ] #3 All errors show user-friendly messages
- [ ] #4 TypeScript strict mode passes
- [ ] #5 Code is well-documented where non-obvious
<!-- AC:END -->
