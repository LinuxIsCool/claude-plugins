#!/bin/bash
#
# Wrapper for auto-summary.py that handles stdin properly
# uv run doesn't pass stdin through, so we capture it first
#

# Read stdin into variable
INPUT=$(cat)

# Debug output if DEBUG_SUMMARY is set
if [ -n "$DEBUG_SUMMARY" ]; then
    echo "[wrapper] Input length: ${#INPUT}" >&2
    echo "[wrapper] Input: $INPUT" >&2
fi

# Pass via environment variable to the Python script
export HOOK_INPUT="$INPUT"

# Run the script (from same directory as this wrapper)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
uv run "${SCRIPT_DIR}/auto-summary.py"
