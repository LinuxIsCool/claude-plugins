# Statusline Plugin Roadmap

This document outlines the strategic roadmap for evolving the statusline plugin from its current state to a robust, extensible, generalizable system.

## Current State Assessment

### Code Inventory (3,191 lines total)

| Component | Lines | Purpose | Health |
|-----------|-------|---------|--------|
| `lib/claude_backend.py` | 706 | Shared library for Python hooks | Bloated, needs review |
| `tools/statusline.sh` | 404 | Main statusline renderer | Growing, self-healing added |
| `tools/registry.py` | 286 | Registry management CLI | Functional |
| `tools/test-prompts.py` | 277 | Prompt testing utility | Needs update |
| `hooks/auto-name.py` | 217 | Name generation | Working |
| `hooks/user-prompt-submit.sh` | 197 | Prompt counter, session ensure | Working |
| `hooks/auto-description.py` | 190 | Description generation | Working |
| `hooks/auto-summary.py` | 173 | Summary generation | Working |
| `tools/history.sh` | 172 | History viewer (NEW) | Clean |
| `hooks/session-start.sh` | 168 | Session registration | Working |
| Prompt files | 158 | name.txt, description.txt, summary.txt | Needs redesign |
| Wrappers + misc | ~243 | Various small files | Functional |

### What's Working Well

1. **Logging infrastructure** - Complete JSONL logging of all events
2. **Self-healing** - Statusline auto-registers missing sessions/data
3. **History viewer** - Can replay and analyze past statuslines
4. **Semantic triplet** - Name/Description/Summary structure is sound

### What's Fragile

1. **Race conditions** - Multiple scripts write to registry.json (potential conflicts)
2. **Duplicated logic** - `log_statusline()` function defined in 3 shell scripts
3. **Large files** - `claude_backend.py` (706 lines) does too much
4. **Hardcoded paths** - Assumes `~/.claude/instances/` everywhere
5. **Prompt coupling** - Prompts may reference specific project context
6. **No configuration** - No way to customize behavior without editing code

---

## Phase 2: Architectural Review

**Goal**: Systematic understanding before refactoring

### 2.1 Code Review Checklist

| File | Review Focus | Status |
|------|--------------|--------|
| `claude_backend.py` | What can be extracted? Dead code? | [ ] |
| `statusline.sh` | Modular components? Error handling? | [ ] |
| `session-start.sh` | Overlap with statusline.sh auto-register? | [ ] |
| `user-prompt-submit.sh` | Overlap with session-start.sh? | [ ] |
| `auto-name.py` | Prompt loading, generation quality | [ ] |
| `auto-description.py` | Same as above | [ ] |
| `auto-summary.py` | Same as above | [ ] |
| `registry.py` | CLI interface quality | [ ] |

### 2.2 Data Flow Documentation

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Claude Code Runtime                          │
└─────────────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
   SessionStart         UserPromptSubmit         Stop
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ session-start.sh│  │ user-prompt-    │  │ auto-summary    │
│                 │  │ submit.sh       │  │ -wrapper.sh     │
│ • Register      │  │ • Increment cnt │  │                 │
│ • Assign C#     │  │ • Ensure session│  │ • Generate      │
│ • Init files    │  │ • Log prompt    │  │   summary       │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         │           ┌────────┴────────┐           │
         │           │                 │           │
         │           ▼                 ▼           │
         │    ┌─────────────┐  ┌─────────────┐    │
         │    │ auto-name   │  │ auto-desc   │    │
         │    │ -wrapper.sh │  │ -wrapper.sh │    │
         │    └──────┬──────┘  └──────┬──────┘    │
         │           │                 │           │
         │           ▼                 ▼           │
         │    ┌─────────────┐  ┌─────────────┐    │
         │    │ auto-name.py│  │ auto-desc.py│    │
         │    └──────┬──────┘  └──────┬──────┘    │
         │           │                 │           │
         ▼           ▼                 ▼           ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ~/.claude/instances/                              │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │
│  │registry.json │ │ counts/      │ │ summaries/   │ │descriptions│ │
│  │              │ │ {sid}.txt    │ │ {sid}.txt    │ │ /{sid}.txt │ │
│  └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘ │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │ statusline.jsonl (append-only log)                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
         │
         ▼ (Statusline command reads all data)
