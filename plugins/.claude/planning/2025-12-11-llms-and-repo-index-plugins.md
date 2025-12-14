# LLMs Plugin & Repository Index Plugin

*Planning document - 2025-12-11*

## Overview

Two new plugins to extend Claude Code's capabilities:

1. **LLMs Plugin** - Shared service for embeddings, completions, and other LLM operations
2. **Repo Index Plugin** - Vector search over repository files (depends on LLMs plugin)

---

## LLMs Plugin

### Purpose

A centralized plugin that provides LLM capabilities as a service for other plugins. Any plugin needing embeddings, summarization, or other LLM operations can depend on this rather than implementing their own.

### Why Centralized?

- **Consistency**: Same embedding model across all plugins = comparable vectors
- **Configuration**: Single place for API keys, model preferences
- **Caching**: Shared cache avoids redundant API calls / computation
- **Upgrades**: Improve embedding quality once, all plugins benefit

### Proposed Capabilities

| Capability | Description | Use Cases |
|------------|-------------|-----------|
| **embed** | Text → vector | Semantic search, similarity |
| **embed_batch** | Multiple texts → vectors | Bulk indexing |
| **summarize** | Text → short summary | Log summaries, file summaries |
| **classify** | Text → category | Intent detection, routing |
| **complete** | Prompt → response | General LLM tasks |

### Embedding Backends (Priority Order)

1. **Hash-based** - Zero dependencies, deterministic, fast (default)
2. **sentence-transformers** - Local, good quality, ~500MB
3. **Ollama** - Local models, flexible
4. **OpenAI** - API-based, high quality
5. **Voyage/Cohere** - Specialized embedding APIs

### Interface Options

**Option A: CLI Tools**
```bash
# Other plugins call via subprocess
uv run plugins/llms/tools/embed.py "text to embed"
uv run plugins/llms/tools/embed.py --batch file_list.txt
uv run plugins/llms/tools/summarize.py "long text..."
```

**Option B: Python Library**
```python
# Other plugins import directly
from plugins.llms.lib import embed, summarize
vector = embed("text to embed")
vectors = embed_batch(["text1", "text2"])
```

**Option C: Both** (recommended)
- Library for Python plugins (faster, no subprocess overhead)
- CLI for shell scripts and non-Python tools

### Configuration

```yaml
# .claude/llms.yaml or plugins/llms/config.yaml
embedding:
  backend: hash  # hash | sentence-transformers | ollama | openai
  model: null    # backend-specific model name
  cache: true    # cache embeddings by content hash

summarization:
  backend: anthropic  # uses ANTHROPIC_API_KEY
  model: claude-3-haiku-20240307

api_keys:
  # Or use environment variables
  openai: ${OPENAI_API_KEY}
  anthropic: ${ANTHROPIC_API_KEY}
```

### Caching Strategy

```
.claude/llms/
├── cache/
│   ├── embeddings.db    # SQLite: content_hash → vector
│   └── summaries.db     # SQLite: content_hash → summary
└── config.yaml
```

Cache key = hash(backend + model + content)

### Proposed Structure

```
plugins/llms/
├── .claude-plugin/
│   └── plugin.json
├── lib/
│   ├── __init__.py
│   ├── embed.py         # Embedding logic
│   ├── summarize.py     # Summarization logic
│   ├── backends/
│   │   ├── hash.py      # Hash-based embeddings
│   │   ├── sentence_transformers.py
│   │   ├── ollama.py
│   │   └── openai.py
│   └── cache.py         # Caching layer
├── tools/
│   ├── embed.py         # CLI: embed text
│   ├── summarize.py     # CLI: summarize text
│   └── config.py        # CLI: show/set config
├── skills/
│   └── llm-tools/
│       └── SKILL.md     # When/how to use LLM tools
└── README.md
```

### Open Questions

1. **Default backend**: Hash (zero deps) or try to detect sentence-transformers?
2. **Vector dimensions**: Fixed (e.g., 384) or backend-dependent?
3. **Batch size limits**: How many texts per call?
4. **Error handling**: What if backend unavailable?
5. **Skill integration**: Should Claude know how to use this directly?

---

## Repository Index Plugin

### Purpose

Semantic search over all source files and documents in a repository.

### Depends On

- **LLMs Plugin** for embeddings

### Proposed Structure

```
plugins/repo-index/
├── .claude-plugin/
│   └── plugin.json
├── tools/
│   ├── index.py         # Build/update index
│   ├── search.py        # Query index
│   └── status.py        # Index statistics
├── lib/
│   ├── chunker.py       # File → chunks
│   ├── store.py         # Vector storage
│   └── filters.py       # File filtering (.gitignore, etc.)
├── skills/
│   └── repo-search/
│       └── SKILL.md
└── README.md
```

### Key Decisions (Deferred)

- Chunking strategy (line-based vs AST-aware)
- What file types to index
- Incremental vs full re-index
- Storage format

---

## Implementation Order

1. **LLMs Plugin** (this session)
   - Core embedding with hash backend
   - CLI interface
   - Caching layer

2. **Upgrade Logging Plugin**
   - Replace inline hash embeddings with LLMs plugin

3. **Repository Index Plugin** (next)
   - Uses LLMs plugin for embeddings
   - Simple chunking initially

---

## Discussion Points

Before implementing LLMs plugin:

1. Interface preference (CLI, library, or both)?
2. Configuration location and format?
3. Which capabilities first (just embed, or also summarize)?
4. Cache location (per-project or global)?
5. Skill for Claude to use it directly?
