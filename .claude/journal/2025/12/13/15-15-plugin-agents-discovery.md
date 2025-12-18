---
id: 2025-12-13-1515
title: "Plugin Agents: Native Namespacing Discovery"
type: atomic
created: 2025-12-13T15:27:00
author: claude-opus-4
description: "Discovered Claude Code natively supports plugin-defined agents with automatic namespacing via plugin.json agents field"
tags: [discovery, architecture, agents, plugins, claude-code]
parent_daily: [[2025-12-13]]
related:
  - [[15-15-agent-architecture-emerges]]
---

# Plugin Agents: Native Namespacing Discovery

Today we discovered that **Claude Code natively supports plugin-defined agents with automatic namespacing**.

## The Discovery

While designing a system to add subagents to plugins, we expected to need:
- A build script to aggregate plugin agents
- Manual copying to `.claude/agents/`
- Custom namespace injection

Instead, we found that `plugin.json` already supports an `agents` field:

```json
{
  "agents": ["./agents/mentor.md"]
}
```

The validation error that revealed this:
```
agents.0: Invalid input: must end with ".md"
```

This error told us:
1. The field exists and is validated
2. It expects specific `.md` file paths (not directories like `skills`)
3. Claude Code handles the rest automatically

## How It Works

```
Plugin defines:     plugins/awareness/agents/mentor.md
Claude Code reads:  plugin.json → "agents": ["./agents/mentor.md"]
Auto-namespaces:    awareness:mentor
Available as:       Task tool subagent_type
```

## The Pattern

| Component | Location | Naming |
|-----------|----------|--------|
| Project agents | `.claude/agents/foo.md` | `foo` |
| Plugin agents | `plugins/bar/agents/baz.md` | `bar:baz` |

## Key Insight

The `agents` field differs from `skills` and `commands`:
- `skills`: `["./skills/"]` ← directory glob
- `commands`: `["./commands/"]` ← directory glob
- `agents`: `["./agents/file.md"]` ← explicit files only

This explicit listing gives plugin authors control over which agents to expose.

## What We Built

1. **awareness:mentor** - The Mentor agent embodying the awareness plugin persona
2. **/awareness:mentor** - Slash command to invoke it with a learning goal
3. Documentation in CLAUDE.md for the pattern

## Implications

- Every plugin can ship domain-expert agents
- Namespacing prevents collisions
- The Task tool becomes extensible through plugins
- Agents can compose with skills (mentor invokes `awareness:awareness`)

## Questions for Later

- Can agents reference other agents? (agent composition)
- How do plugin agents interact with project agents?
- Should there be agent dependency declarations?

## Related

- [[awareness-plugin]]
- [[task-tool-architecture]]
- [[persona-subagents-strategy]]

---

*Parent: [[2025-12-13]]*
