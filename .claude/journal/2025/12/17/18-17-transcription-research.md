---
id: 2025-12-17-1817
title: "Comprehensive Transcription Options Research"
type: atomic
created: 2025-12-17T18:17:14
author: claude-opus-4
description: "Deep research into 20 transcription options with feature matrix, infrastructure analysis, and system-specific recommendations for RTX 4070 workstation"
tags: [transcription, speech-to-text, research, infrastructure, gpu, whisper, plugins]
parent_daily: [[2025-12-17]]
related:
  - [[14-34-claude-web-adapter]]
  - [[13-12-autocommit-classifier-fix]]
---

# Comprehensive Transcription Options Research

## Context

The user requested deep research into transcription options to inform the [[transcripts]] plugin implementation. The scope included:
- Top 20 transcription solutions (cloud APIs + open source)
- Full feature matrix with accuracy, pricing, latency
- Infrastructure implications for the local system
- Hardware/software environment exploration

## System Profile Discovery

Using the [[exploration:exploration-master]] skill's substrate-scanner approach, discovered:

| Component | Specification | Implication |
|-----------|--------------|-------------|
| **OS** | Pop!_OS 22.04 | Excellent Linux support |
| **CPU** | Intel i7-13700F (16c/24t) | Strong CPU inference |
| **RAM** | 32GB (4.5GB available) | Sufficient for large models |
| **GPU** | **NVIDIA RTX 4070 (12GB)** | Compute 8.9 - ideal for local ML |
| **Storage** | 929GB NVMe (214GB free) | Ample model storage |

### Critical Finding

**The RTX 4070 GPU is NOT being utilized.** PyTorch is installed as CPU-only despite having a powerful GPU available. This represents significant untapped performance.

```
PyTorch: 2.9.0+cpu
CUDA available: False
CUDA devices: 0
```

**Remedy:**
```bash
conda install pytorch pytorch-cuda=12.4 -c pytorch -c nvidia
```

## Transcription Options Matrix

### Cloud APIs (9 options)

| Provider | WER | Languages | Real-time | Diarization | Price/min |
|----------|-----|-----------|-----------|-------------|-----------|
| AssemblyAI Universal-2 | 8.4% | 100+ | 300ms | 50 speakers | $0.0025 |
| Deepgram Nova-3 | ~9% | 50+ | 150ms | Yes | $0.0043 |
| OpenAI Whisper API | 9.2% | 99 | Batch only | No | $0.006 |
| Google Cloud Chirp | ~8% | 100+ | Yes | Yes | $0.016 |
| Azure Speech Services | ~10% | 100+ | Yes | Yes | $0.0167 |
| Amazon Transcribe | ~12% | 54+ | Yes | Yes | $0.024 |
| Gladia | 5-10% | 100+ | 300ms | Yes | Competitive |
| Speechmatics | <10% | 55+ | Yes | Yes | Volume-based |
| Rev.ai | ~14% | 58+ | Yes | Yes | $0.035 |

### Open Source / Self-Hosted (11 options)

| Option | WER | GPU Req | Best For |
|--------|-----|---------|----------|
| OpenAI Whisper | 9.2% | 4-16GB | Reference |
| **faster-whisper** | 9.2% | **4GB** | **Recommended for RTX 4070** |
| whisper.cpp | 9.2% | Optional | CPU/Edge |
| WhisperX | 9.2% | 8GB+ | Whisper + diarization |
| **NVIDIA NeMo Parakeet** | **6.05%** | 8GB+ | **#1 Accuracy** |
| **SenseVoice** | <Whisper | 4GB+ | **15x faster** |
| Wav2Vec 2.0 | 3-6% | 8GB+ | Fine-tuning |
| Vosk | 10-15% | CPU | Offline lightweight |
| Kaldi | Variable | Variable | Custom models |
| SpeechBrain | Variable | 8GB+ | Research |
| FunASR | <Whisper | 4GB+ | Chinese focus |

### Speaker Diarization

| Tool | DER | Integration |
|------|-----|-------------|
| pyannote 3.1 | ~10% | WhisperX, standalone |
| NVIDIA NeMo | <10% | Standalone |
| SpeechBrain | ~10% | Standalone |

## Key Insights

### Accuracy Leaders (2025)

1. **NVIDIA NeMo Parakeet TDT 0.6B v2** - 6.05% WER, #1 on HuggingFace
2. **AssemblyAI Universal-2** - 8.4% WER, best commercial
3. **Google Chirp** - ~8% WER with volume pricing

### Speed Leaders

1. **SenseVoice-Small** - 70ms for 10s audio (15x faster than Whisper-Large)
2. **faster-whisper + int8** - 4x faster than vanilla Whisper
3. **Deepgram Nova-3** - 150ms streaming latency

### For This System (RTX 4070 12GB)

| Priority | Recommendation |
|----------|---------------|
| Best Accuracy | NeMo Parakeet TDT |
| Best Speed | faster-whisper (int8) |
| Best Features | WhisperX (diarization) |
| Fastest | SenseVoice-Small |
| Privacy | Any local option |

### Performance Expectations

| Model | VRAM | Speed (10s audio) |
|-------|------|-------------------|
| faster-whisper Large (int8) | 3GB | ~0.8s |
| NeMo Parakeet TDT 0.6B | 4GB | ~0.2s |
| SenseVoice-Small | 2GB | ~0.07s |

**1 hour of audio** processed in ~3-4 minutes with faster-whisper Large on RTX 4070.

## Recommended Stack for Transcripts Plugin

```
Primary:     faster-whisper (Large-v3, int8 quantization)
Diarization: pyannote 3.1
All-in-one:  WhisperX (for batch with alignment)
Real-time:   Vosk or SenseVoice
API Backup:  Deepgram Nova-3 (lowest latency)
```

## Infrastructure Actions

1. **Enable GPU** - Install CUDA toolkit + PyTorch with CUDA
2. **Install faster-whisper** - Best performance/accuracy ratio
3. **Configure quantization** - int8 fits large model in 3GB
4. **Add pyannote** - Speaker diarization capability
5. **Abstract backends** - Port interface supports swapping

## Implications for Plugin

The [[transcripts]] plugin already implements the port/adapter pattern allowing backend flexibility:

```typescript
// src/ports/transcription.ts
interface TranscriptionPort {
  capabilities(): TranscriptionCapabilities;
  transcribe(input, options): Promise<TranscriptionResult>;
}
```

Adapters needed:
- `WhisperAdapter` - Already implemented (whisper-local, whisper-api)
- `FasterWhisperAdapter` - Priority addition
- `NeMoAdapter` - For maximum accuracy
- `SenseVoiceAdapter` - For speed-critical use

## Sources

- [Deepgram Best STT APIs 2025](https://deepgram.com/learn/best-speech-to-text-apis)
- [AssemblyAI Alternatives](https://www.assemblyai.com/blog/deepgram-alternatives)
- [NVIDIA NeMo Parakeet TDT](https://developer.nvidia.com/blog/turbocharge-asr-accuracy-and-speed-with-nvidia-nemo-parakeet-tdt)
- [SenseVoice GitHub](https://github.com/FunAudioLLM/SenseVoice)
- [Choosing Whisper Variants](https://modal.com/blog/choosing-whisper-variants)
- [Top Speaker Diarization 2025](https://www.assemblyai.com/blog/top-speaker-diarization-libraries-and-apis)
- [STT Pricing Breakdown](https://deepgram.com/learn/speech-to-text-api-pricing-breakdown-2025)

---

*Parent: [[2025-12-17]]*
