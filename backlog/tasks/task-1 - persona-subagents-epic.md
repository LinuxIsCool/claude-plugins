---
id: task-1
title: "Ecosystem Activation: Awakening Dormant Agents and Adding Memory to Plugin Personas"
status: "In Progress"
priority: high
labels: [architecture, activation, memory, infrastructure]
milestone: v1.0-activation
created: 2025-12-12
updated: 2025-12-15
assignee: ["@claude"]
---

# Ecosystem Activation: Awakening Dormant Agents and Adding Memory to Plugin Personas

## Description

**Revised framing after discovery on 2025-12-15**: The persona subagent architecture already exists. This epic is about **activation and completion**, not construction.

### What Already Exists

| Component | Location | Status |
|-----------|----------|--------|
| 9 custom agents | `.claude/agents/` | 4 active, 5 dormant |
| 11 plugin personas | `plugins/*/skills/` + registry | Established via skills |
| Agent registry | `.claude/registry/agents.md` | Active, comprehensive |
| Process registry | `.claude/registry/processes.md` | 9 processes mapped |
| Archivist infrastructure | `.claude/archive/` | Directory exists, agent dormant |
| Librarian infrastructure | `.claude/library/` | Directory populated, agent dormant |
| Journal memory system | `.claude/journal/` | Active, atomic-first model |
| Perspectives namespaces | `.claude/perspectives/` | Active for some agents |
| Session logging | `.claude/logging/` | Active, 51+ sessions captured |

### What Needs Activation

1. **Dormant agents**: archivist, librarian, temporal-validator, git-historian, obsidian-quartz
2. **Historical archaeology**: Process 9 defined but never executed
3. **Memory persistence**: Plugin personas lack cross-session memory

### Original vs Revised Understanding

| Original Task | Revised Understanding |
|---------------|----------------------|
| "Build persona subagents" | Activate existing dormant agents |
| "Create persona identities" | Already exist in registry |
| "Design memory architecture" | Use existing journal + archive + library |
| "Build infrastructure" | Infrastructure exists, needs wiring |

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Archivist agent activated and producing observations
- [ ] #2 Librarian agent activated and cataloguing resources
- [ ] #3 Historical archaeology executed (backfill journal from logs)
- [ ] #4 Plugin personas have memory access pattern defined
- [ ] #5 Temporal-validator connected to knowledge graph
- [ ] #6 Memory persistence validated across sessions
- [ ] #7 Documentation updated to reflect activated state
<!-- AC:END -->

## Subtasks (Revised)

### Phase 1: Agent Activation
- [[task-1.1]] - Activate Archivist (artifact observation process)
- [[task-1.2]] - Activate Librarian (resource acquisition process)
- [[task-1.3]] - Execute Historical Archaeology (backfill journal)

### Phase 2: Knowledge Graph
- [[task-1.4]] - Connect Temporal-Validator to FalkorDB/Graphiti

### Phase 3: Plugin Persona Memory
- [[task-1.5]] - Define memory access pattern for plugin personas
- [[task-1.6]] - Prototype memory persistence with one plugin persona

### Future (v2.0)
- [[task-1.7]] - External infrastructure (Letta/Mem0) if markdown insufficient
- [[task-1.8]] - Advanced inter-agent coordination (A2A protocol)

## Key Insight

From `.claude/README.md`:
> "This repository is alive. It has metabolism, organs, nervous system, memory, and immune system. The skeleton is built. Some organs circulate. Others await activation."

**This work is organ activation, not organ construction.**

## Related Documents

- [[.claude/README.md]] - Ecosystem orientation
- [[.claude/registry/agents.md]] - Agent catalogue
- [[.claude/registry/processes.md]] - Process mapping
- [[.claude/storms/2025-12-15.md]] - Discovery brainstorm
- [[PERSONA_SUBAGENTS_STRATEGY.md]] - Original strategy (historical reference)
- [[ADR-001-persona-memory-architecture]] - Architecture decision

## Implementation Notes

### Session 2025-12-12
Research phase. Created original strategy proposing Letta/Mem0/Graphiti. Team consultation (STORM-001) favored markdown-native approach.

### Session 2025-12-15
Discovery: The persona architecture already exists. The ecosystem has:
- Defined agents with full system prompts
- Infrastructure directories ready for use
- Process documentation showing how things should flow
- Active logging capturing everything needed

The backlog has been revised to reflect activation rather than construction.
