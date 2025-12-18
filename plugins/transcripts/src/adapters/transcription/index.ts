/**
 * Transcription Adapters
 *
 * Backend implementations for TranscriptionPort.
 */

export * from "./whisper";

import type { TranscriptionPort, TranscriptionBackendFactory } from "../../ports/transcription";
import { WhisperAdapter, type WhisperConfig } from "./whisper";

/**
 * Available transcription backends
 */
const BACKENDS: Record<string, (config?: Record<string, unknown>) => TranscriptionPort> = {
  whisper: (config) => new WhisperAdapter(config as WhisperConfig),
  "whisper-local": (config) => new WhisperAdapter({ ...config, mode: "local" } as WhisperConfig),
  "whisper-api": (config) => new WhisperAdapter({ ...config, mode: "api" } as WhisperConfig),
};

/**
 * Factory for creating transcription backends
 */
export const transcriptionFactory: TranscriptionBackendFactory = {
  create(name: string, config?: Record<string, unknown>): TranscriptionPort {
    const factory = BACKENDS[name];
    if (!factory) {
      throw new Error(`Unknown transcription backend: ${name}. Available: ${Object.keys(BACKENDS).join(", ")}`);
    }
    return factory(config);
  },

  list(): string[] {
    return Object.keys(BACKENDS);
  },

  default(): TranscriptionPort {
    return new WhisperAdapter();
  },
};
