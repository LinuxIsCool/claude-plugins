# Transcripts Knowledge Graph Architecture

**Design Date**: 2025-12-24
**Author**: obsidian-quartz agent
**Status**: Design specification (implementation pending)

---

## Executive Summary

This document specifies the knowledge graph architecture for the transcripts plugin, designed to transform 2800+ YouTube video transcripts into a queryable, explorable temporal knowledge base. The design leverages FalkorDB/Graphiti's bi-temporal capabilities to create a "metabolic" system that digests utterances into structured knowledge while preserving temporal and speaker context.

## 1. Node Types

### 1.1 Primary Nodes

#### Speaker Node
```cypher
(:Speaker {
  id: string              // SpeakerID (spk_*)
  name: string            // Primary display name
  aliases: [string]       // Alternative names/spellings
  avatar: string          // Emoji or image

  // Voice identity
  has_fingerprint: boolean
  primary_fingerprint_model: string  // e.g., "pyannote-embedding"

  // External links
  messages_account_id: string        // Link to messages plugin
  platform_identities: [string]      // JSON: [{platform, external_id, handle}]
  external_ids: [string]             // JSON: {wikidata, wikipedia, etc.}

  // Statistics
  transcript_count: int
  utterance_count: int
  total_speaking_time_ms: bigint
  first_appearance: datetime
  last_appearance: datetime

  // Temporal
  created_at: datetime
  updated_at: datetime

  // Graph metadata
  embedding: vector       // Voice embedding (if available)
  tags: [string]
})
```

**Purpose**: Represents voice identities across transcripts. Enables "Who said X?" queries and speaker-centric views.

#### Concept Node
```cypher
(:Concept {
  id: string              // Derived from canonical name
  name: string            // Canonical concept name
  aliases: [string]       // Alternative phrasings
  description: string     // LLM-generated summary

  // Classification
  category: string        // e.g., "technique", "belief", "technology", "method"
  domain: [string]        // e.g., ["AI", "agents", "knowledge-graphs"]

  // Salience
  mention_count: int      // Total mentions across all transcripts
  speaker_count: int      // How many unique speakers discussed this
  first_mentioned: datetime
  last_mentioned: datetime

  // Temporal evolution
  definition_changes: [string]  // JSON array of {timestamp, definition, source_tx}

  // Temporal
  created_at: datetime
  updated_at: datetime

  // Graph metadata
  embedding: vector       // Semantic embedding
  keywords: [string]      // Associated keywords
  tags: [string]
})
```

**Purpose**: Represents abstract ideas, techniques, beliefs, or topics discussed in transcripts. Core of semantic queries.

#### Transcript Node
```cypher
(:Transcript {
  id: string              // TID (tx_*)
  title: string           // Video/audio title

  // Source metadata
  platform: string        // e.g., "youtube", "podcast"
  source_url: string
  source_id: string       // Platform-specific ID (youtube video ID)
  channel: string
  duration_ms: bigint

  // Processing
  status: string          // pending|transcribing|diarizing|extracting|complete|failed
  backend: string         // whisper-large-v3, etc.
  language: string
  confidence: float

  // Content stats
  utterance_count: int
  speaker_count: int
  word_count: int

  // Temporal
  source_created_at: datetime   // When video was published
  ingested_at: datetime         // When we processed it
  created_at: datetime
  updated_at: datetime

  // Graph metadata
  tags: [string]
  full_text_embedding: vector   // Embedding of concatenated text
})
```

**Purpose**: Represents source media. Entry point for "What videos discuss X?" queries.

#### Utterance Node
```cypher
(:Utterance {
  id: string              // UtteranceID (ut_*)
  index: int              // Sequential order in transcript
  text: string            // Transcribed text

  // Temporal (within transcript)
  start_ms: bigint
  end_ms: bigint
  duration_ms: bigint

  // Quality
  transcription_confidence: float
  speaker_confidence: float
  timing_confidence: float

  // Temporal
  created_at: datetime

  // Graph metadata
  language: string
  embedding: vector       // Semantic embedding of text
  word_timings: [string]  // JSON: [{word, start_ms, end_ms, confidence}]
})
```

**Purpose**: Atomic speech segment. Enables precise temporal queries and quote attribution.

#### Topic Node
```cypher
(:Topic {
  id: string
  name: string
  confidence: float

  // Metadata
  keywords: [string]
  transcript_count: int

  // Temporal
  created_at: datetime
})
```

**Purpose**: High-level thematic categorization (e.g., "AI agents", "knowledge graphs", "tool use").

#### Belief Node
```cypher
(:Belief {
  id: string
  statement: string       // Normalized belief statement
  polarity: string        // positive|negative|neutral|nuanced
  strength: string        // strong|moderate|weak|exploring

  // Evidence
  evidence_count: int     // How many utterances support this

  // Temporal evolution
  first_stated: datetime
  last_stated: datetime
  position_changes: [string]  // JSON: [{timestamp, new_position, source_ut}]

  // Temporal
  created_at: datetime
  updated_at: datetime

  // Graph metadata
  embedding: vector
})
```

**Purpose**: Represents expressed positions/opinions. Enables "What does X believe about Y?" queries and belief tracking over time.

#### Example Node
```cypher
(:Example {
  id: string
  description: string     // What the example demonstrates
  text: string           // Actual example content/quote

  // Context
  context_summary: string  // Surrounding context

  // Temporal
  created_at: datetime

  // Graph metadata
  embedding: vector
})
```

