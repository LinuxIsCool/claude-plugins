#!/usr/bin/env python3
"""
LLM-Powered Entity Extraction Pipeline for Exploration Knowledge Graph

Extracts entities and relationships from discovery text using local LLMs (Ollama)
or cloud APIs, then adds them to the FalkorDB knowledge graph with bi-temporal properties.

Three operating modes:
- direct: Rule-based extraction (free, fast, limited)
- ollama: Local LLM extraction (free, good quality)
- cloud: Cloud API extraction (best quality, costs money)

Usage:
    python extract_entities.py --text "Discovery text here..."
    python extract_entities.py --file discovery.md
    python extract_entities.py --interactive
"""

import os
import re
import json
import argparse
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

FALKOR_HOST = os.environ.get("FALKORDB_HOST", "localhost")
FALKOR_PORT = int(os.environ.get("FALKORDB_PORT", "6380"))
GRAPH_NAME = "exploration"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")


# Pydantic models for structured extraction
class ExtractedEntity(BaseModel):
    """An entity extracted from discovery text."""
    name: str = Field(description="Name of the entity")
    entity_type: Literal["hardware", "software", "container", "service", "network", "location", "concept"] = Field(
        description="Type of entity"
    )
    circle: Literal["substrate", "tools", "network", "history", "cosmos"] = Field(
        description="Which exploration circle this belongs to"
    )
    properties: dict = Field(default_factory=dict, description="Additional properties")
    confidence: float = Field(default=0.7, ge=0.0, le=1.0, description="Extraction confidence")


class ExtractedRelationship(BaseModel):
    """A relationship extracted between entities."""
    source: str = Field(description="Name of the source entity")
    target: str = Field(description="Name of the target entity")
    relationship: Literal["RUNS_ON", "PART_OF", "USES", "DEPENDS_ON", "CONNECTS_TO", "CONTAINS", "PRODUCES"] = Field(
        description="Type of relationship"
    )
    properties: dict = Field(default_factory=dict, description="Additional properties")
    confidence: float = Field(default=0.7, ge=0.0, le=1.0, description="Extraction confidence")


class ExtractionResult(BaseModel):
    """Complete extraction result from a discovery."""
    entities: list[ExtractedEntity] = Field(default_factory=list)
    relationships: list[ExtractedRelationship] = Field(default_factory=list)
    source_text: str = Field(description="Original text that was processed")
    extraction_mode: str = Field(description="Mode used for extraction")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())


# Extraction prompts
ENTITY_EXTRACTION_PROMPT = """You are an expert at extracting structured knowledge from technical text about computer systems.

Given the following discovery text, extract all entities (hardware, software, containers, services, networks, locations, concepts).

For each entity, identify:
1. name: The specific name of the entity
2. entity_type: One of [hardware, software, container, service, network, location, concept]
3. circle: Which exploration circle it belongs to:
   - substrate: Machine, OS, hardware, runtime
   - tools: Claude Code, MCP, plugins, development tools
   - network: Connectivity, containers, APIs, external services
   - history: Git, evolution, project history
   - cosmos: Natural laws, physics, universal concepts
4. properties: Key-value pairs of additional information
5. confidence: How confident you are (0.0-1.0)

Output valid JSON only. Example format:
{"entities": [{"name": "RTX 4070", "entity_type": "hardware", "circle": "substrate", "properties": {"vram_gb": 12}, "confidence": 0.95}]}

Discovery text:
"""

RELATIONSHIP_EXTRACTION_PROMPT_TEMPLATE = """You are an expert at identifying relationships between technical entities.

Given these entities and the original text, identify relationships between them.

Relationship types:
- RUNS_ON: X runs on Y (e.g., container runs on host)
- PART_OF: X is part of Y (e.g., CPU is part of computer)
- USES: X uses Y (e.g., application uses database)
- DEPENDS_ON: X depends on Y (e.g., service depends on library)
- CONNECTS_TO: X connects to Y (e.g., client connects to server)
- CONTAINS: X contains Y (e.g., network contains hosts)
- PRODUCES: X produces Y (e.g., process produces output)

Output valid JSON only. Example format:
{"relationships": [{"source": "Neo4j", "target": "Docker", "relationship": "RUNS_ON", "properties": {}, "confidence": 0.9}]}

Entities found:
ENTITIES_PLACEHOLDER

Original text:
TEXT_PLACEHOLDER
"""


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


