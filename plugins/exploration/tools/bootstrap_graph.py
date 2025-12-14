#!/usr/bin/env python3
"""
Bootstrap the Exploration Knowledge Graph

Seeds Neo4j with exploration discoveries, creating nodes for:
- Circles (substrate, tools, network, history, cosmos)
- Discovered entities (hardware, software, services, etc.)
- Discoveries and questions
- Relationships between them

Usage:
    python bootstrap_graph.py [--uri URI] [--user USER] [--password PASSWORD]

Environment variables:
    NEO4J_URI (default: bolt://localhost:7687)
    NEO4J_USERNAME (default: neo4j)
    NEO4J_PASSWORD (default: graphiti123)
"""

import os
import argparse
from datetime import datetime

# Neo4j connection settings
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "graphiti123")


def get_driver():
    """Get Neo4j driver, installing if necessary."""
    try:
        from neo4j import GraphDatabase
        return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    except ImportError:
        print("Installing neo4j driver...")
        import subprocess
        subprocess.run(["uv", "pip", "install", "neo4j"], check=True)
        from neo4j import GraphDatabase
        return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def create_exploration_schema(session):
    """Create constraints and indexes for exploration nodes."""
    constraints = [
        "CREATE CONSTRAINT exploration_circle_name IF NOT EXISTS FOR (c:ExplorationCircle) REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT exploration_discovery_id IF NOT EXISTS FOR (d:ExplorationDiscovery) REQUIRE d.id IS UNIQUE",
        "CREATE CONSTRAINT exploration_question_id IF NOT EXISTS FOR (q:ExplorationQuestion) REQUIRE q.id IS UNIQUE",
        "CREATE CONSTRAINT exploration_entity_id IF NOT EXISTS FOR (e:ExplorationEntity) REQUIRE e.id IS UNIQUE",
    ]
    for constraint in constraints:
        try:
            session.run(constraint)
        except Exception as e:
            if "already exists" not in str(e).lower():
                print(f"Warning: {e}")


def seed_circles(session):
    """Create the five concentric circles."""
    circles = [
        {"name": "substrate", "description": "Machine, OS, hardware, filesystems", "mastery": 0.55},
        {"name": "tools", "description": "Claude Code, MCP, plugins, capabilities", "mastery": 0.45},
        {"name": "network", "description": "Connectivity, containers, services", "mastery": 0.40},
        {"name": "history", "description": "Git, evolution, decisions, patterns", "mastery": 0.35},
        {"name": "cosmos", "description": "Natural laws, physics, meaning", "mastery": 0.25},
    ]

    query = """
    UNWIND $circles AS circle
    MERGE (c:ExplorationCircle {name: circle.name})
    SET c.description = circle.description,
        c.mastery = circle.mastery,
        c.updated = datetime()
    RETURN c.name
    """
    result = session.run(query, circles=circles)
    print(f"Created/updated {len(list(result))} circles")


