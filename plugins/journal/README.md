# Journal Plugin

An Obsidian-style linked journal for Claude Code with zettelkasten atomic notes.

## Features

- **Temporal hierarchy**: Yearly, monthly, daily, and atomic timestamped entries
- **Wikilinks**: `[[note-title]]` linking between entries
- **YAML frontmatter**: Rich metadata for each entry type
- **Multiple journaling styles**: Stream of consciousness, bullet journal, structured reflection
- **Planning & reflection**: Dedicated skills for forward-looking and retrospective thinking
- **Aggregation**: Summarize patterns across time periods

## Directory Structure

```
.claude/journal/
├── index.md                      # Master index
├── 2025/
│   ├── 2025.md                   # Yearly note
│   ├── 12/
│   │   ├── 2025-12.md            # Monthly note
│   │   ├── 11/
│   │   │   ├── 2025-12-11.md     # Daily note
│   │   │   └── 143022-insight.md # Atomic note
```

## Entry Types

| Type | Format | Purpose |
|------|--------|---------|
| Yearly | `YYYY.md` | Vision, themes, annual retrospective |
| Monthly | `YYYY-MM.md` | Monthly goals, progress tracking |
| Daily | `YYYY-MM-DD.md` | Daily intentions, reflections |
| Atomic | `HHMMSS-title.md` | Zettelkasten atomic notes |

## Skills

- **journal-writer**: Create journal entries
- **journal-planner**: Planning-focused entries (goals, roadmaps)
- **journal-reflector**: Reflection-focused entries (retrospectives, lessons)
- **journal-linker**: Manage wikilinks and backlinks
- **journal-aggregator**: Summarize over time periods
- **journal-browser**: Navigate and search the journal

## Usage

```
/journal              # Start a journaling session
/journal daily        # Create/open today's daily note
/journal plan         # Planning session
/journal reflect      # Reflection session
```

## Obsidian Compatibility

Entries use standard Obsidian conventions:
- `[[wikilinks]]` for internal links
- `#tags` for categorization
- YAML frontmatter for metadata
- Backlinks tracked in frontmatter

Open `.claude/journal/` in Obsidian for a visual graph view of your thoughts.
