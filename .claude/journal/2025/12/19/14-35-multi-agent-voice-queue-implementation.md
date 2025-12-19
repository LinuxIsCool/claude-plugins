---
id: 2025-12-19-1435
title: "Multi-Agent Voice Queue Implementation"
type: atomic
created: 2025-12-19T14:35:48
author: claude-opus-4
description: "Implemented priority-based voice queue daemon for coordinating speech across multiple Claude instances"
tags: [implementation, voice, coordination, daemon, ipc, priority-queue]
parent_daily: [[2025-12-19]]
related:
  - [[13-49-whisper-stt-implementation]]
  - [[13-50-vad-integration-implementation]]
---

# Multi-Agent Voice Queue Implementation

Completed the implementation of spec `07-multi-agent-queue` - a priority-based voice queue system that coordinates speech output across multiple Claude instances running simultaneously.

## Context

The voice plugin previously used file locks (`/tmp/claude-voice-audio.lock`) to prevent overlapping audio playback. This worked for single instances but created race conditions and uncoordinated output when multiple Claude subagents attempted to speak simultaneously. The user requested an OS-like scheduler approach with proper priority handling.

## Architecture Decisions

### Coordination-Only Daemon

The daemon **schedules but does not synthesize**. Each hook performs its own TTS; the daemon only determines playback order. This provides:

- **Fault isolation**: If TTS fails, only that hook fails, not the daemon
- **Simplicity**: Daemon is a pure scheduler, not a media pipeline
- **Flexibility**: Hooks can use different TTS backends without daemon modification

### Priority Levels (OS-Inspired)

```
CRITICAL (100) - System errors, security alerts (like SIGKILL)
HIGH (80)      - User requests, notifications
NORMAL (50)    - Agent responses
LOW (20)       - Background updates, greetings
AMBIENT (10)   - Optional enhancements
```

Higher priority items preempt lower ones. The `interruptThreshold` (default 80) determines when preemption occurs.

### IPC Design

Unix socket at `/tmp/claude-voice.sock` with JSON-over-newline protocol:

```
Client → Daemon: { type: "enqueue", requestId: "abc", payload: {...} }
Daemon → Client: { type: "queued", requestId: "abc", id: "vq-123", position: 0 }
Daemon → Client: { type: "play_now", id: "vq-123", item: {...} }  // Push message
Client → Daemon: { type: "playback_complete", id: "vq-123", durationMs: 2500 }
```

Request IDs enable **concurrent request/response correlation** - a critical fix identified during code review.

### Interruption Policies

Three configurable behaviors when a higher-priority item preempts:

| Policy | Behavior |
|--------|----------|
| `drop` | Interrupted item is discarded |
| `requeue_front` | Re-queued at front (plays next) |
| `requeue_priority` | Re-inserted at priority position |

Default is `requeue_front` - mirrors OS process swapping where preempted processes resume when ready.

## Files Created

```
plugins/voice/src/coordination/
├── types.ts        # VoicePriority, QueueItem, IPC message types
├── config.ts       # QueueConfig with env var support
├── queue-manager.ts # Priority queue with OS-like scheduling
├── ipc-server.ts   # Unix socket server
├── client.ts       # Hook-side client with request correlation
├── launcher.ts     # Auto-start daemon management
├── daemon.ts       # Main daemon process
└── index.ts        # Public exports

plugins/voice/bin/
└── voice-daemon.ts # CLI entry point
```

## Code Review Fixes

Three code-reviewer agents identified 7 critical issues. All were fixed:

1. **Request/response correlation** - Added `requestId` to protocol; responses matched by ID, not first-pending
2. **VoiceConfig duplication** - Single source of truth via re-export from identity resolver
3. **Environment variables ignored** - All constructors now use `loadConfig()` instead of direct merge
4. **Hard-coded priority values** - Use `VoicePriority` enum in `getStats()`
5. **Silent JSON errors** - Added error logging for protocol debugging
6. **Fragile path resolution** - Simplified to single bin script path
7. **Missing exports** - Added `./coordination` to package.json

## Key Insight: Graceful Degradation

The hook-level integration (voice-hook.ts) uses a **queue-first, fallback-second** pattern:

```typescript
if (USE_QUEUE) {
  try {
    await speakViaQueue(text, priority, resolved);
    return;
  } catch {
    // Queue failed, fall back to direct playback
  }
}
// Fallback: Direct playback with file lock
await performTTS(text, resolved);
```

This ensures voice output continues working even if the daemon crashes. The fallback loses priority ordering but maintains basic functionality.

## Usage

```bash
# Manual daemon control
bun run daemon:start
bun run daemon:status
bun run daemon:stop

# Configuration via environment
VOICE_QUEUE_MAX_SIZE=100 bun run daemon:start
VOICE_QUEUE_INTERRUPTION_POLICY=drop bun run daemon:start
```

## Insights

The implementation revealed how voice coordination maps naturally to OS scheduling:

- Priority levels = process priorities
- Interrupt threshold = preemption policy
- Re-queue policies = process swapping strategies
- Speaker transitions = context switch overhead

The daemon pattern also enables future enhancements like voice mixing, cross-instance identity management, and conversation threading.

---

*Parent: [[2025-12-19]]*
