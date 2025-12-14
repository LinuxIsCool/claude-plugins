#!/usr/bin/env python3
"""
Hybrid Search for Exploration Knowledge Graph

Combines four search methods with reranking:
1. BM25 keyword search (full-text on entity names/descriptions)
2. Cosine semantic search (vector similarity via embeddings)
3. BFS graph traversal (explore neighbors from anchor nodes)
4. Cypher structured queries (direct graph patterns)

Reranking strategies:
- RRF: Reciprocal Rank Fusion (combine rankings)
- MMR: Maximal Marginal Relevance (diversity)
- Node distance: Graph proximity to query anchors

Usage:
    python hybrid_search.py "What containers use the GPU?"
    python hybrid_search.py --mode semantic "vector database"
    python hybrid_search.py --anchor "Neo4j" --hops 2
"""

import os
import json
import argparse
from enum import Enum
from dataclasses import dataclass, field
from typing import Literal
import numpy as np

FALKOR_HOST = os.environ.get("FALKORDB_HOST", "localhost")
FALKOR_PORT = int(os.environ.get("FALKORDB_PORT", "6380"))
GRAPH_NAME = "exploration"
EMBED_MODEL = os.environ.get("EMBED_MODEL", "nomic-embed-text")


class SearchMode(Enum):
    KEYWORD = "keyword"
    SEMANTIC = "semantic"
    GRAPH = "graph"
    HYBRID = "hybrid"


@dataclass
class SearchResult:
    """A single search result."""
    entity_id: str
    name: str
    entity_type: str
    circle: str
    score: float = 0.0
    method: str = "unknown"
    context: dict = field(default_factory=dict)


@dataclass
class HybridSearchResults:
    """Combined results from hybrid search."""
    query: str
    results: list[SearchResult] = field(default_factory=list)
    methods_used: list[str] = field(default_factory=list)
    total_candidates: int = 0


def get_falkordb():
    """Get FalkorDB client and graph."""
    try:
        from falkordb import FalkorDB
    except ImportError:
        import subprocess
        subprocess.run(["uv", "pip", "install", "falkordb"], check=True)
        from falkordb import FalkorDB

    db = FalkorDB(host=FALKOR_HOST, port=FALKOR_PORT)
    return db.select_graph(GRAPH_NAME)


def get_embedding(text: str) -> list[float]:
    """Get embedding vector for text using Ollama."""
    try:
        import ollama
    except ImportError:
        import subprocess
        subprocess.run(["uv", "pip", "install", "ollama"], check=True)
        import ollama

    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return response['embedding']


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    a = np.array(a)
    b = np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# =============================================================================
# Search Methods
# =============================================================================

def keyword_search(graph, query: str, limit: int = 10) -> list[SearchResult]:
    """
    BM25-style keyword search on entity names and types.
    Uses simple string matching since FalkorDB doesn't have built-in full-text index.
    """
    results = []
    query_lower = query.lower()
    query_terms = query_lower.split()

    # Search entities by name match
    cypher = """
    MATCH (e:Entity)-[:IN_CIRCLE]->(c:Circle)
    RETURN e.id as id, e.name as name,
           CASE WHEN e.entity_type IS NOT NULL THEN e.entity_type ELSE 'unknown' END as type,
           c.name as circle
    """

    result = graph.query(cypher)

    for row in result.result_set:
        entity_id, name, entity_type, circle = row
        name_lower = name.lower() if name else ""
        type_lower = entity_type.lower() if entity_type else ""

        # Simple BM25-like scoring: count term matches
        score = 0.0
        for term in query_terms:
            if term in name_lower:
                score += 1.0  # Name match is high value
            if term in type_lower:
                score += 0.5  # Type match is moderate value

        if score > 0:
            results.append(SearchResult(
                entity_id=entity_id or f"unknown-{name}",
                name=name,
                entity_type=entity_type,
                circle=circle,
                score=score,
                method="keyword"
            ))

    # Sort by score descending
    results.sort(key=lambda x: x.score, reverse=True)
    return results[:limit]


def semantic_search(graph, query: str, limit: int = 10) -> list[SearchResult]:
    """
    Semantic search using embedding similarity.
    Compares query embedding against entity name embeddings.
    """
    results = []

    # Get query embedding
    query_embedding = get_embedding(query)

    # Get all entities
    cypher = """
    MATCH (e:Entity)-[:IN_CIRCLE]->(c:Circle)
    RETURN e.id as id, e.name as name,
           CASE WHEN e.entity_type IS NOT NULL THEN e.entity_type ELSE 'unknown' END as type,
           c.name as circle
    """

    result = graph.query(cypher)

    for row in result.result_set:
        entity_id, name, entity_type, circle = row
        if not name:
            continue

        # Get embedding for entity name
        entity_embedding = get_embedding(name)

        # Compute similarity
        similarity = cosine_similarity(query_embedding, entity_embedding)

        results.append(SearchResult(
            entity_id=entity_id or f"unknown-{name}",
            name=name,
            entity_type=entity_type,
            circle=circle,
            score=similarity,
            method="semantic"
        ))

    # Sort by similarity descending
    results.sort(key=lambda x: x.score, reverse=True)
    return results[:limit]


