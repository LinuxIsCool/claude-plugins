# Knowledge Graph Implementation Guide

**Quick-start guide for implementing the transcripts knowledge graph**

---

## Prerequisites

1. **FalkorDB running**:
   ```bash
   docker run -p 6379:6379 falkordb/falkordb:latest
   ```

2. **Graphiti installed**:
   ```bash
   pip install graphiti-core
   ```

3. **OpenAI API key** (or alternative LLM):
   ```bash
   export OPENAI_API_KEY="sk-..."
   ```

---

## Quick Start (15 minutes)

### Step 1: Initialize Graphiti Client

```typescript
// src/kg/client.ts
import { spawn } from 'child_process';
import { promisify } from 'util';

export class GraphitiClient {
  private pythonProcess: any;

  async init() {
    // Initialize Python Graphiti client via subprocess
    this.pythonProcess = spawn('python', ['-m', 'graphiti_mcp_server']);
    await this.buildIndices();
  }

  async buildIndices() {
    // Run Python script to build indices
    const script = `
from graphiti_core import Graphiti
from graphiti_core.driver.falkordb_driver import FalkorDriver

driver = FalkorDriver(host="localhost", port=6379, database="transcripts")
graphiti = Graphiti(graph_driver=driver)
await graphiti.build_indices_and_constraints()
`;
    await this.executePython(script);
  }

  async ingestUtterance(utterance: any, transcript: any) {
    const script = `
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from datetime import datetime, timezone, timedelta

graphiti = Graphiti(...)  # Initialize with driver

await graphiti.add_episode(
    name="${transcript.id}_${utterance.id}",
    episode_body="[${utterance.speaker.name}]: ${utterance.text}",
    source=EpisodeType.message,
    source_description="${transcript.title}",
    reference_time=datetime.fromisoformat("${transcript.source_created_at}") + timedelta(milliseconds=${utterance.start_ms}),
    group_id="${transcript.id}",
    metadata={
        "transcript_id": "${transcript.id}",
        "utterance_id": "${utterance.id}",
        "speaker_id": "${utterance.speaker.id}",
        "start_ms": ${utterance.start_ms},
        "end_ms": ${utterance.end_ms}
    }
)
`;
    await this.executePython(script);
  }

  private async executePython(script: string) {
    // Execute Python script and return result
    // Implementation depends on IPC mechanism
  }
}
```

### Step 2: Define Custom Entity Schemas

```python
# src/kg/schemas.py
from pydantic import BaseModel, Field

class Concept(BaseModel):
    """Abstract idea, technique, or topic"""
    name: str = Field(description="Canonical concept name")
    category: str | None = Field(None, description="technique|belief|technology|method|process")
    description: str | None = Field(None, description="Brief explanation of the concept")
    domain: list[str] | None = Field(None, description="Domains this applies to (AI, agents, KG, etc)")

class Technique(BaseModel):
    """Actionable method or approach"""
    name: str = Field(description="Technique name")
    description: str = Field(description="What this technique does and how it works")
    complexity: str | None = Field(None, description="beginner|intermediate|advanced|expert")
    category: str | None = Field(None, description="prompting|architecture|debugging|optimization")

class Belief(BaseModel):
    """Expressed position or opinion"""
    statement: str = Field(description="The belief statement, normalized")
    polarity: str | None = Field(None, description="positive|negative|neutral|nuanced")
    strength: str | None = Field(None, description="strong|moderate|weak|exploring")

class Example(BaseModel):
    """Concrete instance or demonstration"""
    description: str = Field(description="What this example demonstrates")
    text: str | None = Field(None, description="Actual example content or quote")
    context: str | None = Field(None, description="Surrounding context for understanding")

class SpeakerEntity(BaseModel):
    """Reference to a speaker"""
    name: str = Field(description="Speaker name as mentioned")
    role: str | None = Field(None, description="Role or title if mentioned")
    organization: str | None = Field(None, description="Organization if mentioned")
```

### Step 3: Implement Ingestion Pipeline

