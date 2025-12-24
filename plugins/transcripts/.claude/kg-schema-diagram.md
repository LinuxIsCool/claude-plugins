# Knowledge Graph Schema Diagram

Visual representation of the transcripts knowledge graph schema.

## Node-Edge Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     TRANSCRIPTS KNOWLEDGE GRAPH                      │
└─────────────────────────────────────────────────────────────────────┘

PRIMARY NODES                    EDGE TYPES                  SUPPORTING NODES
════════════                    ════════════                ════════════════

┌──────────┐                                                ┌──────────┐
│ Speaker  │◄────────────── SPOKE ─────────────────────────│Utterance │
│          │                                                │          │
│ id       │◄─────────── DISCUSSES ────────┐               │ text     │
│ name     │                                │               │ start_ms │
│ voice    │◄────────── BELIEVES ────┐     │               │ end_ms   │
└─────┬────┘                          │     │               └────┬─────┘
      │                               │     │                    │
      │                               │     │                    │
      │                               │     │                    │
      │                               │     │                    │
      └──── AGREES_WITH ──────►       │     │                    │
                                      │     │                    │
┌──────────┐                          │     │                    │
│ Belief   │◄─────────────────────────┘     │                    │
│          │                                 │                    │
│statement │◄───── CONTRADICTS ──────►       │                    │
│ strength │                                 │                    │
│ polarity │                                 │                    │
└──────────┘                                 │                    │
                                             │                    │
┌──────────┐                                 │                    │
│ Concept  │◄────────────────────────────────┘                    │
│          │◄────────── MENTIONS ────────────────────────────────┘
│ name     │
│ category │◄───── RELATED_TO ───────►
│ domain   │
└────┬─────┘
     │
     └──────── BUILDS_ON ──────►

┌──────────┐
│Technique │◄────── DEMONSTRATES ──────────────────────────┐
│          │                                                │
│ name     │                                                │
│ category │                                                │
└──────────┘                                                │
                                                            │
┌──────────┐                                                │
│ Example  │────────────────────────────────────────────────┘
│          │
│ text     │◄──── PROVIDES_EXAMPLE ──────────────────┐
│ context  │                                          │
└────┬─────┘                                          │
     │                                                 │
     └──── EXEMPLIFIES ──────► (Concept/Technique)    │
                                                      │
┌──────────┐                                          │
│Transcript│─────── CONTAINS ─────────────────────────┘
│          │
│ title    │◄──────── PART_OF ──────────┐
│ source   │                             │
│ duration │                             │
└──────────┘                             │
                                         │
┌──────────┐                             │
│ Session  │─────────────────────────────┘
│          │
│ name     │
│ series   │
└──────────┘

┌──────────┐
│  Entity  │◄──────── CITES ──────────────────────┐
│          │                                       │
│ type     │                                       │
│ name     │                               (Utterance)
└──────────┘

┌──────────┐
│  Topic   │◄──────── MENTIONS ────────────────────┘
│          │
│ keywords │
└──────────┘
```

## Data Flow Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                      INGESTION PIPELINE                           │
└──────────────────────────────────────────────────────────────────┘

YouTube Video
     │
     ▼
[Whisper Transcription]
     │
     ▼
Transcript + Utterances ────────────────────────────┐
     │                                              │
     │                                              │
     ▼                                              ▼
┌─────────────────┐                       ┌─────────────────┐
│  CUSTOM LAYER   │                       │ GRAPHITI LAYER  │
│   (FalkorDB)    │                       │   (FalkorDB)    │
├─────────────────┤                       ├─────────────────┤
│ • Speaker       │                       │ • EpisodeNode   │
│ • Transcript    │                       │ • EntityNode    │
│ • Utterance     │                       │ • EntityEdge    │
│ • Topic         │                       │ • CommunityNode │
│                 │                       │                 │
│ Voice           │                       │ Temporal KG     │
│ fingerprints    │                       │ Auto-dedup      │
│ Metadata        │                       │ Bi-temporal     │
└────────┬────────┘                       └────────┬────────┘
         │                                         │
         │         ┌──────────────┐                │
         └────────►│ QUERY LAYER  │◄───────────────┘
                   ├──────────────┤
                   │ • Speaker    │
                   │ • Concept    │
                   │ • Temporal   │
                   │ • Discovery  │
                   └──────┬───────┘
                          │
                          ▼
               ┌──────────────────────┐
               │  VISUALIZATION LAYER │
               ├──────────────────────┤
               │ • Obsidian Export    │
               │ • Quartz Graph       │
               │ • D3 Custom Views    │
               └──────────────────────┘
```

## Query Pattern Examples

```
┌──────────────────────────────────────────────────────────────────┐
│                   EXAMPLE QUERY PATTERNS                          │
└──────────────────────────────────────────────────────────────────┘

1. SPEAKER-CENTRIC: "What does Dan discuss?"

   (Speaker: Dan)─[DISCUSSES]→(Concept: AI agents)
                             └→(Concept: knowledge graphs)
                             └→(Concept: tool use)

2. CONCEPT EVOLUTION: "How has thinking on X evolved?"

   Timeline ────────────────────────────────────────────►

   Jan 2024: (Utterance)─[MENTIONS]→(Concept: AI agents)
             "I think agents should use JSON"

   Mar 2024: (Utterance)─[MENTIONS]→(Concept: AI agents)
             "I now prefer structured outputs"

   Jun 2024: (Utterance)─[MENTIONS]→(Concept: AI agents)
             "Tool calling is the best approach"

3. MULTI-HOP REASONING: "What concepts build on X?"

   (Concept: prompting)←[BUILDS_ON]─(Concept: chain-of-thought)
                                    └[BUILDS_ON]─(Concept: ReAct)
                                                └[BUILDS_ON]─(Concept: agents)

4. BELIEF TRACKING: "Track position changes"

   (Speaker: Dan)─[BELIEVES]→(Belief: "Agents need planning")
                  ├─ valid_at: 2024-01-15
                  ├─ invalid_at: 2024-03-20
                  └─ strength: strong

   (Speaker: Dan)─[BELIEVES]→(Belief: "Agents work best reactively")
                  ├─ valid_at: 2024-03-20
                  ├─ invalid_at: NULL
                  └─ strength: moderate

5. CROSS-SPEAKER: "Who agrees with X?"

   (Speaker: Dan)─[AGREES_WITH]→(Speaker: Ethan)
                 ├─ topic: "AI agents"
                 └─ strength: 0.85
```

