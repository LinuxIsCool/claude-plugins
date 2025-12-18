# Generation Tuner Sub-Skill

Iterate on and improve the AI-generated names, summaries, and descriptions that appear in the statusline.

## Architecture Overview

The statusline plugin runs three AI generation hooks on every user prompt:

| Generator | Purpose | Hook | Prompt Template |
|-----------|---------|------|-----------------|
| **Name** | Creative 1-2 word session identity | `auto-name.py` | `prompts/name.txt` |
| **Summary** | 5-10 word first-person activity | `auto-summary.py` | `prompts/summary.txt` |
| **Description** | 2-5 word session arc/role | `auto-description.py` | `prompts/description.txt` |

All three use shared infrastructure in `lib/claude_backend.py`.

## Prompt Templates

### Name Template Variables

| Variable | Source | Example |
|----------|--------|---------|
| `{user_prompt}` | First user message (500 chars) | "Help me fix the login bug in auth.py" |

**Quality goal:** Evocative 1-2 word callsigns that hint at session purpose.

### Summary Template Variables

| Variable | Source | Example |
|----------|--------|---------|
| `{agent_name}` | Session name from registry | "Navigator" |
| `{prev_summaries}` | Last 3 summaries (history) | "Debugging auth flow\nRefactoring database" |
| `{context}` | Last 6 user/assistant messages | "User: Fix the bug\nAssistant: I found..." |

**Quality goal:** Action-oriented first-person statements showing current work.

### Description Template Variables

| Variable | Source | Example |
|----------|--------|---------|
| `{agent_name}` | Session name from registry | "Phoenix" |
| `{first_prompts}` | First 5 user prompts (origin anchor) | "User: Help me redesign..." |
| `{recent_prompts}` | Last 20 user prompts (trajectory) | "User: Now fix the tests..." |
| `{prev_descriptions}` | Last 10 descriptions (arc continuity) | "Database migration guide" |
| `{prev_summaries}` | Last 10 summaries (activity log) | "Running test suite..." |
| `{recent_response}` | Latest Claude response (500 chars) | "I've identified the issue..." |

**Quality goal:** Role/title capturing the session journey, not just current task.

## Iteration Workflow

### Step 1: Identify Quality Issue

Read current prompts to understand what's being asked:

```bash
cat plugins/statusline/prompts/name.txt
cat plugins/statusline/prompts/summary.txt
cat plugins/statusline/prompts/description.txt
```

### Step 2: Preview Filled Prompt

Use test harness to see exactly what the model receives:

```bash
cd plugins/statusline
./tools/test-prompts.py name --preview --user-prompt "Help me debug authentication"
./tools/test-prompts.py summary --preview --agent-name "Navigator" --context "User: Fix the bug"
./tools/test-prompts.py description --preview --session <session_id>
```

### Step 3: Test with Real API

```bash
# Using synthetic data
./tools/test-prompts.py name --user-prompt "Refactor the database layer"

# Using real session data
./tools/test-prompts.py summary --session <session_id>
./tools/test-prompts.py description --session <session_id>
```

### Step 4: Observe in Production

Enable debug output to see prompts during real sessions:

```bash
DEBUG_NAME=1 claude        # Name generation
DEBUG_SUMMARY=1 claude     # Summary generation
DEBUG_DESCRIPTION=1 claude # Description generation
```

### Step 5: Edit and Re-test

Edit templates in `prompts/` directory, then repeat steps 2-4.

## Generation Parameters

| Generator | max_tokens | temperature | Model |
|-----------|------------|-------------|-------|
| Name | 20 | 0.7 | claude-haiku-4-5 |
| Summary | 50 | 0.3 | claude-haiku-4-5 |
| Description | 30 | 0.3 | claude-haiku-4-5 |

Higher temperature for names (creativity), lower for summaries/descriptions (consistency).

## Common Quality Issues

### Name Generator

| Issue | Symptom | Fix |
|-------|---------|-----|
| AI outputs "Claude" | 23 sessions named exactly "Claude" | Add CRITICAL RULE: "NEVER use Claude or Assistant" |
| Too generic | "Helper", "Assistant" | Add examples of evocative names in prompt |
| Too long | "Database Migration Helper" | Emphasize 1-2 word limit |
| Short prompts fail | "Hello", "Test" → default names | Add fallback guidance for minimal prompts |
| Literal slash commands | "/status" → "Status" | Add rule: "NEVER use exact command name" |

