---
created: 2025-12-15T20:00:00
author: persona:coordinator
description: The Coordinator observes and records user scheduling preferences
parent_daily: [[2025-12-15]]
tags: [preference, schedule, yoga, observation, coordinator, persona-memory]
related:
  - "[[plugins/Schedule.md]]"
  - "[[task-1.6]]"
---

# The Coordinator: Observed Preferences

*First memory contribution from a plugin persona*

## Yoga Scheduling Preferences

### Location
**Ember Studios** is the exclusive yoga location.
- All 4 weekly yoga classes are at this studio
- Confidence: **Very High** (4/4 data points)

### Instructors
Two instructors are in regular rotation:
- **David**: Monday evening Powerflow, Saturday morning Powerflow
- **Justin**: Tuesday evening Flow, Friday evening Powerflow

User appears to alternate between instructors throughout the week.
- Confidence: **High** (consistent pattern across schedule)

### Class Types
- **Powerflow**: 3 classes/week (favored)
- **Flow**: 1 class/week

User shows preference for Powerflow over other class types.
- Confidence: **Medium** (may depend on instructor/time availability)

### Time Preferences

| Day | Time | Pattern |
|-----|------|---------|
| Weekday evenings | 5:30-7:00 PM | Post-work yoga (Mon/Tue/Fri) |
| Saturday morning | 10:30 AM | Weekend yoga |

**Key Insight**: User prefers yoga AFTER work hours on weekdays, but MORNING yoga on weekends.
- Confidence: **High** (4 data points consistent)

### Application
When suggesting yoga classes:
1. Prioritize Ember Studios
2. Check David and Justin's schedules
3. Suggest Powerflow classes over other types
4. For weekdays: suggest evening slots (5:30-7:00 PM)
5. For weekends: suggest morning slots (10:00-11:30 AM)

---

## Work Pattern Observations

### Core Hours
- **Start**: 7:00 AM (consistent across all weekdays)
- **Lunch**: 12:00-1:00 PM (daily, protected)
- **End**: Variable by day

### Daily Patterns

| Day | Work Hours | Afternoon Activity |
|-----|------------|-------------------|
| Monday | 7am-3pm (7h) | Hike, then yoga |
| Tuesday | 7am-5pm (9h) | Evening yoga |
| Wednesday | 7am-3pm (7h) | Hike |
| Thursday | 7am-1pm (5h) | Therapy |
| Friday | 7am-3pm (7h) | Hike, then yoga |

**Key Insight**: Tuesday is the "long day" - full 9 hours with evening yoga. M/W/F are balanced with afternoon outdoor time.
- Confidence: **High**

### Application
When scheduling:
- Protect 7am-noon as focused work time
- Never schedule over lunch
- Avoid Tuesday afternoons for non-work activities
- Thursdays are therapy-focused afternoons

---

## Outdoor Activity Patterns

### Hiking with Kai
- **Days**: Monday, Wednesday, Friday
- **Time**: 3:00-4:00 PM (immediately after afternoon work block)
- **Duration**: 1 hour consistently
- **Companion**: "Kai" (appears in all outdoor blocks)

**Key Insight**: User values outdoor time with Kai on M/W/F, scheduled as a transition between work and evening activities.
- Confidence: **Very High** (3 data points, same pattern)

### Application
- If suggesting outdoor activities, M/W/F at 3pm are established slots
- Kai is a regular outdoor companion

---

## Weekly Rhythm Summary

```
Mon: Work → Hike (Kai) → Yoga (David)
Tue: Long work → Evening yoga (Justin)
Wed: Work → Hike (Kai)
Thu: Short work → Therapy (Emily)
Fri: Work → Hike (Kai) → Yoga (Justin)
Sat: Morning yoga (David) → Farmers market
Sun: Deep cleaning
```

### Category Distribution
- Work: 66% (primary focus)
- Yoga: 8% (wellness priority)
- Outdoor: 6% (regular movement)
- Meals: 9% (protected lunch)
- Personal: 4% (therapy, cleaning)
- Errands: 2% (groceries)

---

## How This Memory Will Be Used

When the yoga-scheduler skill is invoked:
1. Query this atomic for preferences
2. Apply preferences to class suggestions
3. Update observations if preferences change

When scheduling conflicts arise:
1. Consult work patterns
2. Protect established rhythms
3. Suggest alternatives aligned with observed preferences

---

*This atomic demonstrates the persona memory pattern: plugin personas observe, record to journal, and recall in future sessions.*

---

*Parent: [[2025-12-15]]*
