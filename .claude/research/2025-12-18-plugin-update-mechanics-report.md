---
created: 2025-12-18T11:55:00-08:00
author: claude
type: research-report
topic: Plugin Update Mechanics and Development Workflow
tags: [research, plugins, caching, hot-reload, symlinks, development-experience]
---

# Plugin Update Mechanics: Deep Research Report

## Executive Summary

Claude Code's plugin system uses a **copy-on-install** architecture with aggressive caching. Changes to plugin source files are **not automatically reflected** in running sessions. The system prioritizes stability over live updates, requiring explicit cache invalidation and session restart for changes to propagate.

This report details the mechanics, identifies optimization opportunities, and catalogues current symlink usage.

---

## Part 1: How Plugin Updates Are Processed

### The Plugin Loading Pipeline

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Source Files   │───▶│  Plugin Install  │───▶│  Cache Copy     │
│  (plugins/)     │    │  (/plugin cmd)   │    │ (~/.claude/...)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Claude Session │◀───│  In-Memory Load  │◀───│  Cache Read     │
│  (tools active) │    │  (startup only)  │    │  (version dir)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Key Discovery: Copy-on-Install, Not Symlink

Claude Code **copies** plugin files to the cache rather than symlinking. This means:

1. **Source changes are invisible** - Editing `plugins/awareness/skills/...` does nothing to the running session
2. **Cache is authoritative** - Claude reads from `~/.claude/plugins/cache/`, not your source
3. **Version isolation** - Each version gets its own directory (e.g., `0.3.0/`)

### Cache Structure (Observed)

```
~/.claude/plugins/
├── cache/
│   └── linuxiscool-claude-plugins/
│       └── awareness/
│           ├── 0.3.0/                    # Versioned copy
│           │   ├── .orphaned_at          # Orphan timestamp (ms)
│           │   ├── skills/
│           │   ├── commands/
│           │   └── ...
│           └── current -> 0.3.0          # Symlink to active version
├── marketplaces/
│   └── linuxiscool-claude-plugins.json   # Marketplace metadata
└── installed_plugins.json                # Plugin registry
```

### The `current` Symlink

Each cached plugin has a `current` symlink pointing to the active version directory. This enables:
- Version switching without full reinstall
- Rollback capability (keep old versions)
- Clean upgrade paths

### Registry vs Reality Discrepancy

**Observed Issue**: `installed_plugins.json` shows version `0.1.0` while cache has `0.3.0`:
```json
{
  "awareness@linuxiscool-claude-plugins": [{
    "installPath": "...awareness/0.1.0",  // ← Points to old version
    "version": "0.1.0"                    // ← Registry hasn't updated
  }]
}
```

This discrepancy suggests the registry is not authoritative—Claude Code likely resolves through the `current` symlink.

### Cache Staleness Evidence

| Location | Last Modified |
|----------|---------------|
| Source file | 2025-12-15 09:56 |
| Cache file | 2025-12-13 16:59 |

The cache is **2 days stale**, confirming that edits to source don't propagate.

---

## Part 2: Why Restart Is Required

### 1. Startup-Only Loading

Claude Code loads plugins **once** at session start:
- Skills are parsed and indexed
- Commands are registered
- Hooks are bound to events
- Agents are catalogued

There is **no runtime refresh mechanism** for these components.

### 2. In-Memory Caching

After loading, plugin data lives in memory:
- Skill descriptions are tokenized
- Hook matchers are compiled
- Tool availability is fixed

Changing files on disk has no effect on the running process.

### 3. MCP Server Exception

MCP servers **can** be restarted during a session via the MCP hot-reload helper. This is because MCP is a separate process communicating via stdio/HTTP, not in-process code.

### 4. Known Bug: /plugin update Doesn't Invalidate Cache

