# Ritual: Session End

**Trigger**: Session concluding or explicit request
**Model**: Sonnet (balanced) or Opus (deep synthesis)
**Duration**: 1-2 minutes

## Purpose

Capture what was learned. Update Conductor state. Ensure continuity for next session.

## Steps

### 1. Invoke Archivist (Optional)
If significant work was done, invoke archivist for metabolic observation:
```
Task(archivist): "Observe this session's artifacts and flows"
```

### 2. Check Journal Need
Decide if session warrants journal entry:
- Significant decision made?
- New pattern discovered?
- Milestone reached?
- Reflection needed?

If yes, invoke journal:scribe or create atomic entry.

### 3. Update User Model
Review session for observations about user:
- Communication patterns observed
- Decision style exhibited
- Quality preferences demonstrated
- Energy level noted

Update user-model.md with new observations.

### 4. Update Pulse
Note session outcomes in pulse.md:
- Agents invoked
- Artifacts created/modified
- Coherence assessment changes

### 5. Update Anticipations
Based on session:
- New hypotheses about user interests
- Gaps identified
- Connections noticed
- Value opportunities

### 6. Create Session Log
Write to `sessions/{session-id}.md`:
```markdown
# Session: {id}
**Date**: {date}
**Duration**: {approximate}

## Intent
{What user wanted to accomplish}

## Outcome
{What actually happened}

## Observations
{Patterns, surprises, learnings}

## User Model Updates
{Dimensions affected, confidence changes}

## Next Session
{What to surface, anticipations}
```

### 7. Commit State
```bash
git add .claude/conductor/
git commit -m "[agent:conductor] observe: session synthesis

Session: {id}
Updates: user-model, pulse, anticipations
Learnings: {brief summary}"
```

## Output Format

```
## Session End

**Captured**:
- {what was saved to Conductor state}

**Learned**:
- {observations about user or ecosystem}

**Next Time**:
- {what to surface in next session}
```

## Quality Gates

- [ ] User model updated if observations made
- [ ] Pulse reflects session outcomes
- [ ] Anticipations updated with new hypotheses
- [ ] Session log created if significant
- [ ] State committed to git

## Learning

Track:
- Were session end updates useful in next session?
- What was missed that should have been captured?
- How can synthesis be more efficient?

---

## Execution Log

| Date | Session ID | Updates Made | Time |
|------|------------|--------------|------|
| *Awaiting first execution* | - | - | - |
