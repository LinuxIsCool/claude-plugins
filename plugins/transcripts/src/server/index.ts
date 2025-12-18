/**
 * Transcripts MCP Server
 *
 * Exposes transcript functionality as MCP tools.
 * Provides programmatic access to transcription, speaker management, and search.
 */

import { createStore, TranscriptStore } from "../infrastructure/store";
import { transcriptionFactory } from "../adapters/transcription";
import {
  isMessagesPluginAvailable,
  emitTranscriptToMessages,
  getMessagesAccounts,
} from "../infrastructure/messages-bridge";
import type { TranscriptInput } from "../domain/entities/transcript";
import type { SpeakerInput } from "../domain/entities/speaker";

// MCP protocol types
interface MCPRequest {
  jsonrpc: "2.0";
  id: string | number;
  method: string;
  params?: Record<string, unknown>;
}

interface MCPResponse {
  jsonrpc: "2.0";
  id: string | number;
  result?: unknown;
  error?: {
    code: number;
    message: string;
    data?: unknown;
  };
}

/**
 * Transcripts MCP Server
 */
export class TranscriptsMCPServer {
  private store: TranscriptStore;

  constructor() {
    this.store = createStore();
  }

  /**
   * Handle MCP request
   */
  async handleRequest(request: MCPRequest): Promise<MCPResponse> {
    const { id, method, params } = request;

    try {
      let result: unknown;

      switch (method) {
        case "initialize":
          result = this.handleInitialize();
          break;

        case "tools/list":
          result = this.handleToolsList();
          break;

        case "tools/call":
          result = await this.handleToolCall(params as { name: string; arguments: Record<string, unknown> });
          break;

        default:
          return {
            jsonrpc: "2.0",
            id,
            error: {
              code: -32601,
              message: `Method not found: ${method}`,
            },
          };
      }

      return { jsonrpc: "2.0", id, result };
    } catch (error) {
      return {
        jsonrpc: "2.0",
        id,
        error: {
          code: -32000,
          message: error instanceof Error ? error.message : String(error),
        },
      };
    }
  }

  /**
   * Handle initialize request
   */
  private handleInitialize() {
    return {
      protocolVersion: "2024-11-05",
      capabilities: {
        tools: {},
      },
      serverInfo: {
        name: "transcripts",
        version: "0.1.0",
      },
    };
  }

  /**
   * List available tools
   */
  private handleToolsList() {
    return {
      tools: [
        {
          name: "transcripts_transcribe",
          description: "Transcribe an audio or video file",
          inputSchema: {
            type: "object",
            properties: {
              file_path: { type: "string", description: "Path to audio/video file" },
              title: { type: "string", description: "Optional title for the transcript" },
              backend: {
                type: "string",
                description: "Transcription backend (whisper, whisper-api)",
                enum: transcriptionFactory.list(),
              },
              language: { type: "string", description: "Language code (e.g., 'en', 'es')" },
              model: { type: "string", description: "Model to use (e.g., 'base', 'large-v3')" },
            },
            required: ["file_path"],
          },
        },
        {
          name: "transcripts_list",
          description: "List all transcripts",
          inputSchema: {
            type: "object",
            properties: {
              limit: { type: "number", description: "Max results (default 20)" },
            },
          },
        },
        {
          name: "transcripts_get",
          description: "Get a transcript by ID",
          inputSchema: {
            type: "object",
            properties: {
              id: { type: "string", description: "Transcript ID (tx_...)" },
            },
            required: ["id"],
          },
        },
        {
          name: "transcripts_speakers_list",
          description: "List all speakers in the database",
          inputSchema: {
            type: "object",
            properties: {
              limit: { type: "number", description: "Max results (default 50)" },
            },
          },
        },
        {
          name: "transcripts_speaker_create",
          description: "Create a new speaker profile",
          inputSchema: {
            type: "object",
            properties: {
              name: { type: "string", description: "Speaker name" },
              aliases: {
                type: "array",
                items: { type: "string" },
                description: "Alternative names",
              },
              description: { type: "string", description: "Description of the speaker" },
            },
            required: ["name"],
          },
        },
        {
          name: "transcripts_speaker_get",
          description: "Get a speaker by ID",
          inputSchema: {
            type: "object",
            properties: {
              id: { type: "string", description: "Speaker ID (spk_...)" },
            },
            required: ["id"],
          },
        },
        {
          name: "transcripts_stats",
          description: "Get statistics about the transcript store",
          inputSchema: {
            type: "object",
            properties: {},
          },
        },
        {
          name: "transcripts_emit_to_messages",
          description: "Emit a transcript to the messages plugin",
          inputSchema: {
            type: "object",
            properties: {
              transcript_id: { type: "string", description: "Transcript ID to emit" },
            },
            required: ["transcript_id"],
          },
        },
        {
          name: "transcripts_backends_list",
          description: "List available transcription backends",
          inputSchema: {
            type: "object",
            properties: {},
          },
        },
      ],
    };
  }

