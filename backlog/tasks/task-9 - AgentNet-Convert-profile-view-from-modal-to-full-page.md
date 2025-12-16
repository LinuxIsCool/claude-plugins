---
id: task-9
title: 'AgentNet: Convert profile view from modal to full page'
status: Done
assignee: []
created_date: '2025-12-15 18:54'
updated_date: '2025-12-15 19:00'
labels:
  - agentnet
  - enhancement
  - ux
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Current Behavior
Agent profile is shown as a modal/popup overlay on the agent list.

## Desired Behavior
Profile should be a full-screen scrollable page with:
- Complete agent information
- Full description (scrollable)
- Stats section
- Actions (View Wall, Message, Back)

## Benefits
- Better readability for long descriptions
- More space for agent details
- Consistent navigation pattern (full screens, not modals)
- Better keyboard navigation
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Profile view takes full screen
- [ ] #2 Content is scrollable with j/k or arrow keys
- [ ] #3 Shows all agent info: ID, role, model, source, description, stats
- [ ] #4 Footer shows available actions: W=Wall, M=Message, B/ESC=Back
- [ ] #5 Back returns to agent list
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Converted profile view from popup/modal to full-page scrollable view. Now has: header with avatar/name/role, bordered content area with stats and description, footer with keybindings (scroll, view wall, message, back, quit). Kept popup version for quick-view from agent list (Enter). The profile command now shows TUI for TTY and plain text for non-TTY.
<!-- SECTION:NOTES:END -->
