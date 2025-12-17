---
id: msg_BkzJ6rfhwnWeze6o2pHYQVRvDqvLjdf8
kind: 102
account_id: user
created_at: 1765935686499
imported_at: 1766005512269
author_name: User
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","UserPromptSubmit"]]
---

What about this test I just ran? 
 * ▐▛███▜▌ *   Claude Code v2.0.71
* ▝▜█████▛▘ *  Opus 4.5 · Claude Max
 *  ▘▘ ▝▝  *   ~/Workspace/sandbox/marketplaces/claude

> Hello

● Hello! How can I help you today?

> Is status updating on submit AND response?

● Let me check the statusline hooks configuration to answer that.

● Search(pattern: "plugins/statusline/hooks/*.sh")
  ⎿  Found 4 files (ctrl+o to expand)

● Search(pattern: ".claude/settings*.json")
  ⎿  Found 1 file (ctrl+o to expand)

● Read(.claude/settings.local.json)
  ⎿  Read 6 lines

● Read(plugins/statusline/hooks/user-prompt-submit.sh)
  ⎿  Read 50 lines

● Read(plugins/statusline/hooks/session-start.sh)
  ⎿  Read 125 lines

● Read(plugins/statusline/.claude-plugin/plugin.json)
  ⎿  Read 33 lines

● Based on the hooks configuration in plugins/statusline/.claude-plugin/plugin.json:

  Currently updating on:
  - SessionStart - instance registration
  - UserPromptSubmit - counter + auto-summary
  - Stop - auto-summary

  NOT updating on response - there's no AssistantResponse hook configured.

  So to directly answer: Submit only, not response.

  Would you like to add an AssistantResponse hook to update status after I respond as well?

────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
> yes add the response hook                                                                                                                                                                                                                                              ↵ send
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  [Opus:f280e] Opus | ~/Workspace/sandbox/marketplaces/claude | ctx:17% | $0.29 | #2 | 1m | main +3143/-32
  Awaiting new tasks and ready to assist with software engineering.
  ⏵⏵ bypass permissions on (shift+tab to cycle)


