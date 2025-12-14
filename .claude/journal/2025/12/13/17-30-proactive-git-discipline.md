---
id: 2025-12-13-1730
title: "Proactive Git Discipline"
type: atomic
created: 2025-12-13T17:30:00
author: claude-opus-4
description: "Established proactive commit discipline: enhanced conventions, commit plan for 50+ files, agent commit rituals"
tags: [git, coordination, discipline, commits, proactive, agents]
parent_daily: [[2025-12-13]]
related:
  - [[17-00-archivist-awakens]]
  - [[16-40-git-coordination-conventions]]
  - [[16-56-git-historian-born]]
---

# Proactive Git Discipline

The shift from reactive batching to proactive commit discipline.

## The Question

User asked: "How can we best have agents proactively use git in a way that creates the most coherence across the repository?"

This triggered a fundamental rethinking of git usage: from passive storage to active coordination layer.

## The Shift

| Before (Reactive) | After (Proactive) |
|-------------------|-------------------|
| Work accumulates | Commit immediately |
| Batch commit later | One semantic unit per commit |
| History is coarse | History is rich |
| Commits as storage | Commits as communication |
| No attribution | Session + Agent in every commit |

## What We Built

### 1. Enhanced Coordination Conventions

Added to `.claude/conventions/coordination.md`:
- **Proactive Commit Discipline** section
- When to commit (triggers)
- Semantic unit definition
- Agent commit ritual
- Session-commit correlation format
- Multi-session coordination
- Commit quality metrics
- Commit plan template

### 2. Commit Plan for Current Batch

Created `.claude/planning/2025-12-13-commit-plan.md`:
- Analyzed 50+ uncommitted files
- Grouped into 20 semantic commits
- Provided exact commands for each
- Established attribution pattern

### 3. Agent Commit Rituals

Added "Your Commit Discipline" sections to:
- **agent-architect** - Commits registry updates
- **archivist** - Commits observations
- **git-historian** - Commits analyses

Each agent now knows:
- When to commit their work
- What format to use
- Why it matters

## Core Principles

### 1. Commits Are Communication

Every commit is a message to:
- Future sessions (context)
- Parallel sessions (coordination)
- The git-historian (analysis)
- Human operators (oversight)

### 2. The Session-Commit Correlation

```
Session: 2025-12-13-15-13-03-6bcca543
Agent: archivist
Intent: First metabolic observation
```

This links conversations to code changes, enabling reconstruction of why changes happened.

### 3. Semantic Units

One sentence = one commit.

Good: "Add archivist agent definition"
Bad: "Add agents, update conventions, fix typos"

### 4. Don't Wait

The proactive rule: After completing a meaningful unit of work:
1. Stage changes
2. Commit with rich message
3. Verify
4. Continue

### 5. Agents Commit Their Own Work

Agents are not passive—they commit. When the archivist finishes an observation, it commits. When the git-historian finishes analysis, it commits.

## The Commit Graph Vision

```
Session A ──invokes──→ Agent Architect ──commits──→ registry/
    │
    └──invokes──→ Process Cartographer ──commits──→ processes/

Session B ──invokes──→ Archivist ──commits──→ archive/
```

Each commit is attributable. The git-historian can trace lineage.

## Impact

| Before | After |
|--------|-------|
| ~30 uncommitted files | Structured commit plan |
| No attribution | Session + Agent in messages |
| Agents observe git | Agents participate in git |
| Coarse history | Rich, queryable history |

## Going Forward

From this point:
- **Commit immediately** after completing work
- **Include session ID** in every commit
- **Never accumulate** more than 1 day of changes
- **Agents commit** their own outputs

The ecosystem now has a git discipline that matches its ambition for self-awareness.

---

*Parent: [[2025-12-13]] → [[2025-12]] → [[2025]]*
