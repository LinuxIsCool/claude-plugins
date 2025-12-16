#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "falkordb",
#     "matplotlib",
#     "networkx",
# ]
# ///
"""
Visualize the Claude Code temporal knowledge graph.
"""

import matplotlib.pyplot as plt
import networkx as nx
from falkordb import FalkorDB

def main():
    # Connect
    db = FalkorDB(host='localhost', port=6380)
    g = db.select_graph('claude_logs')

    # Create NetworkX graph
    G = nx.DiGraph()

    # Get all nodes with labels
    print("Loading nodes...")

    # Sessions
    result = g.query("MATCH (s:Session) RETURN s.id, 'Session'")
    for row in result.result_set:
        G.add_node(f"S:{row[0]}", label=row[0][:6], node_type='Session')

    # Agent Executions
    result = g.query("MATCH (a:AgentExecution) RETURN a.agent_id, 'Agent'")
    for row in result.result_set:
        G.add_node(f"A:{row[0]}", label=row[0][:6], node_type='Agent')

    # Commits
    result = g.query("MATCH (c:Commit) RETURN c.hash, 'Commit'")
    for row in result.result_set:
        G.add_node(f"C:{row[0]}", label=row[0][:6], node_type='Commit')

    # Get relationships
    print("Loading relationships...")

    # SPAWNED: Session -> Agent
    result = g.query("MATCH (s:Session)-[:SPAWNED]->(a:AgentExecution) RETURN s.id, a.agent_id")
    for row in result.result_set:
        G.add_edge(f"S:{row[0]}", f"A:{row[1]}", edge_type='SPAWNED')

    # LIKELY_BY: Commit -> Agent
    result = g.query("MATCH (c:Commit)-[:LIKELY_BY]->(a:AgentExecution) RETURN c.hash, a.agent_id")
    for row in result.result_set:
        G.add_edge(f"C:{row[0]}", f"A:{row[1]}", edge_type='LIKELY_BY')

    # NEXT_SESSION: Session -> Session
    result = g.query("MATCH (s1:Session)-[:NEXT_SESSION]->(s2:Session) RETURN s1.id, s2.id")
    for row in result.result_set:
        G.add_edge(f"S:{row[0]}", f"S:{row[1]}", edge_type='NEXT_SESSION')

    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    # Create visualization
    plt.figure(figsize=(20, 16))

    # Color by type
    color_map = {
        'Session': '#4CAF50',   # Green
        'Agent': '#2196F3',     # Blue
        'Commit': '#FF9800',    # Orange
    }

    node_colors = [color_map.get(G.nodes[n].get('node_type', 'Session'), '#999') for n in G.nodes()]

    # Layout
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

    # Draw
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=100, alpha=0.8)
    nx.draw_networkx_edges(G, pos, alpha=0.3, arrows=True, arrowsize=10)

    # Labels for key nodes only
    labels = {n: G.nodes[n].get('label', '') for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=6)

    # Legend
    legend_elements = [
        plt.scatter([], [], c='#4CAF50', s=100, label='Session'),
        plt.scatter([], [], c='#2196F3', s=100, label='Agent'),
        plt.scatter([], [], c='#FF9800', s=100, label='Commit'),
    ]
    plt.legend(handles=legend_elements, loc='upper left')

    plt.title('Claude Code Temporal Knowledge Graph\nSessions → Agents ← Commits', fontsize=14)
    plt.axis('off')
    plt.tight_layout()

    # Save
    output_path = '/home/ygg/Workspace/sandbox/marketplaces/claude/.claude/tools/graph_visualization.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved to: {output_path}")

    # Also print summary
    print("\n=== Graph Summary ===")
    print(f"Sessions: {len([n for n in G.nodes() if n.startswith('S:')])}")
    print(f"Agents: {len([n for n in G.nodes() if n.startswith('A:')])}")
    print(f"Commits: {len([n for n in G.nodes() if n.startswith('C:')])}")
    print(f"\nEdges:")
    print(f"  SPAWNED (Session→Agent): {len([e for e in G.edges() if G.edges[e].get('edge_type') == 'SPAWNED'])}")
    print(f"  LIKELY_BY (Commit→Agent): {len([e for e in G.edges() if G.edges[e].get('edge_type') == 'LIKELY_BY'])}")
    print(f"  NEXT_SESSION: {len([e for e in G.edges() if G.edges[e].get('edge_type') == 'NEXT_SESSION'])}")


if __name__ == '__main__':
    main()
