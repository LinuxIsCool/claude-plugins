#!/usr/bin/env python3
"""
Ingest web sources and upgrade to bi-temporal schema.

This script:
1. Adds research sources as Knowledge nodes
2. Extracts concepts and techniques
3. Links to existing exploration entities
4. Upgrades schema to bi-temporal model
"""

import os
from datetime import datetime
from falkordb import FalkorDB

FALKOR_HOST = os.environ.get("FALKORDB_HOST", "localhost")
FALKOR_PORT = int(os.environ.get("FALKORDB_PORT", "6380"))
GRAPH_NAME = "exploration"


def get_graph():
    db = FalkorDB(host=FALKOR_HOST, port=FALKOR_PORT)
    return db.select_graph(GRAPH_NAME)


def add_knowledge_sources(graph):
    """Add research papers and articles as Knowledge nodes."""

    sources = [
        {
            "id": "source-zep-temporal",
            "name": "Zep: Temporal Knowledge Graph Architecture for Agent Memory",
            "url": "https://arxiv.org/html/2501.13956v1",
            "type": "research_paper",
            "date": "2025-01",
            "authors": "Preston Rasmussen et al.",
            "key_contributions": [
                "Bi-temporal data model (T and T' timelines)",
                "Hierarchical graph schema (Episode, Semantic, Community)",
                "Hybrid search with BM25 + cosine + BFS",
                "Label propagation for community detection",
                "18.5% accuracy improvement on LongMemEval"
            ]
        },
        {
            "id": "source-kggen",
            "name": "KGGen: Extracting Knowledge Graphs from Plain Text with LLMs",
            "url": "https://arxiv.org/html/2502.09956v1",
            "type": "research_paper",
            "date": "2025-02",
            "authors": "KGGen Authors",
            "key_contributions": [
                "Three-stage pipeline: Generate, Aggregate, Cluster",
                "LLM-as-a-Judge for entity clustering validation",
                "Two-step relation extraction for consistency",
                "MINE benchmark for evaluation",
                "66% accuracy vs 48% GraphRAG"
            ]
        },
        {
            "id": "source-neo4j-extraction",
            "name": "Knowledge Graph Extraction and Challenges",
            "url": "https://neo4j.com/blog/developer/knowledge-graph-extraction-challenges/",
            "type": "blog_post",
            "date": "2024",
            "authors": "Neo4j Team",
            "key_contributions": [
                "LLMGraphTransformer for structured extraction",
                "Configurable node/relationship type constraints",
                "Hybrid search (vector + full-text)",
                "Leiden clustering for community detection",
                "Multi-LLM support (GPT-4o, Gemini, Diffbot)"
            ]
        },
        {
            "id": "source-production-kg-2025",
            "name": "Building Production-Ready Graph Systems in 2025",
            "url": "https://medium.com/@claudiubranzan/from-llms-to-knowledge-graphs-building-production-ready-graph-systems-in-2025-2b4aff1ec99a",
            "type": "blog_post",
            "date": "2025",
            "authors": "Claudiu Branzan",
            "key_contributions": [
                "300-320% ROI from KG implementations",
                "Production maturity reached 2024-2025",
                "Entity standardization best practices",
                "Schema-driven construction patterns"
            ]
        },
        {
            "id": "source-opensource-llm-kg",
            "name": "Best Open Source LLMs for Knowledge Graph Construction 2025",
            "url": "https://www.siliconflow.com/articles/en/best-open-source-LLM-for-Knowledge-Graph-Construction",
            "type": "article",
            "date": "2025",
            "authors": "SiliconFlow",
            "key_contributions": [
                "DeepSeek-R1 recommended for reasoning",
                "Qwen3-235B-A22B for structured output",
                "GLM-4.5 for tool integration",
                "Model selection criteria for KG tasks"
            ]
        }
    ]

    for source in sources:
        # Create source node
        contributions_str = "; ".join(source["key_contributions"])
        query = """
        MERGE (s:Knowledge:Source {id: $id})
        SET s.name = $name,
            s.url = $url,
            s.source_type = $type,
            s.date = $date,
            s.authors = $authors,
            s.key_contributions = $contributions,
            s.ingested_at = $now
        RETURN s.name
        """
        graph.query(query,
            {"id": source["id"], "name": source["name"], "url": source["url"],
             "type": source["type"], "date": source["date"], "authors": source["authors"],
             "contributions": contributions_str, "now": datetime.now().isoformat()})

    print(f"Added {len(sources)} knowledge sources")
    return sources


