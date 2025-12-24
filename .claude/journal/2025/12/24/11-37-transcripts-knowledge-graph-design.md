---
type: atomic
created: 2025-12-24T11:37:40-08:00
tags:
  - design
  - transcripts
  - knowledge-graphs
  - graphiti
  - falkordb
  - architecture
context: Designed knowledge graph architecture for transcripts plugin
related:
  - "[[11-13-transcripts-infrastructure-audit]]"
  - "[[11-04-youtube-ingestion-queue]]"
parent_daily: "[[2025-12-24]]"
---

# Transcripts Knowledge Graph Design

Designed comprehensive knowledge graph architecture for the transcripts plugin to transform 2800+ YouTube video transcripts into queryable, explorable temporal knowledge.

## Context

The transcripts plugin has a queue of 2800+ YouTube videos with domain models for Entity, Speaker, Topic, and Utterance. The ecosystem has a knowledge-graphs plugin with FalkorDB/Graphiti skills. The goal is to build a "metabolic" system that digests transcripts into queryable knowledge.

## Design Deliverables

Created three comprehensive documents in `/home/ygg/Workspace/sandbox/marketplaces/claude/plugins/transcripts/.claude/`:

### 1. knowledge-graph-architecture.md (13,000 words)

Complete architectural specification covering:

**Node Types (8 primary + 3 supporting)**:
- Speaker: Voice identities with fingerprints, stats, cross-transcript presence
- Concept: Abstract ideas (techniques, beliefs, technologies, methods)
- Transcript: Source media metadata
- Utterance: Atomic speech segments with timestamps
- Topic: High-level thematic categorization
- Belief: Expressed positions/opinions with temporal tracking
- Example: Concrete instances and demonstrations
- Technique: Actionable methods with complexity ratings
- Entity, Session, supporting nodes

**Edge Types (11 relationship types)**:
- SPOKE: Speaker → Utterance attribution
- CONTAINS: Transcript → Utterance ordering
- MENTIONS: Utterance → Concept/Entity/Topic (core content links)
- DISCUSSES: Speaker → Concept (aggregated from SPOKE → MENTIONS)
- BELIEVES: Speaker → Belief (bi-temporal tracking of positions)
- DEMONSTRATES: Utterance → Technique (examples)
- RELATED_TO: Concept ↔ Concept (co-occurrence)
- BUILDS_ON: Concept → Concept (prerequisites)
- CONTRADICTS: Belief ↔ Belief (conflicts)
- AGREES_WITH: Speaker ↔ Speaker (alignment)
- CITES: Utterance → Entity (references)

**Temporal Aspects**:
- Bi-temporal model (Graphiti native): `valid_at`, `created_at`, `invalid_at`
- Point-in-time queries: "What did X believe about Y in January 2024?"
- Evolution tracking: "How has thinking on X evolved over time?"
- Belief change detection: "When did speaker X change their position on Y?"

**Query Patterns**:
- Speaker-centric: "What does Dan believe about agents?"
- Concept-centric: "How has thinking on X evolved?"
- Technique-centric: "Show me examples of X"
- Discovery: "What are the most discussed topics?"
- Temporal: "What was said about X in time range Y?"
- Graph traversal: "Who influenced X's thinking on Y?"

**Pipeline Architecture**:
```
YouTube Video
    ↓
[Whisper Transcription + Diarization]
    ↓
Transcript + Utterances
    ↓
[Graphiti Episode Ingestion]
    ↓
Knowledge Extraction (Concepts, Techniques, Beliefs, Examples)
    ↓
Relationship Inference (RELATED_TO, BUILDS_ON, CONTRADICTS)
    ↓
Aggregation (DISCUSSES edges, statistics)
```

**Hybrid Storage Strategy**:
- Graphiti layer: Temporal KG, semantic search, auto-deduplication
- Custom layer: Speaker attribution, voice fingerprints, transcript metadata
- Bridge via metadata and IDs

**Obsidian/Quartz Visualization**:
- Export strategy: Generate markdown files from graph data
- Wikilink generation for graph connectivity
- Custom visualization endpoint serving D3-compatible JSON
- Multiple views: Speaker network, concept map, temporal timeline, belief evolution

**Implementation Roadmap**: 14-week plan with 7 phases

### 2. kg-schema-diagram.md

Visual diagrams covering:
- Node-edge overview (ASCII art schema)
- Data flow architecture (pipeline visualization)
- Query pattern examples (5 illustrated patterns)
- Temporal schema (bi-temporal model visualization)
- Graph statistics (projected scale: 77,600 nodes, 308,500 edges, ~17.5 GB)
- Visualization layouts (4 graph view types)

