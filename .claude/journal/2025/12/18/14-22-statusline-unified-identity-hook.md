---
id: 2025-12-18-1422
title: "Statusline Unified Identity Hook"
type: atomic
created: 2025-12-18T14:22:53
author: claude-opus-4
description: "Consolidated 3 statusline hooks into 1, fixing system freezes and enabling versioned prompt engineering"
tags: [statusline, hooks, performance, refactoring, prompt-engineering]
parent_daily: [[2025-12-18]]
related: []
---

# Statusline Unified Identity Hook

Major refactoring of the statusline plugin's identity generation system, consolidating three separate hooks into one unified hook for 3x performance improvement.

## Context

The statusline plugin generates three identity elements for each Claude session:
- **Name**: Symbolic 1-2 word callsign (e.g., "Oracle", "Meridian")
- **Description**: Grounded role descriptor (e.g., "Statusline Craftsman")
- **Summary**: Current work in 5-10 words (e.g., "Refactoring hook race conditions")

Previously, each element had its own hook (`auto-name.py`, `auto-description.py`, `auto-summary.py`), each spawning a separate subprocess to call the Claude API.

## Problems Solved

### 1. System Freeze (15+ seconds)
Three concurrent subprocess spawns caused resource contention. Opening a new Claude session would freeze the system for 15+ seconds as all three hooks competed for resources with 30-second timeouts.

**Solution**: Consolidated into single `auto-identity.py` hook that makes ONE API call returning all three values as JSON.

### 2. Data Corruption
The auto-register function in `statusline.sh` was overwriting existing session data instead of preserving it. Sessions would lose their names and timestamps.

**Solution**: Fixed jq filter to use `(.name // "Claude")` pattern to preserve existing values.

### 3. Prompt Inference Bug
Identity generation was inferring work from the directory path rather than the user's actual message. Saying "Hello" would result in "Plugin Development Statusline Scribe" based on the CWD.

**Solution**: Updated prompts with explicit "Do NOT infer from directory path" guidance and fallback rules for greetings/tests.

## Technical Implementation

### Unified Hook Architecture
```
hooks/auto-identity.py
  └─> Single API call with JSON output format
      └─> Parses: {"name":"X","description":"Y","summary":"Z"}
          └─> Saves to respective locations
```

### Key Changes to `lib/claude_backend.py`
- Added `multiline=True` parameter to `generate_with_backend()` and `_generate_headless()`
- Previously only returned first line (for single values); now can capture full JSON response

### Versioned Prompt System
Refactored `build_combined_prompt()` to load from versioned files:
```
prompts/
├── config.yaml           # Maps element → active version
├── name/
│   └── 1_ecosystem_aware.md
├── description/
│   └── 1_plugin_role.md
└── summary/
    └── 1_feature_level.md
```

Template variables (`{user_prompt}`, `{agent_name}`, `{context}`, etc.) are filled via Python's `.format()`.

## Commits

1. `[plugin:statusline] fix: preserve existing data in auto-register`
2. `[plugin:statusline] feat: unified identity hook (3x performance)`
3. `[plugin:statusline] fix: prompt inference from directory path`
4. `[plugin:statusline] cleanup: remove old unused hooks and prompts`
5. `[plugin:statusline] refactor: load prompts from versioned files`

## Future Work

- Iterate on prompt quality (description stability, summary informativeness)
- Create version 2 prompts based on observed behavior
- Consider adding `references_date` pattern for temporal grounding in prompts

---

*Parent: [[2025-12-18]]*