def add_concepts(graph):
    """Extract and add key concepts from sources."""

    concepts = [
        # From Zep paper
        {"id": "concept-bitemporal", "name": "Bi-Temporal Data Model", "category": "architecture",
         "description": "Dual timeline tracking: T (event time) and T' (transaction time)",
         "source": "source-zep-temporal"},
        {"id": "concept-edge-timestamps", "name": "Temporal Edge Properties", "category": "schema",
         "description": "t_valid, t_invalid, t'_created, t'_expired on every edge",
         "source": "source-zep-temporal"},
        {"id": "concept-hierarchical-graph", "name": "Hierarchical Graph Schema", "category": "architecture",
         "description": "Three tiers: Episode (raw), Semantic (extracted), Community (clustered)",
         "source": "source-zep-temporal"},
        {"id": "concept-hybrid-search", "name": "Hybrid Search", "category": "algorithm",
         "description": "Combine BM25 keyword + cosine semantic + BFS graph traversal",
         "source": "source-zep-temporal"},
        {"id": "concept-label-propagation", "name": "Label Propagation", "category": "algorithm",
         "description": "Community detection via neighbor plurality voting",
         "source": "source-zep-temporal"},

        # From KGGen paper
        {"id": "concept-three-stage", "name": "Generate-Aggregate-Cluster Pipeline", "category": "pipeline",
         "description": "Extract per-source, merge across sources, deduplicate entities",
         "source": "source-kggen"},
        {"id": "concept-llm-judge", "name": "LLM-as-a-Judge Validation", "category": "technique",
         "description": "Use LLM to validate entity clustering decisions",
         "source": "source-kggen"},
        {"id": "concept-two-step-extraction", "name": "Two-Step Relation Extraction", "category": "technique",
         "description": "First extract entities, then extract relations using those entities",
         "source": "source-kggen"},

        # From Neo4j blog
        {"id": "concept-llmgraphtransformer", "name": "LLMGraphTransformer", "category": "tool",
         "description": "LangChain component for converting text to GraphDocument",
         "source": "source-neo4j-extraction"},
        {"id": "concept-schema-constraints", "name": "Schema Constraints", "category": "technique",
         "description": "Define allowed_nodes and allowed_relationships to reduce noise",
         "source": "source-neo4j-extraction"},
        {"id": "concept-leiden-clustering", "name": "Leiden Clustering", "category": "algorithm",
         "description": "Community detection algorithm for entity grouping",
         "source": "source-neo4j-extraction"},

        # General concepts
        {"id": "concept-entity-resolution", "name": "Entity Resolution", "category": "technique",
         "description": "Merge duplicate entities via embedding similarity + LLM validation",
         "source": "source-kggen"},
        {"id": "concept-rrf", "name": "Reciprocal Rank Fusion", "category": "algorithm",
         "description": "Combine multiple ranking signals: score = 1/(k+rank)",
         "source": "source-zep-temporal"},
        {"id": "concept-mmr", "name": "Maximal Marginal Relevance", "category": "algorithm",
         "description": "Balance relevance with diversity in search results",
         "source": "source-zep-temporal"},
        {"id": "concept-cross-encoder", "name": "Cross-Encoder Reranking", "category": "technique",
         "description": "Use LLM to rerank search results by relevance",
         "source": "source-zep-temporal"},
    ]

    for concept in concepts:
        query = """
        MERGE (c:Knowledge:Concept {id: $id})
        SET c.name = $name,
            c.category = $category,
            c.description = $description,
            c.ingested_at = $now
        WITH c
        MATCH (s:Source {id: $source})
        MERGE (c)-[:EXTRACTED_FROM {created_at: $now}]->(s)
        RETURN c.name
        """
        graph.query(query,
            {"id": concept["id"], "name": concept["name"], "category": concept["category"],
             "description": concept["description"], "source": concept["source"],
             "now": datetime.now().isoformat()})

    print(f"Added {len(concepts)} concepts")
    return concepts


