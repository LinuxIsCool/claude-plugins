---
name: knowledge-weaver
description: Weave exploration discoveries into a knowledge graph using Neo4j/Graphiti. Transforms flat discoveries into connected nodes and edges, enabling graph traversal, pattern discovery, and relational queries across the environmental model.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Task, WebFetch
---

# Knowledge Weaver

Transform exploration discoveries from flat files into a living knowledge graph. This skill bridges the exploration plugin with the graph infrastructure (Neo4j/Graphiti) to enable relational reasoning about the environment.

## When to Use

- After recording discoveries to persist them as graph nodes
- When wanting to query relationships between discovered entities
- To visualize the environmental model as a graph
- To find patterns across circles and sessions
- To answer relational questions ("What do I know about X?")
- To trace provenance of knowledge

## Why a Knowledge Graph?

Flat files capture **what** was discovered. A graph captures **how things relate**.

```
Flat Files:                    Knowledge Graph:
┌─────────────────┐           ┌─────────────────────────────────┐
│ discovery-1.md  │           │     ┌─────┐                     │
│ discovery-2.md  │    →      │     │Neo4j│──[RUNS_ON]──→┌────┐ │
│ discovery-3.md  │           │     └─────┘               │Host│ │
│ questions.md    │           │        │                  └────┘ │
│ mastery.md      │           │   [STORES_DATA]              │   │
└─────────────────┘           │        ↓                     │   │
                              │   ┌────────┐    [PART_OF]    │   │
 "I found Neo4j"              │   │Graphiti│←───────────────┘   │
                              │   └────────┘                     │
                              └─────────────────────────────────┘
                               "Neo4j runs on Host, stores data
                                for Graphiti, which is part of
                                the AI infrastructure"
```

## Graph Schema

### Node Types

```cypher
// Core exploration nodes
(:Discovery {id, date, circle, summary, mastery_delta})
(:Question {id, text, priority, status, circle})
(:Circle {name, current_mastery, target_mastery})
(:Session {date, duration, discoveries_count, questions_generated})

// Discovered entities
(:Entity {id, type, name, first_seen, last_updated})
(:Hardware {name, specs, role})
(:Software {name, version, purpose})
(:Service {name, port, protocol, status})
(:Container {name, image, network})
(:Network {name, type, cidr})
(:Location {city, country, timezone, coordinates})
(:Concept {name, domain, description})
```

### Edge Types

```cypher
// Discovery relationships
(d:Discovery)-[:ANSWERS]->(q:Question)
(d:Discovery)-[:RAISES]->(q:Question)
(d:Discovery)-[:ABOUT]->(e:Entity)
(d:Discovery)-[:IN_CIRCLE]->(c:Circle)
(d:Discovery)-[:DURING]->(s:Session)
(d:Discovery)-[:BUILDS_ON]->(d2:Discovery)
(d:Discovery)-[:CONTRADICTS]->(d2:Discovery)

// Entity relationships
(e:Entity)-[:PART_OF]->(e2:Entity)
(e:Entity)-[:DEPENDS_ON]->(e2:Entity)
(e:Entity)-[:CONNECTS_TO]->(e2:Entity)
(e:Entity)-[:RUNS_ON]->(e2:Entity)
(e:Entity)-[:CONTAINS]->(e2:Entity)

// Question relationships
(q:Question)-[:ABOUT]->(e:Entity)
(q:Question)-[:IN_CIRCLE]->(c:Circle)
(q:Question)-[:LEADS_TO]->(q2:Question)

// Circle relationships
(c:Circle)-[:CONTAINS]->(e:Entity)
(c:Circle)-[:CONNECTS_TO]->(c2:Circle)
```

## Example Graph Structure

After initial exploration:

