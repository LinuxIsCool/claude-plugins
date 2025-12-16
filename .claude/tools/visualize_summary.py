#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "falkordb",
#     "matplotlib",
# ]
# ///
"""
Summary visualization of the knowledge graph.
"""

import matplotlib.pyplot as plt
from falkordb import FalkorDB

def main():
    db = FalkorDB(host='localhost', port=6380)
    g = db.select_graph('claude_logs')

    # Collect stats
    stats = {}

    # Node counts
    for label in ['Session', 'AgentExecution', 'Commit', 'UserMessage', 'AssistantMessage']:
        result = g.query(f"MATCH (n:{label}) RETURN count(n)")
        stats[label] = result.result_set[0][0] if result.result_set else 0

    # Edge counts
    for rel in ['SPAWNED', 'LIKELY_BY', 'NEXT_SESSION', 'IN_SESSION', 'THEN']:
        result = g.query(f"MATCH ()-[r:{rel}]->() RETURN count(r)")
        stats[rel] = result.result_set[0][0] if result.result_set else 0

    # Correlation success rate
    result = g.query("MATCH (c:Commit) RETURN count(c)")
    total_commits = result.result_set[0][0] if result.result_set else 0
    result = g.query("MATCH (c:Commit)-[:LIKELY_BY]->() RETURN count(DISTINCT c)")
    correlated_commits = result.result_set[0][0] if result.result_set else 0

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Node type distribution (pie)
    ax1 = axes[0, 0]
    node_labels = ['Sessions', 'Agents', 'Commits', 'User Msgs', 'Asst Msgs']
    node_values = [stats['Session'], stats['AgentExecution'], stats['Commit'],
                   stats['UserMessage'], stats['AssistantMessage']]
    colors = ['#4CAF50', '#2196F3', '#FF9800', '#9C27B0', '#E91E63']
    ax1.pie(node_values, labels=node_labels, autopct='%1.0f%%', colors=colors, startangle=90)
    ax1.set_title(f'Node Distribution (Total: {sum(node_values)})', fontsize=12)

    # 2. Edge type distribution (bar)
    ax2 = axes[0, 1]
    edge_labels = ['SPAWNED', 'LIKELY_BY', 'NEXT_SESSION', 'IN_SESSION', 'THEN']
    edge_values = [stats[l] for l in edge_labels]
    bars = ax2.barh(edge_labels, edge_values, color=['#4CAF50', '#FF5722', '#607D8B', '#9C27B0', '#795548'])
    ax2.set_xlabel('Count')
    ax2.set_title(f'Relationship Distribution (Total: {sum(edge_values)})', fontsize=12)
    for bar, val in zip(bars, edge_values):
        ax2.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, str(val), va='center')

    # 3. Commit correlation rate
    ax3 = axes[1, 0]
    correlation_rate = correlated_commits / total_commits * 100 if total_commits > 0 else 0
    labels = ['Correlated', 'Not Correlated']
    sizes = [correlated_commits, total_commits - correlated_commits]
    colors = ['#4CAF50', '#BDBDBD']
    ax3.pie(sizes, labels=labels, autopct='%1.0f%%', colors=colors, startangle=90)
    ax3.set_title(f'Commit→Agent Correlation\n({correlated_commits}/{total_commits} = {correlation_rate:.0f}%)', fontsize=12)

    # 4. Key metrics summary
    ax4 = axes[1, 1]
    ax4.axis('off')

    summary_text = f"""
    ╔═══════════════════════════════════════╗
    ║   CLAUDE CODE KNOWLEDGE GRAPH         ║
    ╠═══════════════════════════════════════╣
    ║                                       ║
    ║   Sessions:           {stats['Session']:>5}          ║
    ║   Agent Executions:   {stats['AgentExecution']:>5}          ║
    ║   Git Commits:        {stats['Commit']:>5}          ║
    ║                                       ║
    ║   User Messages:      {stats['UserMessage']:>5}          ║
    ║   Assistant Messages: {stats['AssistantMessage']:>5}          ║
    ║                                       ║
    ╠═══════════════════════════════════════╣
    ║   TRACEABILITY                        ║
    ║   Commit→Agent links: {stats['LIKELY_BY']:>5}          ║
    ║   Correlation rate:   {correlation_rate:>5.0f}%         ║
    ║                                       ║
    ║   Session→Agent:      {stats['SPAWNED']:>5}          ║
    ║   Session chain:      {stats['NEXT_SESSION']:>5}          ║
    ╚═══════════════════════════════════════╝
    """

    ax4.text(0.1, 0.5, summary_text, family='monospace', fontsize=11,
             verticalalignment='center', bbox=dict(boxstyle='round', facecolor='#f5f5f5'))

    plt.suptitle('Agent ID Traceability - Knowledge Graph Summary', fontsize=14, fontweight='bold')
    plt.tight_layout()

    output_path = '/home/ygg/Workspace/sandbox/marketplaces/claude/.claude/tools/graph_summary.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved to: {output_path}")


if __name__ == '__main__':
    main()
