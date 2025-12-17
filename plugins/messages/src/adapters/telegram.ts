/**
 * Telegram Adapter
 *
 * Imports messages from Telegram JSON exports.
 * Telegram Desktop: Settings → Advanced → Export Telegram Data → JSON
 *
 * Export format: result.json contains an array of chats, each with messages.
 */

import type { MessageStore } from "../core/store";
import type { Message, MessageInput, Account, Thread } from "../types";
import { Kind } from "../types";

/**
 * Telegram export message format
 */
interface TelegramMessage {
  id: number;
  type: string;
  date: string;
  date_unixtime?: string;
  from: string;
  from_id: string;
  text: string | TelegramTextEntity[];
  reply_to_message_id?: number;
  forwarded_from?: string;
  media_type?: string;
  file?: string;
  photo?: string;
  sticker_emoji?: string;
}

/**
 * Telegram text entity (for formatted text)
 */
interface TelegramTextEntity {
  type: string;
  text: string;
  href?: string;
}

/**
 * Telegram chat export format
 */
interface TelegramChat {
  name: string;
  type: string;
  id: number;
  messages: TelegramMessage[];
}

/**
 * Telegram full export (result.json)
 */
interface TelegramExport {
  chats?: {
    list: TelegramChat[];
  };
  // Single chat export format
  name?: string;
  type?: string;
  id?: number;
  messages?: TelegramMessage[];
}

/**
 * Import statistics
 */
export interface ImportStats {
  messages: number;
  accounts: number;
  threads: number;
  skipped: number;
}

/**
 * Extract text content from Telegram message
 */
function extractText(text: string | TelegramTextEntity[]): string {
  if (typeof text === "string") {
    return text;
  }

  if (Array.isArray(text)) {
    return text
      .map((entity) => {
        if (typeof entity === "string") return entity;
        if (entity.type === "link" && entity.href) {
          return `[${entity.text}](${entity.href})`;
        }
        return entity.text;
      })
      .join("");
  }

  return "";
}

/**
 * Parse Telegram user ID
 */
function parseUserId(fromId: string): string {
  // fromId format: "user123456789" or "channel123456789"
  return fromId.replace(/^(user|channel)/, "");
}

/**
 * Import messages from a Telegram export file
 */
export async function* importTelegramExport(
  filePath: string,
  store: MessageStore
): AsyncGenerator<Message, ImportStats> {
  const file = Bun.file(filePath);
  const data: TelegramExport = await file.json();

  const stats: ImportStats = {
    messages: 0,
    accounts: 0,
    threads: 0,
    skipped: 0,
  };

  // Handle both full export and single chat export formats
  const chats: TelegramChat[] = [];

  if (data.chats?.list) {
    chats.push(...data.chats.list);
  } else if (data.messages && data.name) {
    // Single chat export
    chats.push({
      name: data.name,
      type: data.type || "personal_chat",
      id: data.id || 0,
      messages: data.messages,
    });
  }

  const seenAccounts = new Set<string>();

  for (const chat of chats) {
    // Create thread for this chat
    const threadId = `tg_${chat.id}`;
    const threadType =
      chat.type === "personal_chat"
        ? "dm"
        : chat.type === "private_group"
        ? "group"
        : "channel";

    await store.getOrCreateThread({
      id: threadId,
      title: chat.name,
      type: threadType,
      participants: [],
      source: {
        platform: "telegram",
        platform_id: String(chat.id),
      },
    });
    stats.threads++;

    // Process messages
    for (const msg of chat.messages) {
      // Skip non-message types
      if (msg.type !== "message") {
        stats.skipped++;
        continue;
      }

      // Extract content
      const content = extractText(msg.text);
      if (!content.trim()) {
        stats.skipped++;
        continue;
      }

      // Parse account
      const rawUserId = parseUserId(msg.from_id);
      const accountId = `tg_${rawUserId}`;

      // Create account if needed
      if (!seenAccounts.has(accountId)) {
        await store.getOrCreateAccount({
          id: accountId,
          name: msg.from,
          identities: [
            {
              platform: "telegram",
              handle: msg.from,
            },
          ],
        });
        seenAccounts.add(accountId);
        stats.accounts++;
      }

      // Parse timestamp
      const createdAt = msg.date_unixtime
        ? parseInt(msg.date_unixtime, 10) * 1000
        : new Date(msg.date).getTime();

      // Build message input
      const input: MessageInput = {
        kind: Kind.Telegram,
        content,
        account_id: accountId,
        author: {
          name: msg.from,
          handle: msg.from,
        },
        created_at: createdAt,
        refs: {
          thread_id: threadId,
          reply_to: msg.reply_to_message_id
            ? `tg_reply_${msg.reply_to_message_id}`
            : undefined,
        },
        source: {
          platform: "telegram",
          platform_id: String(msg.id),
        },
        tags: msg.forwarded_from
          ? [["forwarded_from", msg.forwarded_from]]
          : undefined,
      };

      // Create message
      const message = await store.createMessage(input);
      stats.messages++;

      yield message;
    }
  }

  return stats;
}

/**
 * Count messages in a Telegram export without importing
 */
export async function countTelegramExport(filePath: string): Promise<{
  chats: number;
  messages: number;
  participants: Set<string>;
}> {
  const file = Bun.file(filePath);
  const data: TelegramExport = await file.json();

  const participants = new Set<string>();
  let chatCount = 0;
  let messageCount = 0;

  const chats: TelegramChat[] = [];
  if (data.chats?.list) {
    chats.push(...data.chats.list);
  } else if (data.messages) {
    chats.push({
      name: data.name || "Unknown",
      type: data.type || "personal_chat",
      id: data.id || 0,
      messages: data.messages,
    });
  }

  for (const chat of chats) {
    chatCount++;
    for (const msg of chat.messages) {
      if (msg.type === "message" && extractText(msg.text).trim()) {
        messageCount++;
        participants.add(msg.from);
      }
    }
  }

  return { chats: chatCount, messages: messageCount, participants };
}
