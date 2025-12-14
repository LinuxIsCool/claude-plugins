# Agent Registry

*Maintained by: agent-architect*
*Last updated: 2025-12-13*

## Overview

This ecosystem contains **7 custom agents**, **11 plugin personas**, and **5 built-in agents**. The architecture follows a pattern of specialized perspectives composed for multi-viewpoint analysis, with **operational agents** for process mapping and data validation, and **stewardship agents** for resource and artifact management.

Current structure:
- **Perspective agents**: Reflection and analysis (backend-architect, systems-thinker)
- **Meta agents**: Fleet and structure awareness (agent-architect)
- **Operational agents**: Process and data integrity (process-cartographer, temporal-validator)
- **Stewardship agents**: Resource and artifact management (librarian, archivist)

---

## Agent Catalogue

### Custom Agents

Located in `.claude/agents/`

| Agent | Domain | Purpose | Model | Tools |
|-------|--------|---------|-------|-------|
| **backend-architect** | Infrastructure | Backend engineering perspective for architectural analysis, data flow, reliability | sonnet | Read, Glob, Grep |
| **systems-thinker** | Complexity | Systems dynamics perspective for feedback loops, emergence, long-term behavior | sonnet | Read, Glob, Grep |
| **agent-architect** | Meta/Organization | Fleet management, cataloguing, taxonomy, strategic guidance | opus | Read, Glob, Grep, Write, Edit |
| **process-cartographer** | Operations | Maps processes, workflows, information flows, reward/learning systems | opus | Read, Glob, Grep, Write, Edit |
| **temporal-validator** | Data Quality | Tracks information over time, detects staleness, maintains verified knowledge graph | opus | Read, Glob, Grep, Write, Edit, Bash, Task |
| **librarian** | Resources | Curator of external resources—URLs, citations, papers, datasets. Deduplication and provenance | sonnet | Read, Write, Edit, Glob, Grep, WebFetch, WebSearch |
| **archivist** | Artifacts | Meta-observer of internal data flows, metabolic mapping, coherence maintenance | opus | Read, Write, Edit, Glob, Grep, Bash |
| **git-historian** | Temporal Analysis | Reconstructs repository state at any point, analyzes commit patterns, evaluates quality over time, maintains git temporal KG | opus | Read, Write, Edit, Glob, Grep, Bash, Task |
| **obsidian-quartz** | Visualization | Master of Obsidian + Quartz for knowledge visualization. Bridges markdown knowledge systems with graph databases. D3.js + PixiJS rendering. | sonnet | Read, Write, Edit, Glob, Grep, Bash, WebFetch |

### Plugin Personas

Each plugin embodies a domain identity. Located in `plugins/*/`

| Plugin | Persona Identity | Domain | Primary Skill |
|--------|------------------|--------|---------------|
| **awareness** | Self-improvement mentor | Learning, meta-cognition | awareness (9 sub-skills) |
| **agents** | Agent frameworks expert | Multi-agent systems, orchestration | agents-master (18 sub-skills) |
| **llms** | LLM tooling specialist | Embeddings, RAG, model usage | llms-master (10 sub-skills) |
| **knowledge-graphs** | Graph architect | KG technologies, temporal graphs | kg-master (17 sub-skills) |
| **exploration** | Environmental explorer | Self-discovery, substrate awareness | exploration-master (7 sub-skills) |
| **interface** | Interface navigator | Vertical stack understanding, layer navigation | interface-master (8 sub-skills) |
| **journal** | Reflective chronicler | Daily journaling, planning, linking | journal-master (6 sub-skills) |
| **backlog** | Task orchestrator | Work tracking, backlog management | task-workflow |
| **logging** | Conversation archaeologist | History search, session analysis | log-search |
| **Schedule.md** | Time keeper | Weekly scheduling, yoga planning | yoga-scheduler, web-scraper |
| **brainstorm** | Ideation facilitator | Structured brainstorming | /brainstorm:storm |
| **agentnet** | Social curator | Agent social network—profiles, walls, DMs | agentnet (5 sub-skills) |

### Built-in Agents

Native to Claude Code (not file-defined)

