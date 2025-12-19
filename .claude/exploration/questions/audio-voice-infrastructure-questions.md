---
type: questions
relates_to: discoveries/audio-voice-infrastructure-2025-12-19.md
timestamp: 2025-12-19T11:48:46-08:00
tags: [audio, voice, tts, stt, gpu, architecture]
---

# Audio & Voice Infrastructure - Open Questions

**Source Discovery**: `audio-voice-infrastructure-2025-12-19.md`  
**Question Type**: Technical requirements, architectural decisions, resource constraints

---

## Product & User Experience

### 1. TTS Latency Requirements

**Question**: What's the acceptable TTS latency for real-time agent voice responses?

**Context**: 
- XTTS v2 on GPU: ~500-1000ms for short sentences
- Piper: ~100-300ms
- pyttsx3: Instant (streaming)
- ElevenLabs: 500-1500ms (network dependent)

**Impact**: Determines which TTS backend to prioritize

**Options**:
- A) < 500ms (requires Piper or optimized XTTS)
- B) < 1s (XTTS v2 acceptable)
- C) < 2s (any backend works)
- D) No hard requirement (best quality wins)

---

### 2. Voice Cloning Support

**Question**: Should we support voice cloning for agent personas?

**Context**: 
- XTTS v2, F5-TTS, Bark support voice cloning from 3-30s reference audio
- Allows each agent (Archivist, Scribe, Mentor, etc.) to have unique voice
- Requires reference audio recordings or synthetic samples

**Use Cases**:
- Agent identity reinforcement (different voice per agent)
- Personalized TTS (user provides reference audio)
- Character-based coding assistants

**Trade-offs**:
- Pros: Immersive, engaging, memorable agent personas
- Cons: Storage (1-10MB per voice), complexity, potential uncanny valley

---

### 3. Speech-to-Text Input

**Question**: Do we need STT for voice input to Claude Code?

**Context**: 
- Transcripts plugin has Whisper/Faster-Whisper adapters
- Would enable hands-free coding
- Requires VAD (Voice Activity Detection) for triggering

**Use Cases**:
- Dictating code
- Voice commands ("Claude, refactor this function")
- Accessibility (motor impairment support)

**Technical Considerations**:
- Microphone access in terminal environment
- Background noise handling
- Hotkey/push-to-talk vs continuous listening

---

### 4. Multi-Language TTS

**Question**: Do we need multi-language TTS support?

**Context**: 
- XTTS v2 supports 17 languages
- Piper has models for 50+ languages
- pyttsx3 depends on system TTS (varies)

**Use Cases**:
- International users
- Code comments in native language
- Multi-lingual documentation reading

**Impact**: 
- Model storage (1-2GB per language for XTTS)
- Voice selection complexity
- Language detection requirements

---

### 5. Audio Quality Target

**Question**: What's the target audio quality? (16kHz, 22kHz, 44.1kHz?)

**Context**: 
- 16kHz: Phone quality, smallest files, fastest processing
- 22kHz: Radio quality, good balance (XTTS v2 native)
- 44.1kHz: CD quality, largest files, may be overkill for TTS

**Trade-offs**:
| Sample Rate | File Size | Quality | Processing Time |
|-------------|-----------|---------|-----------------|
| 16kHz | 1x | Acceptable | Fast |
| 22kHz | 1.4x | Good | Medium |
| 44.1kHz | 2.8x | Excellent | Slow |

**Recommendation Needed**: Balance quality vs performance

---

## Architecture & Implementation

### 6. TTS Caching Strategy

**Question**: Should we cache generated audio for common phrases?

**Context**: 
- Repeated phrases: "Task completed", "Error occurred", status messages
- Cache hit could reduce latency to near-zero
- Storage: ~50KB per cached phrase (22kHz WAV)

**Cache Scope**:
- A) Per-agent caching (different voice per agent)
- B) Global caching (same phrase = same audio)
- C) No caching (always fresh synthesis)

**Trade-offs**:
- Pros: Near-instant playback, reduced GPU usage
- Cons: Storage overhead, cache invalidation complexity

**Storage Estimate**:
- 100 common phrases × 50KB = 5MB
- 1000 phrases = 50MB (still negligible)

---

### 7. Long-Form TTS Streaming

**Question**: Should we implement audio streaming for long-form TTS?

**Context**: 
- Current implementation: Synthesize entire text, then play
- Streaming: Start playback while still synthesizing
- Useful for reading long documentation, logs, journal entries

**Benefits**:
- Lower perceived latency (hear first sentence sooner)
- Better UX for long content

**Challenges**:
- Requires streaming-capable backend (ElevenLabs, some HuggingFace models)
- XTTS v2 doesn't natively stream (would need chunking)
- More complex playback control (pause/resume)

---

### 8. Emotion & Style Control

**Question**: Do we want emotion/style control in TTS?

**Context**: 
- Some models (Bark, StyleTTS2) support emotional expression
- Could convey: excitement (new feature!), concern (error), neutral (info)

**Use Cases**:
- Error messages with concerned tone
- Success messages with upbeat tone
- Agent personality expression

**Technical Support**:
- Bark: ✅ Supports emotions via prompt
- StyleTTS2: ✅ Style control
- XTTS v2: ⚠️ Limited (inferred from reference audio)
- Piper: ❌ No emotion control

---

### 9. Voice Profile Database

**Question**: Should we build a voice profile database for agent identities?

