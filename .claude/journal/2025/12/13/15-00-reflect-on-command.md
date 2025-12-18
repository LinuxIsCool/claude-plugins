---
id: 2025-12-13-1500
title: "Multi-Persona Reflection Command"
type: atomic
created: 2025-12-13T15:00:00
author: claude-opus-4
description: "Created /reflect-on slash command for multi-persona document reflection with namespace isolation"
tags: [agents, commands, reflection, personas, backend-architect, systems-thinker]
parent_daily: [[2025-12-13]]
related:
  - [[14-30-subagent-exploration]]
  - [[15-15-agent-architecture-emerges]]
---

# Multi-Persona Reflection Command

Built the `/reflect-on` slash command for multi-persona document analysis.

## Context

With subagent customization understood, wanted to create a practical tool: different agent personas reflecting on planning documents from their unique perspectives.

## What Was Created

### Slash Command

`.claude/commands/reflect-on.md`:
- Takes document path as `$ARGUMENTS`
- Discovers personas from `.claude/agents/`
- Generates reflections from each perspective
- Saves to `.claude/perspectives/{agent}/reflections/`

### Initial Agents

| Agent | Perspective |
|-------|-------------|
| `backend-architect` | Infrastructure, databases, scaling, security |
| `systems-thinker` | Complexity, emergence, feedback loops, dynamics |

### Namespace Pattern

```
.claude/perspectives/
├── backend-architect/
│   └── reflections/
│       └── 2025-12-13-fusion.md
└── systems-thinker/
    └── reflections/
        └── 2025-12-13-fusion.md
```

## Insights

- Each agent maintains isolated output namespace
- Reflections are artifacts, not ephemeral chat
- Multi-perspective analysis reveals blind spots
- Simple workflow: read document → embody persona → write reflection

## Limitation Discovered

Slash commands aren't available until next session. Had to execute workflow directly.

---
*Parent: [[2025-12-13]]*
