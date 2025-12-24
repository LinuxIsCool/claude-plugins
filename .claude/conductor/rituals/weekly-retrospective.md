# Ritual: Weekly Retrospective

**Trigger**: Sunday evening or end of work week
**Model**: Opus (deep synthesis)
**Duration**: 10-15 minutes
**Agents**: Conductor + archivist + agent-architect (optional)

## Purpose

Step back. See the week as a whole. Identify patterns, celebrate progress, course-correct.

## Steps

### 1. Gather Week's Data

**Git Activity**:
```bash
git log --since="1 week ago" --oneline | head -50
git shortlog --since="1 week ago" -s
```

**Sessions**:
```bash
# Count sessions this week
find .claude/logging/$(date +%Y/%m)/ -name "*.jsonl" -mtime -7 | wc -l
```

**Journal Entries**:
```bash
# Atomics this week
find .claude/journal/$(date +%Y/%m)/ -name "*.md" -mtime -7 | wc -l
```

### 2. Invoke Archivist (Optional)

If significant activity:
```
Task(archivist): "What were the metabolic patterns this week?"
```

### 3. Review Against Goals

Check planning documents:
- What did we intend to accomplish?
- What actually happened?
- What's the delta?

### 4. Identify Patterns

**Working Well**:
- What patterns contributed to progress?
- What should we do more of?

**Not Working**:
- What patterns created friction?
- What should we stop or change?

**Emerging**:
- What new patterns are forming?
- What wants to be different?

### 5. Update Conductor State

**User Model**:
- Any new observations from week's behavior?
- Confidence changes?

**Anticipations**:
- Updated hypotheses for next week?
- New value opportunities?

**Pulse**:
- Ecosystem health assessment
- Agent activity patterns

### 6. Create Weekly Summary

```markdown
---
created: {timestamp}
author: conductor
description: "Weekly retrospective: {date-range}"
parent_daily: [[{latest-daily}]]
tags: [retrospective, weekly]
---

# Week of {start-date}

## Numbers
- Sessions: {count}
- Commits: {count}
- Journal atomics: {count}
- Agents invoked: {list}

## What Happened
{2-3 paragraph narrative}

## Working Well
- {pattern 1}
- {pattern 2}

## Not Working
- {friction 1}
- {friction 2}

## Next Week
- {intention 1}
- {intention 2}

## Gratitude
- {what was good this week}

---

*Parent: [[{YYYY-MM-DD}]] → [[{YYYY-MM}]] → [[{YYYY}]]*
```

### 7. Commit

```bash
git add .claude/
git commit -m "[journal] retrospective: week of {date}

Sessions: {N}
Commits: {N}
Key theme: {summary}"
```

## Output Format

```
## Weekly Retrospective: {date-range}

**Activity**: {sessions} sessions, {commits} commits, {atomics} journal entries

**Key Pattern**: {what defined this week}

**Adjustment**: {what to change next week}

**Health**: {ecosystem pulse assessment}
```

## Quality Gates

- [ ] Actually synthesizes, not just reports
- [ ] Identifies actionable patterns
- [ ] Connects to larger trajectory
- [ ] Celebrates progress, however small
- [ ] Honest about friction

## Learning

Track:
- Do retrospectives influence next week?
- Are patterns identified accurate?
- What retrospective questions add most value?

---

## Execution Log

| Week | Sessions | Commits | Key Pattern | Adjustment |
|------|----------|---------|-------------|------------|
| *Awaiting first execution* | - | - | - | - |
