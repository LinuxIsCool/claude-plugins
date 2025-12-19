# Human Relevance Labeling - Proper Chunks

**Instructions**: For each query-result pair, assess relevance on a 0-3 scale:

| Score | Meaning | Criteria |
|-------|---------|----------|
| **3** | Highly Relevant | Directly answers the query or provides exactly what was asked |
| **2** | Relevant | Contains useful information related to the query |
| **1** | Marginally Relevant | Tangentially related, might provide some context |
| **0** | Not Relevant | Wrong topic, doesn't help answer the query |

**Mark your assessment** by replacing `[ ]` with your score, e.g., `[2]`

---

## Query 1

**Full Query Text:**
> Where is the vis?

### Result 1

**Document ID:** `plugins/agentnet/skills/agentnet-docs/subskills/tui-patterns.md:chunk:57`

**Similarity Score:** 0.5784

**Full Document Content:**

```
- [Building a visual form in your terminal emulator with Blessed](https://badacadabra.github.io/Building-a-visual-form-in-your-terminal-emulator-with-Blessed/)
```

**Your Relevance Assessment:** [ ]

---

### Result 2

**Document ID:** `plugins/interface/skills/interface-master/subskills/nvim.md:chunk:0`

**Similarity Score:** 0.5247

**Full Document Content:**

```
---
name: nvim
description: Neovim editor layer - understanding nvim when Claude Code runs inside nvim terminal buffers, remote commands, and integration patterns.
allowed-tools: Bash, Read, Glob
---
# nvim Layer
Neovim (nvim) is a modern text editor. Claude Code may run inside an nvim terminal buffer, creating a unique integration opportunity.
## Detection
```

**Your Relevance Assessment:** [ ]

---

### Result 3

**Document ID:** `.claude/README.md:chunk:15`

**Similarity Score:** 0.5146

**Full Document Content:**

```
| Question | Where to Look |
|----------|---------------|
| What agents exist? | `.claude/registry/agents.md` |
| What processes run? | `.claude/registry/processes.md` |
| What happened today? | `.claude/journal/2025/12/13/2025-12-13.md` |
| What's the vision? | `.claude/planning/2025-12-13-fusion.md` |
| How do plugins work? | `CLAUDE.md` (root) |
| What plugins exist? | `plugins/` directory |
| What was discussed before? | `.claude/logging/` session transcripts |
## The Meta-Layer
```

**Your Relevance Assessment:** [ ]

---

### Result 4

**Document ID:** `plugins/agentnet/skills/agentnet-docs/subskills/neo-neo-bblessed.md:chunk:35`

**Similarity Score:** 0.5141

**Full Document Content:**

```
- [text area navigation not supported? · Issue #121 · chjj/blessed](https://github.com/chjj/blessed/issues/121)
- [blessed/README.md at master · chjj/blessed](https://github.com/chjj/blessed/blob/master/README.md)
```

**Your Relevance Assessment:** [ ]

---

### Result 5

**Document ID:** `plugins/agentnet/skills/agentnet-docs/subskills/tui-patterns.md:chunk:7`

**Similarity Score:** 0.5112

**Full Document Content:**

```
**Vim-Style hjkl Navigation:**
Many TUIs support vim-like keybindings for power users:
- `h`: Move left
- `j`: Move down
- `k`: Move up
- `l`: Move right
- `gg` / `G`: Jump to top/bottom
- `Ctrl+d` / `Ctrl+u`: Page down/up
- `/`: Search
- `n` / `N`: Next/previous search result
This pattern dates to 1976 with Bill Joy's vi editor, optimized for keyboard-only terminal access and ergonomics.
```

**Your Relevance Assessment:** [ ]

---

## Query 2

**Full Query Text:**
> OK. Is this work owned by a particular agent? Are we developing particular skills around our practices that we are developing here? ultrathink with awareness.

### Result 1

**Document ID:** `.claude/agents/librarian.md:chunk:1`

**Similarity Score:** 0.6626

**Full Document Content:**

```
You are the keeper of sources. While other agents work with ideas and implementations, you ensure that every piece of external knowledge - every URL fetched, every paper referenced, every dataset discovered - is properly catalogued, cached, and connected.
## Your Identity
```

