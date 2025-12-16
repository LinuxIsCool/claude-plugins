#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "falkordb",
# ]
# ///
"""
Generate an interactive HTML graph viewer for Claude Code knowledge graph.
Uses vis.js for visualization with hover tooltips and click-to-inspect.
"""

import json
from falkordb import FalkorDB
from pathlib import Path

def main():
    print("Connecting to FalkorDB...")
    db = FalkorDB(host='localhost', port=6380)
    g = db.select_graph('claude_logs')

    nodes = []
    edges = []
    node_details = {}

    print("Loading Sessions...")
    result = g.query("""
        MATCH (s:Session)
        OPTIONAL MATCH (s)<-[:IN_SESSION]-(m)
        WITH s, count(m) as msg_count
        RETURN s.id, s.start_time, s.cwd, s.total_events, msg_count
    """)
    for row in result.result_set:
        sid, start_time, cwd, total_events, msg_count = row
        time_short = start_time[5:16] if start_time else "?"
        cwd_short = cwd.split('/')[-1] if cwd else "?"

        nodes.append({
            'id': f'S:{sid}',
            'label': f'📁 {sid[:6]}\n{time_short}',
            'group': 'session',
            'title': f'Session {sid[:8]}\n{time_short}\n{msg_count} messages'
        })
        node_details[f'S:{sid}'] = {
            'type': 'Session',
            'id': sid,
            'start_time': start_time or 'Unknown',
            'directory': cwd or 'Unknown',
            'total_events': total_events or 0,
            'message_count': msg_count or 0
        }

    print("Loading Agent Executions...")
    result = g.query("""
        MATCH (a:AgentExecution)
        OPTIONAL MATCH (s:Session)-[:SPAWNED]->(a)
        RETURN a.agent_id, a.timestamp, a.session_id, a.transcript_path, s.id
    """)
    for row in result.result_set:
        aid, ts, session_id, transcript, spawner = row
        time_short = ts[11:19] if ts else "?"

        nodes.append({
            'id': f'A:{aid}',
            'label': f'🤖 {aid[:5]}\n{time_short}',
            'group': 'agent',
            'title': f'Agent {aid}\nCompleted: {time_short}\nSession: {session_id[:8] if session_id else "?"}'
        })
        node_details[f'A:{aid}'] = {
            'type': 'AgentExecution',
            'agent_id': aid,
            'timestamp': ts or 'Unknown',
            'session_id': session_id or 'Unknown',
            'transcript_path': transcript or 'Unknown'
        }

    print("Loading Commits...")
    result = g.query("""
        MATCH (c:Commit)
        OPTIONAL MATCH (c)-[r:LIKELY_BY]->(a:AgentExecution)
        RETURN c.hash, c.message, c.timestamp, collect({agent: a.agent_id, secs: r.seconds_before})
    """)
    for row in result.result_set:
        chash, msg, ts, correlations = row
        msg_short = msg[:35] + "..." if msg and len(msg) > 35 else msg or "?"
        time_short = ts[5:16] if ts else "?"

        # Filter out null correlations
        valid_corrs = [c for c in (correlations or []) if c.get('agent')]
        corr_text = f"{len(valid_corrs)} agent(s)" if valid_corrs else "No correlation"

        nodes.append({
            'id': f'C:{chash}',
            'label': f'📝 {chash[:5]}\n{msg_short[:20]}',
            'group': 'commit',
            'title': f'{chash[:8]}\n{msg_short}\n{time_short}\n{corr_text}'
        })
        node_details[f'C:{chash}'] = {
            'type': 'Commit',
            'hash': chash,
            'message': msg or 'Unknown',
            'timestamp': ts or 'Unknown',
            'correlations': [{'agent_id': c['agent'], 'seconds_before': c['secs']}
                           for c in valid_corrs]
        }

    print("Loading relationships...")

    # SPAWNED
    result = g.query("MATCH (s:Session)-[:SPAWNED]->(a:AgentExecution) RETURN s.id, a.agent_id")
    for row in result.result_set:
        edges.append({
            'from': f'S:{row[0]}',
            'to': f'A:{row[1]}',
            'label': 'spawned',
            'arrows': 'to',
            'color': {'color': '#4CAF50', 'opacity': 0.6},
            'dashes': True
        })

    # LIKELY_BY
    result = g.query("MATCH (c:Commit)-[r:LIKELY_BY]->(a:AgentExecution) RETURN c.hash, a.agent_id, r.seconds_before")
    for row in result.result_set:
        edges.append({
            'from': f'C:{row[0]}',
            'to': f'A:{row[1]}',
            'label': f'{row[2]}s',
            'arrows': 'to',
            'color': {'color': '#FF5722', 'opacity': 0.8},
            'width': 2
        })

    # NEXT_SESSION
    result = g.query("MATCH (s1:Session)-[:NEXT_SESSION]->(s2:Session) RETURN s1.id, s2.id")
    for row in result.result_set:
        edges.append({
            'from': f'S:{row[0]}',
            'to': f'S:{row[1]}',
            'label': 'next',
            'arrows': 'to',
            'color': {'color': '#607D8B', 'opacity': 0.4},
            'dashes': [5, 5]
        })

    print(f"Total: {len(nodes)} nodes, {len(edges)} edges")

    # Generate HTML
    html = generate_html(nodes, edges, node_details)

    output_path = Path('/home/ygg/Workspace/sandbox/marketplaces/claude/.claude/tools/graph_viewer.html')
    output_path.write_text(html)
    print(f"\nSaved to: {output_path}")
    print(f"Open in browser: file://{output_path}")


