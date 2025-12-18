---
id: 2025-12-17-1848
title: "Git-Flow Plugin: Worktree-Based Multi-Agent Coordination"
type: atomic
created: 2025-12-17T18:48:32
author: claude-opus-4
description: "Built complete git-flow plugin for per-session worktrees, feature branches, and PR automation. 20 source files, design philosophy on plugin independence."
tags: [git-flow, worktrees, multi-agent, plugin-architecture, design-philosophy, feature-dev]
parent_daily: [[2025-12-17]]
related:
  - [[13-12-autocommit-classifier-fix]]
---

# Git-Flow Plugin: Worktree-Based Multi-Agent Coordination

## What Was Built

A complete plugin enabling **per-session git worktrees** for isolated multi-agent development.

### The Problem

When multiple Claude instances work on the same repository:
- Changes can conflict
- Hard to trace which session made what changes
- No isolation between concurrent work
- Protected branches (main, develop) at risk

### The Solution

Each Claude session operates in an **isolated git worktree**:
- Worktrees stored in `.git/worktrees/{branch-name}/`
- Branch naming: `feature/{agent-name}-{session-id}-{title}`
- Changes don't affect main repo until PR merged
- Registry tracks session→worktree mappings

## Plugin Architecture (20 files)

```
plugins/git-flow/
├── .claude-plugin/plugin.json     # Hooks: SessionStart, PreToolUse, Stop
├── agents/branch-manager.md       # Task tool subagent
├── commands/
│   ├── feature.md                 # PRIMARY: branch + feature-dev workflow
│   ├── branch-create.md           # Just create branch
│   ├── branch-status.md
│   ├── pr-create.md
│   ├── worktree-list.md
│   └── worktree-cleanup.md
├── hooks/
│   ├── session-start.sh           # Detect worktree context
│   ├── pre-tool-use.py            # Block Write/Edit on protected branches
│   └── stop.py                    # Suggest PR on session end
├── skills/git-flow-master/        # Master skill + 4 subskills
└── tools/
    ├── registry.py                # Session→worktree CRUD
    ├── worktree.py                # Git worktree operations
    ├── branch.py                  # Branch naming + Haiku generation
    └── pr.py                      # GitHub PR via gh CLI
```

## Design Philosophy Discussion

### The Question: Should plugins be tightly integrated?

User asked about auto-branching when `/feature-dev` is invoked. This led to important architectural discussion.

### The Answer: Independence via Awareness

**Plugins should be like UNIX tools:**
- Each does one thing well
- Can be combined, but don't depend on each other
- Claude (not code) decides when to use them together

**Integration happens through:**
1. **Awareness** - Skills guide Claude to use tools together when appropriate
2. **Composable commands** - `/git-flow:feature` combines branching + feature-dev
3. **Graceful degradation** - Falls back to defaults when optional features unavailable

### Coupling Assessment

| Dependency | Required? | Fallback |
|------------|-----------|----------|
| Git | Yes | Core functionality |
| `gh` CLI | PR features only | Clear error |
| Statusline | No | Defaults to "claude" |
| Autocommit | No | Manual commits |

Renamed docs section from "Integration Points" to "Complementary Plugins (Optional)" to clarify independence.

## Bug Workaround: Issue #5597

Discovered and worked around a Claude Code bug where commands with optional-only arguments lose user input.

**The bug**: [GitHub #5597](https://github.com/anthropics/claude-code/issues/5597) - MCP prompts with only optional arguments require at least one character to invoke.

**The workaround**: `/git-flow:feature` explicitly validates `$ARGUMENTS` exists and instructs Claude to "STOP immediately" if empty, with usage example.

## Key Innovation: `/git-flow:feature`

A combined workflow command that:
1. Creates isolated worktree + feature branch
2. Proceeds directly into feature-dev workflow phases
3. Includes explicit argument validation (bug workaround)
4. Reminds about PR creation when complete

```bash
/git-flow:feature Add OAuth authentication to user settings
```

## Insights

### On Multi-Agent Coordination

> Git is the coordination layer. Worktrees provide isolation. Branches provide traceability. PRs provide quality gates. No complex protocols needed.

### On Plugin Architecture

> The UNIX philosophy applies: small, focused tools that can be composed. Integration through awareness (Claude's judgment) rather than code coupling.

### On Bug Workarounds

> When platform bugs exist, design around them explicitly. "STOP immediately if empty" is more robust than hoping the bug gets fixed.

---

*Parent: [[2025-12-17]] → [[2025-12]] → [[2025]]*
