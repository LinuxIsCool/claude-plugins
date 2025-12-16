#!/bin/bash
#
# Claude Code Statusline - Instance Identity Display
#
# Displays: [Name:id] dir | ctx:N% | $X.XX
#
# Receives JSON from Claude Code via stdin with:
# - session_id: Unique session identifier
# - model.display_name: Current model
# - workspace.current_dir: Working directory
# - context_window.*: Token usage
# - cost.total_cost_usd: Session cost
#
# Install: Copy to ~/.claude/statusline.sh and chmod +x
# Configure in ~/.claude/settings.json:
# {
#   "statusLine": {
#     "type": "command",
#     "command": "~/.claude/statusline.sh"
#   }
# }

# Read JSON input
input=$(cat)

# Parse fields with jq
SESSION_ID=$(echo "$input" | jq -r '.session_id // "unknown"')
SHORT_ID=$(echo "$SESSION_ID" | cut -c1-5)
MODEL=$(echo "$input" | jq -r '.model.display_name // "Claude"')
CURRENT_DIR=$(echo "$input" | jq -r '.workspace.current_dir // ""')
DIR_NAME=$(basename "$CURRENT_DIR" 2>/dev/null || echo "~")

# Context window percentage
# Use current_usage if available (more accurate), otherwise calculate manually
PCT=$(echo "$input" | jq -r '.current_usage // empty')
if [ -z "$PCT" ] || [ "$PCT" = "null" ]; then
    # Fallback to manual calculation
    INPUT_TOKENS=$(echo "$input" | jq -r '.context_window.total_input_tokens // 0')
    OUTPUT_TOKENS=$(echo "$input" | jq -r '.context_window.total_output_tokens // 0')
    CTX_SIZE=$(echo "$input" | jq -r '.context_window.context_window_size // 200000')
    TOTAL_TOKENS=$((INPUT_TOKENS + OUTPUT_TOKENS))
    if [ "$CTX_SIZE" -gt 0 ]; then
        PCT=$((TOTAL_TOKENS * 100 / CTX_SIZE))
    else
        PCT=0
    fi
fi

# Cost
COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
COST_FMT=$(printf "%.2f" "$COST")

# Look up instance name from registry
# Check multiple locations for the registry
REGISTRY=""
for loc in ".claude/instances/registry.json" "$HOME/.claude/instances/registry.json"; do
    if [ -f "$loc" ]; then
        REGISTRY="$loc"
        break
    fi
done

# Get instance name from registry
REGISTERED_NAME=""
if [ -n "$REGISTRY" ] && command -v jq &> /dev/null; then
    REGISTERED_NAME=$(jq -r --arg sid "$SESSION_ID" '.[$sid].name // empty' "$REGISTRY" 2>/dev/null)
fi

# Determine display name
if [ -n "$REGISTERED_NAME" ] && [[ ! "$REGISTERED_NAME" =~ ^Claude- ]]; then
    # Custom name set - use it
    NAME="$REGISTERED_NAME"
else
    # No custom name - show just the model (Opus, Sonnet, Haiku)
    # The short_id is already shown after the colon
    NAME=$(echo "$MODEL" | sed -E 's/.*(Opus|Sonnet|Haiku).*/\1/')
    if [ -z "$NAME" ] || [ "$NAME" = "$MODEL" ]; then
        NAME="Claude"
    fi
fi

# ANSI colors (optional, comment out for plain text)
# Reset
RST="\033[0m"
# Colors
CYAN="\033[36m"
YELLOW="\033[33m"
GREEN="\033[32m"
DIM="\033[2m"

# Context color based on usage
if [ "$PCT" -lt 50 ]; then
    CTX_COLOR="$GREEN"
elif [ "$PCT" -lt 80 ]; then
    CTX_COLOR="$YELLOW"
else
    CTX_COLOR="\033[31m"  # Red
fi

# Output the statusline
# Format: [Name:id] dir | ctx:N% | $X.XX
echo -e "${CYAN}[${NAME}:${SHORT_ID}]${RST} ${DIM}${DIR_NAME}${RST} | ${CTX_COLOR}ctx:${PCT}%${RST} | ${GREEN}\$${COST_FMT}${RST}"
