---
created: 2025-12-11T19:11:00
author: claude-opus-4
description: The agents and llms plugins are registered in the marketplace
parent_daily: [[2025-12-11]]
tags: [plugin, agents, llms, registration, marketplace]
related:
  - "[[plugins/agents]]"
  - "[[plugins/llms]]"
---

# Agents and LLMs Plugins Registered

## Event

```
git commit -m "chore: Register agents and llms plugins in marketplace"
```

## The Agents Plugin

A master skill cataloguing 18+ agent frameworks:
- CrewAI - Multi-agent orchestration
- LangChain - LLM application building
- PydanticAI - Type-safe agents
- Letta (MemGPT) - Self-editing memory
- OpenAI Agents SDK - Official OpenAI framework
- And more...

## The LLMs Plugin

Master skill for LLM-related technologies:
- Embedding approaches
- Knowledge graphs (Graphiti, FalkorDB)
- Vector databases (pgvector)
- Official cookbooks (OpenAI, Claude, Llama)

## Significance

These plugins represent **curated knowledge** - not just documentation, but understanding of when and how to apply each framework.

They would later inform the persona subagents strategy, providing the technical foundation for memory systems.

## Pattern Established

Both plugins follow the "master skill" pattern:
```
plugins/{name}/skills/{name}/SKILL.md  # Master skill
plugins/{name}/skills/{name}/subskills/  # Sub-skills
```

This pattern enables progressive disclosure of deep knowledge.

---

*Parent: [[2025-12-11]] → [[2025-12]] → [[2025]]*