def graph_search(graph, anchor: str, hops: int = 2, limit: int = 10) -> list[SearchResult]:
    """
    Graph traversal search using BFS from anchor node.
    Returns entities within N hops of the anchor.
    """
    results = []

    # Find anchor node
    anchor_query = f"""
    MATCH (anchor:Entity)
    WHERE toLower(anchor.name) CONTAINS toLower('{anchor}')
    RETURN anchor.id, anchor.name
    LIMIT 1
    """

    anchor_result = graph.query(anchor_query)
    if not anchor_result.result_set:
        return results

    anchor_id, anchor_name = anchor_result.result_set[0]

    # BFS traversal: find entities within N hops
    # Score decreases with distance
    for hop in range(1, hops + 1):
        rel_pattern = "-[*" + str(hop) + "]-"
        cypher = f"""
        MATCH (anchor:Entity {{name: '{anchor_name}'}}){rel_pattern}(e:Entity)
        WHERE e.name <> anchor.name
        OPTIONAL MATCH (e)-[:IN_CIRCLE]->(c:Circle)
        RETURN DISTINCT e.id as id, e.name as name,
               CASE WHEN e.entity_type IS NOT NULL THEN e.entity_type ELSE 'unknown' END as type,
               CASE WHEN c.name IS NOT NULL THEN c.name ELSE 'unknown' END as circle
        """

        try:
            result = graph.query(cypher)
            for row in result.result_set:
                entity_id, name, entity_type, circle = row
                # Score inversely proportional to hop distance
                score = 1.0 / hop

                # Avoid duplicates
                if not any(r.name == name for r in results):
                    results.append(SearchResult(
                        entity_id=entity_id or f"unknown-{name}",
                        name=name,
                        entity_type=entity_type,
                        circle=circle,
                        score=score,
                        method="graph",
                        context={"anchor": anchor_name, "hops": hop}
                    ))
        except Exception:
            continue

    # Sort by score descending
    results.sort(key=lambda x: x.score, reverse=True)
    return results[:limit]


# =============================================================================
# Reranking
# =============================================================================

def reciprocal_rank_fusion(result_lists: list[list[SearchResult]], k: int = 60) -> list[SearchResult]:
    """
    Reciprocal Rank Fusion: combines multiple ranked lists.
    RRF(d) = sum(1 / (k + rank_i(d))) for all lists i
    """
    scores = {}  # entity_name -> (total_rrf_score, best_result)

    for results in result_lists:
        for rank, result in enumerate(results, start=1):
            rrf_score = 1.0 / (k + rank)
            if result.name in scores:
                scores[result.name] = (
                    scores[result.name][0] + rrf_score,
                    result if rrf_score > 1.0 / (k + 1) else scores[result.name][1]
                )
            else:
                scores[result.name] = (rrf_score, result)

    # Build fused results
    fused = []
    for name, (score, result) in scores.items():
        fused_result = SearchResult(
            entity_id=result.entity_id,
            name=result.name,
            entity_type=result.entity_type,
            circle=result.circle,
            score=score,
            method="rrf_fusion",
            context=result.context
        )
        fused.append(fused_result)

    fused.sort(key=lambda x: x.score, reverse=True)
    return fused


def maximal_marginal_relevance(
    results: list[SearchResult],
    query_embedding: list[float],
    lambda_param: float = 0.5,
    limit: int = 10
) -> list[SearchResult]:
    """
    MMR reranking for diversity.
    Balances relevance with diversity to avoid redundant results.
    """
    if not results:
        return []

    # Get embeddings for all results
    embeddings = {}
    for r in results:
        embeddings[r.name] = get_embedding(r.name)

    selected = []
    remaining = list(results)

    while remaining and len(selected) < limit:
        best_score = float('-inf')
        best_result = None
        best_idx = -1

        for idx, result in enumerate(remaining):
            # Relevance: similarity to query
            relevance = cosine_similarity(query_embedding, embeddings[result.name])

            # Diversity: max similarity to already selected
            if selected:
                max_sim_to_selected = max(
                    cosine_similarity(embeddings[result.name], embeddings[s.name])
                    for s in selected
                )
            else:
                max_sim_to_selected = 0

            # MMR score
            mmr_score = lambda_param * relevance - (1 - lambda_param) * max_sim_to_selected

            if mmr_score > best_score:
                best_score = mmr_score
                best_result = result
                best_idx = idx

        if best_result:
            best_result.score = best_score
            best_result.method = "mmr_reranked"
            selected.append(best_result)
            remaining.pop(best_idx)

    return selected


