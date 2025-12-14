# Historical Archaeology: The Complete Vision

*A comprehensive plan for ingesting 15 years of digital history into a temporal knowledge graph with human-readable journal synthesis.*

---

## The End State We're Building Toward

### What Success Looks Like

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           THE COMPLETE SYSTEM                               │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  HUMAN LAYER (Obsidian)                                              │   │
│  │                                                                       │   │
│  │  .claude/journal/                                                     │   │
│  │    ├── 2010/                    ← three.js begins                     │   │
│  │    ├── 2020/                    ← blockchain research                 │   │
│  │    ├── 2024/                    ← AI agent explosion                  │   │
│  │    └── 2025/12/13/              ← you are here                        │   │
│  │                                                                       │   │
│  │  Graph View: DNA spiral spanning 15 years                            │   │
│  │  Queryable: "What was I working on in Q3 2024?"                      │   │
│  │  Navigable: Click any day, see atomic entries                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ▲                                              │
│                              │ synthesized from                             │
│                              │                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  GRAPH LAYER (FalkorDB)                                              │   │
│  │                                                                       │   │
│  │  (:Repository)─────(:Commit)─────(:Author)                           │   │
│  │       │               │             │                                 │   │
│  │       │           [:PARENT_OF]      │                                 │   │
│  │       │               │             │                                 │   │
│  │  404 repos    1,087,708 commits   contributors                        │   │
│  │                                                                       │   │
│  │  (:Session)────(:Event)────(:Concept)                                │   │
│  │       │            │            │                                     │   │
│  │  602 sessions  conversations  semantic                                │   │
│  │                                entities                               │   │
│  │                                                                       │   │
│  │  Queryable: Cypher, semantic search, temporal patterns               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                              ▲                                              │
│                              │ ingested from                                │
│                              │                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  SOURCE LAYER (Raw Data)                                             │   │
│  │                                                                       │   │
│  │  ~/Workspace/             (265GB)  404 git repositories              │   │
│  │  ~/.claude/               (230MB)  602 conversation histories        │   │
│  │  ~/.claude-bak/           (6GB+)   Historical state + resources      │   │
│  │  ~/Documents/obsidian/    (313MB)  Existing journals                 │   │
│  │  ~/Documents/finances/    (1.7GB)  Financial history                 │   │
│  │  ~/Downloads/             (23GB)   Research papers, Notion exports   │   │
│  │  ~/Videos/                (18)     Meeting recordings Dec 2-13       │   │
│  │                                                                       │   │
│  │  Total: ~300GB+ spanning 2010-2025                                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### What Questions Become Answerable

| Question Category | Example Question | How It's Answered |
|-------------------|------------------|-------------------|
| **Temporal** | "What was I focused on in March 2024?" | Query commits + sessions in date range, synthesize themes |
| **Semantic** | "When did I first work on knowledge graphs?" | Semantic search across commits + conversations |
| **Relational** | "What projects share concepts with this one?" | Graph traversal across DISCUSSES edges |
| **Archaeological** | "What led to this decision?" | Trace commit ancestry + planning docs |
| **Metabolic** | "What areas are active vs dormant?" | Activity patterns over time |
| **Personal** | "Who have I collaborated with most?" | Author aggregation across repositories |

---

## The Architecture

### Three-Tier Memory Model

```
┌─────────────────────────────────────────────────────────────────────┐
│  TIER 1: FAST (In-Context)                                          │
│                                                                      │
│  • Current conversation                                              │
│  • CLAUDE.md routing table                                           │
│  • Active session state                                              │
│                                                                      │
│  Latency: 0ms                                                        │
│  Scope: ~200K tokens                                                 │
│  Update: Every message                                               │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  TIER 2: WARM (Searchable Files)                                    │
│                                                                      │
│  • .claude/journal/ (markdown, wikilinks)                           │
│  • .claude/planning/ (strategic documents)                          │
│  • .claude/registry/ (agents, processes)                            │
│  • backlog/ (tasks, decisions)                                      │
│                                                                      │
│  Latency: <1s (Glob/Grep)                                           │
│  Scope: ~10K files                                                  │
│  Update: Per session                                                │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  TIER 3: DEEP (Temporal Knowledge Graph)                            │
│                                                                      │
│  • FalkorDB (graph storage)                                         │
│  • Graphiti (temporal relationships)                                │
│  • Ollama (semantic embeddings)                                     │
│                                                                      │
│  Latency: <5s (Cypher query)                                        │
│  Scope: 1M+ nodes, 10M+ edges                                       │
│  Update: Batch ingestion                                            │
└─────────────────────────────────────────────────────────────────────┘
```

