---
id: task-1.2
title: "Activate Librarian Agent"
status: "To Do"
priority: high
labels: [activation, agents]
milestone: v1.0-activation
parentTaskId: task-1
created: 2025-12-15
assignee: ["@claude"]
---

# Activate Librarian Agent

## Description

The Librarian agent is **fully defined** at `.claude/agents/librarian.md` but has never been actively invoked for cataloguing. This task activates the agent to begin resource acquisition.

### Current State

- **Agent definition**: Complete (129 lines, sonnet model)
- **Infrastructure**: `.claude/library/` directory populated with structure
- **Process**: Process 5 (Resource Acquisition) documented
- **Status**: DORMANT - structure exists but no active cataloguing

### Agent Responsibilities (from definition)

1. **Resource Capture** - Track every external resource accessed
2. **Cataloguing** - Maintain the resource index
3. **Deduplication** - Prevent redundant fetches
4. **Citation Management** - Track provenance
5. **Connection** - Link related resources

### Expected Outputs

```
.claude/library/
├── index.md                    # Master index with stats
├── urls/
│   ├── by-domain/              # github.com.md, arxiv.org.md, etc.
│   └── by-topic/               # Extracted topic clusters
├── papers/
│   └── {author-year-title}.md  # Academic papers
├── transcripts/
│   └── youtube/                # Video transcripts
├── datasets/
│   └── index.md                # API and dataset registry
└── .cache/                     # Raw content cache
```

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Invoke librarian agent via Task tool
- [ ] #2 Librarian scans existing .claude/logging/ for URLs fetched
- [ ] #3 Librarian creates/updates index.md with resource stats
- [ ] #4 Librarian catalogs at least 5 domains from historical sessions
- [ ] #5 Librarian demonstrates deduplication awareness
- [ ] #6 Update registry to show librarian as "Active"
<!-- AC:END -->

## Activation Steps

### Step 1: Invoke the Librarian
```
Use Task tool with:
- Load .claude/agents/librarian.md as system prompt context
- Prompt: "You are the Librarian. Begin cataloguing. Scan the session logs in .claude/logging/ to find all URLs that have been fetched. Create index entries for each unique domain."
```

### Step 2: Backfill Historical Resources
The librarian should scan JSONL logs for WebFetch tool calls and catalog:
- URLs accessed
- When they were accessed
- What session/topic context

### Step 3: Verify Outputs
- Check `.claude/library/index.md` updated
- Check domain files created in `urls/by-domain/`
- Verify no duplicate entries

### Step 4: Update Registry
Edit `.claude/registry/agents.md` to change librarian from dormant to active.

## Principle

From the librarian definition:
> "We shouldn't ever make the same web request twice unnecessarily."

Once activated, the librarian enables this principle by maintaining the resource cache.