def generate_html(nodes, edges, node_details):
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>Claude Code Knowledge Graph</title>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            height: 100vh;
            background: #1a1a2e;
            color: #eee;
        }}
        #graph {{
            flex: 1;
            height: 100%;
            background: #16213e;
        }}
        #sidebar {{
            width: 380px;
            background: #1a1a2e;
            border-left: 1px solid #333;
            padding: 20px;
            overflow-y: auto;
        }}
        #sidebar h2 {{
            color: #4CAF50;
            margin-bottom: 15px;
            font-size: 18px;
        }}
        #sidebar h3 {{
            color: #2196F3;
            margin: 15px 0 10px 0;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .detail-row {{
            margin: 8px 0;
            padding: 8px;
            background: #0f3460;
            border-radius: 4px;
            font-size: 13px;
        }}
        .detail-label {{
            color: #888;
            font-size: 11px;
            text-transform: uppercase;
            margin-bottom: 3px;
        }}
        .detail-value {{
            color: #fff;
            word-break: break-all;
        }}
        .detail-value.mono {{
            font-family: 'SF Mono', 'Monaco', monospace;
            font-size: 12px;
            color: #4CAF50;
        }}
        #legend {{
            margin-bottom: 20px;
            padding: 15px;
            background: #0f3460;
            border-radius: 8px;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            margin: 5px 0;
            font-size: 13px;
        }}
        .legend-dot {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 10px;
        }}
        .correlation {{
            background: #1e3a5f;
            padding: 8px;
            margin: 5px 0;
            border-radius: 4px;
            border-left: 3px solid #FF5722;
        }}
        #help {{
            margin-top: 20px;
            padding: 15px;
            background: #0f3460;
            border-radius: 8px;
            font-size: 12px;
            color: #888;
        }}
        #help strong {{ color: #4CAF50; }}
        #no-selection {{
            color: #666;
            font-style: italic;
            margin-top: 20px;
        }}
        .transcript-link {{
            color: #4CAF50;
            cursor: pointer;
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div id="graph"></div>
    <div id="sidebar">
        <h2>🔍 Claude Code Knowledge Graph</h2>

        <div id="legend">
            <div class="legend-item"><div class="legend-dot" style="background:#4CAF50"></div> Session</div>
            <div class="legend-item"><div class="legend-dot" style="background:#2196F3"></div> Agent Execution</div>
            <div class="legend-item"><div class="legend-dot" style="background:#FF9800"></div> Commit</div>
        </div>

        <div id="details">
            <p id="no-selection">Click a node to see details</p>
        </div>

        <div id="help">
            <strong>Controls:</strong><br>
            • Click node to inspect<br>
            • Scroll to zoom<br>
            • Drag to pan<br>
            • Drag node to reposition
        </div>
    </div>

    <script>
        const nodeDetails = {json.dumps(node_details)};

        const nodes = new vis.DataSet({json.dumps(nodes)});
        const edges = new vis.DataSet({json.dumps(edges)});

        const container = document.getElementById('graph');
        const data = {{ nodes, edges }};

        const options = {{
            nodes: {{
                shape: 'box',
                font: {{
                    size: 11,
                    color: '#fff',
                    face: 'Monaco, monospace'
                }},
                margin: 8,
                borderWidth: 2,
                shadow: true
            }},
            edges: {{
                font: {{ size: 9, color: '#888', strokeWidth: 0 }},
                smooth: {{ type: 'curvedCW', roundness: 0.2 }}
            }},
            groups: {{
                session: {{
                    color: {{ background: '#1b5e20', border: '#4CAF50' }},
                    font: {{ color: '#fff' }}
                }},
                agent: {{
                    color: {{ background: '#0d47a1', border: '#2196F3' }},
                    font: {{ color: '#fff' }}
                }},
                commit: {{
                    color: {{ background: '#e65100', border: '#FF9800' }},
                    font: {{ color: '#fff' }}
                }}
            }},
            physics: {{
                enabled: true,
                solver: 'forceAtlas2Based',
                forceAtlas2Based: {{
                    gravitationalConstant: -50,
                    centralGravity: 0.01,
                    springLength: 100,
                    springConstant: 0.08
                }},
                stabilization: {{ iterations: 150 }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 100
            }}
        }};

        const network = new vis.Network(container, data, options);

        network.on('click', function(params) {{
            const detailsDiv = document.getElementById('details');

            if (params.nodes.length > 0) {{
                const nodeId = params.nodes[0];
                const details = nodeDetails[nodeId];

                if (details) {{
                    let html = '<h3>' + details.type + '</h3>';

                    if (details.type === 'Session') {{
                        html += `
                            <div class="detail-row">
                                <div class="detail-label">Session ID</div>
                                <div class="detail-value mono">${{details.id}}</div>
                            </div>
                            <div class="detail-row">
                                <div class="detail-label">Started</div>
                                <div class="detail-value">${{details.start_time}}</div>
                            </div>
                            <div class="detail-row">
                                <div class="detail-label">Directory</div>
                                <div class="detail-value mono">${{details.directory}}</div>
                            </div>
                            <div class="detail-row">
                                <div class="detail-label">Messages</div>
                                <div class="detail-value">${{details.message_count}} messages (${{details.total_events}} events)</div>
                            </div>
                        `;
                    }} else if (details.type === 'AgentExecution') {{
                        html += `
                            <div class="detail-row">
                                <div class="detail-label">Agent ID</div>
                                <div class="detail-value mono">${{details.agent_id}}</div>
                            </div>
                            <div class="detail-row">
                                <div class="detail-label">Completed At</div>
                                <div class="detail-value">${{details.timestamp}}</div>
                            </div>
                            <div class="detail-row">
                                <div class="detail-label">Session</div>
                                <div class="detail-value mono">${{details.session_id}}</div>
                            </div>
                            <div class="detail-row">
                                <div class="detail-label">Transcript</div>
                                <div class="detail-value mono" style="font-size:10px">${{details.transcript_path || 'N/A'}}</div>
                            </div>
                        `;
                    }} else if (details.type === 'Commit') {{
                        html += `
                            <div class="detail-row">
                                <div class="detail-label">Hash</div>
                                <div class="detail-value mono">${{details.hash}}</div>
                            </div>
                            <div class="detail-row">
                                <div class="detail-label">Message</div>
                                <div class="detail-value">${{details.message}}</div>
                            </div>
                            <div class="detail-row">
                                <div class="detail-label">Timestamp</div>
                                <div class="detail-value">${{details.timestamp}}</div>
                            </div>
                        `;

                        if (details.correlations && details.correlations.length > 0) {{
                            html += '<h3>Agent Correlations</h3>';
                            details.correlations.forEach(c => {{
                                html += `
                                    <div class="correlation">
                                        <div class="detail-label">Agent</div>
                                        <div class="detail-value mono">${{c.agent_id}}</div>
                                        <div class="detail-label" style="margin-top:5px">Timing</div>
                                        <div class="detail-value">${{c.seconds_before}}s before commit</div>
                                    </div>
                                `;
                            }});
                        }} else {{
                            html += '<div class="detail-row"><div class="detail-value" style="color:#888">No agent correlation found</div></div>';
                        }}
                    }}

                    detailsDiv.innerHTML = html;
                }}
            }} else {{
                detailsDiv.innerHTML = '<p id="no-selection">Click a node to see details</p>';
            }}
        }});

        // Stabilization message
        network.on('stabilizationProgress', function(params) {{
            console.log('Stabilizing: ' + Math.round(params.iterations/params.total * 100) + '%');
        }});

        network.once('stabilizationIterationsDone', function() {{
            console.log('Graph stabilized');
            network.setOptions({{ physics: {{ enabled: false }} }});
        }});
    </script>
</body>
</html>'''


if __name__ == '__main__':
    main()