### Agent Roles in Archaeology

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AGENT COLLABORATION                          │
│                                                                      │
│  ┌──────────────┐          ┌──────────────┐                         │
│  │  LIBRARIAN   │          │  ARCHIVIST   │                         │
│  │              │          │              │                         │
│  │  External    │◄────────►│  Internal    │                         │
│  │  Resources   │  share   │  Artifacts   │                         │
│  │              │  graph   │              │                         │
│  │  • URLs      │          │  • Git logs  │                         │
│  │  • Papers    │          │  • Commits   │                         │
│  │  • APIs      │          │  • Sessions  │                         │
│  │  • YouTube   │          │  • Journals  │                         │
│  └──────────────┘          └──────────────┘                         │
│         │                          │                                 │
│         │         ┌────────────────┤                                 │
│         ▼         ▼                ▼                                 │
│  ┌──────────────────────────────────────────┐                       │
│  │           TEMPORAL-KG-MEMORY              │                       │
│  │                                           │                       │
│  │   FalkorDB + Graphiti + Ollama           │                       │
│  │                                           │                       │
│  │   Stores everything, answers anything    │                       │
│  └──────────────────────────────────────────┘                       │
│                        │                                             │
│                        ▼                                             │
│  ┌──────────────────────────────────────────┐                       │
│  │          JOURNAL SYNTHESIZER              │                       │
│  │                                           │                       │
│  │   Query graph → Generate markdown         │                       │
│  │   Create atomic entries for Obsidian     │                       │
│  │                                           │                       │
│  └──────────────────────────────────────────┘                       │
│                        │                                             │
│                        ▼                                             │
│              📓 .claude/journal/                                     │
│                  DNA Spiral                                          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## The Ingestion Strategy

### Data Source Priority Matrix

