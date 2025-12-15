# Agent Deprecation Queue

*Maintained by: agent-architect*
*Last updated: 2025-12-15*

---

## Active Deprecations

| Agent | Reason | Phase | Deadline | Action |
|-------|--------|-------|----------|--------|
| awareness:mentor | Exact duplicate of plugin version | Phase 3 (Archive) | 2025-12-15 | DELETE |

---

## Deprecation Log

### 2025-12-15: awareness:mentor

**Agent**: `.claude/agents/awareness:mentor.md`

**Reason**: This is an exact duplicate of `plugins/awareness/agents/mentor.md`. The plugin version is the authoritative source. Having both creates confusion and wastes context tokens.

**Discovery**: Initial governance audit (health-review-2025-12-15.md)

**Migration Path**: Use the plugin version via namespace `awareness:mentor` or invoke `plugins/awareness/agents/mentor.md` directly.

**Replacement**: `plugins/awareness/agents/mentor.md` (identical functionality)

**Phase Progression**:
- 2025-12-15: Identified as redundant
- 2025-12-15: Moved to archive (immediate - clear redundancy)

**Archive Location**: `.claude/archive/agents/awareness-mentor-deprecated.md`

---

## Completed Deprecations

*None yet - this is the first.*

---

## Notes

Deprecation queue follows the process defined in `.claude/governance/agent-lifecycle.md`:

1. **Phase 1: Review** (7 days) - Flag and document
2. **Phase 2: Soft Deprecation** (14 days) - Add notice, stop recommending
3. **Phase 3: Archive** (Permanent) - Move to archive, preserve history

For clear redundancies (exact duplicates), skip directly to Phase 3.
