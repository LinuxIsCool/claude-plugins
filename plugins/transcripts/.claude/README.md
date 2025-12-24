# Transcripts Plugin Documentation

Knowledge graph architecture and implementation guides for transforming video transcripts into queryable, explorable knowledge.

---

## Quick Navigation

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **knowledge-graph-architecture.md** | Complete technical specification | Designing features, understanding architecture |
| **kg-schema-diagram.md** | Visual diagrams and examples | Quick reference, presentations |
| **kg-implementation-guide.md** | Practical code examples | Implementing the system |

---

## Overview

The transcripts plugin builds a temporal knowledge graph from video transcripts using Graphiti (temporal KG framework) and FalkorDB (graph database).

### What It Does

Transforms raw transcripts into:
- **Speaker knowledge**: "What does X discuss?", "Who believes Y?"
- **Concept evolution**: "How has thinking on X changed over time?"
- **Technique discovery**: "Show me examples of Y"
- **Temporal reasoning**: "What was said about X in Q1 2024?"
- **Relationship inference**: "What concepts relate to X?", "Who influenced Y's thinking?"

### Architecture Summary

```
YouTube Video
    ↓
[Transcription + Diarization]
    ↓
Utterances with Speakers
    ↓
[Graphiti Episode Ingestion]
    ↓
Knowledge Graph (FalkorDB)
    ├─ Speakers (voice identities)
    ├─ Concepts (ideas, techniques, beliefs)
    ├─ Utterances (timestamped speech)
    └─ Relationships (temporal, semantic)
    ↓
[Query Layer]
    ↓
Visualization (Obsidian/Quartz/D3)
```

---

## Core Concepts

### Node Types (11 total)

**Primary**:
- **Speaker**: Voice identities with fingerprints, stats
- **Concept**: Abstract ideas (techniques, beliefs, technologies)
- **Utterance**: Atomic speech segments with timestamps
- **Transcript**: Source media metadata
- **Belief**: Expressed opinions with temporal tracking
- **Technique**: Actionable methods with examples
- **Example**: Concrete demonstrations

**Supporting**:
- **Topic**: High-level themes
- **Entity**: Named entities (people, orgs, products)
- **Session**: Grouped content (series, multi-part)

### Edge Types (11 total)

**Attribution**:
- `SPOKE`: Speaker → Utterance (who said what)
- `CONTAINS`: Transcript → Utterance (ordering)

**Content**:
- `MENTIONS`: Utterance → Concept/Entity/Topic (core links)
- `DISCUSSES`: Speaker → Concept (aggregated stats)
- `BELIEVES`: Speaker → Belief (temporal positions)
- `DEMONSTRATES`: Utterance → Technique (examples)
- `CITES`: Utterance → Entity (references)

**Relationships**:
- `RELATED_TO`: Concept ↔ Concept (co-occurrence)
- `BUILDS_ON`: Concept → Concept (prerequisites)
- `CONTRADICTS`: Belief ↔ Belief (conflicts)
- `AGREES_WITH`: Speaker ↔ Speaker (alignment)

### Temporal Model

Every edge has:
- **valid_at**: When the fact was true (real-world time)
- **created_at**: When we learned this fact (ingestion time)
- **invalid_at**: When the fact became false (null = still valid)

Enables:
- Point-in-time queries: "What did X believe in January?"
- Evolution tracking: "How has thinking changed?"
- Belief invalidation: "When did X change their position?"

---

## Scale Projections

Based on 2800 transcripts @ 6 min avg:

| Metric | Count | Storage |
|--------|-------|---------|
| **Nodes** | 77,600 | ~2 GB |
| **Edges** | 308,500 | - |
| **Embeddings** | - | ~15 GB |
| **Full-text** | - | ~500 MB |
| **Total** | - | **~17.5 GB** |

### Performance Targets

- Query latency: <100ms for simple queries, <1s for complex traversals
- Ingestion: 10 transcripts/minute (with LLM rate limits)
- Graph rendering: 1000+ nodes at 60fps (PixiJS WebGL)

---

## Example Queries

### Speaker-Centric
```cypher
// What does Dan discuss?
MATCH (s:Speaker {name: "Dan Shipper"})-[d:DISCUSSES]->(c:Concept)
RETURN c.name, d.mention_count
ORDER BY d.mention_count DESC
LIMIT 10
```

### Temporal
```cypher
// How has thinking on "AI agents" evolved?
MATCH (c:Concept {name: "AI agents"})<-[m:MENTIONS]-(u:Utterance)<-[:CONTAINS]-(t:Transcript)
ORDER BY t.source_created_at ASC
RETURN t.source_created_at, t.title, u.text
```

### Belief Tracking
```cypher
// Track Dan's position changes on agents
MATCH (s:Speaker {name: "Dan Shipper"})-[b:BELIEVES]->(belief:Belief)
WHERE belief.statement CONTAINS "agents"
RETURN belief.statement, b.strength, b.valid_at, b.invalid_at
ORDER BY b.valid_at
```

