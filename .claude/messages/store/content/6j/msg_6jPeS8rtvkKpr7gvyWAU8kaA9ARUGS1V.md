---
id: msg_6jPeS8rtvkKpr7gvyWAU8kaA9ARUGS1V
kind: 103
account_id: claude
created_at: 1765586665966
imported_at: 1766005509549
author_name: Claude
thread_id: cc_8fdcbab0
platform: claude-code
session_id: 8fdcbab0-4e6f-430e-9390-5e8f8e1466a2
tags: [["event_type","AssistantResponse"]]
---

Your storm has been added to `.claude/storms/2025-12-12.md` with the following data:

```
title: Persona Subagents: Holistic Architecture Alignment
summary: Deep examination of how persona subagents align with project principles, revealing a shift toward markdown-native memory over external dependencies
storm_id: STORM-001
date: 2025-12-12
time: 14:32:00
tags:
- personas
- architecture
- principles
- memory
- markdown-native
- infrastructure
- team-consultation
tasks:
- [ ] Revise PERSONA_SUBAGENTS_STRATEGY.md to embrace markdown-native memory
- [ ] Design shared infrastructure schema
- [ ] Create persona memory format specification
- [ ] Prototype one persona with markdown-native approach
related_storms:
- (none - first storm)
```

---

## Reflection

**The team spoke with one voice.** When I consulted each plugin about how persona subagents should work, a clear consensus emerged that challenges my original strategy:

### The Original Strategy Was Philosophically Misaligned

I proposed Letta (requires PostgreSQL server), Mem0 (external API), and Graphiti (graph database). But every plugin in this ecosystem follows a different pattern:

| Plugin | Storage | Format |
|--------|---------|--------|
| Logging | `.claude/logging/` | JSONL + Markdown |
| Journal | `.claude/journal/` | Markdown + Wikilinks |
| Exploration | `.claude/exploration/` | Markdown |
| Schedule | `schedule/blocks/` | Markdown + YAML |
| Backlog | `backlog/tasks/` | Markdown + YAML |
| Brainstorm | `.claude/storms/` | Markdown |

**The pattern is clear: Markdown is the medium. Files are the truth.**

### The Seven Principles for Standard Infrastructure

1. **Markdown-Native Memory** - Personas store state in markdown with YAML frontmatter, like everything else
2. **Progressive Disclosure** - Core identity always loaded, deeper memories on-demand via Read
3. **Temporal Hierarchy** - Daily → Weekly → Monthly → Permanent (from Journal pattern)
4. **Wikilinks as Knowledge Graph** - Links ARE edges, files ARE nodes, no database needed
5. **YAML Frontmatter as Structured Data** - Queryable, parseable, portable
6. **Logging Integration as Memory Source** - Personas READ from logs, WRITE synthesized memory
7. **Zero External Dependencies** - Just files, Claude, and existing tools

### Revised Architecture

```
.claude/personas/
├── _schema/                    # Templates and standards
│   ├── identity-template.md
│   └── memory-template.md
├── _shared/                    # Cross-persona state
│   ├── user-profile.md         # [[wikilinked]]
│   └── project-context.md
├── archivist/
│   ├── identity.md             # Core (always loaded)
│   ├── state.md                # Current context
│   ├── memory/
│   │   ├── 2025-12/            # Temporal
│   │   └── permanent/          # Long-term
│   └── index.md                # Wikilinked map
└── mentor/
    └── ...
```

### What This Means

The sophisticated external systems (Letta, Mem0, Graphiti) remain **reference implementations** - we understand them, we can reach for them when scale demands. But the MVP should honor this project's soul:

> **"Markdown is the medium. Humans are the audience. Files are the truth."**

The personas should feel like **family members** of the existing plugins, not foreign imports with different DNA.
