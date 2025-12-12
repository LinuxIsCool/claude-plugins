# Schedule.md Plugin - Architecture & Development Plan

## Vision

A markdown-native weekly schedule management system inspired by university class schedulers. Built as a Claude Code plugin with a visual web interface showing color-coded time blocks. Claude can help manage, analyze, and populate the schedule through conversation.

---

## Architecture Overview (Inspired by Backlog.md)

```
schedule.md/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── src/
│   ├── cli.ts                # CLI entry point
│   ├── index.ts              # Public exports
│   ├── core/
│   │   ├── schedule.ts       # Core business logic
│   │   ├── content-store.ts  # Reactive data store
│   │   └── time-utils.ts     # Time parsing/formatting
│   ├── mcp/
│   │   ├── server.ts         # MCP stdio server
│   │   └── tools/
│   │       └── blocks/       # Schedule block tools
│   ├── web/
│   │   ├── App.tsx           # React root
│   │   ├── components/
│   │   │   ├── WeekView.tsx  # Main weekly calendar grid
│   │   │   ├── TimeBlock.tsx # Individual schedule block
│   │   │   └── DayColumn.tsx # Single day column
│   │   └── lib/
│   │       └── api.ts        # Frontend API client
│   ├── server/
│   │   └── index.ts          # HTTP/WebSocket server
│   └── types/
│       └── index.ts          # TypeScript definitions
├── commands/
│   └── schedule.md           # Slash command definitions
├── schedule/
│   ├── config.json           # Schedule configuration
│   └── blocks/               # Markdown block files
├── CLAUDE.md                 # Agent instructions
└── package.json
```

---

## Data Model

### Schedule Block (Markdown Format)

```markdown
---
id: yoga-monday-am
title: Vinyasa Flow
category: yoga
color: "#22c55e"
day: monday
startTime: "09:00"
endTime: "10:30"
location: "Yoga Studio - Room A"
recurring: weekly
tags: [exercise, wellness]
source: manual | google-calendar | yoga-studio
externalId: null
---

# Vinyasa Flow

Monday morning yoga class to start the week.

## Notes
- Bring mat and water
- Arrives 10 minutes early
```

### Categories & Color Coding

```json
{
  "categories": {
    "yoga": { "color": "#22c55e", "label": "Yoga" },
    "work": { "color": "#3b82f6", "label": "Work" },
    "class": { "color": "#8b5cf6", "label": "Class" },
    "personal": { "color": "#f97316", "label": "Personal" },
    "meeting": { "color": "#ef4444", "label": "Meeting" },
    "blocked": { "color": "#6b7280", "label": "Blocked" }
  }
}
```

### Configuration (`schedule/config.json`)

```json
{
  "projectName": "My Schedule",
  "weekStartsOn": "monday",
  "dayStartHour": 6,
  "dayEndHour": 22,
  "timeSlotMinutes": 30,
  "defaultPort": 6421,
  "categories": { ... },
  "integrations": {
    "googleCalendar": { "enabled": false },
    "yogaStudio": { "enabled": false, "url": null }
  }
}
```

---

## Phase 1: Core Schedule System (MVP)

### Goal
Create a functional schedule viewer with manual block entry through Claude.

### Deliverables

#### 1.1 Plugin Structure
- [x] Create `.claude-plugin/plugin.json` manifest
- [ ] Set up TypeScript project with Bun
- [ ] Create package.json with dependencies
- [ ] Initialize directory structure

#### 1.2 Core Module
- [ ] `Schedule` class with CRUD operations for blocks
- [ ] Markdown parser/serializer for schedule blocks
- [ ] Time validation and conflict detection
- [ ] Content store with file watchers

#### 1.3 MCP Server
- [ ] Stdio transport setup
- [ ] Tools:
  - `block_create` - Create new schedule block
  - `block_list` - List blocks (filterable by day/category)
  - `block_view` - View block details
  - `block_edit` - Modify existing block
  - `block_delete` - Remove block
  - `schedule_summary` - Get weekly overview
  - `schedule_search` - Search blocks by text

#### 1.4 Web Interface
- [ ] React app with weekly grid layout
- [ ] Color-coded time blocks
- [ ] Day columns (Mon-Sun)
- [ ] Hour rows (configurable range)
- [ ] Click block to view details
- [ ] Real-time updates via WebSocket