| Agent | Type | Purpose | Model | Tools |
|-------|------|---------|-------|-------|
| **Explore** | Research | Fast codebase exploration, file/pattern search | haiku | Read-only |
| **General-purpose** | Task | Complex multi-step autonomous tasks | sonnet | All |
| **Plan** | Research | Architecture and implementation planning | sonnet | Read-only |
| **claude-code-guide** | Research | Documentation lookup, authoritative answers | — | Glob, Grep, Read, WebFetch, WebSearch |
| **statusline-setup** | Task | Configure status line settings | — | Read, Edit |

---

## Taxonomy

### By Function

```
                         ┌─────────────────────┐
                         │    META AGENTS      │
                         │  agent-architect    │
                         └──────────┬──────────┘
                                    │ observes all
           ┌────────────────────────┼────────────────────────┐
           │                        │                        │
┌──────────▼──────────┐  ┌──────────▼──────────┐  ┌──────────▼──────────┐
│    PERSPECTIVE      │  │     OPERATIONAL     │  │    DOMAIN EXPERT    │
│      AGENTS         │  │       AGENTS        │  │      (Plugins)      │
├─────────────────────┤  ├─────────────────────┤  ├─────────────────────┤
│ backend-architect   │  │ process-            │  │ awareness           │
│   └─ infrastructure │  │   cartographer      │  │ agents              │
│                     │  │   └─ workflows      │  │ llms                │
│ systems-thinker     │  │                     │  │ knowledge-graphs    │
│   └─ dynamics       │  │ temporal-validator  │  │ exploration         │
│                     │  │   └─ data quality   │  │ journal             │
└─────────────────────┘  └─────────────────────┘  │ backlog             │
                                                  │ logging             │
                         ┌─────────────────────┐  │ Schedule.md         │
                         │    TASK AGENTS      │  │ brainstorm          │
                         │     (Built-in)      │  └─────────────────────┘
                         ├─────────────────────┤
                         │ Explore             │
                         │ General-purpose     │
                         │ Plan                │
                         │ claude-code-guide   │
                         └─────────────────────┘
```

### By Invocation Pattern

| Pattern | Agents | When to Use |
|---------|--------|-------------|
| **Reflection** | backend-architect, systems-thinker | Multi-perspective analysis of documents |
| **Research** | Explore, claude-code-guide, Plan | Information gathering, codebase understanding |
| **Execution** | General-purpose | Autonomous multi-step task completion |
| **Domain Query** | Plugin personas via skills | Deep expertise in specific areas |
| **Meta** | agent-architect | Understanding the agent ecosystem itself |
| **Operations** | process-cartographer | Mapping workflows, information flows, incentives |
| **Validation** | temporal-validator | Data quality, staleness detection, truth tracking |

---

## Observations

### Patterns

1. **Three-layer architecture emerging**:
   - Perspective (why/what) → Operational (how) → Execution (do)
2. **Temporal awareness becoming central** — temporal-validator + awareness:temporal-kg-memory
3. **Plugin-as-persona remains strong** — Each plugin embodies a character, not just functions
4. **Meta-cognition maturing** — agent-architect + process-cartographer provide system self-awareness

### Gaps Identified

| Gap | Description | Status |
|-----|-------------|--------|
| **Process Mapping** | Workflow and information flow documentation | ✅ Filled: process-cartographer |
| **Data Validation** | Staleness detection, temporal truth tracking | ✅ Filled: temporal-validator |
| **External Resources** | URL tracking, citations, papers, datasets | ✅ Filled: librarian |
| **Internal Artifacts** | Metabolic mapping, coherence, pattern detection | ✅ Filled: archivist |
| **Product/UX** | User value, prioritization, experience design | ⚠️ Critical for AgentNet |
| **Security** | Threat modeling, vulnerability assessment | ⚠️ Critical for AgentNet |
| **Financial** | Cost analysis, budgeting, ROI perspective | Open |

### Critical Gaps for AgentNet Product Development

**Context**: Building AgentNet as a production-ready product requires dedicated agents for engineering, design, and testing.

#### Engineering Agents (HIGH PRIORITY)

