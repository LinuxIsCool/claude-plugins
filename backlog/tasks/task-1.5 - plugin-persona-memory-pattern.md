---
id: task-1.5
title: "Define Memory Access Pattern for Plugin Personas"
status: "Done"
priority: high
labels: [memory, personas, architecture]
milestone: v1.0-activation
parentTaskId: task-1
created: 2025-12-15
assignee: ["@claude"]
---

# Define Memory Access Pattern for Plugin Personas

## Description

Plugin personas exist (11 catalogued in registry) but lack persistent memory across sessions. This task defines how plugin personas access and contribute to the ecosystem's memory systems.

### Current State

Plugin personas have:
- **Identity**: Via their SKILL.md files
- **Capabilities**: Via sub-skills and tools
- **Recognition**: Catalogued in registry

Plugin personas lack:
- **Cross-session memory**: No way to remember user preferences
- **Learning accumulation**: Each session starts fresh
- **Observation recording**: Insights not persisted

### Existing Memory Systems

| System | Location | Purpose | Available To |
|--------|----------|---------|--------------|
| Journal | `.claude/journal/` | Temporal memory, reflections | All agents |
| Archive | `.claude/archive/` | Patterns, observations | Archivist (primary) |
| Library | `.claude/library/` | External resources | Librarian (primary) |
| Logging | `.claude/logging/` | Full-fidelity history | All (read), Logging plugin (write) |
| Perspectives | `.claude/perspectives/` | Per-agent outputs | Custom agents |

### The Question

How should plugin personas access and contribute to these systems?

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Document which memory systems plugin personas can read
- [ ] #2 Document which memory systems plugin personas can write
- [ ] #3 Define persona memory entry format (if new)
- [ ] #4 Define how personas record learnings
- [ ] #5 Define how personas recall past interactions
- [ ] #6 Create memory access guide for skill developers
<!-- AC:END -->

## Design Options

### Option A: Journal Integration
Plugin personas use the existing journal system:
- **Write**: Create atomic entries for learnings
- **Read**: Query journal for past interactions
- **Format**: Standard atomic format with persona tag

```markdown
---
created: 2025-12-15T10:00:00
author: persona:coordinator
description: User prefers morning yoga
parent_daily: [[2025-12-15]]
tags: [preference, schedule, yoga]
---
# User Prefers Morning Yoga

Observed: User consistently schedules yoga before 10am.
```

**Pros**: Uses existing infrastructure, Obsidian compatible
**Cons**: May clutter journal with persona observations

### Option B: Dedicated Persona Memory
Create `.claude/personas/` directory for persona-specific memory:

```
.claude/personas/
├── _shared/
│   └── user-profile.md
├── coordinator/
│   ├── learnings/
│   └── state.md
├── scribe/
│   ├── learnings/
│   └── state.md
└── ...
```

**Pros**: Clean separation, persona-specific organization
**Cons**: New infrastructure, diverges from existing pattern

### Option C: Hybrid (Recommended)
- **Read**: Journal, Archive, Library, Logging (existing)
- **Write**: Journal (for significant learnings), Archive (for patterns)
- **No new directories**: Use existing systems

Personas contribute to the ecosystem memory, not separate from it.

## Memory Access Pattern

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PLUGIN PERSONA MEMORY ACCESS                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  SKILL INVOCATION                                                    │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  CONTEXT GATHERING (Read)                                    │    │
│  │                                                              │    │
│  │  1. Read skill definition (identity)                         │    │
│  │  2. Query logging for recent relevant interactions           │    │
│  │  3. Check journal for recorded preferences                   │    │
│  │  4. Load archive patterns if available                       │    │
│  └─────────────────────────────────────────────────────────────┘    │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  TASK EXECUTION                                              │    │
│  │                                                              │    │
│  │  Persona performs requested work                             │    │
│  │  - With context from memory systems                          │    │
│  │  - Learning from interaction                                 │    │
│  └─────────────────────────────────────────────────────────────┘    │
│         │                                                            │
│         ▼                                                            │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │  MEMORY CONTRIBUTION (Write)                                 │    │
│  │                                                              │    │
│  │  IF significant learning:                                    │    │
│  │    Create journal atomic (author: persona:{name})            │    │
│  │                                                              │    │
│  │  IF pattern observed:                                        │    │
│  │    Notify archivist (or add to archive directly)             │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Implementation Notes

The key insight: **Plugin personas don't need separate memory - they participate in ecosystem memory.**

The journal's atomic-first model supports multi-author entries. The `author` field can be:
- `user`
- `claude-opus-4`
- `claude-sonnet`
- `agent:{name}` (custom agents)
- `persona:{name}` (plugin personas)

This maintains the unified memory model while enabling persona-specific attribution.
