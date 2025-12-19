# Voice Plugin Strategic Roadmap

**Created**: 2025-12-19
**Status**: Active Planning
**Scope**: Multi-horizon voice infrastructure development

---

## Current State Assessment

### What's Working
- TTS output via hooks (SessionStart, Stop, Notification, SubagentStop)
- Voice identity resolution (session → agent → model → system)
- Structured JSONL logging with metrics (latency, backend, success rate)
- Hot-reload development workflow
- Audio playback fixed (temp file approach, no more clipping)

### What's Missing
- **GPU acceleration**: PyTorch is CPU-only despite RTX 4070 availability
- **STT input**: No speech-to-text processing yet
- **Voice daemon**: No always-on listening
- **Quality evaluation**: No automated testing framework
- **Free alternatives**: Still dependent on ElevenLabs API

### Critical Blockers

| Blocker | Impact | Fix Time |
|---------|--------|----------|
| CUDA toolkit not installed | No GPU TTS | 30 min |
| PyTorch CPU-only | 10-50x slower inference | 15 min |
| sounddevice not installed | No low-level audio control | 5 min |

---

## Infrastructure Layers

### The Voice Stack (Top to Bottom)

```
┌────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│  Voice Plugin ─ Hooks ─ Identity ─ Logging ─ Agents        │
├────────────────────────────────────────────────────────────┤
│                    INFERENCE LAYER                          │
│  TTS Adapters (ElevenLabs, XTTS, Piper, pyttsx3)          │
│  STT Adapters (Whisper, Vosk, Deepgram) [planned]         │
│  VAD Processing (Silero) [planned]                         │
├────────────────────────────────────────────────────────────┤
│                    RUNTIME LAYER                            │
│  Bun (hooks) ─ Python (ML inference) ─ FFmpeg (processing) │
├────────────────────────────────────────────────────────────┤
│                    AUDIO LAYER                              │
│  mpv/ffplay (playback) ─ sounddevice (I/O) [needed]        │
│  PipeWire 1.0.3 ─ ALSA                                     │
├────────────────────────────────────────────────────────────┤
│                    HARDWARE LAYER                           │
│  RTX 4070 (12GB VRAM) ─ Intel HDA ─ C920 Webcam           │
│  NVIDIA HDMI Audio ─ USB Audio                             │
└────────────────────────────────────────────────────────────┘
```

### Layer Access Strategy

**Must Access** (for quality TTS):
- Inference Layer: Direct model control for latency tuning
- Audio Layer: Low-level I/O for streaming, VAD

**Should Access** (for pro features):
- Hardware Layer: GPU memory management, device selection

**Nice to Have**:
- PipeWire session management for advanced routing

---

## Testing Strategy

### Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| TTS Latency (p95) | < 2000ms | Time from text → audio start |
| STT WER | < 10% | Word Error Rate on test set |
| VAD Precision | > 95% | True speech / all detections |
| Uptime | > 99.9% | Daemon availability |
| MOS Score | > 3.5 | Human evaluation (1-5 scale) |

### Test Infrastructure

```
plugins/voice/tests/
├── unit/                    # Fast, deterministic
│   ├── identity.test.ts     # Voice resolution logic
│   ├── queue.test.ts        # Priority queue behavior
│   └── config.test.ts       # Configuration validation
├── component/               # Synthetic audio
│   ├── backends.test.ts     # Adapter contracts
│   ├── vad.test.ts          # VAD on reference audio
│   └── fallback.test.ts     # Backend fallback chain
├── integration/             # Real audio
│   ├── end-to-end.test.ts   # Full pipeline
│   ├── latency.test.ts      # Performance benchmarks
│   └── robustness.test.ts   # Failure injection
├── fixtures/
│   ├── audio/               # Reference audio files
│   └── transcripts/         # Ground truth
└── quality/
    ├── baseline.json        # Current metrics
    ├── gates.json           # CI thresholds
    └── reports/             # Historical trends
```

### Evaluation Loop

```
BASELINE → HYPOTHESIS → EXPERIMENT → MEASURE → DECIDE → (repeat)
```

