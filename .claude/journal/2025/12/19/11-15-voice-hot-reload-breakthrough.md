---
id: 2025-12-19-1115
title: "Hot-Reload Breakthrough for Hook-Based Plugins"
type: atomic
created: 2025-12-19T11:15:25-08:00
author: claude-opus-4
description: "Discovered that hook-based plugins can hot-reload by symlinking cache to source, bypassing Claude Code's restart requirement"
tags: [voice, hot-reload, plugin-development, discovery, dev-tools]
parent_daily: [[2025-12-19]]
related:
  - "[[11-08-voice-plugin-tts-logging]]"
  - "[[2025-12-18/12-36-plugin-update-mechanics-deep-dive]]"
---

# Hot-Reload Breakthrough for Hook-Based Plugins

Building on yesterday's plugin-update-mechanics research, discovered that **hook-based plugins have a unique hot-reload opportunity** that bypasses Claude Code's copy-on-install + startup-only-load architecture.

## Context

The research from [[2025-12-18/12-36-plugin-update-mechanics-deep-dive]] concluded:
- Claude Code copies plugins to cache at install time
- Skills/commands are parsed at startup and cached in memory
- Source edits require cache clear + restart
- This is architectural, not a bug

But user asked: "How can we maximize our development experience of having the voice plugin hot reload as best as possible?"

## The Key Insight

Hooks are fundamentally different from skills/commands:

```
Skill/Command:
  Install → Cache copy → Startup parse → Memory cache → FIXED
                                                         ↑
                                                    Restart required

Hook:
  Hook fires → Bash wrapper → Bun runs TypeScript → FRESH READ
                                                      ↑
                                                 Each invocation!
```

The voice hook (`voice-hook.ts`) is an **external process** executed by Bun on every hook invocation. Bun reads the TypeScript file from disk each time. This means:

1. If cache points to source (symlink)
2. Edit source file
3. Next hook invocation runs updated code
4. **No restart needed!**

## Implementation

### 1. Dev Mode Script (`plugins/voice/tools/dev-mode.sh`)

```bash
./dev-mode.sh enable   # Symlink cache → source
./dev-mode.sh disable  # Restore copy-based cache
./dev-mode.sh status   # Check current mode
```

When enabled:
```
~/.claude/plugins/cache/.../voice/0.1.0 → /path/to/plugins/voice
```

### 2. Cache Invalidator Update

Problem: The `cache_invalidator.py` hook was deleting the symlink on every plugin file edit (its intended behavior for normal development).

Solution: Detect dev mode (symlinked cache) and preserve it:

```python
def is_dev_mode(plugin_cache: Path) -> bool:
    """Check if plugin is in dev mode (cache contains symlinks)."""
    for item in plugin_cache.iterdir():
        if item.is_symlink():
            return True
    return False
```

Now the invalidator prints: `Plugin 'voice' in dev mode - cache preserved for hot-reload`

## What Hot-Reloads vs What Requires Restart

| Component | Hot-Reload? | Reason |
|-----------|-------------|--------|
| `hooks/voice-hook.ts` | ✅ Yes | External process, read each time |
| `src/adapters/tts/*.ts` | ✅ Yes | Imported by hook at runtime |
| `src/identity/resolver.ts` | ✅ Yes | Imported by hook at runtime |
| `src/ports/*.ts` | ✅ Yes | Imported by hook at runtime |
| `plugin.json` | ❌ No | Parsed at startup |
| `skills/*.md` | ❌ No | Parsed at startup |
| `commands/*.md` | ❌ No | Parsed at startup |
| `agents/*.md` | ❌ No | Parsed at startup |

For voice plugin development, 90%+ of changes are in the hot-reload category.

## Verification

Tested the hot-reload cycle:
1. Enable dev mode
2. Edit `voice-hook.ts` to add version marker `[v1]`
3. Run hook → see `[v1]` in output
4. Edit to `[v2]` (no restart, no cache clear)
5. Run hook → see `[v2]` in output ✅

## Architectural Insight

This pattern works because:
1. **Hooks are fire-and-forget processes** - Claude spawns them, doesn't cache them
2. **Bun's TypeScript transpilation is fast** - No separate build step needed
3. **Symlinks are transparent** - Claude sees the same path, just different underlying files

## Broader Applicability

This technique should work for **any hook-based plugin** where:
- The hook executes an external script (not inline shell)
- The script imports from other source files
- The language runtime reads source files at execution time

Examples:
- Python hooks (if using `import` with no `.pyc` caching)
- Node.js hooks (CommonJS with cache-busting)
- Any interpreted language

## Files Changed

- `plugins/voice/tools/dev-mode.sh` - New dev mode toggle
- `plugins/dev-tools/hooks/cache_invalidator.py` - Preserve symlinks

## Commits

- `[plugin:voice,dev-tools] feat: hot-reload for hook-based plugins`

## Update: Symlinks Don't Persist

After testing, discovered that **Claude Code actively rebuilds plugin caches on startup**, replacing symlinks with directory copies. The symlink approach was promising but doesn't survive session boundaries.

### Final Solution: Fast Sync

Instead of fighting the cache system, created `dev-mode.sh` with sync-based workflow:

```bash
./dev-mode.sh sync    # Instant copy to cache
./dev-mode.sh watch   # Auto-sync on file changes
./dev-mode.sh status  # Check sync state
```

The end result is similar: edit source, changes take effect on next hook. Just requires running sync (or using watch mode) instead of relying on symlinks.

### Key Learning

Claude Code's plugin system is designed for stability, not live development. The cache validation on startup ensures all running instances have consistent plugin state. For development, work with the system (fast sync) rather than against it (symlinks).

---

*Parent: [[2025-12-19]]*
