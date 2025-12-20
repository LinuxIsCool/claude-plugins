---
id: 2025-12-19-1400
title: "tmux Window Identity Command"
type: atomic
created: 2025-12-19T14:00:00-08:00
author: Sigil
description: "Created /statusline:rename command for opt-in tmux window naming"
tags: [statusline, tmux, identity, feature]
parent_daily: [[2025-12-19]]
related: []
---

# tmux Window Identity Command

Created `/statusline:rename` command to solve the "all windows named claude" problem.

## The Problem

When running multiple Claude instances in tmux, all windows show `x:claude` because tmux's `automatic-rename` uses `pane_current_command`. With 4+ Claude sessions open, they're indistinguishable:

```
1:claude  2:claude  3:claude  4:claude
```

The user wanted window names to reflect agent identity: `Sigil:C124`, `Tuner:C123`, etc.

## Discovery: The Conflict

tmux's `automatic-rename` constantly overwrites window names with the running command. Testing revealed:

1. `tmux rename-window "Sigil:C124"` works immediately
2. With `automatic-rename on`, tmux overwrites it back to "claude" within seconds
3. Must disable `automatic-rename` per-window for custom names to persist

This creates a trade-off: custom names require opting out of tmux's automatic naming.

## Solution: Opt-in Command

Rather than automatically fighting with tmux (side effects on all windows), created an explicit command:

| Command | Effect |
|---------|--------|
| `/statusline:rename` | Set window to registered identity (e.g., "Sigil:C124") |
| `/statusline:rename Spark` | Set window to custom name |
| `/statusline:rename reset` | Restore automatic naming |

The command:
1. Reads session identity from `.claude/instances/registry.json`
2. Builds window name as `Name:CXXX` format
3. Calls `tmux rename-window`
4. Disables `automatic-rename` for that window only

## Key Insight

The statusline plugin already tracks everything needed:
- `process_number` (C124, C125, etc.) - spawn order
- `name` (Sigil, Tuner, etc.) - self-assigned identity
- `pane_id` (%32, etc.) - for targeting specific windows

The gap was just connecting these to tmux's window naming API.

## Files Changed

- `plugins/statusline/commands/rename.md` - new command

---

*Parent: [[2025-12-19]]*