Every improvement requires:
1. Documented hypothesis
2. A/B test with same audio samples
3. Statistical significance check
4. Rollback plan if regression

---

## Multi-Horizon Roadmap

### Horizon 0: Foundation (This Week)

**Goal**: Unblock GPU and establish quality baseline

- [ ] Install CUDA toolkit: `sudo apt install nvidia-cuda-toolkit`
- [ ] Reinstall PyTorch with CUDA: `pip install torch --index-url .../cu121`
- [ ] Install sounddevice: `pip install sounddevice`
- [ ] Create quality test suite scaffold
- [ ] Document current baseline metrics
- [ ] Verify audio clipping fix works consistently

**Success**: GPU-accelerated inference possible, quality measurable

### Horizon 1: Free TTS (2 Weeks)

**Goal**: Replace ElevenLabs dependency with HuggingFace

- [ ] Implement HuggingFace XTTS adapter
- [ ] Implement Piper adapter (fast CPU fallback)
- [ ] Implement Edge TTS adapter (free cloud)
- [ ] A/B test quality vs ElevenLabs
- [ ] Backend selection logic (GPU available? Latency needs?)
- [ ] Cost tracking dashboard

**Success**: High-quality TTS without API costs

### Horizon 2: Basic STT (1 Month)

**Goal**: Voice input to Claude

- [ ] Whisper adapter (local, batch mode first)
- [ ] VAD integration (Silero)
- [ ] Wake word detection ("hey claude" or similar)
- [ ] Claude input streaming (voice → text → submit)
- [ ] Basic tmux voice commands (switch pane, new window)

**Success**: Can dictate to Claude, navigate tmux by voice

### Horizon 3: Multi-Agent Voice (2 Months)

**Goal**: Distinct personalities for agent fleet

- [ ] Voice personality profiles per agent
- [ ] Priority queue for multi-agent coordination
- [ ] Interrupt handling (higher priority cuts through)
- [ ] Context-aware TTS (time of day, session length, user state)
- [ ] Agent voice preview tool

**Success**: Each agent has recognizable voice and style

### Horizon 4: Voice Daemon (3 Months)

**Goal**: Always-on voice interface

- [ ] Systemd service for continuous listening
- [ ] Full tmux voice control vocabulary
- [ ] Cross-session voice memory
- [ ] Automatic quality tuning
- [ ] Voice-based knowledge retrieval

**Success**: Voice becomes primary dev interface

### Horizon 5: Ultimate Experience (6 Months)

**Goal**: State-of-the-art voice UX

- [ ] Custom voice fine-tuning per agent
- [ ] Multi-speaker diarization
- [ ] Emotion detection and response
- [ ] Predictive intent (anticipate user needs)
- [ ] Voice profile learning over time

**Success**: Feels like talking to human colleagues

---

## HuggingFace Backend Priority

### Model Comparison

| Model | Quality | Latency | VRAM | Voices | License |
|-------|---------|---------|------|--------|---------|
| **XTTS v2** | Excellent | ~1.5s (GPU) | 6-8GB | Clone any | Apache 2.0 |
| **Piper** | Good | ~200ms | <1GB | 100+ presets | MIT |
| **F5-TTS** | Excellent | ~1s | 8-10GB | Clone + emotion | Apache 2.0 |
| **Bark** | Good | ~5s | 4-6GB | Clone + nonverbal | MIT |
| **Edge TTS** | Good | ~300ms | 0 (cloud) | 200+ | Free API |

### Recommended Backend Chain

```typescript
const BACKEND_PRIORITY = {
  "huggingface-xtts": 100,  // Best quality, requires GPU
  "piper": 90,              // Fast fallback, CPU-only
  "edge-tts": 80,           // Free cloud, decent quality
  "elevenlabs": 70,         // Premium cloud, excellent quality
  "openai": 60,             // Premium cloud, good quality
  "pyttsx3": 10,            // Always works, robotic
};
```

