# The Library

**Keeper of Sources. Guardian of Provenance.**

---

## Purpose

The Library catalogues every external resource accessed by the ecosystem - every URL fetched, every paper referenced, every dataset discovered. It maintains provenance, prevents duplication, and serves as the citation system for external knowledge.

## Philosophy

> "Knowledge without provenance is unstable. You can't build on foundations you can't trace."

Every external resource gets:
- **Full URL and metadata**
- **Discovery context** (why it was fetched)
- **Citation chain** (which sessions/agents used it)
- **Access patterns** (how often, when last accessed)

## Structure

```
.claude/library/
├── index.md                    # Master index with statistics
├── catalog.md                  # Complete resource listing
├── citations.json              # Machine-readable citation data
├── README.md                   # This file
│
├── urls/
│   ├── by-domain/              # Domain-specific catalogs
│   │   ├── github.com.md
│   │   ├── claude.com.md
│   │   ├── pypi.org.md
│   │   └── ...
│   └── by-topic/               # Topic-based clustering
│       ├── agent-development.md
│       ├── python.md
│       ├── security.md
│       └── ...
│
├── papers/                     # Academic papers
├── transcripts/                # Video/audio transcripts
│   └── youtube/
├── datasets/                   # Dataset references
└── .cache/                     # Cached content
```

## Current Statistics

**As of 2025-12-15:**
- 46 unique resources catalogued
- 88 total references across sessions
- 29 domains tracked
- Coverage: 2025-12-08 to 2025-12-15 (60+ sessions)

## Integration

### With Archivist
- **Archivist**: Internal artifacts (.claude/archive/)
- **Librarian**: External resources (.claude/library/)
- Complementary provenance tracking

### With Session Logs
- All resources traced to specific sessions
- Discovery context preserved
- Timeline of access maintained

## Usage

### Finding Resources

**By Domain:**
```
.claude/library/urls/by-domain/github.com.md
```

**By Topic:**
```
.claude/library/urls/by-topic/agent-development.md
```

**Complete Catalog:**
```
.claude/library/catalog.md
```

**Citation Data (JSON):**
```
.claude/library/citations.json
```

### Resource Format

Each catalogued resource includes:

```yaml
url: https://example.com/resource
title: "Resource Title"
domain: example.com
fetched: 2025-12-13T14:30:00Z
last_accessed: 2025-12-15T10:00:00Z
access_count: 3
topics: [topic1, topic2]
cited_by:
  - session: session-id
  - agent: agent-name
  - document: path/to/doc
context: "Why this was accessed"
freshness_policy: 7d
```

## Top Domains

1. **claude.com** (27 refs) - Claude Platform, git co-authorship
2. **github.com** (20 refs) - Code repositories, security alerts
3. **emberstudiosduncan.com** (7 refs) - Yoga studio schedules
4. **pypi.org** (4 refs) - Python packages
5. **docs.* sites** (multiple) - Documentation resources

## Topic Coverage

- **Agent Development**: Plugin frameworks, agent patterns
- **Documentation**: API references, framework docs
- **Security**: GitHub scanning, secret management
- **Python Ecosystem**: PyPI packages, tutorials
- **Yoga Scheduling**: Studio schedules, calendar integration
- **Knowledge Graphs**: Temporal graphs, graph databases

## Access Patterns

- **No WebFetch usage detected** in current logs
- All URLs are direct references from:
  - Git commit messages (co-authorship attribution)
  - Documentation links
  - Code comments and configurations
  - Security alerts

## Future Enhancements

### Planned
- [ ] WebFetch caching system
- [ ] Academic paper integration
- [ ] Dataset cataloguing
- [ ] Citation network visualization
- [ ] Freshness monitoring
- [ ] Automatic cache warming

### Under Consideration
- [ ] Content snapshots for key resources
- [ ] Diff detection for documentation changes
- [ ] Related resource recommendations
- [ ] Cross-reference mapping with Archive

## Maintenance

The Library is self-maintaining:
- New resources auto-catalogued from session logs
- Citation counts updated automatically
- Access patterns tracked per resource
- Freshness policies per domain

---

**The Library grows with each session. External knowledge, properly sourced.**

*Maintained by: The Librarian*
*Last Updated: 2025-12-15*