**Purpose**: Concrete instances, case studies, or demonstrations mentioned in transcripts.

#### Technique Node
```cypher
(:Technique {
  id: string
  name: string
  description: string

  // Classification
  category: string        // e.g., "prompting", "architecture", "debugging"
  complexity: string      // beginner|intermediate|advanced|expert

  // Usage tracking
  mention_count: int
  demonstrated_count: int  // How many examples exist

  // Temporal
  created_at: datetime
  updated_at: datetime

  // Graph metadata
  embedding: vector
  aliases: [string]
  related_tools: [string]
})
```

**Purpose**: Actionable methods/approaches. Enables "How do I do X?" queries.

### 1.2 Supporting Nodes

#### Entity Node
```cypher
(:Entity {
  id: string              // EntityID (ent_*)
  type: string            // person|organization|product|location|date|event|custom
  name: string
  aliases: [string]
  description: string

  // Links
  speaker_id: string      // If this entity is also a speaker
  external_ids: [string]  // JSON: {wikidata, wikipedia, dbpedia, ...}

  // Statistics
  mention_count: int

  // Temporal
  created_at: datetime
  updated_at: datetime

  // Graph metadata
  embedding: vector
  tags: [string]
})
```

**Purpose**: Named entities (people, orgs, products). Enables entity-centric queries.

#### Session Node (for multi-part content)
```cypher
(:Session {
  id: string
  name: string            // e.g., "Dan Shipper Interview Series"
  description: string

  // Aggregates
  transcript_count: int
  total_duration_ms: bigint

  // Temporal
  started_at: datetime
  ended_at: datetime
  created_at: datetime
})
```

**Purpose**: Groups related transcripts (e.g., multi-part interviews, podcast series).

---

## 2. Edge Types

### 2.1 Core Relationships

#### SPOKE (Speaker → Utterance)
```cypher
(:Speaker)-[:SPOKE {
  confidence: float       // Speaker attribution confidence
  created_at: datetime
}]->(:Utterance)
```

**Purpose**: Attributes speech to speakers. Enables "What did X say?" queries.

#### CONTAINS (Transcript → Utterance)
```cypher
(:Transcript)-[:CONTAINS {
  index: int             // Utterance order
  created_at: datetime
}]->(:Utterance)
```

**Purpose**: Links utterances to source transcript. Preserves sequential order.

#### MENTIONS (Utterance → Concept|Entity|Topic)
```cypher
(:Utterance)-[:MENTIONS {
  // Context
  text_snippet: string    // Actual mention text
  start_offset: int       // Character position in utterance
  end_offset: int

  // Quality
  confidence: float
  salience: float         // How central is this mention (0-1)

  // Temporal
  timestamp_ms: bigint    // Absolute timestamp in source media
  valid_at: datetime      // When this was stated (bi-temporal)
  created_at: datetime    // When we extracted this (bi-temporal)
}]->(:Concept|:Entity|:Topic)
```

**Purpose**: Links utterances to what they discuss. Core of content-based queries.

#### DISCUSSES (Speaker → Concept)
```cypher
(:Speaker)-[:DISCUSSES {
  // Aggregated from SPOKE → MENTIONS
  mention_count: int      // How many times speaker mentioned this
  first_mentioned: datetime
  last_mentioned: datetime

  // Derived stance
  overall_sentiment: string  // positive|negative|neutral|mixed
  depth: string             // surface|moderate|deep (based on context length)

  // Temporal
  created_at: datetime
  updated_at: datetime
}]->(:Concept)
```

**Purpose**: High-level speaker-concept relationship. Enables "What does Dan discuss?" queries.

#### BELIEVES (Speaker → Belief)
```cypher
(:Speaker)-[:BELIEVES {
  strength: string        // strong|moderate|weak|exploring
  first_stated: datetime
  last_stated: datetime
  position_changes: [string]  // JSON: temporal evolution

  // Evidence
  supporting_utterance_ids: [string]

  // Temporal (bi-temporal)
  valid_at: datetime      // When belief was true
  invalid_at: datetime    // When belief changed/invalidated
  created_at: datetime
}]->(:Belief)
```

**Purpose**: Tracks expressed beliefs/positions. Enables "What does X believe about Y?" with temporal tracking.

#### DEMONSTRATES (Utterance → Technique)
```cypher
(:Utterance)-[:DEMONSTRATES {
  // Context
  how: string             // Brief description of demonstration
  completeness: string    // full|partial|mentioned

  // Quality
  clarity: float          // How clear was the demonstration

  // Temporal
  created_at: datetime
}]->(:Technique)
```

**Purpose**: Links examples to techniques. Enables "Show me examples of X" queries.

#### PROVIDES_EXAMPLE (Utterance → Example)
```cypher
(:Utterance)-[:PROVIDES_EXAMPLE {
  created_at: datetime
}]->(:Example)
```

**Purpose**: Links concrete examples to their source.

#### EXEMPLIFIES (Example → Concept|Technique)
```cypher
(:Example)-[:EXEMPLIFIES {
  relevance: float
  created_at: datetime
}]->(:Concept|:Technique)
```

**Purpose**: Links examples to what they demonstrate.

### 2.2 Cross-Reference Relationships

