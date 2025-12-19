---
id: 2025-12-19-1240
title: "Voice Hook Overlapping Audio Fix"
type: atomic
created: 2025-12-19T12:40:00
author: opus
description: "Fixed multiple bugs causing overlapping voice output and truncated responses in voice plugin hooks"
tags: [voice, hooks, audio, debugging, tts]
parent_daily: [[2025-12-19]]
related: [[2025-12-19-1108-voice-plugin-tts-logging]]
---

# Voice Hook Overlapping Audio Fix

## Problem Statement

User reported two related issues with the voice plugin:
1. **Truncated responses**: Voice output saying "I'll start by understanding..." (thinking output) instead of final responses
2. **Overlapping audio**: Opening a new Claude Code session caused 3-4 voice messages to play simultaneously, creating chaotic overlapping speech

## Root Cause Analysis

### Issue 1: Truncated/Wrong Text

The `getSubagentInfo` function in `voice-hook.ts` was collecting ALL text blocks from ALL transcript entries, then taking the last one:

```typescript
// OLD: Collected from ALL entries
for (const line of lines) {
  // ...collected text from every message
}
result.summary = summarizeForVoice(responses[responses.length - 1]);
```

This captured intermediate thinking/planning output rather than the final response.

### Issue 2: Overlapping Audio

Two layers of duplication:

1. **Multiple cached plugin versions**: Found 6 stale cached versions of `explanatory-output-style` plugin, each registering its own SessionStart hook

2. **Concurrent audio playback**: Multiple events (SessionStart, Notification, SubagentStop) could trigger TTS calls in rapid succession. Each spawned its own `mpv` process, all playing simultaneously

## Solutions Implemented

### Fix 1: Correct Text Extraction

Rewrote `getSubagentInfo` to iterate in **reverse** and find the LAST assistant message, collecting all its text blocks:

```typescript
// NEW: Find LAST assistant message specifically
for (let i = lines.length - 1; i >= 0; i--) {
  const entry = JSON.parse(lines[i]);
  if (entry.type !== "assistant") continue;

  // Collect ALL text blocks from THIS message only
  const textParts: string[] = [];
  for (const block of entry.message?.content || []) {
    if (block.type === "text" && !text.startsWith("<system-reminder>")) {
      textParts.push(text);
    }
  }

  if (textParts.length > 0) {
    result.summary = summarizeForVoice(textParts.join("\n\n"));
    break;  // Stop at first (last) assistant message with text
  }
}
```

Applied same fix to `extractResponse` for Stop events.

### Fix 2: Hook-Level Lock

Added lock file mechanism to prevent duplicate hook triggers:

```typescript
const LOCK_DIR = "/tmp/claude-voice-locks";

async function acquireLock(sessionId: string, event: string): Promise<boolean> {
  const lockFile = `${LOCK_DIR}/${sessionId}-${event}.lock`;
  // Check if lock exists and is recent (<30s)
  // If recent, skip (another instance handling)
  // Otherwise, acquire lock
}
```

### Fix 3: Global Audio Playback Lock

Added global audio mutex in `base.ts` that ensures only ONE audio plays at a time across ALL Claude instances:

```typescript
const AUDIO_LOCK_FILE = "/tmp/claude-voice-audio.lock";

async function killCurrentAudio(): Promise<void> {
  // Kill any mpv/ffplay processes playing our temp audio
  execSync("pkill -f 'mpv.*/tmp/claude-voice/audio-'", { stdio: "ignore" });
}

async function acquireAudioLock(): Promise<boolean> {
  if (existsSync(AUDIO_LOCK_FILE)) {
    // Lock exists - kill current audio and take over
    await killCurrentAudio();
  }
  writeFileSync(AUDIO_LOCK_FILE, `${process.pid}\n${Date.now()}`);
  return true;
}
```

### Fix 4: Cache Cleanup

Cleared stale plugin caches:
- `~/.claude/plugins/cache/claude-plugins-official/explanatory-output-style/` (6 versions!)
- `~/.claude/plugins/cache/claude-plugins-official/ralph-wiggum/`
- `~/.claude/plugins/cache/claude-plugins-official/hookify/`

## Improved Logging

Enhanced voice hook logging:
- Always writes to `/tmp/voice-hook.log` (not just in DEBUG mode)
- Each invocation gets unique 6-char ID for tracing
- Lock acquisition/release logged for debugging

## Files Modified

| File | Changes |
|------|---------|
| `plugins/voice/hooks/voice-hook.ts` | Text extraction fix, hook locks, improved logging |
| `plugins/voice/src/adapters/tts/base.ts` | Global audio playback lock |

## Verification

After fixes, logs show:
- Single invocation ID per event (no duplicates)
- One mpv process at a time (no overlap)
- Correct final response text (not thinking output)
- Lock files properly acquired/released

## Lessons Learned

1. **Plugin cache hygiene matters**: Stale cache versions can cause unexpected duplicate hook registrations
2. **Audio needs global coordination**: Multiple processes/sessions sharing audio output require system-wide locking
3. **Transcript parsing is tricky**: Claude's responses have multiple text blocks per message; must collect all, not just first

---

*Parent: [[2025-12-19]] -> [[2025-12]] -> [[2025]]*
