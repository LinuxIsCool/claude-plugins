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
Visualize commit-to-agent traceability.
Shows only commits with agent correlations.
"""

import matplotlib.pyplot as plt
import networkx as nx
from falkordb import FalkorDB

def main():
    db = FalkorDB(host='localhost', port=6380)
    g = db.select_graph('claude_logs')

    G = nx.DiGraph()

    # Get commit → agent correlations
    result = g.query("""
        MATCH (c:Commit)-[r:LIKELY_BY]->(a:AgentExecution)<-[:SPAWNED]-(s:Session)
        RETURN c.hash, c.message, a.agent_id, s.id, r.seconds_before
        ORDER BY c.timestamp DESC
        LIMIT 40
    """)

    print("=== Commit → Agent Traceability ===\n")

    for row in result.result_set:
        commit_hash, msg, agent_id, session_id, secs = row
        msg_short = msg[:50] if msg else "?"

        # Add nodes
        G.add_node(f"C:{commit_hash}", label=commit_hash[:7], node_type='Commit',
                   full_label=f"{commit_hash[:7]}\n{msg_short}")
        G.add_node(f"A:{agent_id}", label=agent_id[:7], node_type='Agent')
        G.add_node(f"S:{session_id}", label=session_id[:6], node_type='Session')

        # Add edges
        G.add_edge(f"C:{commit_hash}", f"A:{agent_id}", edge_type='LIKELY_BY', weight=secs)
        G.add_edge(f"S:{session_id}", f"A:{agent_id}", edge_type='SPAWNED')

        print(f"Commit {commit_hash[:7]} → Agent {agent_id} ({secs}s) ← Session {session_id[:6]}")
        print(f"  └─ {msg_short}...")

    print(f"\nGraph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    # Visualization
    fig, ax = plt.subplots(figsize=(16, 12))

    # Hierarchical layout: Commits on left, Agents middle, Sessions right
    pos = {}
    commits = [n for n in G.nodes() if n.startswith('C:')]
    agents = [n for n in G.nodes() if n.startswith('A:')]
    sessions = [n for n in G.nodes() if n.startswith('S:')]

    # Position by type
    for i, n in enumerate(commits):
        pos[n] = (0, -i * 0.5)
    for i, n in enumerate(agents):
        pos[n] = (1, -i * 0.4)
    for i, n in enumerate(sessions):
        pos[n] = (2, -i * 0.8)

    # Colors
    colors = []
    for n in G.nodes():
        if n.startswith('C:'):
            colors.append('#FF9800')  # Orange for commits
        elif n.startswith('A:'):
            colors.append('#2196F3')  # Blue for agents
        else:
            colors.append('#4CAF50')  # Green for sessions

    # Draw
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=300, alpha=0.9, ax=ax)

    # Draw edges by type
    likely_edges = [(u, v) for u, v in G.edges() if G.edges[u, v].get('edge_type') == 'LIKELY_BY']
    spawned_edges = [(u, v) for u, v in G.edges() if G.edges[u, v].get('edge_type') == 'SPAWNED']

    nx.draw_networkx_edges(G, pos, edgelist=likely_edges, edge_color='#FF5722',
                          alpha=0.6, arrows=True, arrowsize=15, ax=ax,
                          connectionstyle="arc3,rad=0.1")
    nx.draw_networkx_edges(G, pos, edgelist=spawned_edges, edge_color='#4CAF50',
                          alpha=0.4, arrows=True, arrowsize=10, ax=ax,
                          style='dashed')

    # Labels
    labels = {n: G.nodes[n].get('label', n) for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels, font_size=7, ax=ax)

    # Column labels
    ax.text(0, 1, 'COMMITS', ha='center', fontsize=12, fontweight='bold', color='#FF9800')
    ax.text(1, 1, 'AGENTS', ha='center', fontsize=12, fontweight='bold', color='#2196F3')
    ax.text(2, 1, 'SESSIONS', ha='center', fontsize=12, fontweight='bold', color='#4CAF50')

    # Legend
    ax.text(0, 2, '→ LIKELY_BY (commit made by agent)', fontsize=9, color='#FF5722')
    ax.text(0, 1.7, '⇢ SPAWNED (session spawned agent)', fontsize=9, color='#4CAF50')

    ax.set_title('Agent Traceability: Commits → Agents ← Sessions\n(Recent 40 correlations)', fontsize=14)
    ax.axis('off')

    output_path = '/home/ygg/Workspace/sandbox/marketplaces/claude/.claude/tools/traceability_graph.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"\nSaved to: {output_path}")


if __name__ == '__main__':
    main()