#### RELATED_TO (Concept → Concept)
```cypher
(:Concept)-[:RELATED_TO {
  relationship_type: string  // e.g., "prerequisite", "alternative", "component_of"
  strength: float            // Co-occurrence frequency

  // Evidence
  co_mention_count: int      // How often mentioned together
  source_transcript_ids: [string]

  // Temporal
  created_at: datetime
}]->(:Concept)
```

**Purpose**: Semantic relationships between concepts. Enables graph traversal for "What's related to X?"

#### BUILDS_ON (Concept → Concept)
```cypher
(:Concept)-[:BUILDS_ON {
  // Context
  description: string     // How A builds on B

  // Evidence
  source_utterance_ids: [string]

  // Temporal
  created_at: datetime
}]->(:Concept)
```

**Purpose**: Prerequisite/dependency relationships. Enables learning path queries.

#### CONTRADICTS (Belief → Belief)
```cypher
(:Belief)-[:CONTRADICTS {
  description: string     // Nature of contradiction
  severity: string        // direct|partial|nuanced

  // Evidence
  source_utterance_ids: [string]

  // Temporal
  detected_at: datetime
}]->(:Belief)
```

**Purpose**: Tracks conflicting positions. Enables debate/evolution tracking.

#### AGREES_WITH (Speaker → Speaker)
```cypher
(:Speaker)-[:AGREES_WITH {
  topic: string           // What they agree on
  strength: float         // Degree of alignment

  // Evidence
  supporting_utterance_ids: [string]

  // Temporal
  created_at: datetime
}]->(:Speaker)
```

**Purpose**: Tracks speaker alignment. Enables "Who agrees with X?" queries.

#### CITES (Utterance → Entity)
```cypher
(:Utterance)-[:CITES {
  // Context
  context: string         // How entity was referenced

  // Temporal
  created_at: datetime
}]->(:Entity)
```

**Purpose**: Explicit references to people, organizations, products.

### 2.3 Structural Relationships

#### PART_OF (Transcript → Session)
```cypher
(:Transcript)-[:PART_OF {
  episode_number: int
  created_at: datetime
}]->(:Session)
```

**Purpose**: Groups related transcripts.

#### SAME_AS (Speaker → Speaker | Concept → Concept)
```cypher
(:Speaker)-[:SAME_AS {
  confidence: float       // Entity resolution confidence
  method: string          // "fingerprint"|"name"|"manual"
  created_at: datetime
}]->(:Speaker)
```

**Purpose**: Entity deduplication. Graphiti handles this automatically but we track it.

---

## 3. Temporal Aspects

### 3.1 Bi-Temporal Model (Graphiti Native)

Graphiti provides bi-temporal tracking for edges:

- **valid_at**: When the fact was true in the real world (when it was stated in the video)
- **created_at**: When we ingested this fact into the graph
- **invalid_at**: When the fact became false (e.g., belief changed)

**Example**:
```python
# Video published Jan 2024: "I think agents should use JSON"
# Ingested into graph: Dec 2024
# Valid from: Jan 2024
# Created at: Dec 2024

# Later video published Mar 2024: "I now prefer structured outputs over JSON"
# This INVALIDATES the previous edge
# Original edge: invalid_at = Mar 2024
```

### 3.2 Temporal Query Patterns

#### Point-in-Time Queries
"What did Dan believe about agents in January 2024?"
```cypher
MATCH (s:Speaker {name: "Dan Shipper"})-[b:BELIEVES]->(belief:Belief)
WHERE b.valid_at <= datetime('2024-01-31T23:59:59Z')
  AND (b.invalid_at IS NULL OR b.invalid_at > datetime('2024-01-31T23:59:59Z'))
  AND belief.statement CONTAINS "agents"
RETURN belief.statement, b.strength
```

#### Evolution Tracking
"How has thinking on X evolved over time?"
```cypher
MATCH (c:Concept {name: "AI agents"})<-[m:MENTIONS]-(u:Utterance)<-[:CONTAINS]-(t:Transcript)
WITH c, u, m, t
ORDER BY t.source_created_at ASC
RETURN t.source_created_at, t.title, u.text, m.salience
```

#### Belief Changes
"When did speaker X change their position on Y?"
```cypher
MATCH (s:Speaker {name: "Dan Shipper"})-[b:BELIEVES]->(belief:Belief)
WHERE belief.statement CONTAINS "agents"
  AND b.invalid_at IS NOT NULL
WITH s, belief, b
ORDER BY b.valid_at
RETURN belief.statement, b.valid_at, b.invalid_at, b.strength
```

### 3.3 Temporal Node Properties

Store temporal snapshots in node properties:

```cypher
(:Concept {
  definition_changes: [
    {timestamp: "2024-01-15T10:00:00Z", definition: "...", source_tx: "tx_abc"},
    {timestamp: "2024-03-20T14:30:00Z", definition: "...", source_tx: "tx_def"}
  ]
})
```

This enables "How has the definition of X changed?" queries without complex edge traversal.

---

## 4. Cross-Transcript Links

### 4.1 Entity Resolution Strategy

**Challenge**: Same concept mentioned differently across transcripts.

**Solution**: Multi-stage resolution

#### Stage 1: Exact Match (Cheap)
```python
canonical_name = normalize(extracted_concept)  # lowercase, stemming
existing = graph.query("MATCH (c:Concept) WHERE c.name = $name OR $name IN c.aliases", name=canonical_name)
```

#### Stage 2: Embedding Similarity (Moderate Cost)
```python
embedding = embedder.embed(concept_name)
similar = graph.vector_search("Concept", "embedding", embedding, limit=5)
if max(similar).similarity > 0.95:
    return similar[0]  # Merge
```

