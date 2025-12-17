---
id: msg_GBxMKNdpmvvmUT7vTba4HSSrVw2mfHSn
kind: 103
account_id: claude
created_at: 1765583355293
imported_at: 1766005509346
author_name: Claude
thread_id: cc_0a8bf3f1
platform: claude-code
session_id: 0a8bf3f1-1bed-40e7-8abd-689400f702b9
tags: [["event_type","AssistantResponse"]]
---

## Investigation Complete - Here's What I Found

### The Root Cause: 15,000 Character Budget

Skills are **not in the system prompt** directly. They're in the **Skill tool's description** within the tools array. Claude Code enforces a **15,000 character budget** for the `<available_skills>` section.

### The Truncation Algorithm (Flawed)

According to [GitHub Issue #13343](https://github.com/anthropics/claude-code/issues/13343):

1. **Prioritizes by description length** - Longer descriptions get included first
2. **Penalizes concise writing** - Well-written short descriptions get truncated
3. **No semantic relevance** - Doesn't consider what's useful for the current task

Example from the issue:
```
526 chars - Hook Development       ✓ Included (verbose)
117 chars - jq                     ✗ Truncated (concise)
117 chars - yq                     ✗ Truncated (concise)
```

### Known Bugs (Two Related Issues)

| Issue | Problem |
|-------|---------|
| [#13343](https://github.com/anthropics/claude-code/issues/13343) | Skills truncated at ~30, remaining undiscoverable |
| [#13344](https://github.com/anthropics/claude-code/issues/13344) | Plugin enable/disable ignored - all skills load regardless |

### Why Your Awareness Skills Don't Show

Your awareness skills have **concise descriptions** (~150-200 chars), while agents/llms skills have **verbose descriptions** (~400-500 chars). The algorithm favors verbosity.

### No User Configuration Available

There's no environment variable or setting to:
- Change the 15,000 character budget
- Override the prioritization algorithm
- Force specific skills to appear

### Proposed Fixes (From GitHub)

1. **Raise the limit** - 84 skills at ~200 chars each = ~17k chars (close to limit)
2. **Smart truncation** - Prioritize by relevance to current prompt
3. **Minimal fallback** - Show just skill names for truncated skills so Claude knows they exist

### Workaround

Skills still **work when invoked by name** even if not displayed - as we proved with `awareness:docs-reader`.

---

**Sources:**
- [GitHub Issue #13343 - Skills truncated at 30](https://github.com/anthropics/claude-code/issues/13343)
- [GitHub Issue #13344 - Plugin enable/disable ignored](https://github.com/anthropics/claude-code/issues/13344)
- [Claude Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/) - 15,000 char budget detail
- [Tyler Folkman's Complete Guide to Claude Skills](https://tylerfolkman.substack.com/p/the-complete-guide-to-claude-skills)
