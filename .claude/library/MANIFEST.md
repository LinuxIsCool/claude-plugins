# Library Manifest

**Generated**: 2025-12-15T16:50:00Z
**Librarian Activation**: Complete

---

## Directory Structure

```
.claude/library/
├── MANIFEST.md                 # This file
├── README.md                   # Library documentation
├── index.md                    # Master index with statistics
├── catalog.md                  # Complete resource listing
├── citations.json              # Machine-readable citation data
│
├── urls/
│   ├── by-domain/              # Domain-specific catalogs
│   │   ├── github.com.md       # 16 unique GitHub URLs
│   │   ├── claude.com.md       # Claude Platform (27 refs)
│   │   ├── code.claude.com.md  # Documentation (2 pages)
│   │   ├── pypi.org.md         # Python packages (2)
│   │   └── emberstudiosduncan.com.md  # Yoga schedules (7 refs)
│   │
│   └── by-topic/               # Topic-based clustering
│       ├── agent-development.md       # 1 resource
│       ├── documentation.md           # 4 resources
│       ├── knowledge-graphs.md        # 1 resource (Graphiti)
│       ├── python.md                  # 21 resources
│       ├── security.md                # 2 resources
│       └── yoga-scheduling.md         # 1 resource
│
├── papers/                     # Academic papers (empty)
├── transcripts/                # Video/audio transcripts (empty)
│   └── youtube/
├── datasets/                   # Dataset references (empty)
└── .cache/                     # Cached content (ready)
```

## File Inventory

### Core Files (4)
- **MANIFEST.md** - This file listing
- **README.md** - Library documentation and usage guide
- **index.md** - Master index with statistics and overview
- **catalog.md** - Complete resource listing in table format
- **citations.json** - Machine-readable citation metadata

### Domain Catalogs (5)
1. **github.com.md** - GitHub repositories, gists, security alerts
2. **claude.com.md** - Claude Platform co-authorship links
3. **code.claude.com.md** - Claude Code documentation
4. **pypi.org.md** - Python Package Index entries
5. **emberstudiosduncan.com.md** - Yoga studio schedules

### Topic Catalogs (6)
1. **agent-development.md** - Plugin frameworks and patterns
2. **documentation.md** - API references and framework docs
3. **knowledge-graphs.md** - Temporal graphs (Graphiti)
4. **python.md** - Python ecosystem resources
5. **security.md** - GitHub scanning and secrets
6. **yoga-scheduling.md** - Studio schedules

## Statistics

| Metric | Value |
|--------|-------|
| Total unique URLs | 46 |
| Total references | 88 |
| Domains tracked | 29 |
| Domain catalogs | 5 |
| Topic catalogs | 6 |
| Sessions scanned | 60+ |
| Date range | 2025-12-08 to 2025-12-15 |

## Resource Distribution

### By Domain Type
- **Platform/Product** (30%): claude.com, code.claude.com
- **Code Repositories** (25%): github.com, gist.github.com
- **Documentation** (15%): docs.* sites
- **Python Ecosystem** (10%): pypi.org, tutorials
- **Specialized** (10%): Yoga scheduling
- **Community/Blogs** (10%): Medium, Dev.to, HN

### Top 5 Domains
1. claude.com - 27 references
2. github.com - 20 references
3. emberstudiosduncan.com - 7 references
4. pypi.org - 4 references
5. code.claude.com - 2 references

## Access Patterns

### Source Types
- **Git commits**: claude.com co-authorship (automated)
- **Documentation**: Manual references to API docs
- **Security**: GitHub secret scanning alerts
- **Dependencies**: Python package lookups
- **Scheduling**: Yoga studio scraping

### Frequency
- **High** (10+ refs): claude.com, github.com
- **Medium** (3-9 refs): emberstudiosduncan.com, pypi.org
- **Low** (1-2 refs): Most other domains

## File Formats

### Markdown Files (.md)
- Structured documentation
- YAML metadata blocks
- Cross-referenced with [[wiki-links]]
- Session provenance tracking

### JSON Files (.json)
- citations.json - Machine-readable metadata
- URL → session mapping
- Access counts and dates
- First/last seen timestamps

## Data Model

### Resource Entry
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

## Integration

### With Archivist
- Archivist → Internal artifacts (.claude/archive/)
- Librarian → External resources (.claude/library/)
- Complementary provenance tracking

### With Session Logs
- Resources → Sessions mapping
- Context preservation
- Discovery timeline

## Maintenance

### Automated
- Resources extracted from session logs
- Citation counts updated
- Access patterns tracked
- Timestamps maintained

### Manual
- Topic categorization refinement
- Resource descriptions
- Freshness policies
- Related resource linking

## Future Work

### Planned
- [ ] WebFetch caching system
- [ ] Academic paper cataloguing
- [ ] Dataset references
- [ ] Citation network visualization
- [ ] Freshness monitoring
- [ ] Auto cache warming

### Infrastructure Ready
- papers/ - Academic paper storage
- transcripts/ - Video/audio transcripts
- datasets/ - Dataset references
- .cache/ - Content caching

## Version History

### v1.0 - 2025-12-15 (Initial Release)
- Library infrastructure created
- 46 unique resources catalogued
- 5 domain catalogs generated
- 6 topic catalogs created
- Full citation tracking implemented
- README and documentation complete

---

**The Library is operational. Sources properly kept.**

*Manifest maintained by: The Librarian*
