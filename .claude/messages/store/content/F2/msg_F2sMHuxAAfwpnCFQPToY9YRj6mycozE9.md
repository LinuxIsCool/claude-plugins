---
id: msg_F2sMHuxAAfwpnCFQPToY9YRj6mycozE9
kind: 103
account_id: claude
created_at: 1765992577066
imported_at: 1766005522212
author_name: Claude
thread_id: cc_eee074d5
platform: claude-code
session_id: eee074d5-bf81-41eb-abca-12cb101e55ca
tags: [["event_type","AssistantResponse"]]
---

Now I have all the details. Here's a comprehensive breakdown of all **10 official Claude plugins**:

---

## 1. Code Review (`code-review`)

**Type:** Command  
**Author:** Anthropic

**What it does:** Automated PR review using parallel specialized agents with confidence-based filtering.

**How it works:**
1. Gathers CLAUDE.md guideline files from your repo
2. Launches **4 parallel agents** for independent review:
   - Agents #1 & #2: CLAUDE.md compliance auditors
   - Agent #3: Bug scanner (changes only)
   - Agent #4: Git blame/history context analyzer
3. Scores each issue 0-100 for confidence
4. Only reports issues ≥80 confidence (filters false positives)

**Usage:**
```bash
/code-review
```

---

## 2. Context7 (`context7`)

**Type:** MCP Server (HTTP)  
**Author:** Upstash

**What it does:** Fetches **up-to-date documentation** for any library directly from source repositories.

**How it works:** Connects to Upstash's Context7 API to pull version-specific docs and code examples into your context.

**Tools exposed:**
- `resolve-library-id` - Find library IDs (e.g., `/vercel/next.js`)
- `get-library-docs` - Fetch documentation by topic

**Usage:**
```
"Get React hooks documentation"
"How does Next.js routing work in v14?"
```

---

## 3. Explanatory Output Style (`explanatory-output-style`)

**Type:** SessionStart Hook  
**Author:** Anthropic

**What it does:** Recreates the deprecated "Explanatory" output style. Encourages educational insights about implementation choices.

**How it works:** A SessionStart hook injects instructions at every session start, producing:

```
★ Insight ─────────────────────────────────────
[2-3 key educational points]
─────────────────────────────────────────────────
```

**Currently active in this session!**

`★ Insight ─────────────────────────────────────`
This plugin demonstrates **hooks-only architecture** - no skills, commands, or MCP servers. Just behavior modification via event hooks. The pattern is useful when you want to augment Claude's behavior without requiring explicit invocation.
`─────────────────────────────────────────────────`

---

## 4. Feature Development (`feature-dev`)

**Type:** Command + Agents  
**Author:** Sid Bidasaria (Anthropic)

**What it does:** A **7-phase structured workflow** for building features properly:

| Phase | Purpose |
|-------|---------|
| 1. Discovery | Understand requirements, clarify ambiguities |
| 2. Codebase Exploration | Launch 2-3 `code-explorer` agents in parallel |
| 3. Clarifying Questions | Fill in all gaps before designing |
| 4. Architecture Design | 2-3 `code-architect` agents propose approaches |
| 5. Implementation | Build following chosen architecture |
| 6. Quality Review | 3 `code-reviewer` agents (DRY, bugs, conventions) |
| 7. Summary | Document what was built |

**Agents included:**
- `feature-dev:code-explorer` - Traces execution paths, maps architecture
- `feature-dev:code-architect` - Designs implementation blueprints
- `feature-dev:code-reviewer` - Reviews for bugs/quality (≥80 confidence filter)

**Usage:**
```bash
/feature-dev Add user authentication with OAuth
```

---

## 5. Frontend Design (`frontend-design`)

**Type:** Skill  
**Author:** Prithvi Rajasekaran & Alexander Bricken (Anthropic)

**What it does:** Generates **distinctive, production-grade UI** that avoids generic AI aesthetics.

**Features:**
- Bold aesthetic choices
- Distinctive typography and color palettes
- High-impact animations
- Context-aware implementation

**Usage:**
```
"Create a dashboard for a music streaming app"
"Build a landing page for an AI security startup"
```

