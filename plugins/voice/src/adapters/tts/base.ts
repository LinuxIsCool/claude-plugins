/**
 * Base TTS Adapter
 *
 * Shared utilities and base implementation for TTS adapters.
 */

import { spawn } from "child_process";
import type { TTSPort, TTSCapabilities, TTSOptions, TTSResult, VoiceInfo } from "../../ports/tts.js";

/**
 * Play audio using system audio player
 * Works on Linux with paplay/aplay, macOS with afplay
 */
export async function playAudioBuffer(audio: Buffer, format: string = "mp3"): Promise<void> {
  return new Promise((resolve, reject) => {
    // Try paplay first (PulseAudio), fall back to aplay (ALSA)
    const players = process.platform === "darwin"
      ? [["afplay", ["-"]]]
      : [
          ["paplay", ["--raw", "--format=s16le", "--rate=44100", "--channels=1"]],
          ["mpv", ["--no-terminal", "--no-video", "-"]],
          ["ffplay", ["-nodisp", "-autoexit", "-"]],
        ];

    // For MP3, we need to decode first or use a player that handles MP3
    const mp3Players = process.platform === "darwin"
      ? [["afplay", ["-"]]]
      : [
          ["mpv", ["--no-terminal", "--no-video", "-"]],
          ["ffplay", ["-nodisp", "-autoexit", "-"]],
        ];

    const playerList = format === "mp3" ? mp3Players : players;

    const tryPlayer = (index: number) => {
      if (index >= playerList.length) {
        reject(new Error("No audio player available"));
        return;
      }

      const [cmd, args] = playerList[index];
      const proc = spawn(cmd, args, { stdio: ["pipe", "ignore", "ignore"] });

      proc.on("error", () => {
        tryPlayer(index + 1);
      });

      proc.on("close", (code) => {
        if (code === 0) {
          resolve();
        } else {
          tryPlayer(index + 1);
        }
      });

      proc.stdin.write(audio);
      proc.stdin.end();
    };

    tryPlayer(0);
  });
}

/**
 * Get API key from environment
 */
export function getEnvVar(name: string): string | undefined {
  return process.env[name];
}

/**
 * Base TTS adapter with common functionality
 */
export abstract class BaseTTSAdapter implements TTSPort {
  protected config: Record<string, unknown>;

  constructor(config: Record<string, unknown> = {}) {
    this.config = config;
  }

  abstract name(): string;
  abstract capabilities(): TTSCapabilities;
  abstract isAvailable(): Promise<boolean>;
  abstract synthesize(text: string, options: TTSOptions): Promise<TTSResult>;
  abstract listVoices(): Promise<VoiceInfo[]>;

  async play(audio: Buffer): Promise<void> {
    const caps = this.capabilities();
    const format = caps.supportedFormats[0] || "mp3";
    await playAudioBuffer(audio, format);
  }

  /**
   * Speak text using this adapter (convenience method)
   */
  async speak(text: string, options: TTSOptions): Promise<void> {
    const result = await this.synthesize(text, options);
    await this.play(result.audio);
  }
}