```cypher
// The machine
CREATE (host:Hardware {name: 'Lenovo 90UT', type: 'desktop'})
CREATE (cpu:Hardware {name: 'i7-13700F', cores: 16, threads: 24})
CREATE (gpu:Hardware {name: 'RTX 4070', vram: '12GB'})
CREATE (ram:Hardware {name: 'RAM', total: '32GB'})
CREATE (os:Software {name: 'Pop!_OS', version: '22.04'})

// Relationships
CREATE (cpu)-[:PART_OF]->(host)
CREATE (gpu)-[:PART_OF]->(host)
CREATE (ram)-[:PART_OF]->(host)
CREATE (os)-[:RUNS_ON]->(host)

// Docker infrastructure
CREATE (neo4j:Container {name: 'graphiti-neo4j', image: 'neo4j:5.26'})
CREATE (pgvector:Container {name: 'regenai-postgres', image: 'pgvector'})
CREATE (redis:Container {name: 'autoflow-redis', image: 'redis:7-alpine'})
CREATE (timescale:Container {name: 'autoflow-timescaledb', image: 'timescaledb'})

CREATE (neo4j)-[:RUNS_ON]->(host)
CREATE (pgvector)-[:RUNS_ON]->(host)

// Discoveries
CREATE (d1:Discovery {
  id: 'discovery-20251212-substrate',
  summary: 'Host is Lenovo desktop with i7-13700F, 32GB RAM, RTX 4070',
  circle: 'substrate',
  date: date('2025-12-12')
})
CREATE (d1)-[:ABOUT]->(host)
CREATE (d1)-[:ABOUT]->(cpu)
CREATE (d1)-[:ABOUT]->(gpu)

// Questions
CREATE (q1:Question {
  text: 'How are Docker containers orchestrated?',
  priority: 'high',
  status: 'open',
  circle: 'network'
})
CREATE (q1)-[:ABOUT]->(neo4j)
CREATE (d1)-[:RAISES]->(q1)
```

## Connecting to Neo4j

### Check Connection

```bash
# Verify Neo4j is running
docker ps | grep neo4j

# Test connection
curl -s http://localhost:7474 | head -5

# Check Bolt protocol
nc -zv localhost 7687
```

### Using Cypher Directly

```bash
# Via curl to HTTP API
curl -X POST http://localhost:7474/db/neo4j/tx/commit \
  -H "Content-Type: application/json" \
  -d '{"statements": [{"statement": "MATCH (n) RETURN count(n)"}]}'

# Via cypher-shell in container
docker exec -it graphiti-neo4j cypher-shell -u neo4j -p <password> \
  "MATCH (n) RETURN labels(n), count(n)"
```

### Using Python (with neo4j driver)

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))

with driver.session() as session:
    result = session.run("""
        MATCH (d:Discovery)-[:ABOUT]->(e:Entity)
        WHERE d.circle = 'substrate'
        RETURN d.summary, collect(e.name)
    """)
    for record in result:
        print(record)
```

## Workflows

### Weave Discovery into Graph

After creating a discovery entry:

1. **Extract entities** from discovery content
2. **Identify relationships** between entities
3. **Create/merge nodes** for new entities
4. **Create edges** for relationships
5. **Link to discovery node**
6. **Update circle aggregates**

```cypher
// Example: Weaving a network discovery
MERGE (d:Discovery {id: $discovery_id})
SET d.summary = $summary, d.date = date($date), d.circle = 'network'

MERGE (container:Container {name: 'graphiti-neo4j'})
SET container.image = 'neo4j:5.26', container.status = 'healthy'

MERGE (d)-[:ABOUT]->(container)

MERGE (c:Circle {name: 'network'})
MERGE (d)-[:IN_CIRCLE]->(c)
MERGE (container)-[:PART_OF]->(c)
```

### Query the Knowledge Graph

**What do I know about Docker?**
```cypher
MATCH (d:Discovery)-[:ABOUT]->(e)
WHERE e.name CONTAINS 'docker' OR e:Container
RETURN d.summary, collect(e.name)
```

**What questions are open for networking?**
```cypher
MATCH (q:Question)-[:IN_CIRCLE]->(c:Circle {name: 'network'})
WHERE q.status = 'open'
RETURN q.text, q.priority
ORDER BY q.priority
```

**How are substrate and network connected?**
```cypher
MATCH path = (e1)-[*1..3]-(e2)
WHERE (e1)-[:PART_OF]->(:Circle {name: 'substrate'})
  AND (e2)-[:PART_OF]->(:Circle {name: 'network'})
