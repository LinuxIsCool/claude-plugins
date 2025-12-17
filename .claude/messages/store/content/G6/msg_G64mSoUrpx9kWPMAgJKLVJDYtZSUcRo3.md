---
id: msg_G64mSoUrpx9kWPMAgJKLVJDYtZSUcRo3
kind: 103
account_id: claude
created_at: 1765928857623
imported_at: 1766005511820
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

The **instance registry** is a JSON file at `.claude/instances/registry.json` that tracks all Claude Code sessions running in this repository.

## What It Stores

```json
{
  "e05dab22-0e00-4995-bf56-e7657c004d36": {
    "name": "Phoenix",           // Self-chosen identity
    "task": "Crash recovery",    // What the instance is doing
    "model": "",                 // Model ID (opus/sonnet/haiku)
    "cwd": "/home/ygg/.../claude",
    "created": "2025-12-16T23:43:45Z",
    "last_seen": "2025-12-16T23:45:16Z",
    "status": "active"
  }
}
```

## Purpose

1. **Instance awareness** — Agents can see who else is working in the repo
2. **Coordination** — Avoid conflicting edits on the same files
3. **Identity** — Instances can name themselves (I'm "Phoenix")
4. **Observability** — You can see what agents are doing via `/statusline:instances`

## How It Works

The **statusline plugin** (`plugins/statusline/`) manages this:
- **Hook on SessionStart** — Registers new sessions automatically
- **Registry tool** — `registry.py register <id> <name> --task "description"`
- **Slash command** — `/statusline:instances` lists all instances

## The Problem Now

The registry shows 6 "active" instances, but 5 of them died in the crash. Without a heartbeat/cleanup mechanism, dead instances stay marked as "active" forever — zombie entries.

This was created recently (commit `7d08842` — "[statusline] add: instance registry") so the cleanup/heartbeat logic hasn't been built yet.
