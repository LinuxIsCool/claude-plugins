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
import { kindName } from "./types";

// Parse command line arguments
const { positionals, values } = parseArgs({
  args: Bun.argv.slice(2),
  options: {
    file: { type: "string", short: "f" },
    limit: { type: "string", short: "l" },
    platform: { type: "string", short: "p" },
    "dry-run": { type: "boolean" },
    "include-tools": { type: "boolean" },
    "include-system": { type: "boolean" },
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
  import telegram -f <file>   Import Telegram JSON export
  import logs                 Import Claude Code logs
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
  --dry-run                   Preview import without saving
  --include-tools             Include tool use events (logs import)
  --include-system            Include system events (logs import)
  -h, --help                  Show this help

Examples:
  # Import Telegram export
  bun plugins/messages/src/cli.ts import telegram -f ~/Downloads/result.json

  # Import Claude Code logs
  bun plugins/messages/src/cli.ts import logs

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

      } else {
        console.error(`Unknown import source: ${source}`);
        console.error("Available: telegram, logs");
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
