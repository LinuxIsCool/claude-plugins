---
id: 2025-12-18-1908
title: "Search MCP Integration - Wiring FTS5 to CLI"
type: atomic
created: 2025-12-18T19:08:00-08:00
author: claude-opus-4
description: "Added transcripts_search, transcripts_search_stats, and transcripts_rebuild_index MCP tools"
tags: [transcripts-plugin, mcp, search, fts5, cli-integration]
parent_daily: [[2025-12-18]]
related:
  - [[18-42-search-workflow-fingerprint-integration]]
---

# Search MCP Integration - Wiring FTS5 to CLI

Following the previous session's work building the `TranscriptSearchIndex` infrastructure, this session completed the CLI integration by exposing search functionality through the MCP server.

## Context

The previous session (`18-42-search-workflow-fingerprint-integration`) built:
- `TranscriptSearchIndex` class with FTS5 full-text search
- `TranscriptWorkflow` orchestrator for the full pipeline
- Voice fingerprinting with cosine similarity

However, this infrastructure was orphaned—no way for users to actually search. The search sub-skill documentation even marked `transcripts_search` as "(planned)".

## What Was Built

### 1. transcripts_search MCP Tool

Full-text search across transcript utterances with rich filtering and output options.

**Input Schema:**
```typescript
{
  query: string;           // FTS5 query (required)
  speakers?: string[];     // Filter by speaker IDs
  transcripts?: TID[];     // Filter by transcript IDs
  limit?: number;          // Max results (default 20)
  offset?: number;         // Pagination offset
  highlights?: boolean;    // Include highlighted snippets (default true)
  grouped?: boolean;       // Group by transcript (default false)
}
```

**Three Output Modes:**

1. **Grouped** (`grouped: true`):
```json
{
  "query": "budget",
  "grouped": true,
  "transcript_count": 3,
  "results": [
    {
      "transcript_id": "tx_abc123",
      "title": "Q4 Planning Meeting",
      "match_count": 12,
      "total_score": 8.45,
      "matches": [/* top 5 matches */],
      "more_matches": 7
    }
  ]
}
```

2. **Highlighted** (`highlights: true`, default):
```json
{
  "query": "machine learning",
  "count": 15,
  "results": [
    {
      "transcript_id": "tx_abc123",
      "utterance_id": "tx_abc123:ut_0042",
      "speaker": "Alice Chen",
      "highlight": "...focus on **machine learning** infrastructure...",
      "full_text": "I think we should focus on machine learning...",
      "time": "2m 25s",
      "duration": "7s",
      "score": 2.34
    }
  ]
}
```

3. **Plain** (`highlights: false`):
```json
{
  "query": "budget",
  "count": 20,
  "results": [
    {
      "transcript_id": "tx_abc123",
      "utterance_id": "tx_abc123:ut_0015",
      "speaker": "John Smith",
      "text": "The quarterly budget needs...",
      "time": "1m 5s",
      "score": 1.89
    }
  ]
}
```

### 2. transcripts_search_stats MCP Tool

Returns statistics about the search index for diagnostics and monitoring.

**Output:**
```json
{
  "transcripts_indexed": 42,
  "utterances_indexed": 1847,
  "unique_speakers": 15,
  "date_range": {
    "first": "2025-10-15T14:30:00.000Z",
    "last": "2025-12-18T18:00:00.000Z"
  }
}
```

### 3. transcripts_rebuild_index MCP Tool

Rebuilds the entire FTS5 index from stored transcripts. Essential for:
- Migrating existing transcripts to search
- Recovering from index corruption
- Re-indexing after manual transcript edits

**Input:**
```json
{
  "clear": true  // Clear before rebuild (default true)
}
```

**Output:**
```json
{
  "indexed": 42,
  "cleared": true,
  "errors": null,  // or array of error messages
  "stats": {
    "transcripts": 42,
    "utterances": 1847,
    "speakers": 15,
    "dateRange": { "first": 1729000000000, "last": 1734566400000 }
  }
}
```

## FTS5 Query Syntax

The search tool exposes SQLite FTS5's full query language:

| Syntax | Example | Meaning |
|--------|---------|---------|
| Simple terms | `budget meeting` | Implicit AND |
| Phrases | `"quarterly review"` | Exact phrase match |
| Boolean AND | `budget AND review` | Both terms required |
| Boolean OR | `budget OR revenue` | Either term |
| Boolean NOT | `budget NOT annual` | Exclusion |
| Prefix | `project*` | Matches project, projects, projection... |
| Combined | `"machine learning" AND python` | Phrase + term |

