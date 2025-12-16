#!/bin/bash
#
# Auto-register Claude instance on session start
#
# Receives JSON via stdin with:
# - session_id: Unique session identifier
# - cwd: Current working directory
# - source: startup|resume|clear|compact
#
# Registers instance in .claude/instances/registry.json
# Exports SESSION_ID via CLAUDE_ENV_FILE for Claude to use

# Read JSON input
INPUT=$(cat)

# Parse fields
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')
CWD=$(echo "$INPUT" | jq -r '.cwd // empty')
SOURCE=$(echo "$INPUT" | jq -r '.source // "unknown"')

# Exit if no session ID
if [ -z "$SESSION_ID" ]; then
    exit 0
fi

# Find registry location (project or home)
REGISTRY=""
for loc in "$CWD/.claude/instances/registry.json" "$HOME/.claude/instances/registry.json"; do
    dir=$(dirname "$loc")
    if [ -d "$dir" ] || [ -d "$(dirname "$dir")/.claude" ]; then
        mkdir -p "$dir"
        REGISTRY="$loc"
        break
    fi
done

# Fallback to home
if [ -z "$REGISTRY" ]; then
    mkdir -p "$HOME/.claude/instances"
    REGISTRY="$HOME/.claude/instances/registry.json"
fi

# Initialize registry if needed
if [ ! -f "$REGISTRY" ]; then
    echo "{}" > "$REGISTRY"
fi

# Check if already registered
EXISTING=$(jq -r --arg sid "$SESSION_ID" '.[$sid].name // empty' "$REGISTRY" 2>/dev/null)

if [ -n "$EXISTING" ]; then
    # Update last_seen only
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    jq --arg sid "$SESSION_ID" \
       --arg ts "$TIMESTAMP" \
       '.[$sid].last_seen = $ts | .[$sid].status = "active"' \
       "$REGISTRY" > "$REGISTRY.tmp" && mv "$REGISTRY.tmp" "$REGISTRY"
else
    # New registration with default name
    TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    SHORT_ID=$(echo "$SESSION_ID" | cut -c1-8)
    DEFAULT_NAME="Claude-$SHORT_ID"
    DIR_NAME=$(basename "$CWD" 2>/dev/null || echo "unknown")

    jq --arg sid "$SESSION_ID" \
       --arg name "$DEFAULT_NAME" \
       --arg cwd "$CWD" \
       --arg ts "$TIMESTAMP" \
       --arg dir "$DIR_NAME" \
       '.[$sid] = {
         "name": $name,
         "task": ("Working in " + $dir),
         "model": "",
         "cwd": $cwd,
         "created": $ts,
         "last_seen": $ts,
         "status": "active"
       }' \
       "$REGISTRY" > "$REGISTRY.tmp" && mv "$REGISTRY.tmp" "$REGISTRY"
fi

# Determine current name
CURRENT_NAME="${EXISTING:-$DEFAULT_NAME}"
SHORT_ID=$(echo "$SESSION_ID" | cut -c1-8)

# Export SESSION_ID via CLAUDE_ENV_FILE (if available)
# This makes $SESSION_ID available to Claude for the rest of the session
if [ -n "$CLAUDE_ENV_FILE" ]; then
    echo "SESSION_ID=$SESSION_ID" >> "$CLAUDE_ENV_FILE"
    echo "INSTANCE_NAME=$CURRENT_NAME" >> "$CLAUDE_ENV_FILE"
fi

# Output context for Claude
# This text is added to Claude's context at session start
if [ "$SOURCE" = "startup" ]; then
    if [ -z "$EXISTING" ]; then
        # New session - prompt for self-naming
        cat << EOF
[statusline] Session $SHORT_ID registered. Statusline shows: [Model-$SHORT_ID:$SHORT_ID]
When you understand the user's task, name yourself:
  python3 plugins/statusline/tools/registry.py register "\$SESSION_ID" "Name" --task "description"
EOF
    else
        # Resuming with existing custom name
        echo "[statusline] Session $SHORT_ID: \"$EXISTING\""
    fi
elif [ "$SOURCE" = "resume" ]; then
    if [[ "$CURRENT_NAME" =~ ^Claude- ]]; then
        echo "[statusline] Resumed $SHORT_ID (no custom name yet)"
    else
        echo "[statusline] Resumed $SHORT_ID as \"$CURRENT_NAME\""
    fi
fi

exit 0
