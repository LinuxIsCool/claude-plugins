---
id: task-6
title: 'AgentNet: Fix Global Feed - not displaying posts'
status: Done
assignee: []
created_date: '2025-12-15 18:54'
updated_date: '2025-12-15 18:58'
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
Global Feed menu option is not working - posts are not being displayed.

## To Investigate
- Is the feed fetching data correctly from store?
- Are there posts in the system to display?
- Is the TUI rendering correctly?
- Console output vs TUI mode behavior

## Expected Behavior
- Show aggregated posts from all agents
- Display with author, timestamp, content preview
- Navigate/scroll through posts
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Global Feed displays posts when posts exist
- [ ] #2 Shows 'No posts yet' message when empty
- [ ] #3 Posts show author avatar, name, timestamp, content
- [ ] #4 Works in both TUI and non-TTY modes
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Fixed two issues: (1) Root detection bug - same as task-8. (2) YAML serialization bug - titles with colons were not quoted, causing YAML parse errors. Added yamlString() helper to properly quote strings with special characters. Also fixed existing corrupted post files.
<!-- SECTION:NOTES:END -->
