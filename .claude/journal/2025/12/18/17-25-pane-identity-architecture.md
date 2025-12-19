---
id: 2025-12-18-1725
title: "Pane Identity Architecture: Solving Multi-Instance Session Resolution"
type: atomic
created: 2025-12-18T17:25:43
author: claude-opus-4.5
description: "Architectural fix for agent-finder showing duplicate data by implementing pane-to-session identity tracking"
tags: [architecture, statusline, tmux, multi-instance, bug-fix, session-resolution]
parent_daily: [[2025-12-18]]
related:
  - [[17-46-statusline-elegance-and-identity]]
---

# Pane Identity Architecture: Solving Multi-Instance Session Resolution

Today I tackled a fundamental architectural flaw in the agent-finder's session resolution system. What initially appeared as two simple bugs revealed a deeper design issue with multi-instance Claude coordination.

## Context

The user reported two issues with the recently-implemented statusline integration for the tmux agent-finder:
1. **Duplicate data**: All selection options showed the same session information
2. **Wrong order**: History displayed chronologically instead of reverse-chronologically

Rather than patching symptoms, the user asked for holistic analysis: *"What are the root causes? Is there a way to have cleaner code that prevents these bugs?"*

## The Discovery

After thorough investigation using the Explore agent and manual testing, I identified the root causes:

### Bug 1: CWD-Based Resolution is Fundamentally Lossy

The system was designed for single-Claude usage. The session resolver worked by:
1. Get the tmux pane's working directory
2. Search registry.json for a session with matching CWD
3. Return the most recent match

**The flaw**: Multiple Claude sessions can run in the same directory tree. When 5 panes all have CWD `/home/user/project`, they all resolve to the same session—the most recent one. There's no way to distinguish which pane belongs to which session using CWD alone.

### Bug 2: Pipeline Ordering Oversight

The history function used `sort | tail -N | while...` which:
- Sorts ascending by timestamp
- Takes the last N (most recent)
- Iterates in that order (oldest of N first)

Simple fix: `sort -r | head -N` instead.

## The Solution: Direct Pane Identity Tracking

I implemented a process ancestry approach:

```
Claude session starts
    ↓
session-start.sh hook runs
    ↓
Walk process tree: bash → claude → fish → tmux
    ↓
Match ancestor PID against tmux pane PIDs
    ↓
Store pane_id (%44) and pane_ref (0:5.0) in registry
```

Now each session has a direct link to its tmux pane, enabling precise resolution.

## Files Created/Modified

| File | Purpose |
|------|---------|
| `lib/pane-identity.sh` | **NEW** - Process ancestry walking |
| `hooks/session-start.sh` | Store pane_id on registration |
| `lib/session-resolver.sh` | Two-stage: pane_id first, CWD fallback |
| `lib/statusline-history.sh` | Reverse chronological ordering |

## Architectural Insight

The key insight was recognizing that **CWD is a location, not an identity**. Multiple processes can share a location, but each tmux pane has a unique process tree. By walking up the process ancestry until we hit a tmux pane PID, we establish identity rather than just location.

This pattern—using process hierarchy for identity—could apply to other multi-instance coordination challenges.

## Current Limitation

Existing sessions don't have pane_id (started before tracking existed). They'll continue using CWD fallback until restarted. New sessions automatically get pane identity.

## Insights

The user's request for "holistic analysis" led to discovering a design flaw rather than just a coding bug. The lesson: when symptoms suggest the wrong abstraction, investigate the abstraction rather than patching symptoms.

---

*Parent: [[2025-12-18]]*
