#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "falkordb",
# ]
# ///
"""
Concept Ingestion: Load concepts from the concept registry into FalkorDB.

Creates a semantic layer in the knowledge graph:
- (:Concept) - Named concepts with definitions
- (:Document) - Source documents
- [:RELATES_TO] - Concept-to-concept relationships
- [:INTRODUCED_IN] - Concept source provenance

Usage:
    uv run ingest_concepts.py

Database: concepts (FalkorDB)
"""

from datetime import datetime
from falkordb import FalkorDB

# Concept definitions extracted from .claude/concepts/index.md
CONCEPTS = [
    {
        "name": "Phase Transition",
        "definition": "A fundamental reorganization of a system's structure. In this ecosystem: chaos→structure (Phase 1, complete) and structure→semantics (Phase 2, beginning).",
        "introduced": "2025-12-13",
        "source": ".claude/journal/2025/12/13/19-00-the-phase-transition.md",
        "status": "active",
        "related": ["Creation Addiction", "Semantic Coherence", "Potential Energy"]
    },
    {
        "name": "Creation Addiction",
        "definition": "The preference for existence over function. Finding it more satisfying to create new things than to activate existing ones.",
        "introduced": "2025-12-13",
        "source": ".claude/journal/2025/12/13/19-00-the-phase-transition.md",
        "status": "active",
        "related": ["Phase Transition", "Potential Energy", "Activation"]
    },
    {
        "name": "Semantic Coherence",
        "definition": "The degree to which concepts are extracted, linked, and queryable across artifacts. Measured 1-10.",
        "introduced": "2025-12-13",
        "source": ".claude/archive/assessments/2025-12-13-multi-agent-ecosystem-assessment.md",
        "status": "active",
        "related": ["Structural Coherence", "External Coherence", "Phase Transition"]
    },
    {
        "name": "Potential Energy",
        "definition": "Stored capacity to do work that hasn't been released. Defined agents not activated, structures not filled.",
        "introduced": "2025-12-13",
        "source": ".claude/journal/2025/12/13/19-00-the-phase-transition.md",
        "status": "active",
        "related": ["Kinetic Energy", "Creation Addiction", "Dormant Agents"]
    },
    {
        "name": "Kinetic Energy",
        "definition": "Work actually happening. Agents producing, concepts flowing, resources catalogued, facts verified.",
        "introduced": "2025-12-13",
        "source": ".claude/journal/2025/12/13/19-00-the-phase-transition.md",
        "status": "active",
        "related": ["Potential Energy", "Activation"]
    },
    {
        "name": "Master Skill Pattern",
        "definition": "Plugin architecture using progressive disclosure. One master SKILL.md lists sub-skills; sub-skills loaded on-demand.",
        "introduced": "2025-12-13",
        "source": "CLAUDE.md",
        "status": "verified",
        "related": ["Progressive Disclosure", "Plugin Architecture"]
    },
    {
        "name": "Metabolic Model",
        "definition": "Understanding the ecosystem as organism: ingestion (new info), processing (analysis), output (artifacts), excretion (commits).",
        "introduced": "2025-12-13",
        "source": ".claude/agents/archivist.md",
        "status": "active",
        "related": ["Metabolic Health", "Archivist"]
    },
    {
        "name": "Proactive Commit Discipline",
        "definition": "Committing immediately after semantic units, not batching. Git as coordination layer where commits are messages.",
        "introduced": "2025-12-13",
        "source": ".claude/conventions/coordination.md",
        "status": "active",
        "related": ["Git as Coordination Layer", "Semantic Unit"]
    },
    {
        "name": "Dormant Agents",
        "definition": "Agents defined (markdown files exist) but never activated (never invoked for real work). Potential energy.",
        "introduced": "2025-12-13",
        "source": ".claude/archive/patterns/agent-activity.md",
        "status": "active",
        "related": ["Potential Energy", "Activation"]
    },
    {
        "name": "Activation",
        "definition": "Giving a dormant agent its first real task. Converts potential to kinetic energy.",
        "introduced": "2025-12-15",
        "source": ".claude/journal/2025/12/13/19-00-the-phase-transition.md",
        "status": "active",
        "related": ["Dormant Agents", "Kinetic Energy", "Phase Transition"]
    }
]


def create_schema(g):
    """Create indices for concept graph."""
    indices = [
        "CREATE INDEX FOR (c:Concept) ON (c.name)",
        "CREATE INDEX FOR (c:Concept) ON (c.status)",
        "CREATE INDEX FOR (d:Document) ON (d.path)",
    ]
    for idx in indices:
        try:
            g.query(idx)
        except Exception:
            pass  # Index may already exist