### 3. kg-implementation-guide.md

Practical implementation guide with:
- Prerequisites (FalkorDB, Graphiti, API keys)
- 15-minute quick start
- Custom entity schemas (Concept, Technique, Belief, Example)
- Ingestion pipeline code
- Query interface code
- Minimal working example (MWE)
- Batch migration script
- Incremental ingestion hook
- Slash command implementations
- Troubleshooting guide

## Key Design Decisions

### 1. Graphiti as Foundation

Chose Graphiti over pure FalkorDB for:
- Native bi-temporal tracking (valid_at, invalid_at, created_at)
- Automatic entity deduplication via LLM
- Hybrid retrieval (semantic + keyword + graph traversal)
- Episode-centric ingestion model (natural fit for utterances)

### 2. Dual Storage Model

Maintain both:
- **Graphiti layer**: Temporal reasoning, semantic queries, relationship extraction
- **Custom layer**: Speaker fingerprints, transcript metadata, precise attribution

Rationale: Graphiti excels at knowledge extraction and temporal reasoning, but transcripts have domain-specific needs (voice identity, media metadata).

### 3. Utterance-as-Episode

Each utterance becomes a Graphiti episode:
```python
await graphiti.add_episode(
    name=f"{transcript.id}_{utterance.id}",
    episode_body=f"[{speaker.name}]: {utterance.text}",
    reference_time=video_publish_date + utterance.start_ms,
    group_id=transcript.id  # Namespace per transcript
)
```

This preserves:
- Temporal context (when it was said in real-world time)
- Speaker context (who said it)
- Spatial context (where in the video)

### 4. Belief Tracking with Temporal Invalidation

Key innovation: Track belief evolution using Graphiti's bi-temporal edges.

Example:
```
Jan 2024: (Speaker)-[BELIEVES {valid_at: Jan 2024, strength: strong}]->(Belief: "Agents should use JSON")
Mar 2024: (Speaker)-[BELIEVES {valid_at: Mar 2024, strength: moderate}]->(Belief: "Structured outputs are better")
```

When new belief contradicts old belief, Graphiti automatically sets `invalid_at` on the old edge.

Enables: "How has X's thinking on Y changed over time?"

### 5. Aggregated DISCUSSES Edges

Don't just rely on SPOKE → MENTIONS paths. Build explicit DISCUSSES edges:

```cypher
MATCH (s:Speaker)-[:SPOKE]->(u:Utterance)-[m:MENTIONS]->(c:Concept)
WITH s, c, count(m) as mention_count, min(m.valid_at) as first, max(m.valid_at) as last
MERGE (s)-[d:DISCUSSES]->(c)
SET d.mention_count = mention_count, d.first_mentioned = first, d.last_mentioned = last
```

Benefits:
- Faster queries ("What does Dan discuss?")
- Direct speaker-concept statistics
- Cleaner visualization (fewer edges)

### 6. Custom Entity Schemas

Define Pydantic schemas for domain-specific extraction:

```python
class Technique(BaseModel):
    name: str
    description: str
    complexity: str  # beginner|intermediate|advanced|expert
    category: str    # prompting|architecture|debugging
```

This guides Graphiti's LLM extraction to produce structured, queryable entities instead of generic EntityNodes.

## Projected Scale

Based on 2800 transcripts @ 6 min avg:

**Nodes**: 77,600
- Utterance: 50,000
- Concept: 10,000
- Belief: 5,000
- Entity: 5,000
- Transcript: 2,800
- Example: 3,000
- Technique: 1,000
- Topic: 500
- Session: 200
- Speaker: 100

**Edges**: 308,500
- MENTIONS: 150,000
- SPOKE: 50,000
- CONTAINS: 50,000
- RELATED_TO: 20,000
- DISCUSSES: 10,000
- BELIEVES: 10,000
- CITES: 10,000
- DEMONSTRATES: 5,000
- BUILDS_ON: 2,000
- CONTRADICTS: 1,000
- AGREES_WITH: 500

**Storage**: ~17.5 GB (graph: 2 GB, embeddings: 15 GB, full-text: 500 MB)

## Example Queries Enabled

### "What does Dan believe about agents?"
```cypher
MATCH (s:Speaker {name: "Dan Shipper"})-[b:BELIEVES]->(belief:Belief)
WHERE belief.statement CONTAINS "agents" AND b.invalid_at IS NULL
RETURN belief.statement, b.strength, b.first_stated
```

