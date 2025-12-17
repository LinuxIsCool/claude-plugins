---
id: msg_4N8UGXZ8fAKJXUw557s7CW96KRtY7pWk
kind: 103
account_id: claude
created_at: 1765584349603
imported_at: 1766005509486
author_name: Claude
thread_id: cc_e8b5ca37
platform: claude-code
session_id: e8b5ca37-57c6-41f7-9eda-a84624f86bb4
tags: [["event_type","AssistantResponse"]]
---

## Claude Code Hooks

Hooks are **user-defined shell commands that execute at specific points in Claude Code's lifecycle**. They provide deterministic control, ensuring actions always happen rather than relying on prompting.

### Hook Events (10 available)

| Event | When It Runs |
|-------|--------------|
| `PreToolUse` | Before a tool executes (can block/modify) |
| `PostToolUse` | After a tool completes |
| `PermissionRequest` | When a permission dialog appears |
| `UserPromptSubmit` | When user submits a prompt |
| `Notification` | When Claude sends notifications |
| `Stop` | When main agent finishes |
| `SubagentStop` | When subagent finishes |
| `PreCompact` | Before context compaction |
| `SessionStart` | When session starts/resumes |
| `SessionEnd` | When session ends |

### Configuration

Configure in settings files (JSON format):
- `~/.claude/settings.json` - User settings
- `.claude/settings.json` - Project settings
- `.claude/settings.local.json` - Local (not committed)

**Easiest method**: Run `/hooks` command in Claude Code to configure interactively.

### Basic Example - Log Bash Commands

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.command' >> ~/.claude/bash-log.txt"
          }
        ]
      }
    ]
  }
}
```

### Exit Codes

- **0**: Success (stdout shown in verbose mode)
- **2**: Block the action (stderr shown as error)
- **Other**: Non-blocking error (continues)

### Key Best Practices

1. **Always quote shell variables** (`"$VAR"` not `$VAR`)
2. **Use `$CLAUDE_PROJECT_DIR`** for project-relative paths
3. **Set reasonable timeouts** (default 60s)
4. **Be specific with matchers** - use tool names or regex patterns

### Common Use Cases

- Auto-format files after writes
- Block edits to sensitive files (`.env`, `.git/`)
- Custom desktop notifications
- Logging and auditing
- Auto-approve safe operations

Would you like me to help you set up a specific hook, or dive deeper into any particular aspect?