**Context**: 
- Existing agents: Archivist, Scribe, Mentor, Voice Conductor, Transcriber, etc.
- Could map agent → voice characteristics
- Storage: JSON mapping + reference audio files

**Schema Example**:
```json
{
  "archivist": {
    "voice_id": "precise-methodical",
    "reference_audio": "voices/archivist.wav",
    "characteristics": {
      "gender": "neutral",
      "age": "mature",
      "tone": "calm",
      "accent": "generic"
    }
  }
}
```

**Integration**: 
- Voice plugin already has identity resolver
- Would need voice recording/selection process

---

## Resource Constraints

### 10. TTS Model Storage Budget

**Question**: What's the storage budget for TTS model weights?

**Context**: 
- XTTS v2: ~1.8GB
- F5-TTS: ~1.2GB
- Piper (all voices): ~500MB
- Bark: ~4GB

**Current Available**: 199GB free (total: 929GB, 78% used)

**Options**:
- A) < 2GB (XTTS v2 or Piper only)
- B) < 5GB (XTTS v2 + F5-TTS + Piper)
- C) < 10GB (all models for experimentation)
- D) No hard limit (plenty of space)

---

### 11. VRAM Budget for TTS

**Question**: How much VRAM should we allocate to TTS?

**Context**: 
- Total VRAM: 12GB (RTX 4070)
- XTTS v2: 6-8GB during inference
- Other ML tasks may compete for VRAM

**Sharing Scenarios**:
- TTS only: 12GB available (comfortable)
- TTS + LLM fine-tuning: Need allocation strategy
- TTS + image generation: Conflicts likely

**Options**:
- A) TTS gets exclusive access (12GB)
- B) TTS limited to 8GB (leaves 4GB for other tasks)
- C) Dynamic allocation (swap models as needed)

---

### 12. Audio Cache Storage Limit

**Question**: Should we impose a cache size limit?

**Context**: 
- Cached audio accumulates over time
- 1000 phrases = ~50MB
- 10,000 phrases = ~500MB

**Cache Management**:
- LRU eviction (least recently used)
- TTL expiration (time-to-live)
- Manual clearing

**Recommendation**: Set soft limit (500MB-1GB) with LRU eviction

---

## Integration & Workflow

### 13. Voice Hook Event Triggers

**Question**: Which session events should trigger TTS?

**Context**: 
- Voice plugin has hook system for monitoring events
- Current triggers unknown (need to inspect voice-hook.ts implementation)

**Potential Triggers**:
- Session start/end
- Task completion
- Error occurrence
- Long-running task progress updates
- Agent spawn/termination
- Tool invocations (git commit, file write, etc.)

**User Control**: Should be configurable (enable/disable per event type)

---

### 14. Audio Playback Concurrency

**Question**: How should we handle concurrent TTS requests?

**Scenarios**:
- Multiple agents speaking simultaneously
- New TTS request while previous audio playing

**Options**:
- A) Queue (first-in-first-out)
- B) Interrupt (cancel current, play new)
- C) Mix (play multiple audio streams simultaneously)
- D) Priority-based (agent priority determines behavior)

**Recommendation**: Queue for now, explore mixing later

---

### 15. TTS Backend Selection Strategy

**Question**: How should we choose TTS backend when multiple are available?

**Current Priority** (from code):
1. HuggingFace (100)
2. ElevenLabs (90)
3. OpenAI (80)
4. Piper (70)
5. Coqui (60)
6. pyttsx3 (10)

**Selection Criteria**:
- A) Fixed priority (as above)
- B) Quality-first (F5-TTS/XTTS over Piper)
- C) Speed-first (Piper over XTTS)
- D) Cost-first (local over cloud)
- E) Context-aware (quality for long text, speed for alerts)

**Proposed**: Default to fixed priority, allow per-request override

---

## Exploration Follow-Up

### 16. Cloud TTS Latency Profiling

**Question**: What are the real-world latencies for cloud TTS APIs?

**Need to Probe**:
- ElevenLabs API response time
- OpenAI TTS API response time
- Network-dependent variance
- Geographic factors

**Method**: Network probing (exploration:network-prober)

---

### 17. Past Voice Work Archaeology

**Question**: Has there been previous voice/TTS work in this codebase?

**Need to Investigate**:
- Git history for voice-related commits
- Journal entries mentioning TTS
- Briefings or design docs

**Method**: Context archaeology (exploration:context-archaeologist)

---

### 18. Voice + Logging Integration

**Question**: Should TTS events be logged by the logging plugin?

**Integration Points**:
- Voice synthesis requests
- Backend selection decisions
- Audio playback events
- Error conditions

**Knowledge Graph**: How does voice fit into ecosystem?

**Method**: Knowledge weaving (exploration:knowledge-weaver)

---

## Questions for User

**Priority 1** (Needed for implementation):
1. TTS latency requirements (#1)
2. Voice cloning support (#2)
3. Storage budget for models (#10)

**Priority 2** (Architecture decisions):
4. STT input support (#3)
5. Audio caching strategy (#6)
6. TTS backend selection (#15)

**Priority 3** (Future enhancements):
7. Multi-language support (#4)
8. Emotion/style control (#8)
9. Voice profile database (#9)

---

*Next Steps*: 
- User input on priority questions
- Technical spike for GPU enablement
- Prototype HuggingFace TTS adapter
- Network latency profiling for cloud APIs

