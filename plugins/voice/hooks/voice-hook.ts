#!/usr/bin/env bun
/**
 * Unified Voice Hook
 *
 * Handles all Claude Code hook events for voice integration.
 * Events: SessionStart, Stop, Notification, SubagentStop
 */

import { readFileSync, existsSync } from "fs";
import { join } from "path";

// Load .env from project root (cwd passed in hook data)
// This ensures environment variables are available regardless of where Bun was invoked
function loadEnvFile(cwd: string): void {
  const envPath = join(cwd, ".env");
  if (!existsSync(envPath)) return;

  try {
    const content = readFileSync(envPath, "utf-8");
    for (const line of content.split("\n")) {
      const trimmed = line.trim();
      // Skip comments and empty lines
      if (!trimmed || trimmed.startsWith("#")) continue;

      const eqIndex = trimmed.indexOf("=");
      if (eqIndex === -1) continue;

      const key = trimmed.slice(0, eqIndex).trim();
      let value = trimmed.slice(eqIndex + 1).trim();

      // Remove quotes if present
      if ((value.startsWith('"') && value.endsWith('"')) ||
          (value.startsWith("'") && value.endsWith("'"))) {
        value = value.slice(1, -1);
      }

      // Only set if not already in environment (existing env takes precedence)
      if (!(key in process.env)) {
        process.env[key] = value;
      }
    }
  } catch {
    // Silently continue if .env can't be loaded
  }
}

// Import voice modules
import { getDefaultTTSFactory, speakAndPlay } from "../src/adapters/tts/index.js";
import { resolveVoiceForSession, resolveVoiceForAgent, normalizeVoiceSettings } from "../src/identity/resolver.js";
import type { TTSOptions } from "../src/ports/tts.js";

/**
 * Debug logging
 */
const DEBUG = process.env.VOICE_DEBUG === "1";
const LOG_PATH = process.env.VOICE_LOG_PATH || "/tmp/voice-hook.log";

function log(msg: string): void {
  if (DEBUG) {
    const timestamp = new Date().toISOString();
    const logLine = `[${timestamp}] ${msg}\n`;
    Bun.write(LOG_PATH, logLine, { append: true }).catch(() => {});
    console.error(`[voice] ${msg}`);
  }
}

/**
 * Read JSON from stdin
 */
async function readStdin(): Promise<Record<string, unknown>> {
  try {
    const chunks: Uint8Array[] = [];
    for await (const chunk of Bun.stdin.stream()) {
      chunks.push(chunk);
    }
    const text = Buffer.concat(chunks).toString("utf-8");
    return JSON.parse(text || "{}");
  } catch (e) {
    log(`Failed to read stdin: ${e}`);
    return {};
  }
}

/**
 * Extract last assistant response from transcript
 */
function extractResponse(transcriptPath: string): string {
  if (!transcriptPath || !existsSync(transcriptPath)) {
    return "";
  }

  try {
    const content = readFileSync(transcriptPath, "utf-8");
    const lines = content.trim().split("\n").reverse();

    for (const line of lines) {
      if (!line.trim()) continue;

      const entry = JSON.parse(line);
      if (entry.type === "assistant") {
        const message = entry.message || {};
        const blocks = message.content || [];

        for (const block of blocks) {
          if (block.type === "text") {
            const text = block.text || "";
            // Skip system reminders
            if (!text.startsWith("<system-reminder>")) {
              return text;
            }
          }
        }
      }
    }
  } catch (e) {
    log(`Failed to extract response: ${e}`);
  }

  return "";
}

/**
 * Summarize response for TTS (first 2-3 sentences, max ~100 words)
 */
