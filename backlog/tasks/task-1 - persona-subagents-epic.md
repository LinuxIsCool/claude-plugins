---
id: task-1
title: "Persona Subagents: Plugin Ambassadors with Persistent Memory"
status: "In Progress"
priority: high
labels: [architecture, personas, memory, infrastructure]
milestone: v1.0-personas-mvp
created: 2025-12-12
assignee: ["@claude"]
---

# Persona Subagents: Plugin Ambassadors with Persistent Memory

## Description

Create intelligent, persistent ambassador subagents for each plugin in the ecosystem. Each persona will:
- Embody their plugin's identity and philosophy
- Maintain long-term memory across conversations
- Have full knowledge of their plugin's capabilities and trajectory
- Collaborate with other personas via standardized protocols

This is the parent epic for all persona-related work.

## Background

### The Ten Personas

| Persona | Plugin | Archetype |
|---------|--------|-----------|
| The Archivist | logging | Historian / Keeper of Records |
| The Mentor | awareness | Teacher / Guide to Self-Improvement |
| The Explorer | exploration | Scientist / Environmental Cartographer |
| The Scribe | journal | Reflective Practitioner / Knowledge Curator |
| The Coordinator | schedule | Time Manager / Preference Learner |
| The Organizer | backlog | Project Manager / Task Orchestrator |
| The Synthesizer | brainstorm | Creative Thinker / Idea Weaver |
| The Architect | agents | Systems Builder / Framework Expert |
| The Scholar | llms | Researcher / Knowledge Systematizer |
| The Cartographer | knowledge-graphs | Relationship Mapper / Semantic Navigator |

### Architectural Decision Pending

Two approaches are under consideration:

1. **External Infrastructure Approach** (task-1.1)
   - Letta (MemGPT) for self-editing memory blocks
   - Mem0 for automatic fact extraction
   - Graphiti + FalkorDB for temporal knowledge graphs
   - A2A protocol for inter-agent communication

2. **Markdown-Native Approach** (task-1.2)
   - Memory stored as markdown files with YAML frontmatter
   - Wikilinks for knowledge graph relationships
   - Temporal hierarchy (daily → monthly → permanent)
   - Zero external dependencies

See decision record: [[ADR-001-persona-memory-architecture]]

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Architecture decision documented with rationale
- [ ] #2 Standard infrastructure schema defined
- [ ] #3 One persona fully implemented as prototype
- [ ] #4 Memory persistence validated across sessions
- [ ] #5 All ten personas have identity definitions
- [ ] #6 Inter-persona communication pattern established
- [ ] #7 Integration with logging plugin confirmed
- [ ] #8 Documentation complete for persona development
<!-- AC:END -->

## Subtasks

- [[task-1.1]] - Evaluate External Infrastructure Approach
- [[task-1.2]] - Evaluate Markdown-Native Approach
- [[task-1.3]] - Define Standard Infrastructure Schema
- [[task-1.4]] - Implement Prototype Persona (The Archivist)
- [[task-1.5]] - Create Identity Definitions for All Personas
- [[task-1.6]] - Implement Inter-Persona Communication
- [[task-1.7]] - Documentation and Developer Guide

## Related Documents

- [[PERSONA_SUBAGENTS_STRATEGY.md]] - Original strategy document
- [[.claude/storms/2025-12-12.md]] - Brainstorm on holistic alignment
- [[ADR-001-persona-memory-architecture]] - Architecture decision record

## Implementation Notes

Research phase complete. Team consultation via brainstorm revealed strong preference for markdown-native approach to maintain philosophical consistency with existing plugins.
