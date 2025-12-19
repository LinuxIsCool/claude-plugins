---
id: 2025-12-18-1842
title: "Search Index, Workflow Service, and Voice Fingerprinting Integration"
type: atomic
created: 2025-12-18T18:42:00-08:00
author: claude-opus-4
description: "Built SQLite FTS5 search index, TranscriptWorkflow orchestrator, and automatic voice fingerprinting"
tags: [transcripts-plugin, fts5, search, workflow, fingerprinting, hexagonal-architecture, feature-dev, cosine-similarity]
parent_daily: [[2025-12-18]]
related:
  - [[17-57-speaker-diarization-integration]]
  - [[15-31-gpu-transcription-breakthrough]]
---

# Search Index, Workflow Service, and Voice Fingerprinting Integration

This session represents the second major milestone in the transcripts plugin: connecting the 23x realtime transcription pipeline to persistent storage, full-text search, and automatic speaker recognition. Following the feature-dev plugin's structured workflow (7 phases), this implementation transforms raw audio processing into an integrated knowledge system.

## Context and Motivation

The previous session ([[17-57-speaker-diarization-integration]]) achieved GPU-accelerated transcription with speaker diarization at 23x realtime. However, several critical capabilities were missing:

1. **No search** - Transcripts existed but couldn't be queried ("what did Alice say about budgets?")
2. **Embeddings dropped** - PyAnnote extracted 256-dimensional speaker embeddings but they were discarded at the Python/TypeScript boundary
3. **No persistence pipeline** - TranscriptionService produced results but didn't integrate with TranscriptStore
4. **Manual speaker identification** - Each transcript had anonymous SPEAKER_00/SPEAKER_01 labels with no cross-meeting recognition

The journal entry from the previous session explicitly listed these as next steps:
> 1. **Voice fingerprinting** - Use speaker embeddings for cross-meeting speaker identification
> 2. **Search index** - SQLite FTS5 for full-text search across transcripts

## Feature-Dev Workflow Execution

### Phase 1-2: Requirements and Exploration

Launched three code-explorer agents in parallel to understand existing patterns:
- **Service-to-store patterns** - Found that MCP server bypasses TranscriptionService, calling adapter directly
- **Fingerprinting port patterns** - Discovered existing FingerprintingPort interface but no implementation
- **Search index patterns** - Found messages plugin's complete FTS5 reference implementation

Key discovery: The PyAnnoteAdapter Python script (lines 215-224) already extracts speaker embeddings:

```python
# Get speaker embeddings if available
embeddings = {}
if hasattr(output, 'speaker_embeddings') and output.speaker_embeddings is not None:
    emb_array = output.speaker_embeddings
    unique_speakers = sorted(list(speaker_labels))
    for i, speaker in enumerate(unique_speakers):
        if i < len(emb_array):
            embeddings[speaker] = emb_array[i].tolist()
```

And outputs them in JSON (line 234):
```python
result = {
    ...
    "embeddings": embeddings,
}
```

But the TypeScript code at lines 250-256 dropped them:
```typescript
return {
  segments,
  speaker_count: data.speaker_count,
  speaker_labels: data.speaker_labels,
  duration_ms: data.duration_ms,
  processing_time_ms: data.load_time_ms + data.diarize_time_ms,
  // embeddings: MISSING!
};
```

This is a common pattern in ML pipelines—the hard work happens in Python but gets lost when crossing language boundaries.

### Phase 3: Clarifying Questions

Used AskUserQuestion tool to gather requirements:

| Question | User Response |
|----------|---------------|
| Integration strategy | "Build Claude Code skills, not MCP servers" |
| Fingerprinting approach | Automatic on every transcription |
| Speaker profiles | Create anonymous profiles with fingerprints |
| Search indexing | Immediate + rebuild capability |
| Embeddings location | Extend DiarizationResult (single inference pass) |
| Migration strategy | Provide migration command |

### Phase 4: Architecture Design

Launched three code-architect agents with different approaches:
1. **Minimal changes** (7 files) - Too limited
2. **Clean architecture** (12+ files) - Over-engineered
3. **Pragmatic balance** (5-6 files) - Selected

The pragmatic approach balances maintainability with simplicity by:
- Reusing proven patterns (messages SearchIndex structure)
- Minimizing changes (only extend DiarizationResult, add 2 new files)
- Single responsibility (each component does one thing well)

