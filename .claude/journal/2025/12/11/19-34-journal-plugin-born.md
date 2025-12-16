---
created: 2025-12-11T19:34:00
author: claude-opus-4
description: The journal plugin is created with Obsidian-style linked documents
parent_daily: [[2025-12-11]]
tags: [plugin, journal, obsidian, wikilinks, memory]
related:
  - "[[plugins/journal]]"
---

# Journal Plugin Born

## Event

```
git commit -m "feat(journal): Add Obsidian-style linked journal plugin"
```

## The Vision

A journaling system that treats knowledge as a graph:
- Wikilinks connect ideas ([[related-topic]])
- Temporal organization (daily → weekly → monthly → yearly)
- Atomic-first model (small entries synthesize into larger views)
- Full Obsidian compatibility

## Architecture

```
plugins/journal/skills/
├── journal-writer/    # Create atomic entries
├── journal-browser/   # Navigate and search
├── journal-reflector/ # Generate reflections
├── journal-linker/    # Build connections
├── journal-planner/   # Future-facing entries
└── journal-aggregator/# Roll up to summaries
```

## The /journal Command

```markdown
/journal [daily|plan|reflect|browse|today|note <title>]
```

## Key Decisions

1. **Wikilinks as edges** - Links ARE the knowledge graph
2. **Atomic-first** - Small entries are primary truth
3. **Temporal hierarchy** - Time organizes everything
4. **Human-readable** - Markdown, always

## Significance

This plugin would become the ecosystem's **temporal memory cortex**:
- Where observations are recorded
- Where patterns emerge from atomics
- Where personas contribute (author attribution)
- Where the past becomes queryable

The journal plugin embodied "The Scribe" persona - patient documenter of everything.

---

*Parent: [[2025-12-11]] → [[2025-12]] → [[2025]]*
