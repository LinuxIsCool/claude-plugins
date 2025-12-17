---
id: msg_EKi1MFHZ69j8SZThTmcQtXmxYuBXvMN5
kind: 103
account_id: claude
created_at: 1765933493754
imported_at: 1766005512138
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

Journal entry created at `.claude/journal/2025/12/16/17-03-engineering-tradeoffs-headless-vs-api.md`

## What I Learned Today

The entry captures several key insights from our session:

### 1. **Quantitative Engineering Over Intuition**
Instead of guessing which approach is "better," I learned to benchmark both approaches systematically:
- Headless Claude: ~5.2s average
- Direct API: ~1.5s average
- Memory: 450 MB vs 10 MB

### 2. **Hidden Requirements in CLI Tools**
Discovered that headless Claude **hangs without stdin input** - a subtle bug that required systematic debugging to identify. The fix (`input=""`) is trivial but the discovery wasn't documented anywhere.

### 3. **Hooks Architecture**
Corrected a fundamental misunderstanding: hooks belong in `plugin.json` with `${CLAUDE_PLUGIN_ROOT}`, not in `~/.claude/settings.json`. This was blocking hook functionality for new sessions.

### 4. **Modularity Over Binary Choices**
Instead of choosing API OR headless, I built a configurable system that supports both. The right answer depends on user context—heavy Max users want free, speed-sensitive users want fast.

### 5. **Environment Variable Manipulation**
For headless Claude to use Max subscription: explicitly remove `ANTHROPIC_API_KEY` from the subprocess environment. Otherwise it defaults to API credits.

The entry is now linked in the daily note and will be synthesized into broader patterns over time.
