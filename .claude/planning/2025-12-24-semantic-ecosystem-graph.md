# Semantic Ecosystem Intelligence Graph

*Embedding everything, connecting everything, understanding everything*

## Vision

A unified knowledge graph where every artifact in the ecosystem is:
1. **Embedded** - Vector representation for semantic similarity
2. **Connected** - Graph relationships to other entities
3. **Queryable** - Semantic search + graph traversal
4. **ToM-Mapped** - Linked to personality/identity dimensions

## Current State

**FalkorDB Production Graph** (from `temporal-kg-memory`):
- 468 nodes (Sessions, UserMessages, AssistantMessages)
- 794 relationships (IN_SESSION, THEN)
- 52 sessions ingested
- Query tools working

**Gap**: Only conversation logs. Missing:
- Planning documents (30 files)
- Git commits
- Agent definitions
- Skills
- Semantic embeddings
- ToM dimension mapping

## Target Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SEMANTIC ECOSYSTEM GRAPH                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                               │
│  ENTITY LAYER                                                                 │
│  ────────────                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │ Planning │   │  Commit  │   │  Agent   │   │  Prompt  │   │  ToM     │   │
│  │   Doc    │   │          │   │          │   │          │   │ Dimension│   │
│  │ +embed   │   │ +embed   │   │ +embed   │   │ +embed   │   │ +evidence│   │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   └──────────┘   │
│       │              │              │              │              │          │
│       └──────────────┴──────────────┴──────────────┴──────────────┘          │
│                                     │                                         │
│  RELATIONSHIP LAYER                 ▼                                         │
│  ──────────────────                                                           │
│  • RESULTED_IN:     Prompt → Commit (what work resulted)                      │
│  • MENTIONS:        Prompt → Agent (which agents referenced)                  │
│  • REFERENCES:      Prompt → PlanningDoc (planning context)                   │
│  • IMPLEMENTED_BY:  PlanningDoc → Commit (planning → execution)               │
│  • SPECIFIES:       PlanningDoc → Agent (planning → design)                   │
│  • EVIDENCES:       Prompt → ToMDimension (personality evidence)              │
│  • SIMILAR_TO:      Entity → Entity (embedding similarity > 0.8)              │
│                                                                               │
│  EMBEDDING LAYER                                                              │
│  ───────────────                                                              │
│  • Model: text-embedding-3-small (OpenAI) or nomic-embed-text (Ollama)       │
│  • Dimensions: 1536 (OpenAI) or 768 (Ollama)                                 │
│  • Storage: FalkorDB vector index                                             │
│  • Similarity: Cosine distance for SIMILAR_TO edges                          │
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Schema Extension

### New Node Types

```cypher
// Planning Documents
(:PlanningDoc {
    id: "planning-2025-12-13-fusion",
    path: ".claude/planning/2025-12-13-fusion.md",
    title: "Fusion Vision",
    created: datetime,
    word_count: int,
    embedding: vector<1536>
})

// Git Commits
(:Commit {
    hash: "abc123",
    short_hash: "abc123",
    timestamp: datetime,
    message: "text",
    author: "name",
    files_changed: int,
    insertions: int,
    deletions: int,
    embedding: vector<1536>  // of commit message + files
})

// Agents (existing + plugin)
(:Agent {
    id: "conductor",
    path: ".claude/agents/conductor.md",
    name: "Conductor",
    description: "Central consciousness...",
    model: "opus",
    tools: ["Read", "Write", ...],
    embedding: vector<1536>
})

// Skills
(:Skill {
    id: "awareness:temporal-kg-memory",
    path: "plugins/awareness/skills/temporal-kg-memory/...",
    name: "Temporal KG Memory",
    description: "...",
    embedding: vector<1536>
})

// Enhanced User Prompts (extend existing UserMessage)
(:UserPrompt {
    ... existing fields ...,
    embedding: vector<1536>,
    tom_signals: [list of dimension IDs with evidence]
})

// Theory of Mind Dimensions
(:ToMDimension {
    id: "cognitive-style",
    name: "Cognitive Style",
    description: "How they think...",
    current_assessment: "Analytical/Systematic",
    confidence: 0.85,
    observation_count: 15
})
```

### New Relationship Types

```cypher
// Prompt → Result chain
(p:UserPrompt)-[:RESULTED_IN {confidence: 0.8}]->(c:Commit)
// Inferred by: prompt timestamp < commit timestamp, semantic similarity

// Prompt → Agent references
(p:UserPrompt)-[:MENTIONS]->(a:Agent)
// Detected by: agent name appears in prompt text

// Prompt → Planning references
(p:UserPrompt)-[:REFERENCES]->(d:PlanningDoc)
// Detected by: planning doc path or title appears in prompt

// Planning → Implementation
(d:PlanningDoc)-[:IMPLEMENTED_BY {completeness: 0.7}]->(c:Commit)
// Inferred by: semantic similarity, temporal sequence, file overlap

// Planning → Agent design
(d:PlanningDoc)-[:SPECIFIES]->(a:Agent)
// Detected by: agent name in planning doc

// ToM Evidence
(p:UserPrompt)-[:EVIDENCES {strength: "high", reasoning: "..."}]->(dim:ToMDimension)
// From deep prompt analysis

// Semantic Similarity (computed)
(e1)-[:SIMILAR_TO {score: 0.92}]->(e2)
// When cosine similarity > 0.8
```

