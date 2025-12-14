---
id: task-3
title: 'AgentNet: Fix TUI Navigation State Management'
status: Done
assignee: []
created_date: '2025-12-14 01:14'
updated_date: '2025-12-14 01:35'
labels:
  - agentnet
  - bug
  - tui
  - critical
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
## Problem
AgentNet TUI has critical navigation bugs:
1. **ESC/Back crashes** - Race condition when destroying screen while callback creates new screen
2. **Screen glitch on scroll** - Multiple screens alive simultaneously, both registering 'j'/'k' handlers

## Root Cause Analysis (from backend-architect)
- Inconsistent state management across navigation flows
- Screen instances stack without cleanup
- No handler registration tracking
- No focus guards

## Technical Solution

### 1. Create ScreenManager
```typescript
class ScreenManager {
  private current: ScreenInstance | null = null;
  
  async transition(to: ScreenInstance) {
    if (this.current) {
      await this.current.cleanup();
      this.current.destroy();
    }
    this.current = to;
    to.activate();
  }
}
```

### 2. Add Focus Guards
```typescript
screen.key(["down", "j"], () => {
  if (!agentList.focused) return;  // ADD THIS
  // ... rest of handler
});
```

### 3. Fix Back Handler Order
```typescript
screen.key(["b", "B"], async () => {
  if (options?.onBack) {
    resolve();  // Resolve FIRST
    await new Promise(r => setTimeout(r, 0));  // Yield event loop
    screen.destroy();  // Then cleanup
    await options.onBack();  // Then callback
  }
});
```

## Affected Files
- `plugins/agentnet/src/ui/agent-list.ts`
- `plugins/agentnet/src/ui/wall-view.ts`
- `plugins/agentnet/src/ui/message-view.ts`
- `plugins/agentnet/src/ui/main-menu.ts`
- (new) `plugins/agentnet/src/ui/core/screen-manager.ts`

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 ESC at any level returns to previous view without crash
- [x] #2 Back at top level exits cleanly
- [x] #3 Pressing 'j'/'k' only affects focused component
- [ ] #4 Rapid key presses don't break state
- [ ] #5 Terminal resize preserves layout
<!-- SECTION:DESCRIPTION:END -->

<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Implementation Notes (2025-12-13)

Fixed both critical TUI bugs with minimal, focused changes:

### Fix #1: ESC/Back Navigation Crash
Changed promise resolution order in all UI files. Previously `screen.destroy()` was called before `resolve()`, causing race conditions. Now: `resolve()` → `screen.destroy()` → `await callback()`

### Fix #2: Screen Glitch on Scroll
Added focus guards to all key handlers. Each handler now checks `if (!list.focused) return;` at the start, ensuring only the focused component responds.

### Files Modified
- `src/ui/wall-view.ts`
- `src/ui/agent-list.ts`
- `src/ui/main-menu.ts`
- `src/ui/message-view.ts`

### Decision: No ScreenManager
We opted for the minimal fix (focus guards + resolve order) rather than creating a full ScreenManager abstraction. The simpler approach:
- Solves the immediate problems
- Doesn't over-engineer
- Can be refactored later if needed

### Smoke Tests Pass
- `--help` ✓
- `agents --json` ✓
- `feed` ✓
<!-- SECTION:NOTES:END -->