def seed_substrate_entities(session):
    """Seed entities discovered in substrate exploration."""
    import json
    entities = [
        # Hardware
        {"id": "hw-host", "type": "Hardware", "name": "Lenovo 90UT", "role": "desktop", "vendor": "Lenovo"},
        {"id": "hw-cpu", "type": "Hardware", "name": "Intel i7-13700F", "cores": 16, "threads": 24, "max_mhz": 5200},
        {"id": "hw-gpu", "type": "Hardware", "name": "NVIDIA RTX 4070", "vram_gb": 12, "driver": "580.82"},
        {"id": "hw-ram", "type": "Hardware", "name": "System RAM", "total_gb": 32, "available_gb": 24},
        {"id": "hw-storage", "type": "Hardware", "name": "NVMe SSD", "size_gb": 929, "used_percent": 75},

        # Software
        {"id": "sw-os", "type": "Software", "name": "Pop!_OS 22.04", "base": "Ubuntu", "vendor": "System76"},
        {"id": "sw-kernel", "type": "Software", "name": "Linux 6.17.4", "kernel_type": "mainline"},
        {"id": "sw-claude", "type": "Software", "name": "Claude Code 2.0.67", "sessions": 79},
        {"id": "sw-python", "type": "Software", "name": "Python 3.13.2", "manager": "uv"},

        # Terminal
        {"id": "term-tmux", "type": "Software", "name": "tmux", "socket": "/tmp/tmux-1000/default"},
        {"id": "term-alacritty", "type": "Software", "name": "Alacritty", "colorterm": "truecolor"},
    ]

    for entity in entities:
        entity_id = entity.pop("id")
        entity_type = entity.pop("type")
        entity_name = entity.pop("name")
        # Store remaining fields as individual properties
        props_str = ", ".join([f"e.{k} = ${k}" for k in entity.keys()])

        query = f"""
        MERGE (e:ExplorationEntity {{id: $entity_id}})
        SET e.type = $entity_type,
            e.name = $entity_name,
            e.first_seen = datetime(),
            e.circle = 'substrate'
            {', ' + props_str if props_str else ''}
        WITH e
        MATCH (c:ExplorationCircle {{name: 'substrate'}})
        MERGE (e)-[:PART_OF]->(c)
        RETURN e.name
        """
        session.run(query, entity_id=entity_id, entity_type=entity_type, entity_name=entity_name, **entity)

    print(f"Created/updated {len(entities)} substrate entities")

    # Create hardware relationships
    relationships = [
        ("hw-cpu", "hw-host", "PART_OF"),
        ("hw-gpu", "hw-host", "PART_OF"),
        ("hw-ram", "hw-host", "PART_OF"),
        ("hw-storage", "hw-host", "PART_OF"),
        ("sw-os", "hw-host", "RUNS_ON"),
        ("sw-kernel", "sw-os", "PART_OF"),
        ("sw-claude", "term-tmux", "RUNS_IN"),
        ("term-tmux", "term-alacritty", "RUNS_IN"),
    ]

    rel_query = """
    UNWIND $rels AS rel
    MATCH (a:ExplorationEntity {id: rel[0]})
    MATCH (b:ExplorationEntity {id: rel[1]})
    CALL apoc.merge.relationship(a, rel[2], {}, {}, b) YIELD rel AS r
    RETURN count(r)
    """
    # Fallback without APOC
    for src, tgt, rtype in relationships:
        try:
            session.run(f"""
                MATCH (a:ExplorationEntity {{id: $src}})
                MATCH (b:ExplorationEntity {{id: $tgt}})
                MERGE (a)-[:{rtype}]->(b)
            """, src=src, tgt=tgt)
        except Exception as e:
            print(f"Warning creating relationship: {e}")


def seed_network_entities(session):
    """Seed entities discovered in network exploration."""
    entities = [
        # Containers
        {"id": "container-neo4j", "type": "Container", "name": "graphiti-neo4j", "image": "neo4j:5.26", "port_http": 7474, "port_bolt": 7687},
        {"id": "container-pgvector", "type": "Container", "name": "regenai-postgres", "image": "pgvector", "port": 5435},
        {"id": "container-redis", "type": "Container", "name": "autoflow-redis", "image": "redis:7-alpine"},
        {"id": "container-timescale", "type": "Container", "name": "autoflow-timescaledb", "image": "timescaledb:2.13.1-pg15"},

        # Networks
        {"id": "net-wifi", "type": "Network", "name": "wlo1", "ip": "192.168.1.251", "net_type": "wifi"},
        {"id": "net-docker", "type": "Network", "name": "docker0", "ip": "172.17.0.1", "net_type": "bridge"},

        # Location
        {"id": "loc-city", "type": "Location", "name": "Vancouver, BC", "country": "Canada", "timezone": "America/Vancouver", "coords": "49.25,-123.12"},
    ]

    for entity in entities:
        entity_id = entity.pop("id")
        entity_type = entity.pop("type")
        entity_name = entity.pop("name")
        props_str = ", ".join([f"e.{k} = ${k}" for k in entity.keys()])

        query = f"""
        MERGE (e:ExplorationEntity {{id: $entity_id}})
        SET e.type = $entity_type,
            e.name = $entity_name,
            e.first_seen = datetime(),
            e.circle = 'network'
            {', ' + props_str if props_str else ''}
        WITH e
        MATCH (c:ExplorationCircle {{name: 'network'}})
        MERGE (e)-[:PART_OF]->(c)
        RETURN e.name
        """
        session.run(query, entity_id=entity_id, entity_type=entity_type, entity_name=entity_name, **entity)

    print(f"Created/updated {len(entities)} network entities")

    # Container relationships
    for container in ["container-neo4j", "container-pgvector", "container-redis", "container-timescale"]:
        session.run("""
            MATCH (c:ExplorationEntity {id: $container})
            MATCH (h:ExplorationEntity {id: 'hw-host'})
            MERGE (c)-[:RUNS_ON]->(h)
        """, container=container)


