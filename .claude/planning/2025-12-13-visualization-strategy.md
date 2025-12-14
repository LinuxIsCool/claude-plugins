# Visualization Strategy: Bridging Knowledge Graphs to Human Eyes

*How obsidian-quartz, knowledge-graphs, and the archivist collaborate to make data visible.*

---

## The Problem

We have rich data:
- **1,087,708 commits** in FalkorDB temporal graph
- **602 sessions** of conversation history
- **Atomic journal entries** with wikilinks
- **Semantic concepts** extracted by LLMs

But data without visualization is like a library without a map. The human (Shawn) needs to:
- "Show me what I worked on last week"
- "Show me how concepts connect"
- "Show me the journal's structure"

## The Solution Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                                      │
│                                                                              │
│  "Show me the journal graph"    "Show me commits this week"                 │
│           │                              │                                   │
│           ▼                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                      obsidian-quartz agent                           │   │
│  │                                                                       │   │
│  │  Understands: Quartz config, D3 physics, PixiJS rendering           │   │
│  │  Creates: View configurations, custom plugins, API bridges          │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              │                                              │
│           ┌──────────────────┴──────────────────┐                          │
│           ▼                                      ▼                          │
│  ┌─────────────────────┐            ┌─────────────────────┐                │
│  │  MARKDOWN PATH      │            │  DATABASE PATH       │                │
│  │                     │            │                      │                │
│  │  .claude/journal/   │            │  FalkorDB            │                │
│  │  Quartz build       │            │  Cypher queries      │                │
│  │  Static site        │            │  API endpoint        │                │
│  └──────────┬──────────┘            └──────────┬───────────┘                │
│             │                                   │                            │
│             └─────────────┬─────────────────────┘                            │
│                           ▼                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         RENDERING ENGINE                             │   │
│  │                                                                       │   │
│  │  D3.js Force Simulation          PixiJS WebGL/WebGPU                │   │
│  │  - forceManyBody (repel)         - GPU-accelerated                  │   │
│  │  - forceCenter (gravity)         - Handles 10K+ nodes               │   │
│  │  - forceLink (edges)             - 60fps animations                 │   │
│  │  - forceCollide (spacing)        - Tween transitions                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                           │                                                  │
│                           ▼                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                          BROWSER                                     │   │
│  │                                                                       │   │
│  │  Interactive force-directed graph with:                              │   │
│  │  - Drag nodes                                                        │   │
│  │  - Zoom/pan                                                          │   │
│  │  - Hover highlights                                                  │   │
│  │  - Click navigation                                                  │   │
│  │  - Keyboard shortcuts (Ctrl+G for global)                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Agent Collaboration Model

### Primary Agents

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **obsidian-quartz** | Visualization master | Data, view request | Interactive graph |
| **knowledge-graphs** | Query expertise | View requirements | Cypher queries, data transforms |
| **archivist** | Pattern detection | Graph data | Highlighted patterns, clusters |

### Collaboration Flows

**Flow 1: Journal Visualization**
```
User: "Show me the journal graph"
    │
    ▼
obsidian-quartz: Configure Quartz for .claude/journal/
    │
    ├── Build content index from markdown
    ├── Configure D3 settings for temporal data
    └── Serve via local dev server
    │
    ▼
Browser: Force-directed graph of atomic entries
```

**Flow 2: FalkorDB Query Visualization**
```
User: "Show me commits from the cognitive-ecosystem"
    │
    ▼
obsidian-quartz: Identify this as database view
    │
    └── Consult knowledge-graphs for query pattern
        │
        ▼
        knowledge-graphs: Generate Cypher query
            MATCH (r:Repository {name: 'cognitive-ecosystem'})
            -[:CONTAINS_COMMIT]->(c:Commit)
            -[:AUTHORED_BY]->(a:Author)
            RETURN c, a
    │
    ▼
obsidian-quartz: Transform to D3 format
    │
    ├── nodes: commits + authors
    ├── links: AUTHORED_BY edges
    └── Send to renderer
    │
    ▼
Browser: Commit graph with author clusters
```