```python
# src/kg/ingestion.py
from graphiti_core import Graphiti
from graphiti_core.nodes import EpisodeType
from datetime import datetime, timezone, timedelta
from .schemas import Concept, Technique, Belief, Example, SpeakerEntity

async def ingest_transcript(transcript: dict, graphiti: Graphiti):
    """Ingest a complete transcript into the knowledge graph"""

    # Define entity and edge types
    entity_types = {
        "Concept": Concept,
        "Technique": Technique,
        "Belief": Belief,
        "Example": Example,
        "Speaker": SpeakerEntity
    }

    edge_types = {
        "DEMONSTRATES": {
            "how": str,
            "completeness": str
        },
        "BUILDS_ON": {
            "description": str
        },
        "CONTRADICTS": {
            "severity": str,
            "description": str
        },
        "EXEMPLIFIES": {
            "relevance": float
        }
    }

    # Process each utterance as an episode
    for utterance in transcript['utterances']:
        # Calculate absolute timestamp
        utterance_time = datetime.fromisoformat(transcript['source_created_at'])
        utterance_time += timedelta(milliseconds=utterance['start_ms'])

        # Format episode body with speaker context
        episode_body = f"[{utterance['speaker']['name']}]: {utterance['text']}"

        # Add episode
        await graphiti.add_episode(
            name=f"{transcript['id']}_{utterance['id']}",
            episode_body=episode_body,
            source=EpisodeType.message,
            source_description=f"YouTube: {transcript['title']}",
            reference_time=utterance_time,
            group_id=transcript['id'],
            entity_types=entity_types,
            edge_types=edge_types,
            metadata={
                "transcript_id": transcript['id'],
                "utterance_id": utterance['id'],
                "speaker_id": utterance['speaker']['id'],
                "start_ms": utterance['start_ms'],
                "end_ms": utterance['end_ms'],
                "platform": "youtube",
                "source_url": transcript['source']['url']
            }
        )

        print(f"Ingested utterance {utterance['id']} from {transcript['id']}")

    print(f"Completed ingestion of transcript {transcript['id']}")
```

### Step 4: Implement Query Interface

```python
# src/kg/queries.py
from graphiti_core import Graphiti
from graphiti_core.search.search_config_recipes import (
    EDGE_HYBRID_SEARCH_RRF,
    NODE_HYBRID_SEARCH_RRF
)

class KnowledgeGraphQueries:
    def __init__(self, graphiti: Graphiti):
        self.graphiti = graphiti

    async def search_concepts(self, query: str, limit: int = 10):
        """Search for concepts matching query"""
        config = NODE_HYBRID_SEARCH_RRF.model_copy(deep=True)
        config.limit = limit

        results = await self.graphiti._search(query, config=config)

        return [{
            "name": node.name,
            "summary": node.summary,
            "uuid": node.uuid
        } for node in results.nodes]

    async def get_speaker_concepts(self, speaker_name: str, limit: int = 20):
        """Get concepts discussed by a speaker"""
        query = f"""
        MATCH (s:EntityNode {{name: "{speaker_name}"}})-[d:DISCUSSES]->(c:EntityNode)
        WHERE c.labels CONTAINS "Concept"
        RETURN c.name, c.summary, d.mention_count, d.first_mentioned, d.last_mentioned
        ORDER BY d.mention_count DESC
        LIMIT {limit}
        """

        results = await self.graphiti.driver.execute_query(query)
        return results

    async def track_concept_evolution(self, concept_name: str):
        """Track how a concept has been discussed over time"""
        query = f"""
        MATCH (c:EntityNode {{name: "{concept_name}"}})<-[m:MENTIONS]-(e:EpisodeNode)
        WITH c, e, m
        ORDER BY e.valid_at ASC
        RETURN e.name, e.content, e.valid_at, m.salience
        """

        results = await self.graphiti.driver.execute_query(query)
        return results

    async def find_related_concepts(self, concept_name: str, limit: int = 10):
        """Find concepts related to the given concept"""
        query = f"""
        MATCH (c1:EntityNode {{name: "{concept_name}"}})-[r:RELATED_TO]-(c2:EntityNode)
        RETURN c2.name, r.relationship_type, r.strength, r.co_mention_count
        ORDER BY r.strength DESC
        LIMIT {limit}
        """

        results = await self.graphiti.driver.execute_query(query)
        return results

    async def get_beliefs(self, speaker_name: str, topic: str = None):
        """Get beliefs held by a speaker, optionally filtered by topic"""
        topic_filter = f"AND b.statement CONTAINS '{topic}'" if topic else ""

        query = f"""
        MATCH (s:EntityNode {{name: "{speaker_name}"}})-[rel:BELIEVES]->(b:EntityNode)
        WHERE b.labels CONTAINS "Belief"
          AND rel.invalid_at IS NULL  {topic_filter}
        RETURN b.statement, rel.strength, rel.first_stated, rel.last_stated
        ORDER BY rel.strength DESC
        """

        results = await self.graphiti.driver.execute_query(query)
        return results

    async def find_examples(self, technique_name: str, limit: int = 5):
        """Find examples demonstrating a technique"""
        query = f"""
        MATCH (t:EntityNode {{name: "{technique_name}"}})<-[d:DEMONSTRATES]-(e:EpisodeNode)
        RETURN e.name, e.content, d.how, d.completeness, e.valid_at
        ORDER BY e.valid_at DESC
        LIMIT {limit}
        """

        results = await self.graphiti.driver.execute_query(query)
        return results
```

