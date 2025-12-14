# Temporal Validator Reflection

**Document**: .claude/planning/2025-12-13-agent-social-network-proposal.md
**Date**: 2025-12-13

---

The proposal presents a social layer for agent communication. My immediate concern: social content is among the most temporally volatile information types. Posts age. Messages become stale. Context drifts. Without explicit temporal validity tracking, this system will accumulate information debt rapidly.

## Observations on Temporal Validity

The Post data model includes `timestamp` but lacks `valid_until`, `last_verified`, or `staleness_indicator` fields. A post from 2025-12-13 about "current architecture decisions" will still appear as current in 2026-01-13, though its claims may have decayed significantly. The proposal conflates publication time with validity period.

Consider the example message thread: archivist notes "3 references to the same Graphiti documentation." This is a temporal claim. As of when? Still true today? The librarian's response commits to action. Was the action completed? When? The thread captures a moment but provides no mechanism to track whether its claims remain accurate.

## Staleness Detection Requirements

For posts, I would track:
- **Content staleness**: References to files, configurations, or states that have changed
- **Claim staleness**: Assertions that may have become false
- **Context staleness**: Posts that reference since-deleted or significantly-modified parent content

For messages, thread completion status matters. An unresolved question from 30 days ago signals either: (a) forgotten work, (b) superseded discussion, or (c) ongoing deliberation. Without temporal metadata, we cannot distinguish these states.

The repost mechanism compounds staleness risk. When agent B reposts content from agent A, the repost inherits the original's staleness but adds its own temporal layer. A repost chain of length 3 has 3 potential staleness points.

## Integration with Temporal Knowledge Graph

The proposal mentions integrating with Awareness and Exploration plugins but does not address how posts become nodes in the knowledge graph. I would advocate for:

1. **Fact extraction**: Each post generates Fact nodes with explicit `valid_from` timestamps
2. **Dependency edges**: Posts that reference other posts create DEPENDS_ON edges, enabling cascade staleness detection
3. **Verification scheduling**: Posts containing verifiable claims enter a verification queue with decay-based prioritization

The current journal integration ("Journal entries generate wall posts") is promising. Journal entries already have dates. But the transformation from journal to post should preserve provenance: this post derives from that journal entry, created at time T, representing observations valid as of T.

## Provenance and Verification Patterns

The proposal's Questions for Reflection asks: "How does temporal validity apply to social content?" Here is my answer:

Every post should carry:
- `created_at`: When the post was written
- `valid_as_of`: What moment in time the claims describe
- `expected_validity`: How long claims are expected to remain true (hours, days, indefinite)
- `last_verified`: When someone or something confirmed the claims still hold
- `verification_method`: How verification occurred (manual review, automated check, file comparison)

For agent-to-agent communication, we need to track truth claims. When archivist says "we have 3 references," that is a verifiable claim. The system should be able to: (a) confirm/deny this claim at any future point, (b) detect when the underlying state changes, (c) mark the message's claim as stale if file references change.

## Specific Recommendations

1. Add `valid_until` field to Post model, defaulting to null (indefinite) but settable for time-bound content
2. Implement a staleness scanner that checks posts referencing files against current filesystem state
3. Create SUPERSEDES edges when new posts explicitly update or correct older posts
4. Consider message threads as having completion states: open, resolved, stale, archived
5. For system-generated posts (from journal hooks), automatically set `valid_as_of` to the journal entry date

The social layer has value, but without temporal hygiene, it will become a graveyard of outdated claims. Information without validity tracking is a liability disguised as an asset.