#### Stage 3: LLM-Based Deduplication (Expensive, Graphiti Native)
```python
# Graphiti automatically does this during episode ingestion
await graphiti.add_episode(
    episode_body=utterance.text,
    entity_types={"Concept": ConceptSchema}
)
# Graphiti's entity deduplication will merge "LLM agents" and "language model agents"
```

### 4.2 Cross-Speaker Concept Aggregation

**Pattern**: Build DISCUSSES edges from SPOKE → MENTIONS paths

```cypher
// Aggregation query (run periodically or on-demand)
MATCH (s:Speaker)-[:SPOKE]->(u:Utterance)-[m:MENTIONS]->(c:Concept)
WITH s, c,
     count(m) as mention_count,
     min(m.valid_at) as first_mentioned,
     max(m.valid_at) as last_mentioned,
     collect(u.id) as utterance_ids
MERGE (s)-[d:DISCUSSES]->(c)
SET d.mention_count = mention_count,
    d.first_mentioned = first_mentioned,
    d.last_mentioned = last_mentioned,
    d.updated_at = datetime()
```

### 4.3 Cross-Transcript Concept Evolution

Track how a concept's definition/understanding changes:

```cypher
MATCH (c:Concept)<-[:MENTIONS]-(u:Utterance)<-[:CONTAINS]-(t:Transcript)
WHERE c.name = "AI agents"
WITH c, u, t
ORDER BY t.source_created_at ASC
WITH c, collect({
    date: t.source_created_at,
    context: u.text,
    transcript: t.title
}) as timeline
SET c.definition_changes = timeline
```

---

## 5. Query Patterns

### 5.1 Speaker-Centric Queries

#### "What does Dan believe about agents?"
```cypher
MATCH (s:Speaker {name: "Dan Shipper"})-[b:BELIEVES]->(belief:Belief)
WHERE belief.statement CONTAINS "agents"
  AND b.invalid_at IS NULL  // Current beliefs only
RETURN belief.statement, b.strength, b.first_stated
ORDER BY b.strength DESC
```

#### "What has Dan discussed in the last 6 months?"
```cypher
MATCH (s:Speaker {name: "Dan Shipper"})-[d:DISCUSSES]->(c:Concept)
WHERE d.last_mentioned >= datetime() - duration({months: 6})
RETURN c.name, d.mention_count, d.last_mentioned
ORDER BY d.mention_count DESC
LIMIT 10
```

#### "Find all speakers who discuss X"
```cypher
MATCH (s:Speaker)-[d:DISCUSSES]->(c:Concept {name: "knowledge graphs"})
RETURN s.name, d.mention_count, d.first_mentioned
ORDER BY d.mention_count DESC
```

### 5.2 Concept-Centric Queries

#### "How has thinking on X evolved?"
```cypher
MATCH (c:Concept {name: "AI agents"})<-[m:MENTIONS]-(u:Utterance)<-[:CONTAINS]-(t:Transcript)
WITH c, u, t, m
ORDER BY t.source_created_at ASC
RETURN t.source_created_at, t.title, u.text, m.salience
```

#### "What concepts are related to X?"
```cypher
MATCH (c1:Concept {name: "AI agents"})-[r:RELATED_TO]-(c2:Concept)
RETURN c2.name, r.relationship_type, r.strength, r.co_mention_count
ORDER BY r.strength DESC
LIMIT 10
```

#### "What are the prerequisites for understanding X?"
```cypher
MATCH path = (c:Concept {name: "multi-agent systems"})-[:BUILDS_ON*1..3]->(prereq:Concept)
RETURN prereq.name, length(path) as depth
ORDER BY depth
```

### 5.3 Technique-Centric Queries

#### "Show me examples of X"
```cypher
MATCH (t:Technique {name: "chain-of-thought prompting"})<-[:DEMONSTRATES]-(u:Utterance)
RETURN u.text, u.start_ms, u.end_ms
ORDER BY u.created_at DESC
LIMIT 5
```

#### "Who has demonstrated technique X?"
```cypher
MATCH (s:Speaker)-[:SPOKE]->(u:Utterance)-[:DEMONSTRATES]->(t:Technique {name: "ReAct pattern"})
WITH s, count(u) as demo_count
RETURN s.name, demo_count
ORDER BY demo_count DESC
```

### 5.4 Discovery Queries

#### "What are the most discussed topics?"
```cypher
MATCH (c:Concept)
RETURN c.name, c.mention_count, c.speaker_count
ORDER BY c.mention_count DESC
LIMIT 20
```

#### "Who are the most active speakers?"
```cypher
MATCH (s:Speaker)
RETURN s.name, s.transcript_count, s.utterance_count, s.total_speaking_time_ms
ORDER BY s.total_speaking_time_ms DESC
LIMIT 10
```

#### "Find controversial topics (high disagreement)"
```cypher
MATCH (c:Concept)<-[:DISCUSSES]-(s:Speaker)
WITH c, count(DISTINCT s) as speaker_count
WHERE speaker_count > 3
MATCH (c)<-[d:DISCUSSES]-(s:Speaker)
WITH c, speaker_count, stdev(d.mention_count) as variance
RETURN c.name, speaker_count, variance
ORDER BY variance DESC
LIMIT 10
```

### 5.5 Temporal Queries

