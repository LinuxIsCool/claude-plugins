---
id: task-1.6
title: "Implement Inter-Persona Communication Pattern"
status: "To Do"
priority: medium
labels: [infrastructure, architecture]
milestone: v1.1-inter-agent
parentTaskId: task-1
dependencies: [task-1.4, task-1.5]
created: 2025-12-12
assignee: ["@claude"]
---

# Implement Inter-Persona Communication Pattern

## Description

Define and implement how personas communicate with each other. This enables:
- Task handoffs (Organizer → Scribe: "Document this completed task")
- Knowledge sharing (Explorer → Cartographer: "Map these discoveries")
- Collaborative workflows (Multiple personas working on complex requests)

## Communication Patterns

### Pattern 1: Wikilink References (Passive)
Personas reference each other's memories via wikilinks:
```markdown
## Related
- [[mentor/memory/permanent/teaching-style]]
- [[archivist/memory/2025-12/session-summary]]
```

### Pattern 2: Shared State (Coordinated)
Personas read/write to `_shared/` for coordination:
```markdown
# _shared/active-goals.md
- [ ] Complete authentication feature (@organizer tracking)
- [ ] Document learnings (@scribe assigned)
- [ ] Build knowledge graph (@cartographer queued)
```

### Pattern 3: Explicit Handoff (Active)
One persona explicitly delegates to another:
```markdown
# archivist/outbox/handoff-001.md
---
from: archivist
to: scribe
type: handoff
status: pending
created: 2025-12-12T14:30:00
---

## Request
Please create a journal entry summarizing today's session.

## Context
- Session ID: abc123
- Key topics: authentication, user preferences
- Duration: 45 minutes

## Attachments
- [[archivist/memory/2025-12/session-abc123]]
```

### Pattern 4: Broadcast (One-to-Many)
Persona announces to all:
```markdown
# _shared/announcements/2025-12-12-user-preference.md
---
from: archivist
to: all
type: announcement
---

## New User Preference Detected
The user prefers detailed explanations over brief responses.

All personas should adjust communication style accordingly.
```

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Define wikilink cross-reference conventions
- [ ] #2 Design _shared/ state management patterns
- [ ] #3 Design handoff protocol (request/response format)
- [ ] #4 Design broadcast/announcement pattern
- [ ] #5 Implement handoff processing for prototype personas
- [ ] #6 Test cross-persona memory access
- [ ] #7 Document communication patterns in developer guide
<!-- AC:END -->

## Architecture Options

### Option A: File-Based (Recommended for MVP)
- Handoffs as markdown files in `outbox/` directories
- Shared state in `_shared/`
- Wikilinks for passive references
- Polling via Glob/Grep

### Option B: A2A Protocol (Future)
- Formal agent-to-agent protocol
- JSON-based messages
- Discovery mechanism
- Task lifecycle management

**Recommendation**: Start with Option A (file-based) to maintain markdown-native philosophy. Add A2A in v2.0 if needed for real-time coordination.

## Implementation Notes

Inter-persona communication should feel natural, like colleagues leaving notes for each other. The filesystem provides the "message board" - no need for complex infrastructure.