**Learn more:** [Frontend Aesthetics Cookbook](https://github.com/anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb)

---

## 6. Greptile (`greptile`)

**Type:** MCP Server (HTTP)  
**Author:** Greptile

**What it does:** AI-powered codebase search and PR analysis. Query repositories using natural language.

**Tools exposed:**
- `list_pull_requests` / `list_merge_requests` - Browse PRs
- `get_merge_request` - Get PR details with review analysis
- `list_merge_request_comments` - View comments including Greptile's
- `trigger_code_review` - Start a Greptile code review
- `search_greptile_comments` - Find patterns in review feedback
- `list_custom_context` / `create_custom_context` - Manage coding patterns
- `list_code_reviews` - Browse past reviews

**Requires:** `GREPTILE_API_KEY` environment variable

---

## 7. Hookify (`hookify`)

**Type:** Skill + Commands  
**Author:** Anthropic

**What it does:** Create custom hooks to **prevent unwanted behaviors** without editing `hooks.json`.

**Features:**
- Analyze conversations to find behaviors automatically
- Simple markdown configuration files
- Regex pattern matching
- No restart needed - rules take effect immediately

**Commands:**
```bash
/hookify Warn me when I use rm -rf commands  # Create rule
/hookify                                      # Analyze conversation for issues
/hookify:list                                 # List all rules
/hookify:configure                            # Enable/disable interactively
```

**Rule actions:**
- `warn` - Shows warning but allows operation
- `block` - Prevents operation entirely

---

## 8. Plugin Development (`plugin-dev`)

**Type:** Skills + Command  
**Author:** Daisy Hollman (Anthropic)

**What it does:** Comprehensive toolkit for building Claude Code plugins.

**7 Skills:**
1. **Hook Development** - PreToolUse, PostToolUse, Stop, SessionStart hooks
2. **MCP Integration** - stdio, SSE, HTTP, WebSocket server configs
3. **Plugin Structure** - Manifest, directory layout, auto-discovery
4. **Plugin Settings** - `.local.md` configuration patterns
5. **Command Development** - Slash commands with frontmatter
6. **Agent Development** - Autonomous agents with AI-assisted generation
7. **Skill Development** - Progressive disclosure, strong triggers

**Guided workflow:**
```bash
/plugin-dev:create-plugin A plugin for managing database migrations
```

---

## 9. Ralph Wiggum (`ralph-wiggum`)

**Type:** Command + Stop Hook  
**Author:** Based on Geoffrey Huntley's technique

**What it does:** Implements **iterative, self-referential development loops**. Named after Ralph Wiggum from The Simpsons.

**How it works:**
1. You run `/ralph-loop` with a prompt
2. Claude works on the task
3. When Claude tries to exit, the Stop hook blocks it
4. The **same prompt is fed back** automatically
5. Repeat until completion promise is found

**Usage:**
```bash
/ralph-loop "Build a REST API for todos. Output <promise>COMPLETE</promise> when done." --completion-promise "COMPLETE" --max-iterations 50
```

**Philosophy:**
- Iteration > Perfection
- Failures are data
- Persistence wins

**Real results:** One $50k contract completed for $297 in API costs!

---

## 10. Serena (`serena`)

**Type:** MCP Server (stdio via `uvx`)  
**Author:** Oraios

**What it does:** **Semantic code analysis** via Language Server Protocol (LSP) integration.

**Tools exposed:**
- `find_symbol` - Locate symbols by name path pattern
- `find_referencing_symbols` - Find references to a symbol
- `get_symbols_overview` - High-level file symbol overview
- `replace_symbol_body` - Replace symbol definitions
- `insert_before_symbol` / `insert_after_symbol` - Add code at symbol boundaries
- `rename_symbol` - Rename across entire codebase
- `search_for_pattern` - Regex search with context
- `read_file` / `create_text_file` / `replace_content` - File operations
- `execute_shell_command` - Run shell commands
- Memory tools (`write_memory`, `read_memory`, `list_memories`)
- `activate_project` - Switch between registered projects

`★ Insight ─────────────────────────────────────`
Serena is particularly powerful because it uses **LSP-backed symbol navigation** rather than regex. This means it understands code structure semantically - you can rename a method and it will update all references correctly, even across different files. The `find_symbol` with `include_body=True` is more efficient than reading entire files.
`─────────────────────────────────────────────────`

---

## Summary Table

| Plugin | Type | Primary Use Case |
|--------|------|------------------|
| **code-review** | Command | Automated PR review |
| **context7** | MCP | Library documentation lookup |
| **explanatory-output-style** | Hook | Educational insights mode |
| **feature-dev** | Command+Agents | Structured feature development |
| **frontend-design** | Skill | Production-grade UI generation |
| **greptile** | MCP | Codebase search & PR analysis |
| **hookify** | Skill+Commands | Custom behavior prevention |
| **plugin-dev** | Skills+Command | Plugin development toolkit |
| **ralph-wiggum** | Command+Hook | Iterative self-improvement loops |
| **serena** | MCP | LSP-powered semantic code analysis |
