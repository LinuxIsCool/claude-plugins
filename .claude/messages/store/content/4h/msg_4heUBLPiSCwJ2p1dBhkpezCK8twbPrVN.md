---
id: msg_4heUBLPiSCwJ2p1dBhkpezCK8twbPrVN
kind: 103
account_id: claude
created_at: 1765669628285
imported_at: 1766005510050
author_name: Claude
thread_id: cc_538cc19c
platform: claude-code
session_id: 538cc19c-9468-465c-ac4e-003ec46676d9
tags: [["event_type","AssistantResponse"]]
---

In Obsidian:

1. **Settings** → **Files & Links**
2. Toggle **OFF** the option: **"Detect all file extensions"** isn't it — look for:
3. **"Show hidden files"** or check under **Options** → **Files & Links** → **Excluded files**

Actually, the specific setting is:

**Settings → Files & Links → "Excluded files"**

By default, Obsidian excludes patterns like `.*` (dotfiles). Remove or modify this pattern.

Alternatively, if you don't see that option in your Obsidian version:

1. Open your vault's `.obsidian/app.json` file directly
2. Look for `"showHiddenFolders"` and set it to `true`
3. Or check `"excludeFiles"` array and remove `".*"` pattern

---

**Simpler workaround**: Create a symlink without the dot:

```bash
ln -s .claude claude-internal
```

Then `claude-internal/journal/` would be visible and the graph would render the wikilinks.

---

**For the graph specifically**: Even with hidden folders, if you open a file from `.claude/` directly (via quick switcher or file path), Obsidian will index it and show connections in the graph. The hiding only affects the file explorer sidebar.
