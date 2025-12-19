---
id: 2025-12-18-1842
title: "Search Index, Workflow Service, and Voice Fingerprinting Integration"
type: atomic
created: 2025-12-18T18:42:00-08:00
author: claude-opus-4
description: "Built SQLite FTS5 search index, TranscriptWorkflow orchestrator, and automatic voice fingerprinting"
tags: [transcripts-plugin, fts5, search, workflow, fingerprinting, hexagonal-architecture]
parent_daily: [[2025-12-18]]
related:
  - [[17-57-speaker-diarization-integration]]
---

# Search Index, Workflow Service, and Voice Fingerprinting Integration

Following the feature-dev plugin workflow, implemented the next phase of the transcripts plugin: search indexing, workflow orchestration, and automatic voice fingerprinting.

## What Was Built

### 1. Extended DiarizationResult with Embeddings

**Files modified:**
- `src/ports/diarization.ts:50-55` - Added `embeddings?: Record<string, Float32Array>` field
- `src/adapters/diarization/pyannote.ts:250-257` - Convert and return embeddings from Python
- `src/services/transcription-service.ts:44-49,230` - Pass embeddings through to SpeakerAttributedTranscript

The Python script already extracted embeddings but dropped them. Now they flow through the full pipeline.

### 2. TranscriptSearchIndex (`src/infrastructure/search.ts`)

SQLite FTS5-based full-text search for utterances, following the messages plugin pattern:

```typescript
export class TranscriptSearchIndex {
  search(query: string, options?: SearchOptions): UtteranceSearchResult[]
  searchGrouped(query: string, options?: SearchOptions): TranscriptSearchResult[]
  searchWithHighlights(query: string, options?: SearchOptions): (UtteranceSearchResult & { highlight: string })[]
  index(transcript: Transcript): void
  rebuild(transcripts: Transcript[]): number
  stats(): { transcripts, utterances, speakers, dateRange }
}
```

**Database schema:**
- `utterances_fts` - FTS5 virtual table with porter stemming
- `utterances_meta` - Metadata for filtering (speaker, timestamps)
- `transcripts_meta` - Transcript-level aggregates

### 3. TranscriptWorkflow (`src/services/transcript-workflow.ts`)

Orchestrates the full transcription pipeline:

```typescript
export class TranscriptWorkflow {
  async process(input: AudioInput, options?: TranscriptWorkflowOptions): Promise<TranscriptWorkflowResult> {
    // 1. Transcribe with speaker diarization
    // 2. Convert to TranscriptInput format
    // 3. Store to TranscriptStore
    // 4. Index for FTS5 search
    // 5. Auto-fingerprint speakers with embeddings
  }
}
```

**Automatic voice fingerprinting:**
- Extracts 256-dim embeddings from PyAnnote diarization
- Compares via cosine similarity (threshold ~0.75)
- Matches to existing speakers or creates anonymous profiles

### 4. Migration Support

Added `/transcripts rebuild-index` command and updated the search sub-skill documentation.

## Technical Decisions

### Cosine Similarity for Speaker Matching

```typescript
function cosineSimilarity(a: Float32Array, b: Float32Array): number {
  // Throws on zero vectors (indicates corrupted data)
  if (normA === 0 || normB === 0) {
    throw new Error("Invalid embedding: zero vector detected");
  }
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}
```

Zero vectors indicate corruption, not "0% similarity" - fail fast rather than silently create duplicate speakers.

### Path Construction Fix

Changed from `join(dbPath, "..")` to `dirname(dbPath)` - the former appends ".." as a path segment rather than computing parent directory.

## Architecture

The plugin now has a clean hexagonal architecture:

```
┌─────────────────────────────────────────────────────┐
│              TranscriptWorkflow                      │
│        (orchestrates full pipeline)                  │
└──────┬───────────┬─────────────┬───────────────────┘
       │           │             │
┌──────▼──────┐ ┌──▼──────┐ ┌───▼───────────────────┐
│Transcription│ │  Store  │ │    SearchIndex        │
│  Service    │ │         │ │    (FTS5)             │
└──────┬──────┘ └─────────┘ └───────────────────────┘
       │
┌──────▼──────┐    ┌─────────────────┐
│Diarization  │    │  Fingerprint    │
│   Port      │    │  Matching       │
└──────┬──────┘    └─────────────────┘
       │
┌──────▼──────┐
│ PyAnnote    │
│  Adapter    │
└─────────────┘
```

## Code Review Fixes

Applied fixes from code-reviewer agent:
1. Path construction: Use `dirname()` not `join(path, "..")`
2. Zero-vector handling: Throw error, don't return 0
3. Null safety: Add fallback for `duration_ms`

## Files Changed

| File | Action |
|------|--------|
| `src/ports/diarization.ts` | Modified - added embeddings field |
| `src/adapters/diarization/pyannote.ts` | Modified - return embeddings |
| `src/services/transcription-service.ts` | Modified - pass embeddings through |
| `src/infrastructure/search.ts` | **Created** - FTS5 search index |
| `src/services/transcript-workflow.ts` | **Created** - workflow orchestrator |
| `commands/transcripts.md` | Modified - added rebuild-index action |
| `skills/transcript-master/subskills/search.md` | Modified - documented FTS5 |

## Next Steps

1. **Voice fingerprinting persistence** - Store fingerprint matches in speaker profiles
2. **Search CLI/skill integration** - Wire search to `/transcripts search` command
3. **Entity extraction** - Extract named entities from transcript text
4. **Cross-meeting timeline** - Visualize speaker participation across meetings

---

*Parent: [[2025-12-18]]*