#### 1.5 HTTP Server
- [ ] Bun-based server (port 6421)
- [ ] REST API endpoints
- [ ] WebSocket for live sync
- [ ] Static asset serving

#### 1.6 CLI Commands
- [ ] `schedule init` - Initialize in project
- [ ] `schedule mcp start` - Start MCP server
- [ ] `schedule serve` - Start web server
- [ ] `schedule list` - CLI block listing

### Phase 1 Tech Stack
- **Runtime**: Bun
- **Frontend**: React + Tailwind CSS
- **Backend**: Bun HTTP server
- **Storage**: Markdown files with YAML frontmatter
- **MCP**: @modelcontextprotocol/sdk (stdio transport)

---

## Phase 2: External Integrations

### Goal
Connect to external calendar sources for a unified schedule view.

### Deliverables

#### 2.1 Google Calendar Integration
- [ ] OAuth 2.0 flow for authorization
- [ ] Fetch calendar events via Google Calendar API
- [ ] Map Google events to schedule blocks
- [ ] Visual overlay toggle (show/hide Google events)
- [ ] Configurable calendars to sync
- [ ] One-way sync (read-only from Google)

#### 2.2 Yoga Studio Integration
- [ ] Configurable studio URL
- [ ] Web scraping or API integration (studio-specific)
- [ ] Parse class schedule into blocks
- [ ] Auto-categorize as "yoga"
- [ ] MCP tool: `yoga_fetch_schedule` - Pull latest classes

#### 2.3 Enhanced Web UI
- [ ] Toggle overlays (personal/google/yoga)
- [ ] Visual distinction for external events (opacity, icons)
- [ ] Filtering by source
- [ ] Week navigation (prev/next week)

#### 2.4 MCP Tools
- [ ] `google_sync` - Trigger Google Calendar sync
- [ ] `integration_status` - Check integration status
- [ ] `sources_list` - List configured sources

---

## Phase 3: Analytics & Intelligence

### Goal
Add statistics, smart suggestions, and advanced features.

### Deliverables

#### 3.1 Statistics Dashboard
- [ ] Hours per category per week
- [ ] Weekly/monthly trends
- [ ] Category breakdown pie chart
- [ ] Busiest days analysis
- [ ] Free time windows

#### 3.2 MCP Analytics Tools
- [ ] `stats_weekly` - Get weekly statistics
- [ ] `stats_category` - Time by category
- [ ] `stats_trends` - Historical patterns
- [ ] `free_slots` - Find available time windows

#### 3.3 Smart Features
- [ ] Conflict detection and warnings
- [ ] Schedule optimization suggestions
- [ ] Recurring event support
- [ ] Template schedules (save/load week templates)
- [ ] Natural language time parsing

#### 3.4 Export/Import
- [ ] Export to iCal format
- [ ] Export to PDF (printable weekly view)
- [ ] Import from iCal/CSV
- [ ] Backup/restore schedule data

---

## MCP Tool Schemas (Phase 1)

### block_create

```typescript
{
  name: "block_create",
  description: "Create a new schedule block",
  inputSchema: {
    type: "object",
    properties: {
      title: { type: "string", description: "Block title" },
      category: { type: "string", enum: ["yoga", "work", "class", "personal", "meeting", "blocked"] },
      day: { type: "string", enum: ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"] },
      startTime: { type: "string", pattern: "^([01]?[0-9]|2[0-3]):[0-5][0-9]$", description: "Start time (HH:MM)" },
      endTime: { type: "string", pattern: "^([01]?[0-9]|2[0-3]):[0-5][0-9]$", description: "End time (HH:MM)" },
      location: { type: "string", description: "Optional location" },
      description: { type: "string", description: "Optional description" },
      recurring: { type: "string", enum: ["none", "weekly"], default: "weekly" }
    },
    required: ["title", "category", "day", "startTime", "endTime"]
  }
}
```

### block_list

```typescript
{
  name: "block_list",
  description: "List schedule blocks with optional filters",
  inputSchema: {
    type: "object",
    properties: {
      day: { type: "string", enum: ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"] },
      category: { type: "string" },
      source: { type: "string", enum: ["manual", "google-calendar", "yoga-studio"] }
    }
  }
}
```

