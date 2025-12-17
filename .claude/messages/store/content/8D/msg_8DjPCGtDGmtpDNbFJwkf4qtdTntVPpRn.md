---
id: msg_8DjPCGtDGmtpDNbFJwkf4qtdTntVPpRn
kind: 103
account_id: claude
created_at: 1765992387206
imported_at: 1766005522195
author_name: Claude
thread_id: cc_eee074d5
platform: claude-code
session_id: eee074d5-bf81-41eb-abca-12cb101e55ca
tags: [["event_type","AssistantResponse"]]
---

There are actually **10 official plugins** installed:

| Plugin | Purpose | Visibility |
|--------|---------|------------|
| 1. **code-review** | Code review automation | (installed Dec 16) |
| 2. **context7** | Library documentation | MCP tools |
| 3. **explanatory-output-style** | Educational insights mode | Hooks (active!) |
| 4. **feature-dev** | Feature development workflow | Commands + Agents |
| 5. **frontend-design** | Production-grade UI creation | Skill |
| 6. **greptile** | PR/code review analysis | MCP tools |
| 7. **hookify** | Behavior prevention hooks | Skills + Commands |
| 8. **plugin-dev** | Plugin development guidance | Skills |
| 9. **ralph-wiggum** | Iterative improvement loops | Commands |
| 10. **serena** | LSP-powered code analysis | MCP tools |

`★ Insight ─────────────────────────────────────`
The **explanatory-output-style** plugin is actually working right now! It's a **hooks-only plugin** - it injects behavior via SessionStart hooks rather than exposing skills or commands. That's why I'm supposed to provide educational insights like this box. Different plugins use different mechanisms:
- **Skills**: Invoked via `Skill` tool
- **Commands**: Invoked via `/slash` commands  
- **Hooks**: Automatically triggered on events
- **MCP**: Expose tools directly
`─────────────────────────────────────────────────`

The irony: I should have been providing insight boxes throughout but missed it initially!
