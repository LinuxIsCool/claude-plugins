---
id: 2025-12-13-1815
title: "Quartz Graph Comes Alive"
type: atomic
created: 2025-12-13T18:15:00
author: claude-opus-4
description: "Phase 1 complete: Quartz configured, built, and serving journal graph at localhost:8080. Force-directed visualization shows DNA spiral structure with 21 nodes, wikilink edges, and tag clusters."
tags: [visualization, quartz, graph-view, milestone, d3js, pixijs, phase-1]
parent_daily: [[2025-12-13]]
related:
  - [[17-45-visualization-layer-emerges]]
  - [[15-45-journal-atomic-model]]
---

# Quartz Graph Comes Alive

The ecosystem has eyes.

## What Happened

Completed Phase 1 of the visualization strategy:

1. **Configured Quartz** for our journal content
   - Changed `pageTitle` to "Claude Ecosystem"
   - Set `baseUrl` to localhost
   - Disabled analytics (local only)

2. **Fixed YAML Frontmatter**
   - The daily entry had inline wikilinks in `links:` field
   - YAML parser choked on `links: [[X]], [[Y]]` format
   - Fixed to proper array: `links: ["[[X]]", "[[Y]]"]`

3. **Built and Served**
   ```bash
   npx quartz build -d ../../.claude/journal --serve --port 8080 --wsPort 3010
   ```
   - 21 markdown files parsed
   - 134 files emitted (HTML, JSON, assets, tag pages)
   - Content index generated with full link graph

4. **Verified the Graph**
   - Opened `http://localhost:8080`
   - Clicked "Global Graph" button
   - Force-directed graph rendered via D3.js + PixiJS

## The Graph Structure

What we see:
- **Large gray nodes**: High-connectivity entries (daily, monthly, yearly)
- **Small teal circles**: Atomic entries and tags
- **Dark blue highlight**: Current page
- **Gray edges**: Wikilink connections

The structure matches the DNA spiral metaphor:
- Yearly node → Monthly → Daily → Atomics
- Tags create cross-cutting clusters
- Force simulation naturally reveals temporal hierarchy

## Content Index

The content index at `/static/contentIndex.json` contains:
```json
{
  "slug": "2025/12/13/14-30-subagent-exploration",
  "links": ["2025/12/13/2025-12-13", "2025/12/2025-12", "2025/2025"],
  "tags": ["discovery", "subagents", "cli", "system-prompts"],
  "content": "..."
}
```

Every entry has:
- `slug`: URL path
- `links`: Outgoing wikilinks (resolved to slugs)
- `tags`: Extracted from frontmatter
- `content`: Full text for search

## Technical Notes

**D3 Force Simulation** (from graph.inline.ts):
- `forceManyBody`: Node repulsion
- `forceCenter`: Gravity toward center
- `forceLink`: Edge springs
- `forceCollide`: Prevent overlap

**PixiJS Rendering**:
- WebGL acceleration (fell back from WebGPU)
- Handles thousands of nodes at 60fps
- tween.js for smooth hover transitions

## What's Next

Phase 2: FalkorDB API Bridge
- Create Express endpoint for graph queries
- Transform Cypher results to D3 format
- Enable "Show me commits as a graph"

Phase 3: Multi-View UI
- View selector (journal/commits/concepts)
- Synchronized navigation

Phase 4: Commands
- `/visualize journal`
- `/visualize commits --since="1 week ago"`

## The Moment

Watching the graph materialize in the browser was like watching the ecosystem become self-aware of its own structure. The wikilinks we've been carefully creating aren't just navigation—they're the nervous system made visible.

The data was always there. Now we can see it.

---
*Parent: [[2025-12-13]]*
