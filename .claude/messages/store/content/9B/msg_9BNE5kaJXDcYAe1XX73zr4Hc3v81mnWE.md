---
id: msg_9BNE5kaJXDcYAe1XX73zr4Hc3v81mnWE
kind: 103
account_id: claude
created_at: 1765998234471
imported_at: 1766005522620
author_name: Claude
thread_id: cc_e9f9a384
platform: claude-code
session_id: e9f9a384-cc35-4151-b326-20eeadd918c9
tags: [["event_type","AssistantResponse"]]
---

Now I can give you a complete answer.

`★ Insight ─────────────────────────────────────`
**Logging captures via hooks, not direct CLI interception.** Claude Code exposes specific hook events (SessionStart, UserPromptSubmit, PreToolUse, etc.) that plugins can subscribe to. The logging plugin listens to all of these and records them to JSONL files.
`─────────────────────────────────────────────────`

**Answer: It depends on the type of slash command.**

| Command Type | Logged? | What Gets Captured |
|--------------|---------|-------------------|
| **Built-in CLI commands** (`/model`, `/help`, `/clear`, `/compact`) | **No** | These are handled by the CLI before any hooks fire |
| **Custom slash commands** (`/journal`, `/backlog`, etc.) | **Yes** | Logged as `SlashCommand` tool use via PreToolUse/PostToolUse hooks |

**For your specific example:**
- `/model opus` - **Not logged.** This is a built-in CLI command that runs locally and doesn't trigger the hook system.
- `/journal daily` - **Logged.** This triggers a `SlashCommand` tool use, which gets captured by PreToolUse and PostToolUse hooks.

**What gets captured for custom commands:**

```
PreToolUse:  tool_name: "SlashCommand", tool_input: {command: "/journal daily"}
PostToolUse: tool_name: "SlashCommand", tool_response: <expanded prompt>
UserPromptSubmit: prompt: <the expanded command content>
```

So the original command invocation (`/journal daily`) is captured, plus the expanded prompt content.

**Storage location:**
```
.claude/logging/YYYY/MM/DD/HH-MM-SS-{session}.jsonl  # Raw data
.claude/logging/YYYY/MM/DD/HH-MM-SS-{session}.md    # Human-readable report
```