def add_techniques(graph):
    """Add specific techniques that can be applied."""

    techniques = [
        {"id": "tech-ollama-extraction", "name": "Ollama Local Extraction",
         "description": "Use local LLM (llama3.2, qwen) for entity extraction - free, no rate limits",
         "applies_to": ["plugin-exploration"], "concepts": ["concept-two-step-extraction"]},
        {"id": "tech-temporal-edges", "name": "Temporal Edge Implementation",
         "description": "Add valid_at, created_at, invalid_at to all relationships",
         "applies_to": ["container-falkor"], "concepts": ["concept-bitemporal", "concept-edge-timestamps"]},
        {"id": "tech-hybrid-retrieval", "name": "Hybrid Retrieval Implementation",
         "description": "Combine FalkorDB graph + pgvector embeddings + BM25 full-text",
         "applies_to": ["container-falkor", "container-pgvector"], "concepts": ["concept-hybrid-search", "concept-rrf"]},
        {"id": "tech-entity-dedup", "name": "Entity Deduplication Pipeline",
         "description": "Embed entities, find similar via cosine, validate with LLM",
         "applies_to": ["plugin-exploration"], "concepts": ["concept-entity-resolution", "concept-llm-judge"]},
    ]

    for tech in techniques:
        query = """
        MERGE (t:Knowledge:Technique {id: $id})
        SET t.name = $name,
            t.description = $description,
            t.ingested_at = $now
        RETURN t.name
        """
        graph.query(query, {"id": tech["id"], "name": tech["name"],
                           "description": tech["description"], "now": datetime.now().isoformat()})

        # Link to entities it applies to
        for entity_id in tech["applies_to"]:
            graph.query("""
                MATCH (t:Technique {id: $tech_id})
                MATCH (e:Entity {id: $entity_id})
                MERGE (t)-[:APPLIES_TO {created_at: $now}]->(e)
            """, {"tech_id": tech["id"], "entity_id": entity_id, "now": datetime.now().isoformat()})

        # Link to concepts it uses
        for concept_id in tech["concepts"]:
            graph.query("""
                MATCH (t:Technique {id: $tech_id})
                MATCH (c:Concept {id: $concept_id})
                MERGE (t)-[:USES_CONCEPT {created_at: $now}]->(c)
            """, {"tech_id": tech["id"], "concept_id": concept_id, "now": datetime.now().isoformat()})

    print(f"Added {len(techniques)} techniques")


def upgrade_to_bitemporal(graph):
    """Add temporal properties to existing relationships."""

    now = datetime.now().isoformat()

    # Add temporal properties to all existing relationships
    upgrade_queries = [
        # IN_CIRCLE relationships
        """
        MATCH (e:Entity)-[r:IN_CIRCLE]->(c:Circle)
        WHERE r.valid_at IS NULL
        SET r.valid_at = $now,
            r.created_at = $now,
            r.confidence = 0.9
        RETURN count(r) as upgraded
        """,
        # PART_OF relationships
        """
        MATCH (a)-[r:PART_OF]->(b)
        WHERE r.valid_at IS NULL
        SET r.valid_at = $now,
            r.created_at = $now,
            r.confidence = 0.95
        RETURN count(r) as upgraded
        """,
        # RUNS_ON relationships
        """
        MATCH (a)-[r:RUNS_ON]->(b)
        WHERE r.valid_at IS NULL
        SET r.valid_at = $now,
            r.created_at = $now,
            r.confidence = 0.95
        RETURN count(r) as upgraded
        """,
        # USES relationships
        """
        MATCH (a)-[r:USES]->(b)
        WHERE r.valid_at IS NULL
        SET r.valid_at = $now,
            r.created_at = $now,
            r.confidence = 0.85
        RETURN count(r) as upgraded
        """,
        # All other relationships
        """
        MATCH ()-[r]->()
        WHERE r.valid_at IS NULL
        SET r.valid_at = $now,
            r.created_at = $now,
            r.confidence = 0.8
        RETURN count(r) as upgraded
        """
    ]

    total_upgraded = 0
    for query in upgrade_queries:
        result = graph.query(query, {"now": now})
        if result.result_set:
            total_upgraded += result.result_set[0][0]

    print(f"Upgraded {total_upgraded} relationships to bi-temporal model")


def link_knowledge_to_circles(graph):
    """Link knowledge sources to relevant circles."""

    # Link sources to cosmos circle (meta-knowledge about knowledge)
    graph.query("""
        MATCH (s:Source)
        MATCH (c:Circle {name: 'cosmos'})
        MERGE (s)-[:IN_CIRCLE {created_at: $now, valid_at: $now}]->(c)
    """, {"now": datetime.now().isoformat()})

    # Link concepts to tools circle (techniques we can use)
    graph.query("""
        MATCH (concept:Concept)
        MATCH (c:Circle {name: 'tools'})
        MERGE (concept)-[:INFORMS {created_at: $now, valid_at: $now}]->(c)
    """, {"now": datetime.now().isoformat()})

    # Link techniques to tools circle
    graph.query("""
        MATCH (t:Technique)
        MATCH (c:Circle {name: 'tools'})
        MERGE (t)-[:IN_CIRCLE {created_at: $now, valid_at: $now}]->(c)
    """, {"now": datetime.now().isoformat()})

    print("Linked knowledge to circles")


