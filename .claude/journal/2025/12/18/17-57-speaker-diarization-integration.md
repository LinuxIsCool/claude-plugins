---
id: 2025-12-18-1757
title: "Speaker Diarization Integration Complete"
type: atomic
created: 2025-12-18T17:57:34-08:00
author: claude-opus-4
description: "Built PyAnnoteAdapter and TranscriptionService achieving 23x realtime speaker-attributed transcription"
tags: [transcripts-plugin, pyannote, diarization, faster-whisper, gpu, integration, hexagonal-architecture]
parent_daily: [[2025-12-18]]
related:
  - [[15-31-gpu-transcription-breakthrough]]
---

# Speaker Diarization Integration Complete

A culminating session that brought together GPU-accelerated transcription and speaker diarization into a unified, production-ready pipeline.

## Context

Building on the earlier GPU transcription breakthrough (where we resolved cuDNN library paths and got faster-whisper working with CUDA), this session focused on integrating pyannote speaker diarization and creating a service that produces speaker-attributed transcripts.

## What Was Built

### 1. PyAnnoteAdapter (`src/adapters/diarization/pyannote.ts`)

Implements the `DiarizationPort` interface following hexagonal architecture patterns established by `FasterWhisperAdapter`:

```typescript
export class PyAnnoteAdapter implements DiarizationPort {
  capabilities(): DiarizationCapabilities {
    return {
      max_speakers: 20,
      overlapping_speech: true,
      speaker_embedding: true,  // 256-dim vectors
      supports_streaming: false,
    };
  }

  async diarize(input: AudioInput, options?: DiarizationOptions): Promise<DiarizationResult>
}
```

**Key implementation details:**
- Spawns Python process with `LD_LIBRARY_PATH` injection for cuDNN
- Uses `torchaudio.load()` to bypass torchcodec's FFmpeg dependency
- Reads `HF_TOKEN` from environment or `.env` file for gated model access
- Extracts speaker embeddings (256-dimensional) for future voice fingerprinting

### 2. DiarizationFactory (`src/adapters/diarization/index.ts`)

Singleton factory pattern matching the transcription factory:

```typescript
export function getDiarizationFactory(): DiarizationFactory
export function getDefaultDiarizer(): DiarizationPort
```

### 3. TranscriptionService (`src/services/transcription-service.ts`)

Orchestrates transcription + diarization with speaker attribution:

```typescript
export class TranscriptionService {
  async transcribe(input: AudioInput, options?): Promise<SpeakerAttributedTranscript>
  formatAsText(transcript): string
  formatAsSRT(transcript): string
}
```

**Speaker attribution algorithm:**
1. Run transcription and diarization in parallel
2. For each utterance, find diarization segment with maximum temporal overlap
3. If no overlap, find closest segment by midpoint distance
4. Calculate per-speaker statistics (segment count, total duration)

## Performance Results

Tested on a 5:45 meeting recording (`audio-2025-05-30-darren-gaia-prep.mp4`):

| Metric | Value |
|--------|-------|
| Audio duration | 345 seconds |
| Processing time | 15.2 seconds |
| Speedup | **23x realtime** |
| Speakers detected | 2 (correct) |
| Utterance segments | 83 |

The pipeline correctly identified and separated two speakers throughout the conversation.

## Technical Challenges Solved

### 1. Pyannote Gated Models

Required accepting three separate HuggingFace licenses:
- `pyannote/speaker-diarization-3.1`
- `pyannote/segmentation-3.0`
- `pyannote/speaker-diarization-community-1`

### 2. torchcodec FFmpeg Dependency

Pyannote's default audio loading uses torchcodec which requires system FFmpeg libraries. Bypassed by loading audio with torchaudio and passing as in-memory dict:

```python
waveform, sr = torchaudio.load(file_path)
audio_input = {"waveform": waveform, "sample_rate": sr}
output = pipeline(audio_input)
```

### 3. DiarizeOutput API

The pyannote output structure changed between versions. Correct access pattern:

```python
for turn, _, speaker in output.speaker_diarization.itertracks(yield_label=True):
    # turn.start, turn.end in seconds
    # speaker is "SPEAKER_00", "SPEAKER_01", etc.
```

Speaker embeddings are a numpy array `(num_speakers, 256)`, not a dict.

## Architecture Insights

The transcripts plugin now demonstrates clean hexagonal architecture:

```
┌─────────────────────────────────────────────────┐
│              TranscriptionService               │
│         (orchestrates adapters)                 │
└────────────────┬────────────────┬───────────────┘
                 │                │
    ┌────────────▼────┐    ┌──────▼──────────┐
    │ TranscriptionPort│    │ DiarizationPort │
    │   (interface)    │    │   (interface)   │
    └────────────┬─────┘    └───────┬─────────┘
                 │                  │
    ┌────────────▼────┐    ┌───────▼─────────┐
    │FasterWhisperAdap│    │ PyAnnoteAdapter │
    │   (GPU/CUDA)    │    │   (GPU/CUDA)    │
    └─────────────────┘    └─────────────────┘
```

**Port/adapter separation** allows:
- Easy substitution of backends (whisper.cpp, OpenAI API, etc.)
- Mock adapters for testing
- Future streaming implementations

## Output Formats

The service supports multiple output formats:

**Markdown** (default):
```markdown
**SPEAKER_00** [0:14]
slides look amazing. I was thinking...

**SPEAKER_01** [0:30]
Well, we have like how long do we have?
```

**SRT subtitles**:
```
1
00:00:00,000 --> 00:00:01,200
[SPEAKER_00] I just leave.

2
00:00:01,200 --> 00:00:09,000
[SPEAKER_01] It's not good. I mean, I went to bed...
```

## Next Steps

1. **Voice fingerprinting** - Use speaker embeddings for cross-meeting speaker identification
2. **Search index** - SQLite FTS5 for full-text search across transcripts
3. **Entity extraction** - Named entity recognition for people, organizations, topics
4. **Storage persistence** - Event-sourced storage following messages plugin pattern

## Experiment Log

```jsonl
{"component":"pyannote-adapter","device":"cuda","audio_duration_s":30,"processing_ms":6112,"speakers_detected":2,"success":true}
{"component":"transcription-service","audio":"darren-gaia-prep","duration_s":345,"processing_s":15.2,"speedup":"23x","speakers_detected":2,"segments":83,"success":true}
```

---

*Parent: [[2025-12-18]]*
