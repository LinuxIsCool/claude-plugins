---
type: discovery
circle: substrate+tools
timestamp: 2025-12-19T11:48:46-08:00
mastery_level: 2
tags: [audio, voice, tts, stt, gpu, infrastructure]
---

# Audio & Voice Infrastructure Discovery

**Exploration Date**: 2025-12-19  
**Explorer**: exploration:substrate-scanner + exploration:tool-cartographer  
**Objective**: Map complete audio/voice stack for TTS/STT development with RTX 4070 GPU

---

## Executive Summary

The system has a **partially configured** audio/voice development environment. Strong foundation exists (PipeWire, FFmpeg, pyttsx3) but critical gaps prevent professional GPU-accelerated TTS:

1. **Audio Stack**: Complete and modern (PipeWire → ALSA → Intel/NVIDIA audio)
2. **GPU Infrastructure**: Hardware ready (RTX 4070, 12GB VRAM) but **PyTorch is CPU-only**
3. **Existing Voice System**: Functional `voice` and `transcripts` plugins using pyttsx3 + ElevenLabs
4. **Missing Components**: GPU-enabled PyTorch, sounddevice/pyaudio, librosa, local HuggingFace TTS models

**Status**: Development environment is **70% ready**. Need CUDA toolkit + PyTorch reinstall for GPU TTS.

---

## 1. Audio Stack Depth (Application → Speaker)

### Full Audio Path

```
Application Layer
    ↓
PipeWire 1.0.3 (Modern audio server)
    ↓
PulseAudio Compatibility Layer (Server Version 15.0.0)
    ↓
ALSA (Advanced Linux Sound Architecture)
    ↓
Hardware Layer
    ├─ Intel HDA PCH (ALC897 Analog) - Motherboard audio
    ├─ NVIDIA HDA (RTX 4070 HDMI audio) - GPU audio output
    └─ Logitech C920 Webcam - USB audio input
```

### Audio Server Configuration

| Component | Version | Status | Notes |
|-----------|---------|--------|-------|
| **PipeWire** | 1.0.3 | Active | Modern replacement for PulseAudio/JACK |
| **PulseAudio Compat** | 15.0.0 | Active | PipeWire provides PA compatibility layer |
| **WirePlumber** | 1.0.3 | Active | PipeWire session manager |
| **ALSA** | System | Active | Kernel-level audio subsystem |

### Audio Devices

**Playback Devices**:
- Card 0: HDA Intel PCH - ALC897 Analog (Motherboard)
- Card 2: HDA NVidia - HDMI 0-3 (RTX 4070 - 4 outputs)

**Capture Devices**:
- Card 0: HDA Intel PCH - ALC897 Analog (Motherboard mic)
- Card 0: HDA Intel PCH - ALC897 Alt Analog
- Card 1: Logitech C920 - USB Audio (Webcam mic)

**Default Configuration**:
- Default Sink: `alsa_output.pci-0000_01_00.1.hdmi-stereo` (NVIDIA HDMI)
- Default Source: `alsa_input.usb-046d_HD_Pro_Webcam_C920` (Webcam)
- Sample Format: float32le, 2ch, 48000Hz

**Verdict**: Audio stack is **modern, complete, and professional-grade**. PipeWire provides low-latency routing suitable for real-time TTS.

---

## 2. Low-Level Audio Access Libraries

### Python Audio Libraries

| Library | Status | Purpose | Installation Required |
|---------|--------|---------|----------------------|
| **numpy** | ✅ INSTALLED (2.3.5) | Array operations | - |
| **scipy.io.wavfile** | ✅ INSTALLED | WAV file I/O | - |
| **pyttsx3** | ✅ INSTALLED (2.99) | Offline TTS fallback | - |
| **audioop-lts** | ✅ INSTALLED (0.2.2) | Audio operations | - |
| **ffmpeg-python** | ✅ INSTALLED (0.2.0) | FFmpeg bindings | - |
| **sounddevice** | ❌ MISSING | Low-level playback/record | `pip install sounddevice` + portaudio19-dev |
| **pyaudio** | ❌ MISSING | PortAudio bindings | `pip install pyaudio` + portaudio19-dev |
| **librosa** | ❌ MISSING | Audio analysis/processing | `pip install librosa` |

**System Audio Libraries** (Available):
- PortAudio 2.0.0 (libportaudio.so.2) - ✅ Installed
- JACK 0.0.28 (libjack.so.0) - ✅ Installed
- PulseAudio (libpulse-mainloop-glib.so.0) - ✅ Installed

**Verdict**: Core libraries present, but **sounddevice** and **librosa** are critical gaps for professional audio development.

