---
name: journal-writer
description: Create atomic journal entries in .claude/journal/. Atomic entries are the PRIMARY unit—daily/monthly/yearly notes are SYNTHESIZED from atomics. Each atomic entry has mandatory author and relational fields for DNA-spiral graph rendering.
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Journal Writer

Create atomic journal entries in `.claude/journal/` using Obsidian-compatible markdown. Atomic entries are the **primary unit**—higher-level summaries (daily, monthly, yearly) are synthesized from atomics.

## Core Principle: Atomic First

```
Atomic entries (primary)
    ↓ synthesize into
Daily summaries
    ↓ synthesize into
Monthly summaries
    ↓ synthesize into
Yearly summaries
```

**You don't write daily entries—you write atomic entries that get synthesized into daily summaries.**

## Directory Structure

```
.claude/journal/
├── index.md
├── YYYY/
│   ├── YYYY.md                    # Synthesized from monthlies
│   └── MM/
│       ├── YYYY-MM.md             # Synthesized from dailies
│       └── DD/
│           ├── YYYY-MM-DD.md      # Synthesized from atomics
│           ├── HH-MM-title.md     # Atomic entry (PRIMARY)
│           ├── HH-MM-title.md     # Atomic entry
│           └── ...
```

## Atomic Entry Template (PRIMARY)

**Filename**: `HH-MM-slugified-title.md` (e.g., `14-30-subagent-exploration.md`)

```markdown
---
id: YYYY-MM-DD-HHMM
title: "Entry Title"
type: atomic
created: YYYY-MM-DDTHH:MM:SS
author: agent-name-or-user        # MANDATORY: who wrote this
description: "Brief description"   # MANDATORY: one-line summary
tags: [tag1, tag2]
parent_daily: [[YYYY-MM-DD]]       # MANDATORY: links UP to daily
related: []                        # Other atomic entries this connects to
---

# Entry Title

[Content - one focused idea/moment/discovery per entry]

## Context

[What prompted this entry]

## Insights

[Key takeaways]

---
*Parent: [[YYYY-MM-DD]] → [[YYYY-MM]] → [[YYYY]]*
```

### Mandatory Fields for Atomic Entries

| Field | Purpose | Example |
|-------|---------|---------|
| `created` | Timestamp of creation | `2025-12-13T14:30:00` |
| `author` | Who/what created this entry | `claude-opus-4`, `user`, `backend-architect` |
| `title` | Entry title | `"Subagent Exploration"` |
| `description` | One-line summary | `"Discovered CLI supports custom system prompts"` |
| `tags` | Categorization | `[subagents, cli, discovery]` |
| `parent_daily` | Link UP to daily note | `[[2025-12-13]]` |
| `related` | Links to related atomics | `[[14-45-agent-architecture]]` |

## Daily Note Template (SYNTHESIZED)

Daily notes are synthesized from atomic entries, not written directly.

```markdown
---
date: YYYY-MM-DD
type: daily
created: YYYY-MM-DDTHH:MM:SS
synthesized: true
parent_monthly: [[YYYY-MM]]
children:
  - [[HH-MM-title]]
  - [[HH-MM-title]]
tags: [daily]
---

# YYYY-MM-DD Day-of-Week

## Summary

[Synthesized from atomic entries below]

## Atomic Entries

- [[HH-MM-first-entry]] — description
- [[HH-MM-second-entry]] — description
- ...

## Themes

[Patterns across today's atomics]

---
*Parent: [[YYYY-MM]] → [[YYYY]]*
*Children: [list of atomic wikilinks]*
```

## Monthly Note Template (SYNTHESIZED)

```markdown
---
month: YYYY-MM
type: monthly
created: YYYY-MM-DDTHH:MM:SS
synthesized: true
parent_yearly: [[YYYY]]
children:
  - [[YYYY-MM-DD]]
  - [[YYYY-MM-DD]]
tags: [monthly]
themes: []
---

# YYYY Month-Name

## Summary

[Synthesized from daily notes]

## Daily Notes

- [[YYYY-MM-DD]] — summary
- [[YYYY-MM-DD]] — summary

## Themes

[Patterns across the month]

## Key Atomics

[Standout atomic entries worth highlighting]

---
*Parent: [[YYYY]]*
*Children: [list of daily wikilinks]*
```

## Yearly Note Template (SYNTHESIZED)