#### Real Iteration Example (Dec 2025)

**Problem**: Dataset analysis showed 23 sessions named "Claude" and short prompts getting default names.

**Before** (original prompt):
```
Based on this user's first message, generate a creative 1-2 word name for this Claude session.
```

**After** (improved prompt):
```
CRITICAL RULES:
- NEVER use "Claude" or "Assistant" as the name
- NEVER use the exact command name (e.g., don't output "Status" for "/status")
- For minimal prompts like "Hello" or "Test", use evocative names like "Companion", "Explorer"
```

**Results**:
| Prompt | Before | After |
|--------|--------|-------|
| "Hello" | "Claude-{id}" | "Companion" |
| "/status" | "Status" | "Pulse Monitor" |
| "Can you version control?" | "Claude-{id}" | "Checkpoint" |

### Summary Generator

| Issue | Symptom | Fix |
|-------|---------|-----|
| Third person | "Claude is working on..." | Emphasize first-person in prompt |
| Too vague | "Working on things" | Ask for specific details |
| Repetitive | Same summary every time | Include prev_summaries for variety |

### Description Generator

| Issue | Symptom | Fix |
|-------|---------|-----|
| Too transient | Matches current task only | Emphasize "lifetime arc" concept |
| Doesn't evolve | Same description forever | Include more trajectory context |
| Too verbose | Full sentences | Enforce "2-5 word title" format |

## Backend Selection

The generation system supports two backends:

| Backend | Pros | Cons | Config |
|---------|------|------|--------|
| `api` | Fast (~1s), reliable | Costs API credits | `SUMMARY_BACKEND=api` |
| `headless` | Free (Max subscription) | Slower (~5s), can timeout | `SUMMARY_BACKEND=headless` |

Configure in `~/.claude/statusline.conf`:
```
BACKEND=api
```

## Testing with Session Data

Load real conversation context from an existing session:

```bash
# Find session IDs
ls ~/.claude/instances/registry.json | xargs cat | jq 'keys'

# Test with that session's actual data
./tools/test-prompts.py description --session abc12345 --cwd /path/to/project
```

## Prompt Engineering Tips

1. **Be explicit about format** - "Write ONLY X words, nothing else"
2. **Provide examples** - Show 3-5 examples of good outputs
3. **Use role anchoring** - "You are {agent_name}" helps with voice
4. **Context ordering** - Put most relevant context last (recency bias)
5. **Negative examples** - "Do NOT write..." can prevent common errors

## Building Datasets for Analysis

Quality improvement requires data. Here's how to build datasets:

### Session-Name-Prompt Dataset

```python
# Correlate sessions with their names and first prompts
# Data sources:
# - Registry: ~/.claude/instances/registry.json (names)
# - Logs: .claude/logging/YYYY/MM/DD/*.jsonl (prompts)

# Key analysis:
for session in registries:
    name = session.get("name")
    first_prompt = find_first_prompt(session_id)  # From logs
    is_creative = not name.startswith("Claude-")
    # Track: prompt → name → quality
```

### Analysis Questions

1. **What prompts produce default names?** → Fix with better fallback guidance
2. **What prompts produce literal echoes?** → Add NEVER rules
3. **What's the consistency for same inputs?** → Identify timeout/race issues

### Dataset Location

After running analysis:
```bash
# Full JSON dataset
cat /tmp/naming_dataset.json

# Quick summary
python3 -c "import json; d=json.load(open('/tmp/naming_dataset.json')); print(f'Total: {len(d)}, Creative: {sum(1 for x in d if x[\"is_creative\"])}')"
```

## Files Reference

```
plugins/statusline/
├── prompts/
│   ├── name.txt          # Name generation prompt template
│   ├── summary.txt       # Summary generation prompt template
│   ├── description.txt   # Description generation prompt template
│   └── README.md         # Variable documentation
├── hooks/
│   ├── auto-name.py      # Name generation hook
│   ├── auto-summary.py   # Summary generation hook
│   └── auto-description.py # Description generation hook
├── lib/
│   └── claude_backend.py # Shared generation infrastructure
└── tools/
    └── test-prompts.py   # Prompt testing harness
```
