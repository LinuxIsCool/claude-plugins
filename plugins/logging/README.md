# Claude Code Logging Plugin

Minimal, full-fidelity logging for Claude Code sessions.

## Philosophy

- **Single script**: One file handles all 10 hook types
- **JSONL storage**: Append-only, one JSON object per line
- **Zero truncation**: Full payloads preserved, never data loss
- **No dependencies**: Pure Python, no external packages
- **Per-project storage**: Logs stored in each project's `.claude/logging/`

## Installation

### From Marketplace

```bash
# Add the marketplace (if not already added)
/plugin marketplace add linuxiscool/claude-plugins

# Install the plugin
/plugin install logging@linuxiscool-claude-plugins
```

### From Local Path

```bash
/plugin marketplace add /path/to/marketplaces/claude
/plugin install logging
```

## Data Storage

Logs are stored per-project, organized by date:

```
<your-project>/
└── .claude/
    └── logging/
        └── YYYY/MM/DD/
            └── {session_id}.jsonl
```

Each `.jsonl` file contains one JSON event per line with full payloads:

```json
{"ts": "2025-01-15T10:30:00", "type": "SessionStart", "session_id": "abc123", "data": {...}}
{"ts": "2025-01-15T10:30:05", "type": "UserPromptSubmit", "session_id": "abc123", "data": {...}}
```

## Automatic Reports

When using `--report` with SessionEnd (as shown in the installation example), a Markdown report is automatically generated alongside each session's JSONL file:

```
.claude/logging/2025/01/15/
├── abc12345.jsonl    # Raw event data
└── abc12345.md       # Human-readable report (auto-generated)
```

## Manual Reports

Use the report tool to generate Markdown from logs:

```bash
# Today's sessions
uv run tools/report.py

# Specific date
uv run tools/report.py --date 2025-01-15

# Specific session
uv run tools/report.py --session abc123

# All sessions
uv run tools/report.py --all

# Output to file
uv run tools/report.py --output report.md
```

## Hook Events Logged

| Hook | Description |
|------|-------------|
| SessionStart | Claude Code session begins |
| SessionEnd | Session ends |
| UserPromptSubmit | User sends a prompt |
| PreToolUse | Before a tool executes |
| PostToolUse | After a tool executes |
| PermissionRequest | Permission dialog shown |
| Notification | System notification |
| PreCompact | Context compaction triggered |
| Stop | Main agent stops |
| SubagentStop | Subagent stops |

## Querying Logs

JSONL files work with standard Unix tools:

```bash
# View all events
cat .claude/logging/2025/01/15/*.jsonl | jq .

# Filter by event type
cat .claude/logging/2025/01/15/*.jsonl | jq 'select(.type == "UserPromptSubmit")'

# Count events
wc -l .claude/logging/2025/01/15/*.jsonl

# Search prompts
grep -h "prompt" .claude/logging/2025/01/15/*.jsonl | jq .data.prompt
```

## Structure

```
plugins/logging/
├── .claude-plugin/
│   ├── plugin.json     # Plugin manifest
│   └── hooks.json      # Hook configuration
├── hooks/
│   └── log_event.py    # Single script handles all hooks
├── tools/
│   └── report.py       # Bulk report generator
└── README.md
```

## Design Decisions

### Why a Single Script?
- All hooks do the same thing: read stdin, log to JSONL
- Event type passed via `--event-type` argument
- DRY: no code duplication across 10 files

### Why JSONL?
- **Append-only**: No corruption risk, concurrent-safe
- **Full fidelity**: Never truncate data
- **Human-readable**: Use `cat`, `grep`, `jq`
- **Future-proof**: Import into SQLite/Postgres when needed

### Why No Configuration?
- Sensible defaults work for 99% of cases
- To disable a hook, don't register it
- Complexity reduction > minor flexibility

### Why Generate Reports On-Demand?
- Hooks stay fast and simple
- Avoids sync issues between storage formats
- Can always re-generate from source data

## License

MIT