  /**
   * Handle tool call
   */
  private async handleToolCall(params: { name: string; arguments: Record<string, unknown> }) {
    const { name, arguments: args } = params;

    switch (name) {
      case "transcripts_transcribe":
        return this.toolTranscribe(args);

      case "transcripts_list":
        return this.toolList(args);

      case "transcripts_get":
        return this.toolGet(args);

      case "transcripts_speakers_list":
        return this.toolSpeakersList(args);

      case "transcripts_speaker_create":
        return this.toolSpeakerCreate(args);

      case "transcripts_speaker_get":
        return this.toolSpeakerGet(args);

      case "transcripts_stats":
        return this.toolStats();

      case "transcripts_emit_to_messages":
        return this.toolEmitToMessages(args);

      case "transcripts_backends_list":
        return this.toolBackendsList();

      default:
        throw new Error(`Unknown tool: ${name}`);
    }
  }

  /**
   * Transcribe audio file
   */
  private async toolTranscribe(args: Record<string, unknown>) {
    const filePath = args.file_path as string;
    const title = args.title as string | undefined;
    const backendName = (args.backend as string) || "whisper";
    const language = args.language as string | undefined;
    const model = args.model as string | undefined;

    // Get backend
    const backend = transcriptionFactory.create(backendName);

    // Check availability
    const available = await backend.isAvailable();
    if (!available) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({
              error: `Backend ${backendName} is not available. Check installation/configuration.`,
            }, null, 2),
          },
        ],
      };
    }

    // Transcribe
    const result = await backend.transcribe(
      { type: "file", path: filePath },
      { language, model }
    );

    // Get file stats
    const fs = require("fs");
    const stats = fs.statSync(filePath);
    const path = require("path");

    // Create transcript
    const input: TranscriptInput = {
      title: title || path.basename(filePath),
      source: {
        mode: "file",
        path: filePath,
        filename: path.basename(filePath),
        type: "audio",
        audio: {
          format: path.extname(filePath).slice(1) as any,
          duration_ms: result.duration_ms,
          file_size_bytes: stats.size,
        },
      },
      utterances: result.utterances.map((u, i) => ({
        ...u,
        index: i,
      })),
      processing: {
        backend: backendName,
        model: result.model,
        language: result.language,
        duration_ms: result.processing_time_ms,
      },
      status: "complete",
    };

    const transcript = await this.store.createTranscript(input);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({
            id: transcript.id,
            title: transcript.title,
            utterance_count: transcript.utterances.length,
            duration_ms: result.duration_ms,
            language: result.language,
            processing_time_ms: result.processing_time_ms,
            model: result.model,
          }, null, 2),
        },
      ],
    };
  }

  /**
   * List transcripts
   */
  private async toolList(args: Record<string, unknown>) {
    const limit = (args.limit as number) || 20;
    const transcripts = [];

    for await (const t of this.store.listTranscripts(limit)) {
      transcripts.push(t);
    }

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({ count: transcripts.length, transcripts }, null, 2),
        },
      ],
    };
  }

  /**
   * Get transcript
   */
  private async toolGet(args: Record<string, unknown>) {
    const id = args.id as string;
    const transcript = await this.store.getTranscript(id);

    if (!transcript) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ error: `Transcript ${id} not found` }, null, 2),
          },
        ],
      };
    }

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({
            id: transcript.id,
            title: transcript.title,
            status: transcript.status,
            speaker_count: new Set(transcript.utterances.map((u) => u.speaker.id)).size,
            utterance_count: transcript.utterances.length,
            duration_ms: transcript.source.audio.duration_ms,
            created_at: new Date(transcript.created_at).toISOString(),
            utterances: transcript.utterances.slice(0, 10).map((u) => ({
              speaker: u.speaker.name,
              start: formatTime(u.start_ms),
              text: u.text.slice(0, 100) + (u.text.length > 100 ? "..." : ""),
            })),
            more_utterances: transcript.utterances.length > 10
              ? transcript.utterances.length - 10
              : 0,
          }, null, 2),
        },
      ],
    };
  }

  /**
   * List speakers
   */
  private async toolSpeakersList(args: Record<string, unknown>) {
    const limit = (args.limit as number) || 50;
    const speakers = [];

    for await (const s of this.store.listSpeakers(limit)) {
      speakers.push(s);
    }

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({ count: speakers.length, speakers }, null, 2),
        },
      ],
    };
  }

  /**
   * Create speaker
   */
  private async toolSpeakerCreate(args: Record<string, unknown>) {
    const input: SpeakerInput = {
      name: args.name as string,
      aliases: args.aliases as string[] | undefined,
      description: args.description as string | undefined,
      fingerprints: [],
      identities: [],
      facts: [],
    };

    const speaker = await this.store.createSpeaker(input);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({
            id: speaker.id,
            name: speaker.name,
            created_at: new Date(speaker.created_at).toISOString(),
          }, null, 2),
        },
      ],
    };
  }

  /**
   * Get speaker
   */
  private async toolSpeakerGet(args: Record<string, unknown>) {
    const id = args.id as string;
    const speaker = await this.store.getSpeaker(id);

    if (!speaker) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ error: `Speaker ${id} not found` }, null, 2),
          },
        ],
      };
    }

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({
            id: speaker.id,
            name: speaker.name,
            aliases: speaker.aliases,
            description: speaker.description,
            has_fingerprint: speaker.fingerprints.length > 0,
            linked_platforms: speaker.identities.map((i) => i.platform),
            facts: speaker.facts,
            stats: speaker.stats,
            created_at: new Date(speaker.created_at).toISOString(),
          }, null, 2),
        },
      ],
    };
  }

  /**
   * Get stats
   */
  private async toolStats() {
    const stats = await this.store.getStats();
    const messagesAvailable = isMessagesPluginAvailable();

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({
            ...stats,
            total_duration: formatTime(stats.totalDurationMs),
            messages_plugin_available: messagesAvailable,
          }, null, 2),
        },
      ],
    };
  }

  /**
   * Emit transcript to messages
   */
  private async toolEmitToMessages(args: Record<string, unknown>) {
    const transcriptId = args.transcript_id as string;

    if (!isMessagesPluginAvailable()) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ error: "Messages plugin not available" }, null, 2),
          },
        ],
      };
    }

    const transcript = await this.store.getTranscript(transcriptId);
    if (!transcript) {
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify({ error: `Transcript ${transcriptId} not found` }, null, 2),
          },
        ],
      };
    }

    const result = await emitTranscriptToMessages(transcript);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({
            transcript_id: transcriptId,
            messages_emitted: result.messagesEmitted,
            thread_created: result.threadCreated,
          }, null, 2),
        },
      ],
    };
  }

  /**
   * List backends
   */
  private toolBackendsList() {
    const backends = transcriptionFactory.list();

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify({
            backends,
            default: "whisper",
          }, null, 2),
        },
      ],
    };
  }

  /**
   * Run the server
   */
  async run(): Promise<void> {
    const reader = Bun.stdin.stream().getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });

      let newlineIndex: number;
      while ((newlineIndex = buffer.indexOf("\n")) !== -1) {
        const line = buffer.slice(0, newlineIndex).trim();
        buffer = buffer.slice(newlineIndex + 1);

        if (line) {
          try {
            const request = JSON.parse(line) as MCPRequest;
            const response = await this.handleRequest(request);
            console.log(JSON.stringify(response));
          } catch (error) {
            console.error("Parse error:", error);
          }
        }
      }
    }
  }
}

/**
 * Format milliseconds as time string
 */
function formatTime(ms: number): string {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);

  if (hours > 0) {
    return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
  }
  if (minutes > 0) {
    return `${minutes}m ${seconds % 60}s`;
  }
  return `${seconds}s`;
}

// Run if executed directly
if (import.meta.main) {
  const server = new TranscriptsMCPServer();
  server.run().catch(console.error);
}
