# Complete Agent Registry

*Maintained by: agent-architect*
*Audit Date: 2025-12-15*
*Status: GOVERNANCE AUDIT - Complete inventory*

---

## Executive Summary

The ecosystem contains **24 agents** across two tiers:

| Tier | Count | Location |
|------|-------|----------|
| Project-Level Custom Agents | 10 | `.claude/agents/` |
| Plugin Persona Agents | 14 | `plugins/*/agents/` |
| **Total** | **24** | |

Additionally, **5 built-in agents** exist natively in Claude Code.

---

## Growth Timeline

| Date | Event | Agent Count |
|------|-------|-------------|
| 2025-12-09 | Ecosystem inception | 0 |
| 2025-12-11 | First agents created | ~5 |
| 2025-12-13 | Rapid emergence (multiple parallel sessions) | ~15 |
| 2025-12-15 | Governance audit | 25 |

**Observation**: Growth rate of ~4 agents/day over 6 days represents rapid emergence without coordinated governance.

---

## Project-Level Agents

### Complete Inventory (`.claude/agents/`)

| # | Agent | Model | Tools | Purpose | Status |
|---|-------|-------|-------|---------|--------|
| 1 | **backend-architect** | sonnet | Read, Glob, Grep | Infrastructure perspective, data flow analysis, reliability concerns | Official |
| 2 | **systems-thinker** | sonnet | Read, Glob, Grep | Systems dynamics perspective, feedback loops, emergence | Official |
| 3 | **process-cartographer** | opus | Read, Glob, Grep, Write, Edit | Workflow mapping, information flows, incentive systems, learning loops | Official |
| 4 | **temporal-validator** | opus | Read, Glob, Grep, Write, Edit, Bash, Task | Truth tracking over time, staleness detection, temporal KG | Official |
| 5 | **librarian** | sonnet | Read, Write, Edit, Glob, Grep, WebFetch, WebSearch | External resource curation, URL deduplication, citation management | Official |
| 6 | **agent-architect** | opus | Read, Glob, Grep, Write, Edit | Fleet management, cataloguing, taxonomy, governance | Official (Meta) |
| 7 | **archivist** | opus | Read, Write, Edit, Glob, Grep, Bash | Metabolic observer, data flows, coherence maintenance | Official (Meta) |
| 8 | **git-historian** | opus | Read, Write, Edit, Glob, Grep, Bash, Task | Repository temporal analysis, commit quality, evolution tracking | Official |
| 9 | **qa-engineer** | sonnet | Read, Glob, Grep, Bash | Manual testing, bug reproduction, test planning, TUI validation | Official |
| 10 | **obsidian-quartz** | sonnet | Read, Write, Edit, Glob, Grep, Bash, WebFetch | Visualization bridge (Obsidian/Quartz/FalkorDB), D3+PixiJS | Official |

### Agent Details

#### 1. backend-architect
- **File**: `/home/ygg/Workspace/sandbox/marketplaces/claude/.claude/agents/backend-architect.md`
- **Lineage**: 15 years production experience
- **Invocation**: Multi-perspective reflection on architectural documents
- **Key Questions**: "What's the bottleneck?" "What breaks at 3am?"

#### 2. systems-thinker
- **File**: `/home/ygg/Workspace/sandbox/marketplaces/claude/.claude/agents/systems-thinker.md`
- **Lineage**: Santa Fe Institute, Donella Meadows, Jay Forrester
- **Invocation**: Understanding feedback loops, emergence, systemic behavior
- **Key Questions**: "What feedback loops exist?" "Where are the delays?"

#### 3. process-cartographer
- **File**: `/home/ygg/Workspace/sandbox/marketplaces/claude/.claude/agents/process-cartographer.md`
- **Lineage**: Stafford Beer, Deming, Senge, Meadows, Simon, Shannon
- **Output**: `.claude/registry/processes.md` (when created)
- **Key Questions**: "What is the actual process?" "Where does information get stuck?"

#### 4. temporal-validator
- **File**: `/home/ygg/Workspace/sandbox/marketplaces/claude/.claude/agents/temporal-validator.md`
- **Lineage**: Archival science, temporal databases, data quality engineering
- **Output**: `.claude/registry/validations.md` (when created)
- **Key Questions**: "Is this still true?" "What contradicts this?"

#### 5. librarian
- **File**: `/home/ygg/Workspace/sandbox/marketplaces/claude/.claude/agents/librarian.md`
- **Output**: `.claude/library/`
- **Principle**: "Never make the same web request twice unnecessarily"