def seed_tool_entities(session):
    """Seed entities discovered in tool exploration."""
    entities = [
        # Plugins
        {"id": "plugin-awareness", "type": "Plugin", "name": "awareness", "skills": 7, "purpose": "self-improvement"},
        {"id": "plugin-exploration", "type": "Plugin", "name": "exploration", "skills": 7, "purpose": "environmental-literacy"},
        {"id": "plugin-journal", "type": "Plugin", "name": "journal", "skills": 6, "purpose": "knowledge-management"},
        {"id": "plugin-logging", "type": "Plugin", "name": "logging", "skills": 2, "purpose": "observability"},
        {"id": "plugin-schedule", "type": "Plugin", "name": "schedule", "skills": 2, "purpose": "time-management"},
        {"id": "plugin-backlog", "type": "Plugin", "name": "backlog", "skills": 2, "purpose": "task-management"},
        {"id": "plugin-agents", "type": "Plugin", "name": "agents", "skills": 15, "purpose": "agent-frameworks"},
        {"id": "plugin-llms", "type": "Plugin", "name": "llms", "skills": 10, "purpose": "llm-patterns"},

        # MCP Servers
        {"id": "mcp-schedule", "type": "MCPServer", "name": "schedule-mcp", "tools": 9},
        {"id": "mcp-backlog", "type": "MCPServer", "name": "backlog-mcp"},
        {"id": "mcp-playwright", "type": "MCPServer", "name": "playwright-mcp", "purpose": "browser-automation"},
    ]

    for entity in entities:
        entity_id = entity.pop("id")
        entity_type = entity.pop("type")
        entity_name = entity.pop("name")
        props_str = ", ".join([f"e.{k} = ${k}" for k in entity.keys()])

        query = f"""
        MERGE (e:ExplorationEntity {{id: $entity_id}})
        SET e.type = $entity_type,
            e.name = $entity_name,
            e.first_seen = datetime(),
            e.circle = 'tools'
            {', ' + props_str if props_str else ''}
        WITH e
        MATCH (c:ExplorationCircle {{name: 'tools'}})
        MERGE (e)-[:PART_OF]->(c)
        RETURN e.name
        """
        session.run(query, entity_id=entity_id, entity_type=entity_type, entity_name=entity_name, **entity)

    print(f"Created/updated {len(entities)} tool entities")

    # Plugin relationships
    session.run("""
        MATCH (p:ExplorationEntity {id: 'plugin-exploration'})
        MATCH (a:ExplorationEntity {id: 'plugin-awareness'})
        MERGE (p)-[:COMPLEMENTS]->(a)
    """)


def seed_initial_discovery(session):
    """Create the initial discovery node."""
    query = """
    MERGE (d:ExplorationDiscovery {id: 'discovery-20251212-initial'})
    SET d.date = date('2025-12-12'),
        d.summary = 'Initial comprehensive exploration of environment: Lenovo desktop with i7-13700F, RTX 4070, 32GB RAM running Pop!_OS. Docker infrastructure with Neo4j, PgVector, TimescaleDB, Redis. Claude Code 2.0.67 with 10 plugins. Location: Vancouver, BC.',
        d.mastery_delta = 0.4,
        d.session_type = 'initialization'

    WITH d
    MATCH (c:ExplorationCircle)
    MERGE (d)-[:EXPLORED]->(c)

    WITH d
    MATCH (e:ExplorationEntity)
    WHERE e.circle IN ['substrate', 'network', 'tools']
    MERGE (d)-[:DISCOVERED]->(e)

    RETURN d.id
    """
    session.run(query)
    print("Created initial discovery node with relationships")