def extract_direct(text: str) -> ExtractionResult:
    """
    Direct rule-based extraction (no LLM).
    Fast and free but limited to pattern matching.
    """
    entities = []
    relationships = []

    # Hardware patterns
    hardware_patterns = [
        (r'\b(Intel\s+(?:Core\s+)?i[3579]-\d+\w*)', 'hardware', 'substrate'),
        (r'\b(AMD\s+Ryzen\s+\d+\s+\d+\w*)', 'hardware', 'substrate'),
        (r'\b(NVIDIA\s+(?:GeForce\s+)?(?:RTX|GTX)\s+\d+(?:\s*Ti)?)', 'hardware', 'substrate'),
        (r'\b(\d+\s*GB\s+RAM)', 'hardware', 'substrate'),
        (r'\b(NVMe\s+SSD)', 'hardware', 'substrate'),
    ]

    # Software patterns
    software_patterns = [
        (r'\b(Pop!_OS\s+[\d.]+)', 'software', 'substrate'),
        (r'\b(Ubuntu\s+[\d.]+)', 'software', 'substrate'),
        (r'\b(Linux\s+[\d.]+[-\w]*)', 'software', 'substrate'),
        (r'\b(Python\s+[\d.]+)', 'software', 'substrate'),
        (r'\b(Claude\s+Code\s+[\d.]+)', 'software', 'tools'),
        (r'\b(Node\.?js\s+[\d.]+)', 'software', 'tools'),
    ]

    # Container patterns
    container_patterns = [
        (r'\b(neo4j(?::\S+)?)', 'container', 'network'),
        (r'\b(postgres(?:ql)?(?::\S+)?)', 'container', 'network'),
        (r'\b(redis(?::\S+)?)', 'container', 'network'),
        (r'\b(falkordb(?::\S+)?)', 'container', 'network'),
        (r'\b(timescale(?:db)?(?::\S+)?)', 'container', 'network'),
    ]

    # Network patterns
    network_patterns = [
        (r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', 'network', 'network'),
        (r'\bport\s+(\d{4,5})', 'service', 'network'),
    ]

    all_patterns = hardware_patterns + software_patterns + container_patterns + network_patterns

    for pattern, etype, circle in all_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            entities.append(ExtractedEntity(
                name=match.group(1),
                entity_type=etype,
                circle=circle,
                confidence=0.6  # Lower confidence for rule-based
            ))

    # Infer relationships from context
    if len(entities) > 1:
        containers = [e for e in entities if e.entity_type == 'container']
        hardware = [e for e in entities if e.entity_type == 'hardware']

        # Containers run on hardware
        for c in containers:
            for h in hardware:
                if 'host' in h.name.lower() or 'cpu' in h.name.lower():
                    relationships.append(ExtractedRelationship(
                        source=c.name,
                        target=h.name,
                        relationship="RUNS_ON",
                        confidence=0.5
                    ))

    return ExtractionResult(
        entities=entities,
        relationships=relationships,
        source_text=text,
        extraction_mode="direct"
    )


def extract_ollama(text: str) -> ExtractionResult:
    """
    LLM-based extraction using local Ollama.
    Free, good quality, recommended for most use.
    """
    try:
        import ollama
    except ImportError:
        import subprocess
        subprocess.run(["uv", "pip", "install", "ollama"], check=True)
        import ollama

    # Step 1: Extract entities
    entity_response = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{
            'role': 'user',
            'content': ENTITY_EXTRACTION_PROMPT + text
        }],
        format='json'
    )

    try:
        entity_data = json.loads(entity_response['message']['content'])
        entities = [ExtractedEntity(**e) for e in entity_data.get('entities', [])]
    except (json.JSONDecodeError, KeyError):
        entities = []

    # Step 2: Extract relationships
    if entities:
        entity_names = [e.name for e in entities]
        rel_prompt = RELATIONSHIP_EXTRACTION_PROMPT_TEMPLATE.replace(
            "ENTITIES_PLACEHOLDER", json.dumps(entity_names)
        ).replace(
            "TEXT_PLACEHOLDER", text
        )
        rel_response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{
                'role': 'user',
                'content': rel_prompt
            }],
            format='json'
        )

        try:
            rel_data = json.loads(rel_response['message']['content'])
            relationships = [ExtractedRelationship(**r) for r in rel_data.get('relationships', [])]
        except (json.JSONDecodeError, KeyError):
            relationships = []
    else:
        relationships = []

    return ExtractionResult(
        entities=entities,
        relationships=relationships,
        source_text=text,
        extraction_mode="ollama"
    )


def escape_cypher(value) -> str:
    """Escape a value for use in Cypher query."""
    if isinstance(value, str):
        return value.replace("'", "\\'").replace('"', '\\"')
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, bool):
        return "true" if value else "false"
    else:
        return str(value)


