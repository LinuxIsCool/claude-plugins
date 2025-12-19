---
id: 2025-12-19-1330
title: "Voice Quality Testing Framework Implementation"
type: atomic
created: 2025-12-19T13:30:47
author: claude-opus-4
description: "Built comprehensive TTS quality testing framework with metrics collection, A/B testing, regression detection, and CI integration"
tags: [voice, testing, tts, quality, implementation, feature-dev]
parent_daily: [[2025-12-19]]
related: []
---

# Voice Quality Testing Framework Implementation

Implemented a complete quality testing framework for the voice plugin's TTS backends. This enables automated performance benchmarking, backend comparison, and regression detection for text-to-speech synthesis.

## Context

The voice plugin supports multiple TTS backends (pyttsx3, ElevenLabs, HuggingFace XTTS) but had no systematic way to measure or compare their performance. The spec in `plugins/voice/specs/03-quality-testing/SPEC.md` outlined the requirements for a testing framework. The user invoked the feature-dev workflow to implement it.

## Architecture Decision

Chose a **minimal architecture** (4 core files, ~590 lines) over a clean architecture approach (15+ files). Rationale:

1. This is an internal testing tool, not user-facing code
2. Scope is well-defined (latency metrics, success rate, throughput)
3. Audio quality analysis explicitly out of scope for v1
4. Faster to implement and easier to understand
5. Can refactor later if extension points become necessary

The single `QualityTester` class handles metrics collection, A/B testing, and regression detection. While this violates single-responsibility principle in strict terms, it keeps related functionality cohesive and the file navigable.

## Implementation Details

### Files Created

| File | Lines | Purpose |
|------|-------|---------|
| `src/quality/types.ts` | ~130 | Type definitions (QualityMetrics, ABTestResult, RegressionReport, etc.) |
| `src/quality/tester.ts` | ~590 | Core QualityTester class with all testing logic |
| `src/quality/cli.ts` | ~220 | CLI interface (benchmark, compare, regression, baseline, list) |
| `src/quality/tester.test.ts` | ~230 | Integration tests using bun:test |
| `src/quality/index.ts` | ~30 | Public API exports |
| `src/quality/gates.json` | 5 | Default quality gates configuration |
| `.github/workflows/voice-quality.yml` | 45 | CI workflow for automated quality checks |

### Key Design Choices

**Percentile Calculation**: Used linear interpolation rather than nearest-rank method:
```typescript
const pos = (p / 100) * (sorted.length - 1);
const lower = Math.floor(pos);
const weight = pos - lower;
return sorted[lower] * (1 - weight) + sorted[upper] * weight;
```
This provides accurate percentiles even for small sample sizes common in TTS testing.

**Weighted Scoring for A/B Tests**: The comparison uses 40% latency, 40% success rate, 20% throughput. This prioritizes reliability equally with speed while keeping throughput as a secondary consideration.

**Graceful Degradation**: Tests skip unavailable backends rather than failing. The framework records errors in metrics but continues testing other samples.

**JSONL Storage**: Metrics are appended to `.claude/voice/quality/metrics.jsonl` using `appendFileSync` for atomic writes, preventing race conditions when multiple test runs execute concurrently.

### Bugs Found and Fixed During Code Review

1. **Incorrect percentile formula** - Original used `Math.ceil((p/100) * length) - 1` which produced wrong results
2. **Division by zero in confidence calculation** - When both backend scores are 0
3. **Division by zero in regression detection** - When baseline latency is 0
4. **Race condition in JSONL append** - Was using read-concat-write instead of appendFileSync
5. **Hardcoded backend list in CLI** - Now queries factory dynamically via `listBackends()`

## CLI Usage

```bash
# List available backends with availability status
bun run quality:list

# Benchmark a specific backend
bun run quality:benchmark pyttsx3

# Compare two backends head-to-head
bun run quality:compare pyttsx3 huggingface-xtts

# Check for regressions against baseline
bun run quality:regression pyttsx3

# Establish a new baseline
bun run quality:baseline pyttsx3
```

## Test Results

All 11 tests pass. The framework handles environments where TTS backends aren't fully configured by gracefully skipping synthesis and reporting warnings rather than failing.

## Integration Points

- Uses existing `TTSPort` interface and `TTSBackendFactory`
- Follows established JSONL logging pattern from `voice-hook.ts`
- Added npm scripts to `package.json` for easy invocation
- Created GitHub Actions workflow for CI integration

## Insights

The feature-dev workflow proved effective for this implementation:
1. **Discovery phase** caught that the spec was comprehensive but location was ambiguous
2. **Exploration agents** mapped the hexagonal architecture quickly
3. **Clarifying questions** resolved key decisions upfront (location, test type, backends, CI)
4. **Code review agents** caught 5 real bugs that would have shipped otherwise

The percentile bug was particularly insidious - it would have produced plausible-looking but incorrect metrics, only detectable by careful statistical analysis.

## Future Work

1. Establish initial baselines once TTS backends are properly configured in the environment
2. Add audio quality metrics (v2) using spectrogram/pitch analysis
3. Consider extracting repeated CLI validation patterns into helper function
4. Add webhook integration for external monitoring systems

---

*Parent: [[2025-12-19]]*
