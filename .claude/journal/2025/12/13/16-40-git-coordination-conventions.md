---
id: 2025-12-13-1640
title: "Git Coordination Conventions"
type: atomic
created: 2025-12-13T16:40:00
author: claude-opus-4
description: "Formalized git as the inter-agent coordination layer with conventions, namespace ownership, and commit message standards"
tags: [git, coordination, conventions, architecture, emergence, agents]
parent_daily: [[2025-12-13]]
related:
  - [[15-15-agent-architecture-emerges]]
  - [[16-15-bootstrapping-trajectory]]
---

# Git Coordination Conventions

Formalized the emergent pattern of git-based inter-agent coordination into explicit conventions.

## Context

Earlier today, we discovered that parallel sessions had been coordinating through git and the filesystem without any explicit protocol. One session created agents and commands; another did strategic planning. Neither knew about the other until the filesystem revealed it.

The insight: **git is already a coordination layer**. We were over-engineering.

## What We Formalized

### 1. Constitutional Acknowledgment (CLAUDE.md)

Added to the top of CLAUDE.md:
```markdown
# Coordination

**Git is the inter-agent coordination layer.** Agents coordinate through
observable file changes, not complex protocols.

- **Write** to your designated namespace
- **Read** from anywhere
- **Commit** with structured messages: `[scope] action: description`
- **Observe** git log for ecosystem activity

See `.claude/conventions/coordination.md` for full patterns.
```

### 2. Coordination Conventions Document

Created `.claude/conventions/coordination.md` containing:
- Commit message format: `[scope] action: description`
- Namespace ownership table (who writes where)
- Observation patterns (git commands for awareness)
- Conflict prevention strategies
- Information flow patterns (broadcast, narrowcast, observe)
- Bootstrap protocol for new sessions

### 3. Agent Architect Enhancement

Added "Git as Coordination Layer" section with:
- Ecosystem pulse observation responsibility
- Convention monitoring without policing
- Agent activity tracking via git
- Drift detection patterns
- Partnership with Archivist

### 4. Archivist Enhancement

Added "Git as Primary Observation Channel" section with:
- Git as source of truth
- Specific observation commands
- Healthy vs warning signals
- Feeding observations to Agent Architect

## The Key Principle

**Conventions > Protocols**

Rather than building complex inter-agent communication infrastructure, we:
1. Acknowledged what already works (git + filesystem)
2. Made it explicit (conventions document)
3. Assigned responsibility (Agent Architect, Archivist)
4. Ensconced it at the constitutional level (CLAUDE.md)

## The Hierarchy

```
CLAUDE.md (constitutional)
    ↓
.claude/conventions/coordination.md (detailed patterns)
    ↓
Agent Architect (enforces coherence)
    ↓
Archivist (observes flows)
    ↓
All Agents (follow conventions)
```

## Commit Message Format

```
[scope] action: description

Scopes: agent:{name}, plugin:{name}, system, journal, planning, registry
Actions: create, update, observe, synthesize, archive, refactor
```

## Insight

The best infrastructure is the infrastructure you don't have to build. Git already provides:
- Persistence
- Ordering
- Observability
- Annotation
- Atomicity

We just needed to recognize it and use it deliberately.

---
*Parent: [[2025-12-13]]*
