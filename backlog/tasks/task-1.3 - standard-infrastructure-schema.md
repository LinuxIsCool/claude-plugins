---
id: task-1.3
title: "Define Standard Infrastructure Schema"
status: "To Do"
priority: high
labels: [infrastructure, architecture]
milestone: v1.0-personas-mvp
parentTaskId: task-1
dependencies: [task-1.1, task-1.2]
created: 2025-12-12
assignee: ["@claude"]
---

# Define Standard Infrastructure Schema

## Description

Define the standard infrastructure that ALL personas will share, regardless of which memory approach is chosen. This ensures consistency and interoperability across the persona ecosystem.

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Define identity.md schema (required fields, optional fields)
- [ ] #2 Define state.md schema (session state, active context)
- [ ] #3 Define memory entry schema (type, timestamp, confidence, tags)
- [ ] #4 Define _shared/ directory contents and schemas
- [ ] #5 Define wikilink naming conventions
- [ ] #6 Define temporal directory structure (YYYY-MM pattern)
- [ ] #7 Create template files in _schema/ directory
- [ ] #8 Document loading precedence (what loads when)
- [ ] #9 Define inter-persona reference patterns
- [ ] #10 Create validation script for schema compliance
<!-- AC:END -->

## Schema Components

### 1. Identity Schema

Required fields:
- `name`: Display name (e.g., "The Archivist")
- `plugin`: Associated plugin name
- `archetype`: Role description
- `version`: Schema version
- `created`: Creation timestamp

Optional fields:
- `last_active`: Last interaction timestamp
- `voice`: Personality description
- `capabilities`: List of skills/tools
- `values`: Core principles

### 2. State Schema

Required fields:
- `active_context`: Current focus area
- `session_id`: Current session (if any)
- `last_updated`: Timestamp

Optional fields:
- `pending_tasks`: List of in-progress work
- `recent_topics`: Last N topics discussed
- `user_mood`: Detected user state

### 3. Memory Entry Schema

Required fields:
- `type`: Category (learning, observation, preference, fact)
- `timestamp`: When recorded
- `source`: Where this came from (session ID, file, etc.)

Optional fields:
- `confidence`: 0.0-1.0 certainty level
- `tags`: Categorization
- `supersedes`: ID of memory this replaces
- `expires`: When to archive/forget

### 4. Shared State Schema

Files in `_shared/`:
- `user-profile.md`: User preferences, patterns, context
- `project-context.md`: Current project state
- `vocabulary.md`: Shared terms and definitions
- `active-goals.md`: Cross-persona objectives

### 5. Wikilink Conventions

```
[[persona-name/file]]           - Cross-persona reference
[[memory/YYYY-MM/entry]]        - Temporal memory reference
[[_shared/user-profile]]        - Shared state reference
[[#section-name]]               - Same-file section reference
```

### 6. Temporal Structure

```
memory/
├── permanent/          # Never expires
├── 2025-12/           # Monthly buckets
├── 2025-11/
└── archive/           # Compressed old memories
```

## Implementation Notes

This task should be completed AFTER the architecture decision (task-1.1 vs task-1.2) to ensure the schema supports the chosen approach.