---

## Minimal Working Example (MWE)

Test the full pipeline with a single transcript:

```python
# test_kg.py
import asyncio
from graphiti_core import Graphiti
from graphiti_core.driver.falkordb_driver import FalkorDriver
from src.kg.ingestion import ingest_transcript
from src.kg.queries import KnowledgeGraphQueries

async def main():
    # Initialize Graphiti
    driver = FalkorDriver(
        host="localhost",
        port=6379,
        database="transcripts_test"
    )
    graphiti = Graphiti(graph_driver=driver)

    # Build indices
    await graphiti.build_indices_and_constraints()

    # Sample transcript (minimal)
    transcript = {
        "id": "tx_test_001",
        "title": "Dan Shipper on AI Agents",
        "source_created_at": "2024-06-15T10:00:00Z",
        "source": {"url": "https://youtube.com/watch?v=test"},
        "utterances": [
            {
                "id": "ut_001",
                "text": "I think AI agents are the future of software. They can use tools and make decisions autonomously.",
                "start_ms": 1000,
                "end_ms": 5000,
                "speaker": {"id": "spk_dan", "name": "Dan Shipper"}
            },
            {
                "id": "ut_002",
                "text": "The key technique is chain-of-thought prompting. It helps agents reason step by step.",
                "start_ms": 6000,
                "end_ms": 10000,
                "speaker": {"id": "spk_dan", "name": "Dan Shipper"}
            },
            {
                "id": "ut_003",
                "text": "For example, in my workflow, I use an agent that searches the web and summarizes results.",
                "start_ms": 11000,
                "end_ms": 15000,
                "speaker": {"id": "spk_dan", "name": "Dan Shipper"}
            }
        ]
    }

    # Ingest transcript
    await ingest_transcript(transcript, graphiti)

    # Query the graph
    kg = KnowledgeGraphQueries(graphiti)

    # Search for concepts
    concepts = await kg.search_concepts("AI agents")
    print("\n=== Concepts Found ===")
    for concept in concepts:
        print(f"- {concept['name']}: {concept['summary']}")

    # Get speaker's concepts
    speaker_concepts = await kg.get_speaker_concepts("Dan Shipper")
    print("\n=== Dan Shipper Discusses ===")
    for record in speaker_concepts:
        print(f"- {record['c.name']} ({record['d.mention_count']} mentions)")

    # Find examples
    examples = await kg.find_examples("chain-of-thought prompting")
    print("\n=== Examples of chain-of-thought ===")
    for record in examples:
        print(f"- {record['e.content'][:100]}...")

if __name__ == "__main__":
    asyncio.run(main())
```

Run:
```bash
python test_kg.py
```

Expected output:
```
Ingested utterance ut_001 from tx_test_001
Ingested utterance ut_002 from tx_test_001
Ingested utterance ut_003 from tx_test_001
Completed ingestion of transcript tx_test_001

=== Concepts Found ===
- AI agents: Software systems that can make autonomous decisions and use tools
- chain-of-thought prompting: Technique for step-by-step reasoning

=== Dan Shipper Discusses ===
- AI agents (3 mentions)
- chain-of-thought prompting (1 mentions)
- tool use (1 mentions)

=== Examples of chain-of-thought ===
- [Dan Shipper]: For example, in my workflow, I use an agent that searches the web and summarizes...
```

