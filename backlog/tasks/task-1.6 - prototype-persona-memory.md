---
id: task-1.6
title: "Prototype Memory Persistence with The Coordinator (Schedule)"
status: "Done"
priority: medium
labels: [memory, personas, prototype]
milestone: v1.0-activation
parentTaskId: task-1
dependencies: [task-1.5]
created: 2025-12-15
assignee: ["@claude"]
---

# Prototype Memory Persistence with The Coordinator

## Description

Test the memory access pattern defined in task-1.5 with The Coordinator (Schedule.md plugin persona). This persona is ideal for prototyping because:

1. **Clear preferences**: User has observable patterns (yoga times, work hours)
2. **Existing data**: Schedule blocks encode implicit preferences
3. **Measurable success**: Can validate if persona "remembers" across sessions

### The Coordinator Profile

From registry:
- **Persona Identity**: Time keeper
- **Domain**: Weekly scheduling, yoga planning
- **Primary Skills**: yoga-scheduler, web-scraper

### Current Behavior

The schedule plugin already "learns" preferences by reading existing blocks:
> "The yoga-scheduler learns from existing blocks"

This is implicit memory. The prototype makes it explicit.

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Define what The Coordinator should remember
- [x] #2 Create at least one journal atomic capturing a preference
- [x] #3 Validate preference is queryable in next session
- [x] #4 Demonstrate persona using recalled preference
- [x] #5 Document the memory flow for other personas
<!-- AC:END -->

## What The Coordinator Should Remember

### User Preferences
- Preferred yoga times (e.g., mornings)
- Preferred instructors
- Work hour patterns
- Categories of schedule blocks created

### Interaction Patterns
- How user phrases schedule requests
- Level of detail user prefers
- Conflicts user accepts/rejects

### Observations
- Time spent per category weekly
- Schedule density patterns
- Common adjustments made

## Prototype Flow

### Session 1: Learn and Record

1. User interacts with schedule plugin
2. Coordinator observes: "User prefers yoga at 9am"
3. Coordinator creates journal atomic:

```markdown
---
created: 2025-12-15T10:30:00
author: persona:coordinator
description: User prefers morning yoga sessions
parent_daily: [[2025-12-15]]
tags: [preference, schedule, yoga, coordinator]
related: [[schedule-plugin]]
---

# User Prefers Morning Yoga

## Observation
User has consistently scheduled yoga sessions before 10am.
- Monday: 9:00
- Wednesday: 9:00
- Friday: 9:30

## Confidence
High - 3 data points, consistent pattern

## Application
When suggesting yoga classes, prioritize morning options.
```

### Session 2: Recall and Apply

1. New session begins
2. Coordinator loads (via progressive disclosure):
   - Skill definition (identity)
   - Recent journal atomics tagged `coordinator`
3. User asks: "Can you help me find a yoga class?"
4. Coordinator recalls morning preference
5. Coordinator responds: "Based on your usual schedule, here are morning classes..."

## Success Metrics

| Metric | Target |
|--------|--------|
| Memory recorded | At least 1 atomic created |
| Memory retrieved | Queryable via grep/journal-browser |
| Memory applied | Persona references past preference |
| Pattern replicable | Can document for other personas |

## Implementation Steps

1. **Enhance yoga-scheduler skill** to record preferences
2. **Add journal atomic creation** to skill workflow
3. **Add memory query** at skill invocation
4. **Test across sessions**
5. **Document pattern**

## Notes

This prototype validates the "ecosystem memory" approach:
- No separate persona storage
- Journal as shared memory
- Author attribution (`persona:coordinator`)
- Standard atomic format

If successful, this pattern applies to all 11 plugin personas.
