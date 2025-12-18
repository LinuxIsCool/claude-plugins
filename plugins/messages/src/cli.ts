#!/usr/bin/env bun
/**
 * Messages CLI
 *
 * Command-line interface for the Messages plugin.
 *
 * Usage:
 *   bun plugins/messages/src/cli.ts <command> [options]
 *
 * Commands:
 *   import telegram -f <file>   Import Telegram export
 *   import logs                 Import Claude Code logs
 *   search <query>              Search messages
 *   recent                      Show recent messages
 *   thread <id>                 Show thread messages
 *   threads                     List threads
 *   accounts                    List accounts
 *   stats                       Show statistics
 */

import { parseArgs } from "util";
import { createStore } from "./core/store";
import { createSearchIndex } from "./search";
import { importTelegramExport, countTelegramExport } from "./adapters/telegram";
import { importLogging, countLoggingEvents, getDefaultLogsDir } from "./adapters/logging";
import {
  importClaudeWeb,
  countClaudeWebExport,
  extractConversationsFromZip,
} from "./adapters/claude-web";
import {
  importTelegramApi,
  countTelegramApi,
  isTelegramApiAvailable,
} from "./adapters/telegram-api";
import {
  importEmail,
  countEmail,
  getUserEmail,
} from "./adapters/email";
import {
  TelegramApiClient,
  hasSession,
} from "./integrations/telegram/client";
import { kindName } from "./types";

// Parse command line arguments
const { positionals, values } = parseArgs({
  args: Bun.argv.slice(2),
  options: {
    file: { type: "string", short: "f" },
    limit: { type: "string", short: "l" },
    platform: { type: "string", short: "p" },
    since: { type: "string", short: "s" },
    "dry-run": { type: "boolean" },
    "include-tools": { type: "boolean" },
    "include-system": { type: "boolean" },
    "include-thinking": { type: "boolean" },
    help: { type: "boolean", short: "h" },
  },
  allowPositionals: true,
});

const [command, ...args] = positionals;

// Initialize store and search
const store = createStore();
const search = createSearchIndex();

// Help text
function showHelp(): void {
  console.log(`
Messages CLI - Universal messaging backbone

Usage:
  bun plugins/messages/src/cli.ts <command> [options]

Commands:
  telegram-auth               Authenticate with Telegram (one-time setup)
  import telegram -f <file>   Import Telegram JSON export
  import telegram-api         Import from Telegram API (requires auth)
  import logs                 Import Claude Code logs
  import claude-web -f <zip>  Import Claude Web data export
  import email -f <path>      Import emails (.eml directory or .mbox file)
  search <query>              Search messages
  recent [-l N]               Show recent messages
  thread <id>                 Show thread messages
  threads                     List all threads
  accounts                    List all accounts
  stats                       Show statistics

Options:
  -f, --file <path>           File path for import
  -l, --limit <n>             Limit results (default: 20)
  -p, --platform <name>       Filter by platform
  -s, --since <days|date>     Filter to messages since N days ago or date
  --dry-run                   Preview import without saving
  --include-tools             Include tool use events (logs/claude-web)
  --include-system            Include system events (logs import)
  --include-thinking          Include thinking blocks (claude-web, default: true)
  -h, --help                  Show this help

Examples:
  # Authenticate with Telegram (one-time)
  bun plugins/messages/src/cli.ts telegram-auth

  # Import from Telegram API (last 30 days)
  bun plugins/messages/src/cli.ts import telegram-api

  # Import Telegram JSON export
  bun plugins/messages/src/cli.ts import telegram -f ~/Downloads/result.json

  # Import Claude Code logs
  bun plugins/messages/src/cli.ts import logs

  # Import Claude Web data (last 30 days)
  bun plugins/messages/src/cli.ts import claude-web -f ~/Downloads/data-*.zip -s 30

  # Import emails from .eml directory
  bun plugins/messages/src/cli.ts import email -f ~/Mail/Archive/

  # Import emails from .mbox file
  bun plugins/messages/src/cli.ts import email -f ~/Downloads/gmail-export.mbox

  # Search messages
  bun plugins/messages/src/cli.ts search "authentication"

  # Show recent Claude Code prompts
  bun plugins/messages/src/cli.ts recent -p claude-code -l 10
`);
}

// Format date for display
function formatDate(ts: number): string {
  return new Date(ts).toISOString().replace("T", " ").slice(0, 19);
}

// Truncate text
function truncate(text: string, max: number): string {
  const clean = text.replace(/\n/g, " ").trim();
  return clean.length > max ? clean.slice(0, max) + "..." : clean;
}

