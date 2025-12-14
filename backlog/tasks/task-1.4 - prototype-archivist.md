---
id: task-1.4
title: "Implement Prototype Persona: The Archivist"
status: "To Do"
priority: high
labels: [implementation, personas]
milestone: v1.0-personas-mvp
parentTaskId: task-1
dependencies: [task-1.3]
created: 2025-12-12
assignee: ["@claude"]
---

# Implement Prototype Persona: The Archivist

## Description

Implement The Archivist as the first prototype persona. This persona is the natural choice for prototype because:

1. **Foundational**: All other personas depend on logging for memory source
2. **Clear scope**: Well-defined capabilities (search, recall, pattern finding)
3. **Integration point**: Validates logging plugin integration
4. **Observable**: Easy to verify memory persistence through log inspection

## The Archivist Profile

| Attribute | Value |
|-----------|-------|
| Name | The Archivist |
| Plugin | logging |
| Archetype | Historian / Keeper of Records |
| Core Value | "Every moment matters. Full fidelity, never truncate." |
| Voice | Meticulous, thorough, trustworthy, quiet authority |

### Capabilities
- Search conversation history (log-search skill)
- Session reconstruction and timeline building
- Pattern identification across time
- Context recall for other personas

### Personality Traits
- Values completeness over convenience
- Uncomfortable with data loss or truncation
- Finds meaning in preserving history
- Speaks with precision about past events

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Create `.claude/personas/archivist/identity.md`
- [ ] #2 Create `.claude/personas/archivist/state.md`
- [ ] #3 Create memory directory structure
- [ ] #4 Implement persona skill for invocation
- [ ] #5 Validate integration with logging plugin
- [ ] #6 Test memory persistence across sessions
- [ ] #7 Verify progressive disclosure pattern works
- [ ] #8 Document invocation patterns
<!-- AC:END -->

## Implementation Plan

### Phase 1: Identity and Structure
1. Create directory structure
2. Write identity.md with full personality definition
3. Create initial state.md
4. Set up memory directories

### Phase 2: Skill Integration
1. Create `plugins/personas/skills/archivist/SKILL.md`
2. Define when the persona should be invoked
3. Set allowed tools (Read, Grep, Glob for memory access)
4. Test skill discovery

### Phase 3: Logging Integration
1. Define how Archivist reads from `.claude/logging/`
2. Define how Archivist writes synthesized memories
3. Test search across log history
4. Validate JSONL parsing

### Phase 4: Memory Persistence
1. Simulate multi-session interaction
2. Verify memories persist between sessions
3. Test memory retrieval accuracy
4. Validate temporal queries

## Test Scenarios

### Scenario 1: Basic Recall
```
User: "What did we discuss yesterday about authentication?"
Archivist: [searches logs, synthesizes answer, optionally records learning]
```

### Scenario 2: Pattern Recognition
```
User: "What topics come up most often in our conversations?"
Archivist: [analyzes log history, identifies patterns, reports]
```

### Scenario 3: Memory Recording
```
User: "Remember that I prefer TypeScript over JavaScript"
Archivist: [creates memory entry, confirms storage]
```

### Scenario 4: Cross-Session Continuity
```
Session 1: User mentions preference
[Session ends]
Session 2: Archivist recalls preference without prompting
```

## Success Metrics

| Metric | Target |
|--------|--------|
| Memory recall accuracy | >90% |
| Search latency | <2 seconds |
| Identity consistency | 100% (never breaks character) |
| Session continuity | Memory persists across restarts |

## Implementation Notes

The Archivist prototype will validate the entire persona infrastructure. Success here means the pattern can be replicated for other personas.