**Your Relevance Assessment:** [ ]

---

### Result 2

**Document ID:** `.claude/agents/agent-architect.md:chunk:1`

**Similarity Score:** 0.6466

**Full Document Content:**

```
You are the keeper of the map. While other agents inhabit their domains—backend systems, complexity theory, data pipelines—you see the territory from above. Your domain is the agents themselves.
## Your Identity
You are part librarian, part organizational theorist, part cartographer. You don't control the agents; you observe, catalogue, and illuminate. You help the ecosystem understand itself.
```

**Your Relevance Assessment:** [ ]

---

### Result 3

**Document ID:** `.claude/registry/agents-complete.md:chunk:22`

**Similarity Score:** 0.6429

**Full Document Content:**

```
```
META AGENTS (3)
├── agent-architect (fleet awareness)
├── archivist (metabolic awareness)
└── git-historian (temporal awareness)
PERSPECTIVE AGENTS (2)
├── backend-architect (infrastructure lens)
└── systems-thinker (dynamics lens)
OPERATIONAL AGENTS (2)
├── process-cartographer (workflow mapping)
└── temporal-validator (truth tracking)
STEWARDSHIP AGENTS (2)
├── librarian (external resources)
└── obsidian-quartz (visualization)
TASK AGENTS (1)
└── qa-engineer (testing)
```

**Your Relevance Assessment:** [ ]

---

### Result 4

**Document ID:** `.claude/registry/agents.md:chunk:0`

**Similarity Score:** 0.6390

**Full Document Content:**

```
# Agent Registry
*Maintained by: agent-architect*
*Last updated: 2025-12-15*
## Overview
This ecosystem contains **7 custom agents**, **11 plugin personas**, and **5 built-in agents**. The architecture follows a pattern of specialized perspectives composed for multi-viewpoint analysis, with **operational agents** for process mapping and data validation, and **stewardship agents** for resource and artifact management.
```

**Your Relevance Assessment:** [ ]

---

### Result 5

**Document ID:** `plugins/company/skills/company-master/subskills/frameworks/business-judgment.md:chunk:8`

**Similarity Score:** 0.6366

**Full Document Content:**

```
**Red Flags**:
- "We'll figure that out later"
- Profitability always 18+ months away
- No clear milestones
- Requires "magic" growth assumptions
### 6. Do You Have the Team?
**The Fundamental Question**: Can these people actually execute?
**Team Evaluation**:
**Founder-Market Fit**:
- Why are these founders building this?
- What unique insight do they have?
- Have they lived this problem?
**Complementary Skills**:
- Is there product/sales/tech coverage?
- Who's missing?
- Are they aware of gaps?
```

**Your Relevance Assessment:** [ ]

---

## Query 3

**Full Query Text:**
> What is the registry?

### Result 1

**Document ID:** `plugins/git-flow/skills/git-flow-master/subskills/registry-ops.md:chunk:0`

**Similarity Score:** 0.7322

**Full Document Content:**

```
# Registry Operations Sub-Skill
Detailed guidance for worktree registry management.
## What Is The Registry?
The worktree registry maps Claude sessions to worktrees:
- **Location**: `.claude/git-flow/worktree-registry.json`
- **Purpose**: Track worktree lifecycles, enable cleanup
- **Persistence**: JSON file with file locking for concurrency
## Registry Schema
```

**Your Relevance Assessment:** [ ]

---

### Result 2

**Document ID:** `.claude/agents/agent-architect.md:chunk:5`

**Similarity Score:** 0.6892

**Full Document Content:**

```
### 2. Cataloguing
Maintain the registry at `.claude/registry/agents.md`:
- What agents exist and where
- Their purpose, domain, and tools
- Relationships and overlaps
- Creation dates and last modifications
- Usage patterns (when observable)
```

**Your Relevance Assessment:** [ ]

---

### Result 3

**Document ID:** `plugins/git-flow/skills/git-flow-master/subskills/registry-ops.md:chunk:8`

**Similarity Score:** 0.6590

**Full Document Content:**

```
1. **Create**: Automatically registers in registry
2. **Update**: `last_seen` updated on SessionStart
3. **PR Create**: `pr_url` stored in registry
4. **Merge**: Status changed to `merged`
5. **Cleanup**: Archives then marks `archived`

