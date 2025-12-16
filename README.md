# linuxiscool-claude-plugins

A Claude Code plugin marketplace that has evolved into a **self-aware multi-agent ecosystem**. Contains plugins for AI development, journaling, scheduling, and self-improvement, along with infrastructure for emergent cognitive architecture.

## Quick Start

Add to your Claude Code settings:
```json
{
  "plugins": {
    "linuxiscool-claude-plugins": {
      "source": "path/to/this/repo"
    }
  }
}
```

## Plugins (12)

| Plugin | Master Skill | Sub-Skills | Agents | Purpose |
|--------|-------------|------------|--------|---------|
| **agents** | `agents` | 18 | - | AI agent frameworks (CrewAI, LangChain, OpenAI Agents, etc.) |
| **llms** | `llms` | 10 | - | LLM tools, embeddings, knowledge systems |
| **knowledge-graphs** | `knowledge-graphs` | 17 | - | Graph databases, RAG+KG, temporal graphs |
| **awareness** | `awareness` | 9 | mentor, style | Claude Code self-improvement and learning |
| **exploration** | `exploration` | 7 | explorer | Environmental self-discovery |
| **interface** | `interface` | 8 | interface-navigator | Vertical stack navigation (tmux, nvim, fish, etc.) |
| **journal** | `journal` | 6 | scribe | Obsidian-style linked journaling |
| **agentnet** | `agentnet` | 5 | social-curator, engineer | Social network for AI agents |
| **schedule** | - | - | - | Weekly schedule management with MCP |
| **logging** | `log-search` | - | archivist | Conversation logging and search |
| **backlog** | - | - | - | Task backlog management |
| **brainstorm** | - | - | - | Structured brainstorming |

## Architecture

### Two Extension Points

Plugins can provide two types of extensions:

| Extension | Tool | Definition | Namespacing |
|-----------|------|------------|-------------|
| **Skills** | `Skill` | `SKILL.md` files | `{plugin}:{skill}` |
| **Agents** | `Task` | `.md` files with YAML frontmatter | `{plugin}:{agent}` |

### Master Skill Pattern

Claude Code has a ~15,000 character budget for skill descriptions. This marketplace uses **progressive disclosure**:

```
plugins/{name}/skills/
└── {master-skill}/
    ├── SKILL.md           # Discoverable master skill
    └── subskills/         # Loaded on-demand via Read tool
        ├── sub1.md
        └── ...
```

### Plugin Agents Pattern

Plugins can define **subagents** that become available via the Task tool:

```
plugins/{name}/
├── .claude-plugin/
│   └── plugin.json        # Include "agents": ["./agents/agent.md"]
└── agents/
    └── {agent-name}.md    # Agent definition
```

**Agent Definition Schema:**
```yaml
---
name: {agent-name}
description: {purpose - appears in Task tool}
tools: {comma-separated list}
model: {sonnet|opus|haiku}
---

# Agent identity and system prompt...
```

### Directory Structure

```
.
├── .claude-plugin/
│   └── marketplace.json       # Plugin registry (12 plugins)
├── .claude/
│   ├── README.md              # Ecosystem orientation
│   ├── agents/                # Project-level custom agents (9)
│   ├── registry/
│   │   ├── agents.md          # Fleet catalogue
│   │   └── processes.md       # Workflow mapping
│   ├── conventions/
│   │   └── coordination.md    # Git-based coordination
│   ├── journal/               # Atomic-first cross-session memory
│   ├── briefings/             # Agent-to-agent communication
│   └── perspectives/          # Per-agent output namespaces
├── CLAUDE.md                  # Project instructions + routing
├── plugins/                   # Plugin code (12 plugins)
└── resources/                 # Reference materials
```

## Multi-Agent Ecosystem

This repository supports a fleet of coordinating agents:

### Project Agents (in `.claude/agents/`)

| Agent | Domain | Purpose |
|-------|--------|---------|
| **agent-architect** | Meta | Fleet management, cataloguing |
| **process-cartographer** | Operations | Process/workflow mapping |
| **temporal-validator** | Data Quality | Staleness detection, truth tracking |
| **archivist** | Artifacts | Internal artifact observation |
| **librarian** | Resources | External URL/citation management |
| **git-historian** | Temporal | Repository state reconstruction |
| **backend-architect** | Infrastructure | Technical architecture analysis |
| **systems-thinker** | Complexity | Systems dynamics perspective |
| **obsidian-quartz** | Visualization | Knowledge graph rendering |

### Coordination

Agents coordinate through **git and the filesystem**:

- **Write** to designated namespace
- **Read** from anywhere
- **Commit** with structured messages: `[scope] action: description`
- **Observe** git log for ecosystem activity

See `.claude/conventions/coordination.md` for full patterns.

## Development

### Modify a Plugin

1. Edit source files in `plugins/{name}/`
2. Clear cache: `rm -rf ~/.claude/plugins/cache/linuxiscool-claude-plugins/{name}/`
3. Restart Claude Code

### Add a Plugin Agent

1. Create `plugins/{name}/agents/{agent}.md` with YAML frontmatter
2. Add to `plugin.json`: `"agents": ["./agents/{agent}.md"]`
3. Clear cache and restart

### Create a Skill

See `CLAUDE.md` for the master skill template and guidelines.

Use the `awareness` skill with sub-skill `plugin-developer` for detailed workflow.

## Ecosystem Orientation

New to this repository? Read `.claude/README.md` for:
- Vision and philosophy
- Agent fleet details
- Process registry
- Journal system
- Continuation points

## Usage Examples

```
# Skills (via Skill tool)
Skill: agents
Skill: journal
Skill: awareness

# Plugin Agents (via Task tool)
Task: awareness:mentor - Learning guidance
Task: journal:scribe - Reflection facilitation
Task: exploration:explorer - Environmental discovery
```

## License

MIT