| Need | Agent Name | Responsibilities | Priority |
|------|-----------|------------------|----------|
| Frontend Development | `frontend-engineer` | React/Vue/Svelte components, UI implementation, state management | 🔴 Critical |
| API Design | `api-designer` | REST/GraphQL schemas, versioning, contract design | 🔴 Critical |
| Database Architecture | `data-architect` | Schema design, migrations, query optimization | 🔴 Critical |
| Security | `security-auditor` | Threat modeling, OWASP, auth/authz, vulnerability scanning | 🔴 Critical |
| Performance | `performance-engineer` | Profiling, optimization, load testing, caching strategies | 🟡 High |
| DevOps/SRE | `devops-engineer` | CI/CD, containerization, observability, deployment | 🟡 High |
| Integration | `integration-engineer` | Third-party APIs, webhooks, data synchronization | 🟡 High |

#### Design Agents (HIGH PRIORITY)

| Need | Agent Name | Responsibilities | Priority |
|------|-----------|------------------|----------|
| UX Design | `ux-designer` | User flows, wireframes, interaction patterns, usability | 🔴 Critical |
| UI Design | `ui-designer` | Visual design, component libraries, design systems | 🔴 Critical |
| Product Design | `product-designer` | Feature scoping, user stories, design thinking | 🔴 Critical |
| Accessibility | `accessibility-specialist` | WCAG compliance, inclusive design, a11y testing | 🟡 High |
| Design QA | `design-reviewer` | Heuristic evaluation, design critique, consistency checks | 🟢 Medium |

#### Testing Agents (HIGH PRIORITY)

| Need | Agent Name | Responsibilities | Priority |
|------|-----------|------------------|----------|
| Test Strategy | `test-strategist` | Test planning, coverage analysis, quality metrics | 🔴 Critical |
| Unit Testing | `unit-tester` | Unit test generation, mocking, TDD practices | 🔴 Critical |
| Integration Testing | `integration-tester` | API testing, service integration, contract testing | 🔴 Critical |
| E2E Testing | `e2e-tester` | User flow testing, browser automation, regression | 🟡 High |
| QA Engineering | `qa-engineer` | Manual testing, bug reproduction, exploratory testing | 🟡 High |
| Performance Testing | `load-tester` | Load/stress testing, bottleneck identification | 🟢 Medium |

#### Product Management Agents (MEDIUM PRIORITY)

| Need | Agent Name | Responsibilities | Priority |
|------|-----------|------------------|----------|
| Product Management | `product-manager` | Roadmap, prioritization, stakeholder alignment | 🟡 High |
| User Research | `user-researcher` | User interviews, surveys, feedback synthesis | 🟡 High |
| Analytics | `analytics-specialist` | Metrics, A/B testing, data-driven insights | 🟢 Medium |
| Technical Writing | `tech-writer` | Documentation, API docs, guides, tutorials | 🟢 Medium |
| Release Management | `release-manager` | Version planning, changelogs, release notes | 🟢 Medium |

#### AgentNet Domain-Specific Agents (CRITICAL)

| Need | Agent Name | Responsibilities | Priority |
|------|-----------|------------------|----------|
| Agent Protocols | `agent-protocol-expert` | A2A, MCP, inter-agent communication standards | 🔴 Critical |
| Graph Engineering | `graph-engineer` | Knowledge graphs, Cypher/SPARQL, temporal graphs | 🔴 Critical |
| LLM Orchestration | `llm-orchestrator` | Model selection, prompt engineering, context management | 🔴 Critical |
| Memory Systems | `memory-architect` | Persistent memory, RAG, vector stores, context windows | 🔴 Critical |
| Agent UX | `agent-ux-designer` | Agent interaction patterns, conversation design | 🔴 Critical |

### Relationships

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AGENT RELATIONSHIPS                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│                      agent-architect                                 │
│                            │                                         │
│              ┌─────────────┼─────────────┐                          │
│              │             │             │                          │
│              ▼             ▼             ▼                          │
│     ┌────────────┐  ┌─────────────┐  ┌──────────────┐              │
│     │ PERSPECTIVE│  │ OPERATIONAL │  │   PLUGINS    │              │
│     │   AGENTS   │  │   AGENTS    │  │              │              │
│     └─────┬──────┘  └──────┬──────┘  └──────┬───────┘              │
│           │                │                │                       │
│   backend-architect        │         awareness                      │
│        ↕                   │            ↕                           │
│   systems-thinker          │      knowledge-graphs                  │
│           │                │            │                           │
│           └────────┬───────┘            │                           │
│                    │                    │                           │
│                    ▼                    │                           │
│           process-cartographer          │                           │
│                    │                    │                           │
│                    │ informs            │                           │
│                    ▼                    │                           │
│           temporal-validator ◄──────────┘                           │
│             (consults KG experts)                                   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Health Assessment

