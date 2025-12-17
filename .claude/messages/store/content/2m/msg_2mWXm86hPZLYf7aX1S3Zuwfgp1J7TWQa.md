---
id: msg_2mWXm86hPZLYf7aX1S3Zuwfgp1J7TWQa
kind: 103
account_id: claude
created_at: 1765670148527
imported_at: 1766005510117
author_name: Claude
thread_id: cc_538cc19c
platform: claude-code
session_id: 538cc19c-9468-465c-ac4e-003ec46676d9
tags: [["event_type","AssistantResponse"]]
---

**Solution: Install the "Show Hidden Files" plugin**

1. In Obsidian: **Settings** → **Community plugins** → **Browse**
2. Search for **"Show Hidden Files"**
3. Install and enable it

**Warning from the plugin**: Before enabling, note that if your vault has large dotfolders (100+ files), Obsidian may freeze while scanning. The plugin excludes `.git` and `.venv` by default, but `.claude/` will be scanned.

After enabling, `.claude/` should appear in the file explorer with full access to the journal.

---

Sources:
- [Show Hidden Files Plugin (GitHub)](https://github.com/polyipseity/obsidian-show-hidden-files)
- [Obsidian Forum Discussion](https://forum.obsidian.md/t/enable-use-of-hidden-files-and-folders-starting-with-a-dot-dotfiles-dotfolders-within-obsidian/26908)