[GitHub Issue #14061](https://github.com/anthropics/claude-code/issues/14061) documents that `/plugin update`:
- Does NOT clear `~/.claude/plugins/cache/`
- Does NOT update `installed_plugins.json` gitCommitSha
- Results in stale code running

---

## Part 3: Current Development Workflow

### The Friction Cycle

```
Edit Source → (invisible) → Test → Confused → Remember cache →
Clear cache → Restart → Test → Success
```

### Documented Workflow (from plugin-developer skill)

```bash
# 1. Edit source files
vim plugins/my-plugin/skills/*/SKILL.md

# 2. Clear cache (mandatory)
rm -rf ~/.claude/plugins/cache/linuxiscool-claude-plugins/my-plugin/

# 3. Restart Claude Code (mandatory)
exit  # or Ctrl+C
claude

# 4. Test changes
```

### Existing Tooling

| Tool | Location | Purpose |
|------|----------|---------|
| `/dev-tools:reload` | `plugins/dev-tools/commands/reload.md` | Clears cache for plugins |
| `clear_plugin_cache.py` | (inline in skill) | Python script for cache clearing |

---

## Part 4: Opportunities for Seamless Updates

### Option A: Symlink Source to Cache (Partial Solution)

**Concept**: Instead of copying, symlink from cache to source:
```bash
rm -rf ~/.claude/plugins/cache/linuxiscool-claude-plugins/awareness/0.3.0
ln -s /home/ygg/Workspace/sandbox/marketplaces/claude/plugins/awareness \
      ~/.claude/plugins/cache/linuxiscool-claude-plugins/awareness/0.3.0
```

**Pros**:
- Source changes appear in cache immediately
- No copy drift

**Cons**:
- Still requires restart (in-memory loading unchanged)
- Breaks on plugin uninstall/reinstall
- Claude Code may overwrite with copy on update
- Version management becomes manual

**Verdict**: Marginal improvement, fragile

### Option B: File Watcher + Session Restart Hook

**Concept**: Watch source files, trigger graceful restart on change:
```bash
#!/bin/bash
# watch-plugins.sh
inotifywait -m -r -e modify plugins/ | while read; do
    # Clear cache
    rm -rf ~/.claude/plugins/cache/linuxiscool-claude-plugins/
    # Signal current Claude session
    # (no graceful restart API exists)
done
```

**Cons**:
- No API for graceful session restart
- Would lose context
- User disruption

**Verdict**: Not viable without Claude Code changes

### Option C: Development Mode Flag

**Concept**: A `--dev-mode` flag that:
1. Skips cache entirely
2. Reads directly from source paths
3. Hot-reloads on file change

**Requires**: Claude Code upstream changes

**Verdict**: Best long-term solution, requires feature request

### Option D: Auto-Clear Cache Hook

**Concept**: A `PostToolUse` hook that clears cache when Write/Edit touches plugin files:

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "bash -c 'if [[ \"$TOOL_INPUT\" == *plugins/* ]]; then rm -rf ~/.claude/plugins/cache/linuxiscool-claude-plugins/; fi'"
      }]
    }]
  }
}
```

**Pros**:
- Automatic cache clearing
- Integrates with existing workflow

**Cons**:
- Still requires restart
- Would clear ALL plugin caches (too aggressive)

**Verdict**: Useful optimization, partially implemented in dev-tools

### Option E: Semantic Version Bumping

**Concept**: Auto-increment version in plugin.json on save:
1. Hook detects plugin file edit
2. Bumps patch version (0.3.0 → 0.3.1)
3. Next restart loads new version

**Pros**:
- Clean version history
- Audit trail

**Cons**:
- Version inflation
- Still requires restart

---

## Part 5: Symlink Catalogue

### Repository Symlinks (Non-node_modules)

| # | Location | Target | Purpose |
|---|----------|--------|---------|
| 1 | `resources/Backlog.md/src/guidelines/project-manager-backlog.md` | `../../.claude/agents/project-manager-backlog.md` | Single source for agent definition |
| 2 | `resources/agents/pydantic-ai/AGENTS.md` | `CLAUDE.md` | Naming alias |
| 3 | `resources/agents/anthropic-sdk-typescript/packages/bedrock-sdk/src/internal` | `../../../src/internal` | SDK code deduplication |
| 4 | `resources/agents/anthropic-sdk-typescript/packages/foundry-sdk/src/internal` | `../../../src/internal` | SDK code deduplication |
| 5 | `resources/agents/anthropic-sdk-typescript/packages/vertex-sdk/src/internal` | `../../../src/internal` | SDK code deduplication |
| 6 | `resources/claude-code-hooks-multi-agent-observability/apps/server/.cursor/rules/...` | `../../CLAUDE.md` | IDE config reuse |

### Plugin Cache Symlinks

| Plugin | Symlink | Target |
|--------|---------|--------|
| awareness | `current` | `0.3.0` |
| logging | `current` | `0.4.0` |
| backlog | `current` | `0.1.0` |
| schedule | `current` | `1.0.0` |
| ... (all plugins) | `current` | `{version}` |

### Symlink Design Analysis

**Strengths**:
1. **Single source of truth** - Agent definitions not duplicated
2. **Relative paths** - Repository is relocatable
3. **Clean separation** - Resources vs core code

**Risks**:
1. **Broken symlinks** - If targets move, links break silently
2. **Git handling** - Symlinks may not work on Windows
3. **Build processes** - Some tools don't follow symlinks

**Recommendation**: Current symlink usage is appropriate for:
- Resource deduplication (SDK internals)
- Cross-reference aliasing (AGENTS.md → CLAUDE.md)
- Version management (cache `current` → version)

---

## Part 6: Recommendations

### Immediate Improvements (No Upstream Changes)

1. **Use `/dev-tools:reload`** command consistently
2. **Add pre-edit reminder** via hook:
   ```
   PreToolUse on Write|Edit in plugins/:
   "Remember to clear cache and restart after plugin changes"
   ```
3. **Version bump discipline** - Increment version when making changes
4. **Automate cache clear** - Add to common workflows

### Medium-Term (Local Tooling)

1. **Plugin development script**:
   ```bash
   #!/bin/bash
   # dev-plugin.sh
   PLUGIN=$1
   inotifywait -m -r plugins/$PLUGIN | while read; do
       rm -rf ~/.claude/plugins/cache/linuxiscool-claude-plugins/$PLUGIN/
       echo "Cache cleared. Restart Claude Code to apply."
       notify-send "Plugin $PLUGIN updated - restart required"
   done
   ```

2. **tmux integration** - Auto-restart Claude in adjacent pane

### Long-Term (Feature Requests)

1. **Dev mode** - `claude --dev-plugins ./plugins/` skips cache
2. **Hot reload API** - `/plugin reload awareness` without full restart
3. **File watcher** - Built-in watch for local marketplace sources
4. **Cache bypass** - `"devMode": true` in plugin.json

---

## Conclusion

The plugin update friction is architectural—Claude Code prioritizes stability and predictability over live development ergonomics. The copy-on-install + startup-only-load pattern means:

- **Source edits require cache clear + restart**
- **This is by design, not a bug**
- **Workarounds exist but add friction**

The path to seamless development requires either:
1. Upstream Claude Code changes (dev mode)
2. Accepting the restart cycle with better tooling
3. Hybrid approach (symlink experiments + auto-clear hooks)

For the current ecosystem, the `/dev-tools:reload` command combined with disciplined restarts remains the most reliable workflow.

---

*Research conducted: 2025-12-18*
*Agent: claude (opus-4.5)*
*Tools used: Bash, Read, Grep, Glob, Task (Explore, claude-code-guide)*
