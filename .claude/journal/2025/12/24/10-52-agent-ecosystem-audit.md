---
id: 2025-12-24-1052
title: "Agent Ecosystem Audit: 45 Agents Strong"
type: atomic
created: 2025-12-24T10:52:33-08:00
author: claude-opus-4
description: "Comprehensive audit reveals 45 agents across project and plugin levels, with 3 naming collisions and 1 redundancy to address"
tags: [agents, audit, ecosystem, meta, architecture]
parent_daily: [[2025-12-24]]
related: []
---

# Agent Ecosystem Audit: 45 Agents Strong

On Christmas Eve 2025, conducted a comprehensive audit of the agent ecosystem using the agent-architect meta-agent. The results reveal significant organic growth from the originally documented 7 custom agents to a thriving fleet of 45.

## Context

User requested a health check on the various agents throughout the ecosystem. This prompted spawning the `agent-architect` agent (an opus-powered meta-agent designed specifically to catalogue and track the agent fleet) to perform a systematic audit.

## Findings

### Distribution

| Location | Count |
|----------|-------|
| Project-level (`.claude/agents/`) | 10 |
| Plugin-level (`plugins/*/agents/`) | 35 |
| **Total** | **45** |

### Health Summary

| Status | Count | Details |
|--------|-------|---------|
| Healthy | 41 | Clear identity, purpose, and tools |
| Name Collision | 3 | `analyst` appears in messages, transcripts, and perf plugins |
| Redundant | 1 | `obsidian-quartz` superseded by `visualizer` |

### Notable Agent Teams

**Company Team (5 agents)**
- `board-mentor` (opus) - Multi-perspective advisory with Naval, Elon personas
- `ceo`, `cfo`, `cto` (sonnet) - Executive perspectives
- `chief-of-staff` (haiku) - Operations coordination

**Obsidian Team (4 agents)**
- `graph-curator` - Graph connectivity and orphan detection
- `vault-health` - Vault auditing
- `visualizer` - Quartz/Obsidian visualization
- `link-suggester` - Semantic link suggestions

**Meta Agents (5 agents)**
- `agent-architect` - Fleet management (this audit)
- `archivist` (project) - Ecosystem metabolism
- `mentor` - Self-improvement guide
- `style` - Values guardian
- `orchestrator` - Multi-framework expert

### Model Distribution

| Model | Count | Use Cases |
|-------|-------|-----------|
| Opus | 10 | Complex reasoning, meta-cognition |
| Sonnet | 29 | Standard operations, domain expertise |
| Haiku | 4 | Lightweight tasks, fast responses |

## Issues Requiring Action

### 1. Name Collisions (Priority: High)

Three plugins each define an agent named `analyst`:
- `plugins/messages/agents/analyst.md`
- `plugins/transcripts/agents/analyst.md`
- `plugins/perf/agents/analyst.md`

**Resolution**: Rename to unique identifiers:
- `message-analyst`
- `transcript-analyst`
- `perf-analyst`

### 2. Redundant Agent (Priority: Medium)

`.claude/agents/obsidian-quartz.md` contains explicit note that it's been absorbed by `plugins/obsidian/agents/visualizer.md`.

**Resolution**: Archive or delete the project-level agent.

### 3. Registry Staleness (Priority: High)

`.claude/registry/agents.md` is severely outdated:
- Last updated: 2025-12-15
- Documents only 9 project + 12 plugin agents
- Missing 24+ agents entirely

**Resolution**: Complete rebuild of registry with all 45 agents.

## Next Steps

### Immediate (This Session or Next)

1. **Rename duplicate analysts**
   - Edit `plugins/messages/agents/analyst.md` → rename to `message-analyst`
   - Edit `plugins/transcripts/agents/analyst.md` → rename to `transcript-analyst`
   - Edit `plugins/perf/agents/analyst.md` → rename to `perf-analyst`
   - Update any `plugin.json` references

2. **Archive redundant agent**
   - Move `.claude/agents/obsidian-quartz.md` to `.claude/archive/agents/`
   - Or delete if archive isn't maintained

3. **Update registry**
   - Regenerate `.claude/registry/agents.md` with complete agent list
   - Include all 45 agents with proper categorization
   - Add model and tools columns

### Medium-Term (Within Week)

4. **Validate plugin.json declarations**
   - Ensure all plugin agents are properly declared
   - Check namespacing consistency

5. **Document agent relationships**
   - Create relationship graph showing collaboration patterns
   - Identify which agents spawn which sub-agents

6. **Standardize model selection**
   - Review haiku vs sonnet choices
   - Document model selection criteria

### Long-Term (Ongoing)

7. **Usage analytics**
   - Consider implementing agent invocation tracking
   - Understand which agents are actually used

8. **Health monitoring**
   - Automated checks for agent definition quality
   - Detect drift between registry and reality

## Insights

The audit reveals **coherent pluralism** - each agent has a distinct voice and responsibility, yet they feel like a coordinated family. The organic growth from 7 to 45 agents demonstrates the plugin architecture's scalability, but also highlights the need for better meta-documentation.

The agent-architect agent itself is a fascinating example of meta-cognition: an agent whose purpose is to understand and manage other agents. This recursive pattern enables the ecosystem to be self-documenting.

---

*Parent: [[2025-12-24]]*