```markdown
---
year: YYYY
type: yearly
created: YYYY-MM-DDTHH:MM:SS
synthesized: true
children:
  - [[YYYY-MM]]
  - [[YYYY-MM]]
tags: [yearly]
themes: []
---

# YYYY

## Summary

[Synthesized from monthly notes]

## Monthly Notes

- [[YYYY-01]] — summary
- [[YYYY-02]] — summary
- ...

## Themes

[Patterns across the year]

---
*Children: [list of monthly wikilinks]*
```

## The DNA Spiral Effect

When rendered in Obsidian's force-directed graph:

```
                    ╭──── [[2025]] ────╮
                   ╱                    ╲
           [[2025-11]]              [[2025-12]]
              │                          │
    ╭─────────┼─────────╮      ╭─────────┼─────────╮
    │         │         │      │         │         │
[[12]]    [[13]]    [[14]]  [[12]]    [[13]]    [[14]]
   │╲        │╲        │      │         │╲
   │ ╲       │ ╲       │      │         │ ╲
  ⚫ ⚫     ⚫ ⚫     ⚫      ⚫        ⚫ ⚫ ⚫
  atomics   atomics  atomic  atomic    atomics

The bidirectional links (child→parent, parent→child) create
the spiral/helix structure in force-directed layout.
```

## Creating Entries

### Create Atomic Entry (Primary Action)

```python
# 1. Get current time
timestamp = "14-30"  # HH-MM format
title_slug = "subagent-exploration"
filename = f"{timestamp}-{title_slug}.md"

# 2. Ensure directory exists
path = f".claude/journal/2025/12/13/{filename}"

# 3. Create with mandatory fields
# - created (timestamp)
# - author (who is writing)
# - description (one line)
# - parent_daily (link up)
# - tags
```

### Synthesize Daily from Atomics

```python
# 1. List all atomics in day directory
atomics = glob(".claude/journal/2025/12/13/[0-9][0-9]-[0-9][0-9]-*.md")

# 2. Read each atomic's frontmatter
# 3. Generate summary from descriptions
# 4. Create daily note with children list
# 5. Link each atomic's parent_daily to this daily
```

### Synthesize Monthly from Dailies

```python
# 1. List all daily notes in month
dailies = glob(".claude/journal/2025/12/*/YYYY-MM-DD.md")

# 2. Read each daily's summary
# 3. Generate monthly summary
# 4. Create monthly note with children list
```

## Relational Fields

### Upward Links (Mandatory)

| Entry Type | Links To | Field |
|------------|----------|-------|
| Atomic | Daily | `parent_daily: [[YYYY-MM-DD]]` |
| Daily | Monthly | `parent_monthly: [[YYYY-MM]]` |
| Monthly | Yearly | `parent_yearly: [[YYYY]]` |

### Downward Links (In Synthesis)

| Entry Type | Lists | Field |
|------------|-------|-------|
| Yearly | Monthlies | `children: [[[YYYY-MM]], ...]` |
| Monthly | Dailies | `children: [[[YYYY-MM-DD]], ...]` |
| Daily | Atomics | `children: [[[HH-MM-title]], ...]` |

### Horizontal Links (Optional)

Atomics can link to related atomics:
```yaml
related:
  - [[14-45-agent-architecture]]
  - [[15-20-process-mapping]]
```

## Workflow

### Writing (Create Atomics)

1. **Capture thought** → Create atomic entry
2. **Mandatory fields**: author, created, description, parent_daily, tags
3. **One idea per entry** (zettelkasten principle)
4. **Link related atomics** in `related` field

### Synthesis (Aggregate Up)

1. **End of day**: Synthesize atomics → daily
2. **End of month**: Synthesize dailies → monthly
3. **End of year**: Synthesize monthlies → yearly
4. **Update children lists** in parent notes

## Author Field Values

| Author | When to Use |
|--------|-------------|
| `user` | User wrote this directly |
| `claude-opus-4` | Opus model in Claude Code |
| `claude-sonnet` | Sonnet model |
| `backend-architect` | Agent persona reflection |
| `systems-thinker` | Agent persona reflection |
| `process-cartographer` | Process mapping agent |
| `{agent-name}` | Any custom agent |

## Tags

Common tags:
- `#atomic`, `#daily`, `#monthly`, `#yearly`
- `#discovery`, `#insight`, `#decision`, `#question`
- `#agent/{name}`, `#project/{name}`, `#theme/{name}`

## Notes

- **Atomic first**: Always create atomics; synthesize summaries later
- **HH-MM format**: Use hyphens for readability (`14-30`, not `1430`)
- **Slugify titles**: lowercase, hyphens, no special chars
- **One idea per atomic**: Keep entries focused
- **Link liberally**: Connections create the DNA spiral
- **Author is mandatory**: Track provenance
