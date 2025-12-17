---
id: msg_DzBGzjRAMFCxiTfsy9xugyE4zymxn5MH
kind: 103
account_id: claude
created_at: 1765496103777
imported_at: 1766005508412
author_name: Claude
thread_id: cc_0d56ffcb
platform: claude-code
session_id: 0d56ffcb-4606-4cd4-84b6-6e065ab2d4ca
tags: [["event_type","AssistantResponse"]]
---

## Schedule.md Plugin - Plan Summary

I've created a comprehensive plan at `.claude/planning/schedule-plugin-plan.md`. Here's the reflection on the design and next steps:

---

### Architecture Decisions (Inspired by Backlog.md)

| Component | Approach |
|-----------|----------|
| **Storage** | Markdown files with YAML frontmatter in `schedule/blocks/` |
| **Core Layer** | TypeScript `Schedule` class with CRUD operations |
| **Claude Integration** | MCP stdio server with block management tools |
| **Web Interface** | React + Tailwind with weekly grid layout |
| **Real-time Sync** | WebSocket broadcasts on file changes |
| **Runtime** | Bun (fast, native TypeScript) |

---

### Three-Phase Breakdown

**Phase 1 - Core MVP**
- Weekly calendar grid with color-coded blocks
- Manual block creation/editing via Claude conversations
- MCP tools: `block_create`, `block_list`, `block_view`, `block_edit`, `block_delete`, `schedule_summary`
- CLI: `schedule init`, `schedule serve`, `schedule mcp start`

**Phase 2 - External Integrations**
- Google Calendar OAuth + overlay
- Yoga studio schedule scraping
- Visual source toggles (personal vs external)
- One-way sync from external sources

**Phase 3 - Analytics & Intelligence**
- Hours per category statistics
- Free slot finder
- Conflict detection
- Export to iCal/PDF
- Recurring event templates

---

### Key Data Model

Each schedule block is a markdown file:
```yaml
---
title: Vinyasa Flow
category: yoga
color: "#22c55e"
day: monday
startTime: "09:00"
endTime: "10:30"
---
```

Categories define the color scheme (yoga=green, work=blue, etc.)

---

### Reflection & Next Steps

**Questions to consider:**

1. **Category preset vs custom** - Start with fixed categories (yoga, work, class, personal, meeting, blocked) or allow custom categories from day one?

2. **Recurring events** - Include weekly recurrence in Phase 1 (simplifies yoga schedule) or defer to Phase 3?

3. **Time zone handling** - Assume local time only, or build in timezone support early?

4. **Plugin location** - Create this as a standalone plugin in `resources/Schedule.md/` (like Backlog.md) or a lighter structure?

**Recommended immediate next steps:**

1. Scaffold the plugin structure with `.claude-plugin/plugin.json`
2. Create the core `Schedule` class with markdown parsing
3. Implement the MCP server with `block_create` and `block_list`
4. Build a minimal React weekly grid
5. Wire up the HTTP server

Would you like me to proceed with creating the Phase 1 implementation scaffold?