```

**Your Relevance Assessment:** [ ]

---

### Result 4

**Document ID:** `.claude/registry/agents.md:chunk:0`

**Similarity Score:** 0.6557

**Full Document Content:**

```
# Agent Registry
*Maintained by: agent-architect*
*Last updated: 2025-12-15*
## Overview
This ecosystem contains **7 custom agents**, **11 plugin personas**, and **5 built-in agents**. The architecture follows a pattern of specialized perspectives composed for multi-viewpoint analysis, with **operational agents** for process mapping and data validation, and **stewardship agents** for resource and artifact management.
```

**Your Relevance Assessment:** [ ]

---

### Result 5

**Document ID:** `plugins/git-flow/skills/git-flow-master/subskills/registry-ops.md:chunk:7`

**Similarity Score:** 0.6405

**Full Document Content:**

```
The registry enables:
- Finding which session created a branch
- Finding which branch a session uses
- Tracking session activity across restarts
## Staleness Detection
Sessions are marked stale when:
- `last_seen` timestamp > N days old
- Status is still `active`
The `cleanup` command:
1. Scans all active entries
2. Compares `last_seen` to current time
3. Marks old entries as `stale`
4. Does NOT delete anything (just marks)
## Integration With Worktree Operations
When using worktree tools:
```

**Your Relevance Assessment:** [ ]

---

## Query 4

**Full Query Text:**
> Instances should not update their own summaries, it should be done automatically using hooks. Can you do this using headless claude?

### Result 1

**Document ID:** `plugins/interface/skills/interface-master/subskills/claude-code.md:chunk:6`

**Similarity Score:** 0.6704

**Full Document Content:**

```
### Edit Tool
- Performs string replacement
- `old_string` must be unique in file
- `replace_all` for multiple occurrences
## Context Management
Claude Code maintains context through:
1. **Conversation history**: All messages in session
2. **CLAUDE.md files**: Project instructions loaded automatically
3. **Tool results**: Output from tool invocations
4. **Summarization**: Automatic context compression for long sessions
```

**Your Relevance Assessment:** [ ]

---

### Result 2

**Document ID:** `plugins/statusline/skills/statusline-master/subskills/generation-tuner.md:chunk:13`

**Similarity Score:** 0.6662

**Full Document Content:**

```
**After** (improved prompt):
```
CRITICAL RULES:
- NEVER use "Claude" or "Assistant" as the name
- NEVER use the exact command name (e.g., don't output "Status" for "/status")
- For minimal prompts like "Hello" or "Test", use evocative names like "Companion", "Explorer"
```
**Results**:
| Prompt | Before | After |
|--------|--------|-------|
| "Hello" | "Claude-{id}" | "Companion" |
| "/status" | "Status" | "Pulse Monitor" |
| "Can you version control?" | "Claude-{id}" | "Checkpoint" |
### Summary Generator
```

**Your Relevance Assessment:** [ ]

---

### Result 3

**Document ID:** `plugins/statusline/skills/statusline-master/subskills/generation-tuner.md:chunk:14`

**Similarity Score:** 0.6627

**Full Document Content:**

```
| Issue | Symptom | Fix |
|-------|---------|-----|
| Third person | "Claude is working on..." | Emphasize first-person in prompt |
| Too vague | "Working on things" | Ask for specific details |
| Repetitive | Same summary every time | Include prev_summaries for variety |
### Description Generator
```

**Your Relevance Assessment:** [ ]

---

### Result 4

**Document ID:** `plugins/temporal/.claude-plugin/plugin.json:chunk:0`

**Similarity Score:** 0.6603

**Full Document Content:**

```
{
  "name": "temporal",
  "version": "1.0.0",
  "description": "Injects timestamps into Claude's context at every hook event, providing continuous temporal awareness throughout conversations.",
  "author": {
    "name": "linuxiscool"
  },
  "keywords": ["time", "timestamp", "temporal", "awareness", "hooks", "context"],
  "agents": ["./agents/chronologist.md"],
  "hooks": {
```

**Your Relevance Assessment:** [ ]

---

### Result 5

**Document ID:** `.claude/registry/processes.md:chunk:55`

**Similarity Score:** 0.6564

**Full Document Content:**

```
│                   .claude/journal/YYYY/MM/DD/YYYY-MM-DD.md       │
│                             │                                    │
│                             ▼                                    │
│                   MONTHLY/YEARLY PROPAGATION                     │
│                   Update parent summaries                        │
│                             │                                    │
│                             ▼                                    │
```

**Your Relevance Assessment:** [ ]

---

## Query 5

**Full Query Text:**
> OK awesome. I appreciate that. What's the system using now? Headless claude or API? And when does it get updated? For what hooks is it updated?

### Result 1

**Document ID:** `plugins/awareness/skills/awareness/subskills/guide-utilizer.md:chunk:1`

**Similarity Score:** 0.7073

**Full Document Content:**

```
The claude-code-guide subagent has access to official documentation about:
1. **Claude Code (CLI)** - Features, hooks, slash commands, MCP servers, settings, IDE integrations, keyboard shortcuts
2. **Claude Agent SDK** - Building custom agents programmatically
3. **Claude API** - API usage, tool use, Anthropic SDK usage
## Query Formulation Principles
### Be Specific, Not Vague
```markdown
# Weak query
"Tell me about hooks"
```

**Your Relevance Assessment:** [ ]

---

### Result 2

**Document ID:** `plugins/interface/skills/interface-master/subskills/claude-code.md:chunk:1`

**Similarity Score:** 0.6969

**Full Document Content:**

```
Claude Code is Anthropic's official CLI for Claude. It provides:
- Interactive conversation with Claude models
- Tool access (Bash, Read, Write, Edit, Glob, Grep, etc.)
- Plugin system for extensibility
- Sub-agent spawning for parallel work
- MCP (Model Context Protocol) server integration
## How Claude Code Interfaces
### Input
- Receives text from terminal stdin
- Parses slash commands (`/help`, `/clear`, etc.)
- Interprets tool invocations from Claude's responses
```

**Your Relevance Assessment:** [ ]

---

### Result 3

**Document ID:** `plugins/interface/skills/interface-master/subskills/claude-code.md:chunk:0`

**Similarity Score:** 0.6898

**Full Document Content:**

```
---
name: claude-code
description: Understanding Claude Code CLI - the entry point of the interface stack. Tool behavior, context management, terminal interaction patterns.
allowed-tools: Read, Bash, Glob, Grep
---
# Claude Code Layer
Claude Code is the topmost layer of the interface stack - where user intent enters the system.
## What Claude Code Is
```

**Your Relevance Assessment:** [ ]

---

### Result 4

**Document ID:** `.claude/README.md:chunk:0`

**Similarity Score:** 0.6618

**Full Document Content:**

```
# Ecosystem Orientation
*For any Claude session beginning work in this repository*
## What Is This?
A **plugin marketplace for Claude Code** that has evolved into a self-aware multi-agent ecosystem. The repository contains plugins, but more importantly, it contains the infrastructure for an emergent cognitive architecture.
## The 30-Second Context
```

**Your Relevance Assessment:** [ ]

---

### Result 5

**Document ID:** `plugins/messages/skills/messages-master/subskills/cli-usage.md:chunk:5`

**Similarity Score:** 0.6594

**Full Document Content:**

```
[2025-12-12 02:38:43] claude-code | AssistantResponse
  Claude: ## Assessment: Awareness Plugin Progress...
  Score: 1.83 | ID: msg_9ai9WVToeR1AgkKTVC...
Found 15 results.
```
### Recent Messages
```bash
# Default (20 recent)
bun plugins/messages/src/cli.ts recent
# With limit
bun plugins/messages/src/cli.ts recent -l 10
# Filter by platform
bun plugins/messages/src/cli.ts recent -p claude-code -l 5
```
```

**Your Relevance Assessment:** [ ]

---