### "How has thinking on knowledge graphs evolved?"
```cypher
MATCH (c:Concept {name: "knowledge graphs"})<-[m:MENTIONS]-(u:Utterance)<-[:CONTAINS]-(t:Transcript)
ORDER BY t.source_created_at ASC
RETURN t.source_created_at, t.title, u.text, m.salience
```

### "Who influenced Dan's thinking on agents?"
```cypher
MATCH (target:Speaker {name: "Dan Shipper"})-[d1:DISCUSSES]->(c:Concept {name: "AI agents"})
WITH target, c, d1.first_mentioned as target_first
MATCH (influencer:Speaker)-[d2:DISCUSSES]->(c)
WHERE d2.first_mentioned < target_first AND influencer <> target
RETURN influencer.name, d2.first_mentioned, d2.mention_count
ORDER BY d2.first_mentioned
```

### "Find examples of chain-of-thought prompting"
```cypher
MATCH (t:Technique {name: "chain-of-thought prompting"})<-[:DEMONSTRATES]-(u:Utterance)
RETURN u.text, u.start_ms, u.end_ms
ORDER BY u.created_at DESC
LIMIT 5
```

## Visualization Strategy

### Option 1: Obsidian Export

Generate markdown files with wikilinks:

```markdown
# Dan Shipper

**Transcripts**: 45
**Speaking Time**: 4h 23m

## Discusses

- [[AI agents]] (127 mentions)
- [[knowledge graphs]] (34 mentions)
- [[chain-of-thought prompting]] (18 mentions)
```

Deploy with Quartz for interactive graph visualization.

### Option 2: Custom D3 Endpoint

Serve graph data directly from FalkorDB:

```python
@app.get("/api/graph/speakers")
async def get_speaker_graph():
    query = "MATCH (s:Speaker)-[d:DISCUSSES]->(c:Concept) RETURN s, c, d"
    results = await graphiti.driver.execute_query(query)
    return {"nodes": [...], "links": [...]}  # D3 format
```

Render with D3 + PixiJS for high-performance graph (handles 10k+ nodes).

### View Types

1. **Speaker Network**: Speakers connected by AGREES_WITH (force-directed)
2. **Concept Map**: Concepts connected by BUILDS_ON (hierarchical tree)
3. **Temporal View**: Timeline of concept mentions (time axis)
4. **Knowledge Density**: Heatmap of speaker × concept mentions

## Implementation Path

1. **Week 1-2**: Set up FalkorDB, configure Graphiti, test with 10 transcripts
2. **Week 3-4**: Implement knowledge extraction (concepts, techniques, beliefs)
3. **Week 5-6**: Implement relationship inference (RELATED_TO, BUILDS_ON, CONTRADICTS)
4. **Week 7-8**: Build query interface, implement all query patterns
5. **Week 9-10**: Create visualization layer (Obsidian export + custom endpoint)
6. **Week 11-12**: Batch process all 2800 transcripts, optimize performance
7. **Week 13-14**: Integration (slash commands, subagent, documentation)

## Next Steps

1. **Validate design** with ecosystem maintainer
2. **Set up FalkorDB** instance (Docker or cloud)
3. **Run MWE** with single test transcript
4. **Batch test** with 100 transcripts to validate scale assumptions
5. **Optimize** ingestion pipeline (concurrency, batch size, rate limits)

## Files Created

All documentation in `/home/ygg/Workspace/sandbox/marketplaces/claude/plugins/transcripts/.claude/`:

- `knowledge-graph-architecture.md` (13,000 words, complete spec)
- `kg-schema-diagram.md` (visual diagrams, ASCII art)
- `kg-implementation-guide.md` (practical quick-start, MWE, troubleshooting)

## Design Principles

1. **Episode-centric ingestion**: All data enters as Graphiti episodes
2. **Bi-temporal tracking**: Every edge has valid_at, invalid_at, created_at
3. **Automatic deduplication**: Graphiti merges similar entities via LLM
4. **Hybrid retrieval**: Semantic + keyword + graph traversal
5. **Multi-tenant isolation**: group_id namespacing per transcript
6. **Visualization-first**: Design for explorable graph views

## Open Questions

1. Entity resolution threshold (currently 0.9 similarity)
2. Belief extraction strategy (rule-based vs pure LLM)
3. Aggregation frequency (real-time vs daily batch)
4. Storage duplication (Graphiti + custom layer)
5. Visualization priority (Obsidian export vs custom endpoint first)

---

*Parent: [[2025-12-24]] → [[2025-12]] → [[2025]]*
