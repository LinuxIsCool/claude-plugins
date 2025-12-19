/**
 * Voice Plugin - Main Entry Point
 *
 * Provides voice input/output capabilities for the Claude Code ecosystem.
 */

// Port interfaces
export type {
  TTSPort,
  TTSCapabilities,
  TTSOptions,
  TTSResult,
  VoiceInfo,
  TTSBackendFactory,
} from "./ports/tts.js";

export type {
  STTPort,
  STTCapabilities,
  STTOptions,
  STTResult,
  AudioInput,
  AudioChunk,
  TranscriptSegment,
  StreamingSTTEvent,
  STTProgressCallback,
  STTBackendFactory,
} from "./ports/stt.js";

export type {
  VADPort,
  VADCapabilities,
  VADOptions,
  VADResult,
  SpeechSegment,
  VADStreamEvent,
  VADBackendFactory,
} from "./ports/vad.js";

// TTS adapters
export {
  TTSFactory,
  createTTSFactory,
  getDefaultTTSFactory,
  speak,
  speakAndPlay,
  ElevenLabsAdapter,
  createElevenLabsAdapter,
  Pyttsx3Adapter,
  createPyttsx3Adapter,
} from "./adapters/tts/index.js";

// Voice identity
export {
  resolveVoiceForSession,
  resolveVoiceForAgent,
  setSessionVoiceOverride,
  normalizeVoiceSettings,
  clampVoiceSetting,
  getSystemDefaultVoice,
  MODEL_VOICE_DEFAULTS,
  AGENT_VOICE_DEFAULTS,
  SYSTEM_DEFAULT_VOICE,
} from "./identity/resolver.js";

export type {
  VoiceConfig,
  ResolvedVoice,
} from "./identity/resolver.js";

// Re-export default options
export { DEFAULT_TTS_OPTIONS } from "./ports/tts.js";
export { DEFAULT_STT_OPTIONS } from "./ports/stt.js";
export { DEFAULT_VAD_OPTIONS } from "./ports/vad.js";
