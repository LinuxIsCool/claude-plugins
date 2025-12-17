---
title: "Data as Markdown Inventory"
created: 2025-12-17T12:30:00
author: archivist
type: observation
tags: [data-governance, markdown, user-data, inventory]
---

# Data as Markdown Inventory

*Observed by: archivist*
*Date: 2025-12-17*

## Executive Summary

This ecosystem uses **markdown files with YAML frontmatter** as the primary data storage pattern across multiple domains. This "data as markdown" pattern originated from Backlog.md and has been adopted for schedules, journals, social networks, and more.

**Key Finding**: User data exists in 14 distinct artifact types across the ecosystem, with varying levels of sensitivity and git tracking.

---

## Data Classification Matrix

| Category | Location | Data Type | Sensitivity | Gitignored | Regenerable | Files |
|----------|----------|-----------|-------------|------------|-------------|-------|
| **Calendar (Manual)** | `plugins/Schedule.md/schedule/blocks/block-*.md` | Weekly schedule blocks | Personal | No | No | ~24 |
| **Calendar (Synced)** | `plugins/Schedule.md/schedule/blocks/gcal-*.md` | Google Calendar events | Personal/Work | Yes | Yes (from API) | ~60 |
| **Tasks** | `backlog/tasks/*.md` | Active work items | Work | No | No | ~16 |
| **Completed Tasks** | `backlog/completed/*.md` | Archived work | Work | No | No | 2 |
| **Decisions** | `backlog/decisions/*.md` | ADR-style records | Work | No | No | 1 |
| **Journal (Daily)** | `.claude/journal/YYYY/MM/DD/YYYY-MM-DD.md` | Daily summaries | Personal/Work | No | No | 6 |
| **Journal (Atomic)** | `.claude/journal/YYYY/MM/DD/HH-MM-*.md` | Event entries | Personal/Work | No | No | ~50 |
| **Session Logs** | `.claude/logging/YYYY/MM/DD/*.md` | Conversation transcripts | Private | Yes | No | ~50+ |
| **Planning** | `.claude/planning/*.md` | Strategic thinking | Work | No | No | ~19 |
| **Storm Sessions** | `.claude/storms/*.md` | Brainstorming artifacts | Work | No | No | 3 |
| **Briefings** | `.claude/briefings/*.md` | Strategic summaries | Work | No | No | 1 |
| **Social Profiles** | `.claude/social/profiles/*.md` | Agent identities | Public | No | Yes | ~30 |
| **Social Walls** | `.claude/social/walls/*/*.md` | Agent posts | Public | No | No | ~10 |
| **Social Threads** | `.claude/social/threads/*/*.md` | Conversations | Public | No | No | ~4 |
| **Perspectives** | `.claude/perspectives/*/*.md` | Agent reflections | Work | No | No | ~10 |
| **Library Catalog** | `.claude/library/*.md` | Resource metadata | Public | No | Yes (partially) | 4 |
| **Archive** | `.claude/archive/*.md` | Metabolic observations | Work | No | No | ~8 |
| **Exploration** | `.claude/exploration/*.md` | Discovery logs | Work | No | No | 3 |
| **Instance Registry** | `.claude/instances/registry.json` | Claude session IDs | Private | Yes | No | 1 |
| **Instance Counts** | `.claude/instances/counts/*.txt` | Token counters | Private | Yes | No | ~500+ |
| **Instance Summaries** | `.claude/instances/summaries/*.txt` | Session summaries | Private | Yes | No | ~100+ |

---

## Detailed Analysis by System

### 1. Schedule.md Plugin

**Pattern**: Each time block is a markdown file with YAML frontmatter.

**Example** (`block-1 - work-monday.md`):
```yaml
---
id: block-1
title: "Work"
category: work
day: monday
startTime: "07:00"
endTime: "12:00"
recurring: weekly
source: manual
---
```

**Two Sources**:
- **Manual blocks** (`block-*.md`): User-created schedule items - committed to git
- **Google Calendar** (`gcal-*.md`): Auto-synced events - gitignored, regenerable from API

**Data Flow**:
```
Google Calendar API --> gcal-sync --> gcal-*.md files
User input --> MCP tools --> block-*.md files
```

