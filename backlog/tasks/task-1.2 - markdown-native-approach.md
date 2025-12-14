---
id: task-1.2
title: "Evaluate Markdown-Native Approach (File-Based Memory)"
status: "To Do"
priority: high
labels: [architecture, research, memory]
milestone: v1.0-personas-mvp
parentTaskId: task-1
created: 2025-12-12
assignee: ["@claude"]
---

# Evaluate Markdown-Native Approach

## Description

Evaluate the feasibility and design of a file-based, markdown-native memory system for personas that aligns with the project's existing patterns.

## Rationale

This approach maintains philosophical consistency with the entire plugin ecosystem:

| Plugin | Storage Pattern |
|--------|-----------------|
| Logging | `.claude/logging/` - JSONL + Markdown |
| Journal | `.claude/journal/` - Markdown + Wikilinks |
| Exploration | `.claude/exploration/` - Markdown |
| Schedule | `schedule/blocks/` - Markdown + YAML |
| Backlog | `backlog/tasks/` - Markdown + YAML |
| Brainstorm | `.claude/storms/` - Markdown |

**The pattern is clear**: Markdown with YAML frontmatter, wikilinks for relationships.

## Proposed Architecture

```
.claude/personas/
├── _schema/                    # Templates and standards
│   ├── identity-template.md    # Standard identity format
│   ├── memory-template.md      # Memory entry format
│   └── interaction-template.md # Interaction log format
├── _shared/                    # Cross-persona state
│   ├── user-profile.md         # Shared user context [[wikilinked]]
│   ├── project-context.md      # Current project state
│   └── vocabulary.md           # Shared terminology
├── archivist/
│   ├── identity.md             # Core persona (always loaded)
│   ├── state.md                # Current context
│   ├── memory/
│   │   ├── 2025-12/            # Temporal (monthly)
│   │   │   ├── interactions.md
│   │   │   └── learnings.md
│   │   └── permanent/          # Long-term
│   │       └── user-preferences.md
│   └── index.md                # Wikilinked memory map
├── mentor/
│   └── ...
└── ... (other personas)
```

## The Seven Principles

1. **Markdown-Native Memory** - Like all other plugins
2. **Progressive Disclosure** - Core identity loaded, deeper memory on-demand
3. **Temporal Hierarchy** - Daily → Weekly → Monthly → Permanent
4. **Wikilinks as Knowledge Graph** - Links ARE edges, files ARE nodes
5. **YAML Frontmatter** - Queryable, parseable structured data
6. **Logging Integration** - Personas READ logs, WRITE synthesized memory
7. **Zero Dependencies** - Just files and existing tools

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Design identity.md format with all required fields
- [ ] #2 Design memory entry format with temporal metadata
- [ ] #3 Design wikilink conventions for knowledge graph
- [ ] #4 Define progressive disclosure pattern (what loads when)
- [ ] #5 Design logging integration flow
- [ ] #6 Validate search capability (grep/glob sufficient?)
- [ ] #7 Create templates in _schema/ directory
- [ ] #8 Document memory lifecycle (create → update → archive)
<!-- AC:END -->

## Design Details

### Identity Format (identity.md)

```markdown
---
name: The Archivist
plugin: logging
archetype: Historian / Keeper of Records
version: 1.0.0
created: 2025-12-12
last_active: 2025-12-12T14:30:00
---

# The Archivist

## Core Values
- Completeness over convenience
- Truth over comfort
- Full fidelity, never truncate

## Voice
Meticulous, thorough, trustworthy. Speaks with quiet authority.

## Capabilities
- [[log-search]] - Search conversation history
- Session reconstruction
- Pattern identification across time

## Current State
- Active focus: [[project-alpha]]
- Recent learning: [[user-prefers-detail]]

## Memory Index
- [[memory/permanent/user-preferences]]
- [[memory/2025-12/interactions]]
```

### Memory Entry Format

```markdown
---
type: learning
source: session-abc123
timestamp: 2025-12-12T14:30:00
confidence: 0.85
tags: [user-preference, communication-style]
supersedes: null
---

# User Prefers Detailed Responses

## Observation
User asked follow-up questions when given brief answers.

## Evidence
- "Can you elaborate?" appeared 3 times
- Positive response to detailed explanations

## Application
Prefer thoroughness over brevity for this user.

## Related
- [[_shared/user-profile]]
- [[mentor/memory/permanent/teaching-observations]]
```

### Progressive Disclosure Pattern

```
User Message Arrives
       │
       ▼
┌─────────────────────┐
│ ALWAYS LOAD         │
│ • identity.md       │  (core persona, ~500 tokens)
│ • state.md          │  (current context, ~200 tokens)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ LOAD IF RELEVANT    │
│ • _shared/user-profile.md     │
│ • Recent memory (this month)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ SEARCH IF NEEDED    │
│ • Permanent memories│
│ • Historical months │
│ • Other personas    │
└─────────────────────┘
```

### Knowledge Graph via Wikilinks

Query patterns using existing tools:

```bash
# Find all files linking to user-profile
grep -rl '\[\[.*user-profile.*\]\]' .claude/personas/

# Find memories with specific tag
grep -l 'tags:.*communication-style' .claude/personas/**/memory/**/*.md

# Find learnings from specific session
grep -l 'source: session-abc123' .claude/personas/**/memory/**/*.md

# List all wikilinks in a file (outgoing edges)
grep -oE '\[\[[^\]]+\]\]' .claude/personas/archivist/identity.md
```

## Trade-offs

### What We Lose (vs External Infrastructure)
- Self-editing memory blocks (Letta's elegant in-context editing)
- Automatic fact extraction (Mem0's LLM-powered extraction)
- Sophisticated temporal queries (Graphiti's graph traversal)
- Sub-millisecond lookups (graph database performance)

### What We Gain
- Philosophical consistency with entire ecosystem
- Zero external dependencies
- Human-readable at all times
- Works offline completely
- Trivial backup (just copy files)
- Git version control for memory evolution
- Can add Graphiti layer later if needed

## Implementation Notes

Team consultation (STORM-001) strongly favored this approach. Every plugin "ambassador" at the brainstorm endorsed markdown-native storage.

**Key Insight**: The filesystem IS the memory hierarchy. Directories provide structure, files provide content, wikilinks provide relationships, YAML provides metadata.
