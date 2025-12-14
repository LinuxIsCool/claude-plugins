#!/usr/bin/env python3
"""
Self-Improving Memory for Exploration Knowledge Graph

Implements the Mem0-style pattern for building a memory that learns from:
1. Automatic fact extraction from conversations/discoveries
2. Self-healing contradictions (new facts invalidate old ones)
3. Query-driven improvement (track success/failure, adjust confidence)
4. Gap detection (identify areas needing more exploration)

Usage:
    # Add a memory
    python memory.py add "Neo4j runs on port 7474"

    # Search memories
    python memory.py search "database ports"

    # Record feedback
    python memory.py feedback --helpful "neo4j port query"

    # Find contradictions
    python memory.py contradictions

    # Generate exploration questions
    python memory.py gaps
"""

import os
import json
import argparse
from datetime import datetime
from dataclasses import dataclass, field
from typing import Literal

FALKOR_HOST = os.environ.get("FALKORDB_HOST", "localhost")
FALKOR_PORT = int(os.environ.get("FALKORDB_PORT", "6380"))
GRAPH_NAME = "exploration"


@dataclass
class Memory:
    """A single memory/fact in the system."""
    id: str
    content: str
    category: str  # fact, observation, preference, inference
    confidence: float = 0.7
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    valid_at: str = field(default_factory=lambda: datetime.now().isoformat())
    invalid_at: str | None = None
    source: str = "user"
    query_hits: int = 0
    helpful_feedback: int = 0
    unhelpful_feedback: int = 0


@dataclass
class QueryLog:
    """Log of a query and its outcome."""
    query: str
    timestamp: str
    results_count: int
    was_helpful: bool | None = None
    entities_returned: list[str] = field(default_factory=list)


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


def escape_cypher(value: str) -> str:
    """Escape a string for Cypher query."""
    return value.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')


# =============================================================================
# Memory Operations
# =============================================================================

def add_memory(content: str, category: str = "fact", source: str = "user") -> Memory:
    """
    Add a new memory to the knowledge graph.
    Checks for contradictions and handles them.
    """
    graph = get_falkordb()
    now = datetime.now().isoformat()
    memory_id = f"memory-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}"

    safe_content = escape_cypher(content)

    # Check for potential contradictions
    contradictions = find_contradictions(content)

    # If contradictions found, invalidate old memories
    for old_memory_id in contradictions:
        invalidate_memory(old_memory_id, reason=f"Superseded by {memory_id}")

    # Create the memory node
    query = f"""
    CREATE (m:Memory {{
        id: '{memory_id}',
        content: '{safe_content}',
        category: '{category}',
        confidence: 0.7,
        created_at: '{now}',
        valid_at: '{now}',
        source: '{source}',
        query_hits: 0,
        helpful_feedback: 0,
        unhelpful_feedback: 0
    }})
    RETURN m.id
    """

    graph.query(query)

    # Link to relevant entities (simple keyword matching)
    link_memory_to_entities(graph, memory_id, content)

    return Memory(
        id=memory_id,
        content=content,
        category=category,
        source=source
    )


def link_memory_to_entities(graph, memory_id: str, content: str):
    """Link memory to relevant entities based on content."""
    content_lower = content.lower()

    # Find entities whose names appear in the content
    result = graph.query("MATCH (e:Entity) RETURN e.name")

    for row in result.result_set:
        entity_name = row[0]
        if entity_name and entity_name.lower() in content_lower:
            safe_name = escape_cypher(entity_name)
            now = datetime.now().isoformat()
            link_query = f"""
            MATCH (m:Memory {{id: '{memory_id}'}})
            MATCH (e:Entity {{name: '{safe_name}'}})
            CREATE (m)-[:ABOUT {{created_at: '{now}'}}]->(e)
            """
            try:
                graph.query(link_query)
            except Exception:
                pass  # Ignore if link already exists