#### "What was said about X in time range Y?"
```cypher
MATCH (c:Concept {name: "AI agents"})<-[m:MENTIONS]-(u:Utterance)<-[:CONTAINS]-(t:Transcript)
WHERE t.source_created_at >= datetime('2024-01-01')
  AND t.source_created_at <= datetime('2024-03-31')
RETURN t.title, t.source_created_at, u.text
ORDER BY t.source_created_at
```

#### "Track belief evolution for speaker X on topic Y"
```cypher
MATCH (s:Speaker {name: "Dan Shipper"})-[b:BELIEVES]->(belief:Belief)
WHERE belief.statement CONTAINS "AI agents"
WITH s, belief, b
ORDER BY b.valid_at
RETURN belief.statement, b.strength, b.valid_at, b.invalid_at
```

### 5.6 Graph Traversal Queries

#### "Find speakers connected through concept X"
```cypher
MATCH (s1:Speaker)-[:DISCUSSES]->(c:Concept {name: "knowledge graphs"})<-[:DISCUSSES]-(s2:Speaker)
WHERE s1 <> s2
RETURN s1.name, s2.name, c.name
```

#### "Multi-hop reasoning: Who influenced X's thinking on Y?"
```cypher
// Find speakers who discussed a concept before speaker X
MATCH (target:Speaker {name: "Dan Shipper"})-[d1:DISCUSSES]->(c:Concept {name: "AI agents"})
WITH target, c, d1.first_mentioned as target_first_mention
MATCH (influencer:Speaker)-[d2:DISCUSSES]->(c)
WHERE d2.first_mentioned < target_first_mention
  AND influencer <> target
RETURN influencer.name, d2.first_mentioned, d2.mention_count
ORDER BY d2.first_mentioned
```

---

## 6. Pipeline Architecture

### 6.1 Ingestion Flow

```
YouTube Video → Transcript Extraction → Knowledge Graph Ingestion
                      ↓
    [Whisper Transcription + Diarization]
                      ↓
    Transcript Entity (tx_*) with Utterances
                      ↓
    [Graphiti Episode Processing]
                      ↓
    ┌─────────────────┴─────────────────┐
    ↓                                    ↓
Speaker Nodes                    Concept/Entity Extraction
Voice Fingerprints              (LLM-based, Graphiti native)
SPOKE edges                              ↓
                        Concept/Entity/Technique Nodes
                                         ↓
                        MENTIONS/DISCUSSES/BELIEVES edges
                                         ↓
                        Relationship Extraction
                                         ↓
                        RELATED_TO/BUILDS_ON/CONTRADICTS edges
```

### 6.2 Processing Stages

#### Stage 1: Transcript Creation (Existing)
- Input: YouTube URL
- Output: Transcript entity with utterances
- Duration: ~10-30 min per hour of audio
- Storage: JSON files in transcript storage

#### Stage 2: Graphiti Episode Ingestion (New)
- Input: Transcript entity (utterances)
- Processing:
  - Convert each utterance to Graphiti episode
  - Attach speaker context
  - Attach temporal context (video publish date)
- Output: EntityNodes, EpisodicNodes in FalkorDB
- Duration: ~5-15 min per hour of audio (depends on LLM)

#### Stage 3: Knowledge Extraction (New)
- Input: Graphiti graph with episodes
- Processing:
  - Extract high-level concepts (aggregation)
  - Extract techniques (pattern matching)
  - Extract beliefs (stance detection)
  - Extract examples (demonstration detection)
- Output: Concept/Technique/Belief/Example nodes
- Duration: ~10-20 min per hour of audio

#### Stage 4: Relationship Inference (New)
- Input: Knowledge graph with entities
- Processing:
  - RELATED_TO (co-occurrence analysis)
  - BUILDS_ON (dependency extraction)
  - CONTRADICTS (conflict detection)
  - AGREES_WITH (alignment detection)
- Output: Relationship edges
- Duration: ~5-10 min per transcript

#### Stage 5: Aggregation (Periodic)
- Input: Complete knowledge graph
- Processing:
  - Build DISCUSSES edges from SPOKE → MENTIONS
  - Update statistics on nodes
  - Detect temporal patterns
- Output: Updated aggregated edges
- Duration: ~1-5 min per run
- Frequency: Daily or on-demand

### 6.3 Hybrid Index Strategy

**Problem**: Graphiti expects episodes as input, but we have structured entities (Speaker, Transcript, Utterance).

**Solution**: Dual storage

#### FalkorDB Schema
```
Graphiti Layer:
- EpisodeNode (one per utterance)
- EntityNode (concepts, speakers merged by Graphiti)
- EntityEdge (relationships, bi-temporal)

Custom Layer:
- Speaker (from transcripts plugin domain model)
- Transcript (from transcripts plugin domain model)
- Utterance (from transcripts plugin domain model)

Bridge:
- Episode.source_utterance_id → Utterance.id
- EntityNode.speaker_id → Speaker.id
```

#### Why Both?

1. **Graphiti layer**: Temporal reasoning, semantic search, automatic deduplication
2. **Custom layer**: Precise speaker attribution, voice fingerprinting, transcript metadata

#### Query Strategy

- **"What did Dan say about agents?"** → Start from Speaker (custom), traverse to EntityNode (Graphiti)
- **"How has thinking on agents evolved?"** → Pure Graphiti (temporal queries)
- **"Find all speakers in this video"** → Pure custom layer (transcript metadata)

---

## 7. Graphiti Integration Details

### 7.1 Episode Format

