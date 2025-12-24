# Ritual: Daily Synthesis

**Trigger**: End of working day (manual or scheduled)
**Model**: Sonnet (efficient synthesis)
**Duration**: 2-5 minutes
**Agents**: Conductor + journal:scribe

## Purpose

Synthesize day's work into atomic journal entries. Create daily summary if warranted.

## Steps

### 1. Gather Day's Activity
```bash
# Commits today
git log --since="midnight" --oneline

# Sessions today
ls .claude/logging/$(date +%Y/%m/%d)/ 2>/dev/null || echo "No sessions"

# Changes today
git diff --stat HEAD~5..HEAD 2>/dev/null || git status --short
```

### 2. Identify Journal-Worthy Topics

**Worth documenting**:
- Significant decisions made
- New patterns discovered
- Milestones reached
- Problems solved (or encountered)
- Insights gained
- Direction changes

**Not worth documenting**:
- Routine maintenance
- Minor fixes
- Work-in-progress with no conclusion

### 3. Create Atomic Entries

For each worthy topic:
```markdown
---
created: {timestamp}
author: conductor
description: "{one-line summary}"
parent_daily: [[{YYYY-MM-DD}]]
tags: [{relevant-tags}]
related: [{wikilinks}]
---

# {Title}

{2-4 paragraph reflection}

---

*Parent: [[{YYYY-MM-DD}]] → [[{YYYY-MM}]] → [[{YYYY}]]*
```

### 4. Create Daily Summary (If Multiple Atomics)

Only if >1 atomic entry created:
```markdown
---
created: {timestamp}
author: conductor
description: "Daily synthesis for {date}"
---

# {YYYY-MM-DD}

## Summary
{2-3 sentence overview}

## Atomics
- [[{time}-{title}]]
- [[{time}-{title}]]

## Themes
- {common thread}

---

*Parent: [[{YYYY-MM}]] → [[{YYYY}]]*
```

### 5. Commit

```bash
git add .claude/journal/
git commit -m "[journal] synthesize: daily entries for {date}

Agent: conductor
Atomics: {count}
Themes: {list}"
```

## Output Format

```
## Daily Synthesis: {date}

**Atomics Created**: {count}
- {title 1}
- {title 2}

**Themes**: {common threads}

**Skipped**: {topics deemed not journal-worthy}
```

## Quality Gates

- [ ] Atomics are genuine reflections, not just logs
- [ ] Each atomic stands alone (comprehensible without context)
- [ ] Wikilinks connect to related entries
- [ ] Graph connectivity maintained (parent links in body)

## Learning

Track:
- Are daily syntheses read later?
- Which atomics prove valuable over time?
- Optimize for future retrieval value

---

## Execution Log

| Date | Atomics | Themes | Time |
|------|---------|--------|------|
| *Awaiting first execution* | - | - | - |
