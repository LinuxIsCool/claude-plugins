#!/bin/bash
# Wrapper for auto-description.py to handle stdin for uv run
#
# uv run scripts can have issues reading stdin directly, so this wrapper:
# 1. Captures stdin (hook JSON from Claude Code)
# 2. Sets HOOK_INPUT environment variable
# 3. Runs the Python script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Read stdin and store it
HOOK_INPUT=$(cat)

# Export for Python script to read
export HOOK_INPUT

# Run the description generator
# Use uv run for dependency management (anthropic package)
cd "$SCRIPT_DIR" && uv run --script auto-description.py
