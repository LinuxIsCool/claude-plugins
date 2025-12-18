---
id: 2025-12-13-1615
title: "Bootstrapping Trajectory for Fresh Claude"
type: atomic
created: 2025-12-13T16:15:00
author: claude-opus-4
description: "Designed context-gathering trajectory for new Claude sessions; created .claude/README.md ecosystem orientation document"
tags: [meta, bootstrapping, continuity, orientation, knowledge-transfer]
parent_daily: [[2025-12-13]]
related:
  - [[16-00-historical-archaeology-process]]
  - [[15-15-agent-architecture-emerges]]
---

# Bootstrapping Trajectory for Fresh Claude

Addressed the fundamental question: How does a new Claude session gather context and continue work?

## The Problem

A fresh Claude starts with:
- Zero knowledge of this ecosystem
- Access to files (if given)
- CLAUDE.md as entry point
- Whatever the user tells them

Without guidance, they might:
- Read random files
- Miss the vision
- Not understand what's active vs dormant
- Duplicate completed work
- Lose architectural coherence

## The Solution: Layered Orientation

```
Session Start
     │
     ▼
CLAUDE.md
"New? Read .claude/README.md"
     │
     ▼
.claude/README.md (NEW)
├── 30-second context
├── First 5 minutes guide
├── Key directories
├── Active vs dormant
├── Continuation points
└── How to learn more
     │
     ├─► Agents → .claude/registry/agents.md
     ├─► Processes → .claude/registry/processes.md
     ├─► Recent work → .claude/journal/{date}
     └─► Vision → .claude/planning/
     │
     ▼
Oriented Claude
Ready to continue
```

## Artifacts Created

### .claude/README.md

The ecosystem orientation document containing:
- Vision summary ("Emergence beats design")
- First five minutes reading guide
- Directory map with purposes
- Active vs dormant components table
- Four continuation point options
- Journal system explanation
- Five core primitives
- Meta-layer diagram

### CLAUDE.md Update

Added "Ecosystem Orientation" section at top:
- Points to .claude/README.md
- Quick links to registries, journal, briefings

## The Ideal Trajectory

```
0-30s:  Read CLAUDE.md → see orientation pointer
30s-2m: Read .claude/README.md → understand vision, state
2-4m:   Read latest journal entry → know recent work
4-5m:   Read relevant registry → understand fleet/processes
5m+:    Begin informed continuation
```

## Key Insight

The ecosystem already had the pieces:
- Registries track agents and processes
- Journal provides temporal context
- Briefings give strategic direction
- Planning docs show evolution

What was missing: **A single entry point that routes to all of them.**

The `.claude/README.md` is that routing table for new sessions.

## Who Maintains This?

The README should be updated by:
- **process-cartographer** when processes change
- **agent-architect** when fleet changes
- **archivist** (when active) as overall coordinator

For now: manual updates when significant changes occur.

## Connection to Broader Vision

This addresses the "Context as Currency" primitive:
- Every token has cost
- Don't waste tokens on rediscovery
- Provide efficient paths to understanding

And "Metabolic Intelligence":
- The ecosystem should help new instances orient
- Self-documentation is a form of metabolism
- The system maintains its own coherence

---
*Parent: [[2025-12-13]]*
