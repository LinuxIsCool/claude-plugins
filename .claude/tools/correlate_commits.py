#!/usr/bin/env python3
"""
Correlate git commits with SubagentStop events by timestamp proximity.

This demonstrates that we can link commits to agent executions without
requiring agents to self-report their IDs.
"""

import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import re

def parse_git_log(since_date: str = "2025-12-13") -> list[dict]:
    """Get commits with timestamps."""
    result = subprocess.run(
        ["git", "log", f"--since={since_date}", "--format=%H|%aI|%s"],
        capture_output=True, text=True
    )
    commits = []
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        parts = line.split('|', 2)
        if len(parts) == 3:
            commits.append({
                'hash': parts[0][:8],
                'timestamp': parts[1],
                'message': parts[2]
            })
    return commits

def parse_subagent_stops(log_dir: Path) -> list[dict]:
    """Get SubagentStop events from logs."""
    events = []
    for log_file in log_dir.glob("*.jsonl"):
        with open(log_file) as f:
            for line in f:
                try:
                    event = json.loads(line)
                    if event.get('type') == 'SubagentStop':
                        data = event.get('data', {})
                        agent_id = data.get('agent_id')
                        if agent_id:
                            events.append({
                                'timestamp': event['ts'],
                                'agent_id': agent_id,
                                'session_id': data.get('session_id', '')[:8]
                            })
                except:
                    pass
    return events

def parse_timestamp(ts: str) -> datetime:
    """Parse various timestamp formats."""
    # Remove timezone for simple comparison
    ts = re.sub(r'[+-]\d{2}:\d{2}$', '', ts)
    ts = ts.replace('T', ' ').split('.')[0]
    return datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')

def correlate(commits: list, agents: list, window_seconds: int = 120) -> list[dict]:
    """Find commits that occurred within window_seconds of agent completion."""
    correlations = []

    for commit in commits:
        commit_time = parse_timestamp(commit['timestamp'])

        # Find agents that completed within the window BEFORE the commit
        nearby_agents = []
        for agent in agents:
            agent_time = parse_timestamp(agent['timestamp'])
            delta = (commit_time - agent_time).total_seconds()

            # Agent completed 0-120 seconds before commit
            if 0 <= delta <= window_seconds:
                nearby_agents.append({
                    'agent_id': agent['agent_id'],
                    'session_id': agent['session_id'],
                    'seconds_before': int(delta)
                })

        if nearby_agents:
            # Sort by closest to commit time
            nearby_agents.sort(key=lambda x: x['seconds_before'])
            correlations.append({
                'commit': commit['hash'],
                'message': commit['message'],
                'commit_time': commit['timestamp'],
                'likely_agent': nearby_agents[0],  # Closest match
                'other_candidates': nearby_agents[1:] if len(nearby_agents) > 1 else []
            })

    return correlations

def main():
    # Find log directory
    log_dirs = [
        Path('.claude/logging/2025/12/15'),
        Path('.claude/logging/2025/12/13'),
    ]

    all_agents = []
    for log_dir in log_dirs:
        if log_dir.exists():
            all_agents.extend(parse_subagent_stops(log_dir))

    commits = parse_git_log("2025-12-13")
    correlations = correlate(commits, all_agents, window_seconds=120)

    print("=" * 70)
    print("COMMIT ↔ AGENT CORRELATION ANALYSIS")
    print("=" * 70)
    print(f"Commits analyzed: {len(commits)}")
    print(f"SubagentStop events: {len(all_agents)}")
    print(f"Correlations found: {len(correlations)}")
    print("=" * 70)
    print()

    for corr in correlations[:15]:  # Show first 15
        print(f"Commit: {corr['commit']}")
        print(f"  Message: {corr['message'][:60]}...")
        print(f"  Time: {corr['commit_time']}")
        agent = corr['likely_agent']
        print(f"  → Agent: {agent['agent_id']} (session {agent['session_id']}, {agent['seconds_before']}s before)")
        if corr['other_candidates']:
            print(f"    Other candidates: {[a['agent_id'] for a in corr['other_candidates']]}")
        print()

if __name__ == "__main__":
    main()