def find_contradictions(new_content: str) -> list[str]:
    """
    Find memories that might contradict the new content.
    Uses simple heuristics based on entity mentions and fact patterns.
    """
    graph = get_falkordb()
    contradicting_ids = []

    # Extract key entities from new content
    new_lower = new_content.lower()

    # Look for patterns like "X is Y" or "X uses port Y"
    # If existing memories say "X is Z" where Z != Y, that's a contradiction

    # Simple approach: find memories about same entities with different values
    result = graph.query("""
        MATCH (m:Memory)
        WHERE m.invalid_at IS NULL
        RETURN m.id, m.content
    """)

    for row in result.result_set:
        memory_id, old_content = row
        if not old_content:
            continue

        old_lower = old_content.lower()

        # Check for version/port contradictions
        version_patterns = [
            ("version", "is"),
            ("port", ":"),
            ("runs on", "port"),
        ]

        for pattern, separator in version_patterns:
            if pattern in new_lower and pattern in old_lower:
                # Both mention same pattern - might be contradiction
                # Extract the values and compare
                new_parts = new_lower.split(pattern)
                old_parts = old_lower.split(pattern)

                if len(new_parts) > 1 and len(old_parts) > 1:
                    # Check if they're about the same subject
                    new_subject = new_parts[0].strip().split()[-1] if new_parts[0].strip() else ""
                    old_subject = old_parts[0].strip().split()[-1] if old_parts[0].strip() else ""

                    if new_subject == old_subject and new_parts[1].strip() != old_parts[1].strip():
                        contradicting_ids.append(memory_id)
                        break

    return contradicting_ids


def invalidate_memory(memory_id: str, reason: str = ""):
    """Mark a memory as invalid (superseded by newer information)."""
    graph = get_falkordb()
    now = datetime.now().isoformat()
    safe_reason = escape_cypher(reason)

    query = f"""
    MATCH (m:Memory {{id: '{memory_id}'}})
    SET m.invalid_at = '{now}', m.invalidation_reason = '{safe_reason}'
    RETURN m.id
    """

    graph.query(query)


def search_memories(query: str, limit: int = 10) -> list[Memory]:
    """
    Search memories by content similarity.
    Updates query_hits for accessed memories.
    """
    graph = get_falkordb()
    query_lower = query.lower()
    query_terms = query_lower.split()

    results = []

    # Find matching memories
    result = graph.query("""
        MATCH (m:Memory)
        WHERE m.invalid_at IS NULL
        RETURN m.id, m.content, m.category, m.confidence, m.created_at,
               m.valid_at, m.source, m.query_hits, m.helpful_feedback, m.unhelpful_feedback
    """)

    for row in result.result_set:
        memory_id, content, category, confidence, created_at, valid_at, source, hits, helpful, unhelpful = row

        if not content:
            continue

        content_lower = content.lower()

        # Score based on term matches
        score = sum(1 for term in query_terms if term in content_lower)

        if score > 0:
            results.append((score, Memory(
                id=memory_id,
                content=content,
                category=category or "fact",
                confidence=confidence or 0.7,
                created_at=created_at or "",
                valid_at=valid_at or "",
                source=source or "unknown",
                query_hits=hits or 0,
                helpful_feedback=helpful or 0,
                unhelpful_feedback=unhelpful or 0
            )))

    # Sort by score
    results.sort(key=lambda x: x[0], reverse=True)
    memories = [m for _, m in results[:limit]]

    # Update query hits
    for memory in memories:
        query = f"""
        MATCH (m:Memory {{id: '{memory.id}'}})
        SET m.query_hits = COALESCE(m.query_hits, 0) + 1
        """
        try:
            graph.query(query)
        except Exception:
            pass

    return memories


def record_feedback(query: str, was_helpful: bool):
    """
    Record feedback on search results.
    Adjusts confidence scores based on feedback.
    """
    graph = get_falkordb()

    # Find memories that were likely returned for this query
    memories = search_memories(query, limit=5)

    confidence_delta = 0.05 if was_helpful else -0.05

    for memory in memories:
        feedback_field = "helpful_feedback" if was_helpful else "unhelpful_feedback"

        query = f"""
        MATCH (m:Memory {{id: '{memory.id}'}})
        SET m.{feedback_field} = COALESCE(m.{feedback_field}, 0) + 1,
            m.confidence = CASE
                WHEN m.confidence + {confidence_delta} > 1.0 THEN 1.0
                WHEN m.confidence + {confidence_delta} < 0.1 THEN 0.1
                ELSE m.confidence + {confidence_delta}
            END
        """
        try:
            graph.query(query)
        except Exception:
            pass

    # If unhelpful, generate a question for this area
    if not was_helpful:
        generate_question_from_gap(query)


