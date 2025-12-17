---
id: msg_GKHBG8gkN4ESxZkXz2ZUjo9kaZbHwFAB
kind: 103
account_id: claude
created_at: 1765505723353
imported_at: 1766005508570
author_name: Claude
thread_id: cc_b22351d6
platform: claude-code
session_id: b22351d6-b55f-4ddb-9052-a7ab0e0332ce
tags: [["event_type","AssistantResponse"]]
---

Planning documented. Now let's discuss the LLMs plugin specifics.

## LLMs Plugin - Key Design Questions

### 1. Interface

| Option | Pros | Cons |
|--------|------|------|
| **CLI only** | Simple, language-agnostic | Subprocess overhead for bulk ops |
| **Library only** | Fast, Pythonic | Only usable from Python |
| **Both** | Flexible | More code to maintain |

My lean: **Both** - library for performance, CLI for flexibility

### 2. Initial Capabilities

| Capability | Priority | Notes |
|------------|----------|-------|
| `embed` | Must have | Core use case |
| `embed_batch` | Must have | Bulk indexing |
| `summarize` | Nice to have | Already in logging plugin |
| `complete` | Later | Claude Code already does this |

### 3. Embedding Backends

```
Default: hash (zero deps, works everywhere)
Optional: sentence-transformers (if installed)
Future: ollama, openai, voyage
```

Should the plugin auto-detect available backends and use the best one? Or explicit config only?

### 4. Configuration & Storage Location

Options:
- **Per-project**: `.claude/llms/` (like logging)
- **Global**: `~/.config/claude-code/llms/`
- **Both**: Global defaults, per-project overrides

### 5. Vector Dimensions

Hash-based can produce any dimension. sentence-transformers depends on model (384, 768, 1536). 

Should we:
- **Standardize** on one dimension (e.g., 384)?
- **Let backends choose** and store dimension in metadata?

### 6. Key Questions for You

1. **Do you want Claude to be able to invoke this directly via a skill?** (e.g., "embed this text for me")

2. **Should we extract the existing summarization from logging plugin into this?** (consolidate LLM ops)

3. **API key handling** - environment variables only, or also config file?

4. **Any specific backends you'd want prioritized?** (Ollama? OpenAI?)

What's your vision for how this plugin gets used day-to-day?
