---
id: 2025-12-19-1503
title: "Voice Daemon v0.1: Complete Implementation and Testing"
type: atomic
created: 2025-12-19T15:03:08
author: claude-opus-4
description: "Full implementation of the voice daemon with audio capture, VAD, STT pipeline - from spec to tested production code"
tags: [voice-plugin, daemon, vad, stt, audio-processing, feature-dev, testing, bug-fix]
parent_daily: [[2025-12-19]]
related:
  - [[13-49-whisper-stt-implementation]]
  - [[13-50-vad-integration-implementation]]
---

# Voice Daemon v0.1: Complete Implementation and Testing

Implemented and tested a fully functional voice daemon that provides continuous speech-to-text transcription. The daemon captures audio from the microphone, detects speech using VAD, and transcribes using Whisper STT.

## Implementation Overview

### Files Created

| File | Lines | Purpose |
|------|-------|---------|
| `src/daemon/types.ts` | 103 | Type definitions for config, state, events, handlers |
| `src/daemon/config.ts` | 214 | YAML configuration loader with defaults and validation |
| `src/daemon/audio_capture.py` | 92 | Python audio capture using sounddevice |
| `src/daemon/audio-input.ts` | 257 | TypeScript subprocess wrapper with binary protocol |
| `src/daemon/daemon.ts` | 475 | Main pipeline orchestrator with state machine |
| `src/daemon/start-daemon.ts` | 90 | CLI entry point with argument parsing |
| `src/daemon/index.ts` | 13 | Module exports |

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Voice Daemon v0.1                        │
│                                                              │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐     │
│  │ AudioInput   │──▶│   Silero     │──▶│   Whisper    │──▶📝│
│  │ (Python)     │   │    VAD       │   │    STT       │     │
│  │              │   │              │   │              │     │
│  │ sounddevice  │   │ processStream│   │ transcribe() │     │
│  │ → PCM chunks │   │ → segments   │   │ → text       │     │
│  └──────────────┘   └──────────────┘   └──────────────┘     │
│         │                  │                                 │
│         ▼                  ▼                                 │
│  ┌──────────────┐   ┌──────────────┐                        │
│  │ AudioBuffer  │◀──│pcmToWav()    │                        │
│  │ (rolling     │   │ 44-byte hdr  │                        │
│  │  window)     │   │ conversion   │                        │
│  └──────────────┘   └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## Technical Decisions

### 1. Binary Protocol for Audio (not JSON-RPC)

The audio capture uses a binary protocol instead of the JSON-RPC pattern used by VAD/STT:

```python
# 4-byte little-endian length + raw PCM data
chunk = struct.pack("<I", length) + pcm_data
sys.stdout.buffer.write(chunk)
```

**Rationale:** Base64 encoding in JSON adds 33% overhead. For continuous 16kHz mono audio at ~32KB/s, this would waste significant bandwidth. The binary protocol is more efficient for streaming.

### 2. PCM to WAV Conversion

Whisper (via FFmpeg) cannot read raw PCM without knowing sample rate, channels, and bit depth. The daemon converts PCM to WAV before transcription:

```typescript
function pcmToWav(pcmData: Buffer, sampleRate: number, channels: number): Buffer {
  const header = Buffer.alloc(44);
  header.write("RIFF", 0);
  header.writeUInt32LE(36 + pcmData.length, 4);
  header.write("WAVE", 8);
  // ... fmt chunk with sample rate, channels, bit depth
  header.write("data", 36);
  header.writeUInt32LE(pcmData.length, 40);
  return Buffer.concat([header, pcmData]);
}
```

### 3. AudioBuffer with Timestamp-Based Extraction

The daemon buffers audio chunks with timestamps to extract speech segments after VAD detection:

```typescript
extractSegment(segment: SpeechSegment): Buffer {
  const margin = 100; // 100ms for timing jitter
  const relevantChunks = this.chunks.filter(
    (c) => c.timestampMs >= segment.startMs - margin &&
           c.timestampMs < segment.endMs + margin
  );
  // Concatenate and return
}
```

The margin accounts for:
- Timestamp jitter between processes
- VAD padding (speechPadMs)
- Chunk boundaries not aligning exactly with speech

### 4. Tee Pattern for Audio Flow

Audio flows to both the buffer and VAD simultaneously using an async generator tee:

```typescript
async function* teeStream(
  stream: AsyncGenerator<AudioChunk>,
  buffer: AudioBuffer
): AsyncGenerator<AudioChunk> {
  for await (const chunk of stream) {
    if (!self.running) break;
    buffer.push(chunk);
    yield chunk;
  }
}
```

## Issues Encountered and Resolved

### Issue 1: HTTP 401 from torch.hub

**Symptom:** Silero VAD failed to load with "HTTP Error 401: Unauthorized"

**Root Cause:** `torch.hub` doesn't set a User-Agent header. GitHub returns 401 to requests without proper User-Agent (anti-bot measure).

