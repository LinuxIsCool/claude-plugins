# github.com

*Domain catalogue for GitHub resources*

---

## Domain Statistics

| Metric | Value |
|--------|-------|
| Resources tracked | 1 |
| First accessed | 2025-12-15 |
| Freshness policy | 7 days |

---

## Resources

### graphiti

**URL**: https://github.com/getzep/graphiti

**Metadata**:
```yaml
url: https://github.com/getzep/graphiti
title: "Graphiti - Build and query temporally-aware knowledge graphs"
domain: github.com
fetched: 2025-12-15T19:15:00Z
last_accessed: 2025-12-15T19:15:00Z
access_count: 1
topics: [knowledge-graphs, temporal-graphs, agent-memory, ai-agents]
cited_by:
  - session: 2025-12-13-15-18-40-05038dd8
  - document: plugins/knowledge-graphs/skills/kg-master/subskills/graphiti.md
  - agent: git-historian
freshness_policy: 7d
license: Apache-2.0
```

**Summary**:
Graphiti is an open-source framework by Zep for building and querying temporally-aware knowledge graphs optimized for AI agents. It continuously integrates user interactions, structured/unstructured enterprise data, and external information into a coherent, queryable graph.

**Key Features**:
- Real-time incremental updates without batch recomputation
- Bi-temporal data model (event occurrence time + ingestion time)
- Hybrid retrieval: semantic embeddings + BM25 keyword search + graph traversal
- Custom entity definitions via Pydantic models
- Enterprise scalability with parallel processing
- Point-in-time historical queries

**Use In This Repository**:
- Informed the design of the `git-historian` agent
- Provided patterns for temporal knowledge graph construction
- FalkorDB driver used for git history ingestion
- Bi-temporal model applied to commit validity tracking

**Related Resources**:
- Documentation: https://help.getzep.com/graphiti
- Academic Paper: https://arxiv.org/abs/2501.13956
- MCP Server: Included in repository

**Why Catalogued**:
Foundation resource for temporal knowledge graph capabilities in this ecosystem.

---

*Last updated: 2025-12-15*
