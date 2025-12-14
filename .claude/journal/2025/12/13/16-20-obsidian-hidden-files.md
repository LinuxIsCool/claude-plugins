---
id: 2025-12-13-1620
title: "Obsidian Hidden Files Plugin"
type: atomic
created: 2025-12-13T16:20:00
author: claude-opus-4
description: "Installed show-hidden-files plugin to make .claude/ visible in Obsidian file explorer and graph view"
tags: [obsidian, plugin, infrastructure, tooling, graph]
parent_daily: [[2025-12-13]]
related:
  - [[15-45-journal-atomic-model]]
  - [[16-15-bootstrapping-trajectory]]
---

# Obsidian Hidden Files Plugin

Solved the problem of `.claude/` being invisible in Obsidian's file explorer.

## The Problem

Obsidian hardcodes hiding of dotfolders (directories starting with `.`). This meant:
- `.claude/journal/` invisible in file explorer
- No graph visualization of the DNA spiral
- Wikilinks worked but navigation was broken

Attempted solutions that failed:
- `app.json` setting `"showHiddenFolders": true` — not a real setting
- Symlink `claude -> .claude` — Obsidian ignores symlinks to hidden dirs
- Copying data — creates duplication (unacceptable)

## The Solution

**Plugin**: [obsidian-show-hidden-files](https://github.com/polyipseity/obsidian-show-hidden-files)

### Manual Installation

```bash
mkdir -p .obsidian/plugins/show-hidden-files
cd .obsidian/plugins/show-hidden-files
curl -sL https://github.com/polyipseity/obsidian-show-hidden-files/releases/latest/download/manifest.json -o manifest.json
curl -sL https://github.com/polyipseity/obsidian-show-hidden-files/releases/latest/download/main.js -o main.js
curl -sL https://github.com/polyipseity/obsidian-show-hidden-files/releases/latest/download/styles.css -o styles.css
```

### Activation

1. Close and reopen Obsidian (or toggle community plugins off/on)
2. Enable "Show Hidden Files" in Community plugins settings
3. `.claude/` appears in file explorer

## Result

- `.claude/` now visible in Obsidian file explorer
- Can navigate to `.claude/journal/2025/12/13/` directly
- Graph view will render the DNA spiral with all atomic entries
- Wikilinks fully functional with visual navigation

## Plugin Warning

Before enabling on vaults with large dotfolders (100+ files), note that Obsidian may freeze during initial scan. The plugin excludes `.git` and `.venv` by default.

## Implication for Ecosystem

The journal is now fully accessible in Obsidian:
- Atomic entries visible
- Daily/monthly/yearly synthesis navigable
- Graph view shows temporal relationships
- DNA spiral visualization possible

---
*Parent: [[2025-12-13]] → [[2025-12]] → [[2025]]*
