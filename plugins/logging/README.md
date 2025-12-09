# Claude Code Logging Plugin

Full-fidelity session logging with live Markdown reports.

## Installation

```bash
/plugin marketplace add linuxiscool/claude-plugins
/plugin install logging
```

## What It Does

Every hook event is logged to two files:

```
<project>/.claude/logging/YYYY/MM/DD/
├── {session}.jsonl   # Full data (never truncated)
└── {session}.md      # Live-updating human-readable report
```

## Live Report Format

```markdown
# Session abc12345

**ID:** `abc12345-...`
**Started:** 2025-01-15 10:30:00

---

`10:30:00` 💫 SessionStart startup
`10:30:05` 🍄 UserPromptSubmit Help me refactor...
`10:30:10` 🔨 PreToolUse Read `src/main.py`
`10:30:11` 🏰 PostToolUse Read
`10:30:20` 🟢 Stop 1 prompt, 2 tools
`10:30:20` 🌲 AssistantResponse Done! I refactored...
```

## Events Logged

| Event | Emoji | Info |
|-------|-------|------|
| SessionStart | 💫 | source |
| SessionEnd | ⭐ | |
| UserPromptSubmit | 🍄 | full prompt |
| PreToolUse | 🔨 | tool name + preview |
| PostToolUse | 🏰 | tool name |
| PermissionRequest | 🔑 | |
| Notification | 🟡 | message |
| PreCompact | ♻ | |
| Stop | 🟢 | prompt/tool counts |
| SubagentStop | 🔵 | agent id |
| AssistantResponse | 🌲 | full response |

## Querying JSONL

```bash
# View session events
cat .claude/logging/2025/12/08/*.jsonl | jq .

# Extract prompts
jq -r 'select(.type=="UserPromptSubmit") | .data.prompt' .claude/logging/*/*/*.jsonl

# Count events by type
jq -s 'group_by(.type) | map({type:.[0].type, n:length})' .claude/logging/*/*/*.jsonl

# Search across all sessions
grep -r "keyword" .claude/logging/
```

## Structure

```
plugins/logging/
├── .claude-plugin/
│   └── plugin.json     # Manifest + hooks
└── hooks/
    └── log_event.py    # Single 80-line script
```

## Design

- **Single script**: One file handles all 10 hooks via `-e EventType`
- **JSONL**: Append-only, full fidelity, works with `jq`/`grep`
- **Live Markdown**: Updates after every event, viewable mid-session
- **No config**: Sensible defaults, disable hooks by not registering them