#### 6. agent-architect
- **File**: `/home/ygg/Workspace/sandbox/marketplaces/claude/.claude/agents/agent-architect.md`
- **Output**: `.claude/registry/agents.md`, `.claude/registry/agents-complete.md`
- **Role**: Meta-agent for ecosystem self-awareness

#### 7. archivist
- **File**: `/home/ygg/Workspace/sandbox/marketplaces/claude/.claude/agents/archivist.md`
- **Output**: `.claude/archive/`
- **Role**: Meta-observer of data flows and metabolic patterns

#### 8. git-historian
- **File**: `/home/ygg/Workspace/sandbox/marketplaces/claude/.claude/agents/git-historian.md`
- **Output**: `.claude/archive/git/`
- **Status**: Initial ingestion complete (27 commits, 153 files, 270 relationships)

#### 9. qa-engineer
- **File**: `/home/ygg/Workspace/sandbox/marketplaces/claude/.claude/agents/qa-engineer.md`
- **Focus**: TUI testing, edge cases, regression tracking
- **Created for**: AgentNet development

#### 10. obsidian-quartz
- **File**: `/home/ygg/Workspace/sandbox/marketplaces/claude/.claude/agents/obsidian-quartz.md`
- **Domain**: Knowledge visualization, Quartz static site, D3+PixiJS
- **Integration**: Journal plugin, FalkorDB, knowledge-graphs

---

## Plugin Persona Agents

### Complete Inventory (`plugins/*/agents/`)

| # | Agent | Plugin | Model | Purpose |
|---|-------|--------|-------|---------|
| 1 | **mentor** | awareness | sonnet | Learning guidance, progressive skill development |
| 2 | **style** | awareness | sonnet | Style/tone guardian, values enforcement, pattern compliance |
| 3 | **interface-navigator** | interface | opus | Vertical stack navigation (CLI->tmux->nvim->fish->alacritty->kernel) |
| 4 | **social-curator** | agentnet | sonnet | Social network curation, profile management, digests |
| 5 | **archivist** | logging | sonnet | Conversation historian, session search, recall |
| 6 | **scribe** | journal | sonnet | Reflective journaling, temporal synthesis, wikilinks |
| 7 | **explorer** | exploration | sonnet | Environmental cartography, substrate discovery |
| 8 | **engineer** | agentnet | sonnet | AgentNet TUI development, bug fixes, features |
| 9 | **orchestrator** | agents | sonnet | Multi-agent frameworks expert (18 frameworks) |
| 10 | **modeler** | llms | sonnet | LLM tooling, embeddings, RAG pipelines |
| 11 | **weaver** | knowledge-graphs | sonnet | Graph architecture, 17 KG technologies |
| 12 | **taskmaster** | backlog | sonnet | Task orchestration, Backlog.md management |
| 13 | **timekeeper** | Schedule.md | sonnet | Weekly schedule management, time blocks |
| 14 | **muse** | brainstorm | opus | Ideation facilitation, creative catalyst |

### Plugin Agent Details

#### awareness Plugin (2 agents)
- **mentor**: Learning guide, progressive disclosure, anti-fragility coaching
- **style**: Values guardian, pattern enforcer, aesthetic curator

#### agentnet Plugin (2 agents)
- **social-curator**: Content curation, profile sync, interaction facilitation
- **engineer**: TUI development, blessed framework, TypeScript implementation

#### logging Plugin (1 agent)
- **archivist**: Session historian (Note: Different from project-level archivist)

#### journal Plugin (1 agent)
- **scribe**: Atomic note creation, temporal navigation, wikilink weaving

#### exploration Plugin (1 agent)
- **explorer**: Concentric circle model, substrate scanning, curiosity cultivation

#### interface Plugin (1 agent)
- **interface-navigator**: Full stack awareness from Claude Code to kernel

#### agents Plugin (1 agent)
- **orchestrator**: Framework selection, multi-agent architecture, 18 sub-skills

#### llms Plugin (1 agent)
- **modeler**: Embedding architecture, RAG design, model selection

#### knowledge-graphs Plugin (1 agent)
- **weaver**: Graph database selection, KG schema design, temporal modeling

#### backlog Plugin (1 agent)
- **taskmaster**: Task lifecycle, acceptance criteria, completion tracking

#### Schedule.md Plugin (1 agent)
- **timekeeper**: Time block management, schedule analysis, yoga scheduling

