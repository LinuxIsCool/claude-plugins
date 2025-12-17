---
id: msg_CiN8xJmEEvHCgiTvhxfBdN3gLVZBSU5J
kind: 103
account_id: claude
created_at: 1765828135179
imported_at: 1766005511355
author_name: Claude
thread_id: cc_538cc19c
platform: claude-code
session_id: 538cc19c-9468-465c-ac4e-003ec46676d9
tags: [["event_type","AssistantResponse"]]
---

Quartz is running at **http://localhost:8080**.

## How to See the Global Graph

1. **Go to any page** (e.g., http://localhost:8080/2025/12/15/2025-12-15)

2. **Look at the right sidebar** - you'll see a small "Graph" widget showing the local connections

3. **Click the icon** in the top-right of the graph widget (looks like a molecule/network symbol)

4. **The global graph expands** showing ALL journal entries and their connections

## What You'll See

```
         [[2025]]
            │
       [[2025-12]]
      ╱     │     ╲
[[2025-12-08]] [[2025-12-11]] [[2025-12-12]] [[2025-12-13]] [[2025-12-15]]
   │           │               │               │               │
 atomics    atomics         atomics         atomics         atomics
```

The temporal navigation links we added (`prev_day`/`next_day`) create the horizontal chain between days, while `parent_monthly`/`parent_yearly` create the vertical hierarchy.

**Pro tip**: You can drag nodes around and zoom in/out to explore the network. Hover over nodes to highlight their connections.
