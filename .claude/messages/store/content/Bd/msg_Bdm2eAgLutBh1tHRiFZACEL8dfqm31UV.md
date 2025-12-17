---
id: msg_Bdm2eAgLutBh1tHRiFZACEL8dfqm31UV
kind: 103
account_id: claude
created_at: 1765245558060
imported_at: 1766005508229
author_name: Claude
thread_id: cc_0143495c
platform: claude-code
session_id: 0143495c-64d7-47df-9e2d-f1095b6a3683
tags: [["event_type","AssistantResponse"]]
---

All 5 subagents have completed. Here's a comprehensive synthesis of the research findings:

---

## Hot Reload Research Summary for Claude Code Plugins

### Key Discovery: Partial Hot Reload Already Exists!

**Good news:** Hook *script code* (`.py` files) is already hot-reloadable because each hook executes as a fresh subprocess via `uv run`. When you edit `log_event.py`, the changes take effect on the next hook invocation automatically.

**What requires restart:** Changes to `plugin.json` (hook registration, new events, metadata) require restarting Claude Code because the configuration is loaded once at startup.

---

### 5 Approaches to Simplify the Development Cycle

#### 1. **Do Nothing for Script Changes** (Already Works!)
- Edit your `.py` hook files freely
- Changes apply immediately on next hook trigger
- No restart needed for logic/code changes

#### 2. **UserPromptSubmit Hook with Change Detection** (Recommended)
Add a hook that checks file modification times and warns you:
```python
# Check plugin file mtimes on each prompt
# Warn: "⚠️ plugin.json changed - restart to apply"
```
**Pros:** Works within constraints, no daemon needed
**Cons:** Detection only, not auto-reload

#### 3. **External File Watcher Script** (Full Automation)
```bash
watchmedo auto-restart -d plugins -p '*.json' -- claude
```
Or with Python `watchfiles`:
```python
from watchfiles import watch
for changes in watch('./plugins'):
    subprocess.run(["pkill", "-f", "claude"])
    subprocess.Popen(["claude"])
```
**Pros:** True hot reload, automatic
**Cons:** Disrupts active sessions, external dependency

#### 4. **Custom `/plugin reload` Command** (Feature Request)
Would require Anthropic to add runtime plugin registry updates to Claude Code core. Not currently available.

#### 5. **Symlink Development Pattern** (Workaround)
- Keep plugin source in a dev directory
- Symlink to `plugins/` directory
- Edit source, run `/plugin update`, restart
- Slightly faster than full re-install

---

### Architecture Insight

```
Current Flow:
┌─────────────────────────────────────────────────────┐
│ Claude Code Startup                                 │
│   └─> Load plugin.json (COLD - cached at startup)  │
│   └─> Register hooks in memory                      │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Hook Event Triggered                                │
│   └─> uv run hook_script.py (HOT - fresh process)  │
│   └─> Script reads latest .py code                  │
└─────────────────────────────────────────────────────┘
```

---

### Recommended Development Workflow

| Change Type | Action Required |
|-------------|-----------------|
| Hook logic (`.py`) | Just save - auto-reloads |
| `plugin.json` changes | Restart Claude Code |
| New hook events | Restart Claude Code |
| Plugin metadata | Restart Claude Code |

### Best Practice for Plugin Development

1. **Keep hook logic in `.py` files** - these hot-reload automatically
2. **Minimize `plugin.json` changes** - only update when adding new events
3. **Use a file watcher for `plugin.json`** - get notified when restart is needed
4. **Consider an external wrapper script** - for fully automated reload during heavy development

Would you like me to implement any of these approaches (like the change-detection hook or the file watcher script)?
