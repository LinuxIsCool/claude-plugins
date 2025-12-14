# linuxiscool-claude-plugins

A Claude Code plugin marketplace with specialized skills for AI development, journaling, scheduling, and self-improvement.

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

## Plugins

| Plugin | Master Skill | Sub-Skills | Purpose |
|--------|-------------|------------|---------|
| **agents** | `agents` | 18 | AI agent frameworks (CrewAI, LangChain, OpenAI Agents, etc.) |
| **llms** | `llms` | 10 | LLM tools, embeddings, knowledge systems |
| **knowledge-graphs** | `knowledge-graphs` | 17 | Graph databases, RAG+KG, temporal graphs |
| **awareness** | `awareness` | 9 | Claude Code self-improvement and learning |
| **exploration** | `exploration` | 7 | Environmental self-discovery |
| **journal** | `journal` | 6 | Obsidian-style linked journaling |
| **schedule** | - | - | Weekly schedule management with MCP |
| **logging** | - | - | Conversation logging and search |
| **backlog** | - | - | Task backlog management |
| **brainstorm** | - | - | Structured brainstorming |

## Architecture

### Master Skill Pattern

Claude Code has a ~15,000 character budget for skill descriptions. This marketplace uses **progressive disclosure** to maximize capabilities:

```
plugins/{name}/skills/
└── {master-skill}/
    ├── SKILL.md           # Discoverable master skill
    └── subskills/         # Loaded on-demand via Read tool
        ├── sub1.md
        ├── sub2.md
        └── ...
```

- Each plugin exposes ONE master SKILL.md
- Master skill indexes all sub-skills in its description
- Sub-skills are loaded when needed via the Read tool
- Scales to 100+ skills per plugin without truncation

### Directory Structure

```
.
├── .claude-plugin/
│   └── marketplace.json     # Plugin registry
├── CLAUDE.md                # Project instructions
├── plugins/
│   ├── {plugin}/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json  # Plugin manifest
│   │   ├── skills/          # Master skill + subskills
│   │   ├── commands/        # Slash commands
│   │   └── hooks/           # Event hooks
└── resources/               # Reference materials
```

## Development

### Modify a Plugin

1. Edit source files in `plugins/{name}/`
2. Clear cache: `rm -rf ~/.claude/plugins/cache/linuxiscool-claude-plugins/{name}/`
3. Restart Claude Code

### Add a New Plugin

1. Create `plugins/{name}/.claude-plugin/plugin.json`
2. Add skills using master skill pattern
3. Register in `.claude-plugin/marketplace.json`
4. Clear cache and restart

### Create a Skill

See `CLAUDE.md` for the master skill template and guidelines.

Use the `awareness` skill with sub-skill `plugin-developer` for detailed development workflow.

## Usage Examples

```
# Learn about AI agent frameworks
Skill: agents

# Create a journal entry
Skill: journal

# Explore knowledge graph options
Skill: knowledge-graphs

# Learn Claude Code development
Skill: awareness
```

## License

MIT
