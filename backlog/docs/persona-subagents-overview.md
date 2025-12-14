# Persona Subagents Project Overview

## Vision

Create intelligent, persistent ambassador subagents for each plugin in the Claude Code ecosystem. Each persona embodies their plugin's identity, maintains long-term memory across conversations, and collaborates with other personas.

## The Ten Personas

| Persona | Plugin | Archetype | Role |
|---------|--------|-----------|------|
| **The Archivist** | logging | Historian | Preserves full-fidelity history, enables recall |
| **The Mentor** | awareness | Teacher | Guides learning and self-improvement |
| **The Explorer** | exploration | Scientist | Maps environment, tracks mastery |
| **The Scribe** | journal | Practitioner | Captures reflection, builds knowledge |
| **The Coordinator** | schedule | Manager | Organizes time, learns preferences |
| **The Organizer** | backlog | PM | Tracks tasks, ensures completion |
| **The Synthesizer** | brainstorm | Thinker | Connects ideas, finds patterns |
| **The Architect** | agents | Builder | Designs systems, knows frameworks |
| **The Scholar** | llms | Researcher | Masters LLM tools and patterns |
| **The Cartographer** | knowledge-graphs | Mapper | Builds relationships, enables traversal |

## Architecture Decision

**Pending**: See [[ADR-001-persona-memory-architecture]]

Two approaches under consideration:
1. **External Infrastructure** (Letta/Mem0/Graphiti) - Sophisticated but dependency-heavy
2. **Markdown-Native** (File-based) - Consistent with project philosophy

Team consultation strongly favors markdown-native approach.

## Project Structure

```
backlog/
├── tasks/
│   ├── task-1 - persona-subagents-epic.md      # Parent epic
│   ├── task-1.1 - external-infrastructure.md   # Approach A
│   ├── task-1.2 - markdown-native.md           # Approach B
│   ├── task-1.3 - standard-schema.md           # Shared infrastructure
│   ├── task-1.4 - prototype-archivist.md       # First persona
│   ├── task-1.5 - all-persona-identities.md    # All ten personas
│   ├── task-1.6 - inter-persona-comm.md        # Communication patterns
│   └── task-1.7 - documentation.md             # Developer guide
├── decisions/
│   └── ADR-001-persona-memory-architecture.md
└── docs/
    └── persona-subagents-overview.md           # This file
```

## Milestones

### v1.0-personas-mvp
- [ ] Architecture decision finalized
- [ ] Standard infrastructure schema defined
- [ ] Prototype persona (The Archivist) working
- [ ] Memory persistence validated
- [ ] Basic documentation complete

### v1.1-inter-agent
- [ ] All ten personas have identities
- [ ] Inter-persona communication working
- [ ] Handoff patterns validated
- [ ] Shared state management working

### v2.0-advanced-memory
- [ ] Graphiti overlay for query acceleration (if needed)
- [ ] Semantic search via embeddings
- [ ] A2A protocol for formal communication
- [ ] Advanced temporal queries

## Key Documents

| Document | Purpose |
|----------|---------|
| [[PERSONA_SUBAGENTS_STRATEGY.md]] | Original strategy (external infrastructure) |
| [[.claude/storms/2025-12-12.md]] | Team consultation brainstorm |
| [[ADR-001-persona-memory-architecture]] | Architecture decision record |

## Principles

The project should follow these principles (from team consultation):

1. **Markdown-Native Memory** - Like all other plugins
2. **Progressive Disclosure** - Core identity loaded, deeper memory on-demand
3. **Temporal Hierarchy** - Daily → Weekly → Monthly → Permanent
4. **Wikilinks as Knowledge Graph** - Links ARE edges, files ARE nodes
5. **YAML Frontmatter** - Queryable, parseable structured data
6. **Logging Integration** - Personas READ logs, WRITE synthesized memory
7. **Zero Dependencies** - Just files and existing tools

## Quick Reference

### Proposed Directory Structure (Markdown-Native)
```
.claude/personas/
├── _schema/                    # Templates
├── _shared/                    # Cross-persona state
│   ├── user-profile.md
│   └── project-context.md
└── {persona}/
    ├── identity.md             # Core (always loaded)
    ├── state.md                # Current context
    └── memory/
        ├── permanent/          # Long-term
        └── YYYY-MM/            # Temporal
```

### Memory Loading Pattern
```
Always: identity.md, state.md (~700 tokens)
If relevant: user-profile.md, recent memory
On demand: permanent memories, history, other personas
```
