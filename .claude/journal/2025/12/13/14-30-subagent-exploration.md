---
id: 2025-12-13-1430
title: "Subagent Exploration"
type: atomic
created: 2025-12-13T14:30:00
author: claude-opus-4
description: "Discovered Claude CLI supports custom system prompts via --append-system-prompt, --system-prompt, and --agents flags"
tags: [discovery, subagents, cli, system-prompts]
parent_daily: [[2025-12-13]]
related:
  - [[15-00-reflect-on-command]]
  - [[15-15-agent-architecture-emerges]]
---

# Subagent Exploration

Discovered three approaches for custom system prompts in Claude CLI subagents.

## Context

User wanted to expand use of subagents with different personas/faculties. Invoked awareness:agent-creator and claude-code-guide to understand capabilities.

## Key Discoveries

### Custom Agents Directory

Agents defined in `.claude/agents/` with YAML frontmatter:
```yaml
---
name: agent-name
tools: Read, Glob, Grep
model: opus
---
# Markdown content becomes system prompt
```

### CLI Flags

| Flag | Effect |
|------|--------|
| `--append-system-prompt` | Adds to default prompt |
| `--system-prompt` | Replaces entire prompt |
| `--agents '{json}'` | Dynamic agent definition |

### Dynamic Agent JSON

```json
{
  "agents": [{
    "name": "custom-agent",
    "system_prompt": "Custom instructions..."
  }]
}
```

## Insights

- Agent markdown content IS the system prompt
- Model selection possible per-agent (sonnet, opus, haiku)
- Tool restrictions customizable per-agent
- No complex protocol needed—file conventions suffice

---
*Parent: [[2025-12-13]]*
