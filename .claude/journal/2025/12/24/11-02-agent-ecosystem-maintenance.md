---
id: 2025-12-24-1102
title: "Agent Ecosystem Maintenance: Naming, Archiving, and Registry Rebuild"
type: atomic
created: 2025-12-24T11:02:18-08:00
author: claude-opus-4
description: "Resolved 3 naming collisions, archived 1 redundant agent, and rebuilt the complete agent registry from 45 to 44 agents"
tags: [agents, maintenance, registry, naming, architecture, ecosystem]
parent_daily: [[2025-12-24]]
related:
  - [[10-52-agent-ecosystem-audit]]
---

# Agent Ecosystem Maintenance: Naming, Archiving, and Registry Rebuild

Following the [[10-52-agent-ecosystem-audit]], executed the recommended maintenance actions to improve agent ecosystem health. This entry documents the specific changes made, the reasoning behind each decision, and the lessons learned.

## Context

The audit identified three categories of issues requiring immediate attention:

1. **Naming collisions**: Three plugins each defined an agent named `analyst`
2. **Redundancy**: A project-level agent duplicated plugin functionality
3. **Registry staleness**: Documentation was 24+ agents behind reality

## Actions Taken

### 1. Resolved Naming Collisions

The `analyst` name appeared in three plugins, each with a distinct domain:

| Plugin | Old Path | New Path | Purpose |
|--------|----------|----------|---------|
| messages | `plugins/messages/agents/analyst.md` | `plugins/messages/agents/message-analyst.md` | Message pattern analysis |
| transcripts | `plugins/transcripts/agents/analyst.md` | `plugins/transcripts/agents/transcript-analyst.md` | Entity extraction, topic modeling |
| perf | `plugins/perf/agents/analyst.md` | `plugins/perf/agents/perf-analyst.md` | Performance investigation |

**For each agent, three changes were required:**

1. Edit the `name:` field in the agent's YAML frontmatter
2. Rename the file itself (`.md` extension)
3. Update the `agents` array in the plugin's `.claude-plugin/plugin.json`

**Example - messages plugin:**

Before:
```json
"agents": [
  "./agents/correspondent.md",
  "./agents/indexer.md",
  "./agents/analyst.md"
]
```

After:
```json
"agents": [
  "./agents/correspondent.md",
  "./agents/indexer.md",
  "./agents/message-analyst.md"
]
```

### 2. Archived Redundant Agent

The project-level `obsidian-quartz` agent (`.claude/agents/obsidian-quartz.md`) was identified as redundant. Its functionality had been absorbed by the plugin-level `obsidian:visualizer` agent (`plugins/obsidian/agents/visualizer.md`).

**Action:**
```bash
mkdir -p .claude/archive/agents
mv .claude/agents/obsidian-quartz.md .claude/archive/agents/
```

The archive location preserves the agent for historical reference without cluttering the active agent namespace.

### 3. Rebuilt Agent Registry

The registry at `.claude/registry/agents.md` was severely outdated:
- **Old state**: 9 project agents, 12 plugin personas documented
- **New state**: 9 project agents, 35 plugin agents documented

**New registry structure:**

```
# Agent Registry

## Overview
- Total: 44 agents (9 project, 35 plugin)
- Categories: Perspective, Meta, Operational, Stewardship, Domain Expert

## Project-Level Agents
- Table with: Agent, Purpose, Model, Tools

## Plugin-Level Agents (organized by plugin)
- 24 plugins with agents
- Each with: Agent, Purpose, Model, Tools

## Model Distribution
- opus: 10 agents
- sonnet: 28 agents
- haiku: 4 agents
- inherit: 2 agents

## Taxonomy by Function
- ASCII tree showing hierarchical organization

## Invocation Patterns
- How to call each agent type

## Agent Disambiguation
- Notes on shared names (two "archivist" agents)

## Archived Agents
- obsidian-quartz (reason: superseded)

## Changelog
- Today's changes documented
```

## Technical Details

### Plugin.json Agent Declaration

Claude Code discovers plugin agents through the `agents` field in `plugin.json`:

```json
{
  "name": "plugin-name",
  "agents": [
    "./agents/agent-one.md",
    "./agents/agent-two.md"
  ]
}
```

