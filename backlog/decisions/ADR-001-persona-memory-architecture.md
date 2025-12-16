---
id: ADR-001
title: "Persona Memory Architecture: Activation of Existing Infrastructure"
status: Accepted
created: 2025-12-12
decision_date: 2025-12-15
deciders: ["@claude", "@user"]
---

# ADR-001: Persona Memory Architecture

## Status

**Accepted** - Decision made based on discovery that architecture already exists

## Context

We set out to build persona subagents - intelligent ambassadors for each plugin with persistent memory.

### Original Problem Statement (2025-12-12)

Personas need:
1. Identity persistence
2. User context memory
3. Plugin knowledge
4. Inter-agent coordination
5. Temporal awareness

### Discovery (2025-12-15)

Reading `.claude/README.md` and `.claude/registry/agents.md` revealed:

**The persona architecture already exists.**

| Component | Status | Location |
|-----------|--------|----------|
| 9 custom agents | Defined | `.claude/agents/` |
| 11 plugin personas | Catalogued | Registry |
| Agent registry | Active | `.claude/registry/agents.md` |
| Process registry | Active | `.claude/registry/processes.md` |
| Archivist | DORMANT | `.claude/agents/archivist.md` |
| Librarian | DORMANT | `.claude/agents/librarian.md` |
| Temporal-Validator | DORMANT | `.claude/agents/temporal-validator.md` |
| Archive infrastructure | Ready | `.claude/archive/` |
| Library infrastructure | Ready | `.claude/library/` |
| Journal memory | Active | `.claude/journal/` |
| Session logging | Active | `.claude/logging/` |
| Perspectives | Active | `.claude/perspectives/` |

## Options Considered

### Option A: External Infrastructure (Original Proposal)
- Letta (MemGPT) for self-editing memory
- Mem0 for automatic fact extraction
- Graphiti + FalkorDB for knowledge graphs

**Rejected**: Infrastructure already exists; external dependencies unnecessary.

### Option B: Build New Markdown-Native System
- Create `.claude/personas/` directory
- New schema for persona memory
- New processes for memory flow

**Rejected**: This duplicates what already exists. The ecosystem already has:
- Journal (temporal memory)
- Archive (pattern observation)
- Library (external resources)
- Logging (full-fidelity history)

### Option C: Activate Existing Infrastructure (Chosen)
- Invoke dormant agents (archivist, librarian, temporal-validator)
- Use existing memory systems (journal, archive, library)
- Plugin personas contribute to ecosystem memory, not separate from it

**Accepted**: Honors existing architecture, minimal new work, philosophically consistent.

## Decision

**Activate existing infrastructure rather than build new.**

### What This Means

1. **Dormant agents get invoked**, not redefined
2. **Journal becomes shared memory** for all personas (author attribution)
3. **Archive becomes pattern storage** (archivist manages)
4. **Library becomes resource cache** (librarian manages)
5. **Plugin personas participate in ecosystem memory**

### Memory Access Pattern

```
Plugin Persona Invoked
        │
        ▼
┌───────────────────────┐
│ CONTEXT GATHERING     │
│ - Load skill (identity)│
│ - Query logging       │
│ - Check journal       │
│ - Load archive        │
└───────────────────────┘
        │
        ▼
┌───────────────────────┐
│ TASK EXECUTION        │
│ With ecosystem context│
└───────────────────────┘
        │
        ▼
┌───────────────────────┐
│ MEMORY CONTRIBUTION   │
│ - Journal atomic      │
│   (author: persona:X) │
│ - Archive pattern     │
└───────────────────────┘
```

### Author Attribution in Journal

The journal's atomic format supports multi-author entries:
- `author: user`
- `author: claude-opus-4`
- `author: agent:archivist`
- `author: persona:coordinator`

This maintains unified memory while enabling persona-specific attribution.

## Consequences

### Positive
- No new infrastructure to build
- Immediate activation possible
- Philosophically consistent with ecosystem
- Leverages existing investment in agents and processes
- Single source of truth for memory

### Negative
- Limited query sophistication (grep vs graph database)
- No automatic fact extraction (manual recording)
- Archivist/Librarian need invocation (not automatic)

### Future Options Preserved
- Can add Graphiti layer on top of markdown
- Can add Letta if self-editing memory needed
- Can add Mem0 if auto-extraction valuable

## Implementation

### Phase 1: Agent Activation
1. Invoke archivist → begins artifact observation
2. Invoke librarian → begins resource cataloguing
3. Execute historical archaeology → backfill journal

### Phase 2: Plugin Persona Memory
1. Define memory access pattern (task-1.5)
2. Prototype with The Coordinator (task-1.6)
3. Roll out to all 11 plugin personas

### Phase 3: Knowledge Graph (Optional)
1. Connect temporal-validator to FalkorDB
2. Enable sophisticated temporal queries
3. Only if markdown-native proves insufficient

## Key Insight

From `.claude/README.md`:
> "This repository is alive. It has metabolism, organs, nervous system, memory, and immune system. The skeleton is built. Some organs circulate. Others await activation."

**The persona subagents work is organ activation, not organ construction.**

## Related Documents

- [[.claude/README.md]] - Ecosystem orientation
- [[.claude/registry/agents.md]] - Agent catalogue
- [[.claude/registry/processes.md]] - Process mapping
- [[.claude/storms/2025-12-15.md]] - Discovery brainstorm
- [[PERSONA_SUBAGENTS_STRATEGY.md]] - Original strategy (historical)
- [[task-1]] - Revised epic
