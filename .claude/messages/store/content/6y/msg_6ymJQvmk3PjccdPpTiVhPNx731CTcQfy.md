---
id: msg_6ymJQvmk3PjccdPpTiVhPNx731CTcQfy
kind: 103
account_id: claude
created_at: 1765992311104
imported_at: 1766005522175
author_name: Claude
thread_id: cc_eee074d5
platform: claude-code
session_id: eee074d5-bf81-41eb-abca-12cb101e55ca
tags: [["event_type","AssistantResponse"]]
---

Looking at the available tools and skills, I can see plugins from `claude-plugins-official`. Here's what I can identify:

**From Skills/Commands:**
1. **frontend-design** - Create distinctive, production-grade frontend interfaces
2. **hookify** - Create hooks to prevent unwanted behaviors
3. **plugin-dev** - Plugin development guidance (agents, skills, hooks, commands, MCP)
4. **ralph-wiggum** - Ralph Wiggum looping technique
5. **feature-dev** - Guided feature development with code review, exploration, and architecture agents

**From MCP Tools:**
6. **greptile** - Code review, PR analysis, custom context management
7. **context7** - Up-to-date library documentation fetching
8. **serena** - Semantic code analysis with LSP-powered symbol navigation

That's **8 plugins** I can see from official sources. If you installed 9, there might be one that:
- Doesn't expose skills/commands/MCP tools visibly
- Had an installation issue
- Uses a different namespace

Would you like me to check the plugin cache directory or your Claude Code settings to verify all 9 are properly installed? I could run:

```bash
ls -la ~/.claude/plugins/cache/claude-plugins-official/
```

Or check the settings file to see the full plugin configuration.
