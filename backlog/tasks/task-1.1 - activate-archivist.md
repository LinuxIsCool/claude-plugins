---
id: task-1.1
title: "Activate Archivist Agent"
status: "To Do"
priority: high
labels: [activation, agents]
milestone: v1.0-activation
parentTaskId: task-1
created: 2025-12-15
assignee: ["@claude"]
---

# Activate Archivist Agent

## Description

The Archivist agent is **fully defined** at `.claude/agents/archivist.md` but has never been invoked. This task activates the agent to begin artifact observation.

### Current State

- **Agent definition**: Complete (309 lines, opus model)
- **Infrastructure**: `.claude/archive/` directory exists
- **Process**: Process 6 (Artifact Observation) documented
- **Status**: DORMANT - never invoked

### Agent Responsibilities (from definition)

1. **Metabolic Mapping** - Track what flows through the system
2. **Coherence Maintenance** - Ensure system makes sense as a whole
3. **Pattern Recognition** - Surface non-obvious patterns
4. **Gap Detection** - Identify what's missing
5. **Historical Reconstruction** - Answer questions about the past

### Expected Outputs

```
.claude/archive/
├── metabolism.md           # Current metabolic state
├── patterns/
│   ├── temporal.md         # Time-based patterns
│   ├── topical.md          # Theme clusters
│   └── agent-activity.md   # Agent behavior patterns
├── coherence/
│   ├── gaps.md             # What's missing
│   └── contradictions.md   # What conflicts
└── history/
    └── {date}-snapshot.md  # Periodic snapshots
```

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Invoke archivist agent via Task tool
- [ ] #2 Archivist creates initial metabolism.md
- [ ] #3 Archivist scans .claude/logging/ and produces observations
- [ ] #4 Archivist commits its work to git
- [ ] #5 Archivist produces at least one pattern observation
- [ ] #6 Update registry to show archivist as "Active"
<!-- AC:END -->

## Activation Steps

### Step 1: Invoke the Archivist
```
Use Task tool with:
- subagent_type: general-purpose (or custom if supported)
- Load .claude/agents/archivist.md as system prompt context
- Prompt: "You are the Archivist. Begin your work. Start by creating metabolism.md with the current state of the ecosystem."
```

### Step 2: Verify Outputs
- Check `.claude/archive/metabolism.md` created
- Verify meaningful observations captured
- Check git commit with proper format

### Step 3: Update Registry
Edit `.claude/registry/agents.md` to change archivist from dormant to active.

## Notes

The archivist definition includes:
- Git observation patterns (specific bash commands)
- Commit conventions (`[agent:archivist] action: description`)
- Collaboration patterns with other agents
- The "metabolic view" framework

This is not about building the agent - it's about **invoking what's already built**.
