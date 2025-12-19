---
id: 2025-12-19-1105
title: "Statusline Plugin Bug Fixes"
type: atomic
created: 2025-12-19T11:05:00-08:00
author: claude-opus-4
description: "Fixed pane title cross-contamination and unified JSONL logging location"
tags: [statusline, bugfix, tmux, debugging]
parent_daily: [[2025-12-19]]
related: []
---

# Statusline Plugin Bug Fixes

Deep investigation and fixes for two interconnected bugs in the statusline plugin that were causing confusing behavior.

## Context

User reported that:
1. Description and summary sometimes weren't appearing
2. TMux pane titles showed weird values and changed based on which pane was focused
3. Pane titles sometimes showed command lines instead of the expected emoji + summary format

## Investigation Findings

### Bug 1: Pane Title Cross-Contamination

**Root Cause**: `statusline.sh` was calling `tmux display-message -p '#{pane_title}'` without specifying which pane to query. This returns the title of the *currently focused* pane, not necessarily the Claude session's pane.

**Evidence**:
- `$TMUX_PANE` was set to `%8` (correct Claude pane)
- But `tmux display-message -p '#{pane_id}'` returned `%11` (a fish shell pane)
- Pane %8 had correct title `"✳ Statusline & Pane Title Bugs"`
- Pane %11 showed the command line

**Fix**: Added `-t "$TMUX_PANE"` to target the correct pane explicitly.

### Bug 2: Dual Registry Locations

**Root Cause**: Hooks were writing to project-local registry (`.claude/instances/`) while JSONL logging was hardcoded to home (`~/.claude/instances/statusline.jsonl`). This fragmented data across locations.

**Evidence**:
- Project registry: 93 sessions, counter at 87
- Home registry: 36 sessions, counter at 70
- Same session existed in project but not home
- Debugging was confusing because logs didn't match registry

**Fix**: Made JSONL logging dynamic - it now uses the same directory as the registry, keeping all instance data together.

## Files Modified

| File | Change |
|------|--------|
| `tools/statusline.sh` | Added `-t "$TMUX_PANE"` for pane title, set STATUSLINE_LOG from registry |
| `hooks/session-start.sh` | Set STATUSLINE_LOG after finding registry |
| `hooks/user-prompt-submit.sh` | Set STATUSLINE_LOG after finding instances dir |
| `lib/statusline-utils.sh` | Added `get_instances_dir_for_cwd()` and `configure_statusline_paths()` |
| `lib/claude_backend.py` | Added `instances_dir` parameter to `log_statusline_event()` |
| `hooks/auto-identity.py` | Pass `instances_dir` to all logging calls |

## Insights

1. **TMux context matters**: When running commands in tmux, the "current" pane can differ from the calling context. Always be explicit with `-t` targeting.

2. **Single source of truth**: Splitting related data across locations creates debugging nightmares. All instance data (registry, summaries, descriptions, JSONL) should live together.

3. **The bugs were related**: Fixing bug 1 alone would have resolved the user's main complaint (weird pane titles), but bug 2 was important for maintainability.

---

*Parent: [[2025-12-19]]*