┌─────────────────────────────────────────────────────────────────────┐
│                      statusline.sh                                  │
│  • Receives JSON from Claude Code                                   │
│  • Reads registry, counts, summaries, descriptions                  │
│  • Auto-registers if missing (self-healing)                         │
│  • Renders formatted output                                         │
│  • Logs claude_input + statusline_render                            │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.3 Identified Fragility Points

| Issue | Location | Risk | Fix Priority |
|-------|----------|------|--------------|
| Registry race conditions | Multiple writers | Data corruption | High |
| Duplicated log function | 3 shell scripts | Maintenance burden | Medium |
| No atomic file writes | registry.json updates | Partial writes | High |
| PATH assumptions | All shell scripts | Portability | Medium |
| No error recovery | All hooks | Silent failures | High |

---

## Phase 3: Refactoring for Robustness

**Goal**: Small, simple, reliable code

### 3.1 Consolidate Shared Code

**Current**: `log_statusline()` defined in 3 places
**Target**: Single `lib/statusline-utils.sh` sourced by all

```bash
# lib/statusline-utils.sh
STATUSLINE_LOG="$HOME/.claude/instances/statusline.jsonl"

log_statusline() {
    local type="$1" session="$2" value="$3" ok="${4:-true}"
    local ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local short_session="${session:0:8}"
    mkdir -p "$(dirname "$STATUSLINE_LOG")"
    echo "{\"ts\":\"$ts\",\"session\":\"$short_session\",\"type\":\"$type\",\"value\":\"$value\",\"ok\":$ok}" >> "$STATUSLINE_LOG"
}
```

### 3.2 Atomic Registry Updates

**Current**: `jq ... > file.tmp && mv file.tmp file`
**Target**: Use flock for atomic operations

```bash
update_registry() {
    local registry="$1"
    local jq_filter="$2"
    (
        flock -x 200
        jq "$jq_filter" "$registry" > "$registry.tmp" && mv "$registry.tmp" "$registry"
    ) 200>"$registry.lock"
}
```

### 3.3 Configuration Layer

**Target**: `~/.claude/statusline.conf` or plugin settings

```yaml
# Configuration options
instances_dir: ~/.claude/instances
log_file: statusline.jsonl
default_name: Claude
features:
  git_stats: true
  git_history: false  # Future feature
  duration: true
```

### 3.4 Reduce claude_backend.py

**Current**: 706 lines doing too much
**Target**: Split into focused modules

```
lib/
├── __init__.py
├── conversation.py    # Conversation reading/parsing
├── generation.py      # LLM generation utilities
├── registry.py        # Registry read/write
├── logging.py         # JSONL logging
└── prompts.py         # Prompt loading/templating
```

---

## Phase 4: Extensibility Architecture

**Goal**: Easy to add new statusline features

### 4.1 Component System

Each statusline element becomes a "component" that can be enabled/disabled:

```
components/
├── identity.sh      # [Name:id]
├── model.sh         # Opus 4.5
├── context.sh       # ctx:N%
├── cost.sh          # $X.XX
├── session.sh       # C#:A#N
├── duration.sh      # Xh Ym
├── git-branch.sh    # branch +X/-Y
├── git-history.sh   # (future) last 3 commits
└── custom/          # User-defined components
```

### 4.2 Component Interface

Each component:
1. Receives statusline JSON via stdin
2. Outputs formatted segment
3. Logs own data
4. Handles own errors gracefully

```bash
# components/git-branch.sh
#!/bin/bash
source lib/component-base.sh

render() {
    local branch=$(git branch --show-current 2>/dev/null)
    [ -z "$branch" ] && return 0  # Graceful skip if no git

    local dirty=""
    [ -n "$(git status --porcelain 2>/dev/null)" ] && dirty="yes"

    local stats=$(get_git_stats)

    if [ "$dirty" = "yes" ]; then
        echo -e "${BOLD}${RED}${branch}${RST} ${DIM}${stats}${RST}"
    else
        echo -e "${BOLD}${BLUE}${branch}${RST} ${DIM}${stats}${RST}"
    fi
}

render
```

### 4.3 Future Feature: Git History Line

