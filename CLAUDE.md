NEVER truncate data. Truncating data in code causes silent data loss. This is a bad practice. If there is a strong case for truncation, check in with the user before doing so.
NEVER add hard-coded data to documents. Data will typically change rapidly making those documents outdated very fast.
ABSOLUTELY NO INSIPID LLM-ESSE. DO NOT EVER USE THE PHRASE: "NOT JUST X BUT Y" OR "WE ARE NOT JUST X WE ARE Y". NEVER USE THAT PATTERN OR SIMILAR PATTERNS IN ENGLISH!
Produce clean, reliable, maintainable code that maximizes quality and generality while minimizing lines of code, minimizing rigidity, and minimizing fragility.
NEVER PRODUCE MOCK DATA. NEVER PRODUCE FAKE DATA. ONLY USE DATA FROM RELIABLE SOURCES. CHECK ALL SOURCES ALWAYS.

# Coordination

**Git is the inter-agent coordination layer.** Agents coordinate through observable file changes, not complex protocols.

- **Write** to your designated namespace
- **Read** from anywhere
- **Commit** with structured messages: `[scope] action: description`
- **Observe** git log for ecosystem activity

See `.claude/conventions/coordination.md` for full patterns.

---

# Ecosystem Orientation

**New to this repository?** Read `.claude/README.md` for complete context:
- Vision and philosophy
- Agent fleet (7 custom agents)
- Process registry (9 mapped processes)
- Journal system (atomic-first)
- Active vs dormant components
- Continuation points

**Quick links**:
- Current state: `.claude/journal/` (latest daily entry)
- Agent fleet: `.claude/registry/agents.md`
- Processes: `.claude/registry/processes.md`
- Strategic context: `.claude/briefings/`

# Plugin Architecture

## Master Skill Pattern

Claude Code has a ~15,000 character budget for skill descriptions. To prevent truncation ("Showing X of Y skills"), use **progressive disclosure**:

- **One master skill per plugin**: Each plugin exposes ONE discoverable SKILL.md
- **Sub-skills via Read tool**: Master skill contains an index; sub-skills are loaded on-demand from `subskills/` directory
- **Description lists sub-skills**: Master skill description enumerates available sub-skills for discoverability

### Directory Structure
```
plugins/{plugin-name}/skills/
└── {skill-name}/
    ├── SKILL.md           # Master skill (discoverable)
    └── subskills/         # Sub-skills (loaded via Read)
        ├── sub1.md
        ├── sub2.md
        └── ...
```

### Master SKILL.md Template
```markdown
---
name: {plugin-name}
description: Master skill for [purpose]. Sub-skills (N): name1, name2, name3. Invoke for [use cases].
allowed-tools: Read, Skill, Task, Glob, Grep
---

# {Plugin Name} - Master Skill

## Sub-Skills Index

| Sub-Skill | Use When | File |
|-----------|----------|------|
| **name1** | [trigger condition] | `subskills/name1.md` |
```

## Plugin Development Workflow

```
Edit Source → Validate → Clear Cache → Restart Claude Code
```

### Cache Location
```
~/.claude/plugins/cache/linuxiscool-claude-plugins/{plugin-name}/
```

### Clear Cache
```bash
rm -rf ~/.claude/plugins/cache/linuxiscool-claude-plugins/{plugin-name}/
```

Use the `awareness:plugin-developer` sub-skill for detailed development guidance.

## Plugin Agents Pattern

Plugins can define **subagents** that become available via the Task tool with namespaced identifiers.

### Directory Structure
```
plugins/{plugin-name}/
├── .claude-plugin/
│   └── plugin.json        # Include "agents": ["./agents/"]
├── skills/                # Skills (via Skill tool)
├── commands/              # Slash commands
└── agents/                # Subagents (via Task tool)
    └── {agent-name}.md
```

### Agent Definition Schema
```markdown
---
name: {agent-name}
description: {what the agent does - appears in Task tool}
tools: {comma-separated tool list}
model: {sonnet|opus|haiku}
---

# Agent identity and prompt content...
```

### Namespacing Convention

| Source | Subagent Type |
|--------|---------------|
| `.claude/agents/archivist.md` | `archivist` |
| `plugins/awareness/agents/mentor.md` | `awareness:mentor` |
| `plugins/journal/agents/scribe.md` | `journal:scribe` |

### plugin.json Extension
```json
{
  "name": "awareness",
  "skills": ["./skills/"],
  "commands": ["./commands/"],
  "agents": ["./agents/mentor.md"]
}
```

**Note**: Unlike `skills` and `commands`, the `agents` field requires specific `.md` file paths, not directories.

### Current Status

**Both project-level and plugin-level agents are natively supported by Claude Code.**

- Project agents: `.claude/agents/*.md` → subagent_type: `{name}`
- Plugin agents: Listed in `plugin.json` `agents` field → subagent_type: `{plugin}:{name}`

The aggregation script (`scripts/aggregate-plugin-agents.sh`) is optional - useful for copying plugin agents to project level if needed.