def generate_question_from_gap(failed_query: str):
    """Generate a question to address knowledge gaps."""
    graph = get_falkordb()
    now = datetime.now().isoformat()
    question_id = f"q-gap-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    safe_query = escape_cypher(failed_query)

    query = f"""
    CREATE (q:Question {{
        id: '{question_id}',
        text: 'Need more information about: {safe_query}',
        priority: 'medium',
        status: 'open',
        generated_from: 'memory_gap',
        created_at: '{now}'
    }})
    RETURN q.id
    """

    try:
        graph.query(query)
    except Exception:
        pass


# =============================================================================
# Analytics & Improvement
# =============================================================================

def get_memory_stats() -> dict:
    """Get statistics about the memory system."""
    graph = get_falkordb()

    stats = {}

    # Total memories
    result = graph.query("MATCH (m:Memory) RETURN count(m)")
    stats["total_memories"] = result.result_set[0][0] if result.result_set else 0

    # Active vs invalidated
    result = graph.query("MATCH (m:Memory) WHERE m.invalid_at IS NULL RETURN count(m)")
    stats["active_memories"] = result.result_set[0][0] if result.result_set else 0

    result = graph.query("MATCH (m:Memory) WHERE m.invalid_at IS NOT NULL RETURN count(m)")
    stats["invalidated_memories"] = result.result_set[0][0] if result.result_set else 0

    # By category
    result = graph.query("""
        MATCH (m:Memory) WHERE m.invalid_at IS NULL
        RETURN m.category, count(m)
    """)
    stats["by_category"] = {row[0]: row[1] for row in result.result_set if row[0]}

    # Average confidence
    result = graph.query("""
        MATCH (m:Memory) WHERE m.invalid_at IS NULL
        RETURN avg(m.confidence)
    """)
    stats["avg_confidence"] = round(result.result_set[0][0] or 0, 3)

    # Most queried
    result = graph.query("""
        MATCH (m:Memory) WHERE m.invalid_at IS NULL
        RETURN m.content, m.query_hits
        ORDER BY m.query_hits DESC LIMIT 5
    """)
    stats["most_queried"] = [(row[0][:50] + "..." if len(row[0] or "") > 50 else row[0], row[1])
                            for row in result.result_set]

    # Feedback summary
    result = graph.query("""
        MATCH (m:Memory)
        RETURN sum(m.helpful_feedback), sum(m.unhelpful_feedback)
    """)
    if result.result_set:
        stats["total_helpful"] = result.result_set[0][0] or 0
        stats["total_unhelpful"] = result.result_set[0][1] or 0

    return stats


def find_knowledge_gaps() -> list[dict]:
    """
    Identify areas where the knowledge graph needs improvement.
    Returns questions/areas needing more exploration.
    """
    graph = get_falkordb()
    gaps = []

    # Low confidence memories
    result = graph.query("""
        MATCH (m:Memory)
        WHERE m.invalid_at IS NULL AND m.confidence < 0.5
        RETURN m.id, m.content, m.confidence
        ORDER BY m.confidence ASC LIMIT 5
    """)

    for row in result.result_set:
        gaps.append({
            "type": "low_confidence",
            "memory_id": row[0],
            "content": row[1],
            "confidence": row[2],
            "suggestion": "Verify or update this information"
        })

    # Open questions
    result = graph.query("""
        MATCH (q:Question)
        WHERE q.status = 'open'
        RETURN q.id, q.text, q.priority
        ORDER BY
            CASE q.priority
                WHEN 'high' THEN 1
                WHEN 'medium' THEN 2
                ELSE 3
            END
        LIMIT 5
    """)

    for row in result.result_set:
        gaps.append({
            "type": "open_question",
            "question_id": row[0],
            "text": row[1],
            "priority": row[2],
            "suggestion": "Explore to answer this question"
        })

    # Circles with low entity count
    result = graph.query("""
        MATCH (c:Circle)
        OPTIONAL MATCH (e:Entity)-[:IN_CIRCLE]->(c)
        WITH c.name as circle, count(e) as entity_count
        WHERE entity_count < 5
        RETURN circle, entity_count
    """)

    for row in result.result_set:
        gaps.append({
            "type": "sparse_circle",
            "circle": row[0],
            "entity_count": row[1],
            "suggestion": f"Explore the {row[0]} circle more thoroughly"
        })

    return gaps


