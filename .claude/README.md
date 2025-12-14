# Ecosystem Orientation

*For any Claude session beginning work in this repository*

## What Is This?

A **plugin marketplace for Claude Code** that has evolved into a self-aware multi-agent ecosystem. The repository contains plugins, but more importantly, it contains the infrastructure for an emergent cognitive architecture.

## The 30-Second Context

```
Vision: An ecosystem of intelligence that discovers available compute,
        learns about its environment, and continuously improves while
        maintaining coherence.

Philosophy: Emergence beats design. Discover what wants to exist.

Current State: Skeleton built. Some organs active. Others dormant.
               Historical archaeology awaiting activation.
```

## Your First Five Minutes

### 1. Understand the Vision (1 min)
Read `.claude/planning/2025-12-13-fusion.md` for the stream-of-consciousness vision, or `.claude/planning/2025-12-13-planning.md` for the synthesized version.

### 2. Know the Fleet (1 min)
Read `.claude/registry/agents.md` — 7 custom agents exist:
- **Active**: backend-architect, systems-thinker, agent-architect, process-cartographer
- **Dormant**: librarian, archivist, temporal-validator

### 3. Know the Processes (1 min)
Read `.claude/registry/processes.md` — 9 core processes mapped:
- 5 active (conversation, plugin dev, agent creation, reflection, task mgmt)
- 4 dormant (resource acquisition, artifact observation, KG construction, historical archaeology)

### 4. Know Today's Work (2 min)
Read `.claude/journal/2025/12/13/2025-12-13.md` — the daily entry synthesized from atomics.

Or browse atomics directly in `.claude/journal/2025/12/13/`:
- `14-30-subagent-exploration.md`
- `15-00-reflect-on-command.md`
- `15-15-agent-architecture-emerges.md`
- `15-30-process-cartographer-activated.md`
- `15-45-journal-atomic-model.md`
- `16-00-historical-archaeology-process.md`

## Key Directories

```
.claude/
├── README.md              ← You are here
├── agents/                ← Custom agent definitions (system prompts)
├── registry/
│   ├── agents.md          ← Fleet catalogue
│   └── processes.md       ← Workflow mapping
├── journal/               ← Atomic-first cross-session memory
│   └── 2025/12/13/        ← Today's atomics
├── briefings/             ← Strategic context for agents
├── planning/              ← Strategic thinking documents
├── perspectives/          ← Per-agent output namespaces
├── library/               ← Librarian's domain (dormant)
├── archive/               ← Archivist's domain (dormant)
├── logging/               ← Session transcripts (historical data!)
└── commands/              ← Slash commands

plugins/                   ← The actual plugin code
├── awareness/             ← Self-improvement, learning
├── journal/               ← Obsidian-style journaling
├── schedule/              ← Weekly schedule management
├── backlog/               ← Task tracking
├── brainstorm/            ← Structured ideation
├── logging/               ← Session logging
├── agents/                ← Agent framework skills
├── llms/                  ← LLM tooling skills
├── knowledge-graphs/      ← KG skills
├── exploration/           ← Environmental discovery
└── interface/             ← Interface stack navigation
```

## What's Active vs Dormant

### Active
- Multi-persona reflection (`/reflect-on`)
- Plugin development workflow
- Agent creation process
- Journal (atomic entries for Dec 13)
- Task management (backlog)

### Dormant (Defined but Not Running)
| Agent | What It Would Do | Blocker |
|-------|------------------|---------|
| **librarian** | Catalog external URLs, prevent duplicate fetches | Never invoked |
| **archivist** | Track all internal artifacts, surface patterns | Never invoked |
| **temporal-validator** | Track information validity over time | No FalkorDB connection |

### Designed but Not Started
- **Historical Archaeology**: Archivist + Librarian collaboration to backfill journal from session logs, git history, planning docs

## Immediate Continuation Points

### Option A: Activate Historical Archaeology
The session logs (`.claude/logging/`) contain 51 sessions spanning Dec 8-13. The archivist and librarian can mine these for historical atomic entries.

**To continue**: Invoke the archivist agent to scan internal sources, generate atomic entries for Dec 8, 11, 12.

### Option B: Activate Dormant Agents
The librarian and archivist are defined but never run. Their infrastructure exists (`.claude/library/`, `.claude/archive/`).

**To continue**: Invoke each agent to begin their work.

### Option C: Continue Plugin Development
The plugin ecosystem has 10 plugins. More capabilities can be added.

**To continue**: Review plugin architecture in CLAUDE.md, identify gaps.

### Option D: Connect Temporal Infrastructure
The temporal-validator agent needs FalkorDB + Graphiti connection.

**To continue**: Use `awareness:temporal-kg-memory` skill for guidance.

## The Journal System

**Atomic-First Model**:
```
Atomic entries (HH-MM-title.md) — PRIMARY
    ↓ synthesize into
Daily summaries (YYYY-MM-DD.md)
    ↓ synthesize into
Monthly summaries (YYYY-MM.md)
    ↓ synthesize into
Yearly summaries (YYYY.md)
```

Each atomic has mandatory fields: `created`, `author`, `description`, `parent_daily`, `tags`, `related`.

Bidirectional links create DNA spiral in Obsidian graph view.

## Five Core Primitives

From the fusion vision synthesis:

| Primitive | Essence |
|-----------|---------|
| **Context as Currency** | Every token has cost; CLAUDE.md as routing table |
| **Network of Networks** | Heterogeneous graphs with multiple edge types |
| **Temporal-Spatial Dimensions** | Knowledge has coordinates in time and space |
| **Metabolic Intelligence** | Ingest, digest, integrate, excrete |
| **Financial Metabolism** | Agents have budgets; value creates survival |

## How to Learn More

| Question | Where to Look |
|----------|---------------|
| What agents exist? | `.claude/registry/agents.md` |
| What processes run? | `.claude/registry/processes.md` |
| What happened today? | `.claude/journal/2025/12/13/2025-12-13.md` |
| What's the vision? | `.claude/planning/2025-12-13-fusion.md` |
| How do plugins work? | `CLAUDE.md` (root) |
| What plugins exist? | `plugins/` directory |
| What was discussed before? | `.claude/logging/` session transcripts |

## The Meta-Layer

Three agents form ecosystem self-awareness:

```
AGENT-ARCHITECT     ARCHIVIST           LIBRARIAN
"Who exists?"       "What flows?"       "What comes from outside?"
     │                   │                    │
     └───────────────────┼────────────────────┘
                         ▼
              ECOSYSTEM AWARENESS
```

## Closing Note

This repository is alive. It has metabolism (information flows), organs (agents), nervous system (logging, awareness), memory (journal, git), and immune system (temporal-validator checking staleness).

The skeleton is built. Some organs circulate. Others await activation.

Your work continues the emergence.

---

*Last updated: 2025-12-13*
*Maintained by: process-cartographer, archivist (when active)*