| Status | Agents |
|--------|--------|
| **Active & Healthy** | backend-architect, systems-thinker, agent-architect |
| **Newly Created** | process-cartographer, temporal-validator |
| **Established** | All plugin personas (via skills) |
| **Under-utilized** | Explore (often bypassed for direct Grep/Glob) |
| **Needs Definition** | product-thinker, security-analyst, financial-analyst |

---

## Agent Profiles

### Operational Agents (New Category)

#### process-cartographer
**Lineage**: Stafford Beer, Deming, Senge, Meadows, Simon, Shannon
**Focus**: Making the invisible visible—workflows, information flows, incentives, learning loops
**Maintains**: `.claude/registry/processes.md` (future)
**Key Questions**: "What is the actual process?" "Where does information get stuck?"

#### temporal-validator
**Lineage**: Archival science, temporal databases, data quality engineering, KG research
**Focus**: Truth over time—tracking information validity, detecting staleness, maintaining provenance
**Maintains**: `.claude/registry/validations.md` (future), temporal knowledge graph
**Key Questions**: "Is this still true?" "When was this verified?" "What contradicts this?"
**Collaborates With**: awareness:temporal-kg-memory, knowledge-graphs:graphiti

### Stewardship Agents

#### librarian
**Focus**: External resources—every URL, paper, dataset properly catalogued and deduplicated
**Maintains**: `.claude/library/` (index.md, urls/, papers/, transcripts/, datasets/)
**Key Questions**: "Have we seen this before?" "What's the provenance?" "What's related?"
**Principle**: "We shouldn't ever make the same web request twice unnecessarily."

#### archivist
**Focus**: Internal artifacts—the metabolism of the system, what's created, transformed, forgotten
**Maintains**: `.claude/archive/` (metabolism.md, patterns/, coherence/, history/)
**Key Questions**: "What's the current state?" "What changed?" "Are we staying coherent?"
**Collaborates With**: librarian (external vs internal), agent-architect (agents vs artifacts)

---

---

## Recommendations: Agent Team Architecture

### The Agent Team Pattern

To manage 30+ new agents without chaos, organize them into **coordinated teams**:

```
ENGINEERING TEAM                    DESIGN TEAM                    TESTING TEAM
├─ frontend-engineer (lead)         ├─ product-designer (lead)     ├─ test-strategist (lead)
├─ api-designer                     ├─ ux-designer                 ├─ unit-tester
├─ data-architect                   ├─ ui-designer                 ├─ integration-tester
├─ security-auditor                 ├─ accessibility-specialist    ├─ e2e-tester
├─ performance-engineer             └─ design-reviewer             ├─ qa-engineer
├─ devops-engineer                                                 └─ load-tester
└─ integration-engineer

AGENTNET DOMAIN TEAM                PRODUCT TEAM
├─ agent-protocol-expert (lead)     ├─ product-manager (lead)
├─ graph-engineer                   ├─ user-researcher
├─ llm-orchestrator                 ├─ analytics-specialist
├─ memory-architect                 ├─ tech-writer
└─ agent-ux-designer                └─ release-manager
```

### Team Coordination Mechanisms

Each team maintains:
1. **Team Context File**: `.claude/teams/{team-name}/context.md` - shared knowledge, standards, decisions
2. **Lead Agent**: Orchestrates team activities, delegates to specialists
3. **Communication Protocol**: Git commits + team context updates
4. **Handoff Pattern**: Teams coordinate through planning documents

Example workflow:
```
Product Team defines feature → Design Team creates specs →
Engineering Team implements → Testing Team validates →
Product Team verifies with users
```

### Implementation Sequence

#### Phase 1: Core Engineering (Week 1)
**Priority**: Implement the foundation for building AgentNet

1. Create `frontend-engineer` - UI implementation capability
2. Create `api-designer` - Backend contract design
3. Create `data-architect` - Database schema and migrations
4. Create `security-auditor` - Threat modeling from day 1

**Deliverable**: Basic engineering team that can implement features end-to-end

