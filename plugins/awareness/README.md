# Awareness Plugin

A self-awareness and learning plugin for Claude Code that enables systematic documentation reading, guide utilization, and technique mastery.

## Philosophy

> *Seek first to understand before seeking to be understood.*

This plugin embodies:
- **Self-reflection** - Examine decisions and patterns
- **Anti-fragility** - Grow stronger from challenges
- **Curiosity** - Active exploration, question assumptions
- **Self-improvement** - Compound learnings over time

## Skills

### 1. docs-reader

Systematically read and digest Claude Code documentation.

**When it's invoked**: When learning about Claude Code features, understanding system capabilities, or building foundational knowledge.

**Learning progression**: Fundamentals → Configuration → Extension → Advanced → Mastery

### 2. guide-utilizer

Effectively use the claude-code-guide subagent for authoritative information.

**When it's invoked**: When you need accurate information about Claude Code features, hooks, MCP servers, settings, IDE integrations, or the Agent SDK.

**Key principle**: Be specific, include context, ask for details.

### 3. techniques

Practice and master Claude Code techniques through incremental experimentation.

**When it's invoked**: When developing new capabilities, testing ideas, improving workflow, or compounding skill mastery.

**Core method**: Observe → Hypothesize → Test (small) → Learn → Compound

## Core Principles

1. **Start small** - Begin with fundamentals, smallest experiments
2. **Digest as you go** - Understanding > speed
3. **Compound learning** - Each concept builds on previous
4. **Maximize coherence** - Seek connections between topics
5. **Test incrementally** - Never build too far ahead of verification

## Installation

```bash
# Navigate to your Claude Code workspace
cd /path/to/your/project

# Install the awareness plugin
/plugin install awareness@linuxiscool-claude-plugins
```

Or add to marketplace.json:

```json
{
  "plugins": [
    {"name": "awareness", "source": "./plugins/awareness/"}
  ]
}
```

## Usage

The skills are model-invoked, meaning Claude will automatically use them when the context matches. You can also explicitly request them:

```markdown
# Trigger docs-reader
Help me learn about Claude Code hooks systematically

# Trigger guide-utilizer
I need authoritative information about MCP server configuration

# Trigger techniques
Let's practice the Edit tool technique
```

## Directory Structure

```
awareness/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── skills/
│   ├── docs-reader/
│   │   └── SKILL.md         # Documentation reading skill
│   ├── guide-utilizer/
│   │   └── SKILL.md         # Guide utilization skill
│   └── techniques/
│       └── SKILL.md         # Technique mastery skill
├── commands/                 # (Future: slash commands)
└── README.md
```

## Roadmap

- [ ] Add `/reflect` command for session reflection
- [ ] Add hooks for automatic learning capture
- [ ] Add memory persistence for learnings/patterns
- [ ] Add `/awareness-status` dashboard command

## Version History

- **0.1.0** - Initial release with three core skills

## License

MIT
