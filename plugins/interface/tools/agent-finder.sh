#!/bin/bash
#
# Agent Finder - Interactive fuzzy finder for Claude agent panes
#
# Uses fzf to present a searchable list of Claude agent panes,
# then switches to the selected pane.
#
# Designed to be invoked from:
#   - tmux display-popup (recommended)
#   - Direct shell execution
#   - tmux keybinding
#
# Usage:
#   ./agent-finder.sh              # Interactive fuzzy finder
#   ./agent-finder.sh --popup      # Optimized for tmux popup context
#   ./agent-finder.sh --preview    # Include preview pane
#
# Keybinding example (add to ~/.tmux.conf):
#   bind-key g display-popup -E -w 80% -h 60% "path/to/agent-finder.sh --popup"
#
# Exit codes:
#   0 - Success (selection made or cancelled)
#   1 - Error (dependencies missing, etc.)

set -euo pipefail

# Script directory (for finding agent-scanner.sh)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCANNER="${SCRIPT_DIR}/agent-scanner.sh"

# Verify dependencies
if ! command -v fzf &>/dev/null; then
    echo "Error: fzf not found. Install with: sudo apt install fzf" >&2
    exit 1
fi

if ! command -v tmux &>/dev/null; then
    echo "Error: tmux not found" >&2
    exit 1
fi

if [[ ! -x "$SCANNER" ]]; then
    echo "Error: agent-scanner.sh not found or not executable at: $SCANNER" >&2
    exit 1
fi

# Parse arguments
POPUP_MODE=false
PREVIEW_MODE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --popup)
            POPUP_MODE=true
            shift
            ;;
        --preview)
            PREVIEW_MODE=true
            shift
            ;;
        -h|--help)
            echo "Usage: agent-finder.sh [OPTIONS]"
            echo ""
            echo "Interactive fuzzy finder for Claude agent panes."
            echo ""
            echo "Options:"
            echo "  --popup    Optimized for tmux popup context"
            echo "  --preview  Show preview pane with pane content"
            echo "  -h, --help Show this help"
            echo ""
            echo "Keybinding example (add to ~/.tmux.conf):"
            echo "  bind-key g display-popup -E -w 80% -h 60% \"${SCRIPT_DIR}/agent-finder.sh --popup\""
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# Get list of Claude agents in fzf format
AGENTS=$("$SCANNER" --format=fzf)

if [[ -z "$AGENTS" ]]; then
    echo "No Claude agents found in tmux panes." >&2
    echo "Agents are identified by pane titles starting with ✳" >&2
    exit 0
fi

# Build fzf options
FZF_OPTS=(
    --ansi
    --no-multi
    --reverse
    --border=rounded
    --border-label=" Claude Agents "
    --prompt="Jump to > "
    --header="Select an agent pane to switch to (ESC to cancel)"
    --header-first
    --height=100%
)

# Add preview if requested
if [[ "$PREVIEW_MODE" == "true" ]]; then
    # Preview shows captured pane content
    # Use awk for safer extraction to avoid command injection
    FZF_OPTS+=(
        --preview='pane_ref=$(echo {} | awk -F"[][]" "{print \$2}"); tmux capture-pane -t "$pane_ref" -p -S -10 2>/dev/null | head -20'
        --preview-window=right:40%:wrap
    )
fi

# Run fzf for selection
SELECTED=$(echo "$AGENTS" | fzf "${FZF_OPTS[@]}") || true

# If nothing selected (ESC pressed), exit gracefully
if [[ -z "$SELECTED" ]]; then
    exit 0
fi

# Extract pane reference from selected line
# Format: [session:window.pane] ✳ Summary
PANE_REF=$(echo "$SELECTED" | sed 's/^\[\([^]]*\)\].*/\1/')

if [[ -z "$PANE_REF" ]]; then
    echo "Error: Could not extract pane reference from selection" >&2
    exit 1
fi

# Parse session and window.pane
SESSION_NAME=$(echo "$PANE_REF" | cut -d: -f1)
WINDOW_PANE=$(echo "$PANE_REF" | cut -d: -f2)

# Switch to the selected pane
# tmux select-pane -t target automatically selects the window too
if [[ "$POPUP_MODE" == "true" ]]; then
    # In popup mode, switch-client changes session if needed
    tmux switch-client -t "${SESSION_NAME}:${WINDOW_PANE}"
else
    # Direct mode: select the pane (implicitly selects window)
    tmux select-pane -t "${SESSION_NAME}:${WINDOW_PANE}"
fi

exit 0
