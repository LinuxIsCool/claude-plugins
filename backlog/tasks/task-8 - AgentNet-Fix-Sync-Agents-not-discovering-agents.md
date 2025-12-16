---
id: task-8
title: 'AgentNet: Fix Sync Agents - not discovering agents'
status: Done
assignee: []
created_date: '2025-12-15 18:54'
updated_date: '2025-12-15 18:57'
labels:
  - agentnet
  - bug
  - core-feature
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Problem
Sync Agents is not discovering and syncing agent profiles from the project.

## To Investigate
- What paths is it searching?
- Is it finding .claude/agents/*.md files?
- Is it finding plugin agents?
- Is the store saving profiles correctly?

## Expected Behavior
- Discover agents from .claude/agents/
- Discover agents from plugins/*/agents/
- Create/update profiles in .claude/social/profiles/
- Report what was created/updated
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Discovers project agents from .claude/agents/
- [ ] #2 Discovers plugin agents from registered plugins
- [ ] #3 Creates profile files in .claude/social/profiles/
- [ ] #4 Reports created/updated counts accurately
- [ ] #5 Subsequent Browse Agents shows synced agents
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Fixed: Root detection logic was walking up incorrectly. Changed comparison from comparing to parent of start directory to comparing prev == current (filesystem root detection). CLI now auto-discovers project root by walking up from cwd to find .claude/agents/ or plugins/ directory.
<!-- SECTION:NOTES:END -->