def add_to_graph(graph, result: ExtractionResult) -> dict:
    """Add extracted entities and relationships to FalkorDB with bi-temporal properties."""
    now = datetime.now().isoformat()
    stats = {"entities_added": 0, "relationships_added": 0, "errors": []}

    # Add entities
    for entity in result.entities:
        try:
            # Generate ID from name
            entity_id = f"extracted-{entity.name.lower().replace(' ', '-').replace('/', '-')}"
            safe_name = escape_cypher(entity.name)

            query = f"""
            MERGE (e:Entity:Extracted {{name: '{safe_name}'}})
            ON CREATE SET e.id = '{entity_id}',
                         e.entity_type = '{entity.entity_type}',
                         e.extracted_at = '{now}',
                         e.confidence = {entity.confidence},
                         e.source_mode = '{result.extraction_mode}'
            WITH e
            MATCH (c:Circle {{name: '{entity.circle}'}})
            MERGE (e)-[r:IN_CIRCLE]->(c)
            ON CREATE SET r.valid_at = '{now}', r.created_at = '{now}', r.confidence = {entity.confidence}
            RETURN e.id
            """

            graph.query(query)
            stats["entities_added"] += 1

        except Exception as e:
            stats["errors"].append(f"Entity {entity.name}: {str(e)}")

    # Add relationships
    for rel in result.relationships:
        try:
            safe_source = escape_cypher(rel.source)
            safe_target = escape_cypher(rel.target)

            query = f"""
            MATCH (source:Entity {{name: '{safe_source}'}})
            MATCH (target:Entity {{name: '{safe_target}'}})
            MERGE (source)-[r:{rel.relationship}]->(target)
            ON CREATE SET r.valid_at = '{now}', r.created_at = '{now}', r.confidence = {rel.confidence}
            RETURN type(r)
            """

            graph.query(query)
            stats["relationships_added"] += 1

        except Exception as e:
            stats["errors"].append(f"Relationship {rel.source}->{rel.target}: {str(e)}")

    # Create discovery record
    discovery_id = f"discovery-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    summary = escape_cypher(result.source_text[:200] + "..." if len(result.source_text) > 200 else result.source_text)
    try:
        query = f"""
        CREATE (d:Discovery {{
            id: '{discovery_id}',
            date: '{datetime.now().strftime('%Y-%m-%d')}',
            summary: '{summary}',
            extraction_mode: '{result.extraction_mode}',
            entities_found: {len(result.entities)},
            relationships_found: {len(result.relationships)}
        }})
        RETURN d.id
        """

        graph.query(query)
    except Exception as e:
        stats["errors"].append(f"Discovery creation: {str(e)}")

    return stats


def extract(text: str, mode: str = "ollama") -> ExtractionResult:
    """
    Main extraction function.

    Args:
        text: Discovery text to extract from
        mode: Extraction mode - "direct", "ollama", or "cloud"

    Returns:
        ExtractionResult with entities and relationships
    """
    if mode == "direct":
        return extract_direct(text)
    elif mode == "ollama":
        return extract_ollama(text)
    elif mode == "cloud":
        raise NotImplementedError("Cloud extraction not yet implemented")
    else:
        raise ValueError(f"Unknown mode: {mode}")


def main():
    parser = argparse.ArgumentParser(description="Extract entities from discovery text")
    parser.add_argument("--text", help="Text to extract from")
    parser.add_argument("--file", help="File containing text to extract")
    parser.add_argument("--mode", choices=["direct", "ollama", "cloud"], default="ollama",
                       help="Extraction mode (default: ollama)")
    parser.add_argument("--add-to-graph", action="store_true", help="Add results to FalkorDB")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    args = parser.parse_args()

    if args.interactive:
        print("Entity Extraction Pipeline")
        print("=" * 40)
        print(f"Mode: {args.mode}")
        print("Enter discovery text (Ctrl+D to finish):\n")

        import sys
        text = sys.stdin.read()
    elif args.file:
        with open(args.file) as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        parser.print_help()
        return

    print(f"\nExtracting entities using {args.mode} mode...")
    result = extract(text, mode=args.mode)

    print(f"\n=== Extraction Results ===")
    print(f"Entities found: {len(result.entities)}")
    for e in result.entities:
        print(f"  - [{e.entity_type}] {e.name} ({e.circle}) confidence={e.confidence}")

    print(f"\nRelationships found: {len(result.relationships)}")
    for r in result.relationships:
        print(f"  - {r.source} -[{r.relationship}]-> {r.target} confidence={r.confidence}")

    if args.add_to_graph:
        print("\nAdding to FalkorDB...")
        graph = get_falkordb()
        stats = add_to_graph(graph, result)
        print(f"  Added {stats['entities_added']} entities")
        print(f"  Added {stats['relationships_added']} relationships")
        if stats['errors']:
            print(f"  Errors: {len(stats['errors'])}")
            for err in stats['errors']:
                print(f"    - {err}")


if __name__ == "__main__":
    main()