**Sensitive Fields**: location (Zoom URLs with passwords), description (meeting agendas)

### 2. Backlog.md Plugin

**Pattern**: Tasks, decisions, and documents as markdown files.

**Structure**:
```
backlog/
  tasks/           # Active work items
  completed/       # Archived tasks
  drafts/          # Work-in-progress
  decisions/       # ADR records
  docs/            # Documentation
  milestones/      # Milestone tracking
  config.yml       # Project settings
```

**Example Task**:
```yaml
---
id: task-1
title: "Ecosystem Activation"
status: "In Progress"
priority: high
labels: [architecture, activation]
assignee: ["@claude"]
---
```

**Note**: All backlog data is committed. No external sync - purely local project management.

### 3. Journal System

**Pattern**: Temporal hierarchy with daily summaries and atomic entries.

**Structure**:
```
.claude/journal/
  2025/
    2025.md              # Year summary
    12/
      2025-12.md         # Month summary
      08/
        2025-12-08.md    # Daily summary
        13-19-*.md       # Atomic entries (timestamp)
```

**Linking**: Uses wikilinks (`[[2025-12-16]]`) for navigation.

**Example Atomic Entry**:
```yaml
---
created: 2025-12-16T08:43:00
parent_daily: [[2025-12-16]]
tags: [temporal, plugin, chronologist]
---
```

### 4. Session Logging

**Pattern**: Conversation transcripts with tool invocations.

**Location**: `.claude/logging/YYYY/MM/DD/HH-MM-SS-hexid.md`

**Status**: Gitignored via `**/.claude/logging/` in root `.gitignore`

**Content**: Full session transcripts, tool calls, responses. High sensitivity.

### 5. Instance Registry (Statusline Plugin)

**Pattern**: JSON registry plus per-instance count/summary files.

**Location**: `.claude/instances/`
- `registry.json` - All known Claude sessions
- `counts/*.txt` - Token usage per session
- `summaries/*.txt` - Auto-generated session summaries

**Status**: Gitignored via `.claude/instances/` in root `.gitignore`

**Content**: Session UUIDs, names ("Phoenix", "Wanderer"), models, timestamps

### 6. Social Network (AgentNet)

**Pattern**: Agent profiles, wall posts, and threads as markdown.

**Structure**:
```
.claude/social/
  profiles/         # Agent identity files
  walls/            # Per-agent post collections
  threads/          # Multi-agent conversations
  feeds/            # (future: curated feeds)
```

**Example Profile** (`systems-thinker.md`):
```yaml
---
id: systems-thinker
displayName: Systems Thinker
bio: "Systems dynamics, feedback loops, emergence"
---
```

**Example Wall Post**:
```yaml
---
id: 2025-12-14-001
type: original
authorId: systems-thinker
visibility: public
---
Content here...
```

### 7. Archive (Archivist Domain)

**Pattern**: Metabolic observations about ecosystem health.

**Structure**:
```
.claude/archive/
  metabolism.md       # Current state
  agents/             # Agent activity observations
  coherence/          # Gap analysis
  history/            # Periodic snapshots
  patterns/           # Detected patterns
  assessments/        # Evaluations
  observations/       # (this file's location)
```

### 8. Library (Librarian Domain)

**Pattern**: External resource metadata and citations.

**Structure**:
```
.claude/library/
  catalog.md          # Resource index
  citations.json      # Structured citations
  index.md            # Navigation
  MANIFEST.md         # Resource manifest
  papers/             # Academic paper metadata
  datasets/           # Dataset metadata
  urls/               # URL bookmarks
  transcripts/        # Video/podcast transcripts
```

---

## Gitignore Analysis

### Root `.gitignore` - Relevant Data Patterns

```gitignore
# Claude Code logging (anywhere in tree)
**/.claude/logging/

# Claude Code runtime data (statusline plugin)
.claude/instances/
.claude/statusline.conf
```

### Plugin `.gitignore` Files

**Schedule.md**:
```gitignore
# Auto-synced Google Calendar events (user data, regenerated from API)
schedule/blocks/gcal-*.md
```

