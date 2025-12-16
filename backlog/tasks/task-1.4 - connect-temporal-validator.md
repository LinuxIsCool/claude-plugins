---
id: task-1.4
title: "Connect Temporal-Validator to Knowledge Graph"
status: "To Do"
priority: medium
labels: [activation, knowledge-graph]
milestone: v1.0-activation
parentTaskId: task-1
created: 2025-12-15
assignee: ["@claude"]
---

# Connect Temporal-Validator to Knowledge Graph

## Description

The Temporal-Validator agent is **fully defined** at `.claude/agents/temporal-validator.md` but needs FalkorDB/Graphiti connection to operate. This task establishes that connection.

### Current State

- **Agent definition**: Complete (opus model)
- **Infrastructure**: Agent ready, no graph database connected
- **Skills available**: `awareness:temporal-kg-memory` (Expert level 0.60)
- **Status**: BLOCKED on infrastructure

### Agent Purpose (from registry)

> "Tracks information over time, detects staleness, maintains verified knowledge graph"

### Required Infrastructure

1. **FalkorDB**: Graph database for temporal knowledge
2. **Graphiti**: LLM-powered entity extraction layer
3. **Connection config**: API keys or local instance

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 FalkorDB instance available (local Docker or cloud)
- [ ] #2 Graphiti configured for entity extraction
- [ ] #3 Temporal-validator can write to graph
- [ ] #4 Temporal-validator can query for validity
- [ ] #5 At least one fact tracked with temporal metadata
- [ ] #6 Update registry to show temporal-validator as "Active"
<!-- AC:END -->

## Implementation Options

### Option A: Local FalkorDB (Docker)
```bash
docker run -p 6379:6379 -it --rm falkordb/falkordb
```
Pros: Full control, offline capable
Cons: Requires Docker, local resources

### Option B: FalkorDB Cloud
Use hosted FalkorDB instance
Pros: No local setup
Cons: Requires account, network dependency

### Option C: Defer to v2.0
Continue with markdown-native approach; add graph layer when scale requires
Pros: Simpler for now
Cons: Delays sophisticated temporal queries

**Recommendation**: Start with Option C (defer), implement Option A when ready for deeper temporal capabilities.

## Reference

The `awareness:temporal-kg-memory` skill documents:
- FalkorDB + Graphiti integration
- Three modes: Direct FalkorDB, Ollama (local), Cloud API
- Temporal queries and session analysis

Read: `plugins/awareness/skills/awareness/subskills/temporal-kg-memory.md`

## Notes

This task can be deferred without blocking other activation work. The ecosystem can function with:
- Journal for temporal memory
- Archive for pattern observation
- Logging for full-fidelity history

The knowledge graph adds **query sophistication**, not fundamental capability.
