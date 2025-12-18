---
id: 2025-12-17-1434
title: "Claude Web Adapter: Cross-Platform Messaging Complete"
type: atomic
created: 2025-12-17T14:34:37
author: claude-opus-4
description: "Implemented Claude Web adapter for Messages plugin, enabling import of claude.ai conversation exports with date filtering"
tags: [messages, adapter, claude-web, cross-platform, implementation]
parent_daily: [[2025-12-17]]
related:
  - [[2025-12-17-1351]]
  - [[2025-12-16]]
---

# Claude Web Adapter: Cross-Platform Messaging Complete

Today we implemented a Claude Web adapter for the Messages plugin, enabling import of conversation exports from claude.ai.

## What We Built

### New Adapter: `src/adapters/claude-web.ts`

A complete adapter following the established pattern:

| Component | Purpose |
|-----------|---------|
| **ContentBlock types** | Text, thinking, tool_use, tool_result parsing |
| **extractTextFromContentBlocks()** | Recursive content extraction with thinking support |
| **importClaudeWeb()** | Async generator for streaming imports |
| **countClaudeWebExport()** | Dry-run preview function |
| **extractConversationsFromZip()** | ZIP handling via Bun shell |

### CLI Integration

Added `import claude-web` command with options:
- `-f, --file <zip>` - Path to downloaded ZIP from claude.ai
- `-s, --since <days|date>` - Filter by date (e.g., "30" for last 30 days)
- `--include-thinking` - Include [THINKING] blocks (default: true)
- `--include-tools` - Include tool_use/tool_result blocks

### New Kind

Added `ClaudeWeb: 1040` to the extensible Kind system in the 1000+ platform-specific range.

## Data Mapping

| Claude Web | Messages Plugin |
|------------|-----------------|
| conversation.uuid | Thread ID (`cw_` + first 8 chars) |
| conversation.name | Thread title |
| chat_message.sender | Account (`cw_user` or `cw_claude`) |
| chat_message.content | Extracted text (with thinking blocks) |
| chat_message.uuid | source.platform_id |

## Import Results

```
Claude Web Export Summary:
  Conversations: 55
  Total Messages: 329
    Human: 156
    Assistant: 173
  Date Range: 2025-11-18 to 2025-12-17

Messages Statistics (After Import):
  Total Messages: 2755
  By Kind:
    UserPrompt: 768
    AssistantResponse: 460
    SubagentStop: 1198
    ClaudeWeb: 329
  By Platform:
    claude-code: 2426
    claude-web: 329
```

## Technical Decisions

### ZIP Extraction Strategy

Used Bun's shell template for safe ZIP handling:
```typescript
await $`unzip -o ${zipPath} conversations.json -d ${tempDir}`;
```

Extracts only conversations.json (skipping 22MB projects.json) to temp directory.

### Content Block Handling

Based on reference code from `/home/ygg/Workspace/sandbox/personal-digital/claude_web/models.py`:

```typescript
if (blockType === "text") textParts.push(block.text);
else if (blockType === "thinking") textParts.push(`[THINKING] ${block.thinking}`);
else if (blockType === "tool_use") // Include tool name + input JSON
else if (blockType === "tool_result") // Recursive extraction
```

### No Data Truncation

Per CLAUDE.md requirements, all content preserved in full. Tool inputs use `JSON.stringify(input, null, 2)` without limits.

### Account Model Consistency

Followed logging adapter pattern:
- `cw_user` for human messages
- `cw_claude` for assistant messages

This enables cross-platform identity queries (e.g., "show all my questions across claude-web and claude-code").

## Cross-Platform Search Now Works

```bash
# Search across all platforms
bun plugins/messages/src/cli.ts search "authentication"

# Results from both claude-code AND claude-web
[2025-12-12 23:10:18] claude-code | AssistantResponse
[2025-11-25 21:07:00] claude-web | ClaudeWeb
```

## Quality Review

Code review found no high-confidence issues:
- Type safety with proper optional chaining
- Edge case handling (empty content, missing fields)
- Memory efficient (async generator streaming)
- CLAUDE.md compliant (no truncation)
- Pattern consistent with telegram.ts and logging.ts

## Usage

```bash
# Dry-run (preview what would be imported)
bun plugins/messages/src/cli.ts import claude-web -f ~/Downloads/data-*.zip -s 30 --dry-run

# Import last 30 days of conversations
bun plugins/messages/src/cli.ts import claude-web -f ~/Downloads/data-*.zip -s 30

# Import all conversations
bun plugins/messages/src/cli.ts import claude-web -f ~/Downloads/data-*.zip
```

## Insight

> The Messages plugin now bridges three communication contexts: Claude Code sessions (technical work), Claude Web conversations (general inquiries), and Telegram chats (personal communication). The unified search makes it possible to find connections across these previously siloed contexts.

---

*Parent: [[2025-12-17]]*
