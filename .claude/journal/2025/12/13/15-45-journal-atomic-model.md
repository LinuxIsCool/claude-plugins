---
id: 2025-12-13-1545
title: "Journal Atomic Model"
type: atomic
created: 2025-12-13T15:45:00
author: claude-opus-4
description: "Redesigned journal plugin to atomic-first model with HH-MM-title naming and mandatory relational fields for DNA spiral graph effect"
tags: [journal, atomic, obsidian, graph, refactoring, zettelkasten]
parent_daily: [[2025-12-13]]
related:
  - [[15-30-process-cartographer-activated]]
  - [[14-30-subagent-exploration]]
---

# Journal Atomic Model

Restructured journal plugin around atomic-first principle with mandatory relational fields.

## Context

User clarified the journal plugin wasn't following intended design. Wanted atomic entries (HH-MM-title.md) as primary units, synthesized upward to daily → monthly → yearly summaries.

## The Core Principle

```
Atomic entries (PRIMARY)
    ↓ synthesize into
Daily summaries
    ↓ synthesize into
Monthly summaries
    ↓ synthesize into
Yearly summaries
```

**You don't write daily entries—you write atomics that get synthesized.**

## Mandatory Fields

| Field | Purpose | Example |
|-------|---------|---------|
| `created` | Timestamp | `2025-12-13T15:45:00` |
| `author` | Provenance | `claude-opus-4`, `user` |
| `description` | One-line summary | `"Redesigned journal..."` |
| `parent_daily` | Link UP | `[[2025-12-13]]` |
| `tags` | Categorization | `[journal, atomic]` |
| `related` | Horizontal links | `[[15-30-process-...]]` |

## The DNA Spiral Effect

When rendered in Obsidian's force-directed graph:

```
        ╭──── [[2025]] ────╮
       ╱                    ╲
[[2025-11]]              [[2025-12]]
    │                        │
    ├────────┬────────┤     ├────────┬────────┤
   [[12]]   [[13]]   [[14]] ...
     │╲      │╲
    ⚫ ⚫    ⚫ ⚫ ⚫
   atomics  atomics
```

Bidirectional links (child→parent, parent→child) create the spiral/helix structure.

## What Changed

Rewrote `plugins/journal/skills/journal-master/subskills/journal-writer.md`:
- Atomic template as PRIMARY
- Daily/monthly/yearly as SYNTHESIZED
- Relational field requirements
- DNA spiral visualization explanation
- Author field values table

## Insight

Structure enables emergence. The relational fields aren't bureaucracy—they're the connective tissue that creates meaning in the graph.

---
*Parent: [[2025-12-13]] → [[2025-12]] → [[2025]]*