### Discovery
```cypher
// Find most discussed concepts
MATCH (c:Concept)
RETURN c.name, c.mention_count, c.speaker_count
ORDER BY c.mention_count DESC
LIMIT 20
```

### Relationship Inference
```cypher
// Who influenced Dan's thinking on agents?
MATCH (target:Speaker {name: "Dan Shipper"})-[d1:DISCUSSES]->(c:Concept {name: "AI agents"})
WITH target, c, d1.first_mentioned as target_first
MATCH (influencer:Speaker)-[d2:DISCUSSES]->(c)
WHERE d2.first_mentioned < target_first AND influencer <> target
RETURN influencer.name, d2.first_mentioned
ORDER BY d2.first_mentioned
```

---

## Visualization

### Obsidian/Quartz Export

Generate markdown files with wikilinks:

```markdown
# Dan Shipper

**Transcripts**: 45
**Speaking Time**: 4h 23m

## Discusses
- [[AI agents]] (127 mentions)
- [[knowledge graphs]] (34 mentions)
```

Deploy with Quartz for interactive graph visualization.

### Custom D3 Views

Four view types:
1. **Speaker Network**: Force-directed graph of speaker alignment
2. **Concept Map**: Hierarchical tree of concept dependencies
3. **Temporal Timeline**: Concept mentions over time
4. **Knowledge Density**: Heatmap of speaker × concept activity

---

## Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- Set up FalkorDB
- Configure Graphiti
- Define entity schemas
- Test with 10 transcripts

### Phase 2: Knowledge Extraction (Week 3-4)
- Concept extraction
- Technique extraction
- Belief extraction
- Aggregation queries

### Phase 3: Relationship Inference (Week 5-6)
- RELATED_TO (co-occurrence)
- BUILDS_ON (dependencies)
- CONTRADICTS (conflicts)
- AGREES_WITH (alignment)

### Phase 4: Query Interface (Week 7-8)
- Query API design
- Speaker/concept/technique queries
- Temporal queries

### Phase 5: Visualization (Week 9-10)
- Obsidian export
- Quartz configuration
- Custom D3 endpoint
- Interactive views

### Phase 6: Batch Processing (Week 11-12)
- Batch ingestion pipeline
- Process all 2800 transcripts
- Performance optimization

### Phase 7: Integration (Week 13-14)
- Slash commands
- Subagent creation
- Documentation

---

## Quick Start

### Prerequisites
```bash
# FalkorDB
docker run -d -p 6379:6379 falkordb/falkordb:latest

# Graphiti
pip install graphiti-core

# Environment
export OPENAI_API_KEY="sk-..."
```

### Minimal Working Example

See `kg-implementation-guide.md` for complete MWE with test transcript.

Key steps:
1. Initialize Graphiti with FalkorDB driver
2. Convert utterances to episodes
3. Ingest with custom entity schemas
4. Query the graph

---

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Graph DB | FalkorDB | Redis-based graph storage |
| Temporal KG | Graphiti | Bi-temporal knowledge graph framework |
| Embeddings | OpenAI/Voyage | Semantic similarity |
| LLM | GPT-4/Claude | Entity extraction, deduplication |
| Visualization | Quartz + D3 + PixiJS | Interactive graph rendering |
| Query | Cypher | Graph query language |

---

## Design Principles

1. **Episode-centric ingestion**: All data enters as Graphiti episodes
2. **Bi-temporal tracking**: Every edge tracks valid_at, invalid_at, created_at
3. **Automatic deduplication**: Graphiti merges similar entities
4. **Hybrid retrieval**: Semantic + keyword + graph traversal
5. **Multi-tenant isolation**: group_id namespacing per transcript
6. **Visualization-first**: Design for explorable graph views

---

## File Manifest

```
.claude/
├── README.md (this file)
├── knowledge-graph-architecture.md    # 13,000-word spec
├── kg-schema-diagram.md               # Visual diagrams
└── kg-implementation-guide.md         # Practical guide with MWE
```

---

## Next Steps

1. **Read** `knowledge-graph-architecture.md` for complete technical understanding
2. **Review** `kg-schema-diagram.md` for visual reference
3. **Implement** using `kg-implementation-guide.md` MWE
4. **Test** with 10 sample transcripts
5. **Scale** to 100, then 1000 transcripts
6. **Optimize** based on performance metrics
7. **Visualize** using Obsidian export or custom D3 views

---

## Open Questions

1. **Entity resolution threshold**: What similarity score triggers merging? (Default: 0.9)
2. **Belief extraction**: Rule-based or pure LLM?
3. **Aggregation frequency**: Real-time or batch?
4. **Storage strategy**: Duplicate between Graphiti and custom layer?
5. **Visualization priority**: Obsidian export or custom endpoint first?

---

## Support

- **Architecture questions**: See `knowledge-graph-architecture.md`
- **Implementation help**: See `kg-implementation-guide.md`
- **Visual reference**: See `kg-schema-diagram.md`
- **Ecosystem context**: See `/home/ygg/Workspace/sandbox/marketplaces/claude/.claude/README.md`

---

**Status**: Design phase complete, implementation pending
**Created**: 2025-12-24
**Author**: obsidian-quartz agent