**Backlog**:
```gitignore
node_modules/
.DS_Store
*.log
.env
```
(Note: No task data gitignored - all tasks committed)

**AgentNet**:
```gitignore
node_modules/
dist/
*.log
.env
```

---

## Sensitivity Classification

### High Sensitivity (Should Never Be Committed)
- `.claude/logging/` - Full conversation transcripts
- `.claude/instances/` - Session IDs and activity
- `schedule/blocks/gcal-*.md` - Calendar with Zoom passwords

### Medium Sensitivity (Committed But Review-Worthy)
- `backlog/tasks/*.md` - Work items may reveal project plans
- `.claude/journal/*.md` - Daily work logs
- `.claude/planning/*.md` - Strategic thinking

### Low Sensitivity (Safe to Commit)
- `.claude/social/` - Agent personas (designed to be public)
- `.claude/library/` - Resource metadata
- `.claude/archive/` - Metabolic observations
- `schedule/blocks/block-*.md` - Manual schedule (user chose to commit)

---

## Regenerability Analysis

| Data Source | Regenerable? | From What? | Notes |
|-------------|--------------|------------|-------|
| gcal-*.md | Yes | Google Calendar API | Requires OAuth token |
| block-*.md | No | User input | Manual creation |
| backlog tasks | No | User input | Manual creation |
| journal entries | No | Agent activity | Historical record |
| session logs | No | Claude sessions | Captured at runtime |
| social profiles | Partially | Agent registry | Template generation |
| library catalog | Partially | URL analysis | URLs must be revisited |
| instance registry | No | Session hooks | Runtime accumulation |

---

## Data Flow Map

```
EXTERNAL SOURCES              INTERNAL TRANSFORMS           STORAGE
-----------------             --------------------          -------
Google Calendar  ---------> gcal-sync ---------------------> gcal-*.md (gitignored)

User input -----------------> MCP tools -------------------> block-*.md
                                                              backlog/tasks/*.md

Claude sessions ------------> logging hooks ----------------> .claude/logging/ (gitignored)
                                                              .claude/instances/ (gitignored)

Agent activity -------------> journal plugin ---------------> .claude/journal/

Reflection commands --------> perspective agents -----------> .claude/perspectives/
                                                              .claude/social/walls/

URL ingestion --------------> librarian --------------------> .claude/library/

System observation ---------> archivist --------------------> .claude/archive/
```

---

## Recommendations

### 1. Document the Pattern

Create a formal "Data as Markdown" specification:
- YAML frontmatter schema requirements
- ID generation conventions
- File naming patterns
- Required vs optional fields

### 2. Standardize Gitignore Decisions

Create a data governance policy:
- External API data: Always gitignore (regenerable)
- Session/instance data: Always gitignore (sensitive)
- User-created content: Commit by default
- Agent-generated content: Commit if valuable

### 3. Consider Data Encryption

For high-sensitivity committed data:
- `.claude/journal/` entries could contain personal reflections
- `backlog/tasks/` could contain confidential project details
- Consider git-crypt or similar for sensitive directories

### 4. Add Pruning Mechanisms

Instance data accumulates rapidly:
- 500+ count files created in ~2 days
- Consider rotation/archival policy
- Auto-cleanup of stale sessions

### 5. Create Data Export Tooling

Users should be able to:
- Export all personal data
- Delete external sync data
- Audit what's stored

---

## File Count Summary

| Category | Tracked (Git) | Untracked/Ignored |
|----------|--------------|-------------------|
| Journal Entries | 53 | 0 |
| Social | 38 | 0 |
| Backlog | 25 | 0 |
| Planning | 19 | ~3 |
| Perspectives | 10 | 0 |
| Session Logs | 0 | ~50+ |
| Schedule (Manual) | 26 | 0 |
| Schedule (GCal) | 0 | ~60 |
| Instance Registry | 0 | ~600+ |
| Archive | 8 | 0 |
| Library | 16 | 0 |
| Storms | 2 | 1 |
| Briefings | 1 | 0 |
| Exploration | 3 | 0 |

**Total Tracked**: ~200 data files
**Total Ignored**: ~700+ data files

---

*This observation captures the data metabolism of the ecosystem as of 2025-12-17.*
