#!/bin/bash
#
# Claude Code Statusline - Instance Identity Display
#
# Displays: [Name:id] Model | dir | ctx:N% | $X.XX | #N Tm | branch +X/-Y
#           comprehensive summary (on second line)
#
# Branch color: blue=clean, red=dirty
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
# Show full path, shortened with ~ for home
CWD_DISPLAY=$(echo "$CURRENT_DIR" | sed "s|^$HOME|~|")

# Context window percentage - simple calculation from cache tokens
CTX_SIZE=$(echo "$input" | jq -r '.context_window.context_window_size // 200000')
CURRENT_INPUT=$(echo "$input" | jq -r '.context_window.current_usage.input_tokens // 0')
CACHE_CREATION=$(echo "$input" | jq -r '.context_window.current_usage.cache_creation_input_tokens // 0')
CACHE_READ=$(echo "$input" | jq -r '.context_window.current_usage.cache_read_input_tokens // 0')

# Total tokens from current_usage
TOTAL_TOKENS=$((CURRENT_INPUT + CACHE_CREATION + CACHE_READ))

if [ "$CTX_SIZE" -gt 0 ] && [ "$TOTAL_TOKENS" -gt 0 ]; then
    PCT=$((TOTAL_TOKENS * 100 / CTX_SIZE))
else
    PCT=0
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

# Extract short model name (Opus, Sonnet, Haiku)
MODEL_SHORT=$(echo "$MODEL" | sed -E 's/.*(Opus|Sonnet|Haiku).*/\1/')
if [ -z "$MODEL_SHORT" ] || [ "$MODEL_SHORT" = "$MODEL" ]; then
    MODEL_SHORT="Claude"
fi

# Backfill model to registry if missing
if [ -n "$REGISTRY" ] && [ -n "$SESSION_ID" ] && [ "$SESSION_ID" != "unknown" ]; then
    STORED_MODEL=$(jq -r --arg sid "$SESSION_ID" '.[$sid].model // empty' "$REGISTRY" 2>/dev/null)
    if [ -z "$STORED_MODEL" ] && [ -n "$MODEL" ] && [ "$MODEL" != "Claude" ]; then
        jq --arg sid "$SESSION_ID" --arg model "$MODEL" \
           '.[$sid].model = $model' "$REGISTRY" > "$REGISTRY.tmp" 2>/dev/null && \
           mv "$REGISTRY.tmp" "$REGISTRY" 2>/dev/null
    fi
fi

# Read user prompt count (default to 0 for new sessions)
MSG_COUNT="0"
COUNTS_DIR=$(dirname "$REGISTRY")/counts
COUNT_FILE="$COUNTS_DIR/${SESSION_ID}.txt"
if [ -f "$COUNT_FILE" ]; then
    MSG_COUNT=$(cat "$COUNT_FILE" 2>/dev/null)
fi

# Calculate session duration (default to 0m for new sessions)
DURATION="0m"
if [ -n "$REGISTRY" ] && [ -n "$SESSION_ID" ]; then
    CREATED=$(jq -r --arg sid "$SESSION_ID" '.[$sid].created // empty' "$REGISTRY" 2>/dev/null)
    if [ -n "$CREATED" ]; then
        # Convert ISO timestamp to epoch
        CREATED_EPOCH=$(date -d "$CREATED" +%s 2>/dev/null)
        NOW_EPOCH=$(date +%s)
        if [ -n "$CREATED_EPOCH" ]; then
            DIFF=$((NOW_EPOCH - CREATED_EPOCH))
            HOURS=$((DIFF / 3600))
            MINS=$(((DIFF % 3600) / 60))
            if [ "$HOURS" -gt 0 ]; then
                DURATION="${HOURS}h${MINS}m"
            else
                DURATION="${MINS}m"
            fi
        fi
    fi
fi

# Git info: branch, dirty state, and diff stats
BRANCH=""
GIT_DIRTY=""
GIT_STATS=""
if command -v git &> /dev/null && git rev-parse --git-dir &> /dev/null; then
    BRANCH=$(git branch --show-current 2>/dev/null)

    # Check if workspace is dirty
    if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
        GIT_DIRTY="yes"
    fi

    # Get diff stats (insertions/deletions) including untracked files
    # Use HEAD to include both staged and unstaged changes
    DIFF_STAT=$(git diff --shortstat HEAD 2>/dev/null)
    INSERTIONS=0
    DELETIONS=0
    if [ -n "$DIFF_STAT" ]; then
        # Parse: " 3 files changed, 45 insertions(+), 12 deletions(-)"
        INSERTIONS=$(echo "$DIFF_STAT" | grep -oP '\d+(?= insertion)' || echo "0")
        DELETIONS=$(echo "$DIFF_STAT" | grep -oP '\d+(?= deletion)' || echo "0")
        [ -z "$INSERTIONS" ] && INSERTIONS="0"
        [ -z "$DELETIONS" ] && DELETIONS="0"
    fi

    # Add lines from untracked files to insertions count
    UNTRACKED_LINES=$(git status --porcelain 2>/dev/null | grep "^??" | cut -c4- | xargs wc -l 2>/dev/null | tail -1 | awk '{print $1}')
    [ -n "$UNTRACKED_LINES" ] && INSERTIONS=$((INSERTIONS + UNTRACKED_LINES))

    if [ "$INSERTIONS" != "0" ] || [ "$DELETIONS" != "0" ]; then
        GIT_STATS="+${INSERTIONS}/-${DELETIONS}"
    fi
fi

# Read conversation summary if available
SUMMARY=""
SUMMARY_DIR=$(dirname "$REGISTRY")/summaries
SUMMARY_FILE="$SUMMARY_DIR/${SESSION_ID}.txt"
if [ -f "$SUMMARY_FILE" ]; then
    SUMMARY=$(cat "$SUMMARY_FILE" 2>/dev/null)
fi

# Output the statusline
# Format: [Name:id] Model | dir | ctx:N% | $X.XX | #N Tm | branch +X/-Y
#         summary on next line
MAGENTA="\033[35m"
BLUE="\033[34m"
RED="\033[31m"

# Build the first line
LINE1="${CYAN}[${NAME}:${SHORT_ID}]${RST} ${YELLOW}${MODEL_SHORT}${RST} | ${DIM}${CWD_DISPLAY}${RST} | ${CTX_COLOR}ctx:${PCT}%${RST} | ${GREEN}\$${COST_FMT}${RST}"

# Add message count and duration (with pipe between them)
if [ -n "$MSG_COUNT" ]; then
    LINE1="${LINE1} | ${MAGENTA}#${MSG_COUNT}${RST}"
    if [ -n "$DURATION" ]; then
        LINE1="${LINE1} | ${DIM}${DURATION}${RST}"
    fi
fi

# Add git info: branch (blue=clean, red=dirty) and diff stats
if [ -n "$BRANCH" ]; then
    if [ -n "$GIT_DIRTY" ]; then
        LINE1="${LINE1} | ${RED}${BRANCH}${RST}"
    else
        LINE1="${LINE1} | ${BLUE}${BRANCH}${RST}"
    fi
    if [ -n "$GIT_STATS" ]; then
        LINE1="${LINE1} ${DIM}${GIT_STATS}${RST}"
    fi
fi

echo -e "$LINE1"

# Second line: summary (if available)
if [ -n "$SUMMARY" ]; then
    echo -e "${DIM}${SUMMARY}${RST}"
fi