def create_knowledge_graph_entity(graph):
    """Add FalkorDB and the exploration graph as entities."""

    now = datetime.now().isoformat()

    # Add FalkorDB as a tool entity
    graph.query("""
        MERGE (f:Entity:Software {id: 'sw-falkordb'})
        SET f.name = 'FalkorDB',
            f.type = 'Software',
            f.purpose = 'graph-database',
            f.port_browser = 3001,
            f.port_redis = 6380,
            f.first_seen = $now
        WITH f
        MATCH (c:Circle {name: 'tools'})
        MERGE (f)-[:IN_CIRCLE {created_at: $now, valid_at: $now}]->(c)
        WITH f
        MATCH (host:Entity {id: 'hw-host'})
        MERGE (f)-[:RUNS_ON {created_at: $now, valid_at: $now}]->(host)
    """, {"now": now})

    # Add the exploration graph itself as an entity
    graph.query("""
        MERGE (g:Entity:KnowledgeGraph {id: 'kg-exploration'})
        SET g.name = 'Exploration Knowledge Graph',
            g.type = 'KnowledgeGraph',
            g.purpose = 'environmental-model',
            g.graph_name = 'exploration',
            g.first_seen = $now
        WITH g
        MATCH (f:Entity {id: 'sw-falkordb'})
        MERGE (g)-[:STORED_IN {created_at: $now, valid_at: $now}]->(f)
        WITH g
        MATCH (c:Circle {name: 'tools'})
        MERGE (g)-[:IN_CIRCLE {created_at: $now, valid_at: $now}]->(c)
    """, {"now": now})

    # Link exploration plugin to the graph
    graph.query("""
        MATCH (p:Entity {id: 'plugin-exploration'})
        MATCH (g:Entity {id: 'kg-exploration'})
        MERGE (p)-[:PRODUCES {created_at: $now, valid_at: $now}]->(g)
    """, {"now": now})

    print("Added FalkorDB and exploration graph as entities")


def print_summary(graph):
    """Print updated graph statistics."""

    result = graph.query("""
        MATCH (n)
        RETURN labels(n)[0] as type, count(n) as count
        ORDER BY count DESC
    """)

    print("\n=== Updated Graph Summary ===")
    print("\nNode counts:")
    for record in result.result_set:
        print(f"  {record[0]}: {record[1]}")

    result = graph.query("""
        MATCH ()-[r]->()
        RETURN type(r) as type, count(r) as count
        ORDER BY count DESC
        LIMIT 15
    """)

    print("\nRelationship counts:")
    for record in result.result_set:
        print(f"  {record[0]}: {record[1]}")

    # Count temporal relationships
    result = graph.query("""
        MATCH ()-[r]->()
        WHERE r.valid_at IS NOT NULL
        RETURN count(r) as temporal_edges
    """)
    print(f"\nTemporal edges: {result.result_set[0][0]}")

    # Count knowledge nodes
    result = graph.query("""
        MATCH (k:Knowledge)
        RETURN count(k) as knowledge_nodes
    """)
    print(f"Knowledge nodes: {result.result_set[0][0]}")


def main():
    print("Connecting to FalkorDB...")
    graph = get_graph()

    print("\n=== Phase 1: Ingesting Knowledge Sources ===")
    add_knowledge_sources(graph)

    print("\n=== Phase 2: Extracting Concepts ===")
    add_concepts(graph)

    print("\n=== Phase 3: Adding Techniques ===")
    add_techniques(graph)

    print("\n=== Phase 4: Upgrading to Bi-Temporal Model ===")
    upgrade_to_bitemporal(graph)

    print("\n=== Phase 5: Linking Knowledge to Circles ===")
    link_knowledge_to_circles(graph)

    print("\n=== Phase 6: Adding Graph Self-Reference ===")
    create_knowledge_graph_entity(graph)

    print_summary(graph)

    print("\n✓ Knowledge ingestion and temporal upgrade complete!")
    print("  View at: http://localhost:3001")
    print("  Try: MATCH (k:Knowledge)-[r]->(x) RETURN k, r, x")


if __name__ == "__main__":
    main()
