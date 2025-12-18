#!/bin/bash
#
# Agent Scanner - Extract Claude agent panes from tmux
#
# Discovers Claude Code instances by scanning tmux pane titles.
# Claude Code sets pane titles via escape sequences with format: "✳ Summary"
#
# Output format (tab-separated):
#   session:window.pane \t pane_id \t pane_title
#
# The ✳ prefix indicates a Claude agent; other panes (nvim, fish, etc.)
# have titles like "nvim /path" or "fish /path".
#
# Usage:
#   ./agent-scanner.sh              # Scan all sessions for Claude agents
#   ./agent-scanner.sh --session=X  # Scan specific session only
#   ./agent-scanner.sh --all        # Include non-Claude panes too
#   ./agent-scanner.sh --format=fzf # Output formatted for fzf selection
#
# Exit codes:
#   0 - Success (found agents or not)
#   1 - Error (not in tmux, etc.)

set -euo pipefail

# Verify tmux is available
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
INCLUDE_ALL=false
OUTPUT_FORMAT="tsv"

while [[ $# -gt 0 ]]; do
    case $1 in
        --session=*)
            SESSION_FILTER="${1#*=}"
            shift
            ;;
        --all)
            INCLUDE_ALL=true
            shift
            ;;
        --format=*)
            OUTPUT_FORMAT="${1#*=}"
            shift
            ;;
        -h|--help)
            echo "Usage: agent-scanner.sh [OPTIONS]"
            echo ""
            echo "Scans tmux panes for Claude agent instances."
            echo ""
            echo "Options:"
            echo "  --session=NAME  Scan specific session only"
            echo "  --all           Include non-Claude panes"
            echo "  --format=FORMAT Output format: tsv (default), fzf"
            echo "  -h, --help      Show this help"
            echo ""
            echo "Output (tsv format):"
            echo "  session:window.pane \\t pane_id \\t pane_title"
            echo ""
            echo "Output (fzf format):"
            echo "  [session:window.pane] ✳ Summary Text"
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
    # Validate session exists
    if ! tmux has-session -t "$SESSION_FILTER" 2>/dev/null; then
        echo "Error: Session '$SESSION_FILTER' not found" >&2
        exit 1
    fi
    PANES=$(tmux list-panes -t "$SESSION_FILTER" -a -F '#{session_name}:#{window_index}.#{pane_index}	#{pane_id}	#{pane_title}' 2>/dev/null) || true
else
    PANES=$(tmux list-panes -a -F '#{session_name}:#{window_index}.#{pane_index}	#{pane_id}	#{pane_title}' 2>/dev/null) || true
fi

# Claude agent pattern: title starts with ✳
CLAUDE_PATTERN='^✳'

# Process panes
echo "$PANES" | while IFS=$'\t' read -r pane_ref pane_id pane_title; do
    # Skip if we couldn't parse the line
    [[ -z "$pane_ref" ]] && continue

    # Filter for Claude agents unless --all specified
    if [[ "$INCLUDE_ALL" != "true" ]]; then
        if ! echo "$pane_title" | grep -qE "$CLAUDE_PATTERN"; then
            continue
        fi
    fi

    # Output based on format
    case "$OUTPUT_FORMAT" in
        fzf)
            # Format for fzf: [pane_ref] pane_title
            # The pane_id is embedded in the pane_ref for later extraction
            printf '[%s] %s\n' "$pane_ref" "$pane_title"
            ;;
        *)
            # Default TSV format
            printf '%s\t%s\t%s\n' "$pane_ref" "$pane_id" "$pane_title"
            ;;
    esac
done

# Exit successfully even if no agents found (empty output is valid)
exit 0
