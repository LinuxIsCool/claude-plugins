# Statusline Plugin Refactor Plan

## Current Problems
- Over-engineered prompts coupled to this repository
- Unreliable output (showing "C?" and "0m")
- Complex, bloated code without foundational design
- No historical logging for performance analysis
- Fragile and brittle system

## Design Principles (First Principles)

### Names
- **ONE WORD** only
- Intuitively relate to the work being done
- Never change once initialized (unless manually requested)
- Need clear examples that are user-approved

### Descriptions
- **ALWAYS 2 words**: `<Component> <Role>`
- Rarely change - only when session significantly shifts focus
- Stable identity throughout session

### Summary
- Updated on every user submit AND agent stop
- Represents current focus of the session
- Dynamic, reflects immediate work

### Code Quality
- Small, simple, reliable
- Designed intentionally from the ground up
- No bloat, no over-engineering
- Prompts: small, simple, modular, maintainable, generalizable

## Investigation Completed

### Current State Analysis
**Code size**: ~1237 lines total
- `claude_backend.py`: 665 lines (shared library - too large)
- `auto-name.py`: 214 lines
- `auto-description.py`: 187 lines
- `auto-summary.py`: 170 lines

**Data location**: `~/.claude/instances/`
- `registry.json` - main registry
- `descriptions/` - history by session
- `summaries/` - history by session
- No unified log with timestamps

### Statusline Logging Decision

**Recommendation**: Statusline handles own logging (standalone)

**Rationale**:
- Aligns with "compatible and complimentary but standalone" principle
- No dependency on logging plugin
- Simple, single file, append-only
- Logging plugin can optionally index if desired

**Log format**: JSONL (one line per event)
```
{"ts":"2025-12-18T11:00:00Z","session":"a1c04f9d","type":"name","value":"Phoenix","ok":true}
{"ts":"2025-12-18T11:00:01Z","session":"a1c04f9d","type":"description","value":"Statusline Craftsman","ok":true}
{"ts":"2025-12-18T11:00:02Z","session":"a1c04f9d","type":"summary","value":"Working on prompts","ok":true}
```

**Location**: `~/.claude/instances/statusline.jsonl`

**Benefits**:
- Queryable with grep/jq
- Append-only (no corruption risk)
- Single source of truth for history
- Enables performance analysis

## Action Plan

### Phase 1: Implement Statusline Logging (COMPLETE)
**Goal**: Enable historical analysis before making changes

Tasks:
- [x] Add JSONL logging to each hook (name, description, summary)
- [x] Log on UserPromptSubmit and Stop events
- [x] Include: timestamp, session_id, type, value, success/failure
- [x] Single file: `~/.claude/instances/statusline.jsonl`
- [x] Log raw Claude Code input (`claude_input` event type)
- [x] Log complete statusline render with all 15 display values (`statusline_render` event type)

**Implementation**:
- Added `log_statusline_event()` to claude_backend.py, integrated into all 3 hooks
- Added `log_claude_input()` to statusline.sh - captures raw JSON from Claude Code
- Added `log_statusline_state()` to statusline.sh - captures all derived display values

**Event types logged**:
- `session_start` / `session_resume` - from session-start.sh
- `prompt_count` - from user-prompt-submit.sh
- `model` - from statusline.sh (backfill)
- `name` / `description` / `summary` - from Python hooks
- `claude_input` - raw Claude Code JSON
- `statusline_render` - all 15 display values

**Note**: Also fixed critical issue where `lib/` directory was not tracked by git due to .gitignore rule. Added exception `!plugins/*/lib/`.

### Phase 2: Code Review
**Goal**: Understand what we have before changing it

Tasks:
- [ ] Review `claude_backend.py` (665 lines - likely bloated)
- [ ] Review each hook file
- [ ] Identify dead code, over-engineering, coupling
- [ ] Document data flow and dependencies
- [ ] Identify root cause of "C?" and "0m" failures

**Implementation**: Use code-reviewer agent

### Phase 3: Simplify & Refactor
**Goal**: Small, simple, reliable code from ground up

Tasks:
- [ ] Design minimal architecture
- [ ] Remove unnecessary abstraction
- [ ] Simplify prompts (remove repository coupling)
- [ ] Create user-approved name examples
- [ ] Ensure reliability (proper error handling, fallbacks)

### Phase 4: Validate
**Goal**: Prove it works

Tasks:
- [ ] Test all scenarios
- [ ] Analyze logs for quality
- [ ] Get user approval on generated outputs
- [ ] Iterate based on data

## Prompt Requirements (User Approved)

### Name Prompt
- Generate ONE WORD only
- Intuitively relate to work being done
- Need user-approved examples list
- Never changes after initialization

### Description Prompt
- ALWAYS 2 words: `<Component> <Role>`
- Rarely changes (only on significant focus shift)
- Need user-approved examples list

### Summary Prompt
- Updates every UserPromptSubmit and Stop
- Represents current session focus
- Should be clear and specific

## Notes
- Use `/feature-dev` for implementation work
- Consult plugin-dev plugin for architecture decisions
- Plugins should be compatible and complimentary but standalone
- RELIABILITY is non-negotiable - no "C?" or "0m" failures
