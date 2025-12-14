---
id: task-3
title: 'AgentNet: Fix TUI Navigation State Management'
status: To Do
assignee: []
created_date: '2025-12-14 01:14'
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
- [ ] ESC at any level returns to previous view without crash
- [ ] Back at top level exits cleanly
- [ ] Pressing 'j'/'k' only affects focused component
- [ ] Rapid key presses don't break state
- [ ] Terminal resize preserves layout
<!-- SECTION:DESCRIPTION:END -->