## Temporal Schema

```
┌──────────────────────────────────────────────────────────────────┐
│                    BI-TEMPORAL MODEL                              │
└──────────────────────────────────────────────────────────────────┘

Every Edge Has:

┌─────────────────────────────────────────────────────────────────┐
│ EntityEdge                                                       │
├─────────────────────────────────────────────────────────────────┤
│ valid_at       : datetime   # When fact was true (real world)   │
│ invalid_at     : datetime   # When fact became false            │
│ created_at     : datetime   # When we learned this fact         │
└─────────────────────────────────────────────────────────────────┘

Example Timeline:

Real-World Time (valid_at) ──────────────────────────────────────►

Jan 2024                Mar 2024                Jun 2024
   │                       │                       │
   │ "Kamala is AG"        │ "Kamala is Senator"   │
   │                       │                       │
   ├───────────────────────┤                       │
   │  Edge 1               │  Edge 2               │
   │  valid_at: Jan 2024   │  valid_at: Mar 2024   │
   │  invalid_at: Mar 2024 │  invalid_at: NULL     │
   └───────────────────────┴───────────────────────┘

Ingestion Time (created_at) ──────────────────────────────────────►

                     Both edges created Dec 2024
                     when we processed the videos
```

## Graph Statistics (Projected)

```
┌──────────────────────────────────────────────────────────────────┐
│                  EXPECTED GRAPH SIZE                              │
└──────────────────────────────────────────────────────────────────┘

Based on 2800 transcripts @ 6 min avg:

NODES:
  Transcript       2,800        (1 per video)
  Utterance       50,000        (~18 per transcript)
  Speaker            100        (assuming multi-speaker content)
  Concept         10,000        (with deduplication)
  Technique        1,000        (subset of concepts)
  Belief           5,000        (opinions expressed)
  Example          3,000        (demonstrations)
  Entity           5,000        (people, orgs, products)
  Topic              500        (high-level themes)
  Session            200        (grouped content)
  ───────────────────────
  TOTAL           77,600 nodes

EDGES:
  SPOKE           50,000        (utterances → speakers)
  CONTAINS        50,000        (transcripts → utterances)
  MENTIONS       150,000        (utterances → concepts/entities)
  DISCUSSES       10,000        (speakers → concepts, aggregated)
  BELIEVES        10,000        (speakers → beliefs)
  DEMONSTRATES     5,000        (utterances → techniques)
  RELATED_TO      20,000        (concepts ↔ concepts)
  BUILDS_ON        2,000        (concepts → concepts)
  CONTRADICTS      1,000        (beliefs ↔ beliefs)
  AGREES_WITH        500        (speakers ↔ speakers)
  CITES           10,000        (utterances → entities)
  ───────────────────────
  TOTAL          308,500 edges

STORAGE (estimated):
  Graph data:       ~2 GB
  Embeddings:      ~15 GB (assuming 1536-dim vectors)
  Full-text:       ~500 MB
  ───────────────────────
  TOTAL            ~17.5 GB
```

## Visualization Layouts

```
┌──────────────────────────────────────────────────────────────────┐
│                    GRAPH VIEW TYPES                               │
└──────────────────────────────────────────────────────────────────┘

1. SPEAKER NETWORK (Force-Directed)

        Dan ────────── Ethan
         │ \           /
         │  \         /
         │   \       /
         │    \     /
         │     \   /
         │      \ /
        Sam ─── Alex

   Nodes: Speakers
   Edges: AGREES_WITH (weighted by strength)
   Layout: Force-directed, edge weight = link distance

2. CONCEPT MAP (Hierarchical)

              AI
               │
       ┌───────┼───────┐
       │       │       │
    Agents  Prompts  RAG
       │       │       │
    ┌──┼──┐  ┌┼┐   ┌──┼──┐
   ReAct Tool CoT BM25 Vector

   Nodes: Concepts
   Edges: BUILDS_ON
   Layout: Tree, depth = prerequisite chain

3. TEMPORAL VIEW (Timeline)

   Time ────────────────────────────────────────────────►

   2024-01
     │  ● "JSON for agents"
     │
   2024-03
     │  ● "Structured outputs better"
     │
   2024-06
     │  ● "Tool calling is best"

   Nodes: Utterances
   X-axis: Timestamp
   Y-axis: Concept (grouped)

4. KNOWLEDGE DENSITY (Heatmap)

   Speaker │ AI Agents │ KG │ RAG │ Prompts
   ────────┼───────────┼────┼─────┼────────
   Dan     │    ████   │ ██ │ ███ │   █
   Ethan   │    ██     │ ██ │  █  │  ███
   Sam     │    █      │ ██ │ ███ │   ██

   Color intensity = mention_count
```

---

**File Purpose**: Supplement to knowledge-graph-architecture.md
**Created**: 2025-12-24
**Author**: obsidian-quartz agent
