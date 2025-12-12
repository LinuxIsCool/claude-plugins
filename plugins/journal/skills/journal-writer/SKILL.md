---
name: journal-writer
description: Create journal entries in .claude/journal/. Use when the user wants to journal, write notes, capture thoughts, create daily/monthly/yearly entries, or record atomic ideas in zettelkasten style.
allowed-tools: Read, Write, Edit, Glob, Bash
---

# Journal Writer

Create and manage journal entries in `.claude/journal/` using Obsidian-compatible markdown with zettelkasten atomic notes.

## When to Use

- User wants to journal or write notes
- Capturing a thought, idea, or insight
- Creating daily, monthly, or yearly entries
- Recording learnings or observations
- Starting a new note on a topic

## Directory Structure

```
.claude/journal/
├── index.md                      # Master index (create if missing)
├── YYYY/
│   ├── YYYY.md                   # Yearly note
│   ├── MM/
│   │   ├── YYYY-MM.md            # Monthly note
│   │   ├── DD/
│   │   │   ├── YYYY-MM-DD.md     # Daily note
│   │   │   └── HHMMSS-title.md   # Atomic timestamped note
```

## Entry Templates

### Daily Note Template

```markdown
---
date: YYYY-MM-DD
type: daily
mood: null
energy: null
weather: null
tags: [daily]
links: []
created: YYYY-MM-DDTHH:MM:SS
---

# YYYY-MM-DD Day-of-Week

## Morning Intentions
-

## Log
-

## Evening Reflection
-

## Links
- [[YYYY-MM]] | [[YYYY]]

---
*Atomic notes from today:*
```

### Monthly Note Template

```markdown
---
month: YYYY-MM
type: monthly
themes: []
goals: []
highlights: []
challenges: []
tags: [monthly]
links: []
created: YYYY-MM-DDTHH:MM:SS
---

# YYYY Month-Name

## Themes
-

## Goals
- [ ]

## Progress


## Highlights
-

## Challenges
-

## Lessons Learned
-

## Links
- [[YYYY]]

---
*Daily notes:*
```

### Yearly Note Template

```markdown
---
year: YYYY
type: yearly
vision: ""
themes: []
milestones: []
word-of-year: ""
tags: [yearly]
links: []
created: YYYY-MM-DDTHH:MM:SS
---

# YYYY

## Vision


## Word of the Year


## Themes
-

## Quarterly Goals

### Q1
- [ ]

### Q2
- [ ]

### Q3
- [ ]

### Q4
- [ ]

## Milestones
-

## Annual Review


---
*Monthly notes:*
```

### Atomic Note Template

```markdown
---
id: YYYY-MM-DD-HHMMSS
title: "Note Title"
type: atomic
tags: []
links: []
source: null
created: YYYY-MM-DDTHH:MM:SS
---

# Note Title

[Content goes here - one idea per note]

## Related
-

## Source
-

---
*Links: [[YYYY-MM-DD]]*
```

### Index Template

```markdown
---
title: Journal Index
type: index
created: YYYY-MM-DDTHH:MM:SS
updated: YYYY-MM-DDTHH:MM:SS
---

# Journal Index

## Recent Entries
-

## Years
-

## Tags
-

## Graph
This journal uses [[wikilinks]] for connections. Open in Obsidian for graph view.
```

## Journaling Styles

### 1. Stream of Consciousness
Free-form writing without structure. Just write what comes to mind.

### 2. Bullet Journal (Rapid Logging)
```markdown
## Log
- Task incomplete
- x Task complete
- > Task migrated
- < Task scheduled
- o Event
- - Note
- ! Priority
- ? Question to explore
```

### 3. Gratitude
```markdown
## Gratitude
1.
2.
3.
```

### 4. Learning Log
```markdown
## What I Learned
-

## Questions
-

## Insights
-
```

### 5. Decision Journal
```markdown
## Decision: [Title]

**Context**:

**Options Considered**:
1.
2.

**Decision**:

**Reasoning**:

**Expected Outcome**:

**Review Date**:
```

### 6. Morning Pages
Three pages of stream-of-consciousness writing first thing in the morning.

## Creating Entries

### Create Daily Note
1. Calculate today's date
2. Ensure directory exists: `.claude/journal/YYYY/MM/DD/`
3. Check if daily note exists: `YYYY-MM-DD.md`
4. If not, create from template
5. Return path to note

### Create Atomic Note
1. Generate timestamp: `HHMMSS`
2. Slugify title: `my-idea`
3. Create in today's directory: `HHMMSS-my-idea.md`
4. Add backlink to daily note
5. Return path to note

### Create Monthly/Yearly
1. Check if exists
2. Create from template if not
3. Link to parent (yearly links to nothing, monthly links to yearly)

## Wikilink Conventions

- Daily to monthly: `[[YYYY-MM]]`
- Daily to yearly: `[[YYYY]]`
- Atomic to daily: `[[YYYY-MM-DD]]`
- Cross-reference: `[[HHMMSS-title]]` or `[[title]]`

## Tags

Common tags to suggest:
- `#daily`, `#monthly`, `#yearly`, `#atomic`
- `#idea`, `#insight`, `#question`, `#decision`
- `#learning`, `#reflection`, `#planning`
- `#project/name`, `#area/name`

## Workflow

1. **Check for existing entry** before creating
2. **Create parent directories** as needed
3. **Use templates** for consistency
4. **Add wikilinks** to related entries
5. **Update index.md** periodically (or on aggregation)

## Example: Creating Today's Daily Note

```bash
# Get today's date components
YEAR=$(date +%Y)
MONTH=$(date +%m)
DAY=$(date +%d)
DATE=$(date +%Y-%m-%d)
DOW=$(date +%A)

# Ensure directory exists
mkdir -p .claude/journal/$YEAR/$MONTH/$DAY

# Create daily note if missing
if [ ! -f ".claude/journal/$YEAR/$MONTH/$DAY/$DATE.md" ]; then
  # Write template...
fi
```

## Notes

- Always use ISO 8601 dates (YYYY-MM-DD)
- Timestamps in 24-hour format (HHMMSS)
- Slugify titles: lowercase, hyphens, no special chars
- One idea per atomic note (zettelkasten principle)
- Link liberally - connections create value
