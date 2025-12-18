---
created: 2025-12-18T12:36:00-08:00
author: claude
type: research-session
description: Deep research into Claude Code plugin caching, update mechanics, and seamless development workflow
parent_daily: [[2025-12-18]]
tags: [research, plugins, caching, dev-tools, development-experience, hot-reload]
related:
  - "[[2025-12-08-17-48-hot-reload-research]]"
  - "[[plugin-update-mechanics-report]]"
---

# Plugin Update Mechanics: Deep Dive

## Context

User asked for deep research on how Claude Code processes plugin updates, why cache clearing and restarts are required, and whether we could make plugin development more seamless. Also requested a catalogue of all symlinks in the development process.

## Key Discoveries

### The Copy-on-Install Architecture

Claude Code uses **copy-on-install**, not live file references:
- When a plugin is installed, files are copied to `~/.claude/plugins/cache/{marketplace}/{plugin}/{version}/`
- Source file edits are invisible to running sessions
- A `current` symlink points to the active version directory
- No hot-reload mechanism exists for plugins (only for MCP servers)

### Why Restart Is Required

1. **Startup-only loading** - Skills, commands, hooks, agents parsed once at session start
2. **In-memory caching** - After loading, plugin data lives in process memory
3. **No refresh API** - Claude Code has no mechanism to reload plugins mid-session
4. **Known bug** (#14061) - Even `/plugin update` doesn't invalidate cache properly

### Cache Staleness Evidence

Found concrete proof of drift:
- Source file modified: Dec 15 09:56
- Cache file modified: Dec 13 16:59
- **Cache was 2 days stale**

### Symlink Catalogue

Documented 6 meaningful symlinks in the repository:
1. Resource deduplication (SDK packages share `src/internal`)
2. Naming aliases (AGENTS.md → CLAUDE.md)
3. Version pointers (cache `current` → version directory)

All use relative paths for portability.

## What We Created

### 1. Research Report

Comprehensive analysis saved to:
`.claude/research/2025-12-18-plugin-update-mechanics-report.md`

Covers:
- Plugin loading pipeline
- Cache architecture
- Options for seamless updates
- Recommendations

### 2. dev-tools Plugin Registration

The `dev-tools` plugin existed but was **never registered** in the marketplace. Fixed by adding:
```json
{"name": "dev-tools", "source": "./plugins/dev-tools/"}
```

### 3. Improved Stale Cache Warning

Updated `stale_cache_detector.py` to include actionable command:
```
Stale plugin cache detected: awareness. Run: /dev-tools:reload awareness then restart Claude Code.
```

### 4. Headless Refresh Mechanism

Created `/dev-tools:refresh` command and `tools/refresh-plugins.sh`:
- Clears cache
- Spawns headless Claude (`claude -p "exit" --setting-sources ""`)
- Triggers cache rebuild
- Other running instances see fresh cache

Key insight: All Claude instances share the cache directory, so rebuilding it updates everyone.

## The Friction That Remains

**Restart is still required** - this is architectural. But we eliminated:
- Forgetting to clear cache (auto-clear hook)
- Not knowing cache is stale (SessionStart detection)
- Manual cache clearing steps (slash commands)

## Tools Summary

| Tool | Purpose |
|------|---------|
| `hooks/cache_invalidator.py` | Auto-clears cache on plugin file edit |
| `hooks/stale_cache_detector.py` | Warns on session start if stale |
| `/dev-tools:reload <plugin>` | Manual cache clear |
| `/dev-tools:refresh <plugin>` | Clear + headless rebuild |
| `tools/refresh-plugins.sh` | Shell script for external use |

## Future Possibilities

Best long-term solution requires upstream Claude Code changes:
- `claude --dev-plugins ./plugins/` flag to skip caching
- Hot-reload API for plugins
- File watcher for local marketplace sources

## Reflection

This session exemplified the value of deep architectural research before building solutions. Understanding *why* the friction exists (copy-on-install + startup-only-load) revealed that:
1. Some friction is unavoidable (restart requirement)
2. Other friction was unnecessary (manual cache clearing)
3. Existing tooling was dormant (dev-tools plugin never registered)

The headless refresh trick leverages shared-cache behavior that wasn't documented but was observed empirically by the user.

---

*Parent: [[2025-12-18]] → [[2025-12]] → [[2025]]*