### Bun/TypeScript Audio

**Current State**: 
- Bun 1.2.9 installed
- `plugins/voice` uses Node.js `child_process` for Python interop
- No native Bun audio libraries discovered

**Potential Libraries** (Research needed):
- `naudiodon` - Node.js PortAudio bindings
- `speaker` - Node.js audio playback
- `node-portaudio` - Direct PortAudio access

**Verdict**: TypeScript voice plugin relies on Python subprocess calls. Native Bun audio is **unexplored territory**.

---

## 3. GPU Utilization Status

### Hardware Configuration

**GPU**: NVIDIA GeForce RTX 4070  
- VRAM: 12282 MiB (12GB)
- Compute Capability: 8.9 (Ada Lovelace architecture)
- Driver Version: 580.82.09 (Latest stable)

**CPU**: Intel 13th/14th Gen (inferred from HDA device)  
**RAM**: 32GB (22GB available)  
**Storage**: 929GB (199GB free)

### CUDA Installation Status

| Component | Status | Notes |
|-----------|--------|-------|
| **NVIDIA Driver** | ✅ INSTALLED (580.82.09) | Up to date |
| **CUDA Runtime** | ✅ PARTIAL | libcuda.so.1 found in ldconfig |
| **CUDA Toolkit** | ❌ MISSING | `nvcc` not found |
| **cuDNN** | ❌ MISSING | No packages found |
| **PyTorch** | ⚠️ CPU-ONLY | Version 2.9.0+cpu |
| **torchvision** | ⚠️ CPU-ONLY | Version 0.24.0+cpu |

**PyTorch Test**:
```python
>>> torch.cuda.is_available()
False
>>> torch.version.cuda
None
```

**Root Cause**: PyTorch installed from CPU-only wheel. CUDA toolkit exists in system libraries but not accessible to PyTorch.

### What's Needed for GPU TTS

**Installation Steps**:

1. **Install CUDA Toolkit** (Ubuntu 22.04 - Pop!_OS):
   ```bash
   sudo apt install nvidia-cuda-toolkit
   # Or download from NVIDIA (recommended for latest version)
   ```

2. **Verify CUDA Version Compatibility**:
   - RTX 4070 requires CUDA 11.8+ (supports up to CUDA 12.x)
   - PyTorch 2.9.0 supports CUDA 11.8, 12.1, 12.4

3. **Reinstall PyTorch with CUDA**:
   ```bash
   pip uninstall torch torchvision
   # For CUDA 12.1 (recommended)
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
   ```

4. **Install cuDNN** (if not included in PyTorch wheel):
   ```bash
   sudo apt install libcudnn8 libcudnn8-dev
   ```

5. **Verify GPU Access**:
   ```python
   import torch
   torch.cuda.is_available()  # Should return True
   torch.cuda.get_device_name(0)  # Should show "NVIDIA GeForce RTX 4070"
   ```

**Verdict**: GPU is **ready but inaccessible** to ML frameworks. 30-minute fix with CUDA toolkit + PyTorch reinstall.

---

## 4. Local TTS Options (HuggingFace Models)

### Evaluation Criteria

For real-time, high-quality TTS:
- **Latency**: < 1s for short sentences
- **Quality**: Natural prosody, emotion, multi-speaker
- **VRAM**: Must fit in 12GB (RTX 4070)
- **License**: Open source, commercial-friendly

### Recommended Models

| Model | Quality | Speed | VRAM | Voices | License | Notes |
|-------|---------|-------|------|--------|---------|-------|
| **XTTS v2** | ⭐⭐⭐⭐⭐ | Medium | 6-8GB | Clone any | Apache 2.0 | Best quality, voice cloning, 17 languages |
| **Piper** | ⭐⭐⭐⭐ | Fast | < 1GB | Many | MIT | Ultra-fast, many voices, no GPU needed |
| **F5-TTS** | ⭐⭐⭐⭐⭐ | Slow | 8-10GB | Clone any | Apache 2.0 | Newest, best prosody, research-grade |
| **Bark** | ⭐⭐⭐⭐ | Slow | 4-6GB | Clone any | MIT | Multi-lingual, music/effects, creative |
| **StyleTTS2** | ⭐⭐⭐⭐ | Medium | 4-6GB | Clone any | MIT | Style control, expressive |
| **Parler-TTS** | ⭐⭐⭐ | Fast | 2-4GB | Describe voice | Apache 2.0 | Text-described voices, unique approach |

**Current System Capability** (CPU-only):
- Piper: ✅ Works well (designed for CPU)
- pyttsx3: ✅ Already functional (used in voice plugin)
- Others: ⚠️ Will work but 10-50x slower

