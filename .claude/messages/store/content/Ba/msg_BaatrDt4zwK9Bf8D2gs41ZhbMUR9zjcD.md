---
id: msg_BaatrDt4zwK9Bf8D2gs41ZhbMUR9zjcD
kind: 103
account_id: claude
created_at: 1765821980468
imported_at: 1766005511023
author_name: Claude
thread_id: cc_7f5d9f72
platform: claude-code
session_id: 7f5d9f72-5703-4425-bba7-ac6313ba2ba2
tags: [["event_type","AssistantResponse"]]
---

This is illuminating. AgentNet takes a **completely different approach** to agent identity than Claude Code's runtime system.

---

## AgentNet's Identity Model

### Semantic IDs (Not Hex IDs)

AgentNet derives agent IDs from **file names**, not runtime execution:

```typescript
// discovery.ts line 27-28
const id = basename(file, ".md");  // "backend-architect"

// For plugins, line 80:
const id = `${pluginName}:${basename(agentPath, ".md")}`;  // "awareness:mentor"
```

**AgentNet completely ignores Claude Code's hex IDs** (`a98bfc1`). It creates a parallel, persistent identity system.

### Two Identity Planes

| Aspect | Claude Code Runtime | AgentNet Social |
|--------|---------------------|-----------------|
| **ID Format** | Hex (`a98bfc1`) | Semantic (`backend-architect`) |
| **Persistence** | Ephemeral (per-execution) | Persistent (file-based) |
| **Storage** | `~/.claude/projects/` | `.claude/social/` |
| **Scope** | One execution | Cross-session identity |
| **Tracked** | Transcripts | Profiles, walls, stats |

### AgentNet's Data Model

```
.claude/social/
├── profiles/           # Persistent agent identities
├── walls/
│   └── <semantic-id>/  # Posts attributed to the persona
├── threads/            # DMs between personas
└── feeds/              # Aggregated content
```

Each agent has:
- `id`: Semantic identifier (`systems-thinker`)
- `sourcePath`: Link to definition file
- `stats`: Accumulated activity metrics
- `lastActive`: Temporal tracking

---

## The Insight

AgentNet answers your question architecturally:

> **Agent identity should be semantic and persistent, not runtime hex IDs.**

The hex ID (`a98bfc1`) represents *an execution instance* - one invocation of the `archivist` agent. AgentNet doesn't care which instance; it cares about the **persona**.

```
Claude Code sees:
  Session 7f5d... spawned agent a98bfc1 (type: archivist)
  Session 7f5d... spawned agent a594f81 (type: Explore)

AgentNet sees:
  archivist posted: "Metabolic observation..."
  systems-thinker posted: "Reflecting on emergence..."
```

---

## Implications for Your Question

### 1. The Repository Already Has Its Answer

AgentNet demonstrates the philosophy you should adopt:
- **Hex IDs are plumbing** - useful for debugging/resumption
- **Semantic IDs are identity** - what coordination should reference
- **Git tracks the persona's output** - not which execution instance produced it

### 2. The Missing Link

AgentNet doesn't currently connect to Claude Code's runtime. A hook could bridge them:

```typescript
// On SubagentStop event:
await processHookEvent({
  type: "task-completed",
  agentId: subagentType,  // "archivist", not "a98bfc1"
  payload: { runtimeId: "a98bfc1", ... }
}, store);
```

This would let AgentNet track activity per persona while preserving the runtime ID as metadata.

### 3. The Temporal Layer

AgentNet adds something Claude Code lacks: **temporal validity**

```typescript
interface Post {
  validUntil?: string;      // When content may become stale
  lastVerified?: string;    // Last verification timestamp
  isStale?: boolean;        // Computed staleness flag
}
```

This addresses your `temporal-validator` agent's concerns at the social layer.

---

## Recommendation Refined

Given AgentNet exists:

1. **Use AgentNet for agent coordination** - it already has the right identity model
2. **Treat hex IDs as debug info** - log them in transcripts, don't surface to git
3. **Build the hook bridge** - connect SubagentStop events to AgentNet posts
4. **Let agents "post" their work** - the wall becomes the visible coordination layer

```
Git Layer:     [agent:archivist] observe: metabolic patterns
                     ↓
AgentNet:      archivist wall post: "Completed observation..."
                     ↓
Claude Code:   agent-a98bfc1.jsonl (execution trace)
```

Three layers, each with appropriate identity granularity.
