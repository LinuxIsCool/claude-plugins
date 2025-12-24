---
id: 2025-12-24-1104
title: "YouTube Ingestion Queue: Rate-Limited Transcript Accumulation"
type: atomic
created: 2025-12-24T11:04:17
author: claude-opus-4
description: "Built a persistent, rate-limit-aware YouTube transcript ingestion queue with channel subscriptions and exponential backoff"
tags: [youtube, transcripts, queue, rate-limiting, infrastructure, indydevdan]
parent_daily: [[2025-12-24]]
related: []
---

# YouTube Ingestion Queue: Rate-Limited Transcript Accumulation

Built a complete rate-limit-aware queue system for ingesting YouTube transcripts over time, enabling the ecosystem to "clone" thought leaders by accumulating their content.

## Context

The user wanted to ingest IndyDevDan's YouTube content (mentioned in the 2026 strategy roadmap as a trust-and-autonomy exemplar). Previous session had built the YouTube ingestion adapter (`youtube.ts`) with yt-dlp integration. The challenge: YouTube rate limits. Can't download 200 videos at once without triggering blocks.

The solution needed to:
- Queue videos from subscribed channels
- Process in small batches respecting rate limits
- Persist state across sessions
- Resume where it left off
- Support multiple "people to clone"

## Implementation

### Core Components

**1. Queue Data Structure** (`src/infrastructure/youtube-queue.ts`)

```typescript
interface QueuedVideo {
  id: string;                    // YouTube video ID
  channel_id: string;            // Channel subscription ID
  title: string;
  upload_date: string;           // YYYYMMDD
  status: "pending" | "processing" | "completed" | "failed" | "rate_limited";
  attempts: number;
  last_attempt: number | null;
  error: string | null;
  added_at: number;
}

interface QueueState {
  is_rate_limited: boolean;
  rate_limit_until: number | null;
  backoff_minutes: number;        // 5 → 10 → 20 → ... → 1440 (24h max)
  last_successful_ingest: number | null;
  total_ingested: number;
  total_failed: number;
  processing_enabled: boolean;
}
```

**2. Rate Limit Detection**

Pattern matching on yt-dlp error messages:
- `HTTP Error 429`
- `Too Many Requests`
- `rate.?limit`
- `quota.?exceeded`
- `sign in to confirm` (YouTube anti-bot)
- `blocked`

**3. Storage Structure**

```
~/.claude/transcripts/youtube-queue/
├── state.json      # Queue state (backoff, last run)
├── channels.json   # Subscribed channels
└── queue.jsonl     # Pending videos (append-only, last wins)
```

**4. Processing Order**

- Channels sorted by priority (high → medium → low)
- Within priority: oldest videos first (chronological accumulation)
- Batch size: 5 videos per run (configurable)

### MCP Tools Added (8 total)

| Tool | Purpose |
|------|---------|
| `transcripts_queue_subscribe` | Add channel to ingestion queue |
| `transcripts_queue_unsubscribe` | Remove channel |
| `transcripts_queue_channels` | List subscribed channels |
| `transcripts_queue_status` | Queue stats + rate limit info |
| `transcripts_queue_process` | Process batch with backoff |
| `transcripts_queue_retry_failed` | Reset failed → pending |
| `transcripts_queue_clear_rate_limit` | Manual override |
| `transcripts_queue_check_new` | Discover new videos on channels |

### SessionStart Hook

Created `hooks/session-start.md` to check queue status on session start and optionally process a batch.

## Results

Tested with IndyDevDan channel:

```
Subscribed: IndyDevDan (@IndyDevDan)
Videos queued: 176
Priority: high

First batch (3 videos): 3/3 succeeded
Second batch (20 newest): 20/20 succeeded

Total captions ingested: ~33,000+ lines
Rate limits hit: 0
```

## Architecture Insights

**Why JSONL for queue?**
- Append-only avoids file corruption
- Last state wins on reload (simple conflict resolution)
- Full audit trail of state changes
- No complex database needed

**Why exponential backoff?**
- 5 min → 10 → 20 → 40 → 80 → 160 → 320 → 640 → 1280 → 1440 (max)
- Aggressive growth prevents repeated rate limit triggers
- 24-hour max is reasonable recovery period
- Resets to 5 min after any successful ingest

**Why oldest-first processing?**
- Builds chronological transcript archive
- Earlier content often foundational
- Can switch to newest-first by modifying sort order

## Future Enhancements

1. **Auto-check for new videos** - Periodic hook or cron job
2. **Store integration** - Currently caches but doesn't persist to event store
3. **Search indexing** - Index transcripts on ingest for full-text search
4. **Cross-channel deduplication** - Same video on multiple channels
5. **Smart scheduling** - Process during low-usage hours

## Key Files

- `plugins/transcripts/src/infrastructure/youtube-queue.ts` - Queue implementation
- `plugins/transcripts/src/server/index.ts` - MCP tools (lines 381-467, 534-557, 1497-1752)
- `plugins/transcripts/hooks/session-start.md` - SessionStart hook
- `plugins/transcripts/.claude-plugin/plugin.json` - Updated with hooks

---

*Parent: [[2025-12-24]]*
