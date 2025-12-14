---
id: task-1.1
title: "Evaluate External Infrastructure Approach (Letta/Mem0/Graphiti)"
status: "To Do"
priority: medium
labels: [architecture, research, memory]
milestone: v1.0-personas-mvp
parentTaskId: task-1
created: 2025-12-12
assignee: ["@claude"]
---

# Evaluate External Infrastructure Approach

## Description

Evaluate the feasibility and trade-offs of using external infrastructure for persona memory:
- **Letta (MemGPT)**: Self-editing memory blocks with PostgreSQL persistence
- **Mem0**: Automatic fact extraction with semantic search
- **Graphiti**: Temporal knowledge graphs with FalkorDB backend
- **A2A Protocol**: Agent-to-agent communication standard

## Rationale

This approach offers sophisticated capabilities:
- Self-editing memory (agent modifies own context)
- Automatic fact extraction from conversations
- Temporal querying across all sessions
- Sub-millisecond graph traversal
- Multi-agent coordination patterns

## Concerns Identified

1. **External Dependencies**: Requires Letta server, PostgreSQL, potentially cloud APIs
2. **Philosophical Mismatch**: All other plugins use markdown-native storage
3. **Operational Complexity**: More moving parts to maintain
4. **Portability**: Harder to backup, version control, or migrate
5. **Human Readability**: Memory not directly inspectable as files

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Document Letta setup requirements and complexity
- [ ] #2 Document Mem0 integration patterns
- [ ] #3 Document Graphiti/FalkorDB setup
- [ ] #4 Estimate operational overhead
- [ ] #5 Create comparison matrix with markdown-native approach
- [ ] #6 Identify use cases where this approach is necessary
<!-- AC:END -->

## Research Completed

Extensive documentation exists in:
- `plugins/agents/skills/agents-master/subskills/letta.md`
- `plugins/agents/skills/agents-master/subskills/mem0.md`
- `plugins/llms/skills/llms-master/subskills/graphiti.md`
- `plugins/agents/skills/agents-master/subskills/a2a.md`

### Letta Architecture (from research)

```
Memory Hierarchy:
├── Core Memory (In-Context) - Self-editable blocks
│   ├── persona block (agent identity)
│   ├── human block (user context)
│   └── custom blocks (state, projects, etc.)
├── Recall Memory - Message history, semantic search
└── Archival Memory - Long-term facts, documents
```

**Key Insight**: Letta's memory blocks are elegant but require running infrastructure. The self-editing behavior (agent modifies its own memory) is unique and powerful.

### Mem0 Architecture (from research)

```
Multi-Level Organization:
├── User-level memories (user_id)
├── Agent-level memories (agent_id)
├── Session-level memories (session_id)
└── Run-level memories (run_id)
```

**Key Insight**: Automatic LLM-based fact extraction removes manual memory management but requires API calls.

### When This Approach Makes Sense

1. **Scale**: Hundreds of personas or millions of memory entries
2. **Complex Queries**: Multi-hop reasoning across temporal relationships
3. **Real-time Collaboration**: Multiple agents editing shared state simultaneously
4. **Production Deployment**: When operational complexity is acceptable

## Implementation Notes

This approach documented in `PERSONA_SUBAGENTS_STRATEGY.md`. The team consultation (STORM-001) raised concerns about philosophical alignment with project principles.

**Recommendation**: Defer to v2.0 unless markdown-native approach proves insufficient.