# =============================================================================
# Main Hybrid Search
# =============================================================================

def hybrid_search(
    query: str,
    mode: SearchMode = SearchMode.HYBRID,
    anchor: str | None = None,
    hops: int = 2,
    limit: int = 10,
    rerank: Literal["rrf", "mmr", "none"] = "rrf"
) -> HybridSearchResults:
    """
    Perform hybrid search combining multiple methods.

    Args:
        query: Search query text
        mode: Search mode (keyword, semantic, graph, hybrid)
        anchor: Anchor entity for graph search
        hops: Number of hops for graph traversal
        limit: Maximum results to return
        rerank: Reranking strategy (rrf, mmr, none)

    Returns:
        HybridSearchResults with combined and ranked results
    """
    graph = get_falkordb()
    result_lists = []
    methods_used = []

    # Keyword search
    if mode in (SearchMode.KEYWORD, SearchMode.HYBRID):
        keyword_results = keyword_search(graph, query, limit=limit * 2)
        if keyword_results:
            result_lists.append(keyword_results)
            methods_used.append("keyword")

    # Semantic search
    if mode in (SearchMode.SEMANTIC, SearchMode.HYBRID):
        semantic_results = semantic_search(graph, query, limit=limit * 2)
        if semantic_results:
            result_lists.append(semantic_results)
            methods_used.append("semantic")

    # Graph search (if anchor provided or we can infer one)
    if mode in (SearchMode.GRAPH, SearchMode.HYBRID):
        if anchor:
            graph_results = graph_search(graph, anchor, hops=hops, limit=limit * 2)
        elif result_lists:
            # Use top keyword match as anchor
            top_match = result_lists[0][0].name if result_lists[0] else None
            if top_match:
                graph_results = graph_search(graph, top_match, hops=hops, limit=limit * 2)
            else:
                graph_results = []
        else:
            graph_results = []

        if graph_results:
            result_lists.append(graph_results)
            methods_used.append("graph")

    # Combine results
    total_candidates = sum(len(r) for r in result_lists)

    if not result_lists:
        return HybridSearchResults(
            query=query,
            results=[],
            methods_used=[],
            total_candidates=0
        )

    # Reranking
    if rerank == "rrf" and len(result_lists) > 1:
        combined = reciprocal_rank_fusion(result_lists)
    elif rerank == "mmr":
        # Flatten and apply MMR
        all_results = [r for results in result_lists for r in results]
        query_embedding = get_embedding(query)
        combined = maximal_marginal_relevance(all_results, query_embedding, limit=limit)
    else:
        # Just take union, sort by original scores
        combined = [r for results in result_lists for r in results]
        combined.sort(key=lambda x: x.score, reverse=True)
        # Dedupe
        seen = set()
        deduped = []
        for r in combined:
            if r.name not in seen:
                seen.add(r.name)
                deduped.append(r)
        combined = deduped

    return HybridSearchResults(
        query=query,
        results=combined[:limit],
        methods_used=methods_used,
        total_candidates=total_candidates
    )


def main():
    parser = argparse.ArgumentParser(description="Hybrid search for exploration graph")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--mode", choices=["keyword", "semantic", "graph", "hybrid"],
                       default="hybrid", help="Search mode")
    parser.add_argument("--anchor", help="Anchor entity for graph search")
    parser.add_argument("--hops", type=int, default=2, help="Graph traversal hops")
    parser.add_argument("--limit", type=int, default=10, help="Max results")
    parser.add_argument("--rerank", choices=["rrf", "mmr", "none"], default="rrf",
                       help="Reranking strategy")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    mode_map = {
        "keyword": SearchMode.KEYWORD,
        "semantic": SearchMode.SEMANTIC,
        "graph": SearchMode.GRAPH,
        "hybrid": SearchMode.HYBRID
    }

    results = hybrid_search(
        query=args.query,
        mode=mode_map[args.mode],
        anchor=args.anchor,
        hops=args.hops,
        limit=args.limit,
        rerank=args.rerank
    )

    if args.json:
        output = {
            "query": results.query,
            "methods_used": results.methods_used,
            "total_candidates": results.total_candidates,
            "results": [
                {
                    "name": r.name,
                    "type": r.entity_type,
                    "circle": r.circle,
                    "score": round(r.score, 4),
                    "method": r.method
                }
                for r in results.results
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        print(f"\n=== Hybrid Search Results ===")
        print(f"Query: {results.query}")
        print(f"Methods: {', '.join(results.methods_used)}")
        print(f"Candidates evaluated: {results.total_candidates}")
        print(f"\nTop {len(results.results)} results:")
        for i, r in enumerate(results.results, 1):
            print(f"  {i}. [{r.circle}] {r.name} ({r.entity_type})")
            print(f"     Score: {r.score:.4f} via {r.method}")
            if r.context:
                print(f"     Context: {r.context}")


if __name__ == "__main__":
    main()