**With GPU Enabled**:
- XTTS v2: ✅ Ideal for production (< 1s latency)
- F5-TTS: ✅ Best quality for non-real-time
- Bark: ✅ Creative applications (music, effects)

### HuggingFace Integration

**Transformers Library**: ✅ INSTALLED (4.57.1)

**Example Model Inference** (XTTS v2):
```python
from TTS.api import TTS

# After GPU setup
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")

# Voice cloning
tts.tts_to_file(
    text="Hello, this is a cloned voice.",
    file_path="output.wav",
    speaker_wav="reference_audio.wav",
    language="en"
)
```

**Verdict**: **XTTS v2 is the clear winner** for professional TTS once GPU is enabled. Piper is best for CPU-only scenarios.

---

## 5. Audio Processing Tools

### Format Conversion & Manipulation

**FFmpeg 4.4.2** - ✅ INSTALLED (Comprehensive build)

**Capabilities**:
- Codecs: MP3, AAC, FLAC, Opus, Vorbis, PCM (all formats)
- Containers: WAV, MP3, OGG, OPUS
- Filters: Silence detection, normalization, resampling
- Hardware acceleration: Available via NVENC/NVDEC (RTX 4070)

**Key FFmpeg Operations for TTS**:

```bash
# Normalize audio levels
ffmpeg -i input.wav -af "loudnorm=I=-16:TP=-1.5:LRA=11" output.wav

# Add silence padding
ffmpeg -i input.wav -af "apad=pad_dur=0.5" output.wav

# Convert format
ffmpeg -i input.mp3 -ar 22050 -ac 1 output.wav

# Speed adjustment
ffmpeg -i input.wav -filter:a "atempo=1.2" output.wav

# Trim silence
ffmpeg -i input.wav -af "silenceremove=1:0:-50dB" output.wav
```

### Python Audio Processing

**Available Libraries**:
- **scipy.io.wavfile**: ✅ WAV read/write
- **numpy**: ✅ Array manipulation
- **ffmpeg-python**: ✅ FFmpeg bindings
- **librosa**: ❌ MISSING (need to install)

**Librosa Capabilities** (after installation):
- Pitch shifting
- Time stretching
- Feature extraction (MFCC, spectrograms)
- Audio effects (reverb, EQ)
- Onset detection

**Installation**:
```bash
pip install librosa soundfile
```

### System Tools

| Tool | Status | Purpose |
|------|--------|---------|
| **ffmpeg** | ✅ 4.4.2 | Audio/video conversion, filtering |
| **ffplay** | ✅ | Audio playback testing |
| **paplay** | ✅ | PulseAudio playback |
| **aplay** | ✅ | ALSA playback |
| **sox** | ❌ | Audio Swiss Army knife (could install) |

**Verdict**: FFmpeg provides **professional-grade** audio manipulation. Librosa would add ML-focused audio analysis.

---

## 6. Existing Voice Infrastructure

### Voice Plugin Architecture

**Location**: `/home/ygg/Workspace/sandbox/marketplaces/claude/plugins/voice/`

**Components**:
- **TTS Adapters**: ElevenLabs, pyttsx3 (HuggingFace stubbed)
- **Ports**: TTS, STT, VAD (Voice Activity Detection)
- **Hooks**: voice-hook.ts (session event monitoring)
- **Identity Resolver**: Agent-specific voice mapping

**TTS Backend Priority** (from code):
```
1. HuggingFace (100) - NOT IMPLEMENTED
2. ElevenLabs (90) - IMPLEMENTED (cloud API)
3. OpenAI (80) - NOT IMPLEMENTED
4. Piper (70) - NOT IMPLEMENTED
5. Coqui (60) - NOT IMPLEMENTED
6. pyttsx3 (10) - IMPLEMENTED (fallback)
```

**Current Functionality**:
- ✅ pyttsx3 working (offline, espeak backend)
- ✅ ElevenLabs working (cloud, paid API)
- ❌ HuggingFace adapter stubbed (highest priority, unimplemented)

**Code Architecture** (TypeScript/Bun):
- Hexagonal architecture (ports/adapters)
- Factory pattern for backend selection
- Fallback chain for reliability

### Transcripts Plugin

**Location**: `/home/ygg/Workspace/sandbox/marketplaces/claude/plugins/transcripts/`

**Components**:
- **STT Adapters**: Whisper, Faster-Whisper
- **Diarization**: Pyannote (speaker identification)
- **Voice Fingerprinting**: Speaker database
- **Knowledge Extraction**: Entity extraction from transcripts

**Status**: Designed but implementation status unknown (TypeScript stubs visible).

### Integration Points