```bash
# components/git-history.sh
render() {
    local commits=$(git log --oneline -3 2>/dev/null | head -3)
    [ -z "$commits" ] && return 0

    echo "$commits" | while read hash msg; do
        echo -e "${DIM}${hash:0:7}${RST} ${msg:0:40}"
    done
}
```

### 4.4 Statusline Composer

Main script becomes a composer that:
1. Reads configuration
2. Loads enabled components
3. Arranges output (line 1, line 2, etc.)
4. Handles separators and formatting

---

## Phase 5: Prompt Engineering Framework

**Goal**: Systematic approach to prompt quality

### 5.1 Prompt Structure

```
prompts/
├── templates/
│   ├── name.md          # Template with placeholders
│   ├── description.md
│   └── summary.md
├── examples/
│   ├── name-examples.yaml      # User-approved examples
│   ├── description-examples.yaml
│   └── summary-examples.yaml
├── constraints/
│   └── format-rules.yaml       # ONE WORD, TWO WORDS, etc.
└── tests/
    └── prompt-test-cases.yaml  # Expected outputs for inputs
```

### 5.2 Example-Driven Generation

```yaml
# examples/name-examples.yaml
# User-approved names with context
examples:
  - context: "Working on authentication system"
    good: ["Auth", "Guardian", "Keymaster", "Access"]
    bad: ["AuthenticationSystemBuilder", "Security Expert", "The Authenticator"]

  - context: "Refactoring database queries"
    good: ["Query", "Schema", "Index", "Tables"]
    bad: ["DatabaseQueryRefactorer", "SQL Master"]

  - context: "Debugging race conditions"
    good: ["Race", "Sync", "Thread", "Lock"]
    bad: ["ConcurrencyDebugger", "Race Condition Fixer"]

principles:
  - ONE WORD only
  - Metaphorical/symbolic preferred over literal
  - Relates to the *essence* of the work, not the specific task
  - Should be memorable and pronounceable
```

### 5.3 Prompt Testing Framework

```python
# test-prompts.py improvements
def test_name_generation():
    """Test name prompt against known scenarios."""
    test_cases = load_yaml("prompts/tests/name-test-cases.yaml")

    for case in test_cases:
        result = generate_name(case.conversation_context)

        # Check format constraints
        assert len(result.split()) == 1, "Name must be ONE WORD"
        assert len(result) <= 15, "Name too long"

        # Check quality (if examples provided)
        if case.expected_category:
            assert result in case.acceptable_names
```

### 5.4 Prompt Iteration Process

```
1. Collect logged outputs
   └── grep 'type":"name"' statusline.jsonl

2. Analyze quality
   └── Which names were good? Which were bad?

3. Update examples
   └── Add good examples to examples/*.yaml
   └── Add bad examples as negative examples

4. Refine prompt template
   └── Adjust wording, add constraints

5. Test against historical data
   └── Run test-prompts.py with real conversations

6. Deploy and monitor
   └── Watch new logs for quality
```

---

## Phase 6: Generalization & Standalone

**Goal**: Plugin works anywhere, for anyone

### 6.1 Remove Repository Coupling

| Current | Generalized |
|---------|-------------|
| Hardcoded project paths | Use `$CLAUDE_PROJECT_DIR` or cwd |
| Prompts reference specific context | Generic prompts with examples |
| Assumes specific directory structure | Graceful fallbacks |

### 6.2 Cross-Platform Compatibility

| Issue | Solution |
|-------|----------|
| `$HOME` on Windows | Use `$USERPROFILE` fallback |
| `date` command differences | Use portable date formats |
| `jq` dependency | Document requirement, graceful error |
| Path separators | Use portable path handling |

### 6.3 Installation & Configuration

```bash
# Installation
claude plugins install statusline

# Or from source
git clone https://github.com/user/claude-statusline
cd claude-statusline
./install.sh

# Configuration
claude statusline configure
# Interactive setup wizard
```

### 6.4 Documentation Requirements

- [ ] README with clear purpose and screenshots
- [ ] Installation guide (multiple methods)
- [ ] Configuration reference
- [ ] Troubleshooting guide
- [ ] Contributing guide (for prompt examples)
- [ ] API documentation (for component development)

---

## Phase 7: Quality Assurance

**Goal**: Prove it works reliably

### 7.1 Test Scenarios

