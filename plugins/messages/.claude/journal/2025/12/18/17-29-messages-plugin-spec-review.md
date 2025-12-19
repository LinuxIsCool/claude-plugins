---
id: 2025-12-18-1729
title: "Messages Plugin Spec Review"
type: atomic
created: 2025-12-18T17:29:30
author: claude-opus-4
description: "Comprehensive review of messages plugin specs vs implementation - Phases 1-3 complete, Phase 4 (TUI) pending"
tags: [messages-plugin, spec-review, architecture, roadmap]
parent_daily: [[2025-12-18]]
related: []
---

# Messages Plugin Spec Review

Review of three specification documents against the current implementation state.

## Context

The messages plugin has three specs representing different architectural approaches:
- **01-minimal-viable.md** - Fast path (2-3 days, ~1,720 LOC)
- **02-full-content-addressed.md** - Production-grade (2-3 weeks, ~5,800 LOC)
- **03-pragmatic-phased.md** - Incremental delivery (~9 days)

The implementation follows the **Pragmatic Phased** approach.

## Implementation Status by Phase

### Phase 1: Foundation + Telegram (Complete)

| Component | Status |
|-----------|--------|
| Core types (`types/index.ts`) | Enhanced beyond spec with Author, MessageRefs, MessageSource |
| JSONL store (`core/store.ts`) | Full event sourcing, content-addressed markdown |
| Telegram adapter | Export file import working |
| SQLite FTS5 search | Porter stemming, platform filtering |
| Basic CLI | All commands functional |

### Phase 2: CIDs + Email (Complete + Extended)

| Component | Status |
|-----------|--------|
| CID generation (`core/cid.ts`) | SHA-256 + base58, `msg_` prefix |
| Email adapter (`.eml` files) | Complete via `adapters/email.ts` |
| **Beyond spec**: Live IMAP sync | `email-imap.ts` + `imap-client.ts` |
| **Beyond spec**: Email parser utilities | `integrations/email/parser.ts` |

The IMAP implementation includes:
- Two-phase fetch (ENVELOPE first, RFC822 for new only)
- Cross-folder deduplication (Gmail shows same message in INBOX + All Mail)
- 65% bandwidth savings in testing (507 vs 1,441 potential fetches)

### Phase 3: DIDs + Claude Code (Complete + Extended)

| Component | Status |
|-----------|--------|
| DID generation (`core/did.ts`) | did:key Ed25519 |
| Claude Code logging adapter | `adapters/logging.ts` |
| **Beyond spec**: Live Telegram API | MTProto via `telegram-api.ts` |
| **Beyond spec**: Claude web adapter | `adapters/claude-web.ts` |

### Phase 4: TUI Browser (Not Started)

The Ink-based TUI is not implemented. Expected structure:
```
src/tui/
├── app.tsx        # Main menu, navigation
├── timeline.tsx   # Recent messages view
├── thread.tsx     # Thread browser
└── search.tsx     # Search interface
```

## From Full Spec (Not Implemented)

| Feature | Purpose | Priority |
|---------|---------|----------|
| Merkle DAG threads | Verifiable chains | Low |
| Message signatures | Ed25519 authorship proof | Medium |
| Vector embeddings | Semantic search | Medium |
| MCP server | Tool exposure for Claude | High |
| Projection engine | Event replay/rebuild | Low |

## Insights

**What went well:**
- Implementation exceeds spec in practical ways (live sync vs file import)
- Two-phase IMAP fetch pattern from external dev significantly improved performance
- Modular `integrations/` architecture enables adapter reuse

**What's pending:**
- Phase 4 TUI would provide user-facing interface
- MCP server would make messages accessible as Claude tools
- Vector search would enable semantic similarity queries

## Recommendations

1. **Next**: Implement Phase 4 TUI for message browsing
2. **High value**: Add MCP server for Claude Code integration
3. **Later**: Vector search when semantic similarity becomes valuable

---

*Parent: [[2025-12-18]]*