**Voice Plugin Hook** (`hooks/voice-hook.ts`):
- Monitors session events
- Triggers TTS on specific events
- Maps agent identity to voice profiles

**Verdict**: Well-designed plugin architecture exists. **HuggingFace adapter is the missing link** for local GPU TTS.

---

## 7. Critical Gaps Summary

### Blocking Issues (Priority 1)

1. **CUDA Toolkit Not Installed**
   - Impact: GPU unusable for ML workloads
   - Fix: `sudo apt install nvidia-cuda-toolkit` (or NVIDIA installer)
   - Time: 30 minutes

2. **PyTorch CPU-Only Build**
   - Impact: All TTS will run on CPU (10-50x slower)
   - Fix: Reinstall PyTorch with CUDA support
   - Time: 15 minutes

### High-Priority Gaps (Priority 2)

3. **HuggingFace TTS Adapter Unimplemented**
   - Impact: Cannot use local GPU TTS models
   - Fix: Implement adapter following pyttsx3/ElevenLabs pattern
   - Time: 2-4 hours

4. **Missing sounddevice/pyaudio**
   - Impact: Limited low-level audio control
   - Fix: `sudo apt install portaudio19-dev && pip install sounddevice pyaudio`
   - Time: 10 minutes

5. **Missing librosa**
   - Impact: No advanced audio analysis/manipulation
   - Fix: `pip install librosa soundfile`
   - Time: 5 minutes

### Nice-to-Have Gaps (Priority 3)

6. **Bun Native Audio Libraries**
   - Impact: Voice plugin relies on Python subprocesses
   - Fix: Research naudiodon, speaker, node-portaudio
   - Time: Research + 4-8 hours implementation

7. **SoX Audio Tool**
   - Impact: Less flexible command-line audio processing
   - Fix: `sudo apt install sox libsox-fmt-all`
   - Time: 2 minutes

---

## 8. Recommended Action Plan

### Phase 1: GPU Enablement (1 hour)

```bash
# 1. Install CUDA toolkit
sudo apt update
sudo apt install nvidia-cuda-toolkit

# 2. Verify CUDA installation
nvcc --version

# 3. Reinstall PyTorch with CUDA support
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121

# 4. Test GPU access
python3 -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

### Phase 2: Audio Libraries (15 minutes)

```bash
# Install system dependencies
sudo apt install portaudio19-dev libsndfile1

# Install Python audio libraries
pip install sounddevice librosa soundfile

# Test installation
python3 -c "import sounddevice as sd; import librosa; print('Audio stack ready')"
```

### Phase 3: HuggingFace TTS Integration (4-8 hours)

```bash
# Install TTS library (Coqui TTS for XTTS v2)
pip install TTS

# Test XTTS v2
python3 -c "from TTS.api import TTS; tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2').to('cuda'); print('XTTS ready')"

# Implement HuggingFace adapter
# - Create plugins/voice/src/adapters/tts/huggingface.ts
# - Follow pyttsx3 adapter pattern (Python subprocess)
# - Add XTTS v2, Piper, F5-TTS support
```

### Phase 4: Testing & Optimization (2-4 hours)

- Benchmark XTTS v2 latency
- Tune VRAM usage
- Test voice cloning quality
- Integrate with voice-hook system

---

## 9. Questions Raised

See: `.claude/exploration/questions/audio-voice-infrastructure-questions.md`

1. What's the acceptable TTS latency for real-time agent voice responses?
2. Should we support voice cloning for agent personas?
3. Do we need STT for voice input to Claude Code?
4. What's the storage budget for TTS model weights? (XTTS v2 = 1.8GB)
5. Should we cache generated audio for common phrases?
6. Do we need multi-language TTS support?
7. What's the target audio quality? (16kHz, 22kHz, 44.1kHz?)
8. Should we implement audio streaming for long-form TTS?
9. Do we want emotion/style control in TTS?
10. Should we build a voice profile database for agent identities?

---

## 10. Map Reference

This discovery contributes to:
- **Substrate Map**: Hardware, OS, audio drivers
- **Tools Map**: Python/Bun libraries, FFmpeg, CUDA
- **Cosmos Map**: What are the natural limits of voice synthesis quality?

**Next Exploration**: 
- Network probing for cloud TTS API latencies
- Context archaeology for past voice-related work
- Knowledge weaving to connect voice + logging + journal systems

---

*Explorer's Note*: The hardware is magnificent (RTX 4070, modern audio stack) but the software connection is incomplete. Like having a high-performance engine without a transmission. Once GPU-enabled PyTorch is installed, this system will be capable of **state-of-the-art local TTS** rivaling commercial APIs.