**Key observations:**
- The `agents` field requires explicit file paths (unlike `skills` and `commands` which accept directories)
- Agents are namespaced as `{plugin}:{agent-name}` when invoked
- The `name` field inside the agent `.md` file determines the agent's identity in logs and outputs

### Cache Implications

After renaming agents, the plugin cache may need clearing:

```bash
rm -rf ~/.claude/plugins/cache/linuxiscool-claude-plugins/{messages,transcripts,perf}/
```

Without cache clearing, Claude Code may not recognize the renamed agents until the next cache refresh.

### Model Selection Patterns

Observed model selection patterns across the 44 agents:

| Model | When Used |
|-------|-----------|
| **opus** | Complex reasoning, meta-cognition, strategic decisions, multi-perspective synthesis |
| **sonnet** | Standard domain expertise, most operational tasks |
| **haiku** | Lightweight tasks, timestamp injection, fast health checks |
| **inherit** | When the agent should use the calling context's model |

Examples:
- `board-mentor` uses opus for multi-perspective advisory combining Naval, Elon, Dragons Den
- `chronologist` uses haiku for lightweight timestamp injection
- `correspondent` uses inherit to match the user's current model selection

## Insights

### 1. Naming Matters for Observability

When multiple agents share a name, debugging becomes difficult:
- Git commits with `[agent:analyst]` don't indicate which analyst
- Task outputs blur together in logs
- Cross-referencing conversation history fails

Domain-prefixed names (`message-analyst`, `transcript-analyst`, `perf-analyst`) provide immediate context.

### 2. The Archive Pattern

Rather than deleting superseded agents, archiving preserves:
- Historical decisions about agent design
- Reference implementations
- The ability to restore if the replacement proves inadequate

Location: `.claude/archive/agents/`

### 3. Registry as Living Documentation

The registry serves multiple purposes:
- **Discovery**: What agents exist and what can they do?
- **Disambiguation**: Which "archivist" do I want?
- **Governance**: Who maintains what, and what's the model cost?
- **Evolution**: What changed and when?

Automated registry generation (from agent frontmatter) would prevent future staleness.

### 4. Plugin Architecture Scalability

The ecosystem grew from 7 documented agents to 44 actual agents organically. The plugin architecture enables this:
- Each plugin owns its agents
- Namespacing prevents collisions at the Task tool level
- Agents can be added without modifying core configuration

However, the registry staleness shows that documentation doesn't scale automatically.

## Files Modified

```
.claude/agents/obsidian-quartz.md
  → archived to .claude/archive/agents/obsidian-quartz.md

plugins/messages/agents/analyst.md
  → renamed to plugins/messages/agents/message-analyst.md
  → name field: analyst → message-analyst

plugins/messages/.claude-plugin/plugin.json
  → agents array: ./agents/analyst.md → ./agents/message-analyst.md

plugins/transcripts/agents/analyst.md
  → renamed to plugins/transcripts/agents/transcript-analyst.md
  → name field: analyst → transcript-analyst

plugins/transcripts/.claude-plugin/plugin.json
  → agents array: ./agents/analyst.md → ./agents/transcript-analyst.md

plugins/perf/agents/analyst.md
  → renamed to plugins/perf/agents/perf-analyst.md
  → name field: analyst → perf-analyst

plugins/perf/.claude-plugin/plugin.json
  → agents array: ./agents/analyst.md → ./agents/perf-analyst.md

.claude/registry/agents.md
  → complete rebuild with 44 agents
```

## Remaining Work

### Medium Priority

1. **Validate plugin cache after restart** - Confirm renamed agents are discoverable
2. **Update any hardcoded references** - Search for "analyst" in skills/commands that might reference old names
3. **Consider renaming logging:archivist** - Two agents named "archivist" still exist (though with different scopes)

### Low Priority

4. **Automate registry generation** - Script to extract frontmatter and build registry
5. **Add usage analytics** - Track which agents are actually invoked
6. **Document agent relationships** - Which agents spawn which sub-agents

## Metrics

| Metric | Before | After |
|--------|--------|-------|
| Name collisions | 3 | 0 |
| Redundant agents | 1 | 0 |
| Registry coverage | ~47% (21/45) | 100% (44/44) |
| Project agents | 10 | 9 |
| Plugin agents | 35 | 35 |
| Total | 45 | 44 |

---

*Parent: [[2025-12-24]]*