**Flow 3: Pattern Highlighting**
```
archivist: "I noticed a cluster of activity around 'knowledge graphs'"
    │
    ▼
obsidian-quartz: Create highlighted view
    │
    ├── Query commits containing 'knowledge graph'
    ├── Configure node colors by relevance
    └── Enable radial layout around cluster
    │
    ▼
Browser: Radial graph focused on knowledge graph commits
```

## View Types

### 1. Journal DNA Spiral

**Purpose:** Navigate temporal journal entries

**Data Source:** `.claude/journal/**/*.md` via Quartz build

**Configuration:**
```typescript
{
  depth: -1,           // All nodes
  enableRadial: true,  // Spiral layout
  showTags: true,      // Show tag clusters
  focusOnHover: true,  // Dim non-neighbors
}
```

**Features:**
- Daily entries as hub nodes (many connections)
- Atomic entries as leaf nodes (few connections)
- Tags as connecting concepts

### 2. Commit Timeline

**Purpose:** Understand development history

**Data Source:** FalkorDB `git_history` graph

**Query Pattern:**
```cypher
MATCH (c:Commit)
WHERE c.timestamp > $start AND c.timestamp < $end
OPTIONAL MATCH (c)-[:HAS_TYPE]->(t:CommitType)
OPTIONAL MATCH (c)-[:AUTHORED_BY]->(a:Author)
RETURN c, t, a
```

**Features:**
- X-axis: time
- Clusters by commit type (feat/fix/chore)
- Author coloring
- Click to see commit details

### 3. Concept Semantic Graph

**Purpose:** Explore how concepts relate

**Data Source:** FalkorDB semantic entities (from Ollama enrichment)

**Query Pattern:**
```cypher
MATCH (c1:Concept)-[:RELATES_TO]->(c2:Concept)
RETURN c1, c2
UNION
MATCH (c:Concept)<-[:DISCUSSES]-(commit:Commit)
RETURN c, commit
```

**Features:**
- Concept nodes sized by mention count
- Edges by co-occurrence
- Cluster detection (community algorithms)

### 4. Session Flow

**Purpose:** Understand conversation patterns

**Data Source:** FalkorDB `claude_logs` graph

**Query Pattern:**
```cypher
MATCH (s:Session)-[:CONTAINS]->(e:Event)
WHERE s.start_time > $date
RETURN s, e ORDER BY e.timestamp
```

**Features:**
- Sessions as columns
- Events as sequential nodes
- Tool usage highlighted
- Duration encoding (node size)

## Implementation Phases

### Phase 1: Quartz Setup (Immediate)

**Goal:** Get basic journal graph rendering in browser

**Tasks:**
1. Configure `quartz.config.ts` for this repo
2. Point content to `.claude/journal/`
3. Run `npx quartz build && npx quartz serve`
4. Verify graph view works

**Success Criteria:** DNA spiral visible in browser at localhost

### Phase 2: API Bridge (Week 1)

**Goal:** Query FalkorDB, render results

**Tasks:**
1. Create Express/Fastify API server
2. Implement Cypher query endpoints
3. Transform results to D3 format
4. Create Quartz plugin for external data

**Endpoints:**
```
GET /api/graph/commits?repo=X&since=Y
GET /api/graph/concepts?query=X
GET /api/graph/sessions?date=X
```

**Success Criteria:** Can render FalkorDB data in Quartz graph

### Phase 3: Multi-View UI (Week 2)

**Goal:** Switch between views seamlessly

**Tasks:**
1. View selector component
2. Cached data for fast switching
3. Synchronized zoom/pan across views
4. Bookmarkable view states

**Success Criteria:** User can flip between journal/commits/concepts views

### Phase 4: Commands (Week 3)

**Goal:** Natural language → visualization

**Tasks:**
1. Create `/visualize` command
2. Parse intent (what view, what filter)
3. Open browser with correct view
4. Integrate with Claude Code flow

**Commands:**
```
/visualize journal
/visualize commits --since="1 week ago"
/visualize concepts --around="knowledge graphs"
```

