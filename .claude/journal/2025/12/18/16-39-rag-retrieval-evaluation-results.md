---
created: 2025-12-18T16:39:00-08:00
parent_daily: "[[2025-12-18]]"
tags:
  - search
  - rag
  - evaluation
  - metrics
  - research
---

# RAG Retrieval Evaluation Results

Comprehensive evaluation of retrieval strategies for the Claude plugins ecosystem knowledge base.

## Test Configuration

- **Index**: 209 files, 21,188 chunks
- **Files indexed**: `.claude/registry/*.md`, `.claude/agents/*.md`, `.claude/briefings/*.md`, `CLAUDE.md`, `plugins/*/skills/**/*.md`, `plugins/*/.claude-plugin/plugin.json`
- **Chunk size**: 512 tokens, 50 overlap
- **Embeddings**: `nomic-embed-text` via Ollama
- **Judge model**: `llama3.2:3b` via Ollama
- **Test queries**: 122 ecosystem-specific queries across 5 categories

### Query Categories

| Category | Count | Description |
|----------|-------|-------------|
| entity | 43 | Agent/plugin identity queries |
| confirmation | 47 | Capability verification queries |
| discovery | 9 | Exploration queries |
| process | 21 | Process/workflow queries |
| historical | 2 | Temporal queries |

## Results Summary

| Config | MRR | P@3 | P@5 | Time |
|--------|-----|-----|-----|------|
| vector | 1.000 | 1.000 | 0.997 | 388s |
| hybrid | 0.801 | 0.538 | 0.521 | 17s |
| hybrid+rerank | 0.700 | 0.500 | 0.467 | 29s |
| contextual vector | 1.000 | 1.000 | 1.000 | 402s |

### Category Breakdown (MRR)

| Category | vector | hybrid | hybrid+rerank |
|----------|--------|--------|---------------|
| confirmation | 1.000 | 0.839 | 0.656 |
| discovery | 1.000 | 0.944 | 0.587 |
| entity | 1.000 | 0.663 | 0.659 |
| historical | 1.000 | 0.625 | 1.000 |
| process | 1.000 | 0.952 | 0.901 |

## Key Findings

### 1. Vector Retrieval Dominates for Semantic Documentation

Pure vector retrieval achieves near-perfect scores (MRR 1.000) on this documentation-heavy corpus. This makes sense because:
- Documentation is semantically rich with meaningful natural language
- Queries are semantic in nature ("What does X do?", "How do I Y?")
- Embedding models excel at capturing conceptual similarity

### 2. Hybrid Search Underperforms (Surprising)

Hybrid retrieval (BM25 + Vector with RRF fusion) scored significantly lower:
- MRR dropped from 1.000 to 0.801
- P@5 dropped from 0.997 to 0.521
- 24x faster (17s vs 388s) but quality tradeoff is severe

**Hypothesis**: BM25's lexical matching may be introducing noise for semantic queries. RRF fusion gives equal weight to both signals, diluting the strong vector signal with weaker keyword matches.

### 3. Reranking Hurts Hybrid (Counterintuitive!)

Adding cross-encoder reranking to hybrid retrieval made it worse:
- MRR: 0.801 → 0.700
- P@5: 0.521 → 0.467

**Hypothesis**: Cross-encoder (`ms-marco-MiniLM-L-6-v2`) is trained on web search relevance, not documentation semantics. The reranker's relevance model may not align with documentation retrieval tasks.

### 4. Contextual Chunking Has Marginal Impact

Anthropic's contextual chunking technique (prepending LLM-generated context to each chunk before embedding) showed minimal improvement:
- P@5: 0.997 → 1.000 (already at ceiling)

For this well-structured documentation corpus, the standard chunking already provides sufficient context. Contextual chunking may show more benefit for:
- Poorly organized content
- Content lacking clear boundaries
- Corpora where chunks lose meaning in isolation

## Implications for Plugin Design

### Recommended Configuration

For the ecosystem knowledge base:
1. **Use pure vector retrieval** for highest quality
2. **Consider hybrid only if latency is critical** (accept 20% MRR drop for 24x speedup)
3. **Skip reranking** - it hurts more than it helps on this corpus
4. **Skip contextual chunking** - marginal benefit doesn't justify 2x indexing cost

### When to Revisit

- If adding code files (may need hybrid for symbol matching)
- If adding user-generated content (more variance in quality)
- If query patterns shift toward keyword-heavy searches

## Technical Artifacts

- Regular index: `.rag-index/`
- Contextual index: `.rag-index-contextual/`
- Test results: `plugins/search/tools/ecosystem-full.json`
- Contextual results: `plugins/search/tools/ecosystem-contextual.json`

---

*Parent: [[2025-12-18]] → [[2025-12]] → [[2025]]*