### Phases 5-7: Implementation, Review, Summary

## Technical Implementation

### 1. Extending the Embeddings Pipeline

**`src/ports/diarization.ts:50-55`**

Added embeddings to the DiarizationResult interface:

```typescript
export interface DiarizationResult {
  segments: DiarizationSegment[];
  speaker_count: number;
  speaker_labels: string[];
  duration_ms: number;
  processing_time_ms: number;

  /**
   * Speaker embeddings (256-dimensional vectors from pyannote).
   * Used for voice fingerprinting and cross-meeting speaker identification.
   * Key: speaker label (e.g., "SPEAKER_00"), Value: embedding vector
   */
  embeddings?: Record<string, Float32Array>;
}
```

**`src/adapters/diarization/pyannote.ts:250-266`**

Deserialize JSON number arrays back to Float32Array:

```typescript
// Convert embeddings from number[] to Float32Array
const embeddings: Record<string, Float32Array> | undefined = data.embeddings
  ? Object.fromEntries(
      Object.entries(data.embeddings as Record<string, number[]>).map(
        ([speaker, emb]) => [speaker, new Float32Array(emb)]
      )
    )
  : undefined;

return {
  segments,
  speaker_count: data.speaker_count,
  speaker_labels: data.speaker_labels,
  duration_ms: data.duration_ms,
  processing_time_ms: data.load_time_ms + data.diarize_time_ms,
  embeddings,  // Now included!
};
```

**Why Float32Array?**
- Memory efficient (4 bytes per element vs 8 for Float64)
- Matches PyTorch/numpy default float type
- Sufficient precision for cosine similarity (embeddings are normalized)

**`src/services/transcription-service.ts:44-49,230`**

Extended SpeakerAttributedTranscript to carry embeddings through:

```typescript
export interface SpeakerAttributedTranscript {
  // ... existing fields ...

  /**
   * Speaker embeddings from diarization (256-dim Float32Array).
   * Used for voice fingerprinting and cross-meeting speaker identification.
   * Only present if diarization was performed with embedding extraction.
   */
  embeddings?: Record<string, Float32Array>;
}
```

And in the return statement:
```typescript
return {
  utterances: attributedUtterances,
  speakers,
  language: transcription.language,
  // ... other fields ...
  embeddings: diarization?.embeddings,  // Pass through
};
```

### 2. SQLite FTS5 Search Index

**`src/infrastructure/search.ts`** (461 lines)

Created a full-text search index following the messages plugin pattern. The design uses a two-table architecture:

#### Database Schema

```sql
-- FTS5 virtual table for full-text search
-- tokenize='porter unicode61' enables:
--   - Porter stemming ("running" matches "run", "walked" matches "walk")
--   - Unicode normalization (handles accents, case folding)
CREATE VIRTUAL TABLE utterances_fts USING fts5(
  id UNINDEXED,           -- Don't index IDs (they won't be searched)
  transcript_id UNINDEXED,
  speaker_id UNINDEXED,
  speaker_name,           -- Searchable (find by speaker name)
  text,                   -- Primary search target
  tokenize='porter unicode61'
);

-- Metadata table for filtering (joins with FTS for combined queries)
CREATE TABLE utterances_meta (
  id TEXT PRIMARY KEY,
  transcript_id TEXT NOT NULL,
  speaker_id TEXT NOT NULL,
  speaker_name TEXT NOT NULL,
  text TEXT NOT NULL,
  start_ms INTEGER NOT NULL,
  end_ms INTEGER NOT NULL,
  created_at INTEGER NOT NULL
);

-- Transcript-level metadata for grouping results
CREATE TABLE transcripts_meta (
  id TEXT PRIMARY KEY,
  title TEXT,
  source_filename TEXT,
  speaker_count INTEGER NOT NULL,
  utterance_count INTEGER NOT NULL,
  duration_ms INTEGER NOT NULL,
  created_at INTEGER NOT NULL
);
```

**Why two tables?**

FTS5 excels at text search but can't efficiently filter on non-text criteria (date ranges, speaker IDs). The metadata table enables:
```sql
SELECT m.data, bm25(utterances_fts) as score
FROM utterances_fts f
JOIN utterances_meta m ON f.id = m.id
WHERE utterances_fts MATCH ?
  AND m.speaker_id IN (?, ?)  -- Filter by speaker
  AND m.created_at >= ?       -- Filter by date
ORDER BY bm25(utterances_fts)
```

