#!/bin/bash
#
# Track user prompt submissions per session
#
# Receives JSON via stdin with:
# - session_id: Unique session identifier
# - cwd: Current working directory
#
# Increments counter in .claude/instances/counts/{session_id}.txt

# Read JSON input
INPUT=$(cat)

# Parse fields
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')
CWD=$(echo "$INPUT" | jq -r '.cwd // empty')

# Exit if no session ID
if [ -z "$SESSION_ID" ]; then
    exit 0
fi

# Find instances directory (use absolute CWD path, fallback to HOME)
INSTANCES_DIR=""
for loc in "$CWD/.claude/instances" "$HOME/.claude/instances"; do
    if [ -d "$loc" ]; then
        INSTANCES_DIR="$loc"
        break
    fi
done

if [ -z "$INSTANCES_DIR" ]; then
    exit 0
fi

# Create counts directory
COUNTS_DIR="$INSTANCES_DIR/counts"
mkdir -p "$COUNTS_DIR"

# Increment counter
COUNT_FILE="$COUNTS_DIR/${SESSION_ID}.txt"
if [ -f "$COUNT_FILE" ]; then
    COUNT=$(cat "$COUNT_FILE")
    COUNT=$((COUNT + 1))
else
    COUNT=1
fi

echo "$COUNT" > "$COUNT_FILE"

exit 0
