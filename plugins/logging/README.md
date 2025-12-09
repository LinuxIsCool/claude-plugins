# Claude Code Logging Plugin

Full-fidelity session logging with Markdown reports.

## Installation

```bash
/plugin install logging
```

## What It Does

Logs every hook event to JSONL (source of truth) and generates Markdown reports:

```
<project>/.claude/logging/YYYY/MM/DD/
├── HH-MM-SS-{session}.jsonl   # Full data, never truncated
└── HH-MM-SS-{session}.md      # Conversation-style report
```

## Report Format

```markdown
# Session abc12345

**ID:** `abc12345-...`
**Started:** 2025-01-15 10:30:00

---

`10:30:00` 💫 SessionStart startup

---
### 10:30:05

🍄 **User**
> Help me refactor the logging plugin

<details>
<summary>📦 3 tools: Read (2), Edit (1)</summary>

- Read `src/main.py`
- Read `src/utils.py`
- Edit `src/main.py`

</details>

🌲 **Claude**
> Done! I refactored the logging plugin to be more modular...
```

## Querying JSONL

```bash
# View session events
cat .claude/logging/2025/12/08/*.jsonl | jq .

# Extract prompts
jq -r 'select(.type=="UserPromptSubmit") | .data.prompt' .claude/logging/*/*/*.jsonl

# Count events by type
jq -s 'group_by(.type) | map({type:.[0].type, n:length})' .claude/logging/*/*/*.jsonl
```

## Design

- **JSONL source of truth**: Append-only, full fidelity
- **Markdown on Stop**: Regenerated from JSONL after each exchange
- **Aggregated tools**: Grouped in collapsible details
- **Conversation format**: User/Claude exchanges with visual separators
