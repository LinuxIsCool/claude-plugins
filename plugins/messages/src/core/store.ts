/**
 * Message Store
 *
 * Append-only event log with content-addressed storage.
 * Follows patterns from logging plugin (JSONL events + markdown content).
 *
 * Storage structure:
 * .claude/messages/
 * ├── store/
 * │   ├── events/              # Append-only JSONL (source of truth)
 * │   │   └── YYYY/MM/DD/
 * │   │       └── events.jsonl
 * │   └── content/             # Content-addressed markdown files
 * │       └── XX/              # First 2 chars of CID (after prefix)
 * │           └── {cid}.md
 * ├── views/                   # Materialized projections
 * │   ├── threads/
 * │   ├── accounts/
 * │   └── timeline/
 * └── search/
 *     └── index.db             # SQLite FTS5
 */

import { join } from "path";
import { existsSync, mkdirSync, appendFileSync, readFileSync, readdirSync, statSync } from "fs";
import { generateCID } from "./cid";
import type {
  Message,
  MessageInput,
  MessageFilter,
  Account,
  AccountInput,
  Thread,
  ThreadInput,
  Event,
  MessageCreatedEvent,
  AccountCreatedEvent,
  ThreadCreatedEvent,
} from "../types";

const DEFAULT_BASE_PATH = ".claude/messages";

/**
 * Message Store - Core data access layer
 */
export class MessageStore {
  private basePath: string;

  constructor(basePath = DEFAULT_BASE_PATH) {
    this.basePath = basePath;
    this.ensureDirectories();
  }

  // ===========================================================================
  // Directory Management
  // ===========================================================================

  private ensureDirectories(): void {
    const dirs = [
      "store/events",
      "store/content",
      "views/threads",
      "views/accounts",
      "views/timeline",
      "search",
    ];

    for (const dir of dirs) {
      const path = join(this.basePath, dir);
      if (!existsSync(path)) {
        mkdirSync(path, { recursive: true });
      }
    }
  }

  /**
   * Get path for today's event log
   */
  private getEventLogPath(date = new Date()): string {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");

    const dir = join(this.basePath, "store/events", String(year), month, day);
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }

