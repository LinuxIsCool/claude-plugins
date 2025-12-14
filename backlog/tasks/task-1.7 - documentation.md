---
id: task-1.7
title: "Documentation and Developer Guide"
status: "To Do"
priority: medium
labels: [documentation]
milestone: v1.0-personas-mvp
parentTaskId: task-1
dependencies: [task-1.4, task-1.5, task-1.6]
created: 2025-12-12
assignee: ["@claude"]
---

# Documentation and Developer Guide

## Description

Create comprehensive documentation for the persona subagent system, enabling others to:
- Understand the architecture and philosophy
- Create new personas
- Extend existing personas
- Debug persona behavior

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Architecture overview document
- [ ] #2 "Creating a New Persona" guide
- [ ] #3 Schema reference documentation
- [ ] #4 Memory management best practices
- [ ] #5 Inter-persona communication guide
- [ ] #6 Troubleshooting guide
- [ ] #7 API/tool reference for persona interaction
- [ ] #8 Example workflows documented
<!-- AC:END -->

## Documentation Structure

```
plugins/personas/
├── README.md                    # Overview and quick start
├── docs/
│   ├── architecture.md          # System design
│   ├── creating-personas.md     # Step-by-step guide
│   ├── schemas.md               # Format reference
│   ├── memory-management.md     # Memory patterns
│   ├── communication.md         # Inter-persona patterns
│   ├── troubleshooting.md       # Common issues
│   └── examples/
│       ├── simple-persona.md
│       └── advanced-patterns.md
└── CHANGELOG.md                 # Version history
```

## Key Topics to Cover

### Architecture Overview
- Philosophy: Markdown-native, zero dependencies
- Memory hierarchy: Core → Recent → Permanent
- Progressive disclosure pattern
- Integration with logging plugin
- Wikilinks as knowledge graph

### Creating a New Persona
1. Choose archetype and plugin association
2. Create directory structure
3. Write identity.md
4. Set up memory directories
5. Create skill for invocation
6. Test and iterate

### Schema Reference
- identity.md required/optional fields
- state.md structure
- Memory entry format
- Shared state conventions
- Wikilink naming patterns

### Memory Management
- When to create memories
- Confidence scoring
- Temporal organization
- Memory consolidation (daily → permanent)
- Forgetting/archiving patterns

### Inter-Persona Communication
- Wikilink references
- Shared state coordination
- Handoff protocols
- Broadcast patterns

## Implementation Notes

Documentation should follow the same markdown-native philosophy as the personas themselves. Use wikilinks within docs for cross-referencing.
