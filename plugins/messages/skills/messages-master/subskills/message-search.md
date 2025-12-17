# Message Search Sub-Skill

Full-text search and filtering across all messages.

## Search Architecture

The messages plugin uses **SQLite FTS5** (Full-Text Search 5) for fast, ranked search results.

### Index Location
```
.claude/messages/search/index.db
```

### What Gets Indexed
- Message content (full text)
- Author name
- Platform
- Kind (message type)
- Thread ID
- Timestamps

## Search via CLI

### Basic Search
```bash
bun plugins/messages/src/cli.ts search "authentication"
```

### With Platform Filter
```bash
bun plugins/messages/src/cli.ts search "meeting" -p telegram
```

### With Limit
```bash
bun plugins/messages/src/cli.ts search "error" -l 50
```

## Search via MCP

### messages_search Tool

```json
{
  "query": "search terms",
  "limit": 20,
  "offset": 0,
  "platforms": ["claude-code", "telegram"],
  "kinds": [101, 102],
  "since": 1702800000000,
  "until": 1702900000000
}
```

### Response Format
```json
{
  "results": [
    {
      "message": { /* full message object */ },
      "score": 2.45,
      "highlights": ["...matched **text**..."]
    }
  ],
  "total": 150
}
```

## Search Query Syntax

FTS5 supports special query syntax:

### Phrase Search
```
"exact phrase"
```

### AND (implicit)
```
word1 word2
```
Both words must appear.

### OR
```
word1 OR word2
```

### NOT
```
word1 NOT word2
```

### Prefix
```
auth*
```
Matches "authentication", "authorize", "author".

### Column-Specific
```
content:error platform:telegram
```

## Filtering Options

| Filter | Description | CLI Flag | MCP Param |
|--------|-------------|----------|-----------|
| Platform | Source platform | `-p, --platform` | `platforms` |
| Limit | Max results | `-l, --limit` | `limit` |
| Kind | Message type | N/A | `kinds` |
| Since | After timestamp | N/A | `since` |
| Until | Before timestamp | N/A | `until` |

## Programmatic Search

### TypeScript API

```typescript
import { createSearchIndex } from "@plugins/messages";

const search = createSearchIndex();

// Basic search
const results = search.search("query", { limit: 20 });

// With filters
const filtered = search.search("error", {
  limit: 50,
  platforms: ["claude-code"],
  kinds: [101, 102]
});

// Get recent messages
const recent = search.recent(10);

// Get thread messages
const thread = search.getThreadMessages("thread-id", 100);
```

### Search Result Object

```typescript
interface SearchResult {
  message: Message;
  score: number;        // BM25 relevance score
  highlights?: string[]; // Matched snippets
}
```

## Best Practices

### Effective Queries
- Use specific terms over generic ones
- Combine with platform filters for large datasets
- Use phrase search for exact matches
- Limit results when exploring

### Performance
- Index is updated on each import
- Large imports may take time to index
- Search is fast even with millions of messages

### Common Patterns

**Find all Claude responses about a topic:**
```bash
bun plugins/messages/src/cli.ts search "authentication" -p claude-code
```

**Find recent Telegram messages:**
```bash
bun plugins/messages/src/cli.ts recent -p telegram -l 20
```

**Search within date range (via MCP):**
```json
{
  "query": "meeting",
  "since": 1702800000000,
  "until": 1702900000000
}
```
