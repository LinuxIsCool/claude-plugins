---
id: msg_Gn9yKxrsuM9J2bma4FDrBEPJum1nA9kH
kind: 103
account_id: claude
created_at: 1765584457305
imported_at: 1766005509498
author_name: Claude
thread_id: cc_e8b5ca37
platform: claude-code
session_id: e8b5ca37-57c6-41f7-9eda-a84624f86bb4
tags: [["event_type","AssistantResponse"]]
---

Based on what's registered in my Skill tool, here are the available skills:

## Logging
| Skill | Purpose |
|-------|---------|
| `logging:log-search` | Search conversation history for past discussions, decisions, context |

## Scheduling
| Skill | Purpose |
|-------|---------|
| `schedule:web-scraper` | Playwright browser automation for JavaScript-heavy sites |
| `schedule:yoga-scheduler` | Plan yoga classes from studio schedules |

## Agent Frameworks (duplicated - appears twice)
| Skill | Purpose |
|-------|---------|
| `agents:letta` | MemGPT-style stateful agents with persistent self-editing memory |
| `agents:n8n` | Workflow automation with AI/LangChain nodes |
| `agents:pydantic-ai` | Type-safe Python agents with Pydantic validation |
| `agents:claude-agent-sdk-python` | Programmatically control Claude Code from Python |
| `agents:eliza` | ElizaOS multi-agent TypeScript framework |
| `agents:archon` | AI agent platform with RAG, MCP, multi-model orchestration |
| `agents:openai-agents-python` | OpenAI SDK for multi-agent workflows |
| `agents:langchain` | LLM apps with chains, agents, tools |
| `agents:lucid-agents` | Commerce SDK for AI agents with payments |
| `agents:anthropic-sdk-typescript` | Official TypeScript SDK for Claude API |
| `agents:agents` | Master the 91-agent marketplace architecture |
| `agents:a2a` | Agent2Agent protocol for cross-framework collaboration |
| `agents:mem0` | Self-improving memory layer with fact extraction |
| `agents:crewai` | Multi-agent orchestration with roles and tasks |
| `agents:adk-python` | Google's Agent Development Kit |
| `agents:openapi-specification` | API contracts for tool interfaces |

## LLM Tools & Knowledge
| Skill | Purpose |
|-------|---------|
| `llms:graphiti` | Temporally-aware knowledge graphs |
| `llms:pgvector-python` | Vector operations with Django, SQLAlchemy, etc. |
| `llms:falkordb` | Ultra-fast graph database for agent memory |
| `llms:anthropic-courses` | Official Anthropic educational courses |
| `llms:llama-cookbook` | Meta's Llama models guide |
| `llms:pgvector` | Vector similarity search in PostgreSQL |
| `llms:archon` | RAG pipelines with hybrid search |
| `llms:openai-cookbook` | OpenAI API patterns (80+ examples) |
| `llms:claude-cookbooks` | Claude API patterns (50+ examples) |

*Note: The system shows "45 of 84 skills" due to token limits - there are more available.*

## How Skills Work

Skills are invoked via the `Skill` tool. When I use one, it injects specialized knowledge/prompts into my context. For example, if you ask me to build something with CrewAI, I'd invoke `agents:crewai` to get the relevant documentation and patterns.

Would you like me to invoke a specific skill to demonstrate, or explore what a particular one provides?
