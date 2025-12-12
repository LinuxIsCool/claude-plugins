# Awareness Plugin Synthesis

## Deep Contemplation: What I've Learned

### Repository Understanding

This repository is a **Claude Code Plugin Marketplace** - a modular ecosystem for extending Claude Code's capabilities. The design philosophy is clear:

1. **Never truncate data** - Silent data loss is unacceptable
2. **No hard-coded data** - Data changes rapidly, static docs become stale
3. **Clean, reliable, maintainable code** - Quality over quantity

Three plugins exist, each teaching different patterns:

| Plugin | Pattern | Key Learning |
|--------|---------|--------------|
| **brainstorm** | Commands | Markdown-based structured output with YAML frontmatter |
| **logging** | Hooks | Event-driven architecture capturing all 10+ hook events |
| **Schedule.md** | MCP Server | TypeScript full-stack with tools, web UI, and skills |

### Claude Code Architecture

The system is layered:

```
User Input → Claude Code CLI → Model (Opus/Sonnet/Haiku) → Tools → Output
                    ↑
              Hooks intercept at key points
              Skills auto-discovered and invoked
              Memory (CLAUDE.md) persists across sessions
```

**14 Core Tools**: Read, Write, Edit, Bash, Glob, Grep, WebFetch, WebSearch, Task, Skill, SlashCommand, NotebookEdit, AskUserQuestion, TodoWrite

**11 Hook Events**: SessionStart, PreToolUse, PostToolUse, PermissionRequest, UserPromptSubmit, Stop, SubagentStop, Notification, PreCompact, SessionEnd

**Sub-agent Types**: Explore (fast search), General-purpose (multi-step), Plan (architecture), Custom (user-defined)

### Key Insights from Documentation

1. **Skills are model-invoked** - Claude autonomously uses them based on description matching
2. **Extended thinking** - Toggle with Tab, deepen with "think hard/deeply/extensively"
3. **Hooks enable event-driven automation** - Can block, modify, or log any operation
4. **CLAUDE.md hierarchy** - Enterprise → Project → Rules → User → Local
5. **Headless mode** - Full programmatic access via `-p` flag and JSON output

### Claude Agent SDK Patterns

For building aware, learning systems:

1. **ClaudeSDKClient** for persistent multi-turn conversations
2. **Memory persistence** via JSON files in `.claude/` directory
3. **Hook-based monitoring** to capture learning events automatically
4. **Structured outputs** for consistent learning extraction
5. **Subagent delegation** for specialized analysis

---

## Awareness Plugin Design

### Core Philosophy

The awareness plugin embodies:

- **Self-reflection** - Continuously examine decisions and patterns
- **Anti-fragility** - Learn from stress and failure, grow stronger
- **Curiosity** - Active exploration, question assumptions
- **Self-improvement** - Compound learnings over time

*"Seek first to understand before seeking to be understood."*

### Architecture

```
.claude/awareness/
├── memory/
│   ├── sessions.json       # Session history and insights
│   ├── patterns.json       # Discovered patterns
│   ├── learnings.json      # Explicit learnings
│   └── techniques.json     # Mastered techniques
├── skills/
│   ├── docs-reader/        # Skill: Read and digest docs
│   ├── guide-utilizer/     # Skill: Use claude-code-guide effectively
│   └── techniques/         # Skill: Claude Code technique mastery
└── reflections/
    └── YYYY-MM-DD.md       # Daily reflection logs
```

### Skills to Implement

#### Skill 1: docs-reader

**Purpose**: Systematically read and digest Claude Code documentation

```yaml
---
name: docs-reader
description: Read and digest Claude Code documentation. Use when learning about Claude Code features, capabilities, or best practices.
allowed-tools: Task, Read, WebFetch, WebSearch
---
```

**Behavior**:
- Invoke claude-code-guide subagent for specific topics
- Extract key concepts and store in memory
- Build understanding progressively
- Cross-reference multiple sources

#### Skill 2: guide-utilizer

**Purpose**: Maximize effectiveness of claude-code-guide subagent

```yaml
---
name: guide-utilizer
description: Effectively use the claude-code-guide subagent. Use when you need accurate information about Claude Code features, hooks, MCP servers, settings, or the Agent SDK.
allowed-tools: Task
---
```

**Behavior**:
- Formulate precise queries for the guide
- Resume previous guide sessions for continuity
- Chain queries for complex topics
- Validate understanding through application

#### Skill 3: techniques-master

**Purpose**: Practice and master Claude Code techniques

```yaml
---
name: techniques-master
description: Practice and master Claude Code techniques. Use when developing new capabilities, testing techniques, or improving workflow mastery.
allowed-tools: Read, Write, Edit, Bash, Task
---
```

**Behavior**:
- Start small, test incrementally
- Compound learnings (each technique builds on previous)
- Record successes and failures
- Iterate towards mastery

### Hooks for Awareness

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "python .claude/awareness/hooks/session_start.py"
      }]
    }],
    "PostToolUse": [{
      "hooks": [{
        "type": "command",
        "command": "python .claude/awareness/hooks/log_tool_use.py"
      }]
    }],
    "SessionEnd": [{
      "hooks": [{
        "type": "command",
        "command": "python .claude/awareness/hooks/reflect_and_save.py"
      }]
    }]
  }
}
```

### Memory System

Persistent memory structure for learning:

```json
{
  "learnings": [
    {
      "id": "learning-001",
      "date": "2025-12-11",
      "topic": "Claude Code hooks",
      "insight": "Hooks can be prompt-based for intelligent decisions",
      "confidence": 0.9,
      "source": "docs/hooks.md",
      "applied": true
    }
  ],
  "patterns": [
    {
      "id": "pattern-001",
      "name": "Plugin structure",
      "description": ".claude-plugin/plugin.json + commands/ + hooks/",
      "occurrences": 3,
      "reliability": "high"
    }
  ],
  "techniques": [
    {
      "id": "technique-001",
      "name": "Extended thinking",
      "trigger": "Tab key or 'think deeply'",
      "mastery_level": 0.7,
      "last_practiced": "2025-12-11"
    }
  ]
}
```

---

## Next Steps: Gradual Implementation

Following the principle "start small, test incrementally, compound learnings":

### Phase 1: Foundation (Now)
1. Create plugin directory structure
2. Implement docs-reader skill
3. Test with simple documentation reads

### Phase 2: Integration
4. Implement guide-utilizer skill
5. Add memory persistence
6. Create session hooks

### Phase 3: Mastery
7. Implement techniques-master skill
8. Add reflection commands
9. Create awareness dashboard

### Phase 4: Evolution
10. Self-improvement capabilities
11. Pattern recognition across sessions
12. Autonomous learning cycles

---

## Reflections

### What I Understand Deeply

1. **Plugin patterns** - Commands (markdown), Hooks (event-driven), MCP (tools+resources)
2. **Memory hierarchy** - Project → User → Local, with rules for modularity
3. **Sub-agents** - Specialized personalities with isolated context
4. **Skills vs Commands** - Model-invoked vs user-invoked

### What I Need to Practice

1. Creating MCP servers in TypeScript
2. Building multi-file skills with helper scripts
3. Using hooks for sophisticated automation
4. Structuring memory for efficient retrieval

### Principles for Building

1. **Coherence over completeness** - Better to deeply understand a few things than superficially many
2. **Test as you go** - Never build too far ahead of verification
3. **Compound learning** - Each step should build on the previous
4. **Minimalism** - Least code that achieves the goal

---

*Generated during awareness plugin development session, 2025-12-11*
