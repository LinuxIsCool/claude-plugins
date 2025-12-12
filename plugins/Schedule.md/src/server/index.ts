/**
 * Schedule.md HTTP Server
 *
 * Serves the web interface and provides REST API + WebSocket for real-time sync
 */

import { watch } from "node:fs";
import { readFile } from "node:fs/promises";
import { join, dirname } from "node:path";
import { Schedule } from "../core/schedule";
import type { CreateBlockInput, EditBlockInput, BlockFilter, DayOfWeek } from "../types";

// Get the web directory (relative to this file)
const WEB_DIR = join(dirname(import.meta.dir), "web");

interface ServerOptions {
  port: number;
  scheduleDir: string;
}

export async function startServer(options: ServerOptions) {
  const { port, scheduleDir } = options;

  // Initialize schedule
  const schedule = new Schedule(scheduleDir);
  await schedule.init();

  // Track connected WebSocket clients
  const wsClients = new Set<WebSocket>();

  // Broadcast to all connected clients
  function broadcast(event: { type: string; data?: unknown }) {
    const message = JSON.stringify(event);
    for (const client of wsClients) {
      if (client.readyState === WebSocket.OPEN) {
        client.send(message);
      }
    }
  }

  // Watch for file changes and broadcast updates
  const blocksDir = join(scheduleDir, "blocks");
  try {
    watch(blocksDir, { recursive: true }, async (eventType, filename) => {
      if (filename?.endsWith(".md")) {
        await schedule.reload();
        broadcast({ type: "blocks-updated" });
      }
    });
  } catch {
    // Directory might not exist yet
  }

  // Watch config changes
  const configPath = join(scheduleDir, "config.json");
  try {
    watch(configPath, async () => {
      await schedule.reload();
      broadcast({ type: "config-updated" });
    });
  } catch {
    // Config might not exist yet
  }

  // Build the web bundle
  const webBundle = await Bun.build({
    entrypoints: [join(WEB_DIR, "index.tsx")],
    outdir: join(WEB_DIR, "dist"),
    minify: false,
    sourcemap: "inline",
    external: [],
  });

  if (!webBundle.success) {
    console.error("Failed to build web bundle:", webBundle.logs);
    throw new Error("Web build failed");
  }

  // Create Bun server
  const server = Bun.serve({
    port,
    async fetch(req, server) {
      const url = new URL(req.url);
      const path = url.pathname;

      // Handle WebSocket upgrade
      if (path === "/ws") {
        const upgraded = server.upgrade(req);
        if (upgraded) return undefined;
        return new Response("WebSocket upgrade failed", { status: 400 });
      }

      // API routes
      if (path.startsWith("/api/")) {
        return handleApiRequest(req, schedule, path.slice(5));
      }

      // Serve static files
      return handleStaticRequest(path);
    },
    websocket: {
      open(ws) {
        wsClients.add(ws as unknown as WebSocket);
        (ws as unknown as WebSocket).send(JSON.stringify({ type: "connected" }));
      },
      close(ws) {
        wsClients.delete(ws as unknown as WebSocket);
      },
      message() {
        // Currently no client-to-server messages needed
      },
    },
  });

  console.log(`Schedule.md server running at http://localhost:${port}`);

  return server;
}

/**
 * Handle API requests
 */
async function handleApiRequest(
  req: Request,
  schedule: Schedule,
  path: string
): Promise<Response> {
  const method = req.method;

  try {
    // GET /api/config
    if (path === "config" && method === "GET") {
      const config = schedule.getConfig();
      return json(config);
    }

    // PATCH /api/config
    if (path === "config" && method === "PATCH") {
      const updates = await req.json();
      const config = await schedule.updateConfig(updates);
      return json(config);
    }

    // GET /api/blocks
    if (path === "blocks" && method === "GET") {
      const url = new URL(req.url);
      const filter: BlockFilter = {};
      if (url.searchParams.has("day")) {
        filter.day = url.searchParams.get("day") as DayOfWeek;
      }
      if (url.searchParams.has("category")) {
        filter.category = url.searchParams.get("category")!;
      }
      if (url.searchParams.has("source")) {
        filter.source = url.searchParams.get("source") as "manual" | "google-calendar" | "yoga-studio";
      }
      const blocks = await schedule.listBlocks(filter);
      return json(blocks);
    }

    // POST /api/blocks
    if (path === "blocks" && method === "POST") {
      const input = (await req.json()) as CreateBlockInput;
      const block = await schedule.createBlock(input);
      return json(block, 201);
    }

    // GET /api/blocks/:id
    const blockMatch = path.match(/^blocks\/([^/]+)$/);
    if (blockMatch && method === "GET") {
      const id = decodeURIComponent(blockMatch[1]);
      const block = await schedule.getBlock(id);
      if (!block) {
        return json({ error: "Block not found" }, 404);
      }
      return json(block);
    }

    // PATCH /api/blocks/:id
    if (blockMatch && method === "PATCH") {
      const id = decodeURIComponent(blockMatch[1]);
      const updates = (await req.json()) as EditBlockInput;
      const block = await schedule.editBlock(id, updates);
      if (!block) {
        return json({ error: "Block not found" }, 404);
      }
      return json(block);
    }

    // DELETE /api/blocks/:id
    if (blockMatch && method === "DELETE") {
      const id = decodeURIComponent(blockMatch[1]);
      const success = await schedule.deleteBlock(id);
      if (!success) {
        return json({ error: "Block not found" }, 404);
      }
      return json({ success: true });
    }

    // GET /api/summary
    if (path === "summary" && method === "GET") {
      const summary = await schedule.getSummary();
      return json(summary);
    }

    // Not found
    return json({ error: "Not found" }, 404);
  } catch (error) {
    console.error("API error:", error);
    return json(
      { error: error instanceof Error ? error.message : "Internal error" },
      500
    );
  }
}

/**
 * Handle static file requests
 */
async function handleStaticRequest(path: string): Promise<Response> {
  // Default to index.html
  if (path === "/" || path === "/index.html") {
    const html = await readFile(join(WEB_DIR, "index.html"), "utf-8");
    return new Response(html, {
      headers: { "Content-Type": "text/html" },
    });
  }

  // Serve bundled JS
  if (path === "/index.js") {
    try {
      const js = await readFile(join(WEB_DIR, "dist", "index.js"), "utf-8");
      return new Response(js, {
        headers: { "Content-Type": "application/javascript" },
      });
    } catch {
      return new Response("Not found", { status: 404 });
    }
  }

  // Other static files
  try {
    const file = Bun.file(join(WEB_DIR, path));
    return new Response(file);
  } catch {
    return new Response("Not found", { status: 404 });
  }
}

/**
 * JSON response helper
 */
function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}