def clear_concepts(g):
    """Clear existing concept data."""
    g.query("MATCH (c:Concept) DETACH DELETE c")
    g.query("MATCH (d:Document) WHERE d.type = 'concept_source' DETACH DELETE d")
    print("Cleared existing concepts")


def ingest_concepts(g):
    """Ingest concepts into the graph."""
    # First pass: Create all concept nodes
    for concept in CONCEPTS:
        query = """
        MERGE (c:Concept {name: $name})
        SET c.definition = $definition,
            c.introduced = $introduced,
            c.status = $status,
            c.ingested_at = $now
        """
        g.query(query, {
            "name": concept["name"],
            "definition": concept["definition"],
            "introduced": concept["introduced"],
            "status": concept["status"],
            "now": datetime.now().isoformat()
        })

        # Create source document node and link
        source_query = """
        MERGE (d:Document {path: $path})
        SET d.type = 'concept_source'
        WITH d
        MATCH (c:Concept {name: $concept_name})
        MERGE (c)-[:INTRODUCED_IN]->(d)
        """
        g.query(source_query, {
            "path": concept["source"],
            "concept_name": concept["name"]
        })

    print(f"Created {len(CONCEPTS)} concept nodes")

    # Second pass: Create relationships between concepts
    relationship_count = 0
    for concept in CONCEPTS:
        for related_name in concept.get("related", []):
            # Only create if related concept exists
            rel_query = """
            MATCH (a:Concept {name: $from_name})
            MATCH (b:Concept {name: $to_name})
            MERGE (a)-[:RELATES_TO]->(b)
            """
            try:
                result = g.query(rel_query, {
                    "from_name": concept["name"],
                    "to_name": related_name
                })
                relationship_count += 1
            except Exception:
                pass  # Related concept may not exist yet

    print(f"Created {relationship_count} relationships")


def print_summary(g):
    """Print graph summary."""
    concepts = g.query("MATCH (c:Concept) RETURN count(c) as count").result_set[0][0]
    documents = g.query("MATCH (d:Document) WHERE d.type = 'concept_source' RETURN count(d) as count").result_set[0][0]
    relationships = g.query("MATCH ()-[r:RELATES_TO]->() RETURN count(r) as count").result_set[0][0]
    intros = g.query("MATCH ()-[r:INTRODUCED_IN]->() RETURN count(r) as count").result_set[0][0]

    print("\n--- Concept Graph Summary ---")
    print(f"  Concepts: {concepts}")
    print(f"  Source Documents: {documents}")
    print(f"  RELATES_TO edges: {relationships}")
    print(f"  INTRODUCED_IN edges: {intros}")


def explore_graph(g):
    """Show some interesting queries."""
    print("\n--- Sample Queries ---\n")

    # Most connected concepts
    print("Most connected concepts:")
    result = g.query("""
        MATCH (c:Concept)-[r]->()
        RETURN c.name, count(r) as connections
        ORDER BY connections DESC
        LIMIT 5
    """)
    for row in result.result_set:
        print(f"  {row[0]}: {row[1]} connections")

    # Concepts by status
    print("\nConcepts by status:")
    result = g.query("""
        MATCH (c:Concept)
        RETURN c.status, count(c) as count
    """)
    for row in result.result_set:
        print(f"  {row[0]}: {row[1]}")

    # Path between concepts
    print("\nPath: Phase Transition → Activation")
    result = g.query("""
        MATCH path = (a:Concept {name: 'Phase Transition'})-[:RELATES_TO*1..3]->(b:Concept {name: 'Activation'})
        RETURN [n in nodes(path) | n.name] as path
        LIMIT 3
    """)
    for row in result.result_set:
        print(f"  {' → '.join(row[0])}")


def main():
    # Connect to FalkorDB (port 6380 based on docker mapping)
    db = FalkorDB(host="localhost", port=6380)
    g = db.select_graph("concepts")

    print("Connected to FalkorDB (concepts graph)")

    # Create schema
    create_schema(g)

    # Clear and re-ingest
    clear_concepts(g)

    # Ingest concepts
    ingest_concepts(g)

    # Print summary
    print_summary(g)

    # Explore
    explore_graph(g)

    print("\n✓ Concept ingestion complete")


if __name__ == "__main__":
    main()