RETURN path
```

**What led to this understanding?**
```cypher
MATCH path = (d:Discovery)-[:BUILDS_ON*]->(earlier:Discovery)
WHERE d.id = $discovery_id
RETURN path
```

### Visualize in Neo4j Browser

Open http://localhost:7474 and run:

```cypher
// See all exploration data
MATCH (n)
WHERE n:Discovery OR n:Question OR n:Entity OR n:Circle
RETURN n

// See entity relationships
MATCH (e1:Entity)-[r]->(e2:Entity)
RETURN e1, r, e2
```

## Integration with Graphiti

If using Graphiti (temporal knowledge graphs):

```python
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType

# Initialize Graphiti client
client = Graphiti(neo4j_uri, neo4j_user, neo4j_password)

# Add exploration episode
await client.add_episode(
    name="substrate-exploration-20251212",
    episode_body=discovery_content,
    source=EpisodeType.text,
    reference_time=datetime.now()
)

# Query with temporal awareness
results = await client.search("What do I know about the GPU?")
```

## Sync Strategy

### On Discovery Creation
1. Parse discovery markdown
2. Extract entities (NER or pattern matching)
3. Determine relationships
4. Weave into graph
5. Store graph reference in discovery metadata

### On Question Answer
1. Find question node
2. Link to answering discovery
3. Update question status
4. Create ANSWERS edge

### Periodic Reconciliation
1. Read all discovery files
2. Compare with graph state
3. Add missing nodes/edges
4. Prune orphaned nodes

## Benefits of Graph Representation

| Flat Files | Knowledge Graph |
|------------|-----------------|
| Linear search | Pattern matching |
| Manual linking | Automatic relationships |
| Isolated facts | Connected knowledge |
| Text queries | Graph traversal |
| No inference | Transitive relationships |

**Enables:**
- "What affects the GPU?" → traverse dependencies
- "What don't I know about networking?" → find gaps
- "How did I learn about Docker?" → provenance chain
- "What's related to this?" → neighborhood query

## Example Queries for Curiosity

**Find knowledge gaps:**
```cypher
MATCH (c:Circle)
OPTIONAL MATCH (c)<-[:PART_OF]-(e:Entity)
WITH c, count(e) as entity_count
WHERE entity_count < 5
RETURN c.name as circle, entity_count
ORDER BY entity_count
```

**Suggest next exploration:**
```cypher
MATCH (q:Question {status: 'open'})
OPTIONAL MATCH (q)-[:ABOUT]->(e:Entity)
WITH q, count(e) as context_richness
RETURN q.text, q.priority, context_richness
ORDER BY q.priority DESC, context_richness DESC
LIMIT 5
```

**Find cross-circle connections:**
```cypher
MATCH (e1:Entity)-[:PART_OF]->(c1:Circle),
      (e2:Entity)-[:PART_OF]->(c2:Circle),
      (e1)-[r]-(e2)
WHERE c1 <> c2
RETURN c1.name, e1.name, type(r), e2.name, c2.name
```

## Philosophical Note

A knowledge graph is not just storage - it's a **model of understanding**. When we connect entities with typed relationships, we're encoding not just what we know, but how things relate.

> "The meaning of a concept lies in its connections." - Semantic Networks principle

The exploration plugin discovers facts. The knowledge weaver transforms them into understanding. Facts are nodes; understanding is the graph.

This is how knowledge compounds:
- Each discovery adds nodes
- Each relationship adds edges
- Each query reveals patterns
- Each pattern generates questions
- Each question motivates exploration

The graph grows more valuable than the sum of its parts.