    return join(dir, "events.jsonl");
  }

  /**
   * Get path for a content file
   */
  private getContentPath(cid: string): string {
    // Use characters after "msg_" prefix for directory
    const prefix = cid.slice(4, 6);
    const dir = join(this.basePath, "store/content", prefix);

    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }

    return join(dir, `${cid}.md`);
  }

  // ===========================================================================
  // Event Log
  // ===========================================================================

  /**
   * Append an event to the log
   */
  private appendEvent(event: Event): void {
    const path = this.getEventLogPath();
    appendFileSync(path, JSON.stringify(event) + "\n");
  }

  /**
   * Iterate over all events (for rebuilding views)
   */
  async *getAllEvents(): AsyncGenerator<Event> {
    const eventsDir = join(this.basePath, "store/events");

    if (!existsSync(eventsDir)) {
      return;
    }

    // Scan year directories
    const years = readdirSync(eventsDir).filter((f) =>
      statSync(join(eventsDir, f)).isDirectory()
    );

    for (const year of years.sort()) {
      const yearDir = join(eventsDir, year);
      const months = readdirSync(yearDir).filter((f) =>
        statSync(join(yearDir, f)).isDirectory()
      );

      for (const month of months.sort()) {
        const monthDir = join(yearDir, month);
        const days = readdirSync(monthDir).filter((f) =>
          statSync(join(monthDir, f)).isDirectory()
        );

        for (const day of days.sort()) {
          const eventFile = join(monthDir, day, "events.jsonl");

          if (existsSync(eventFile)) {
            const content = readFileSync(eventFile, "utf-8");

            for (const line of content.trim().split("\n")) {
              if (line) {
                yield JSON.parse(line) as Event;
              }
            }
          }
        }
      }
    }
  }

  // ===========================================================================
  // Messages
  // ===========================================================================

  /**
   * Create a new message
   *
   * Write order: content file first, then event log.
   * This ensures that if crash occurs after content write, we have the content
   * and can detect missing event on next scan. Event without content is harder to recover.
   */
  async createMessage(input: MessageInput): Promise<Message> {
    const id = generateCID(input);

    const message: Message = {
      ...input,
      id,
      imported_at: Date.now(),
    };

    // Write content file first (recoverable if event write fails)
    await this.writeContentFile(message);

    // Then append to event log (source of truth)
    const event: MessageCreatedEvent = {
      ts: new Date().toISOString(),
      op: "message.created",
      data: message,
    };
    this.appendEvent(event);

    return message;
  }

  /**
   * Write message as markdown content file
   */
  private async writeContentFile(message: Message): Promise<void> {
    const path = this.getContentPath(message.id);

    // Build YAML frontmatter
    const frontmatter: Record<string, unknown> = {
      id: message.id,
      kind: message.kind,
      account_id: message.account_id,
      created_at: message.created_at,
      imported_at: message.imported_at,
    };

    if (message.author.did) frontmatter.author_did = message.author.did;
    if (message.author.name) frontmatter.author_name = message.author.name;
    if (message.title) frontmatter.title = message.title;
    if (message.visibility) frontmatter.visibility = message.visibility;

    if (message.refs.thread_id) frontmatter.thread_id = message.refs.thread_id;
    if (message.refs.reply_to) frontmatter.reply_to = message.refs.reply_to;
    if (message.refs.room_id) frontmatter.room_id = message.refs.room_id;

    frontmatter.platform = message.source.platform;
    if (message.source.platform_id) frontmatter.platform_id = message.source.platform_id;
    if (message.source.session_id) frontmatter.session_id = message.source.session_id;
    if (message.source.agent_id) frontmatter.agent_id = message.source.agent_id;

    if (message.tags && message.tags.length > 0) {
      frontmatter.tags = message.tags;
    }

    // Format YAML
    const yamlLines = Object.entries(frontmatter).map(([key, value]) => {
      if (typeof value === "string") {
        // Quote strings that might need it
        if (value.includes(":") || value.includes("#") || value.includes("\n")) {
          return `${key}: "${value.replace(/"/g, '\\"')}"`;
        }
        return `${key}: ${value}`;
      }
      return `${key}: ${JSON.stringify(value)}`;
    });

    const content = `---
${yamlLines.join("\n")}
---

${message.content}
`;

    await Bun.write(path, content);
  }

  /**
   * Get a message by CID
   */
  async getMessage(id: string): Promise<Message | null> {
    // Check content file exists
    const path = this.getContentPath(id);

    if (!existsSync(path)) {
      return null;
    }

    // Parse content file - but for now, scan events (content file parsing is complex)
    // TODO: Implement content file parsing
    for await (const event of this.getAllEvents()) {
      if (event.op === "message.created" && (event as MessageCreatedEvent).data.id === id) {
        return (event as MessageCreatedEvent).data;
      }
    }

    return null;
  }

  /**
   * List messages with optional filtering
   */
  async *listMessages(filter?: MessageFilter): AsyncGenerator<Message> {
    let count = 0;
    const limit = filter?.limit ?? Infinity;
    const offset = filter?.offset ?? 0;
    let skipped = 0;

    for await (const event of this.getAllEvents()) {
      if (event.op !== "message.created") continue;

      const message = (event as MessageCreatedEvent).data;

      // Apply filters
      if (filter?.kinds && !filter.kinds.includes(message.kind as number)) continue;
      if (filter?.accounts && !filter.accounts.includes(message.account_id)) continue;
      if (filter?.threads && message.refs.thread_id && !filter.threads.includes(message.refs.thread_id)) continue;
      if (filter?.platforms && !filter.platforms.includes(message.source.platform)) continue;
      if (filter?.since && message.created_at < filter.since) continue;
      if (filter?.until && message.created_at > filter.until) continue;

      // Handle offset
      if (skipped < offset) {
        skipped++;
        continue;
      }

      // Check limit
      if (count >= limit) break;

      yield message;
      count++;
    }
  }

  // ===========================================================================
  // Accounts
  // ===========================================================================

  /**
   * Create a new account
   */
  async createAccount(input: AccountInput): Promise<Account> {
    const account: Account = {
      ...input,
      created_at: Date.now(),
      stats: {
        message_count: 0,
      },
    };

    // Append to event log
    const event: AccountCreatedEvent = {
      ts: new Date().toISOString(),
      op: "account.created",
      data: account,
    };
    this.appendEvent(event);

    // Write account view file (fire and forget - views are derived)
    void this.writeAccountFile(account);

    return account;
  }

  /**
   * Write account to views
   */
  private async writeAccountFile(account: Account): Promise<void> {
    const path = join(this.basePath, "views/accounts", `${account.id}.md`);

    const frontmatter: Record<string, unknown> = {
      id: account.id,
      name: account.name,
      created_at: account.created_at,
    };

    if (account.did) frontmatter.did = account.did;
    if (account.avatar) frontmatter.avatar = account.avatar;
    if (account.identities.length > 0) frontmatter.identities = account.identities;
    if (account.agent) frontmatter.agent = account.agent;

    const yamlLines = Object.entries(frontmatter).map(([key, value]) => {
      if (typeof value === "string") return `${key}: ${value}`;
      return `${key}: ${JSON.stringify(value)}`;
    });

    const content = `---
${yamlLines.join("\n")}
---

# ${account.name}

${account.identities.map((i) => `- ${i.platform}: ${i.handle}`).join("\n")}
`;

    await Bun.write(path, content);
  }

  /**
   * Get an account by ID
   */
  async getAccount(id: string): Promise<Account | null> {
    for await (const event of this.getAllEvents()) {
      if (event.op === "account.created" && (event as AccountCreatedEvent).data.id === id) {
        return (event as AccountCreatedEvent).data;
      }
    }
    return null;
  }

  /**
   * Get or create an account
   */
  async getOrCreateAccount(input: AccountInput): Promise<Account> {
    const existing = await this.getAccount(input.id);
    if (existing) return existing;
    return this.createAccount(input);
  }

  /**
   * List all accounts
   */
  async *listAccounts(limit?: number): AsyncGenerator<Account> {
    const seen = new Set<string>();
    let count = 0;
    const maxCount = limit ?? Infinity;

    for await (const event of this.getAllEvents()) {
      if (event.op === "account.created") {
        const account = (event as AccountCreatedEvent).data;
        if (!seen.has(account.id)) {
          seen.add(account.id);
          yield account;
          count++;
          if (count >= maxCount) return;
        }
      }
    }
  }

  // ===========================================================================
  // Threads
  // ===========================================================================

  /**
   * Create a new thread
   */
  async createThread(input: ThreadInput): Promise<Thread> {
    const thread: Thread = {
      ...input,
      created_at: Date.now(),
      message_count: 0,
    };

    // Append to event log
    const event: ThreadCreatedEvent = {
      ts: new Date().toISOString(),
      op: "thread.created",
      data: thread,
    };
    this.appendEvent(event);

    // Write thread view file (fire and forget - views are derived)
    void this.writeThreadFile(thread);

    return thread;
  }

  /**
   * Write thread to views
   */
  private async writeThreadFile(thread: Thread): Promise<void> {
    const path = join(this.basePath, "views/threads", `${thread.id}.md`);

    const frontmatter: Record<string, unknown> = {
      id: thread.id,
      type: thread.type,
      platform: thread.source.platform,
      created_at: thread.created_at,
      message_count: thread.message_count,
    };

    if (thread.title) frontmatter.title = thread.title;
    if (thread.participants.length > 0) frontmatter.participants = thread.participants;
    if (thread.last_message_at) frontmatter.last_message_at = thread.last_message_at;

    const yamlLines = Object.entries(frontmatter).map(([key, value]) => {
      if (typeof value === "string") return `${key}: ${value}`;
      return `${key}: ${JSON.stringify(value)}`;
    });

    const content = `---
${yamlLines.join("\n")}
---

# ${thread.title || `Thread ${thread.id}`}

Type: ${thread.type}
Platform: ${thread.source.platform}
Messages: ${thread.message_count}
`;

    await Bun.write(path, content);
  }

  /**
   * Get a thread by ID
   */
  async getThread(id: string): Promise<Thread | null> {
    for await (const event of this.getAllEvents()) {
      if (event.op === "thread.created" && (event as ThreadCreatedEvent).data.id === id) {
        return (event as ThreadCreatedEvent).data;
      }
    }
    return null;
  }

  /**
   * Get or create a thread
   */
  async getOrCreateThread(input: ThreadInput): Promise<Thread> {
    const existing = await this.getThread(input.id);
    if (existing) return existing;
    return this.createThread(input);
  }

  /**
   * List all threads
   */
  async *listThreads(limit?: number): AsyncGenerator<Thread> {
    const seen = new Set<string>();
    let count = 0;
    const maxCount = limit ?? Infinity;

    for await (const event of this.getAllEvents()) {
      if (event.op === "thread.created") {
        const thread = (event as ThreadCreatedEvent).data;
        if (!seen.has(thread.id)) {
          seen.add(thread.id);
          yield thread;
          count++;
          if (count >= maxCount) return;
        }
      }
    }
  }

  /**
   * Get messages in a thread
   */
  async *getThreadMessages(threadId: string): AsyncGenerator<Message> {
    for await (const message of this.listMessages({ threads: [threadId] })) {
      yield message;
    }
  }

  // ===========================================================================
  // Statistics
  // ===========================================================================

  /**
   * Get store statistics
   */
  async getStats(): Promise<{
    messageCount: number;
    accountCount: number;
    threadCount: number;
    platforms: string[];
    dateRange: { first: number; last: number } | null;
  }> {
    let messageCount = 0;
    let accountCount = 0;
    let threadCount = 0;
    const platforms = new Set<string>();
    let first: number | null = null;
    let last: number | null = null;

    for await (const event of this.getAllEvents()) {
      if (event.op === "message.created") {
        messageCount++;
        const msg = (event as MessageCreatedEvent).data;
        platforms.add(msg.source.platform);

        if (first === null || msg.created_at < first) first = msg.created_at;
        if (last === null || msg.created_at > last) last = msg.created_at;
      } else if (event.op === "account.created") {
        accountCount++;
      } else if (event.op === "thread.created") {
        threadCount++;
      }
    }

    return {
      messageCount,
      accountCount,
      threadCount,
      platforms: Array.from(platforms),
      dateRange: first !== null && last !== null ? { first, last } : null,
    };
  }
}

/**
 * Create a message store instance
 */
export function createStore(basePath?: string): MessageStore {
  return new MessageStore(basePath);
}