Each utterance becomes a Graphiti episode:

```python
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType

async def ingest_transcript(transcript: Transcript, graphiti: Graphiti):
    for utterance in transcript.utterances:
        await graphiti.add_episode(
            name=f"{transcript.id}_{utterance.id}",
            episode_body=f"[{utterance.speaker.name}]: {utterance.text}",
            source=EpisodeType.message,
            source_description=f"YouTube: {transcript.title}",
            reference_time=transcript.source_created_at + timedelta(milliseconds=utterance.start_ms),
            group_id=transcript.id,  # Namespace per transcript
            metadata={
                "transcript_id": transcript.id,
                "utterance_id": utterance.id,
                "speaker_id": utterance.speaker.id,
                "start_ms": utterance.start_ms,
                "end_ms": utterance.end_ms,
                "platform": "youtube",
                "source_url": transcript.source.url
            }
        )
```

### 7.2 Custom Entity Types

Define domain-specific schemas for better extraction:

```python
from pydantic import BaseModel, Field

class Concept(BaseModel):
    """Abstract idea, technique, or topic"""
    name: str = Field(description="Canonical concept name")
    category: str | None = Field(None, description="technique|belief|technology|method")
    description: str | None = Field(None, description="Brief explanation")

class Technique(BaseModel):
    """Actionable method or approach"""
    name: str = Field(description="Technique name")
    description: str = Field(description="What this technique does")
    complexity: str | None = Field(None, description="beginner|intermediate|advanced")

class Belief(BaseModel):
    """Expressed position or opinion"""
    statement: str = Field(description="The belief statement")
    polarity: str | None = Field(None, description="positive|negative|neutral")
    strength: str | None = Field(None, description="strong|moderate|weak")

class Example(BaseModel):
    """Concrete instance or demonstration"""
    description: str = Field(description="What this example shows")
    context: str | None = Field(None, description="Surrounding context")

class SpeakerEntity(BaseModel):
    """Reference to a speaker (for linking)"""
    name: str = Field(description="Speaker name")
    role: str | None = Field(None, description="Role or title if mentioned")
```

Use during ingestion:

```python
await graphiti.add_episode(
    name=f"{transcript.id}_{utterance.id}",
    episode_body=utterance.text,
    entity_types={
        "Concept": Concept,
        "Technique": Technique,
        "Belief": Belief,
        "Example": Example,
        "Speaker": SpeakerEntity
    },
    edge_types={
        "DEMONSTRATES": {"description": str},
        "BUILDS_ON": {"description": str},
        "CONTRADICTS": {"severity": str}
    }
)
```

### 7.3 Search Patterns

#### Semantic Search
```python
# Find facts about "AI agents"
results = await graphiti.search("AI agents", limit=10)
for edge in results.edges:
    print(f"{edge.fact} (valid: {edge.valid_at})")
```

#### Filtered Search
```python
from graphiti_core.search.search_filters import SearchFilters

# Only search within specific transcript
filters = SearchFilters(
    group_ids=[transcript_id]
)
results = await graphiti.search("knowledge graphs", filters=filters)
```

#### Temporal Search
```python
# What was said in Q1 2024?
filters = SearchFilters(
    created_at_start=datetime(2024, 1, 1, tzinfo=timezone.utc),
    created_at_end=datetime(2024, 3, 31, tzinfo=timezone.utc)
)
results = await graphiti.search("AI agents", filters=filters)
```

#### Graph-Aware Reranking
```python
# Find concepts related to a center node
initial_results = await graphiti.search("knowledge graphs")
if initial_results.edges:
    center_node_uuid = initial_results.edges[0].source_node_uuid

    # Rerank by graph distance
    reranked = await graphiti.search(
        "knowledge graphs",
        center_node_uuid=center_node_uuid
    )
```

---

## 8. Obsidian/Quartz Visualization

### 8.1 Graph View Mapping

**Challenge**: Quartz expects markdown files with wikilinks. Graphiti stores data in FalkorDB.

**Solution**: Generate markdown files from graph data

#### Export Strategy

```python
async def export_to_obsidian(graphiti: Graphiti, output_dir: Path):
    """Export knowledge graph to Obsidian-compatible markdown"""

    # Export speakers
    speakers_dir = output_dir / "speakers"
    speakers_dir.mkdir(exist_ok=True)

    speakers = await get_all_speakers(graphiti)
    for speaker in speakers:
        content = f"""# {speaker.name}

**Transcripts**: {speaker.transcript_count}
**Speaking Time**: {format_duration(speaker.total_speaking_time_ms)}
**First Appearance**: {speaker.first_appearance}

## Discusses

{await get_speaker_concepts(speaker.id)}

## Beliefs

{await get_speaker_beliefs(speaker.id)}

## Transcripts

{await get_speaker_transcripts(speaker.id)}
"""
        (speakers_dir / f"{speaker.id}.md").write_text(content)

    # Export concepts
    concepts_dir = output_dir / "concepts"
    concepts_dir.mkdir(exist_ok=True)

    concepts = await get_all_concepts(graphiti)
    for concept in concepts:
        content = f"""# {concept.name}

{concept.description}

**Category**: {concept.category}
**Mentions**: {concept.mention_count}
**Speakers**: {concept.speaker_count}

## Discussed By

{await get_concept_speakers(concept.id)}

## Related Concepts

{await get_related_concepts(concept.id)}

## Examples

{await get_concept_examples(concept.id)}
"""
        (concepts_dir / f"{slugify(concept.name)}.md").write_text(content)
```