### schedule_summary

```typescript
{
  name: "schedule_summary",
  description: "Get a summary of the weekly schedule",
  inputSchema: {
    type: "object",
    properties: {
      includeStats: { type: "boolean", default: false }
    }
  }
}
```

---

## Web Interface Design

### Weekly Grid Layout

```
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│   Monday    │   Tuesday   │  Wednesday  │  Thursday   │   Friday    │  Saturday   │   Sunday    │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ 6:00        │             │             │             │             │             │             │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ 7:00        │             │ ┌─────────┐ │             │             │             │             │
│             │             │ │ Morning │ │             │             │             │             │
├─────────────┼─────────────┤ │  Yoga   │ ├─────────────┼─────────────┼─────────────┼─────────────┤
│ 8:00        │             │ │ (green) │ │             │             │             │             │
│             │             │ └─────────┘ │             │             │             │             │
├─────────────┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┼─────────────┤
│ 9:00        │ ┌─────────┐ │             │ ┌─────────┐ │             │             │             │
│             │ │  Work   │ │             │ │  Work   │ │             │             │             │
│             │ │  Block  │ │             │ │  Block  │ │             │             │             │
│             │ │ (blue)  │ │             │ │ (blue)  │ │             │             │             │
├─────────────┤ └─────────┘ ├─────────────┤ └─────────┘ ├─────────────┼─────────────┼─────────────┤
│ ...         │             │             │             │             │             │             │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘

Legend: [Yoga] [Work] [Class] [Personal] [Meeting] [Blocked] [Google Calendar (overlay)]
```

### Component Hierarchy

```
App
├── Header
│   ├── Title
│   ├── WeekSelector (← Week →)
│   └── OverlayToggles (Phase 2)
├── WeekView
│   ├── TimeColumn (hour labels)
│   └── DayColumn × 7
│       └── TimeBlock × N (positioned absolutely)
├── BlockDetailsModal
│   ├── BlockInfo
│   └── EditForm
└── StatsPanel (Phase 3)
```

---

## Conversation Examples with Claude

### Adding a Schedule Block

```
User: Add yoga at 9am on Monday and Wednesday mornings
Claude: I'll create those yoga blocks for you.
        [Uses block_create tool twice]
        Done! Added:
        - Monday 9:00-10:00 AM - Yoga
        - Wednesday 9:00-10:00 AM - Yoga
        View your schedule at http://localhost:6421
```

### Checking Schedule

```
User: How does my Tuesday look?
Claude: [Uses schedule_summary with day filter]
        Your Tuesday schedule:
        - 9:00-12:00: Work Block
        - 12:30-13:00: Lunch Meeting
        - 14:00-17:00: Work Block

        You have 5 hours of work scheduled and 1 meeting.
        Free slots: 6:00-9:00, 13:00-14:00, 17:00-22:00
```

### Phase 2 - Yoga Integration

```
User: Can you pull in my yoga schedule from the studio?
Claude: [Uses yoga_fetch_schedule tool]
        Found 6 classes from your yoga studio this week:
        - Mon 9:00 AM: Vinyasa Flow (Room A)
        - Tue 6:00 PM: Restorative Yoga (Room B)
        ...
        Would you like me to add these to your schedule?
```

---

## Development Roadmap

### Phase 1 Timeline (Core MVP)
1. Project setup & plugin structure
2. Core module (Schedule class, markdown parsing)
3. MCP server with basic tools
4. Web interface (weekly grid, blocks)
5. HTTP server & real-time sync
6. CLI commands & initialization

### Phase 2 Timeline (Integrations)
1. Google Calendar OAuth setup
2. Google Calendar API integration
3. Yoga studio scraper/connector
4. UI overlays and source toggling
5. Integration MCP tools

### Phase 3 Timeline (Analytics)
1. Statistics calculations
2. Stats dashboard UI
3. Analytics MCP tools
4. Smart features (conflicts, suggestions)
5. Export functionality

---

## Next Steps

1. **Create plugin scaffold** - Set up the basic structure
2. **Implement Schedule core class** - CRUD operations for blocks
3. **Build MCP server** - Basic tools for Claude integration
4. **Create web interface** - Weekly grid with time blocks
5. **Connect everything** - HTTP server with WebSocket sync

Ready to begin Phase 1 implementation?
