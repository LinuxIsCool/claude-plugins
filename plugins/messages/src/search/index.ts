/**
 * Search Index
 *
 * SQLite FTS5-based full-text search for messages.
 * Provides fast keyword search with relevance ranking.
 */

import { Database } from "bun:sqlite";
import { join } from "path";
import { existsSync, mkdirSync } from "fs";
import type { Message, SearchResult } from "../types";
import { kindName } from "../types";

const DEFAULT_DB_PATH = ".claude/messages/search/index.db";

/**
 * Search Index using SQLite FTS5
 */
export class SearchIndex {
  private db: Database;

  constructor(dbPath = DEFAULT_DB_PATH) {
    // Ensure directory exists
    const dir = join(dbPath, "..");
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }

    this.db = new Database(dbPath);
    this.initialize();
  }

  /**
   * Initialize database schema
   */
  private initialize(): void {
    // FTS5 table for full-text search
    this.db.run(`
      CREATE VIRTUAL TABLE IF NOT EXISTS messages_fts USING fts5(
        id UNINDEXED,
        content,
        title,
        author_name,
        platform,
        tags,
        tokenize='porter unicode61'
      )
    `);

    // Metadata table for filtering
    this.db.run(`
      CREATE TABLE IF NOT EXISTS messages_meta (
        id TEXT PRIMARY KEY,
        kind INTEGER NOT NULL,
        account_id TEXT NOT NULL,
        thread_id TEXT,
        platform TEXT NOT NULL,
        created_at INTEGER NOT NULL,
        imported_at INTEGER NOT NULL,
        data TEXT NOT NULL
      )
    `);

    // Indexes for common filters
    this.db.run(`CREATE INDEX IF NOT EXISTS idx_kind ON messages_meta(kind)`);
    this.db.run(`CREATE INDEX IF NOT EXISTS idx_platform ON messages_meta(platform)`);
    this.db.run(`CREATE INDEX IF NOT EXISTS idx_account ON messages_meta(account_id)`);
    this.db.run(`CREATE INDEX IF NOT EXISTS idx_thread ON messages_meta(thread_id)`);
    this.db.run(`CREATE INDEX IF NOT EXISTS idx_created ON messages_meta(created_at)`);
  }

  /**
   * Index a message for search
   */
  index(message: Message): void {
    // Format tags for search
    const tagsText = message.tags?.map(([k, v]) => `${k}:${v}`).join(" ") || "";

    // Insert/update FTS
    this.db.run(
      `INSERT OR REPLACE INTO messages_fts (id, content, title, author_name, platform, tags)
       VALUES (?, ?, ?, ?, ?, ?)`,
      [
        message.id,
        message.content,
        message.title || "",
        message.author.name || "",
        message.source.platform,
        tagsText,
      ]
    );

    // Insert/update metadata
    this.db.run(
      `INSERT OR REPLACE INTO messages_meta
       (id, kind, account_id, thread_id, platform, created_at, imported_at, data)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
      [
        message.id,
        message.kind,
        message.account_id,
        message.refs.thread_id || null,
        message.source.platform,
        message.created_at,
        message.imported_at,
        JSON.stringify(message),
      ]
    );
  }

  /**
   * Index multiple messages in a batch
   */
  indexBatch(messages: Message[]): void {
    const insertFts = this.db.prepare(
      `INSERT OR REPLACE INTO messages_fts (id, content, title, author_name, platform, tags)
       VALUES (?, ?, ?, ?, ?, ?)`
    );

    const insertMeta = this.db.prepare(
      `INSERT OR REPLACE INTO messages_meta
       (id, kind, account_id, thread_id, platform, created_at, imported_at, data)
       VALUES (?, ?, ?, ?, ?, ?, ?, ?)`
    );

    const transaction = this.db.transaction(() => {
      for (const message of messages) {
        const tagsText = message.tags?.map(([k, v]) => `${k}:${v}`).join(" ") || "";

        insertFts.run(
          message.id,
          message.content,
          message.title || "",
          message.author.name || "",
          message.source.platform,
          tagsText
        );

        insertMeta.run(
          message.id,
          message.kind,
          message.account_id,
          message.refs.thread_id || null,
          message.source.platform,
          message.created_at,
          message.imported_at,
          JSON.stringify(message)
        );
      }
    });

    transaction();
  }

  /**
   * Search messages
   *
   * @param query Search query (supports FTS5 syntax)
   * @param options Search options
   */
  search(
    query: string,
    options: {
      limit?: number;
      offset?: number;
      kinds?: number[];
      platforms?: string[];
      accounts?: string[];
      threads?: string[];
      since?: number;
      until?: number;
    } = {}
  ): SearchResult[] {
    const limit = options.limit ?? 50;
    const offset = options.offset ?? 0;

    // Build WHERE clause for metadata filters
    const conditions: string[] = [];
    const params: (string | number | null)[] = [query];

    if (options.kinds?.length) {
      conditions.push(`m.kind IN (${options.kinds.map(() => "?").join(",")})`);
      params.push(...options.kinds);
    }

    if (options.platforms?.length) {
      conditions.push(`m.platform IN (${options.platforms.map(() => "?").join(",")})`);
      params.push(...options.platforms);
    }

    if (options.accounts?.length) {
      conditions.push(`m.account_id IN (${options.accounts.map(() => "?").join(",")})`);
      params.push(...options.accounts);
    }

    if (options.threads?.length) {
      conditions.push(`m.thread_id IN (${options.threads.map(() => "?").join(",")})`);
      params.push(...options.threads);
    }

    if (options.since !== undefined) {
      conditions.push("m.created_at >= ?");
      params.push(options.since);
    }

    if (options.until !== undefined) {
      conditions.push("m.created_at <= ?");
      params.push(options.until);
    }

    const whereClause = conditions.length > 0 ? `AND ${conditions.join(" AND ")}` : "";

    params.push(limit, offset);

    const sql = `
      SELECT
        m.data,
        bm25(messages_fts) as score
      FROM messages_fts f
      JOIN messages_meta m ON f.id = m.id
      WHERE messages_fts MATCH ?
      ${whereClause}
      ORDER BY bm25(messages_fts)
      LIMIT ? OFFSET ?
    `;

    const rows = this.db.query(sql).all(...params) as { data: string; score: number }[];

    return rows.map((row) => ({
      message: JSON.parse(row.data) as Message,
      score: -row.score, // BM25 returns negative scores, lower is better
    }));
  }

  /**
   * Search with highlighted snippets
   */
  searchWithHighlights(
    query: string,
    options: Parameters<SearchIndex["search"]>[1] = {}
  ): (SearchResult & { highlights: string[] })[] {
    const limit = options.limit ?? 50;
    const offset = options.offset ?? 0;

    const sql = `
      SELECT
        m.data,
        bm25(messages_fts) as score,
        snippet(messages_fts, 1, '**', '**', '...', 64) as content_snippet
      FROM messages_fts f
      JOIN messages_meta m ON f.id = m.id
      WHERE messages_fts MATCH ?
      ORDER BY bm25(messages_fts)
      LIMIT ? OFFSET ?
    `;

    const rows = this.db.query(sql).all(query, limit, offset) as {
      data: string;
      score: number;
      content_snippet: string;
    }[];

    return rows.map((row) => ({
      message: JSON.parse(row.data) as Message,
      score: -row.score,
      highlights: [row.content_snippet],
    }));
  }

  /**
   * Get recent messages
   */
  recent(limit = 50): Message[] {
    const rows = this.db
      .query(
        `SELECT data FROM messages_meta
         ORDER BY created_at DESC
         LIMIT ?`
      )
      .all(limit) as { data: string }[];

    return rows.map((row) => JSON.parse(row.data) as Message);
  }

  /**
   * Get messages by thread
   */
  getThreadMessages(threadId: string, limit = 100): Message[] {
    const rows = this.db
      .query(
        `SELECT data FROM messages_meta
         WHERE thread_id = ?
         ORDER BY created_at ASC
         LIMIT ?`
      )
      .all(threadId, limit) as { data: string }[];

    return rows.map((row) => JSON.parse(row.data) as Message);
  }

  /**
   * Get messages by account
   */
  getAccountMessages(accountId: string, limit = 100): Message[] {
    const rows = this.db
      .query(
        `SELECT data FROM messages_meta
         WHERE account_id = ?
         ORDER BY created_at DESC
         LIMIT ?`
      )
      .all(accountId, limit) as { data: string }[];

    return rows.map((row) => JSON.parse(row.data) as Message);
  }

  /**
   * Get message count
   */
  count(): number {
    const row = this.db.query("SELECT COUNT(*) as count FROM messages_meta").get() as {
      count: number;
    };
    return row.count;
  }

  /**
   * Get statistics
   */
  stats(): {
    total: number;
    byKind: Record<string, number>;
    byPlatform: Record<string, number>;
    dateRange: { first: number; last: number } | null;
  } {
    const total = this.count();

    // By kind
    const kindRows = this.db
      .query(
        `SELECT kind, COUNT(*) as count FROM messages_meta
         GROUP BY kind`
      )
      .all() as { kind: number; count: number }[];

    const byKind: Record<string, number> = {};
    for (const row of kindRows) {
      byKind[kindName(row.kind)] = row.count;
    }

    // By platform
    const platformRows = this.db
      .query(
        `SELECT platform, COUNT(*) as count FROM messages_meta
         GROUP BY platform`
      )
      .all() as { platform: string; count: number }[];

    const byPlatform: Record<string, number> = {};
    for (const row of platformRows) {
      byPlatform[row.platform] = row.count;
    }

    // Date range
    const rangeRow = this.db
      .query(
        `SELECT MIN(created_at) as first, MAX(created_at) as last
         FROM messages_meta`
      )
      .get() as { first: number | null; last: number | null };

    const dateRange =
      rangeRow.first !== null && rangeRow.last !== null
        ? { first: rangeRow.first, last: rangeRow.last }
        : null;

    return { total, byKind, byPlatform, dateRange };
  }

  /**
   * Delete a message from the index
   */
  delete(id: string): void {
    this.db.run("DELETE FROM messages_fts WHERE id = ?", [id]);
    this.db.run("DELETE FROM messages_meta WHERE id = ?", [id]);
  }

  /**
   * Clear all indexed data
   */
  clear(): void {
    this.db.run("DELETE FROM messages_fts");
    this.db.run("DELETE FROM messages_meta");
  }

  /**
   * Close the database connection
   */
  close(): void {
    this.db.close();
  }
}

/**
 * Create a search index instance
 */
export function createSearchIndex(dbPath?: string): SearchIndex {
  return new SearchIndex(dbPath);
}
