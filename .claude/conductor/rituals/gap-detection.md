# Ritual: Gap Detection

**Trigger**: Proactive check (session start, weekly review, explicit request)
**Model**: Sonnet (efficient scanning)
**Duration**: 30-60 seconds

## Purpose

Notice what's missing, stale, or incomplete. Surface gaps before they cause problems.

## Gaps to Detect

### Journal Gaps
```bash
# Check for missing daily entries
ls .claude/journal/2025/12/ | wc -l
# Compare to expected days in month
```

**Threshold**: Alert if >3 consecutive days missing

### Librarian Activity
```bash
# Check last URL catalogue update
git log -1 --format="%ar" -- .claude/library/
```

**Threshold**: Alert if >7 days since last update

### Archivist Metabolism
```bash
# Check last metabolism update
git log -1 --format="%ar" -- .claude/archive/metabolism.md
```

**Threshold**: Alert if >7 days since last update

### Temporal Validation
Check if temporal-validator has run:
- Are there stale facts flagged?
- When was last staleness scan?

**Threshold**: Alert if temporal-validator never invoked

### Plugin Health
```bash
# Check plugin.json for each plugin
# Look for missing skills, broken hooks, etc.
```

**Threshold**: Alert if >50% plugins first-draft

### Git Uncommitted
```bash
git status --short | wc -l
```

**Threshold**: Alert if >10 uncommitted changes

### Agent Dormancy
Review agent registry:
- Which agents haven't been invoked?
- Are dormant agents still relevant?

**Threshold**: Alert if >50% agents dormant

## Output Format

```markdown
## Gap Detection Report

### Critical
| Gap | Days | Impact | Recommendation |
|-----|------|--------|----------------|
| {gap} | {N} | {severity} | {action} |

### Moderate
| Gap | Days | Impact | Recommendation |
|-----|------|--------|----------------|
| {gap} | {N} | {severity} | {action} |

### Minor
- {gap}: {brief note}

### No Issues
- {area}: Current as of {date}
```

## Surfacing Protocol

Present gaps as questions, not demands:
- "I notice the journal gap from Dec 20-24. Worth backfilling?"
- "Librarian hasn't catalogued URLs in 9 days. Relevant resources missed?"
- "Temporal-validator is dormant. Enable staleness checks?"

## Quality Gates

- [ ] Only surface actionable gaps
- [ ] Prioritize by impact (critical > moderate > minor)
- [ ] Offer, don't impose
- [ ] Track which gap alerts are acted upon

## Learning

Track:
- Which gap alerts led to action?
- Which were dismissed as not valuable?
- Adjust thresholds based on user preference

---

## Execution Log

| Date | Gaps Found | Acted Upon | Ignored |
|------|------------|------------|---------|
| *Awaiting first execution* | - | - | - |
