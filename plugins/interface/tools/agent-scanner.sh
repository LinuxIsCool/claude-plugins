#!/bin/bash
#
# Agent Scanner - Extract Claude agent panes from tmux
#
# Scans all tmux panes across all sessions for Claude agent statuslines.
# Detects the pattern: [Name:xxxxx] produced by the statusline plugin.
#
# Output format (tab-separated):
#   session:window.pane \t statusline_content
#
# Usage:
#   ./agent-scanner.sh              # Scan all sessions
#   ./agent-scanner.sh --session=X  # Scan specific session only
#
# Exit codes:
#   0 - Success (found agents or not)
#   1 - Error (not in tmux, etc.)

set -euo pipefail

# Verify we're in tmux (or tmux is available)
if ! command -v tmux &>/dev/null; then
    echo "Error: tmux not found" >&2
    exit 1
fi

if ! tmux list-sessions &>/dev/null; then
    echo "Error: No tmux sessions found" >&2
    exit 1
fi

# Parse arguments
SESSION_FILTER=""
while [[ $# -gt 0 ]]; do
    case $1 in
        --session=*)
            SESSION_FILTER="${1#*=}"
            shift
            ;;
        -h|--help)
            echo "Usage: agent-scanner.sh [--session=NAME]"
            echo "Scans tmux panes for Claude agent statuslines."
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Build pane list command
if [[ -n "$SESSION_FILTER" ]]; then
    PANE_LIST_CMD="tmux list-panes -t '$SESSION_FILTER' -a -F '#{session_name}:#{window_index}.#{pane_index}\t#{pane_id}'"
else
    PANE_LIST_CMD="tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index}\t#{pane_id}'"
fi

# Statusline pattern: [Name:xxxxx] where Name can contain letters/numbers/spaces
# and xxxxx is the short session ID (typically 5 alphanumeric chars)
STATUSLINE_PATTERN='\[[^]]+:[a-zA-Z0-9]{5}\]'

# Scan all panes
eval "$PANE_LIST_CMD" 2>/dev/null | while IFS=$'\t' read -r pane_ref pane_id; do
    # Skip if we couldn't parse the line
    [[ -z "$pane_ref" ]] && continue

    # Capture first 3 lines of pane (statusline is typically at top)
    # Use || true to prevent set -e from killing us on capture errors
    content=$(tmux capture-pane -t "$pane_id" -p -S 0 -E 2 2>/dev/null) || true

    # Skip if capture failed or empty
    [[ -z "$content" ]] && continue

    # Look for statusline pattern in captured content
    # Extract the full line containing the pattern
    statusline=$(echo "$content" | grep -E "$STATUSLINE_PATTERN" 2>/dev/null | head -1) || true

    # Only output if we found a statusline
    if [[ -n "$statusline" ]]; then
        # Output: pane_ref \t statusline (tab-separated for easy parsing)
        printf '%s\t%s\n' "$pane_ref" "$statusline"
    fi
done

# Exit successfully even if no agents found (empty output is valid)
exit 0
