---
created: 2025-12-18T19:04:01-08:00
parent_daily: "[[2025-12-18]]"
tags:
  - search
  - rag
  - classifier
  - evaluation
  - lessons-learned
---

# RAG Query Classifier: Lessons in Humility

Built a query classifier to pre-filter unanswerable queries before RAG retrieval. The results were instructive about the limits of both classification and retrieval.

## The Classifier

Heuristic-based classifier detecting four query types:

| Type | Pattern | Example |
|------|---------|---------|
| ACTION | "can you make/create/change" | "Can you make the statusline bold?" |
| DEBUGGING | "not working", "why did" | "Why is agent renaming not working?" |
| CONTEXT | pronouns without entities | "Where is it documented?" |
| KNOWLEDGE | "what is", "how does" | "What is the registry?" |

Achieved 94% accuracy on curated test set of 16 queries.

## Reality Check on Real Queries

Tested against 40 real user queries from session logs:

| Outcome | Count | % |
|---------|-------|---|
| Correctly filtered (true negative) | 15 | 38% |
| Correctly retrieved (true positive) | 6 | 15% |
| Wrongly filtered (false negative) | 7 | 18% |
| Wrongly retrieved (false positive) | 12 | 30% |

The classifier filtered 7 queries that actually would have succeeded—including "Where is it documented?" which has context-dependent pronoun "it" but contains enough signal ("documented") to retrieve correctly.

## The Fundamental Problem

Only **32% of real queries are answerable** by static retrieval:

```
Real user queries
├── 68% unanswerable
│   ├── Context-dependent (need conversation history)
│   ├── Action requests (not information seeking)
│   └── Debugging (runtime state, not indexed)
└── 32% potentially answerable
    ├── Some retrieved successfully
    └── Some fail due to chunk/embedding quality
```

A perfect classifier could achieve MRR 0.56 (vs current 0.18). Our classifier achieves 0.19—barely better because it over-filters.

## Key Insight

**Be permissive, not restrictive.**

Instead of pre-filtering, let retrieval attempt and fail gracefully:
1. Attempt retrieval on all queries
2. Use confidence threshold (0.55-0.65) to reject low-quality results
3. Return "no relevant documents found" rather than refusing to try

This captures the upside of queries that look context-dependent but actually contain enough signal.

## Artifacts

- `rag/classifier.py` - Query type classifier
- `FINDINGS.md` - Comprehensive analysis and recommendations
- `analyze_perfect_classifier.py` - Upper bound analysis script

## Continuation

Next session should:
1. Implement confidence thresholding in retrieval pipeline
2. Create standalone query test set for fair evaluation
3. Explore hybrid: threshold + classifier fallback

---

*Parent: [[2025-12-18]] → [[2025-12]] → [[2025]]*
