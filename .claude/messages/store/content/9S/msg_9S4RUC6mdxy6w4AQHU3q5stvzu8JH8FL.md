---
id: msg_9S4RUC6mdxy6w4AQHU3q5stvzu8JH8FL
kind: 103
account_id: claude
created_at: 1765584345359
imported_at: 1766005509373
author_name: Claude
thread_id: cc_0a8bf3f1
platform: claude-code
session_id: 0a8bf3f1-1bed-40e7-8abd-689400f702b9
tags: [["event_type","AssistantResponse"]]
---

That's expected! The `claude-code-guide` subagent is hardcoded in the system prompt to handle questions about Claude Code features:

> "When the user directly asks about... how to use a specific Claude Code feature (eg. implement a hook)... Use the Task tool with subagent_type='claude-code-guide'"

The `awareness:awareness` skill serves a different purpose - meta-learning and creation, not direct feature questions.

## Better Test Prompts

Try prompts that match the awareness skill's description but not claude-code-guide:

| Prompt | Should Match |
|--------|--------------|
| "Help me create a new skill for code review" | awareness → skill-creator |
| "Build a knowledge graph from my conversation logs" | awareness → temporal-kg-memory |
| "I want to systematically improve my Claude Code mastery" | awareness → techniques |
| "Study how the logging plugin is implemented" | awareness → plugin-studier |

## The Real Test

The real value is **character budget savings**. Before your restart:
- Did you see `awareness:*` skills in the truncated list?
- How many skills showed vs total? (was it "Showing X of Y"?)

After the change, you should see:
- `awareness:awareness` instead of 8 separate awareness skills
- More room for other plugins' skills to appear

Can you check:
1. What skills appear in your new session's available_skills?
2. Is the truncation less severe?