**Selection Logic**:
- High-quality agent voices → XTTS (if GPU available)
- Low-latency responses → Piper
- No GPU, no API keys → Edge TTS
- Premium tier → ElevenLabs

---

## Edge Cases & Failure Modes

### Multi-Agent Coordination

| Scenario | Solution |
|----------|----------|
| Two agents speak simultaneously | Priority queue, lower priority waits |
| User interrupts agent | Stop playback, flush queue, process user |
| Subagent speaks during parent | Brief pause, announce speaker change |
| Queue overflow (>10 pending) | Drop lowest priority, log warning |

### Graceful Degradation

```
TTS fails → Try next backend → Text-only fallback → Log error
STT fails → Retry once → Prompt for text input → Log error
Daemon crash → Systemd restart → Notify user → Resume
Device disconnect → Pause voice → Monitor → Resume on reconnect
```

### Personality Edge Cases

| Case | Handling |
|------|----------|
| Agent unknown | Use model-based default voice |
| Custom voice file missing | Fall back to preset voice |
| SSML not supported | Strip SSML, use plain text |
| Emotion detection fails | Use neutral tone |

---

## Quality Improvement Tracking

### Awareness Integration

Voice quality is a **learning domain** tracked via awareness plugin:

```markdown
## Learning Path: Voice Quality

### Stage: Fundamentals
- [x] Understand WER, MOS, latency
- [x] Know backend options

### Stage: Competence (Current)
- [x] Run basic quality tests
- [ ] Interpret metrics trends
- [ ] Tune VAD thresholds

### Stage: Proficiency (Next)
- [ ] A/B testing methodology
- [ ] Custom voice profiles
- [ ] Multi-objective optimization

### Stage: Mastery (Future)
- [ ] Voice fine-tuning
- [ ] Predictive quality tuning
- [ ] Novel voice architectures
```

### Quality Dashboard

Location: `.claude/voice/quality/`

```
quality/
├── baseline.json       # Reference metrics
├── trends.jsonl        # Historical data
├── experiments/        # A/B test records
├── gates.json          # CI thresholds
└── reports/            # Generated reports
```

### Regression Prevention

```json
// gates.json
{
  "tts_latency_p95_max_ms": 2000,
  "stt_wer_max": 0.10,
  "vad_precision_min": 0.95,
  "failure_rate_max": 0.01
}
```

CI fails if any gate violated.

---

## Immediate Action Items

### Today

1. **Fix GPU access** (30 min)
   ```bash
   sudo apt install nvidia-cuda-toolkit
   pip uninstall torch torchvision
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
   ```

2. **Install audio libraries** (5 min)
   ```bash
   pip install sounddevice librosa
   ```

3. **Verify clipping fix** (10 min)
   - Run SessionStart hook manually
   - Listen for clean "Ready" pronunciation
   - Adjust audio-buffer if needed

### This Week

4. **Quality test scaffold** (2 hours)
   - Create test directory structure
   - Implement baseline measurement
   - Add to CI pipeline

5. **HuggingFace adapter** (4 hours)
   - Start with XTTS v2
   - Python subprocess for inference
   - Bun/TS wrapper

6. **Documentation** (1 hour)
   - Update subskills with this roadmap
   - Create quality-testing subskill

---

## Open Questions

### Architecture
- Should voice daemon be separate process or integrated?
- How to handle voice across multiple Claude sessions?
- What's the storage budget for model weights?

### User Experience
- What's acceptable TTS latency? (<500ms? <1s? <2s?)
- Should agents introduce themselves by voice?
- How verbose should voice summaries be?

### Technical
- How to test MOS without human raters?
- Can we cache common phrases (greetings, errors)?
- Should we support multiple simultaneous voices?

---

## Related Documents

- Architecture: `plugins/voice/ARCHITECTURE.md`
- ElevenLabs API: `plugins/voice/skills/voice-master/subskills/elevenlabs.md`
- Exploration: `.claude/exploration/discoveries/audio-voice-infrastructure-2025-12-19.md`
- Questions: `.claude/exploration/questions/audio-voice-infrastructure-questions.md`
