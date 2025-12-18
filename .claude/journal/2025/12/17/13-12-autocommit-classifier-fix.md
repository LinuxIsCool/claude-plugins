---
id: 2025-12-17-1312
title: "Autocommit Classifier: Teaching Haiku to Stop Being Helpful"
type: atomic
created: 2025-12-17T13:12:00
author: claude-opus-4
description: "Fixed the autocommit hook by reframing Haiku from helpful assistant to strict classifier, git porcelain parsing bug, and backtick stripping"
tags: [autocommit, haiku, prompt-engineering, classifier, git, debugging]
parent_daily: [[2025-12-17]]
related: [[2025-12-16-autocommit-plugin-born]]
---

# Autocommit Classifier: Teaching Haiku to Stop Being Helpful

## The Problem

The autocommit hook was running on every `UserPromptSubmit`, but Haiku kept failing to produce valid output. The log was full of errors like:

```
ERROR - Unknown decision from Haiku: I need to examine the logs and context...
ERROR - Unknown decision from Haiku: I'll search the recent logs...
ERROR - Unknown decision from Haiku: <function_calls><invok...
```

Haiku was trying to:
1. Reason about the task ("I need to examine...")
2. Take actions ("Let me search...")
3. Call tools (despite having none available)

When all we needed was a binary decision: `COMMIT` or `SKIP`.

## Root Cause Analysis

The original prompt started with:

> "You are an intelligent version control assistant that captures collaborative insights."

This framing triggered Haiku's helpful assistant instincts. The full conversation context (~2000 chars) made it think it was mid-conversation. The output format requirements were buried at the END of a long prompt, easily forgotten by the time Haiku started generating.

## The Fix: Three Changes

### 1. Classifier Framing (Not Assistant)

Changed the prompt opening from "intelligent assistant" to:

```
CLASSIFIER FUNCTION - NOT AN ASSISTANT

You are a commit decision classifier. You output EXACTLY one of two formats. Nothing else.
Do NOT explain. Do NOT use tools. Do NOT ask questions. Just output the format.
```

### 2. Few-Shot Examples

Added 5 concrete examples showing exactly what COMMIT and SKIP responses look like:

```
User: "looks good!"
Files: 3 changed
COMMIT
[auth] add: email validation

Added format validation for email inputs on login form.
...

---

User: "there's still an error"
Files: 2 changed
SKIP: User reports error, work incomplete
```

### 3. `--max-turns 1`

Added to the headless Claude invocation:

```python
"--max-turns",
"1",  # Single turn only - no tool use, no follow-ups
```

This prevents any multi-turn behavior or tool call attempts, even if Haiku tries.

## Bonus Bug: Git Porcelain Parsing

While testing, discovered that files starting with `.` (like `.claude-plugin/marketplace.json`) were losing their leading dot.

**Root cause**: Git porcelain format is `XY PATH` where:
- X = index status (position 0)
- Y = worktree status (position 1)
- PATH = starts at position 2 or 3 depending on Y

When Y is a space (e.g., `M ` for "staged, worktree unchanged"), there's NO additional separator. The space at position 1 doubles as both status and separator.

**Before (broken)**:
```python
filepath = line[3:].strip()  # Always assumed separator at position 2
```

**After (fixed)**:
```python
if len(line) > 2 and line[2] == ' ':
    filepath = line[3:].strip()  # Normal case: separator at position 2
else:
    filepath = line[2:].strip()  # Edge case: Y is space, path at position 2
```

## Fourth Bug: Backtick Contamination (discovered 13:25)

Even after the classifier fixes, commit messages were appearing with markdown code block markers:

```
git log --oneline
bc82452 ``` COMMIT [plugin:autocommit,logging] fix: classifier prompt...
e8d9479 ``` COMMIT [plugin:autocommit,logging] fix: classifier prompt...
```

**Root cause**: Two bugs working together:

1. **Line-oriented stripping assumed separate lines**: The code assumed "```" and "COMMIT" were on separate lines, but Haiku often outputs them on the same line: "``` COMMIT"

2. **Fallback used wrong variable**: Even when stripping worked, the fallback parser returned `response` (original) instead of `cleaned` (stripped)

**Fix**: Handle both backtick patterns:

```python
if cleaned.startswith("```"):
    first_line = cleaned[:first_newline] if first_newline != -1 else cleaned
    after_backticks = first_line[3:].strip()

    if after_backticks:
        # Case 2: "``` COMMIT..." - keep content, remove only backticks
        cleaned = after_backticks + "\n" + cleaned[first_newline + 1:]
    else:
        # Case 1: "```\nCOMMIT..." - remove entire first line
        cleaned = cleaned[first_newline + 1:]
```

And fix the fallback to use `cleaned`:

```python
else:
    if "COMMIT" in cleaned[:50]:  # was: response[:50]
        result["message"] = cleaned  # was: response
```

**Validation**: End-to-end test confirmed clean output:
```
Raw response: 'COMMIT\n[plugin:autocommit] fix: autocommit hook improvements...'
Message first line: [plugin:autocommit] fix: autocommit hook improvements
✓ MESSAGE IS CLEAN
```

## Results

After the fixes:
- `SKIP: User is executing the /logging:obsidian command...` - Proper format!
- Test commit `f2cd7ba` successfully included `.claude-plugin/marketplace.json`
- Backticks properly stripped from commit messages
- End-to-end Haiku test validates clean output

## Key Insights

### On Prompt Engineering for Smaller Models

Haiku (and smaller models generally) need **very explicit framing** to avoid reverting to assistant behavior. The techniques that work:

1. **Negative instructions**: "Do NOT explain. Do NOT use tools."
2. **Role declaration first**: Put "CLASSIFIER" before any context
3. **Examples over rules**: Showing the exact output format is more effective than describing it
4. **Minimal context**: Less conversation history = less confusion

### On Git Porcelain Format

The git documentation describes the format as `XY PATH` but doesn't explicitly mention that when Y is a space, the format becomes `X PATH` (only one space between status and path). This manifests only for:
- Staged files (status `M `)
- Deleted files (status `D `)
- Files with paths starting with `.`

A rare bug that only appears in specific combinations.

### On Debugging Approach

The path to understanding this bug:
1. `git status --porcelain` showed correct output
2. Python parsing showed wrong filepath
3. `repr()` revealed exact character positions
4. `xxd` confirmed byte-level analysis
5. Traced through git status codes to understand the format edge case

Sometimes you need to go all the way down to bytes to understand what's happening.

---

*Parent: [[2025-12-17]]*