## Ingestion Pipeline

### Phase 1: Entity Extraction

```
┌─────────────────────────────────────────────────────────────────┐
│                     ENTITY EXTRACTORS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Planning Docs                                                │
│     .claude/planning/*.md → parse YAML frontmatter + content     │
│     → create PlanningDoc nodes                                   │
│                                                                  │
│  2. Git Commits                                                  │
│     git log --format=json → parse commit metadata                │
│     → create Commit nodes                                        │
│                                                                  │
│  3. Agents                                                       │
│     .claude/agents/*.md + plugins/*/agents/*.md → parse YAML     │
│     → create Agent nodes                                         │
│                                                                  │
│  4. Skills                                                       │
│     plugins/*/skills/**/SKILL.md → parse YAML                    │
│     → create Skill nodes                                         │
│                                                                  │
│  5. User Prompts (existing + enhance)                            │
│     Add embeddings to existing UserMessage nodes                 │
│                                                                  │
│  6. ToM Dimensions                                               │
│     Create from user-model.md schema                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Phase 2: Embedding Generation

```python
async def embed_entity(entity: dict, embed_fn) -> list[float]:
    """Generate embedding for any entity type."""

    if entity['type'] == 'PlanningDoc':
        # Embed title + first 2000 chars of content
        text = f"{entity['title']}\n\n{entity['content'][:2000]}"

    elif entity['type'] == 'Commit':
        # Embed commit message + file paths
        text = f"{entity['message']}\n\nFiles: {', '.join(entity['files'])}"

    elif entity['type'] == 'Agent':
        # Embed name + description + tools
        text = f"{entity['name']}: {entity['description']}\nTools: {entity['tools']}"

    elif entity['type'] == 'UserPrompt':
        # Embed full prompt text
        text = entity['text']

    return await embed_fn(text)
```

### Phase 3: Relationship Inference

```python
async def infer_relationships(graph):
    """Create edges based on rules and embeddings."""

    # 1. MENTIONS: Simple text matching
    for prompt in graph.get_nodes('UserPrompt'):
        for agent in graph.get_nodes('Agent'):
            if agent.name.lower() in prompt.text.lower():
                graph.create_edge(prompt, 'MENTIONS', agent)

    # 2. REFERENCES: Text matching for planning docs
    for prompt in graph.get_nodes('UserPrompt'):
        for doc in graph.get_nodes('PlanningDoc'):
            if doc.title.lower() in prompt.text.lower():
                graph.create_edge(prompt, 'REFERENCES', doc)

    # 3. RESULTED_IN: Temporal + semantic inference
    for prompt in graph.get_nodes('UserPrompt'):
        # Find commits within 30 minutes after prompt
        nearby_commits = graph.query("""
            MATCH (c:Commit)
            WHERE c.timestamp > $prompt_time
              AND c.timestamp < $prompt_time + duration('PT30M')
            RETURN c
        """, prompt_time=prompt.timestamp)

        for commit in nearby_commits:
            similarity = cosine_similarity(prompt.embedding, commit.embedding)
            if similarity > 0.6:
                graph.create_edge(prompt, 'RESULTED_IN', commit,
                                  confidence=similarity)

    # 4. SIMILAR_TO: Embedding-based
    all_embeddings = graph.get_all_embeddings()
    for i, (id1, emb1) in enumerate(all_embeddings):
        for id2, emb2 in all_embeddings[i+1:]:
            sim = cosine_similarity(emb1, emb2)
            if sim > 0.85:  # High threshold
                graph.create_edge(id1, 'SIMILAR_TO', id2, score=sim)
```

### Phase 4: ToM Integration

```python
async def link_tom_evidence(graph, deep_analysis: dict):
    """Connect prompts to ToM dimensions based on deep analysis."""

    for prompt_analysis in deep_analysis['prompts']:
        prompt_id = prompt_analysis['id']

        for inference in prompt_analysis['inferences']:
            dimension = inference['dimension']  # e.g., "cognitive-style"
            evidence = inference['evidence']
            confidence = inference['confidence']
            reasoning = inference['reasoning']

            graph.create_edge(
                prompt_id,
                'EVIDENCES',
                f"tom:{dimension}",
                strength=confidence,
                reasoning=reasoning,
                evidence_quote=evidence
            )
```

## Query Capabilities

### Semantic Queries

```cypher
// "What prompts led to commits about the conductor?"
MATCH (p:UserPrompt)-[:RESULTED_IN]->(c:Commit)
WHERE c.message CONTAINS 'conductor'
RETURN p.text, c.message, c.timestamp

