---
created: 2025-12-11T17:01:00
author: user
description: Schedule.md v1.0.0 is released - the first 1.0 plugin in the marketplace
parent_daily: [[2025-12-11]]
tags: [release, milestone, schedule, mcp, v1]
related:
  - "[[plugins/Schedule.md]]"
---

# Schedule.md v1.0.0 Released

## Event

The Schedule.md plugin reaches v1.0.0 - the first plugin in the marketplace to achieve release status.

```
git commit -m "feat(schedule.md): Release v1.0.0 - Markdown-native weekly schedule manager"
```

## What It Does

A markdown-native weekly schedule manager:
- Schedule blocks stored as markdown files
- MCP server for tool access
- Yoga scheduler integration
- Web scraper for studio schedules
- All data in human-readable format

## Architecture

```
plugins/Schedule.md/
├── schedule/
│   ├── config.json
│   └── blocks/           # Markdown schedule entries
├── src/
│   ├── mcp/server.ts     # MCP tool server
│   ├── core/schedule.ts  # Core logic
│   └── markdown/         # Parser/serializer
└── skills/
    └── yoga-scheduler/   # Learning preferences
```

## Significance

This release demonstrated:
1. **MCP integration** - First plugin with tool server
2. **Skill pattern** - Progressive disclosure via skills
3. **Markdown-native** - Data as documents, not databases
4. **Domain specificity** - Solves a real user need

## The Coordinator Persona

Schedule.md would later be identified as the embodiment of "The Coordinator" persona:
- Time keeper
- Pattern observer
- Preference learner

This release established the foundation for persona memory prototyping.

---

*Parent: [[2025-12-11]]*
