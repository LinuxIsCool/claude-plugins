# Ritual: Session Start

**Trigger**: New session begins (SessionStart hook or Conductor invocation)
**Model**: Haiku (lightweight) or Opus (full briefing)
**Duration**: <30 seconds (Haiku) or 1-2 minutes (Opus)

## Purpose

Provide context continuity. Help user pick up where they left off. Surface anything that needs attention.

## Lightweight Mode (Haiku)

Used by SessionStart hook for every session.

### Steps
1. Check git log for commits since last session
2. Scan pulse.md for critical updates
3. Output 1-2 sentence context

### Output Format
```
[Context: {brief summary}. {proactive if any}]
```

### Example
```
[Context: 5 commits since last session. Conductor infrastructure created. Ready to test.]
```

## Full Briefing Mode (Opus)

Used when Conductor is explicitly invoked at session start.

### Steps
1. Load user-model.md (understand the human)
2. Check git log -20 for recent activity
3. Review pulse.md for ecosystem state
4. Check anticipations.md for proactive opportunities
5. Scan .claude/briefings/ for agent communications
6. Check journal for recent entries

### Output Format
```
## Session Briefing

**Since Last Session**:
- {commits, changes, activity}

**Ecosystem Pulse**:
- {active/dormant, health, concerns}

**Anticipations**:
- {proactive suggestions, gaps noticed}

**Question**: What wants to happen today?
```

## Quality Gates

- [ ] Briefing is concise (not overwhelming)
- [ ] Only surfaces actionable information
- [ ] Questions > assertions
- [ ] Calibrated to user energy

## Learning

Track effectiveness:
- Did briefing content prove useful?
- Was anything missed that should have been surfaced?
- Was anything surfaced that wasn't valuable?

Update this ritual based on learnings.

---

## Execution Log

| Date | Mode | Duration | Feedback |
|------|------|----------|----------|
| *Awaiting first execution* | - | - | - |