**Success Criteria:** "Show me X" → browser opens with X

## Technical Details

### Quartz Configuration

```typescript
// quartz.config.ts
import { QuartzConfig } from "./quartz/cfg"

const config: QuartzConfig = {
  configuration: {
    pageTitle: "Claude Ecosystem",
    enablePopovers: true,
    baseUrl: "localhost:8080",
  },
  content: {
    source: ".claude/journal",
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.WikiLinks(),
      Plugin.SyntaxHighlighting(),
    ],
    filters: [
      Plugin.RemoveDrafts(),
    ],
    emitters: [
      Plugin.ContentPage(),
      Plugin.ContentIndex(),  // Builds the link graph
      Plugin.ComponentResources(),
    ],
  },
}

export default config
```

### FalkorDB → D3 Transform

```python
def falkordb_to_d3(cypher_result):
    """Transform FalkorDB result to D3-compatible format."""
    nodes = {}
    links = []

    for record in cypher_result:
        for item in record.values():
            if hasattr(item, 'labels'):  # Node
                node_id = item.properties.get('id') or item.properties.get('hash')
                nodes[node_id] = {
                    'id': node_id,
                    'text': item.properties.get('title') or item.properties.get('message'),
                    'tags': item.labels,
                }
            elif hasattr(item, 'type'):  # Relationship
                links.append({
                    'source': item.start_node,
                    'target': item.end_node,
                    'type': item.type,
                })

    return {
        'nodes': list(nodes.values()),
        'links': links,
    }
```

### Custom Quartz Plugin for FalkorDB

```typescript
// quartz/plugins/emitters/falkordb.ts
import { QuartzEmitterPlugin } from "../types"

export const FalkorDBGraph: QuartzEmitterPlugin = {
  name: "FalkorDBGraph",
  emit: async (ctx, content, resources) => {
    const apiUrl = process.env.FALKORDB_API || 'http://localhost:3000/api'

    const views = ['commits', 'concepts', 'sessions']
    const results = []

    for (const view of views) {
      const response = await fetch(`${apiUrl}/graph/${view}`)
      const data = await response.json()

      results.push({
        slug: `graph/${view}` as FullSlug,
        ext: ".json",
        content: JSON.stringify(data),
      })
    }

    return results
  },
}
```

## Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Time to first graph | <5s | From command to browser render |
| Nodes rendered | 10K+ | Performance test with large graph |
| Frame rate | 60fps | Browser dev tools |
| View switch time | <1s | User perception |
| Command coverage | 5 views | Feature completion |

## Questions for Future Exploration

1. **3D visualization?** Three.js for spatial layouts
2. **VR/AR?** WebXR for immersive exploration
3. **Collaborative?** Multiple users exploring same graph
4. **Temporal animation?** Time-lapse of graph evolution
5. **AI-guided tours?** "Let me show you the interesting parts"

---

## Agent Coordination Summary

```
                    ┌─────────────────────────┐
                    │         USER            │
                    │   "Show me X graph"     │
                    └───────────┬─────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │    obsidian-quartz      │
                    │   (Visualization Lead)   │
                    └───────────┬─────────────┘
                                │
            ┌───────────────────┼───────────────────┐
            │                   │                   │
            ▼                   ▼                   ▼
┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
│ knowledge-graphs  │ │    archivist      │ │     journal       │
│                   │ │                   │ │                   │
│ Query expertise   │ │ Pattern detection │ │ Content source    │
│ Cypher patterns   │ │ Coherence check   │ │ Markdown entries  │
│ Graph algorithms  │ │ Flow observation  │ │ Wikilinks         │
└───────────────────┘ └───────────────────┘ └───────────────────┘
            │                   │                   │
            └───────────────────┼───────────────────┘
                                │
                                ▼
                    ┌─────────────────────────┐
                    │       FalkorDB          │
                    │   (Temporal Graph DB)   │
                    └─────────────────────────┘
```

**The ecosystem has eyes now.**

---

*Created: 2025-12-13*
*Status: Strategy defined, Phase 1 ready to begin*