---

## Integration with Existing Transcripts

### Option 1: Batch Migration Script

```python
# scripts/migrate_transcripts_to_kg.py
import asyncio
import json
from pathlib import Path
from src.kg.ingestion import ingest_transcript
from graphiti_core import Graphiti

async def migrate_all(transcript_dir: Path, batch_size: int = 10):
    """Migrate all existing transcripts to knowledge graph"""

    graphiti = await initialize_graphiti()

    # Find all transcript JSON files
    transcript_files = list(transcript_dir.glob("**/*.json"))
    print(f"Found {len(transcript_files)} transcripts")

    # Process in batches
    for i in range(0, len(transcript_files), batch_size):
        batch = transcript_files[i:i+batch_size]

        tasks = []
        for file_path in batch:
            transcript = json.loads(file_path.read_text())
            tasks.append(ingest_transcript(transcript, graphiti))

        # Run batch in parallel
        await asyncio.gather(*tasks, return_exceptions=True)

        print(f"Processed {i+len(batch)}/{len(transcript_files)}")

        # Rate limiting
        await asyncio.sleep(5)

    print("Migration complete!")

if __name__ == "__main__":
    transcript_dir = Path("./data/transcripts")
    asyncio.run(migrate_all(transcript_dir, batch_size=10))
```

### Option 2: Incremental Ingestion (Hook into Existing Pipeline)

```typescript
// src/services/transcript-workflow.ts
import { GraphitiClient } from '../kg/client';

export class TranscriptWorkflow {
  private kgClient: GraphitiClient;

  async processTranscript(transcript: Transcript) {
    // Existing processing...
    await this.transcribe(transcript);
    await this.diarize(transcript);
    await this.extractEntities(transcript);

    // NEW: Ingest into knowledge graph
    await this.ingestIntoKG(transcript);

    return transcript;
  }

  private async ingestIntoKG(transcript: Transcript) {
    if (!this.kgClient) {
      this.kgClient = new GraphitiClient();
      await this.kgClient.init();
    }

    for (const utterance of transcript.utterances) {
      await this.kgClient.ingestUtterance(utterance, transcript);
    }
  }
}
```

---

## Slash Commands

Add to `commands/`:

```typescript
// commands/kg-search.ts
import { GraphitiClient } from '../src/kg/client';

export async function kgSearch(args: {
  query: string;
  type?: 'speaker' | 'concept' | 'technique' | 'belief';
  limit?: number;
}) {
  const kg = new GraphitiClient();
  await kg.init();

  const results = await kg.search({
    query: args.query,
    entity_types: args.type ? [args.type] : undefined,
    limit: args.limit || 10
  });

  return formatResults(results);
}

function formatResults(results: any[]) {
  return results.map(r => ({
    name: r.name,
    summary: r.summary,
    relevance: r.score
  }));
}
```

Usage:
```
/kg-search query:"AI agents" type:concept limit:5
```

---

## Next Steps

1. **Run MWE**: Verify Graphiti setup with test transcript
2. **Batch ingest**: Migrate 10-100 sample transcripts
3. **Validate queries**: Test all query patterns from architecture doc
4. **Scale test**: Process 1000 transcripts, measure performance
5. **Optimize**: Tune `SEMAPHORE_LIMIT`, batch sizes, index strategy
6. **Visualize**: Export to Obsidian or build custom D3 view

---

## Troubleshooting

### Issue: "Connection refused to FalkorDB"
**Solution**: Ensure FalkorDB is running on port 6379:
```bash
docker ps | grep falkordb
docker run -d -p 6379:6379 falkordb/falkordb:latest
```

### Issue: "Rate limit exceeded (429)"
**Solution**: Reduce concurrency:
```bash
export SEMAPHORE_LIMIT=2
```

### Issue: "Entity deduplication too aggressive"
**Solution**: Increase similarity threshold in Graphiti config (requires custom node operations)

### Issue: "Query timeout"
**Solution**: Ensure indices are built:
```python
await graphiti.build_indices_and_constraints()
```

---

**File Purpose**: Practical implementation guide
**Created**: 2025-12-24
**Author**: obsidian-quartz agent