The `porter` tokenizer enables stemming:
- "running" matches "run", "runs", "ran"
- "meetings" matches "meeting", "meet"

## Implementation Details

### Server Class Changes

```typescript
export class TranscriptsMCPServer {
  private store: TranscriptStore;
  private searchIndex: TranscriptSearchIndex;  // NEW

  constructor() {
    this.store = createStore();
    this.searchIndex = new TranscriptSearchIndex();  // NEW
  }
```

The search index is instantiated once per server lifecycle, sharing the SQLite connection across all search operations.

### Error Handling

Search errors (malformed FTS5 queries) return helpful hints:

```typescript
catch (error) {
  return {
    content: [{
      type: "text",
      text: JSON.stringify({
        error: `Search failed: ${error.message}`,
        hint: "FTS5 query syntax: use AND/OR/NOT, \"phrases\", prefix* wildcards",
      }, null, 2),
    }],
  };
}
```

### Time Formatting

All temporal values are formatted consistently using the existing `formatTime()` helper:
- `"2m 25s"` for utterance timestamps
- `"7s"` for utterance durations
- Handles hours when needed: `"1h 30m 45s"`

## Architecture

The MCP layer sits cleanly above the infrastructure:

```
┌────────────────────────────────────────────────────────┐
│                    CLI / Claude                         │
│              /transcripts search "query"                │
└───────────────────────┬────────────────────────────────┘
                        │
┌───────────────────────▼────────────────────────────────┐
│               TranscriptsMCPServer                      │
│  tools/call → toolSearch() → searchIndex.search()      │
└───────────────────────┬────────────────────────────────┘
                        │
┌───────────────────────▼────────────────────────────────┐
│              TranscriptSearchIndex                      │
│         search() / searchGrouped() / searchWithHighlights()      │
└───────────────────────┬────────────────────────────────┘
                        │
┌───────────────────────▼────────────────────────────────┐
│                   SQLite FTS5                           │
│         bm25 ranking · porter stemming · unicode61      │
└────────────────────────────────────────────────────────┘
```

## Files Changed

| File | Lines | Action |
|------|-------|--------|
| `src/server/index.ts` | +170 | Added 3 MCP tools + implementations |
| `commands/transcripts.md` | +30 | Search syntax docs + implementation |
| `skills/transcript-master/subskills/search.md` | +30 | Marked tools as implemented |

## Design Decisions

### Why Three Output Modes?

1. **Grouped**: Best for "which meetings discussed X?" queries
2. **Highlighted**: Best for "show me the context around X" queries
3. **Plain**: Best for API consumers who want raw data

The default (`highlights: true, grouped: false`) optimizes for human readability.

### Why Rebuild as Separate Tool?

Rather than auto-rebuilding on every startup:
- Explicit control over when expensive operations run
- Clear feedback on progress and errors
- Supports incremental use patterns (index only new transcripts)

### Why Not Expose Filter by Date?

The `SearchOptions` interface supports `createdAfter`/`createdBefore`, but the MCP tool doesn't expose them yet. Reasoning:
- Date filtering is complex UX (timezone handling, input formats)
- Speaker/transcript filters cover most use cases
- Can add later without breaking changes

## Usage Examples

### Find what Alice said about machine learning
```
/transcripts search "machine learning" --speaker spk_alice
```

### Find all mentions of a project across meetings
```
/transcripts search "project falcon" --grouped
```

### Check index health
```
/transcripts search-stats
```

### Rebuild after importing old transcripts
```
/transcripts rebuild-index
```

## Performance Notes

- **BM25 scoring**: FTS5's default ranking algorithm, optimized for relevance
- **Porter stemming**: Applied at index time, no runtime cost
- **Pagination**: `limit`/`offset` push filtering to SQLite, not post-query
- **Index size**: Roughly 2x the raw text size (inverted index + metadata)

## Next Steps

From the previous session's roadmap:
1. ~~Search CLI integration~~ ✓ **DONE**
2. Voice fingerprinting persistence - Store matches in speaker profiles
3. Entity extraction - Extract named entities from transcript text
4. Cross-meeting timeline - Visualize speaker participation over time

The search foundation is now complete. Entity extraction would build on top of it by tagging utterances and enabling entity-filtered search.

---

*Parent: [[2025-12-18]]*
*Related: [[18-42-search-workflow-fingerprint-integration]]*