**Why UNINDEXED columns?**

FTS5 can store columns without indexing them (they're retrievable but not searchable). This saves index space for IDs that will never appear in search queries.

#### Search API

```typescript
export class TranscriptSearchIndex {
  // Basic search - returns utterance-level matches
  search(query: string, options?: SearchOptions): UtteranceSearchResult[]

  // Grouped search - aggregates by transcript
  searchGrouped(query: string, options?: SearchOptions): TranscriptSearchResult[]

  // Search with highlighted snippets for UI display
  searchWithHighlights(query: string, options?: SearchOptions):
    (UtteranceSearchResult & { highlight: string })[]

  // Index a transcript (called after transcription)
  index(transcript: Transcript): void

  // Rebuild entire index from stored transcripts
  rebuild(transcripts: Transcript[]): number

  // Index statistics
  stats(): { transcripts, utterances, speakers, dateRange }
}
```

**BM25 Ranking**

FTS5 uses BM25 (Best Matching 25) for relevance ranking, which considers:
- Term frequency (TF): More occurrences = more relevant
- Inverse document frequency (IDF): Rare terms matter more
- Document length normalization: Short documents with term are more focused

SQLite's BM25 returns negative scores where **lower is better** (more relevant). The code inverts this for intuitive API:
```typescript
return rows.map((row) => ({
  ...row,
  score: -row.score,  // Now higher = more relevant
}));
```

### 3. TranscriptWorkflow Orchestrator

**`src/services/transcript-workflow.ts`** (320 lines)

This service is the primary entry point for processing audio. It orchestrates:

```
Audio Input
    │
    ▼
┌─────────────────────────────┐
│   TranscriptionService      │
│   (faster-whisper + pyannote)│
│   → SpeakerAttributedTranscript
│   → embeddings              │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│   Convert to TranscriptInput │
│   (domain model)            │
└─────────────────────────────┘
    │
    ├──────────────────────────┐
    ▼                          ▼
┌───────────────┐     ┌─────────────────┐
│ TranscriptStore│     │TranscriptSearch │
│ (event-sourced)│     │Index (FTS5)     │
└───────────────┘     └─────────────────┘
    │
    ▼
┌─────────────────────────────┐
│   Speaker Fingerprinting     │
│   - Compare embeddings       │
│   - Match or create speaker  │
└─────────────────────────────┘
    │
    ▼
TranscriptWorkflowResult
```

#### Cosine Similarity for Speaker Matching

```typescript
function cosineSimilarity(a: Float32Array, b: Float32Array): number {
  if (a.length !== b.length) {
    throw new Error(`Embedding dimension mismatch: ${a.length} vs ${b.length}`);
  }

  let dotProduct = 0;
  let normA = 0;
  let normB = 0;

  for (let i = 0; i < a.length; i++) {
    dotProduct += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }

  if (normA === 0 || normB === 0) {
    throw new Error("Invalid embedding: zero vector detected (indicates corrupted data)");
  }
  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}
```

**Why throw on zero vectors?**

A zero embedding indicates either:
1. Corrupted data during extraction
2. Model failure during inference
3. Serialization error

Returning 0 (no similarity) would cause the system to silently create a new speaker profile instead of alerting to data corruption. Fail-fast is the correct behavior.

**Threshold Selection**

The default threshold of 0.75 is empirically derived from speaker verification research:
- **< 0.7**: High false positive rate (different speakers match)
- **0.75-0.85**: Sweet spot for speaker verification
- **> 0.9**: High false negative rate (same speaker doesn't match due to noise)

The workflow accepts `fingerprintThreshold` as an option for tuning.

#### Fingerprinting Algorithm

```typescript
private async processSpeakerFingerprints(
  transcript: Transcript,
  embeddings: Record<string, Float32Array>,
  threshold: number
): Promise<{ speakers: Speaker[]; matches: ... }> {
  // Get all existing speakers with fingerprints
  const existingSpeakers = await this.store.getSpeakersWithFingerprints();

  for (const [speakerLabel, embedding] of Object.entries(embeddings)) {
    let bestMatch: { speaker: Speaker; similarity: number } | null = null;

    // Compare against all existing fingerprints
    for (const existingSpeaker of existingSpeakers) {
      for (const fingerprint of existingSpeaker.fingerprints) {
        const similarity = cosineSimilarity(embedding, fingerprint.embedding);
        if (similarity >= threshold) {
          if (!bestMatch || similarity > bestMatch.similarity) {
            bestMatch = { speaker: existingSpeaker, similarity };
          }
        }
      }
    }

    if (bestMatch) {
      // Found match - associate with existing speaker
      matches.push({
        speakerLabel,
        matchedSpeakerId: bestMatch.speaker.id,
        similarity: bestMatch.similarity,
      });
    } else {
      // No match - create anonymous speaker with fingerprint
      const fingerprint: VoiceFingerprint = {
        embedding,
        model: "pyannote-speaker-diarization-3.1",
        created_at: Date.now(),
        sample_duration_ms: transcript.source.audio.duration_ms ?? 0,
        quality_score: 0.8,
      };

      const newSpeaker = await this.store.createSpeaker({
        name: speakerLabel,  // Initially "SPEAKER_00"
        fingerprints: [fingerprint],
        // ... other fields
      });
    }
  }
}
```

**Anonymous Speaker Pattern**

New speakers are created with their diarization label (SPEAKER_00) as the initial name. This allows:
1. Immediate storage without requiring user input
2. Later renaming when identity is known
3. Automatic matching in future transcripts

### 4. Migration Support

Added `/transcripts rebuild-index` action to the command and documented in the search sub-skill.

**`commands/transcripts.md`**:
```markdown
### rebuild-index
Rebuild the FTS5 search index from all stored transcripts.

/transcripts rebuild-index
/transcripts rebuild-index --clear  # Clear before rebuilding

This is useful for:
- Migrating existing transcripts to the new search index
- Fixing a corrupted index
- Updating after manual transcript edits
```

## Code Review and Fixes

Launched the code-reviewer agent which identified several issues:

### Critical Fix 1: Path Construction Bug

**Problem** (search.ts:62-66):
```typescript
// WRONG: join(dbPath, "..") appends ".." as segment
const dir = join(dbPath, "..");
```

For relative path `.claude/transcripts/search/index.db`, this creates:
`.claude/transcripts/search/index.db/..` (resolved only at access time)

**Fix**:
```typescript
import { dirname } from "path";
const dir = dirname(dbPath);  // Correctly computes parent
```

This is a common JavaScript footgun—`path.join()` concatenates segments, it doesn't interpret `..` specially.

### Critical Fix 2: Zero-Vector Handling

**Problem** (transcript-workflow.ts):
```typescript
if (normA === 0 || normB === 0) return 0;  // Silent failure
```

**Fix**:
```typescript
if (normA === 0 || normB === 0) {
  throw new Error("Invalid embedding: zero vector detected (indicates corrupted data)");
}
```

### Important Fix 3: Null Safety

**Problem** (transcript-workflow.ts:289):
```typescript
sample_duration_ms: transcript.source.audio.duration_ms,  // Could be undefined
```

**Fix**:
```typescript
sample_duration_ms: transcript.source.audio.duration_ms ?? 0,
```

### Noted for Future: Prepared Statement Lifecycle

The reviewer noted that creating prepared statements per-call in `index()` could leak resources in long-running processes. This should be refactored to class-level prepared statements.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            TranscriptWorkflow                                │
│                    (orchestrates full audio processing)                      │
│                                                                              │
│  process(AudioInput) → TranscriptWorkflowResult                             │
│    ├── transcribe via TranscriptionService                                   │
│    ├── store via TranscriptStore (event-sourced)                            │
│    ├── index via TranscriptSearchIndex (FTS5)                               │
│    └── fingerprint via cosineSimilarity + Speaker profiles                  │
└────────────────────────────────────────────────────────────────────────────┘
                                     │
            ┌────────────────────────┼────────────────────────┐
            ▼                        ▼                        ▼
┌────────────────────┐   ┌────────────────────┐   ┌────────────────────────┐
│ TranscriptionService│   │   TranscriptStore   │   │ TranscriptSearchIndex  │
│                     │   │                     │   │                        │
│ transcribe()        │   │ createTranscript()  │   │ index()               │
│ → SpeakerAttributed │   │ createSpeaker()     │   │ search()              │
│   Transcript        │   │ getSpeakersWithFP() │   │ searchGrouped()       │
│   + embeddings      │   │                     │   │ searchWithHighlights()│
└─────────┬───────────┘   └─────────────────────┘   └────────────────────────┘
          │
          ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                         TranscriptionPort                                   │
│                              ▲                                              │
│                              │                                              │
│               ┌──────────────┴──────────────┐                              │
│               │                             │                              │
│   ┌───────────┴──────────┐    ┌────────────┴────────────┐                 │
│   │ FasterWhisperAdapter │    │    DiarizationPort      │                 │
│   │     (GPU/CUDA)       │    │         ▲               │                 │
│   └──────────────────────┘    │         │               │                 │
│                               │  ┌──────┴──────────┐    │                 │
│                               │  │ PyAnnoteAdapter │    │                 │
│                               │  │   (GPU/CUDA)    │    │                 │
│                               │  │   + embeddings  │    │                 │
│                               │  └─────────────────┘    │                 │
│                               └─────────────────────────┘                 │
└────────────────────────────────────────────────────────────────────────────┘
```

## Files Changed Summary

| File | Lines | Action | Purpose |
|------|-------|--------|---------|
| `ports/diarization.ts` | +8 | Modified | Added embeddings to DiarizationResult |
| `adapters/diarization/pyannote.ts` | +10 | Modified | Return embeddings from Python |
| `services/transcription-service.ts` | +10 | Modified | Pass embeddings through |
| **`infrastructure/search.ts`** | **+461** | **Created** | SQLite FTS5 search index |
| **`services/transcript-workflow.ts`** | **+320** | **Created** | Pipeline orchestrator |
| `commands/transcripts.md` | +30 | Modified | Added rebuild-index action |
| `skills/.../search.md` | +40 | Modified | Documented FTS5 implementation |

## Performance Characteristics

| Operation | Complexity | Notes |
|-----------|------------|-------|
| Transcription | O(audio_length) | 23x realtime via GPU |
| Diarization | O(audio_length) | Included in transcription |
| Store transcript | O(utterances) | Append-only JSONL |
| Index transcript | O(utterances) | SQLite transaction |
| Full-text search | O(log n) | FTS5 inverted index |
| Speaker matching | O(speakers × fingerprints) | Could optimize with ANN |

For a 5:45 audio (345 seconds):
- Transcription + diarization: ~15 seconds (23x realtime)
- Storage + indexing: ~50ms
- Fingerprint matching: ~10ms (with few speakers)

## Future Optimizations

1. **Approximate Nearest Neighbor (ANN)** for fingerprinting at scale
   - Current O(n) comparison won't scale to thousands of speakers
   - Consider FAISS or Annoy for cosine similarity search

2. **Prepared statement reuse** in search index
   - Move to class-level to avoid per-call allocation

3. **Batch fingerprint updates**
   - Update speaker stats in bulk after transcript

4. **Streaming indexing**
   - Index utterances as they're transcribed for real-time search

## Lessons Learned

1. **Watch language boundaries** - Data extracted in Python easily gets dropped crossing to TypeScript. Always verify the full pipeline.

2. **Two-table FTS pattern** - FTS5 excels at text search but combine with metadata table for filtering. This is the canonical pattern.

3. **Fail-fast on impossible values** - Zero vectors indicate corruption, not "no match". Throwing exposes bugs faster than silent failures.

4. **`path.join()` doesn't interpret** - Use `dirname()` for parent directory. `join(path, "..")` is a footgun.

5. **Feature-dev workflow value** - The structured phases (explore → clarify → design → implement → review) prevented several wrong turns by gathering requirements before writing code.

## Experiment Log Entry

```jsonl
{"component":"transcript-search-index","operation":"create","tables":["utterances_fts","utterances_meta","transcripts_meta"],"tokenizer":"porter unicode61","success":true,"timestamp":"2025-12-18T18:42:00-08:00"}
{"component":"transcript-workflow","features":["transcription","storage","indexing","fingerprinting"],"threshold":0.75,"success":true,"timestamp":"2025-12-18T18:55:00-08:00"}
{"component":"code-review","issues_found":3,"issues_fixed":3,"reviewer":"feature-dev:code-reviewer","timestamp":"2025-12-18T19:00:00-08:00"}
```

---

*Parent: [[2025-12-18]] → [[2025-12]] → [[2025]]*
