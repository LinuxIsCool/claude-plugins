#!/usr/bin/env python3
"""
Graphiti Configuration for Exploration Knowledge Graph

Thin wrapper that configures Graphiti with local infrastructure:
- FalkorDB for graph storage (fast, Redis-based)
- Ollama for LLM when semantic extraction needed
- Ollama embeddings for vector similarity

For detailed Graphiti patterns, see: llms:graphiti
For FalkorDB Cypher patterns, see: llms:falkordb

Usage:
    from graphiti_config import get_graphiti, get_falkordb

    # For Graphiti operations (episodes, search)
    graphiti = await get_graphiti()

    # For direct FalkorDB queries (faster, no LLM)
    graph = get_falkordb()
"""

import os
from datetime import datetime, timezone

# Infrastructure configuration
FALKOR_HOST = os.environ.get("FALKORDB_HOST", "localhost")
FALKOR_PORT = int(os.environ.get("FALKORDB_PORT", "6380"))
GRAPH_NAME = os.environ.get("EXPLORATION_GRAPH", "exploration")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:3b")
EMBED_MODEL = os.environ.get("EMBED_MODEL", "nomic-embed-text")


def _install_package(package: str):
    """Install a package using pip."""
    import subprocess
    import sys
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", package], check=True)


def get_falkordb():
    """
    Get direct FalkorDB graph connection.

    Use this for:
    - Direct Cypher queries (fastest)
    - Structured data ingestion (no LLM needed)
    - Schema operations

    Pattern from awareness:temporal-kg-memory - direct parsing is
    100x faster than LLM extraction for structured data.
    """
    try:
        from falkordb import FalkorDB
    except ImportError:
        _install_package("falkordb")
        from falkordb import FalkorDB

    db = FalkorDB(host=FALKOR_HOST, port=FALKOR_PORT)
    return db.select_graph(GRAPH_NAME)


async def get_graphiti():
    """
    Get configured Graphiti instance.

    Use this for:
    - Episode ingestion with entity extraction
    - Hybrid search (semantic + keyword + graph)
    - When you need LLM-powered understanding

    Note: For structured data, prefer get_falkordb() with direct parsing.
    See awareness:temporal-kg-memory for the production pattern.
    """
    try:
        from graphiti_core import Graphiti
        from graphiti_core.llm_client.ollama_client import OllamaClient
        from graphiti_core.embedder.ollama import OllamaEmbedder
        from graphiti_core.llm_client.config import LLMConfig
        from graphiti_core.embedder.config import EmbedderConfig
    except ImportError:
        _install_package("graphiti-core")
        from graphiti_core import Graphiti
        from graphiti_core.llm_client.ollama_client import OllamaClient
        from graphiti_core.embedder.ollama import OllamaEmbedder
        from graphiti_core.llm_client.config import LLMConfig
        from graphiti_core.embedder.config import EmbedderConfig

    # Configure Ollama LLM (free, local)
    llm_config = LLMConfig(model=OLLAMA_MODEL)
    llm_client = OllamaClient(config=llm_config)

    # Configure Ollama embeddings (free, local)
    embed_config = EmbedderConfig(model=EMBED_MODEL)
    embedder = OllamaEmbedder(config=embed_config)

    # Use FalkorDB as graph backend
    graphiti = Graphiti(
        uri=f"redis://{FALKOR_HOST}:{FALKOR_PORT}",
        llm_client=llm_client,
        embedder=embedder
    )

    return graphiti


def escape_cypher(value: str) -> str:
    """Escape a string for safe use in Cypher queries."""
    if not isinstance(value, str):
        return str(value)
    return value.replace("'", "\\'").replace('"', '\\"').replace('\n', ' ')


def now_iso() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


# Exploration domain constants
CIRCLES = ["substrate", "tools", "network", "history", "cosmos"]

ENTITY_TYPES = [
    "hardware", "software", "container", "service",
    "network", "location", "concept", "plugin", "mcp"
]

MASTERY_LEVELS = {
    (0.0, 0.2): "stranger",
    (0.2, 0.4): "tourist",
    (0.4, 0.6): "resident",
    (0.6, 0.8): "native",
    (0.8, 1.0): "cartographer"
}


def get_mastery_level(score: float) -> str:
    """Convert mastery score to level name."""
    for (low, high), name in MASTERY_LEVELS.items():
        if low <= score < high:
            return name
    return "cartographer" if score >= 1.0 else "stranger"
