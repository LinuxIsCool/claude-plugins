---
id: 2025-12-18-1531
title: "GPU Transcription Breakthrough"
type: atomic
created: 2025-12-18T15:31:57-08:00
author: claude-opus-4
description: "Resolved cuDNN library path issue enabling GPU-accelerated transcription, fixed ESM imports, installed pyannote-audio"
tags: [transcripts-plugin, gpu, cuda, cudnn, faster-whisper, pyannote, dependency-management]
parent_daily: [[2025-12-18]]
related: []
---

# GPU Transcription Breakthrough

A productive session debugging and fixing the shared ML environment for the [[transcripts-plugin]].

## Context

Continued work from yesterday on the transcripts plugin. The `FasterWhisperAdapter` was created but GPU acceleration wasn't working due to cuDNN library path issues. The session began by picking up where we left off - investigating why `libcudnn_ops.so.9.1.0` couldn't be found.

## The Problem

The `nvidia-cudnn-cu12` package installs cuDNN libraries to a nested path:
```
~/.venvs/ml/lib/python3.11/site-packages/nvidia/cudnn/lib/
```

But `ctranslate2` (faster-whisper's backend) searches standard library paths and couldn't find them. The error:
```
Unable to load any of {libcudnn_ops.so.9.1.0, libcudnn_ops.so.9.1, ...}
```

## The Solution

Set `LD_LIBRARY_PATH` when spawning Python processes:

```typescript
const cudnnPath = getCudnnLibPath();
const env = {
  ...process.env,
  LD_LIBRARY_PATH: cudnnPath + (process.env.LD_LIBRARY_PATH ? `:${process.env.LD_LIBRARY_PATH}` : ""),
};
const proc = spawn(pythonPath, ["-c", script], { env });
```

This simple fix enabled GPU transcription with impressive results:

| Model | Device | Load | Inference |
|-------|--------|------|-----------|
| tiny | CPU | 400ms | 400ms |
| tiny | CUDA | 500ms | 310ms |
| base | CUDA | 350ms | 120ms |

## ESM Import Fixes

The TypeScript codebase had mixed ESM import styles. Fixed all relative imports to use `.js` extensions as required by Node's `node16` module resolution.

## Pyannote Installation

Added `pyannote-audio 4.0.3` to the shared ML environment for speaker diarization. This triggered dependency hell - pyannote pulled in incompatible torch versions.

**Key learning**: Always reinstall the PyTorch ecosystem together from the same index:
```bash
uv pip install torch==2.5.1+cu121 torchvision==0.20.1+cu121 torchaudio==2.5.1+cu121 \
  --index-url https://download.pytorch.org/whl/cu121
```

## Insights

1. **Library path isolation**: Python venvs isolate packages well, but CUDA libraries need explicit `LD_LIBRARY_PATH` injection
2. **GPU can be faster with larger models**: The base model (350ms load, 120ms inference) outperformed tiny due to better GPU occupancy
3. **Dependency pinning is critical**: ML ecosystems have tight version coupling; always pin core deps together

## Shared ML Environment Status

`~/.venvs/ml` now contains:
- PyTorch 2.5.1+cu121
- torchaudio 2.5.1+cu121
- faster-whisper 1.2.1
- pyannote-audio 4.0.3
- nvidia-cudnn-cu12 9.1.0

Next: Build `PyAnnoteAdapter` for speaker diarization (requires HuggingFace token for pretrained models).

---

*Parent: [[2025-12-18]]*