#### Wikilink Generation

```python
async def get_speaker_concepts(speaker_id: str) -> str:
    """Generate wikilinks for speaker's concepts"""
    results = await graphiti.driver.execute_query(
        "MATCH (s:Speaker {id: $id})-[d:DISCUSSES]->(c:Concept) RETURN c.name, d.mention_count ORDER BY d.mention_count DESC LIMIT 20",
        id=speaker_id
    )

    lines = []
    for record in results:
        concept_name = record['c.name']
        mention_count = record['d.mention_count']
        lines.append(f"- [[{concept_name}]] ({mention_count} mentions)")

    return "\n".join(lines)
```

### 8.2 Quartz Configuration

```typescript
// quartz.config.ts
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Transcripts Knowledge Graph",
    enablePopovers: true,
  },
  plugins: {
    transformers: [...],
    filters: [
      Plugin.RemoveDrafts(),
    ],
    emitters: [
      Plugin.ContentIndex(),  // Generates link graph
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.Graph({
        localGraph: {
          depth: 2,
          showTags: true,
        },
        globalGraph: {
          depth: -1,  // Show all connections
          repelForce: 0.8,
          centerForce: 0.3,
          linkDistance: 50,
        },
      }),
    ],
  },
}
```

### 8.3 Custom Visualization Endpoint

Alternative: Serve graph data directly from FalkorDB

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/api/graph/speakers")
async def get_speaker_graph():
    """Return speaker-concept graph in D3 format"""
    query = """
    MATCH (s:Speaker)-[d:DISCUSSES]->(c:Concept)
    WHERE d.mention_count > 5
    RETURN s, c, d
    """

    results = await graphiti.driver.execute_query(query)

    nodes = []
    links = []
    node_ids = set()

    for record in results:
        speaker = record['s']
        concept = record['c']
        discusses = record['d']

        if speaker.id not in node_ids:
            nodes.append({
                "id": speaker.id,
                "name": speaker.name,
                "type": "speaker",
                "size": speaker.transcript_count
            })
            node_ids.add(speaker.id)

        if concept.id not in node_ids:
            nodes.append({
                "id": concept.id,
                "name": concept.name,
                "type": "concept",
                "size": concept.mention_count
            })
            node_ids.add(concept.id)

        links.append({
            "source": speaker.id,
            "target": concept.id,
            "value": discusses.mention_count
        })

    return JSONResponse({"nodes": nodes, "links": links})
```

### 8.4 Interactive Views

Define multiple graph views:

1. **Speaker Network**: Speakers connected by shared concepts
2. **Concept Map**: Concepts connected by RELATED_TO/BUILDS_ON
3. **Temporal View**: Time-axis layout showing concept evolution
4. **Belief Evolution**: Track position changes over time

Each view queries FalkorDB and renders using D3 + PixiJS.

---

## 9. Performance Considerations

### 9.1 Scalability Targets

- **2800+ transcripts**: ~280 hours of content (assuming 6 min avg)
- **~50,000 utterances**: ~30 utterances per 6-min video
- **~10,000 concepts**: Assuming moderate redundancy
- **~100 speakers**: Assuming 28 speakers per video (multi-speaker content)

### 9.2 FalkorDB Configuration

```python
# High-performance configuration
driver = FalkorDriver(
    host="localhost",
    port=6379,
    password="password",
    database="transcripts_kg",
    max_pool_size=20,  # Increase connection pool
    timeout=30000      # 30 second timeout for complex queries
)
```

### 9.3 Batch Processing Strategy

Process transcripts in batches to avoid rate limits:

```python
async def ingest_all_transcripts(transcripts: list[Transcript], batch_size: int = 10):
    """Ingest transcripts in batches"""
    for i in range(0, len(transcripts), batch_size):
        batch = transcripts[i:i+batch_size]

        # Process batch in parallel
        tasks = [ingest_transcript(t, graphiti) for t in batch]
        await asyncio.gather(*tasks, return_exceptions=True)

        print(f"Processed {i+len(batch)}/{len(transcripts)}")

        # Rate limiting pause
        await asyncio.sleep(5)
```

### 9.4 Index Optimization

```cypher
// Create indices on frequently queried properties
CREATE INDEX speaker_name FOR (s:Speaker) ON (s.name)
CREATE INDEX concept_name FOR (c:Concept) ON (c.name)
CREATE INDEX transcript_date FOR (t:Transcript) ON (t.source_created_at)
CREATE INDEX utterance_embedding FOR (u:Utterance) ON (u.embedding)

// Composite indices for common query patterns
CREATE INDEX speaker_discusses FOR ()-[d:DISCUSSES]->() ON (d.mention_count, d.last_mentioned)
```

### 9.5 Query Optimization

Use query plans for complex traversals:

```cypher
// Efficient: Start from specific speaker
MATCH (s:Speaker {name: "Dan Shipper"})-[:DISCUSSES]->(c:Concept)
WHERE c.mention_count > 10
RETURN c
// Fast: Uses speaker_name index, filters early