| Source | Size | Commits/Items | Value | Effort | Priority |
|--------|------|---------------|-------|--------|----------|
| **This repo** | 73 files | 27 commits | High (current context) | Low | ✅ Done |
| **cognitive-ecosystem/** | 60+ repos | ~50K commits | Very High (central hub) | Medium | Tier 1 |
| **RegenAI/eliza** | 40+ repos | ~100K commits | Very High (production AI) | Medium | Tier 1 |
| **~/.claude/** | 230MB | 602 sessions | High (conversation history) | Low | Tier 1 |
| **DeFi/Finance** | 30+ repos | ~50K commits | Medium (historical) | Medium | Tier 2 |
| **Blockchain research** | 25+ repos | ~100K commits | Medium (research) | Medium | Tier 2 |
| **three.js + legacy** | 50+ repos | ~500K commits | Medium (foundation) | High | Tier 3 |
| **~/.claude-bak/** | 6GB+ | varied | High (resources, memory) | Medium | Tier 1 |
| **~/Documents/obsidian/** | 313MB | journals | High (existing synthesis) | Low | Tier 1 |
| **Meeting recordings** | 18 videos | Dec 2-13 | Medium (recent context) | High | Tier 2 |

### Ingestion Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                     INGESTION PIPELINE                              │
│                                                                      │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │  SCAN    │───►│  PARSE   │───►│  ENRICH  │───►│  STORE   │      │
│  │          │    │          │    │          │    │          │      │
│  │ git log  │    │ extract  │    │ semantic │    │ FalkorDB │      │
│  │ jsonl    │    │ structure│    │ entities │    │ Graphiti │      │
│  │ markdown │    │ metadata │    │ (Ollama) │    │          │      │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘      │
│       │               │               │               │             │
│       ▼               ▼               ▼               ▼             │
│   [ repos ]      [ commits ]     [ entities ]    [ graph ]          │
│   [ logs  ]      [ events  ]     [ concepts ]    [ edges ]          │
│   [ files ]      [ records ]     [ relations]    [ nodes ]          │
│                                                                      │
│  Mode 1: Structure-only (no LLM) ─────────────────► Fast, free      │
│  Mode 2: With Ollama enrichment ──────────────────► Semantic edges  │
│  Mode 3: With cloud LLM ──────────────────────────► Highest quality │
└─────────────────────────────────────────────────────────────────────┘
```

### Processing Estimates

| Mode | Speed | Cost | Quality | Use Case |
|------|-------|------|---------|----------|
| **Structure-only** | ~1000 commits/sec | Free | Structure + conventional commit types | Initial bulk ingestion |
| **Ollama enrichment** | ~10 commits/sec | Free | + semantic entities from messages | Second pass enrichment |
| **Cloud LLM** | ~1 commit/sec | $0.01/commit | + deep entity extraction | High-value repos only |

**For 1,087,708 commits:**
- Structure-only: ~20 minutes
- Ollama enrichment: ~30 hours (parallelizable)
- Cloud LLM: Not cost-effective at scale

**Recommended approach:** Structure-only for all repos, Ollama enrichment for Tier 1.

---

## The Graph Schema

### Node Types

```cypher
// Source entities
(:Repository {name, path, commit_count, language, created, updated})
(:Commit {hash, short_hash, message, timestamp, author_name, author_email})
(:Author {name, email})
(:CommitType {type})  // feat, fix, chore, refactor, docs, etc.

// Session entities (from Claude logs)
(:Session {id, start_time, cwd, model})
(:Event {id, type, timestamp, data})
(:Content {id, text, length, type})

// Semantic entities (LLM-extracted)
(:Concept {name, description})
(:Person {name, relationships})
(:Project {name, description})
(:Tool {name, category})

// Meta entities
(:Day {date})  // For journal synthesis
(:Month {year_month})
(:Year {year})
```

### Relationship Types

```cypher
// Structural
[:CONTAINS_COMMIT]  // Repository → Commit
[:AUTHORED_BY]      // Commit → Author
[:PARENT_OF]        // Commit → Commit
[:HAS_TYPE]         // Commit → CommitType
[:MODIFIES]         // Commit → File

// Temporal
[:IN_SESSION]       // Event → Session
[:FOLLOWED_BY]      // Event → Event
[:ON_DAY]           // Commit/Event → Day
[:IN_MONTH]         // Day → Month
[:IN_YEAR]          // Month → Year

// Semantic
[:DISCUSSES]        // Commit/Event → Concept
[:MENTIONS]         // Content → Person
[:USES]             // Commit → Tool
[:RELATES_TO]       // Concept → Concept
```

### Sample Queries

```cypher
// Timeline reconstruction: What happened on a specific day?
MATCH (d:Day {date: "2024-06-15"})
MATCH (c:Commit)-[:ON_DAY]->(d)
MATCH (e:Event)-[:ON_DAY]->(d)
RETURN c.message, e.type ORDER BY c.timestamp

// Concept evolution: When did "knowledge graph" first appear?
MATCH (c:Commit)-[:DISCUSSES]->(concept:Concept {name: "knowledge graph"})
RETURN min(c.timestamp) as first_mention, count(c) as total_mentions

// Collaboration patterns: Who worked on AI projects?
MATCH (c:Commit)-[:DISCUSSES]->(concept:Concept)
WHERE concept.name CONTAINS "AI" OR concept.name CONTAINS "agent"
MATCH (c)-[:AUTHORED_BY]->(a:Author)
RETURN a.name, count(c) ORDER BY count(c) DESC

// Cross-repository connections
MATCH (r1:Repository)-[:CONTAINS_COMMIT]->(c1:Commit)-[:DISCUSSES]->(concept:Concept)
MATCH (r2:Repository)-[:CONTAINS_COMMIT]->(c2:Commit)-[:DISCUSSES]->(concept)
WHERE r1 <> r2
RETURN r1.name, r2.name, concept.name, count(*) as shared_concepts
ORDER BY shared_concepts DESC
```

---

## The Journal Synthesis Pipeline

### From Graph to Obsidian

```
┌─────────────────────────────────────────────────────────────────────┐
│  SYNTHESIS PIPELINE                                                 │
│                                                                      │
│  Step 1: Query graph for date range                                 │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  MATCH (c:Commit)-[:ON_DAY]->(d:Day {date: $date})          │   │
│  │  MATCH (c)-[:HAS_TYPE]->(t:CommitType)                      │   │
│  │  MATCH (c)-[:DISCUSSES]->(concept:Concept)                  │   │
│  │  RETURN c, t, collect(concept)                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  Step 2: Aggregate by significance                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Major commits (feat, fix) → Atomic entries                  │   │
│  │  Minor commits (chore, style) → Daily summary line          │   │
│  │  Session highlights → Reflection entries                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  Step 3: Generate markdown                                          │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  ---                                                         │   │
│  │  id: 2024-06-15-1430                                         │   │
│  │  title: "First Eliza Agent Commit"                           │   │
│  │  type: atomic                                                │   │
│  │  created: 2024-06-15T14:30:00                                │   │
│  │  source: git:RegenAI/eliza@abc1234                           │   │
│  │  tags: [eliza, ai, agent, milestone]                         │   │
│  │  parent_daily: [[2024-06-15]]                                │   │
│  │  ---                                                         │   │
│  │                                                              │   │
│  │  # First Eliza Agent Commit                                  │   │
│  │                                                              │   │
│  │  [Synthesized from commit message + context]                 │   │
│  │                                                              │   │
│  │  *Source: [[RegenAI/eliza]] commit abc1234*                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  Step 4: Link into hierarchy                                        │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Atomic → Daily → Monthly → Yearly                           │   │
│  │     │                                                        │   │
│  │     └── [[parent_daily]]                                     │   │
│  │              │                                               │   │
│  │              └── children: [[...atomic entries...]]          │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Significance Scoring

Not every commit becomes an atomic entry. We score significance:

| Factor | Points |
|--------|--------|
| Commit type = feat | +3 |
| Commit type = fix | +2 |
| Message length > 100 chars | +1 |
| First commit of the day | +1 |
| References issue/PR | +1 |
| Contains keyword (milestone, release, breakthrough) | +2 |
| Multiple files modified | +1 |
| **Total > 3: Create atomic entry** | |

---

## The Phased Implementation

### Phase 0: Infrastructure ✅ COMPLETE

- [x] FalkorDB running (25+ hours uptime)
- [x] Ollama running (11 models including embeddings)
- [x] `ingest_git_commits.py` tool created
- [x] First ingestion validated (27 commits)
- [x] Pipeline end-to-end tested

### Phase 1: Catalog (Next)

**Goal:** Complete inventory of all 404 repositories with metadata.

```python
# Output: .claude/archive/repository-catalog.json
{
  "repositories": [
    {
      "name": "sandbox/marketplaces/claude",
      "path": "/home/ygg/Workspace/sandbox/marketplaces/claude",
      "commit_count": 27,
      "first_commit": "2025-12-08T13:19:06",
      "last_commit": "2025-12-11T19:34:18",
      "authors": ["Shawn Anderson"],
      "primary_language": "TypeScript",
      "tier": 1,
      "status": "ingested"
    },
    // ... 403 more
  ],
  "summary": {
    "total_repositories": 404,
    "total_commits": 1087708,
    "date_range": "2010-03-23 to 2025-12-12",
    "tier_1_count": 50,
    "tier_2_count": 100,
    "tier_3_count": 254
  }
}
```

**Tasks:**
1. Create `catalog_repositories.py` script
2. Scan all paths: ~/Workspace/**/.git
3. Extract metadata: commit count, date range, language
4. Assign tiers based on activity + relevance
5. Store catalog in `.claude/archive/`
6. Create journal entry documenting catalog