// Main command handler
async function main(): Promise<void> {
  if (values.help || !command) {
    showHelp();
    return;
  }

  const limit = values.limit ? parseInt(values.limit, 10) : 20;

  switch (command) {
    case "telegram-auth": {
      console.log("Telegram Authentication");
      console.log("=======================\n");

      // Check for credentials
      if (!process.env.TELEGRAM_API_ID || !process.env.TELEGRAM_API_HASH || !process.env.TELEGRAM_PHONE) {
        console.error("Error: Missing Telegram credentials in .env");
        console.error("Required: TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE");
        process.exit(1);
      }

      if (hasSession()) {
        console.log("You already have a saved session.");
        console.log("To re-authenticate, delete .claude/messages/telegram-session.txt first.");
        return;
      }

      console.log(`Phone: ${process.env.TELEGRAM_PHONE}`);
      console.log("\nConnecting to Telegram...");
      console.log("A verification code will be sent to your Telegram app.\n");

      const client = new TelegramApiClient();

      // Dynamic import for input module
      const input = await import("input");

      try {
        await client.authenticate({
          onCodeRequest: async () => {
            return await input.text("Enter the code from Telegram: ");
          },
          onPasswordRequest: async () => {
            return await input.text("Enter your 2FA password (if enabled): ");
          },
          onError: (err) => {
            console.error("Authentication error:", err.message);
          },
        });

        console.log("\n✓ Successfully authenticated!");
        console.log("Session saved. You can now run: import telegram-api");
      } catch (error) {
        console.error("\nAuthentication failed:", error);
        process.exit(1);
      }
      break;
    }

    case "import": {
      const [source] = args;

      if (source === "telegram") {
        if (!values.file) {
          console.error("Error: --file/-f required for Telegram import");
          process.exit(1);
        }

        if (values["dry-run"]) {
          console.log("Counting Telegram export...");
          const counts = await countTelegramExport(values.file);
          console.log(`
Telegram Export Summary:
  Chats: ${counts.chats}
  Messages: ${counts.messages}
  Participants: ${counts.participants.size}

Participants: ${Array.from(counts.participants).join(", ")}
`);
          return;
        }

        console.log(`Importing from ${values.file}...`);
        let imported = 0;
        const generator = importTelegramExport(values.file, store);

        for await (const message of generator) {
          search.index(message);
          imported++;
          if (imported % 100 === 0) {
            process.stdout.write(`\rImported ${imported} messages...`);
          }
        }

        console.log(`\nDone! Imported ${imported} messages.`);

      } else if (source === "logs") {
        const logsDir = getDefaultLogsDir();

        if (values["dry-run"]) {
          console.log("Counting Claude Code logs...");
          const counts = await countLoggingEvents(logsDir);
          console.log(`
Claude Code Logs Summary:
  Files: ${counts.files}
  Events: ${counts.events}
  Sessions: ${counts.sessions.size}
  Date Range: ${counts.dateRange?.first} to ${counts.dateRange?.last}

Event Types:`);
          for (const [type, count] of counts.eventTypes) {
            console.log(`  ${type}: ${count}`);
          }
          return;
        }

        console.log(`Importing from ${logsDir}...`);
        let imported = 0;
        const generator = importLogging(logsDir, store, {
          includeToolUse: values["include-tools"],
          includeSystemEvents: values["include-system"],
        });

        for await (const message of generator) {
          search.index(message);
          imported++;
          if (imported % 100 === 0) {
            process.stdout.write(`\rImported ${imported} messages...`);
          }
        }

        console.log(`\nDone! Imported ${imported} messages.`);

      } else if (source === "claude-web") {
        if (!values.file) {
          console.error("Error: --file/-f required for Claude Web import");
          console.error("Provide the path to the data-*.zip file downloaded from claude.ai");
          process.exit(1);
        }

        // Parse since option (days or date)
        let sinceDate: Date | undefined;
        if (values.since) {
          const daysAgo = parseInt(values.since, 10);
          if (!isNaN(daysAgo)) {
            // Treat as number of days ago
            sinceDate = new Date(Date.now() - daysAgo * 24 * 60 * 60 * 1000);
          } else {
            // Try to parse as date
            sinceDate = new Date(values.since);
            if (isNaN(sinceDate.getTime())) {
              console.error(`Error: Invalid date or days value: ${values.since}`);
              process.exit(1);
            }
          }
        }

        // Extract conversations.json from ZIP
        console.log("Extracting conversations.json from ZIP...");
        let conversationsPath: string;
        try {
          conversationsPath = await extractConversationsFromZip(values.file);
        } catch (error) {
          console.error("Error extracting ZIP:", error);
          process.exit(1);
        }

        const importOptions = {
          since: sinceDate,
          includeThinking: values["include-thinking"] !== false, // default true
          includeTools: values["include-tools"] || false,
        };

        if (values["dry-run"]) {
          console.log("Counting Claude Web messages...");
          const counts = await countClaudeWebExport(conversationsPath, importOptions);
          console.log(`
Claude Web Export Summary:
  Conversations: ${counts.conversations}
  Total Messages: ${counts.messages}
    Human: ${counts.humanMessages}
    Assistant: ${counts.assistantMessages}
  Date Range: ${counts.dateRange.earliest?.toISOString().slice(0, 10) || "N/A"} to ${counts.dateRange.latest?.toISOString().slice(0, 10) || "N/A"}
${sinceDate ? `\n  (Filtered to messages since ${sinceDate.toISOString().slice(0, 10)})` : ""}
`);
          return;
        }

        console.log(`Importing from Claude Web export...`);
        if (sinceDate) {
          console.log(`  Filtering to messages since ${sinceDate.toISOString().slice(0, 10)}`);
        }

        let imported = 0;
        const generator = importClaudeWeb(conversationsPath, store, importOptions);

        for await (const message of generator) {
          search.index(message);
          imported++;
          if (imported % 100 === 0) {
            process.stdout.write(`\rImported ${imported} messages...`);
          }
        }

        console.log(`\nDone! Imported ${imported} messages.`);

      } else if (source === "telegram-api") {
        // Check for session
        if (!isTelegramApiAvailable()) {
          console.error("Error: No Telegram session found.");
          console.error("Run 'telegram-auth' first to authenticate.");
          process.exit(1);
        }

        // Parse since option (days)
        const daysBack = values.since ? parseInt(values.since, 10) : 30;
        if (isNaN(daysBack)) {
          console.error(`Error: Invalid days value: ${values.since}`);
          process.exit(1);
        }

        if (values["dry-run"]) {
          console.log("Counting Telegram chats...");
          try {
            const counts = await countTelegramApi({ daysBack });
            console.log(`
Telegram API Summary:
  Chats available: ${counts.dialogs}
  Estimated messages: ${counts.estimatedMessages}

Chats:`);
            for (const d of counts.dialogList.slice(0, 20)) {
              console.log(`  [${d.type}] ${d.title}`);
            }
            if (counts.dialogList.length > 20) {
              console.log(`  ... and ${counts.dialogList.length - 20} more`);
            }
          } catch (error) {
            console.error("Error:", error);
            process.exit(1);
          }
          return;
        }

        console.log(`Importing from Telegram API (last ${daysBack} days)...`);

        let imported = 0;
        try {
          const generator = importTelegramApi(store, { daysBack });

          for await (const message of generator) {
            search.index(message);
            imported++;
            if (imported % 50 === 0) {
              process.stdout.write(`\rImported ${imported} messages...`);
            }
          }

          console.log(`\nDone! Imported ${imported} messages.`);
        } catch (error) {
          console.error("\nError during import:", error);
          process.exit(1);
        }

      } else if (source === "email") {
        if (!values.file) {
          console.error("Error: --file/-f required for email import");
          console.error("Provide the path to .eml directory or .mbox file");
          process.exit(1);
        }

        const userEmail = getUserEmail();
        if (!userEmail) {
          console.error("Error: EMAIL_ADDRESS environment variable required");
          console.error("Set your email address in .env: EMAIL_ADDRESS=you@example.com");
          process.exit(1);
        }

        // Parse since option (days or date)
        let sinceDate: Date | undefined;
        if (values.since) {
          const daysAgo = parseInt(values.since, 10);
          if (!isNaN(daysAgo)) {
            sinceDate = new Date(Date.now() - daysAgo * 24 * 60 * 60 * 1000);
          } else {
            sinceDate = new Date(values.since);
            if (isNaN(sinceDate.getTime())) {
              console.error(`Error: Invalid date or days value: ${values.since}`);
              process.exit(1);
            }
          }
        }

        if (values["dry-run"]) {
          console.log("Counting emails...");
          try {
            const counts = await countEmail({
              source: values.file,
              userEmail,
              since: sinceDate,
            });
            console.log(`
Email Import Summary:
  Messages: ${counts.messages}
  Threads: ${counts.threads}
  Accounts: ${counts.accounts.size}
  Attachments: ${counts.attachments}
  Date Range: ${counts.dateRange.earliest?.toISOString().slice(0, 10) || "N/A"} to ${counts.dateRange.latest?.toISOString().slice(0, 10) || "N/A"}
${sinceDate ? `\n  (Filtered to messages since ${sinceDate.toISOString().slice(0, 10)})` : ""}
`);
          } catch (error) {
            console.error("Error:", error);
            process.exit(1);
          }
          return;
        }

        console.log(`Importing emails from ${values.file}...`);
        console.log(`  User email: ${userEmail}`);
        if (sinceDate) {
          console.log(`  Filtering to messages since ${sinceDate.toISOString().slice(0, 10)}`);
        }

        let imported = 0;
        try {
          const generator = importEmail(store, {
            source: values.file,
            userEmail,
            since: sinceDate,
            includeAttachments: true,
          });

          for await (const message of generator) {
            search.index(message);
            imported++;
            if (imported % 100 === 0) {
              process.stdout.write(`\rImported ${imported} messages...`);
            }
          }

          console.log(`\nDone! Imported ${imported} messages.`);
        } catch (error) {
          console.error("\nError during import:", error);
          process.exit(1);
        }

      } else {
        console.error(`Unknown import source: ${source}`);
        console.error("Available: telegram, telegram-api, logs, claude-web, email");
        process.exit(1);
      }
      break;
    }

    case "search": {
      const query = args.join(" ");
      if (!query) {
        console.error("Error: search query required");
        process.exit(1);
      }

      console.log(`Searching for: "${query}"\n`);
      const results = search.search(query, {
        limit,
        platforms: values.platform ? [values.platform] : undefined,
      });

      if (results.length === 0) {
        console.log("No results found.");
        return;
      }

      for (const result of results) {
        const msg = result.message;
        const date = formatDate(msg.created_at);
        const kind = kindName(msg.kind as number);
        const content = truncate(msg.content, 100);

        console.log(`[${date}] ${msg.source.platform} | ${kind}`);
        console.log(`  ${msg.author.name}: ${content}`);
        console.log(`  Score: ${result.score.toFixed(2)} | ID: ${msg.id}`);
        console.log();
      }

      console.log(`Found ${results.length} results.`);
      break;
    }

    case "recent": {
      console.log("Recent messages:\n");
      const messages = search.recent(limit);

      if (messages.length === 0) {
        console.log("No messages found. Try importing some first.");
        return;
      }

      for (const msg of messages) {
        const date = formatDate(msg.created_at);
        const content = truncate(msg.content, 100);

        console.log(`[${date}] ${msg.source.platform}`);
        console.log(`  ${msg.author.name}: ${content}`);
        console.log();
      }
      break;
    }

    case "thread": {
      const [threadId] = args;
      if (!threadId) {
        console.error("Error: thread ID required");
        process.exit(1);
      }

      console.log(`Thread: ${threadId}\n`);
      const messages = search.getThreadMessages(threadId, limit);

      if (messages.length === 0) {
        console.log("No messages found in this thread.");
        return;
      }

      for (const msg of messages) {
        const date = formatDate(msg.created_at);
        const content = truncate(msg.content, 200);

        console.log(`[${date}] ${msg.author.name}:`);
        console.log(`  ${content}`);
        console.log();
      }

      console.log(`Showing ${messages.length} messages.`);
      break;
    }

    case "threads": {
      console.log("Threads:\n");
      let count = 0;

      for await (const thread of store.listThreads(limit)) {
        count++;
        console.log(`${thread.id}`);
        console.log(`  Title: ${thread.title || "(untitled)"}`);
        console.log(`  Type: ${thread.type} | Platform: ${thread.source.platform}`);
        console.log(`  Messages: ${thread.message_count}`);
        console.log();
      }

      if (count === 0) {
        console.log("No threads found. Try importing some messages first.");
      }
      break;
    }

    case "accounts": {
      console.log("Accounts:\n");
      let count = 0;

      for await (const account of store.listAccounts(limit)) {
        count++;

        const platforms = account.identities.map((i) => i.platform).join(", ");
        console.log(`${account.id}: ${account.name}`);
        console.log(`  Platforms: ${platforms}`);
        if (account.did) {
          console.log(`  DID: ${account.did}`);
        }
        console.log();
      }

      if (count === 0) {
        console.log("No accounts found. Try importing some messages first.");
      }
      break;
    }

    case "stats": {
      const stats = search.stats();

      console.log(`
Messages Statistics
==================
Total Messages: ${stats.total}

By Kind:`);
      for (const [kind, count] of Object.entries(stats.byKind)) {
        console.log(`  ${kind}: ${count}`);
      }

      console.log(`
By Platform:`);
      for (const [platform, count] of Object.entries(stats.byPlatform)) {
        console.log(`  ${platform}: ${count}`);
      }

      if (stats.dateRange) {
        console.log(`
Date Range:
  First: ${formatDate(stats.dateRange.first)}
  Last: ${formatDate(stats.dateRange.last)}
`);
      }
      break;
    }

    default:
      console.error(`Unknown command: ${command}`);
      showHelp();
      process.exit(1);
  }
}

// Run
main().catch((error) => {
  console.error("Error:", error);
  process.exit(1);
});