// "Find similar planning docs to this one"
MATCH (d1:PlanningDoc {title: "Trust and Autonomy Plan"})
      -[:SIMILAR_TO {score}]-(d2:PlanningDoc)
WHERE score > 0.8
RETURN d2.title, score
ORDER BY score DESC

// "Which agents are most referenced in prompts?"
MATCH (p:UserPrompt)-[:MENTIONS]->(a:Agent)
RETURN a.name, count(p) as mention_count
ORDER BY mention_count DESC

// "What prompts evidence the 'autonomy preference' ToM dimension?"
MATCH (p:UserPrompt)-[e:EVIDENCES]->(d:ToMDimension {id: 'collaboration-preferences'})
RETURN p.text, e.reasoning, e.strength
ORDER BY e.strength DESC
```

### Pattern Discovery

```cypher
// "How does thinking evolve over time on a topic?"
MATCH (p:UserPrompt)-[:SIMILAR_TO*1..3]-(related:UserPrompt)
WHERE p.text CONTAINS 'knowledge graph'
RETURN p.timestamp, p.text, collect(related.text) as related_prompts
ORDER BY p.timestamp

// "What's the implementation gap? Planning not yet in commits"
MATCH (d:PlanningDoc)
WHERE NOT (d)-[:IMPLEMENTED_BY]->(:Commit)
RETURN d.title, d.path

// "Agent collaboration patterns"
MATCH (p:UserPrompt)-[:MENTIONS]->(a1:Agent),
      (p)-[:MENTIONS]->(a2:Agent)
WHERE a1 <> a2
RETURN a1.name, a2.name, count(p) as co_mention_count
ORDER BY co_mention_count DESC
```

## Automation: Continuous Ingestion

### Git Hook: Post-Commit

```python
#!/usr/bin/env python3
"""Post-commit hook: Add commit to ecosystem graph."""

async def on_commit():
    # Get commit info
    commit = get_latest_commit()

    # Generate embedding
    embedding = await embed(f"{commit.message}\n\nFiles: {commit.files}")

    # Add to graph
    graph.create_node('Commit', {
        'hash': commit.hash,
        'message': commit.message,
        'embedding': embedding,
        ...
    })

    # Infer relationships to recent prompts
    await infer_resulted_in(commit)
```

### Session Hook: On Prompt

```python
async def on_user_prompt(prompt_text: str, session_id: str):
    """Called by UserPromptSubmit hook."""

    # Generate embedding
    embedding = await embed(prompt_text)

    # Add/update prompt node
    graph.upsert_node('UserPrompt', {
        'text': prompt_text,
        'session_id': session_id,
        'embedding': embedding,
        'timestamp': now()
    })

    # Detect agent/planning mentions
    await infer_mentions(prompt_text)
```

### Periodic: Deep ToM Analysis

```python
async def periodic_tom_analysis():
    """Run weekly: Deep analysis of new prompts for ToM signals."""

    # Get prompts without ToM analysis
    unanalyzed = graph.query("""
        MATCH (p:UserPrompt)
        WHERE NOT (p)-[:EVIDENCES]->(:ToMDimension)
        RETURN p
        ORDER BY p.timestamp DESC
        LIMIT 50
    """)

    # Run Sherlock-level analysis (Opus)
    for prompt in unanalyzed:
        analysis = await deep_analyze_prompt(prompt)
        await link_tom_evidence(graph, analysis)
```

## Implementation Priority

### Phase 1: Foundation (This Session)
- [ ] Create ingestion scripts for planning docs, commits, agents
- [ ] Add embeddings to existing prompt nodes
- [ ] Create ToMDimension nodes from user-model.md

### Phase 2: Relationships (Next Session)
- [ ] Implement MENTIONS detection (prompt → agent)
- [ ] Implement REFERENCES detection (prompt → planning)
- [ ] Implement SIMILAR_TO computation

### Phase 3: Automation (Future)
- [ ] Post-commit hook for real-time ingestion
- [ ] UserPromptSubmit hook for prompt embeddings
- [ ] Periodic ToM analysis job

### Phase 4: Query Interface (Future)
- [ ] MCP server with semantic query tools
- [ ] Conductor integration for proactive surfacing
- [ ] Dashboard visualization

## Dependencies

- FalkorDB (running, 468 nodes currently)
- Embedding model: OpenAI text-embedding-3-small OR Ollama nomic-embed-text
- Graphiti (optional, for advanced entity extraction)

## Success Metrics

| Metric | Target |
|--------|--------|
| Entities in graph | 1000+ (from current 468) |
| Entity types | 7 (Session, UserMessage, AssistantMessage, PlanningDoc, Commit, Agent, Skill) |
| Relationship types | 10+ (add MENTIONS, REFERENCES, RESULTED_IN, SIMILAR_TO, EVIDENCES, etc.) |
| Embedding coverage | 100% of prompts, planning docs, commits |
| ToM evidence links | 50+ prompts → dimensions |
| Query latency | <100ms for most queries |

---

*The graph is the ecosystem's memory. Everything connected, nothing forgotten.*
