---
id: msg_DAC7QDDz3KwQDAAmDJT7QQuvnbV2MFYB
kind: 103
account_id: claude
created_at: 1765918715870
imported_at: 1766005511780
author_name: Claude
thread_id: cc_56d52765
platform: claude-code
session_id: 56d52765-83a5-4ce6-84e2-938e81ceffbf
tags: [["event_type","AssistantResponse"]]
---

**No native mechanism for arbitrary folder distribution**, but there are practical workarounds.

## What Plugins Can Distribute

Only these are "recognized" by Claude Code:
- `commands/`, `agents/`, `skills/`, `hooks/`, `.mcp.json`

Any other files are included in the plugin but not auto-integrated.

## Workarounds

### 1. SessionStart Hook as Installer
The most practical approach - use a hook script to copy files on session start:

```json
// plugin.json
{
  "hooks": {
    "SessionStart": [{
      "type": "command",
      "command": "${CLAUDE_PLUGIN_ROOT}/hooks/install.sh"
    }]
  }
}
```

```bash
# hooks/install.sh
#!/bin/bash
PLUGIN_ROOT="$(dirname "$0")/.."
TARGET="$HOME/.claude/output-styles"

mkdir -p "$TARGET"
cp -n "$PLUGIN_ROOT/resources/output-styles/"*.md "$TARGET/" 2>/dev/null
```

### 2. Bundle with Skills/Agents
Include files alongside skills and reference them via `${CLAUDE_PLUGIN_ROOT}`:
```
plugin/
├── skills/my-skill/
│   ├── SKILL.md
│   └── resources/      # Referenced by skill instructions
└── resources/
    └── output-styles/  # Copied by hook
```

### 3. MCP Server Bundling
MCP servers can include any supporting files they need.

## For Output Styles Specifically

You could create a plugin that:
1. Bundles output style `.md` files in a `resources/` folder
2. Uses a SessionStart hook to symlink or copy them to `~/.claude/output-styles/`
3. Optionally includes a slash command like `/install-styles` for manual installation

This is a reasonable workaround until (if ever) plugins get native support for output style distribution.
