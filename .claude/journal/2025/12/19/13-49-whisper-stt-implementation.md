---
id: 2025-12-19-1349
title: "Whisper STT Adapter Implementation"
type: atomic
created: 2025-12-19T13:49:00
author: claude-opus-4
description: "Implemented full Whisper speech-to-text adapter with batch and streaming modes for voice plugin"
tags: [voice, stt, whisper, implementation, hexagonal-architecture, json-rpc]
parent_daily: [[2025-12-19]]
related:
  - [[13-00-huggingface-xtts-implementation]]
---

# Whisper STT Adapter Implementation

Completed implementation of a full-featured Whisper speech-to-text adapter for the voice plugin, following the established hexagonal architecture pattern.

## Context

The voice plugin needed STT (speech-to-text) capabilities to complement its existing TTS (text-to-speech) backends. The spec at `plugins/voice/specs/05-whisper-stt/SPEC.md` defined the requirements, but the user requested enhancements beyond the original scope:

- **All 4 AudioInput types** (file, buffer, url, stream) instead of just file/buffer
- **Full streaming support** instead of batch-only for v1
- **Use existing ML venv** (`~/.venvs/ml/bin/python`) for consistency with XTTS
- **Persistent process model** to amortize model loading time

## Implementation

### Files Created

| File | Lines | Purpose |
|------|-------|---------|
| `src/adapters/stt/base.ts` | 165 | Shared utilities for audio input handling |
| `src/adapters/stt/whisper.ts` | 540 | TypeScript adapter implementing STTPort |
| `src/adapters/stt/whisper_server.py` | 430 | Python inference server with faster-whisper |
| `src/adapters/stt/index.ts` | 200 | Factory with priority-based fallback |

### Architecture Decisions

1. **JSON-RPC over stdin/stdout** - Same pattern as XTTS adapter. Python process stays alive, model stays loaded. First request takes 5-60s (model loading), subsequent requests <2s.

2. **Session-based streaming** - Each `transcribeStream()` call gets a unique session ID. Python spawns a worker thread per session. Audio chunks sent as JSON-RPC notifications (no response expected). Segment events emitted back as notifications.

3. **Timeout protection** - Stream event consumer loop has timeout to prevent infinite hangs if Python crashes. Cancellation sent to Python on error to clean up orphaned worker threads.

4. **Unified segment conversion** - Extracted `_segment_to_dict()` helper in Python to eliminate code duplication between batch and streaming modes.

### Key Code Patterns

**AudioInput normalization** (base.ts):
```typescript
// All 4 input types → file path for Whisper
async function audioInputToFile(input: AudioInput): Promise<[string, boolean]> {
  switch (input.type) {
    case "file":   return [input.path, false];  // No cleanup
    case "buffer": return [writeToTempFile(input.data), true];
    case "url":    return [await downloadToTempFile(input.url), true];
    case "stream": return [await streamToTempFile(input.stream), true];
  }
}
```

**Streaming event loop** (whisper.ts):
```typescript
// Yield events with timeout protection
while (!streamState.completed || streamState.eventQueue.length > 0) {
  if (Date.now() - startTime > timeout) {
    throw new Error(`Stream timeout after ${timeout}ms`);
  }
  if (streamState.eventQueue.length > 0) {
    yield streamState.eventQueue.shift()!;
  } else {
    await new Promise(r => setTimeout(r, 50));
  }
}
```

**Python streaming** (whisper_server.py):
```python
# Worker thread processes audio chunks
while not session.cancelled:
    if session.is_final or enough_audio_accumulated:
        segments = model.transcribe(temp_file)
        for segment in segments:
            send_stream_event(session_id, segment)
```

## Insights

### Streaming Complexity

Real-time streaming with Whisper is fundamentally chunked batch processing, not true sample-by-sample streaming. The model processes accumulated audio in chunks (~1 second intervals). True real-time STT requires different architectures (Vosk, Deepgram WebSocket).

### Model Size Trade-offs

| Model | Load Time | Speed (30s audio) | WER |
|-------|-----------|-------------------|-----|
| tiny | 5s | 1s | 15-20% |
| small | 15s | 4s | 5-8% |
| large-v3 | 60s | 20s | 3-4% |

Defaulted to `small` for best balance. Users can configure via `WhisperConfig.model`.

### Resource Management

The persistent process pattern requires careful cleanup:
- Process exit handler rejects all pending requests
- Stream cancellation sent to Python on TypeScript error
- Temp files cleaned in `finally` blocks
- Session state tracked with timeout protection

## Quality Review Findings

Three code reviewers identified issues:

1. **Stream timeout missing** (95% confidence) - Fixed with timeout in event loop
2. **Orphaned worker threads** (95% confidence) - Fixed with cancel_stream on error
3. **Segment duplication** (95% confidence) - Fixed with `_segment_to_dict()` helper
4. **Missing interface method** (100% confidence) - Added `getWithFallback` to STTBackendFactory
5. **Buffer format docs** (90% confidence) - Added documentation about format handling

## Usage

```typescript
// Batch transcription
import { transcribe } from "@plugins/voice/stt";
const result = await transcribe({ type: "file", path: "/tmp/audio.wav" });

// Streaming transcription
import { transcribeStream } from "@plugins/voice/stt";
for await (const event of transcribeStream({ type: "file", path: "/tmp/audio.wav" })) {
  if (event.type === "partial") console.log("...", event.text);
  if (event.type === "final") console.log("Final:", event.segment.text);
}
```

## Next Steps

- [ ] Integration test with real audio files
- [ ] GPU acceleration verification with large models
- [ ] Hook into voice feedback loop
- [ ] Implement Deepgram adapter for true real-time streaming

---

*Parent: [[2025-12-19]]*