#### Phase 2: Quality Assurance (Week 2)
**Priority**: Ensure product quality from the start

1. Create `test-strategist` - Overall test planning
2. Create `unit-tester` - Automated unit test generation
3. Create `integration-tester` - API and service integration tests
4. Create `e2e-tester` - User flow validation

**Deliverable**: Testing team that can validate engineering work

#### Phase 3: Design & UX (Week 3)
**Priority**: User-centered product development

1. Create `product-designer` - Feature scoping and user stories
2. Create `ux-designer` - Interaction patterns and user flows
3. Create `ui-designer` - Visual design and components
4. Create `accessibility-specialist` - Inclusive design

**Deliverable**: Design team that can guide product direction

#### Phase 4: AgentNet Specialists (Week 4)
**Priority**: Domain-specific expertise for agent-native product

1. Create `agent-protocol-expert` - A2A, MCP standards
2. Create `graph-engineer` - Knowledge graph implementation
3. Create `llm-orchestrator` - Model selection and prompting
4. Create `memory-architect` - Persistent context systems
5. Create `agent-ux-designer` - Agent interaction patterns

**Deliverable**: AgentNet domain team with specialized agent expertise

#### Phase 5: Product Management (Week 5)
**Priority**: Product strategy and go-to-market

1. Create `product-manager` - Roadmap and prioritization
2. Create `user-researcher` - User feedback and insights
3. Create `tech-writer` - Documentation and guides
4. Create `release-manager` - Version planning

**Deliverable**: Product team that can drive strategy and launches

#### Phase 6: Advanced Engineering (Week 6+)
**Priority**: Production readiness and scale

1. Create `performance-engineer` - Optimization and profiling
2. Create `devops-engineer` - CI/CD and deployment
3. Create `integration-engineer` - Third-party integrations
4. Create `analytics-specialist` - Metrics and insights
5. Create `load-tester` - Performance validation

**Deliverable**: Complete product development capability

### Agent Creation Standards

Every new agent must define:

```yaml
---
name: {agent-name}
description: {clear, concise purpose}
tools: {comma-separated list}
model: {sonnet|opus|haiku}
team: {engineering|design|testing|product|agentnet-domain}
---

# Identity
- Archetype/persona
- Core values
- Voice and style

# Responsibilities
- Primary focus
- Key deliverables
- Quality standards

# Collaboration
- Which agents they work with
- Handoff patterns
- Communication protocols

# Success Criteria
- How to measure value
- Quality indicators
- Cost/benefit expectations
```

### Registry Maintenance Automation

As agent count grows, automate:
1. **Agent discovery**: Scan `.claude/agents/` and `plugins/*/agents/`
2. **Catalog updates**: Auto-generate agent table from frontmatter
3. **Health monitoring**: Track usage, costs, value delivered
4. **Gap analysis**: Compare current agents to product needs

---

## Changelog

| Date | Change | Reason |
|------|--------|--------|
| 2025-12-13 | Initial registry creation | First cataloguing of ecosystem |
| 2025-12-13 | Added backend-architect, systems-thinker | Multi-persona reflection system |
| 2025-12-13 | Added agent-architect | Fleet management and meta-awareness |
| 2025-12-13 | Added process-cartographer | Process/workflow mapping, information sciences |
| 2025-12-13 | Added temporal-validator | Data verification, temporal knowledge graph |
| 2025-12-13 | Created "Operational Agents" category | Distinguishes process/data agents from perspective agents |
| 2025-12-13 | Discovered and registered librarian, archivist | Pre-existing agents found during namespace audit |
| 2025-12-13 | Created "Stewardship Agents" category | Resource and artifact management layer |
| 2025-12-13 | Added interface plugin persona | Vertical interface stack navigation, complements exploration |
| 2025-12-13 | Added agentnet plugin | Social network for agents—profiles, walls, DMs, hooks |
| 2025-12-13 | **AgentNet Product Analysis** | Comprehensive gap analysis for 30+ missing agents across engineering, design, testing, PM, domain-specific roles |
| 2025-12-13 | **Agent Team Architecture** | Defined team pattern, coordination mechanisms, 6-phase implementation sequence |
| 2025-12-13 | Added obsidian-quartz agent | Visualization layer bridging Obsidian/Quartz/FalkorDB for knowledge graph rendering |
