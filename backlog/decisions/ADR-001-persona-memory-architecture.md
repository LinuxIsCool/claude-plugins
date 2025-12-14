---
id: ADR-001
title: "Persona Memory Architecture: Markdown-Native vs External Infrastructure"
status: Proposed
created: 2025-12-12
decision_date: null
deciders: ["@claude", "@user"]
---

# ADR-001: Persona Memory Architecture

## Status

**Proposed** - Awaiting final decision

## Context

We are building persona subagents - intelligent ambassadors for each plugin with persistent memory. A critical architectural decision is how to implement the memory system.

### The Problem

Personas need:
1. **Identity persistence** - Maintain consistent personality across sessions
2. **User context** - Remember user preferences and history
3. **Plugin knowledge** - Understand their associated plugin deeply
4. **Inter-agent coordination** - Share information with other personas
5. **Temporal awareness** - Recall past interactions accurately

### The Options

Two architectural approaches have been identified:

## Option A: External Infrastructure (Letta/Mem0/Graphiti)

Use sophisticated external systems for memory management.

### Components
- **Letta (MemGPT)**: Self-editing memory blocks with PostgreSQL persistence
- **Mem0**: Automatic LLM-powered fact extraction
- **Graphiti**: Temporal knowledge graphs with FalkorDB backend
- **A2A Protocol**: Formal agent-to-agent communication

### Pros
- Self-editing memory (agent modifies own context)
- Automatic fact extraction without manual prompting
- Sophisticated temporal queries across all history
- Sub-millisecond graph traversal for complex queries
- Proven patterns from MemGPT research

### Cons
- **External Dependencies**: Requires running Letta server, PostgreSQL
- **Philosophical Mismatch**: Every other plugin uses markdown-native storage
- **Operational Complexity**: More moving parts to maintain
- **Portability**: Harder to backup, version control, migrate
- **Human Readability**: Memory not directly inspectable as files

### When Appropriate
- Scale: Hundreds of personas or millions of memory entries
- Complex Queries: Multi-hop reasoning across temporal relationships
- Real-time: Multiple agents editing shared state simultaneously

## Option B: Markdown-Native (File-Based Memory)

Use the same markdown + YAML pattern as all other plugins.

### Components
- **Identity files**: `identity.md` with personality definition
- **State files**: `state.md` with current context
- **Memory directories**: Temporal hierarchy (daily → monthly → permanent)
- **Wikilinks**: Knowledge graph via `[[references]]`
- **YAML frontmatter**: Structured metadata

### Architecture
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

### Pros
- **Philosophical Consistency**: Same pattern as all plugins
- **Zero Dependencies**: Just files and existing tools
- **Human Readable**: Memory always inspectable
- **Portability**: Trivial backup, git version control
- **Offline**: Works without network
- **Extensible**: Can add Graphiti layer later if needed

### Cons
- No self-editing memory blocks (must use Edit tool)
- No automatic fact extraction (must explicitly record)
- Limited query sophistication (grep/glob vs graph queries)
- Slower for large memory sets (file I/O vs database)

### When Appropriate
- MVP: Getting the system working initially
- Consistency: When philosophical alignment matters
- Simplicity: When operational overhead should be minimal

## Team Consultation

A brainstorm session (STORM-001) consulted all ten plugin "ambassadors":

| Persona | Recommendation |
|---------|----------------|
| Archivist | "Full fidelity doesn't require complexity. Store in files the human can read." |
| Mentor | "Progressive disclosure - don't overwhelm. Memory should follow master skill pattern." |
| Explorer | "The filesystem IS the memory hierarchy." |
| Scribe | "Obsidian compatibility means human-readable, tool-accessible, portable." |
| Coordinator | "The schedule IS the preference database. No separate storage needed." |
| Organizer | "If a task can persist in markdown, why not persona memory?" |
| Synthesizer | "Tags and wikilinks ARE a knowledge graph in markdown." |
| Architect | "Start simple. Add complexity only when markdown fails." |
| Scholar | "Semantic search can work on markdown files. BM25 exists in logging." |
| Cartographer | "Wikilinks ARE edges. Files ARE nodes. We just need schema." |

**Unanimous recommendation**: Markdown-native for MVP.

## Recommendation

**Option B: Markdown-Native** for v1.0-personas-mvp

### Rationale

1. **Philosophical Alignment**: This project has a clear aesthetic - markdown is the medium, humans are the audience, files are the truth. Every plugin follows this pattern. Breaking it for personas would create dissonance.

2. **Incremental Complexity**: We can always add Graphiti/FalkorDB layer on top of markdown files later. Starting with external infrastructure locks us into dependencies.

3. **Validated Pattern**: The logging plugin already demonstrates full-fidelity persistence in markdown. The journal plugin shows temporal organization works. The exploration plugin shows mastery tracking in files.

4. **Zero Dependency**: The system works offline, requires no servers, backs up trivially, and can be version controlled with git.

### Escape Hatch

If markdown-native proves insufficient for:
- Query performance at scale
- Real-time multi-agent coordination
- Complex temporal reasoning

We can add Graphiti as a **read layer** on top of the markdown files. The markdown remains source of truth; Graphiti provides query acceleration.

## Decision

**[Pending user confirmation]**

Proposed: Adopt Option B (Markdown-Native) for initial implementation, with Option A available as future enhancement if scale requires.

## Consequences

### If Markdown-Native is chosen:
- Memory stored in `.claude/personas/`
- Wikilinks for knowledge graph
- Progressive disclosure for memory loading
- grep/glob for queries
- Manual memory recording (no auto-extraction)

### Future work enabled:
- Graphiti overlay for query acceleration
- Semantic search via embeddings
- A2A protocol for formal agent communication

## Related Documents

- [[PERSONA_SUBAGENTS_STRATEGY.md]] - Original external infrastructure proposal
- [[.claude/storms/2025-12-12.md]] - Team consultation brainstorm
- [[task-1.1]] - External infrastructure evaluation
- [[task-1.2]] - Markdown-native evaluation