function summarizeForVoice(text: string): string {
  if (!text) return "";

  // Remove markdown code blocks
  let cleaned = text.replace(/```[\s\S]*?```/g, "(code block)");

  // Remove inline code
  cleaned = cleaned.replace(/`[^`]+`/g, "");

  // Remove markdown links, keep text
  cleaned = cleaned.replace(/\[([^\]]+)\]\([^)]+\)/g, "$1");

  // Remove markdown formatting
  cleaned = cleaned.replace(/[*_#]+/g, "");

  // Split into sentences
  const sentences = cleaned
    .split(/(?<=[.!?])\s+/)
    .filter((s) => s.trim().length > 0);

  // Take first 2-3 sentences, max ~100 words
  let result = "";
  let wordCount = 0;
  const maxSentences = 3;
  const maxWords = 100;

  for (let i = 0; i < Math.min(sentences.length, maxSentences); i++) {
    const sentence = sentences[i].trim();
    const words = sentence.split(/\s+/).length;

    if (wordCount + words > maxWords && result) break;

    result += (result ? " " : "") + sentence;
    wordCount += words;
  }

  return result || text.slice(0, 300);
}

/**
 * Get agent info from subagent transcript
 */
function getSubagentInfo(
  transcriptPath: string
): { model: string; summary: string } {
  const result = { model: "", summary: "" };

  if (!transcriptPath || !existsSync(transcriptPath)) {
    return result;
  }

  try {
    const content = readFileSync(transcriptPath, "utf-8");
    const lines = content.trim().split("\n");
    const responses: string[] = [];

    for (const line of lines) {
      if (!line.trim()) continue;
      const entry = JSON.parse(line);

      // Get model from first entry
      if (!result.model) {
        const model = entry.message?.model || "";
        if (model.includes("opus")) result.model = "opus";
        else if (model.includes("sonnet")) result.model = "sonnet";
        else if (model.includes("haiku")) result.model = "haiku";
      }

      // Collect text responses
      const blocks = entry.message?.content || [];
      for (const block of blocks) {
        if (block.type === "text") {
          const text = block.text?.trim();
          if (text && !text.startsWith("<system-reminder>")) {
            responses.push(text);
          }
        }
      }
    }

    // Use last response as summary
    if (responses.length > 0) {
      result.summary = summarizeForVoice(responses[responses.length - 1]);
    }
  } catch (e) {
    log(`Failed to get subagent info: ${e}`);
  }

  return result;
}

/**
 * Speak text using resolved voice configuration
 */
async function speak(
  text: string,
  sessionId: string,
  cwd: string,
  agentId?: string
): Promise<void> {
  if (!text) return;

  log(`Speaking: "${text.slice(0, 50)}..."`);

  try {
    // Resolve voice
    const resolved = agentId
      ? await resolveVoiceForAgent(agentId, cwd)
      : await resolveVoiceForSession(sessionId, cwd);

    log(`Voice resolved: ${resolved.source} -> ${resolved.config.backend}:${resolved.config.voiceId}`);

    // Normalize settings to valid ranges
    const normalizedSettings = normalizeVoiceSettings(resolved.config.settings);

    const options: Partial<TTSOptions> = {
      voiceId: resolved.config.voiceId,
      ...normalizedSettings,
    };

    await speakAndPlay(text, options, resolved.config.backend);
    log("Speech complete");
  } catch (e) {
    log(`Speech failed: ${e}`);
    // Log to stderr so failures are visible even without debug mode
    console.error(`[voice] TTS failed: ${e instanceof Error ? e.message : String(e)}`);
    // Don't throw - voice failure shouldn't break Claude
  }
}

/**
 * Handle SessionStart event
 */
async function handleSessionStart(
  data: Record<string, unknown>
): Promise<void> {
  const sessionId = data.session_id as string;
  const cwd = (data.cwd as string) || ".";

  log(`SessionStart: ${sessionId}`);
  await speak("Ready.", sessionId, cwd);
}

/**
 * Handle Stop event
 */
async function handleStop(data: Record<string, unknown>): Promise<void> {
  const sessionId = data.session_id as string;
  const cwd = (data.cwd as string) || ".";
  const transcriptPath = data.transcript_path as string;

  log(`Stop: ${sessionId}`);

  // Extract and summarize response
  const response = extractResponse(transcriptPath);
  const summary = summarizeForVoice(response);

  if (summary) {
    await speak(summary, sessionId, cwd);
  }
}

/**
 * Handle Notification event
 */
async function handleNotification(
  data: Record<string, unknown>
): Promise<void> {
  const sessionId = data.session_id as string;
  const cwd = (data.cwd as string) || ".";
  const message = (data.message as string) || "I need your attention.";

  log(`Notification: ${sessionId} - ${message}`);
  await speak(message, sessionId, cwd);
}

/**
 * Handle SubagentStop event
 */
async function handleSubagentStop(
  data: Record<string, unknown>
): Promise<void> {
  const sessionId = data.session_id as string;
  const cwd = (data.cwd as string) || ".";
  const agentId = data.agent_id as string;
  const agentTranscriptPath = data.agent_transcript_path as string;

  log(`SubagentStop: ${agentId}`);

  // Get subagent info
  const info = getSubagentInfo(agentTranscriptPath);

  if (info.summary) {
    // Use agent-specific voice
    await speak(info.summary, sessionId, cwd, agentId);
  }
}

/**
 * Main entry point
 */
async function main(): Promise<void> {
  const event = process.argv[2];
  if (!event) {
    console.error("Usage: voice-hook.ts <event>");
    process.exit(1);
  }

  log(`Event: ${event}`);

  // Read input data
  const data = await readStdin();
  log(`Data keys: ${Object.keys(data).join(", ")}`);

  // Load environment from project .env (cwd from hook data)
  // Resolve relative paths against current process directory
  const cwdRaw = (data.cwd as string) || ".";
  const cwd = cwdRaw.startsWith("/") ? cwdRaw : join(process.cwd(), cwdRaw);
  loadEnvFile(cwd);
  log(`Loaded .env from: ${cwd}`);

  // Handle event
  switch (event) {
    case "SessionStart":
      await handleSessionStart(data);
      break;
    case "Stop":
      await handleStop(data);
      break;
    case "Notification":
      await handleNotification(data);
      break;
    case "SubagentStop":
      await handleSubagentStop(data);
      break;
    default:
      log(`Unknown event: ${event}`);
  }
}

// Run
main().catch((e) => {
  log(`Fatal error: ${e}`);
  process.exit(0); // Don't fail the hook
});
