---
id: 2025-12-19-1434
title: "Voice Character Curator and Plugin Cache Infrastructure"
type: atomic
created: 2025-12-19T14:34:36
author: claude-opus-4
description: "Created voice-character-curator agent, fixed plugin cache infrastructure, enhanced dev-tools refresh workflow"
tags: [voice, agents, plugin-architecture, cache, hot-reload, character-design]
parent_daily: [[2025-12-19]]
related:
  - [[13-49-whisper-stt-implementation]]
  - [[13-50-vad-integration-implementation]]
---

# Voice Character Curator and Plugin Cache Infrastructure

This session accomplished two major milestones: creating a comprehensive voice character system design and fixing critical plugin cache infrastructure issues.

## Context

The voice plugin was experiencing hook failures after cache operations. Investigation revealed a cascade of issues stemming from how Claude Code manages plugin caches, particularly for hook-based plugins. Simultaneously, the user requested creation of a "voice-character-curator" agent to serve as the creative director for voice personality design.

## The Cache Problem

When the Stop hook failed with "No such file or directory", investigation revealed:

1. **Missing settings.json entry**: `voice@linuxiscool-claude-plugins` was absent from `enabledPlugins`
2. **Cache not rebuilding**: Claude's headless rebuild (`claude -p "exit"`) wasn't populating the voice plugin cache
3. **Symlink limitation**: Earlier discovery (documented in previous sessions) showed Claude Code validates and rebuilds caches on startup, breaking symlinks

### Root Cause Analysis

```
User runs: /dev-tools:refresh voice
  ↓
Cache cleared: ~/.claude/plugins/cache/linuxiscool-claude-plugins/voice/
  ↓
Headless Claude spawned: claude -p "exit" --setting-sources ""
  ↓
Voice plugin NOT in enabledPlugins → Cache not rebuilt
  ↓
Next hook invocation fails: "No such file or directory"
```

The `installed_plugins.json` had the voice plugin registered with `scope: "local"` tied to the project, but the `settings.json` `enabledPlugins` object was missing the voice entry entirely.

## The Solution

### 1. Enable the Plugin

Added to `~/.claude/settings.json`:
```json
"voice@linuxiscool-claude-plugins": true
```

### 2. Enhance dev-mode.sh

The voice plugin already had a `dev-mode.sh` script for hot-reload development. Enhanced it to also sync the `agents/` directory:

```bash
# Sync agents (subagents via Task tool)
if [[ -d "$SOURCE_DIR/agents" ]]; then
    echo "  Syncing agents/..."
    mkdir -p "$CACHE_DIR/agents"
    cp -r "$SOURCE_DIR/agents/"* "$CACHE_DIR/agents/"
fi
```

This enables hot-reload of agent definitions without Claude restart.

### 3. Enhance refresh-plugins.sh

Made `/dev-tools:refresh` automatically run `dev-mode.sh sync` for any plugin that has one:

```bash
sync_plugin() {
    local plugin_name="$1"
    local dev_mode_script="$SCRIPT_DIR/$plugin_name/tools/dev-mode.sh"

    if [[ -x "$dev_mode_script" ]]; then
        echo "  Running dev-mode.sh sync for $plugin_name..."
        bash "$dev_mode_script" sync 2>&1 | sed 's/^/    /'
    fi
}
```

**New workflow:**
1. Clear cache
2. Trigger Claude headless rebuild
3. Run `dev-mode.sh sync` for each plugin that has it

## Voice Character Curator Agent

Created `plugins/voice/agents/voice-character-curator.md` as the creative director for voice personality design. This agent synthesizes insights from 5 research domains:

### Research Foundation (5 Parallel Agents)

Launched 5 research agents simultaneously to gather "essences":

| Agent | Domain | Output |
|-------|--------|--------|
| Philosophy | Authentic voice principles | `01-philosophy-of-authentic-voice.md` |
| Sound Design | Sonic architecture | `02-sonic-architecture.md` |
| Character | Emergence systems | `03-character-emergence.md` |
| Systems | Coherence theory | `04-systems-coherence.md` |
| Conversation | Flow intelligence | `05-conversational-flow.md` |

