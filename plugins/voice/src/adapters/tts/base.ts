/**
 * Base TTS Adapter
 *
 * Shared utilities and base implementation for TTS adapters.
 */

import { spawn, execSync } from "child_process";
import { writeFileSync, unlinkSync, existsSync, mkdirSync } from "fs";
import { join } from "path";
import { tmpdir } from "os";
import type { TTSPort, TTSCapabilities, TTSOptions, TTSResult, VoiceInfo } from "../../ports/tts.js";

/**
 * Generate silence buffer (MP3 format)
 * Creates a short silence to prevent audio clipping at start
 */
function generateSilencePadding(durationMs: number = 100): Buffer {
  // For MP3, we prepend a very short silence using ffmpeg if available
  // This is a minimal valid MP3 frame (silence)
  // Alternatively, we handle this in the playback command
  return Buffer.alloc(0); // We'll handle padding via playback options instead
}

/**
 * Get temp file path for audio
 */
function getTempAudioPath(format: string): string {
  const tempDir = join(tmpdir(), "claude-voice");
  if (!existsSync(tempDir)) {
    mkdirSync(tempDir, { recursive: true });
  }
  return join(tempDir, `audio-${Date.now()}.${format}`);
}

/**
 * Global audio lock file to prevent overlapping playback across all Claude instances
 */
const AUDIO_LOCK_FILE = "/tmp/claude-voice-audio.lock";

/**
 * Kill any currently playing audio to prevent overlap
 */
async function killCurrentAudio(): Promise<void> {
  try {
    // Kill any running mpv/ffplay processes playing our temp audio files
    // The temp files are in /tmp/claude-voice/audio-*.mp3
    execSync("pkill -f 'mpv.*/tmp/claude-voice/audio-' 2>/dev/null || true", { stdio: "ignore" });
    execSync("pkill -f 'ffplay.*/tmp/claude-voice/audio-' 2>/dev/null || true", { stdio: "ignore" });
    execSync("pkill -f 'paplay.*/tmp/claude-voice/audio-' 2>/dev/null || true", { stdio: "ignore" });
  } catch {
    // Ignore errors - processes may not exist
  }
}

/**
 * Acquire global audio playback lock
 * Returns true if lock acquired (and previous audio killed), false if should skip
 */
async function acquireAudioLock(): Promise<boolean> {
  try {
    // Check if lock exists and is recent
    if (existsSync(AUDIO_LOCK_FILE)) {
      const stat = await import("fs").then(fs => fs.statSync(AUDIO_LOCK_FILE));
      const ageMs = Date.now() - stat.mtimeMs;

      if (ageMs < 60000) {
        // Lock is recent - kill current audio and take over
        await killCurrentAudio();
      }
      // Remove stale lock
      unlinkSync(AUDIO_LOCK_FILE);
    }

    // Create new lock with our PID
    writeFileSync(AUDIO_LOCK_FILE, `${process.pid}\n${Date.now()}`);
    return true;
  } catch {
    return true; // Proceed anyway on error
  }
}

/**
 * Release global audio playback lock
 */
function releaseAudioLock(): void {
  try {
    unlinkSync(AUDIO_LOCK_FILE);
  } catch {
    // Ignore - file may not exist
  }
}

/**
 * Play audio using system audio player
 * Uses temp file approach for reliable playback without clipping
 * Works on Linux with mpv/ffplay, macOS with afplay
 * Includes global lock to prevent overlapping audio across Claude instances
 */
export async function playAudioBuffer(audio: Buffer, format: string = "mp3"): Promise<void> {
  // Acquire global audio lock (kills any current playback)
  await acquireAudioLock();

  // Write to temp file to avoid stdin buffering issues that cause clipping
  const tempPath = getTempAudioPath(format);

  try {
    writeFileSync(tempPath, audio);

    return new Promise((resolve, reject) => {
      // Players with options optimized for smooth playback
      // mpv: --audio-buffer for pre-buffering, --demuxer-readahead-secs for read-ahead
      const players = process.platform === "darwin"
        ? [
            ["afplay", [tempPath]],
          ]
        : [
            // mpv with audio buffer to prevent clipping
            ["mpv", [
              "--no-terminal",
              "--no-video",
              "--audio-buffer=0.2",           // 200ms audio buffer
              "--demuxer-readahead-secs=0.5", // Read ahead
              "--hr-seek=no",                 // Disable seeking overhead
              tempPath
            ]],
            // ffplay with buffer options
            ["ffplay", [
              "-nodisp",
              "-autoexit",
              "-infbuf",                      // Infinite buffer (read all before playing)
              "-probesize", "32",             // Faster probe
              tempPath
            ]],
            // paplay for raw PCM (won't work for MP3)
            ["paplay", [tempPath]],
          ];

      const tryPlayer = (index: number) => {
        if (index >= players.length) {
          // Clean up and reject
          try { unlinkSync(tempPath); } catch {}
          releaseAudioLock();
          reject(new Error("No audio player available"));
          return;
        }

        const [cmd, args] = players[index];
        const proc = spawn(cmd, args as string[], { stdio: ["ignore", "ignore", "ignore"] });

        proc.on("error", () => {
          tryPlayer(index + 1);
        });

        proc.on("close", (code) => {
          // Clean up temp file and release lock
          try { unlinkSync(tempPath); } catch {}
          releaseAudioLock();

          if (code === 0) {
            resolve();
          } else {
            tryPlayer(index + 1);
          }
        });
      };

      tryPlayer(0);
    });
  } catch (err) {
    // Clean up on error
    try { unlinkSync(tempPath); } catch {}
    releaseAudioLock();
    throw err;
  }
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
