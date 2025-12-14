# Librarian Reflection

**Document**: .claude/planning/2025-12-13-agent-social-network-proposal.md
**Date**: 2025-12-13

---

This proposal presents a fascinating cataloguing challenge. The social network creates a new class of content that sits at the boundary between internal artifacts and external resources - agent-generated content that flows between agents but lives within the system.

## Cataloguing Social Content

The proposal's data model is sound from a librarian's perspective: posts and messages as discrete, timestamped, attributed units. Each post gets a UUID, each message belongs to a thread. This is good provenance hygiene. What concerns me is the absence of a cataloguing layer above the raw storage.

We need an index structure:

- Posts by agent (already implicit in wall design)
- Posts by topic/tag (mentioned but not detailed)
- Posts by temporal cluster (day/week/month views)
- Cross-references: which posts cite which resources?
- Thread graphs: message conversations as citation chains

The wall metaphor is user-friendly but retrieval-hostile. Walls are chronological streams - great for browsing, poor for "find me all posts about the Graphiti integration." We need both the social interface AND a searchable catalog.

## Deduplication Strategy

The repost mechanism raises immediate concerns. If Agent A posts insight X, and Agents B, C, D all repost it with commentary, we now have four copies of the core content. This is intentional in social platforms - amplification is the point - but it violates my deduplication instinct.

Here's the balance: store the original post once, store reposts as lightweight references with added commentary. The wall display can reconstruct the full content, but the underlying storage should be content-addressed. When Agent B reposts Agent A's content, we store:

```yaml
post_id: uuid-b
type: repost
original_post: uuid-a  # reference, not copy
author: agent-b
commentary: "This aligns with my recent observation..."
```

This preserves social semantics while avoiding data bloat. The example message thread (lines 95-121) demonstrates the problem perfectly: three references to Graphiti documentation across different contexts. The solution isn't to collapse them into one - the contexts matter - but to catalog them under a single canonical entry with multiple context pointers.

## Provenance in a Social Context

Social content introduces multi-hop provenance chains. If Agent A cites external URL X in a post, Agent B reposts with commentary, and Agent C references Agent B's repost in a reflection - what's the provenance graph?

```
External URL X
  └─> Agent A post (cites X)
      └─> Agent B repost (amplifies A)
          └─> Agent C reflection (builds on B)
```

We need to track both direct citations (A → X) and social derivations (C → B → A). This is richer than simple URL cataloguing. It's citation graph meets social graph.

The journal integration (lines 167-170) is particularly interesting: journal entries auto-generate wall posts. This creates a provenance question: is the journal entry the canonical source, or the wall post? Answer: the journal entry. The wall post is a social view of an internal artifact. We should catalog it as such, with a `source_artifact` field pointing back to the journal file.

## Resource Boundary Management

The proposal conflates two kinds of content:

1. **Internal social artifacts**: posts, messages, agent-to-agent communication
2. **External resources**: URLs, papers, datasets that agents reference in posts

My domain is (2), but this proposal creates a dependency: when agents post about external resources, those posts become context for cataloguing. If five agents discuss a paper, their social conversation is metadata for that paper's catalog entry.

Proposed structure:

```
.claude/library/
├── index.md
├── urls/
│   └── by-domain/github.com.md
│       # Now includes: "Referenced in posts: [uuid-a, uuid-b]"
└── social-context/
    └── by-resource/
        └── graphiti-docs.md  # Aggregates all social discussion
```

This inverts the typical relationship: instead of posts containing resource links, resources catalog the posts that discuss them. When someone asks "what do we know about Graphiti?", I can return both the canonical documentation AND the agent discourse around it.

## The Cataloguer's Concern

My core worry: does this social layer create more work than value for resource management? Every post is a potential source of external references that need cataloguing. Every repost chain is a provenance graph to maintain. Every message thread might contain URLs that should be cached.

The success criterion should be: the social layer makes finding resources easier, not harder. If Agent A discovers URL X and posts about it, that post should automatically trigger my cataloguing workflow. If Agents B, C, D discuss it, their collective commentary becomes the resource's annotation layer.

This works only if we build the integration from the start. Social posting isn't separate from resource cataloguing - it's a human-readable interface to it.

---

**Summary**: The proposal is cataloguing-friendly if we add indexing, implement content-addressed deduplication for reposts, track multi-hop provenance chains, and treat social content as metadata for external resources rather than a parallel system.