**Fix:** Manually downloaded the Silero model to cache:
```python
# Manually download with User-Agent
req = urllib.request.Request(archive_url)
req.add_header('User-Agent', 'Python/torch-hub')
# Extract to ~/.cache/torch/hub/snakers4_silero-vad_master/
```

### Issue 2: "Invalid data found when processing input"

**Symptom:** Whisper failed with FFmpeg error code 1094995529

**Root Cause:** Raw PCM was written to a `.pcm` file. FFmpeg cannot decode raw PCM without format metadata.

**Fix:** Added `pcmToWav()` conversion before STT:
```typescript
const wavData = pcmToWav(audioData, sampleRate, channels);
await stt.transcribe({ type: "buffer", data: wavData, format: "wav" });
```

### Issue 3: Unbounded Buffer Growth

**Symptom:** Code review identified O(n²) buffer copying in audio-input.ts

**Root Cause:** Each chunk was copied to a new array:
```typescript
const newBuffer = new Uint8Array(buffer.length + value.length);
newBuffer.set(buffer);  // O(n) copy
```

**Fix:** Use array of chunks with consolidation on demand:
```typescript
const bufferChunks: Uint8Array[] = [];
bufferChunks.push(value);  // O(1) append
// Consolidate only when processing
```

### Issue 4: Reader Lock Not Released

**Symptom:** Code review identified resource leak in waitForReady()

**Root Cause:** stderr reader lock held on error path:
```typescript
if (done) {
  throw new Error("Process exited");  // Lock not released!
}
```

**Fix:** Pass reader through call chain instead of releasing and re-acquiring:
```typescript
if (line.includes("READY")) {
  // Continue with SAME reader for background logging
  this.logStderrWithReader(reader, decoder, buffer);
  return;
}
```

### Issue 5: Partial Writes on Signal

**Symptom:** Code review identified race condition in Python

**Root Cause:** Signal could arrive between length write and data write, leaving partial chunk

**Fix:** Combine into single atomic write:
```python
chunk = struct.pack("<I", length) + pcm_data
sys.stdout.buffer.write(chunk)  # Single write
```

## Testing Methodology

### Unit Tests

1. **CLI Interface:** Verified `--help` and `--sample-config` output
2. **pcmToWav:** Extracted PCM from WAV, reconverted, verified identical
3. **AudioBuffer:** Simulated chunk storage and segment extraction

### Integration Tests

1. **STT Direct:** Transcribed real speech from video file
   - Input: 10s audio from meeting recording
   - Output: "I slept good um I mean I went to bed at like one so I just woke up"

2. **Full Pipeline Simulation:**
   ```
   Read WAV → Extract PCM → Split 313 chunks → Buffer →
   Extract segment → pcmToWav → Transcribe → SUCCESS
   ```

3. **Daemon E2E:** Ran daemon, observed:
   - VAD loads on CUDA (0.6s)
   - STT loads on CUDA (0.7s)
   - Audio capture starts
   - State machine transitions correctly
   - Graceful shutdown on SIGTERM

### Limitations

- No live microphone testing (CI environment has no audio input)
- Verified using file-based audio and pipeline simulation
- Real-world testing requires actual microphone

## Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Silero VAD load | 0.6s | CUDA, cached model |
| Whisper STT load | 0.7s | CUDA float16, small model |
| 10s transcription | ~1s | After model loaded |
| Audio chunk latency | ~32ms | 512 samples @ 16kHz |

## Future Enhancements (v0.2+)

- **v0.2:** Wake word detection (Vosk/Porcupine)
- **v0.3:** Intent routing with TranscriptHandler interface (already scaffolded)
- **v1.0:** PM2 process management, systemd integration

## Code Quality Review

Three parallel code-reviewer agents identified 6 issues:
1. Memory leak (unbounded buffer) - Fixed
2. Resource leak (reader lock) - Fixed
3. Race condition (concurrent readers) - Fixed
4. Logic error (timestamp filtering) - Fixed
5. Resource leak (STT factory) - Documented (no disposeAll method)
6. Generator deadlock potential - Fixed

All high-confidence issues were addressed before testing.

## Insights

### Streaming Pipeline Design

The async generator composition pattern proved elegant for streaming:
```typescript
audioInput.stream() → teeStream() → vad.processStream() → handleVADEvent()
```

Each stage can apply backpressure naturally. If STT is slow, VAD yields less frequently, which slows audio consumption.

### Binary vs JSON for Audio

For discrete RPC calls (VAD process, STT transcribe), JSON-RPC is cleaner. For continuous streams (audio capture), binary protocols are essential. The daemon uses both appropriately.

### WAV as Interchange Format

WAV's 44-byte header is trivial to generate and universally supported. Converting PCM to WAV at the boundary between capture and STT was the right abstraction point.

---

*Parent: [[2025-12-19]] → [[2025-12]] → [[2025]]*