### Core Principles

**Character Through Constraint**: Unlimited possibility produces chaos. Character emerges from what you choose *not* to be. An AI constrained to speak as a thoughtful observer or curious explorer—now we have character.

**Presence Over Performance**: There exists a species of AI voice optimized to *sound* helpful without *being* helpful. Presence operates differently—expression matches state, creating trust.

**Coherent Pluralism**: Unity through diversity. Each agent has distinct voice identity, but all voices share underlying tonal principles. Archivist and Explorer sound different, but like *family*.

**The Edge of Chaos**: Balance between predictability (trust) and flexibility (genuine relationship). Living systems find equilibrium at the edge.

### Agent Responsibilities

1. **Character Architecture** - Design foundational identity for each voice-enabled agent
2. **Sonic Identity Design** - Curate audio signatures, non-verbal vocabulary
3. **Conversational Direction** - Guide flow state protection, turn-taking intelligence
4. **Character Emergence Cultivation** - Nurture characters that grow through interaction
5. **Systems Coherence** - Maintain coherent pluralism across agent fleet

### Non-Verbal Vocabulary (R2D2-Style)

| Category | Purpose | Design Principle |
|----------|---------|------------------|
| Greeting chirps | Agent presence announcement | Rising pitch, warm timbre |
| Thinking sounds | Processing indicators | Gentle oscillation, low volume |
| Success signals | Task completion | Ascending resolution, bright |
| Error tones | Problem indication | Descending, darker (never punishing) |
| Attention requests | Interrupt requests | Distinctive, respectful urgency |

## Technical Commits

| Hash | Description |
|------|-------------|
| `2482af5` | Voice character curator agent + 5 research specs |
| `91731a9` | Fix JSONL append bug (Bun.write → appendFile) |
| `d805b3c` | dev-mode.sh syncs agents directory |
| `ecb5de2` | refresh-plugins.sh auto-runs dev-mode.sh sync |

## Insights

### Hot-Reload Architecture Pattern

For hook-based plugins, the hot-reload pattern is:

```
Source (plugins/voice/)
    ↓ dev-mode.sh sync
Cache (~/.claude/plugins/cache/...)
    ↓ bun runs hook
Claude Code event handler
```

What hot-reloads without restart:
- `hooks/*.ts` - Main hook logic
- `src/**/*.ts` - TTS adapters, identity resolution
- `agents/*.md` - Agent definitions (loaded on Task invocation)

What requires restart:
- `.claude-plugin/plugin.json` - Plugin manifest
- New skill files
- New command files

### Plugin Registration Layers

Claude Code has multiple plugin registration layers that must align:

1. **installed_plugins.json** - Plugin version and path registry
2. **settings.json enabledPlugins** - Enable/disable switch
3. **Cache directory** - Actual plugin files Claude executes

If any layer is missing, the plugin won't work correctly. The voice plugin was in layer 1 but missing from layer 2.

### Bun.write Append Gotcha

`Bun.write(file, data, { append: true })` does NOT append—it overwrites. For true append behavior, use:

```typescript
import { appendFile } from "fs/promises";
await appendFile(file, data);
```

This caused the voice event logging to lose events until fixed.

## Philosophical Anchor

> *"Sound is not decoration. Sound is meaning."*
> *"Character is not configuration. Character is relationship."*
> *"The goal is not to make AI agents sound human. The goal is to make AI agents sound meaningful, emotionally resonant, and genuinely alive."*

The constraint is the foundation. The silence is the meaning. The character emerges from the relationship.

## Next Steps

1. Implement `VoicePersonalityManager` class
2. Create personality profiles for Explore, Archivist, Mentor agents
3. Design and source non-verbal sound files (R2D2-style)
4. Implement flow controller with queue management
5. Integrate with AgentNet for voice profile coordination

---

*Parent: [[2025-12-19]]*
