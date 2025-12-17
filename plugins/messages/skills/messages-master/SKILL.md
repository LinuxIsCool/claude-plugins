---
name: messages
description: "Universal messaging backbone with content-addressed storage and DID-based identity. Sub-skills: store, adapters, accounts, threads, search, tui. Invoke for message management, platform imports, and agent-to-agent communication."
allowed-tools: Read, Glob, Grep, Bash, Write, Edit
---

# Messages Plugin - Master Skill

Universal messaging backbone that unifies messages from all platforms.

## Quick Reference

| Action | How |
|--------|-----|
| Import messages | Use platform adapter |
| Search messages | `messages search "query"` |
| View thread | `messages thread <id>` |
| List accounts | `messages accounts` |
| View timeline | `messages timeline` |

## Sub-Skills Index

| Sub-Skill | Use When | File |
|-----------|----------|------|
| **store** | Understanding storage architecture, CIDs, events | `subskills/store.md` |
| **adapters** | Importing from platforms (Telegram, Email, Claude Code) | `subskills/adapters.md` |
| **accounts** | Managing identities and DIDs | `subskills/accounts.md` |
| **threads** | Working with conversations | `subskills/threads.md` |
| **search** | Finding messages | `subskills/search.md` |
| **tui** | Terminal interface navigation | `subskills/tui.md` |

## Core Concepts

### Content-Addressed Messages

Every message has a CID (Content Identifier) - a hash of its content. This provides:
- **Immutability**: Content can't change without changing ID
- **Verification**: Anyone can verify content matches CID
- **Deduplication**: Same content = same CID = store once

### DID-Based Identity

Accounts use Decentralized Identifiers (DIDs) for portable identity:
- **Portable**: Identity isn't tied to any platform
- **Verifiable**: Cryptographically authenticated
- **Linkable**: Connect multiple platform handles to one identity

### Platform Adapters

Import messages from any source:
- **Telegram**: Chat exports or Bot API
- **Email**: IMAP or export files
- **Claude Code**: Session events, prompts, responses
- **More**: Discord, Slack, forums, etc.

## Directory Structure

```
.claude/messages/
├── store/
│   ├── events/              # Append-only event log
│   │   └── YYYY/MM/DD/
│   │       └── events.jsonl
│   └── content/             # Content-addressed blobs
│       └── XX/
│           └── {cid}.md
├── views/                   # Materialized projections
│   ├── threads/
│   ├── accounts/
│   ├── by-kind/
│   └── timeline/
├── adapters/                # Adapter state/cache
└── search/
    └── index.db             # Full-text search
```

## Message Kinds

| Kind | Description |
|------|-------------|
| 1-99 | Core message types (text, media, reactions) |
| 100-199 | Claude Code events (sessions, prompts, responses) |
| 200-249 | Git events (commits, branches) |
| 1000+ | Platform-specific (Telegram, WhatsApp, Email, etc.) |

## Usage Patterns

### Import from Telegram
```bash
bun plugins/messages/src/cli.ts import telegram --file export.json
```

### Search Messages
```bash
bun plugins/messages/src/cli.ts search "meeting tomorrow"
```

### View Thread
```bash
bun plugins/messages/src/cli.ts thread thread-001
```

### Launch TUI
```bash
bun plugins/messages/src/cli.ts tui
```

## Design Principles

1. **Content-Addressed**: Every message has a CID
2. **Identity-Portable**: DIDs decouple from platforms
3. **Event-First**: Append-only event log
4. **Adapter-Based**: Pluggable platform imports
5. **Markdown-Native**: Human-readable storage
6. **Standalone-Enhanced**: Works alone, better with ecosystem
