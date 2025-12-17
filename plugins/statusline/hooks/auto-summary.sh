#!/bin/bash
#
# Auto-generate session summary using headless Claude
#
# Triggers on UserPromptSubmit - reads recent conversation context
# and generates a 5-10 word first-person summary via headless Claude.
#
# Receives JSON via stdin with:
# - session_id: Unique session identifier

# Read JSON input
INPUT=$(cat)

# Parse session ID
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')

# Exit if no session ID
if [ -z "$SESSION_ID" ]; then
    exit 0
fi

# Find instances directory
INSTANCES_DIR=""
for loc in ".claude/instances" "$HOME/.claude/instances"; do
    if [ -d "$loc" ]; then
        INSTANCES_DIR="$loc"
        break
    fi
done

if [ -z "$INSTANCES_DIR" ]; then
    exit 0
fi

# Get agent name from registry
REGISTRY="$INSTANCES_DIR/registry.json"
AGENT_NAME="Claude"
if [ -f "$REGISTRY" ]; then
    AGENT_NAME=$(jq -r --arg sid "$SESSION_ID" '.[$sid].name // "Claude"' "$REGISTRY" 2>/dev/null)
fi

# Find the most recent log file for this session
LOG_DIR=".claude/logging"
if [ ! -d "$LOG_DIR" ]; then
    LOG_DIR="$HOME/.claude/logging"
fi

# Find log file matching session ID
LOG_FILE=$(find "$LOG_DIR" -name "*${SESSION_ID:0:8}*.jsonl" -type f 2>/dev/null | head -1)

if [ -z "$LOG_FILE" ] || [ ! -f "$LOG_FILE" ]; then
    exit 0
fi

# Extract last few user/assistant messages for context (grep then parse for efficiency)
CONTEXT=$(grep -E '"UserPromptSubmit"|"AssistantResponse"' "$LOG_FILE" | tail -6 | jq -r '
    if .type == "UserPromptSubmit" then "User: " + ((.data.prompt // "")[0:150])
    elif .type == "AssistantResponse" then "Assistant: " + ((.data.response // "")[0:150])
    else empty end
' 2>/dev/null)

if [ -z "$CONTEXT" ]; then
    exit 0
fi

# Get previous summaries for continuity
HISTORY_FILE="$INSTANCES_DIR/summaries/${SESSION_ID}.history"
PREV_SUMMARIES=""
if [ -f "$HISTORY_FILE" ]; then
    PREV_SUMMARIES=$(tail -3 "$HISTORY_FILE" 2>/dev/null)
fi

# Generate summary using headless Claude
SUMMARY_FILE="$INSTANCES_DIR/summaries/${SESSION_ID}.txt"
mkdir -p "$INSTANCES_DIR/summaries"

PROMPT="You are $AGENT_NAME. Based on this recent conversation, write a 5-10 word first-person summary of what you're working on. Be concise and natural.

Previous summaries for continuity:
$PREV_SUMMARIES

Recent conversation:
$CONTEXT

Write ONLY the summary, nothing else:"

# Unset API key so headless Claude uses Max subscription instead of API credits
unset ANTHROPIC_API_KEY

# Call headless Claude (with timeout, using haiku for speed/cost)
SUMMARY=$(printf '%s' "$PROMPT" | timeout 30 claude -p --model haiku 2>/dev/null | head -1)

if [ -n "$SUMMARY" ]; then
    # Write to files
    echo "$SUMMARY" > "$SUMMARY_FILE"
    echo "$SUMMARY" >> "$HISTORY_FILE"
fi

exit 0
