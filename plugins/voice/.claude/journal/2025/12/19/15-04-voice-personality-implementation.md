---
created: 2025-12-19T15:04:00-08:00
type: implementation
status: complete
tags:
  - voice-plugin
  - personality-system
  - text-transformation
  - feature-dev
parent_daily: "[[2025-12-19]]"
spec: "[[plugins/voice/specs/08-voice-personality/SPEC.md]]"
---

# Voice Personality System Implementation

Implemented the voice personality system from spec `08-voice-personality`, enabling distinct personality profiles for different agents with text transformations, emotional defaults, and configurable TTS settings.

## Architecture Decisions

### SSML Skipped

During the interactive design phase, the question of SSML (Speech Synthesis Markup Language) arose. After investigation, SSML was intentionally excluded because:

- **No backend support**: None of the current TTS backends support SSML:
  - ElevenLabs: Uses proprietary settings (stability, similarity_boost, style)
  - Piper: Neural TTS, no markup support
  - XTTS: Coqui's neural TTS, no markup
  - pyttsx3: Wrapper around system TTS, limited/inconsistent SSML

- **SSML's purpose**: Designed for older rule-based TTS engines (Festival, eSpeak, AWS Polly, Google Cloud TTS). Neural TTS models learn prosody from training data rather than explicit markup.

- **The better path**: Use each backend's native controls (ElevenLabs' stability/similarity_boost, Piper's speaker embeddings) rather than forcing a legacy abstraction.

### Personality Separate from Voice Identity

The personality system is deliberately decoupled from the existing voice identity resolution (`src/identity/resolver.ts`):

| Concern | System | Purpose |
|---------|--------|---------|
| Voice Identity | `resolver.ts` | WHO speaks (voice selection, speaker ID) |
| Personality | `personality/` | HOW they speak (text transforms, emotion, style) |

This separation allows:
- Same voice, different personalities (mentor vs explorer using same ElevenLabs voice)
- Same personality, different voices (mentor on Opus vs Sonnet)
- Independent evolution of both systems

### Text Transformation as Pre-TTS Layer

Text transformation happens BEFORE TTS synthesis, not after audio generation. This is a pure text→text pipeline:

```
Claude Response → PersonalityManager.getForAgent() → TextTransformer.transform() → TTS Synthesis
```

The transformation pipeline:
1. Sentence truncation (maxSentences limit)
2. Code block verbosity adjustment (minimal/moderate/verbose)
3. Filler insertion (~20% of non-first sentences)
4. Greeting prepending (for SessionStart events)

## Files Created

### Core Types (`src/personality/types.ts`)

```typescript
export type EmotionType =
  | "neutral" | "happy" | "calm" | "serious"
  | "enthusiastic" | "concerned" | "thoughtful";

export interface VoicePersonality {
  id: string;
  name: string;
  agentId?: string;
  description?: string;
  style: { speed: number; pitch: number; volume: number; variability: number; };
  ttsSettings: { stability?: number; similarityBoost?: number; styleExaggeration?: number; };
  textTransforms: { addGreeting: boolean; addFillers: boolean; maxSentences?: number; codeVerbosity: "minimal" | "moderate" | "verbose"; };
  emotion: { default: EmotionType; greetingEmotion: EmotionType; errorEmotion: EmotionType; successEmotion: EmotionType; };
}
```

### Presets (`src/personality/presets.ts`)

Five built-in personality presets:
- **professional**: Neutral, minimal fillers, code blocks summarized
- **friendly**: Happy/enthusiastic, greetings enabled, moderate fillers
- **mentor**: Thoughtful, explanatory, patient pacing
- **archivist**: Serious/calm, precise language, verbose code handling
- **explorer**: Enthusiastic, curious, higher speech variability

Emotion-mapped phrase pools:
- `GREETINGS`: Opening phrases by emotion type
- `FILLERS`: Conversational bridges by emotion type

### Manager (`src/personality/manager.ts`)

PersonalityManager with fallback resolution:

```typescript
getForAgent(agentId: string): VoicePersonality {
  // 1. Exact match: "awareness:mentor"
  // 2. Type match: "mentor" (strip namespace)
  // 3. Default personality
}
```

Profile loading from two sources:
- Built-in: `src/personality/profiles/agents/*.json` (read-only)
- User overrides: `.claude/voice/personalities/*.json` (writable)

### Transformer (`src/personality/transformer.ts`)

Pure text transformation functions:
- `truncateSentences()`: Limit response length
- `adjustCodeVerbosity()`: Handle code blocks
- `addFillers()`: Insert conversational phrases
- `addGreeting()`: Prepend emotion-appropriate greeting

### Agent Profiles

JSON personality configurations for:
- `profiles/agents/archivist.json`: Calm, serious, verbose code
- `profiles/agents/mentor.json`: Thoughtful, encouraging, greetings enabled
- `profiles/agents/explorer.json`: Enthusiastic, curious, high variability

## Files Modified

### `hooks/voice-hook.ts`

Added personality transformation to `speak()` function:

```typescript
// Get personality for agent
const personality = getPersonalityManager(cwd).getForAgent(agentId || "default");
const transformer = new TextTransformer(personality);

// Build context from event
const context: TransformContext = {
  eventType,
  isGreeting: eventType === "SessionStart",
  isError: eventType === "Notification",
  isSuccess: eventType === "Stop",
};

// Transform before TTS
transformedText = transformer.transform(text, context);
```

### `src/index.ts`

Added exports for personality system types and functions.

## Quality Issues Fixed

Five issues identified by code-reviewer agents:

| Issue | Confidence | Fix |
|-------|------------|-----|
| Built-in profiles path uses fragile `import.meta.url.replace()` | 100% | Created `getBuiltinProfilesDir()` function with proper file:// handling |
| Agent fallback skips non-namespaced IDs | 85% | Changed to `if (agentId.includes(":"))` guard |
| `addFillers` corrupts sentence capitalization | 90% | Removed lowercase transformation, preserve original |
| Private `cwd` property accessed via bracket notation | 80% | Changed to `readonly cwd` public property |
| Sentence splitting regex duplicated | 85% | Extracted to `SENTENCE_SPLIT_REGEX` constant and `splitSentences()` helper |

## Key Insights

1. **Decoupling enables flexibility**: Voice identity (who) and personality (how) being separate means agents can share voices while having distinct personalities, and personalities can be swapped without changing voice configuration.

2. **Text transformation is the right abstraction**: Rather than trying to control TTS behavior with SSML, transforming the text before synthesis works with any backend and produces more natural results.

3. **Fallback chains provide graceful degradation**: The resolution chain (exact ID → type → default) means new agents automatically get reasonable personalities without explicit configuration.

4. **JSON profiles enable user customization**: Users can override built-in personalities or create new ones by dropping JSON files in `.claude/voice/personalities/`.

---

*Parent: [[2025-12-19]] → [[2025-12]] → [[2025]]*