def boost_entity_confidence(entity_name: str, delta: float = 0.05):
    """Boost confidence of an entity based on successful queries."""
    graph = get_falkordb()
    safe_name = escape_cypher(entity_name)

    # Update confidence on related edges
    query = f"""
    MATCH (e:Entity {{name: '{safe_name}'}})-[r]-()
    WHERE r.confidence IS NOT NULL
    SET r.confidence = CASE
        WHEN r.confidence + {delta} > 1.0 THEN 1.0
        ELSE r.confidence + {delta}
    END
    RETURN count(r)
    """

    try:
        graph.query(query)
    except Exception:
        pass


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Self-improving memory for exploration graph")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Add memory
    add_parser = subparsers.add_parser("add", help="Add a new memory")
    add_parser.add_argument("content", help="Memory content")
    add_parser.add_argument("--category", default="fact",
                          choices=["fact", "observation", "preference", "inference"])
    add_parser.add_argument("--source", default="user")

    # Search memories
    search_parser = subparsers.add_parser("search", help="Search memories")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--limit", type=int, default=10)

    # Record feedback
    feedback_parser = subparsers.add_parser("feedback", help="Record feedback")
    feedback_parser.add_argument("query", help="Original query")
    feedback_parser.add_argument("--helpful", action="store_true")
    feedback_parser.add_argument("--unhelpful", action="store_true")

    # Find contradictions
    subparsers.add_parser("contradictions", help="Find potential contradictions")

    # Find gaps
    subparsers.add_parser("gaps", help="Find knowledge gaps")

    # Stats
    subparsers.add_parser("stats", help="Show memory statistics")

    args = parser.parse_args()

    if args.command == "add":
        memory = add_memory(args.content, args.category, args.source)
        print(f"Added memory: {memory.id}")
        print(f"  Content: {memory.content}")
        print(f"  Category: {memory.category}")

    elif args.command == "search":
        memories = search_memories(args.query, args.limit)
        print(f"\n=== Memory Search: '{args.query}' ===")
        print(f"Found {len(memories)} memories:\n")
        for m in memories:
            print(f"  [{m.category}] {m.content}")
            print(f"    Confidence: {m.confidence:.2f} | Hits: {m.query_hits}")
            print()

    elif args.command == "feedback":
        if args.helpful:
            record_feedback(args.query, was_helpful=True)
            print(f"Recorded HELPFUL feedback for: {args.query}")
        elif args.unhelpful:
            record_feedback(args.query, was_helpful=False)
            print(f"Recorded UNHELPFUL feedback for: {args.query}")
            print("Generated question to address this gap.")
        else:
            print("Specify --helpful or --unhelpful")

    elif args.command == "contradictions":
        # Show recently invalidated memories
        graph = get_falkordb()
        result = graph.query("""
            MATCH (m:Memory)
            WHERE m.invalid_at IS NOT NULL
            RETURN m.id, m.content, m.invalid_at, m.invalidation_reason
            ORDER BY m.invalid_at DESC LIMIT 10
        """)

        print("\n=== Invalidated Memories (Contradictions Resolved) ===\n")
        if not result.result_set:
            print("No contradictions found.")
        else:
            for row in result.result_set:
                print(f"  ID: {row[0]}")
                print(f"  Content: {row[1]}")
                print(f"  Invalidated: {row[2]}")
                print(f"  Reason: {row[3]}")
                print()

    elif args.command == "gaps":
        gaps = find_knowledge_gaps()
        print("\n=== Knowledge Gaps ===\n")
        if not gaps:
            print("No significant gaps found.")
        else:
            for gap in gaps:
                print(f"  Type: {gap['type']}")
                if 'content' in gap:
                    print(f"  Content: {gap['content']}")
                if 'text' in gap:
                    print(f"  Question: {gap['text']}")
                if 'circle' in gap:
                    print(f"  Circle: {gap['circle']}")
                print(f"  Suggestion: {gap['suggestion']}")
                print()

    elif args.command == "stats":
        stats = get_memory_stats()
        print("\n=== Memory System Statistics ===\n")
        print(f"  Total memories: {stats['total_memories']}")
        print(f"  Active: {stats['active_memories']}")
        print(f"  Invalidated: {stats['invalidated_memories']}")
        print(f"  Average confidence: {stats['avg_confidence']}")
        print(f"\n  By category:")
        for cat, count in stats.get('by_category', {}).items():
            print(f"    {cat}: {count}")
        print(f"\n  Feedback: {stats.get('total_helpful', 0)} helpful, {stats.get('total_unhelpful', 0)} unhelpful")
        print(f"\n  Most queried:")
        for content, hits in stats.get('most_queried', []):
            print(f"    [{hits} hits] {content}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
