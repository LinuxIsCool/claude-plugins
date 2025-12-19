---
type: map
synthesis: audio-voice-infrastructure
timestamp: 2025-12-19T11:48:46-08:00
tags: [audio, voice, tts, gpu, readiness]
---

# Audio & Voice Development Environment - Readiness Map

**Generated**: 2025-12-19  
**Source**: Discovery exploration of substrate + tools  

---

## Environment Readiness: 70%

```
┌─────────────────────────────────────────────────────┐
│                  AUDIO/VOICE STACK                   │
├─────────────────────────────────────────────────────┤
│ ✅ Audio Path        │ PipeWire → ALSA → HW          │
│ ✅ Audio Tools       │ FFmpeg, paplay, aplay         │
│ ✅ Python Base       │ numpy, scipy, pyttsx3         │
│ ✅ ML Framework      │ transformers 4.57.1           │
│ ⚠️  GPU Access       │ RTX 4070 (CUDA not enabled)   │
│ ❌ PyTorch GPU       │ CPU-only build                │
│ ❌ Audio Processing  │ sounddevice, librosa missing  │
│ ❌ HF TTS Adapter    │ Unimplemented                 │
└─────────────────────────────────────────────────────┘
```

---

## Component Status Matrix

| Layer | Component | Status | Blocking? | Fix Time |
|-------|-----------|--------|-----------|----------|
| **Hardware** | ||||
| | RTX 4070 GPU | ✅ Ready | No | - |
| | 32GB RAM | ✅ Ready | No | - |
| | Audio devices | ✅ Ready | No | - |
| **System** | ||||
| | PipeWire 1.0.3 | ✅ Running | No | - |
| | NVIDIA Driver 580 | ✅ Running | No | - |
| | CUDA Runtime libs | ✅ Partial | No | - |
| | CUDA Toolkit | ❌ Missing | **YES** | 30min |
| **Python Stack** | ||||
| | Python 3.13.2 | ✅ Ready | No | - |
| | PyTorch 2.9.0 | ⚠️ CPU-only | **YES** | 15min |
| | transformers | ✅ Ready | No | - |
| | numpy/scipy | ✅ Ready | No | - |
| | pyttsx3 | ✅ Ready | No | - |
| | sounddevice | ❌ Missing | No | 10min |
| | librosa | ❌ Missing | No | 5min |
| **Tools** | ||||
| | FFmpeg 4.4.2 | ✅ Ready | No | - |
| | Bun 1.2.9 | ✅ Ready | No | - |
| **Plugins** | ||||
| | voice plugin | ✅ Exists | No | - |
| | ElevenLabs adapter | ✅ Works | No | - |
| | pyttsx3 adapter | ✅ Works | No | - |
| | HF TTS adapter | ❌ Stubbed | No | 4-8hrs |
| **Models** | ||||
| | XTTS v2 | ❌ Not installed | No | 1hr |
| | Piper | ❌ Not installed | No | 30min |

---

## Blocking Issues (2)

### 1. CUDA Toolkit Not Installed
- **Impact**: GPU completely inaccessible to ML frameworks
- **Fix**: `sudo apt install nvidia-cuda-toolkit`
- **Time**: 30 minutes
- **Priority**: P0 (blocks all GPU work)

### 2. PyTorch CPU-Only Build
- **Impact**: TTS will run 10-50x slower than possible
- **Fix**: `pip install torch --index-url https://download.pytorch.org/whl/cu121`
- **Time**: 15 minutes
- **Priority**: P0 (blocks GPU TTS)

---

## Capabilities Matrix

### Current (CPU-only)

| Capability | Status | Performance | Notes |
|------------|--------|-------------|-------|
| **Offline TTS** | ✅ | Poor | pyttsx3 (robotic voice) |
| **Cloud TTS** | ✅ | Good | ElevenLabs (requires API key) |
| **Voice Cloning** | ❌ | N/A | Needs GPU + XTTS |
| **Audio Processing** | ⚠️ | Limited | FFmpeg only |
| **STT** | ❌ | N/A | Whisper stubbed |

### After GPU Enablement

