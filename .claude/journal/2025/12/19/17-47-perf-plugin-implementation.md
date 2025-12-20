---
id: 2025-12-19-1747
title: "Performance Profiling Plugin Implementation"
type: atomic
created: 2025-12-19T17:47:06
author: claude-opus-4
description: "Created comprehensive perf plugin for Claude Code performance profiling with zero-overhead design"
tags: [plugin-development, performance, profiling, architecture, feature-dev]
parent_daily: [[2025-12-19]]
related: []
---

# Performance Profiling Plugin Implementation

Implemented a complete performance profiling plugin for Claude Code, designed to investigate and address slow startup times observed across the ecosystem.

## Context

The user reported that new Claude Code instances were taking a long time to startup. Initial investigation revealed:

- **243 MB plugin cache** with 11,518 files requiring scanning
- **6+ SessionStart hooks** running on every startup (statusline, temporal, logging, voice, company, dev-tools)
- **Shell scripts with jq** doing JSON parsing on the critical startup path

This prompted the creation of a dedicated plugin to profile, analyze, and recommend optimizations.

## Architecture Decision: Zero Overhead

The key architectural decision was **zero runtime hooks**. This is deliberately ironic—a performance plugin that adds performance overhead would defeat its purpose.

**Design principle**: Observe without interfering.

The plugin:
1. **Reuses existing data** from the logging plugin's JSONL files
2. **Scans filesystem** for cache analysis (mtime-based staleness detection)
3. **Analyzes on-demand** via commands rather than continuous monitoring

This means profiling has **zero cost when inactive** and only incurs overhead when the user explicitly runs `/perf:start`.

## Components Implemented

### Commands (4)

| Command | Purpose |
|---------|---------|
| `/perf:start [name]` | Begin profiling session |
| `/perf:stop` | End session, generate report |
| `/perf:report [id]` | View existing report |
| `/perf:history` | Compare sessions, detect regressions |

### Skills (Master + 3 Sub-skills)

Following the **master skill pattern** for progressive disclosure:

- **profiler**: Guide for running profiling sessions
- **analyzer**: Interpreting performance data, identifying bottlenecks
- **optimizer**: Optimization patterns and recommendations

### Agent (1)

**perf:analyst** - "The Performance Detective"

A data-driven investigator persona that can autonomously analyze profiles, trace root causes, and generate actionable recommendations. Uses Read, Bash, Glob, Grep tools.

### Python Tools (3)

| Tool | Function |
|------|----------|
| `hook_analyzer.py` | Extract hook timings from logging JSONL |
| `cache_analyzer.py` | Analyze cache size, staleness, health |
| `report_generator.py` | Generate markdown performance reports |

### Shared Library

Extracted common utilities to `lib/utils.py` following DRY principle:
- `get_plugin_cache_dir()`
- `get_newest_mtime()`
- `calculate_hook_summary()`
- etc.

## Key Insights

### Investigation Findings

Initial cache analysis revealed:
- **228 MB total cache** (reduced from 243 MB during session)
- **11,605 files** across 33 cached plugins
- **Medium priority**: Cache exceeds 200 MB threshold
- `schedule` and `agentnet` are the largest plugins

### Design Patterns Applied

1. **Master skill pattern**: Prevents skill description truncation
2. **JSONL for data storage**: Append-only, crash-safe
3. **Markdown for reports**: Human-readable, CI-friendly
4. **Agent persona**: "The Detective" archetype for analytical work

### Quality Improvements During Review

Code review identified and fixed:
- Duplicated utility functions (extracted to shared lib)
- Repeated summary calculation logic (single function now)
- Missing error handling in file I/O (added try/except)
- Edge cases in max() with empty lists (explicit length checks)

## Workflow Used

This feature was built using the **feature-dev** plugin's guided workflow:

1. **Phase 1: Discovery** - Understood the problem space
2. **Phase 2: Codebase Exploration** - Launched 3 code-explorer agents in parallel
3. **Phase 3: Clarifying Questions** - Used AskUserQuestion for interactive requirements gathering
4. **Phase 4: Architecture Design** - 2 code-architect agents proposed minimal vs clean approaches
5. **Phase 5: Implementation** - Built 16 files following the hybrid architecture
6. **Phase 6: Quality Review** - code-reviewer and plugin-validator agents
7. **Phase 7: Summary** - This documentation

The entire process demonstrated effective use of the agent ecosystem for complex feature development.

## Files Created

```
plugins/perf/
├── .claude-plugin/plugin.json    # Plugin manifest
├── README.md                     # Documentation
├── agents/analyst.md             # Performance analyst agent
├── commands/{start,stop,report,history}.md
├── lib/{__init__,utils}.py       # Shared utilities
├── skills/perf-master/
│   ├── SKILL.md                  # Master skill
│   └── subskills/{profiler,analyzer,optimizer}.md
└── tools/{hook_analyzer,cache_analyzer,report_generator}.py
```

**Total: 16 files**

## Next Steps

1. Clear plugin cache and restart Claude Code to activate
2. Run initial baseline profile: `/perf:start baseline`
3. Use analyst agent for deep investigation of startup bottlenecks
4. Consider consolidating SessionStart hooks (as statusline did for 3x improvement)

---

*Parent: [[2025-12-19]]*
