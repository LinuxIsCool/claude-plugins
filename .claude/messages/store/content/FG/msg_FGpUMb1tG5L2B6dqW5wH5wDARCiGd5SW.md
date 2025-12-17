---
id: msg_FGpUMb1tG5L2B6dqW5wH5wDARCiGd5SW
kind: 103
account_id: claude
created_at: 1765674919894
imported_at: 1766005510732
author_name: Claude
thread_id: cc_05038dd8
platform: claude-code
session_id: 05038dd8-d486-4cd4-bf86-b4c6b896d9d3
tags: [["event_type","AssistantResponse"]]
---

I've created three backlog tasks. Now let me give you the complete picture.

---

## Summary: How to Maintain AgentNet

### Answer to Your Core Questions

**Should you use the backlog?**
Yes. I just created three tasks:
- `task-3`: Fix TUI Navigation (HIGH - the bugs you found)
- `task-4`: QA Checklist & Testing Infrastructure (HIGH)
- `task-5`: Create Missing Agent Types (MEDIUM)

**Do you have dedicated engineering/design/testing agents?**
Not yet. agent-architect created a registry at `.claude/registry/agents.md` identifying **30+ missing agent types**:

| Category | Missing Agents | Priority |
|----------|----------------|----------|
| Testing | qa-engineer, tui-tester, test-strategist | **Critical** |
| Engineering | tui-specialist, frontend-engineer | High |
| Design | ux-designer, product-designer | Medium |
| Product | product-manager, tech-writer | Medium |

**How to find issues before users?**
1. **QA Checklist** - A 2-minute manual test catches 90% of TUI bugs
2. **Focus Guards** - Code change to prevent handler conflicts
3. **Screen Manager** - Architectural fix for navigation state

---

### The Bug Root Causes

**backend-architect diagnosed both issues:**

```
┌─────────────────────────────────────────────────────────────┐
│ BUG 1: ESC/Back Crash                                       │
│                                                             │
│ screen.destroy() → callback creates new screen              │
│                    ↑ Old event loop still unwinding         │
│                    └─ RACE CONDITION                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ BUG 2: Scroll Glitch with 'j'                              │
│                                                             │
│ Screen A: agent list  ─┬─ both register screen.key(['j'])  │
│ Screen B: profile     ─┘                                    │
│                         ↓                                   │
│                    BOTH HANDLERS FIRE                       │
└─────────────────────────────────────────────────────────────┘
```

**Fix**: Single `ScreenManager` that owns all input, with explicit cleanup on navigation.

---

### Recommended Development Process

From **process-cartographer**:

```
Code Change → Manual Test → QA Checklist → Release
     ↑                           │
     └─── Fix Issues ←───────────┘
```

**Rhythm:**
- **Daily**: Manual test after changes
- **Per-release**: Run full QA checklist
- **Weekly**: Review backlog issues

---

### Meta-Insight from systems-thinker

> "AgentNet could coordinate its own development. The system is already bootstrapping itself."

The agents just used AgentNet's data structures to analyze AgentNet's bugs. The feedback loop is forming.

---

### Immediate Next Steps

| Priority | Action | Owner |
|----------|--------|-------|
| 1 | Fix navigation bugs (task-3) | Engineering |
| 2 | Create QA.md checklist (task-4) | Process |
| 3 | Create qa-engineer agent (task-5) | Meta |

Want me to start fixing the navigation bugs now? Or create the QA checklist first so we can validate the fixes?