| Capability | Status | Performance | Notes |
|------------|--------|-------------|-------|
| **Offline TTS** | ✅ | Excellent | XTTS v2 < 1s latency |
| **Cloud TTS** | ✅ | Good | ElevenLabs (unchanged) |
| **Voice Cloning** | ✅ | Excellent | XTTS v2, F5-TTS |
| **Audio Processing** | ✅ | Excellent | librosa + FFmpeg |
| **STT** | ✅ | Excellent | Faster-Whisper |

---

## TTS Model Comparison

| Model | Quality | Speed | VRAM | GPU? | Status |
|-------|---------|-------|------|------|--------|
| **pyttsx3** | ⭐⭐ | Fast | 0 | No | ✅ Working |
| **Piper** | ⭐⭐⭐⭐ | Fast | < 1GB | Optional | ❌ Not installed |
| **XTTS v2** | ⭐⭐⭐⭐⭐ | Medium | 6-8GB | Required | ❌ Not installed |
| **F5-TTS** | ⭐⭐⭐⭐⭐ | Slow | 8-10GB | Required | ❌ Not installed |
| **ElevenLabs** | ⭐⭐⭐⭐⭐ | Medium | 0 | Cloud | ✅ Working |

**Recommended**: Piper (CPU fallback) + XTTS v2 (GPU primary)

---

## Installation Phases

### Phase 1: GPU Enablement (1 hour) - BLOCKING

```bash
sudo apt update
sudo apt install nvidia-cuda-toolkit
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
python3 -c "import torch; print(torch.cuda.is_available())"
```

**Unlocks**: All GPU-accelerated TTS models

---

### Phase 2: Audio Libraries (15 minutes) - HIGH PRIORITY

```bash
sudo apt install portaudio19-dev libsndfile1
pip install sounddevice librosa soundfile
```

**Unlocks**: Professional audio manipulation, analysis

---

### Phase 3: TTS Models (1-2 hours) - MEDIUM PRIORITY

```bash
pip install TTS  # Coqui TTS (XTTS v2)
pip install piper-tts  # Optional CPU fallback
```

**Unlocks**: High-quality local TTS

---

### Phase 4: HF Adapter Implementation (4-8 hours) - LOW PRIORITY

- Create `plugins/voice/src/adapters/tts/huggingface.ts`
- Follow pyttsx3 adapter pattern
- Support XTTS v2, Piper, F5-TTS

**Unlocks**: Integration with voice plugin ecosystem

---

## Architecture Gaps

### Voice Plugin (TypeScript/Bun)

**Implemented**:
- ✅ TTS port interface
- ✅ Factory pattern
- ✅ ElevenLabs adapter
- ✅ pyttsx3 adapter
- ✅ Identity resolver
- ✅ Voice hooks

**Missing**:
- ❌ HuggingFace adapter (highest priority!)
- ❌ Piper adapter
- ❌ OpenAI adapter
- ❌ STT implementation
- ❌ VAD implementation

**Design Quality**: Excellent (hexagonal architecture, clear ports)

---

## Knowledge Graph Position

```
Voice Infrastructure
    ├─ Substrate
    │   ├─ Hardware: RTX 4070 (12GB VRAM) ✅
    │   ├─ Audio: PipeWire → ALSA → HW ✅
    │   └─ Drivers: NVIDIA 580.82.09 ✅
    ├─ Tools
    │   ├─ System: FFmpeg, PipeWire ✅
    │   ├─ Python: torch (CPU), transformers ⚠️
    │   ├─ Bun: voice plugin ✅
    │   └─ Models: None installed ❌
    ├─ Network
    │   └─ Cloud: ElevenLabs API ✅
    └─ Cosmos
        └─ Question: What are the limits of voice synthesis quality?
```

---

## Next Exploration Vectors

1. **Network**: Probe ElevenLabs latency, compare to local inference
2. **Context**: Git archaeology for past voice work
3. **Knowledge**: Map voice → logging → journal integration
4. **Curiosity**: What can we do with 12GB VRAM besides TTS?

---

## Verdict

**Environment Status**: Like a Formula 1 car with regular gasoline.

The hardware is magnificent. The software stack is well-designed. But the critical connection (CUDA toolkit → PyTorch → GPU) is missing.

**Time to Production-Ready**: 
- GPU TTS: 1 hour (GPU enablement)
- Full voice system: 5-6 hours (GPU + libraries + adapter)

**Recommendation**: Prioritize GPU enablement. Everything else is easy once that's in place.