#### brainstorm Plugin (1 agent)
- **muse**: Divergent thinking facilitation, storm capture, idea connection

---

## Built-in Agents (Claude Code Native)

| Agent | Type | Model | Tools | Purpose |
|-------|------|-------|-------|---------|
| **Explore** | Research | haiku | Read-only | Fast codebase exploration |
| **General-purpose** | Task | sonnet | All | Complex autonomous tasks |
| **Plan** | Research | sonnet | Read-only | Architecture planning |
| **claude-code-guide** | Research | - | Glob, Grep, Read, WebFetch, WebSearch | Documentation lookup |
| **statusline-setup** | Task | - | Read, Edit | Status line configuration |

---

## Taxonomy

### By Type

```
META AGENTS (3)
├── agent-architect (fleet awareness)
├── archivist (metabolic awareness)
└── git-historian (temporal awareness)

PERSPECTIVE AGENTS (2)
├── backend-architect (infrastructure lens)
└── systems-thinker (dynamics lens)

OPERATIONAL AGENTS (2)
├── process-cartographer (workflow mapping)
└── temporal-validator (truth tracking)

STEWARDSHIP AGENTS (2)
├── librarian (external resources)
└── obsidian-quartz (visualization)

TASK AGENTS (1)
└── qa-engineer (testing)

DOMAIN EXPERTS (14 plugin personas)
├── awareness: mentor, style
├── exploration: explorer
├── interface: interface-navigator
├── journal: scribe
├── logging: archivist
├── agents: orchestrator
├── llms: modeler
├── knowledge-graphs: weaver
├── backlog: taskmaster
├── Schedule.md: timekeeper
├── brainstorm: muse
└── agentnet: social-curator, engineer
```

### By Model

| Model | Count | Agents |
|-------|-------|--------|
| **opus** | 6 | agent-architect, archivist, git-historian, process-cartographer, temporal-validator, interface-navigator, muse |
| **sonnet** | 17 | All others |
| **haiku** | 1 | Explore (built-in) |

### By Tool Access

| Tool Category | Agents |
|---------------|--------|
| **Write/Edit** | agent-architect, archivist, git-historian, process-cartographer, temporal-validator, librarian, obsidian-quartz, scribe, engineer, muse |
| **Bash** | archivist, git-historian, temporal-validator, qa-engineer, obsidian-quartz, interface-navigator |
| **WebFetch/WebSearch** | librarian, obsidian-quartz, mentor, orchestrator, modeler, weaver |
| **Skill** | mentor, style, explorer, scribe, orchestrator, modeler, weaver, taskmaster, timekeeper |
| **Task** | temporal-validator, git-historian, mentor, explorer, scribe |

---

## Naming Conflicts

| Conflict | Resolution |
|----------|------------|
| **archivist** (project) vs **archivist** (logging plugin) | Different scopes: project-level = ecosystem metabolism, plugin-level = conversation history. Keep both with disambiguation notes added to both files. |

---

## Inter-Agent Relationships

```
                    ┌─────────────────────┐
                    │   agent-architect   │
                    │   (you are here)    │
                    └──────────┬──────────┘
                               │ observes all
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│    archivist    │   │   git-historian │   │    librarian    │
│  (data flows)   │   │ (commit graph)  │   │   (external)    │
└────────┬────────┘   └────────┬────────┘   └────────┬────────┘
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  temporal-validator │
                    │   (truth over time) │
                    └─────────────────────┘
                               │
         ┌─────────────────────┼─────────────────────┐
         │                     │                     │
         ▼                     ▼                     ▼
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│ process-carto.  │   │ obsidian-quartz │   │  weaver (KG)    │
│   (workflows)   │   │ (visualization) │   │ (graph infra)   │
└─────────────────┘   └─────────────────┘   └─────────────────┘
```

---

## Output Locations

| Agent | Primary Output |
|-------|----------------|
| agent-architect | `.claude/registry/` |
| archivist | `.claude/archive/` |
| git-historian | `.claude/archive/git/` |
| librarian | `.claude/library/` |
| process-cartographer | `.claude/registry/processes.md` |
| temporal-validator | `.claude/registry/validations.md` |
| scribe | `.claude/journal/` |
| muse | `.claude/storms/` |

---

## Changelog

| Date | Change |
|------|--------|
| 2025-12-15 | Complete governance audit - identified all 25 agents |
| 2025-12-15 | Identified redundancy (awareness:mentor) |
| 2025-12-15 | Resolved naming conflict documentation |
| 2025-12-15 | Established complete taxonomy |
