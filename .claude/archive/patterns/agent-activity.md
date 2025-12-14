# Agent Activity Patterns

*Archivist observations on agent behavior*
*First observation: 2025-12-13*

---

## Agent Fleet Status

### Custom Agents (8)

| Agent | Created | Times Invoked | Output Produced |
|-------|---------|---------------|-----------------|
| **backend-architect** | Dec 13 | 2 | 2 reflections |
| **systems-thinker** | Dec 13 | 2 | 2 reflections |
| **agent-architect** | Dec 13 | 3+ | Registry, journal entries |
| **process-cartographer** | Dec 13 | 1 | Process registry |
| **temporal-validator** | Dec 13 | 0 | (dormant) |
| **librarian** | Dec 13 | 0 | (dormant) |
| **archivist** | Dec 13 | 1 | This archive |
| **git-historian** | Dec 13 | 1 | FalkorDB git_history graph |

### Plugin Personas (12)

| Plugin | Persona | Activity |
|--------|---------|----------|
| awareness | Self-improvement mentor | Skills invoked |
| agents | Agent frameworks expert | Skills defined |
| llms | LLM tooling specialist | Skills defined |
| knowledge-graphs | Graph architect | Skills defined |
| exploration | Environmental explorer | Commands run |
| journal | Reflective chronicler | Daily use |
| backlog | Task orchestrator | Commands available |
| logging | Conversation archaeologist | Active every session |
| Schedule.md | Time keeper | MCP tools active |
| brainstorm | Ideation facilitator | Commands available |
| interface | Interface navigator | Skills defined |
| agentnet | Social curator | Skills defined |

---

## Agent Interaction Patterns

### Observed Collaborations

1. **Multi-Persona Reflection**
   - `/reflect-on` invokes backend-architect + systems-thinker
   - Each produces perspective in `.claude/perspectives/{agent}/`
   - No direct agent-to-agent communication

2. **Registry Maintenance**
   - agent-architect updates `.claude/registry/agents.md`
   - process-cartographer updates `.claude/registry/processes.md`
   - No conflict—clear namespace ownership

3. **Git-Based Coordination**
   - Agents coordinate through file changes + git commits
   - No explicit messaging protocol
   - Works via filesystem observation

### Potential Collaborations (Not Yet Observed)

| Agent 1 | Agent 2 | Collaboration |
|---------|---------|---------------|
| git-historian | temporal-validator | Fact verification against git |
| librarian | archivist | External vs internal tracking |
| process-cartographer | systems-thinker | Workflow analysis |
| agent-architect | archivist | Fleet health assessment |

---

## Agent Output Locations

### Namespace Ownership

| Agent | Write Location | Status |
|-------|----------------|--------|
| backend-architect | `.claude/perspectives/backend-architect/` | Active |
| systems-thinker | `.claude/perspectives/systems-thinker/` | Active |
| agent-architect | `.claude/registry/agents.md` | Active |
| process-cartographer | `.claude/registry/processes.md` | Active |
| temporal-validator | `.claude/validations/` (future) | Dormant |
| librarian | `.claude/library/` | Dormant |
| archivist | `.claude/archive/` | Active (now) |
| git-historian | FalkorDB `git_history` | Active |

### Output Volume (Today)

| Agent | Files Created | Lines Written |
|-------|---------------|---------------|
| backend-architect | 2 | ~200 |
| systems-thinker | 2 | ~200 |
| agent-architect | 3 | ~350 |
| process-cartographer | 1 | ~150 |
| archivist | 4 | ~400 |
| git-historian | 2 scripts + KG | ~500 |

---

## Activation Patterns

### How Agents Get Invoked

1. **Slash Commands** - `/reflect-on`, `/awareness:mentor`
2. **Direct Task Tool** - User requests agent via Task
3. **Embodiment** - Human embodies agent perspective
4. **Autonomous** - Not yet observed (future: hooks?)

### Invocation Frequency (Dec 13)

```
agent-architect:       ███ 3+
backend-architect:     ██ 2
systems-thinker:       ██ 2
process-cartographer:  █ 1
git-historian:         █ 1
archivist:             █ 1 (this session)
temporal-validator:    (none)
librarian:             (none)
```

### Dormancy Analysis

| Agent | Why Dormant | What Would Activate |
|-------|-------------|---------------------|
| temporal-validator | No fact verification tasks | Query about "is X still true?" |
| librarian | No external URLs to catalogue | WebFetch of new resource |

---

## Agent Evolution

### Creation Timeline (Dec 13)

```
14:30  backend-architect, systems-thinker (reflection system)
15:15  agent-architect (meta-awareness)
15:30  process-cartographer (workflow mapping)
15:45  temporal-validator (data quality)
16:00  librarian, archivist (discovered from parallel session)
16:56  git-historian (temporal KG)
```

All 8 agents created in a single day. Rapid ecosystem formation.

### Capability Growth

```
Start of day:  0 custom agents
End of day:    8 custom agents
               + 12 plugin personas
               + 5 built-in agents
               = 25 total agent identities
```

---

## Health Indicators

### Healthy Signs
- Clear namespace ownership (no collisions)
- Git-based coordination working
- Multi-persona reflection functional
- Registry kept current

### Warning Signs
- 2 agents completely dormant (temporal-validator, librarian)
- No agent-to-agent direct communication yet
- High ratio of definition to invocation

### Recommendations

1. **Activate dormant agents** - Give them tasks
2. **Test agent composition** - Can agents invoke agents?
3. **Establish health checks** - Regular registry audits

---

*Agent activity will be tracked as the ecosystem evolves.*

---

## Update: 2025-12-13 ~18:00

### Archivist Second Activation

This session marks the archivist's second invocation, demonstrating continuity across sessions.

**What was done**:
1. Read previous observation artifacts (metabolism.md, patterns/, coherence/)
2. Examined what changed since last observation (~1 hour gap)
3. Created missing `topical.md` pattern file
4. Updated metabolism.md with current state
5. Updated this activity log

### Agent Invocation Count (Updated)

```
agent-architect:       ███ 3+
backend-architect:     ██ 2
systems-thinker:       ██ 2
process-cartographer:  █ 1
git-historian:         █ 1
archivist:             ██ 2 (this is the second)
temporal-validator:    (none)
librarian:             (none)
```

### New Observation: Archivist Continuity

Unlike other agents which perform discrete tasks, the archivist:
- Reads its own previous output
- Updates rather than recreates
- Maintains temporal continuity
- Tracks delta (change over time)

This is the **metabolic pattern** - the archivist digests the ecosystem's state and produces observations, which then become input for the next observation.

### Agent Collaboration Patterns Observed

| From | To | Via | Purpose |
|------|----|-----|---------|
| Multiple sessions | git-historian | FalkorDB | Historical queries |
| archivist | journal | Reading entries | Theme extraction |
| agent-architect | archivist | Registry file | Agent catalogue |

**Not yet observed**:
- Direct agent-to-agent invocation
- Librarian cataloguing external resources
- Temporal-validator verifying facts

### Dormancy Analysis (Updated)

| Agent | Hours Dormant | Infrastructure Ready | Activation Trigger |
|-------|---------------|---------------------|-------------------|
| temporal-validator | Since creation (~2h) | Yes (FalkorDB) | First "is X true?" query |
| librarian | Since creation (~3h) | Yes (.claude/library/) | First WebFetch |

### Next Expected Activations

1. **QA-engineer** (mentioned in registry) - Testing needs
2. **Librarian** - When external resources needed
3. **Temporal-validator** - When fact verification needed
