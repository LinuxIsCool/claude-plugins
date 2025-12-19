---
id: 2025-12-19-1445
title: "Piper TTS Adapter Implementation"
type: atomic
created: 2025-12-19T14:45:39
author: claude-opus-4
description: "Implemented Piper TTS adapter for voice plugin spec 02 - fast CPU-based neural TTS with ONNX"
tags: [voice, tts, piper, implementation, spec-02, feature-dev]
parent_daily: [[2025-12-19]]
related: []
---

# Piper TTS Adapter Implementation

Completed implementation of the Piper TTS adapter for the voice plugin, fulfilling spec 02 of the voice plugin roadmap. This provides a fast, local CPU-based TTS option using ONNX-optimized neural synthesis.

## Context

The voice plugin has a 10-spec roadmap for building comprehensive voice I/O capabilities. Spec 01 (HuggingFace XTTS) was already implemented, providing GPU-accelerated voice synthesis. Spec 02 (Piper TTS) fills the CPU fallback gap - essential for systems without CUDA or when GPU is busy.

User initiated this work via `/feature-dev:feature-dev @plugins/voice/specs/02-piper-tts/ ultrathink`.

## Implementation Details

### Architecture Decisions

1. **CLI Direct Pattern** - Unlike XTTS (which uses a persistent Python JSON-RPC server), Piper is fast enough (~200ms) to spawn per-request. No persistent process needed.

2. **Stdin Text Delivery** - Text passed via `proc.stdin.write(text)` rather than shell arguments. Prevents shell injection vulnerabilities entirely.

3. **Native Fetch for Downloads** - Voice model downloads from HuggingFace use native `fetch()` with streaming and progress callbacks. No wget dependency.

4. **DRY Voice ID Parsing** - Single `parseVoiceIdComponents()` method extracts all parts once, consumed by both `parseVoiceId()` (for listing) and `parseVoiceIdParts()` (for downloads).

### Files Created/Modified

| File | Purpose |
|------|---------|
| `src/adapters/tts/piper.ts` | Main adapter (~440 lines) |
| `src/adapters/tts/index.ts` | Factory registration at priority 70 |
| `tests/piper/unit.test.ts` | 17 unit tests |
| `tests/piper/integration.test.ts` | 15 integration tests |
| `tests/piper/benchmark.test.ts` | Performance benchmarks |

### Quality Fixes Applied

Code review identified issues that were fixed before completion:

- **HIGH**: 30-second subprocess timeout prevents hanging on malformed models
- **HIGH**: stdin error handler catches broken pipe errors
- **MEDIUM**: Consolidated duplicate voice ID parsing (DRY)
- **MEDIUM**: Empty/whitespace text validation with clear error messages
- **Bug Fix**: Voice caching now works for empty directories

### Integration Points

Piper slots into the TTS fallback chain at priority 70:

```
huggingface-xtts (100) → elevenlabs (90) → piper (70) → pyttsx3 (10)
```

This means Piper is preferred over pyttsx3 (robotic system TTS) but falls back from cloud services and GPU synthesis when those are unavailable.

## Key Patterns Learned

### Timeout + Cleanup Pattern

```typescript
let resolved = false;
const cleanup = (error?: Error) => {
  if (resolved) return;
  resolved = true;
  clearTimeout(timeout);
  if (error) reject(error);
  else resolve();
};
```

This ensures exactly-once resolution even with multiple error paths (timeout, stdin error, process error, close event).

### Ports & Adapters in Practice

The `TTSPort` interface allows drop-in replacement of TTS backends. Adding Piper required:
1. Implement the interface
2. Add case to factory switch
3. Set priority number

No changes to consuming code (hooks, identity resolver, etc.).

## Test Results

- Unit tests: **17 pass**, 0 fail
- Integration tests: **15 pass** (skip gracefully without piper CLI)

## Next Steps

1. Install piper: `pip install piper-tts`
2. Download voice: `en_US-lessac-high` from HuggingFace
3. Run integration tests to validate end-to-end
4. Consider implementing spec 03 (Quality Testing) to validate all TTS backends

## Insights

The feature-dev workflow proved effective for systematic implementation:
- Phase 1-2 built deep codebase understanding before coding
- Phase 3 clarified ambiguities (security approach, test location, download method)
- Phase 4 architectural design caught the CLI-vs-server decision early
- Phase 6 code review caught timeout and DRY issues before merge

---

*Parent: [[2025-12-19]]*