def seed_questions(session):
    """Seed open questions from the question bank."""
    questions = [
        {"id": "q-docker-orch", "text": "How are Docker containers orchestrated?", "priority": "high", "circle": "network"},
        {"id": "q-neo4j-data", "text": "What data exists in Neo4j?", "priority": "high", "circle": "network"},
        {"id": "q-mcp-unused", "text": "What MCP tools are available but unused?", "priority": "high", "circle": "tools"},
        {"id": "q-graphiti-rel", "text": "How does Graphiti use the Neo4j container?", "priority": "high", "circle": "network"},
        {"id": "q-agent-diff", "text": "How do the 15+ agent framework skills differ?", "priority": "high", "circle": "tools"},
        {"id": "q-decisions", "text": "What were the key decision points in project evolution?", "priority": "high", "circle": "history"},
        {"id": "q-landauer", "text": "What are the Landauer limits for this hardware?", "priority": "medium", "circle": "cosmos"},
    ]

    query = """
    UNWIND $questions AS q
    MERGE (question:ExplorationQuestion {id: q.id})
    SET question.text = q.text,
        question.priority = q.priority,
        question.status = 'open',
        question.created = datetime()
    WITH question, q
    MATCH (c:ExplorationCircle {name: q.circle})
    MERGE (question)-[:IN_CIRCLE]->(c)
    RETURN question.id
    """
    result = session.run(query, questions=questions)
    print(f"Created/updated {len(list(result))} questions")

    # Link questions to entities
    entity_links = [
        ("q-docker-orch", "container-neo4j"),
        ("q-neo4j-data", "container-neo4j"),
        ("q-graphiti-rel", "container-neo4j"),
        ("q-mcp-unused", "mcp-schedule"),
        ("q-agent-diff", "plugin-agents"),
    ]
    for q_id, e_id in entity_links:
        session.run("""
            MATCH (q:ExplorationQuestion {id: $q_id})
            MATCH (e:ExplorationEntity {id: $e_id})
            MERGE (q)-[:ABOUT]->(e)
        """, q_id=q_id, e_id=e_id)


def create_cross_circle_connections(session):
    """Create relationships between entities in different circles."""
    connections = [
        # Containers run on hardware
        ("container-neo4j", "hw-host", "RUNS_ON"),
        ("container-pgvector", "hw-host", "RUNS_ON"),

        # Software uses hardware
        ("sw-claude", "hw-gpu", "CAN_USE"),
        ("container-neo4j", "hw-storage", "USES"),

        # Plugins connect to network
        ("plugin-schedule", "mcp-schedule", "USES"),
        ("plugin-backlog", "mcp-backlog", "USES"),

        # Tools use containers
        ("mcp-playwright", "sw-claude", "PART_OF"),
    ]

    for src, tgt, rtype in connections:
        try:
            session.run(f"""
                MATCH (a:ExplorationEntity {{id: $src}})
                MATCH (b:ExplorationEntity {{id: $tgt}})
                MERGE (a)-[:{rtype}]->(b)
            """, src=src, tgt=tgt)
        except Exception as e:
            print(f"Warning creating cross-circle connection: {e}")

    print("Created cross-circle connections")


def main():
    parser = argparse.ArgumentParser(description="Bootstrap Exploration Knowledge Graph")
    parser.add_argument("--uri", default=NEO4J_URI, help="Neo4j URI")
    parser.add_argument("--user", default=NEO4J_USER, help="Neo4j username")
    parser.add_argument("--password", default=NEO4J_PASSWORD, help="Neo4j password")
    args = parser.parse_args()

    print(f"Connecting to Neo4j at {args.uri}...")

    driver = get_driver()

    with driver.session() as session:
        print("\n=== Creating Schema ===")
        create_exploration_schema(session)

        print("\n=== Seeding Circles ===")
        seed_circles(session)

        print("\n=== Seeding Substrate Entities ===")
        seed_substrate_entities(session)

        print("\n=== Seeding Network Entities ===")
        seed_network_entities(session)

        print("\n=== Seeding Tool Entities ===")
        seed_tool_entities(session)

        print("\n=== Creating Initial Discovery ===")
        seed_initial_discovery(session)

        print("\n=== Seeding Questions ===")
        seed_questions(session)

        print("\n=== Creating Cross-Circle Connections ===")
        create_cross_circle_connections(session)

        # Summary
        result = session.run("""
            MATCH (n)
            WHERE n:ExplorationCircle OR n:ExplorationDiscovery
                  OR n:ExplorationQuestion OR n:ExplorationEntity
            RETURN labels(n)[0] as type, count(n) as count
            ORDER BY type
        """)

        print("\n=== Knowledge Graph Summary ===")
        for record in result:
            print(f"  {record['type']}: {record['count']} nodes")

        # Count relationships
        rel_result = session.run("""
            MATCH ()-[r]->()
            WHERE startNode(r):ExplorationEntity OR startNode(r):ExplorationDiscovery
                  OR startNode(r):ExplorationQuestion OR startNode(r):ExplorationCircle
            RETURN count(r) as total
        """)
        print(f"  Relationships: {rel_result.single()['total']} edges")

    driver.close()
    print("\n✓ Exploration knowledge graph bootstrapped successfully!")
    print("  View at: http://localhost:7474")
    print("  Query: MATCH (n:ExplorationEntity)-[r]->(m) RETURN n, r, m")


if __name__ == "__main__":
    main()