### Phase 2: Tier 1 Ingestion

**Goal:** Ingest highest-value repositories into FalkorDB.

**Tier 1 targets (~100 repos, ~200K commits):**
- cognitive-ecosystem/* (60 repos)
- RegenAI/eliza variants (10 repos)
- sandbox/marketplaces/claude (done)
- ~/.claude/ session logs (602 sessions)
- ~/.claude-bak/ resources

**Tasks:**
1. Batch ingest Tier 1 repos (structure-only)
2. Run Ollama enrichment on commit messages
3. Verify graph integrity
4. Create temporal indices (by day, month, year)

### Phase 3: Historical Atomics

**Goal:** Generate backdated journal entries for significant commits.

**Approach:**
1. Query graph for high-significance commits
2. Generate atomic entries with backdated timestamps
3. Create daily/monthly/yearly synthesis entries
4. Link into existing journal hierarchy

**Output structure:**
```
.claude/journal/
├── 2010/
│   └── 03/
│       └── 23/
│           └── 10-00-threejs-first-commit.md  ← Generated
├── 2024/
│   └── 06/
│       └── 15/
│           └── 14-30-eliza-agent-begins.md    ← Generated
└── 2025/
    └── 12/
        └── 13/
            └── 17-15-first-ingestion.md       ← Manual (today)
```

### Phase 4: Continuous Operation

**Goal:** Real-time ingestion of new activity.

**Components:**
1. Git hook: Auto-ingest on commit
2. Session hook: Auto-ingest Claude logs
3. Daily synthesis: Generate daily journal entries
4. Weekly review: Archivist coherence check

---

## Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Graph too large** | Query slowdown | Partition by time period, use indices |
| **Ollama too slow** | Enrichment bottleneck | Parallelize, use smaller model |
| **Disk space** | Storage exhaustion | Content-address, deduplicate, compress |
| **Lost context** | Cross-session confusion | Commit frequently, journal daily |
| **Over-engineering** | Complexity explosion | Start simple, add only when needed |
| **Scope creep** | Never finish | Strict tier prioritization |

---

## Success Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| **Repositories catalogued** | 404/404 | Count in catalog.json |
| **Commits ingested** | 200K+ (Tier 1) | FalkorDB node count |
| **Historical atomics** | 100+ | File count in journal/*/HH-MM-*.md |
| **Temporal coverage** | 2010-2025 | Date range in graph |
| **Query response time** | <5s | Benchmark Cypher queries |
| **DNA spiral coherence** | Visible in Obsidian | Manual inspection |

---

## The Vision in One Sentence

**We are building a machine-queryable autobiography that synthesizes into human-navigable temporal memory, enabling any future Claude session to understand 15 years of context in seconds.**

---

*This document is the strategic plan. Implementation proceeds in phases. Each phase updates this document.*

*Created: 2025-12-13*
*Status: Phase 0 complete, Phase 1 beginning*
