---
id: msg_6Ngy1612qggH5ZthVjQmXyajYFkRzauw
kind: 103
account_id: claude
created_at: 1765904981844
imported_at: 1766005511633
author_name: Claude
thread_id: cc_d49e6b0a
platform: claude-code
session_id: d49e6b0a-03db-4ab3-922d-43b820eea0bb
tags: [["event_type","AssistantResponse"]]
---

This is a critical question. Let me break down the cost dimensions:

## Cost Analysis by Approach

### 1. Manual Extraction (current approach)

| Dimension | Cost |
|-----------|------|
| API tokens | $0 |
| Compute | Negligible (FalkorDB writes) |
| Human time | ~5-10 min/document |
| **136 docs** | **11-23 hours of work** |

**Quality**: High precision, but doesn't scale.

---

### 2. Structure-Only Parsing (no LLM)

Parse frontmatter, headers, wikilinks as nodes/edges.

| Dimension | Cost |
|-----------|------|
| API tokens | $0 |
| Compute | ~1 minute total |
| Human time | ~1 hour to write parser |

**Quality**: Gets structure but misses semantic meaning. A `[[link]]` becomes an edge, but we don't know *why* they're connected.

---

### 3. LLM-based Extraction

Send documents to LLM, extract entities and relationships.

**Token estimation for 136 documents:**
```
Average doc size: ~1,000 tokens
Total input:      ~136,000 tokens
Output per doc:   ~200 tokens (extracted concepts)
Total output:     ~27,000 tokens
```

| Model | Input Cost | Output Cost | **Total** |
|-------|------------|-------------|-----------|
| Haiku | $0.03 | $0.03 | **~$0.07** |
| Sonnet | $0.41 | $0.41 | **~$0.82** |
| Opus | $2.04 | $2.04 | **~$4.00** |

**Quality**: Good extraction, may miss nuance or hallucinate relationships.

---

### 4. Graphiti-style (Embeddings + LLM + Temporal)

Full knowledge graph with vector search, entity resolution, temporal edges.

| Component | Cost |
|-----------|------|
| Embeddings (OpenAI) | ~$0.02 (136K tokens) |
| LLM extraction | ~$0.82 (Sonnet) |
| Entity resolution | ~$0.20 (deduplication passes) |
| **Total** | **~$1.00-1.50** |

**Quality**: Highest - semantic search, temporal awareness, entity deduplication.

---

## The Hidden Costs

### Ongoing Maintenance
```
New document created → needs ingestion
Document edited     → needs re-ingestion  
Document deleted    → needs graph cleanup
```

Without automation, the graph drifts from reality.

### Quality Degradation
- Automated extraction introduces noise
- Noise accumulates over time
- Eventually need human curation passes

### Context Window Tax
Every time we query the graph in a session, results consume context tokens. A dense graph with 500 nodes might return 50 relevant results = ~2,000 tokens of context per query.

---

## The Real Tradeoff

```
                    Quality
                       ↑
                       │
         Graphiti ─────┼───── Manual
         ($1.50)       │      (20 hrs)
                       │
    LLM Extraction ────┤
         ($0.82)       │
                       │
   Structure-Only ─────┼─────
         ($0)          │
                       └──────────────→ Cost
```

**My recommendation**: Start with **LLM extraction using Haiku (~$0.07)** to populate a baseline graph, then selectively enrich high-value nodes manually. The 100x cost difference between Haiku and manual time makes automation compelling even if quality is 80% of manual.

Want me to build the automated ingestion pipeline?