// Inefficient: Scan all concepts first
MATCH (c:Concept)
WHERE c.mention_count > 10
MATCH (s:Speaker {name: "Dan Shipper"})-[:DISCUSSES]->(c)
RETURN c
// Slow: Scans all concepts before filtering
```

---

## 10. Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Set up FalkorDB instance
- [ ] Configure Graphiti client
- [ ] Define custom entity schemas (Concept, Technique, Belief, Example)
- [ ] Implement basic episode ingestion pipeline
- [ ] Test with 10 sample transcripts

### Phase 2: Knowledge Extraction (Week 3-4)
- [ ] Implement concept extraction
- [ ] Implement technique extraction
- [ ] Implement belief extraction
- [ ] Implement example extraction
- [ ] Build aggregation queries (DISCUSSES edges)

### Phase 3: Relationship Inference (Week 5-6)
- [ ] Implement RELATED_TO inference (co-occurrence)
- [ ] Implement BUILDS_ON inference (dependency detection)
- [ ] Implement CONTRADICTS inference (conflict detection)
- [ ] Implement AGREES_WITH inference (alignment detection)

### Phase 4: Query Interface (Week 7-8)
- [ ] Design query API
- [ ] Implement speaker-centric queries
- [ ] Implement concept-centric queries
- [ ] Implement technique-centric queries
- [ ] Implement temporal queries

### Phase 5: Visualization (Week 9-10)
- [ ] Export to Obsidian markdown
- [ ] Configure Quartz for graph visualization
- [ ] Implement custom visualization endpoint
- [ ] Create interactive views (speaker network, concept map, temporal)

### Phase 6: Batch Processing (Week 11-12)
- [ ] Implement batch ingestion pipeline
- [ ] Process all 2800 transcripts
- [ ] Optimize query performance
- [ ] Build monitoring/health checks

### Phase 7: Integration (Week 13-14)
- [ ] Create slash commands (/kg-search, /kg-speaker, /kg-concept)
- [ ] Create subagent for graph queries
- [ ] Document query patterns
- [ ] Create user guide

---

## 11. Commands & Subagents

### 11.1 Slash Commands

```typescript
// commands/kg-ingest.ts
export async function kgIngest(args: {transcript_id?: string, batch_size?: number}) {
  if (args.transcript_id) {
    // Ingest single transcript
    await ingestTranscript(args.transcript_id)
  } else {
    // Ingest all pending transcripts
    await ingestBatch(args.batch_size || 10)
  }
}
```

```typescript
// commands/kg-search.ts
export async function kgSearch(args: {query: string, type?: "speaker"|"concept"|"technique"}) {
  const results = await graphiti.search(args.query, {
    filters: args.type ? {entity_types: [args.type]} : undefined
  })
  return formatResults(results)
}
```

```typescript
// commands/kg-speaker.ts
export async function kgSpeaker(args: {name: string}) {
  const speaker = await getSpeaker(args.name)
  const concepts = await getSpeakerConcepts(speaker.id)
  const beliefs = await getSpeakerBeliefs(speaker.id)

  return {
    speaker,
    top_concepts: concepts.slice(0, 10),
    recent_beliefs: beliefs.filter(b => b.invalid_at === null)
  }
}
```

### 11.2 Subagent

```markdown
---
name: kg-explorer
description: Query the transcripts knowledge graph. Ask questions about speakers, concepts, beliefs, techniques, or temporal evolution.
tools: Read, Bash, Grep
model: sonnet
---

# Knowledge Graph Explorer

You are an expert at querying the transcripts knowledge graph built with Graphiti and FalkorDB.

## Your Capabilities

1. **Speaker Queries**: "What does X discuss?", "Who has spoken about Y?"
2. **Concept Queries**: "How has thinking on X evolved?", "What's related to Y?"
3. **Technique Queries**: "Show me examples of X", "Who demonstrates Y?"
4. **Temporal Queries**: "What was said about X in 2024?", "How has X's position changed?"
5. **Discovery**: "What are the most discussed topics?", "Find controversial beliefs"

## Query Patterns

Use Cypher queries via the FalkorDB driver:

```python
from plugins.transcripts.src.kg.client import get_kg_client

async def query():
    kg = await get_kg_client()
    result = await kg.driver.execute_query("""
        MATCH (s:Speaker {name: $name})-[d:DISCUSSES]->(c:Concept)
        RETURN c.name, d.mention_count
        ORDER BY d.mention_count DESC
        LIMIT 10
    """, name="Dan Shipper")
    return result
```

## Output Format

Always provide:
1. Natural language summary
2. Raw query results (top 10)
3. Suggested follow-up queries
```

---

## 12. Open Questions

1. **Entity Resolution Threshold**: What similarity score triggers automatic merging? (Current Graphiti default: ~0.9)
2. **Belief Extraction**: Rule-based or pure LLM? (Recommend: LLM with few-shot examples)
3. **Aggregation Frequency**: Real-time or batch? (Recommend: Daily batch + on-demand)
4. **Storage Split**: Should we duplicate data between Graphiti and custom layer? (Recommend: Yes, for performance)
5. **Visualization Priority**: Obsidian export or custom endpoint first? (Recommend: Custom endpoint for flexibility)

---

## 13. References

### Internal Documents
- `/home/ygg/Workspace/sandbox/marketplaces/claude/plugins/transcripts/src/domain/entities/`
- `/home/ygg/Workspace/sandbox/marketplaces/claude/plugins/knowledge-graphs/skills/kg-master/subskills/graphiti.md`

### External Resources
- Graphiti Documentation: https://github.com/getzep/graphiti
- FalkorDB Documentation: https://docs.falkordb.com/
- Quartz Graph View: https://quartz.jzhao.xyz/features/graph-view

---

**End of Specification**
