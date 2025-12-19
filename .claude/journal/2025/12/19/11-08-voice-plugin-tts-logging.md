---
id: 2025-12-19-1108
title: "Voice Plugin: TTS Output and Structured Logging"
type: atomic
created: 2025-12-19T11:08:34-08:00
author: claude-opus-4
description: "Completed voice plugin TTS output with multi-backend support and comprehensive JSONL event logging for evaluation"
tags: [voice, tts, plugin, logging, hooks, elevenlabs]
parent_daily: [[2025-12-19]]
related: []
---

# Voice Plugin: TTS Output and Structured Logging

This morning's session completed the voice plugin's TTS output infrastructure with structured logging, enabling evaluation of voice synthesis performance as development continues.

## Context

The voice plugin was built in a previous session but wasn't functioning—no sound on session start, and the plugin wasn't visible in `/plugins`. This session focused on debugging plugin discovery, fixing hook integration, and implementing comprehensive logging.

## Plugin Discovery Debugging

The journey to get the plugin working revealed several critical details about Claude Code's plugin system:

### Issue 1: Plugin Not in Marketplace
The voice plugin wasn't registered in `.claude-plugin/marketplace.json`. Added the entry:
```json
{"name": "voice", "source": "./plugins/voice/"}
```

### Issue 2: Hook Format
Inline hooks in `plugin.json` don't work—Claude Code requires an external `hooks.json` file referenced via:
```json
"hooks": "./hooks/hooks.json"
```

The hooks file uses a specific nested structure:
```json
{
  "hooks": {
    "SessionStart": [{ "hooks": [{ "type": "command", "command": "bash ${CLAUDE_PLUGIN_ROOT}/hooks/voice-hook.sh SessionStart" }] }]
  }
}
```

### Issue 3: Stale Entry in installed_plugins.json
Even after correct configuration, the plugin wouldn't appear. Created a minimal test plugin (`test-minimal`) which worked immediately. The culprit: a stale `voice@linuxiscool-claude-plugins` entry in `~/.claude/plugins/installed_plugins.json` that blocked re-discovery. Removed it with a Python script, and "voice" then worked.

### Issue 4: Missing Directories
`plugin.json` referenced `"commands": ["./commands/"]` but the directory didn't exist, causing silent failures.

## TTS Architecture

The voice hook now handles four Claude Code events:

| Event | Trigger | Voice Output |
|-------|---------|--------------|
| `SessionStart` | New Claude session | "Ready." |
| `Stop` | Response complete | First 2-3 sentences of response |
| `Notification` | Attention needed | The notification message |
| `SubagentStop` | Agent completes | Summary of agent's work |

### Voice Identity Resolution

Three-tier resolution system (`plugins/voice/src/identity/resolver.ts`):

1. **Session-specific**: `.claude/voice/sessions/{session_id}.json`
2. **Agent-specific**: `.claude/voice/agents/{agent_type}.json`
3. **Model-based**: Different voices for opus/sonnet/haiku
4. **System default**: ElevenLabs Rachel voice

### Multi-Backend TTS

Adapters for:
- **ElevenLabs**: Primary, high-quality cloud TTS
- **pyttsx3**: Local fallback, no API key required

Factory pattern allows easy addition of new backends.

## Structured JSONL Logging

The core deliverable of this session—comprehensive event logging for evaluation.

### VoiceEvent Schema

```typescript
interface VoiceEvent {
  timestamp: string;        // ISO 8601
  session_id: string;       // Correlate with transcripts
  event: string;            // SessionStart, Stop, Notification, SubagentStop
  text: string;             // What was spoken
  text_length: number;      // Character count
  backend: string;          // elevenlabs, pyttsx3
  voice_id: string;         // Specific voice used
  voice_source: string;     // session, agent, model, system
  agent_id?: string;        // For SubagentStop events
  duration_ms?: number;     // TTS latency measurement
  success: boolean;
  error?: string;           // If failed
}
```

### Log Locations

**Daily logs** (partitioned for archival):
```
.claude/voice/YYYY/MM/DD/events.jsonl
```

**Global log** (for quick queries):
```
.claude/voice/events.jsonl
```

### Example Event

```json
{
  "timestamp": "2025-12-19T19:06:04.301Z",
  "session_id": "test-123",
  "event": "SessionStart",
  "text": "Ready.",
  "text_length": 6,
  "backend": "elevenlabs",
  "voice_id": "21m00Tcm4TlvDq8ikWAM",
  "voice_source": "system",
  "success": true,
  "duration_ms": 1211
}
```

### Analytics Queries

```bash
# Average latency by backend
cat .claude/voice/events.jsonl | jq -s 'group_by(.backend) | map({backend: .[0].backend, avg_ms: (map(.duration_ms) | add / length)})'

# Failure rate
cat .claude/voice/events.jsonl | jq -s '[.[] | .success] | (map(select(. == false)) | length) / length * 100'

# Events by type
cat .claude/voice/events.jsonl | jq -s 'group_by(.event) | map({event: .[0].event, count: length})'

# Text length distribution
cat .claude/voice/events.jsonl | jq -s 'map(.text_length) | sort | {min: .[0], max: .[-1], avg: (add / length)}'
```

## Files Modified

| File | Change |
|------|--------|
| `plugins/voice/hooks/voice-hook.ts` | Added logging infrastructure, updated handlers |
| `plugins/voice/hooks/hooks.json` | External hooks file (required format) |
| `plugins/voice/hooks/voice-hook.sh` | Bash wrapper for PATH/env setup |
| `plugins/voice/.claude-plugin/plugin.json` | Proper hooks reference |
| `.claude-plugin/marketplace.json` | Added voice plugin |
| `.gitignore` | Added `.claude/voice/` (runtime data) |

## Commits

- `[plugin:voice] feat: add structured JSONL voice event logging`
- `[planning] doc: update voice plugin status`

## Insights

1. **Plugin discovery is fragile**: Stale entries in `installed_plugins.json` can block plugins silently. When debugging, create a minimal test plugin to isolate the issue.

2. **External hooks.json is mandatory**: Inline hooks in plugin.json don't work. The hooks file format has unusual nesting (`hooks.hooks`) that must be exact.

3. **Dual-log strategy**: Daily partitioned logs + global log balances archival needs with query convenience. The global log enables quick analysis without date math.

4. **Voice source tracking**: Knowing whether a voice came from session config, agent config, model default, or system fallback enables analysis of identity resolution patterns.

## Next Steps

Per the planning document:
- [ ] STT input processing (background listener)
- [ ] Tmux voice navigation
- [ ] Claude input streaming via VTT
- [ ] Agent-specific voice registry integration
- [ ] Multi-voice backend exploration (Huggingface models)

---

*Parent: [[2025-12-19]]*
