---
id: 2025-12-19-1350
title: "Silero VAD Integration: Production Architecture Implementation"
type: atomic
created: 2025-12-19T13:50:59
author: claude-opus-4
description: "Implemented Voice Activity Detection using Silero VAD with production-grade TypeScript/Python architecture"
tags: [voice-plugin, vad, silero, python-integration, hexagonal-architecture, feature-dev]
parent_daily: [[2025-12-19]]
related: [[13-00-huggingface-xtts-implementation]]
---

# Silero VAD Integration: Production Architecture Implementation

Completed implementation of Voice Activity Detection (VAD) for the voice plugin using Silero VAD model. This was a feature-dev guided implementation that resulted in a production-grade, reusable architecture.

## Context

The voice plugin needed VAD to detect speech segments in audio streams—a prerequisite for efficient STT (Speech-to-Text) processing. The spec at `plugins/voice/specs/06-vad-integration/SPEC.md` outlined requirements, but the existing codebase had its own patterns that needed consideration.

## Implementation Phases

### Phase 1: Discovery & Exploration

Three code-explorer agents analyzed:
1. **TTS/STT patterns** - Discovered XTTS uses JSON-RPC over stdin/stdout to Python
2. **Port interfaces** - Found existing `VADPort` at `ports/vad.ts` with different signature than spec
3. **Audio processing flow** - Understood `AudioChunk` format and streaming patterns

Key discovery: The existing `VADPort` interface used synchronous `process()` but our Python backend requires async. Solution: Use `processStream()` as the primary API.

### Phase 2: Architecture Decision

Chose **Production with base class** approach (~750 lines) over Minimal (~600 lines):

```
BasePythonProcessAdapter<TConfig>       (abstract base)
       ↓ extends
SileroVADAdapter                        (VAD implementation)
       ↓ uses
VADFactory                              (priority-based backend selection)
```

This extracts the JSON-RPC/process management pattern from XTTS for reuse, avoiding code duplication as more Python-backed adapters are added.

### Phase 3: Files Created

| File | Purpose | Lines |
|------|---------|-------|
| `src/adapters/base-python-process.ts` | Generic Python process management with JSON-RPC | ~440 |
| `src/adapters/vad/silero.ts` | Silero VAD adapter implementing VADPort | ~390 |
| `src/adapters/vad/silero_server.py` | Python server wrapping Silero model | ~255 |
| `src/adapters/vad/index.ts` | VADFactory with fallback chain | ~190 |

### Phase 4: Technical Patterns

**JSON-RPC 2.0 Protocol**
```typescript
// TypeScript sends
{"jsonrpc": "2.0", "id": 1, "method": "process", "params": {...}}

// Python responds
{"jsonrpc": "2.0", "id": 1, "result": {"is_speech": true, "probability": 0.95}}
```

**Speech Segment State Machine**
```
SILENCE ←→ SPEECH transitions based on:
- threshold: probability above which chunk is considered speech
- minSpeechDurationMs: minimum speech duration to emit segment
- minSilenceDurationMs: silence duration before ending segment
- speechPadMs: padding added to segment boundaries
```

**Audio Encoding**
- Base64 encoding for audio data in JSON (consistent with XTTS pattern)
- int16 PCM → float32 normalization: `audio_np.astype(np.float32) / 32768.0`

### Phase 5: Issues Found & Fixed

Code review (3 parallel agents) identified several issues:

1. **Config Duplication**: `sileroConfig` property duplicated base class config
   - Fix: Removed, use `this.config` directly

2. **`process` Naming Conflict**: Base class `process` (ChildProcess) vs VADPort `process()` method
   - Fix: Renamed to `pythonProcess` throughout base class

3. **Missing Error Events**: `processStream()` threw exceptions instead of yielding
   - Fix: Try-catch wrapper yields `{type: "error", error}` events

4. **Unbounded Buffer Growth**: Output buffer could grow indefinitely
   - Fix: Added `MAX_OUTPUT_BUFFER_SIZE = 1MB` with overflow handling

5. **Race Condition in `waitForReady()`**: Could resolve even if process died
   - Fix: Added `if (this.pythonProcess === null && !this.ready)` check

## Insights

### Hexagonal Architecture Pays Off

The port/adapter pattern allowed implementing against `VADPort` interface while making significant internal changes. Factory provides fallback chain for future backends (WebRTC, Pyannote).

### Python Process Lifecycle

Managing persistent Python processes requires careful attention to:
- Ready signal detection (JSON-RPC notification pattern)
- Graceful shutdown with pending request cleanup
- Process death handling with request rejection
- Environment setup (LD_LIBRARY_PATH for cuDNN)

### Deferred Refactoring

XTTS refactor to extend `BasePythonProcessAdapter` was started but reverted—the complexity and risk of breaking existing functionality wasn't justified. The base class proves the pattern; XTTS migration is a follow-up task.

## Next Steps

1. Write integration tests for VAD streaming
2. Implement VAD-gated STT pipeline
3. Consider WebRTC VAD as lightweight fallback
4. Eventually refactor XTTS to use base class

---

*Parent: [[2025-12-19]]*
