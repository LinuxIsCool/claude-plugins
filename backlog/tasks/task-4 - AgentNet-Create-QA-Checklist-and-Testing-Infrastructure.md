---
id: task-4
title: 'AgentNet: Create QA Checklist and Testing Infrastructure'
status: To Do
assignee: []
created_date: '2025-12-14 01:14'
updated_date: '2025-12-14 01:21'
labels:
  - agentnet
  - qa
  - process
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Context
From process-cartographer: "A 2-minute checklist catches 90% of issues."

AgentNet needs manual QA validation before releases to catch TUI-specific bugs that automated tests miss.

## Deliverables

### 1. QA Checklist (plugins/agentnet/QA.md)
- Smoke tests: sync, agents, navigation
- Navigation edge cases: ESC at top, back at top, rapid keys
- Data edge cases: empty dirs, no agents, malformed YAML
- Integration: project agents, plugin agents, wall posts
- Regression tests: track fixed issues

### 2. CHANGELOG.md
- Track all changes
- SemVer versioning
- Link to issues

### 3. Issue Templates
- backlog/issues/agentnet/_template.md
- Structured format: repro steps, expected, actual, environment

### 4. Development Workflow Documentation
- Commit message guidelines
- Manual test before commit
- Update QA regression section for each fix

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 QA.md exists and covers all navigation flows
- [ ] #2 CHANGELOG.md exists with current version
- [ ] #3 Issue template captures all needed info
- [ ] #4 README has "Development" section
<!-- SECTION:DESCRIPTION:END -->

<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2025-12-14: Created QA.md with comprehensive checklist covering all views, navigation flows, known bugs (#1 ESC crash, #2 scroll glitch), edge cases, and test session template.
<!-- SECTION:NOTES:END -->