| Scenario | Expected Behavior | Test Method |
|----------|-------------------|-------------|
| New session | Shows `[Claude:xxxxx]`, `C##`, `Awaiting instructions.` | Manual |
| Continued session | Preserves name, updates summary | Manual |
| Context compaction | Agent session increments | Log analysis |
| No git repository | Git components hidden | Automated |
| Missing jq | Graceful error message | Automated |
| Concurrent sessions | No registry corruption | Stress test |

### 7.2 Log Analysis Queries

```bash
# Quality of names over time
jq -r 'select(.type=="name") | .value' statusline.jsonl | sort | uniq -c | sort -rn

# Sessions with issues (no process number)
jq -r 'select(.type=="statusline_render" and .value.process_num=="?")' statusline.jsonl

# Average context % at summary updates
jq -r 'select(.type=="summary") | .session' statusline.jsonl | while read s; do
  grep "\"session\":\"$s\"" statusline.jsonl | grep statusline_render | tail -1 | jq '.value.context_pct'
done
```

### 7.3 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Race condition failures | 0 | Log analysis |
| "C?" appearances | 0 | Log analysis |
| Name quality (user approval) | >80% | Manual review |
| Description format compliance | 100% | Automated check |
| Startup time | <100ms | Timing |

---

## Development Workflow

**Reference**: [[2025-12-18/12-36-plugin-update-mechanics-deep-dive]]

### The Cache Problem

Claude Code uses **copy-on-install** architecture:
- Plugin files are copied to `~/.claude/plugins/cache/{marketplace}/{plugin}/{version}/`
- Source file edits are invisible to running sessions
- No hot-reload mechanism exists for plugins
- Restart is required after changes (architectural constraint)

### Development Cycle

```
1. Edit source files
   └── plugins/statusline/hooks/*.py, *.sh

2. Clear cache
   └── /dev-tools:reload statusline
   └── OR: rm -rf ~/.claude/plugins/cache/linuxiscool-claude-plugins/statusline/

3. Restart Claude Code
   └── Exit current session, start new one

4. Verify changes took effect
   └── Check logs, test functionality
```

### Available Tools (dev-tools plugin)

| Tool | Purpose |
|------|---------|
| `hooks/cache_invalidator.py` | Auto-clears cache when plugin files change |
| `hooks/stale_cache_detector.py` | Warns at session start if cache is stale |
| `/dev-tools:reload <plugin>` | Manual cache clear |
| `/dev-tools:refresh <plugin>` | Clear + headless rebuild (updates all instances) |
| `tools/refresh-plugins.sh` | Shell script for external/CI use |

### Testing Changes

Before declaring a change "done":

1. **Clear cache**: `/dev-tools:reload statusline`
2. **Start fresh session**: New Claude Code instance
3. **Verify in logs**: `tail ~/.claude/instances/statusline.jsonl`
4. **Test edge cases**: New session, continued session, compaction

### Cache Location Reference

```
~/.claude/plugins/cache/linuxiscool-claude-plugins/statusline/
├── 0.4.0/           # Version directory (copied files live here)
│   ├── hooks/
│   ├── tools/
│   ├── lib/
│   └── ...
└── current -> 0.4.0  # Symlink to active version
```

---

## Implementation Priority

### Immediate (This Week)
1. Consolidate `log_statusline()` function
2. Add flock for atomic registry updates
3. Document current prompts

### Short Term (Next 2 Weeks)
1. Split `claude_backend.py` into modules
2. Create prompt examples files
3. Add prompt testing framework

### Medium Term (Next Month)
1. Implement component architecture
2. Add configuration layer
3. Cross-platform testing

### Long Term (Next Quarter)
1. Full generalization
2. Public release preparation
3. Community prompt examples

---

## Open Questions

1. **Component discovery**: How do users add custom components?
2. **Prompt sharing**: How do we share good prompt examples across users?
3. **Versioning**: How do we handle prompt/config version migrations?
4. **Multi-machine sync**: Should registry sync across machines?
5. **Privacy**: What data is safe to log/share for prompt improvement?

---

## Notes

- Use `/feature-dev` command for implementation work
- Consult `plugin-dev` plugin for architecture decisions
- Test on fresh machines before declaring "done"
- Get user approval on example lists before finalizing prompts
- Document every decision for future sessions

*Last updated: 2025-12-18*
