---
id: msg_Ea8gdxFyQ2Fej838pn95UPL8Wb6C824P
kind: 103
account_id: claude
created_at: 1766003249737
imported_at: 1766005522351
author_name: Claude
thread_id: cc_835d7c4b
platform: claude-code
session_id: 835d7c4b-361c-4a49-82a1-3ab400150ee6
tags: [["event_type","AssistantResponse"]]
---

They're **Google Calendar events synced to markdown files** by your Schedule.md plugin.

### Example 1: Therapy Appointment
```yaml
---
id: gcal-3bjk96
title: "Resonance Therapy and Coaching"
category: personal
day: thursday
startTime: "13:30"
endTime: "14:45"
recurring: weekly
source: google-calendar
---
```

### Example 2: Flight
```yaml
---
id: gcal-269q6c
title: "Flight to Seattle (AS 462)"
day: saturday
startTime: "15:08"
location: "Newark EWR"
source: google-calendar
---
```

### What They Are

| Aspect | Detail |
|--------|--------|
| **Source** | Auto-synced from your Google Calendar |
| **Content** | Personal appointments, meetings, flights, therapy sessions |
| **Count** | 48 files |
| **Nature** | Generated data, not hand-written code |

### The Decision

**Commit them?**
- ✓ Version-controlled schedule history
- ✗ Personal data in git
- ✗ Will change constantly as calendar changes
- ✗ Can be regenerated from Google Calendar API

**Gitignore them?**
- ✓ Keeps repo clean
- ✓ No personal data in version control
- ✓ Regenerated on demand from Google Calendar
- ✗ No local backup in git

**Your call** - this is personal preference about whether you want calendar data version-controlled.
