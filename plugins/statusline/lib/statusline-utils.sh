#!/bin/bash
#
# Statusline shared utilities
#
# Source this file from hooks and tools:
#   SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
#   source "$SCRIPT_DIR/../lib/statusline-utils.sh"
#

# ============================================================================
# Configuration
# ============================================================================

STATUSLINE_LOG="${STATUSLINE_LOG:-$HOME/.claude/instances/statusline.jsonl}"
STATUSLINE_INSTANCES_DIR="${STATUSLINE_INSTANCES_DIR:-$HOME/.claude/instances}"

# ============================================================================
# Logging
# ============================================================================

# Log a statusline event to JSONL
#
# Usage: log_statusline <type> <session_id> <value> [ok]
#
# Arguments:
#   type       - Event type (session_start, session_resume, prompt_count, etc.)
#   session_id - Full session ID (will be truncated to 8 chars)
#   value      - Event value/payload
#   ok         - Optional boolean (default: true)
#
# Example:
#   log_statusline "session_start" "$SESSION_ID" "cwd=$CWD"
#   log_statusline "error" "$SESSION_ID" "registry write failed" false
#
log_statusline() {
    local type="$1"
    local session="$2"
    local value="$3"
    local ok="${4:-true}"

    local ts
    ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local short_session="${session:0:8}"

    mkdir -p "$(dirname "$STATUSLINE_LOG")"
    echo "{\"ts\":\"$ts\",\"session\":\"$short_session\",\"type\":\"$type\",\"value\":\"$value\",\"ok\":$ok}" >> "$STATUSLINE_LOG"
}

# Log a complex object (JSON value instead of string)
#
# Usage: log_statusline_json <type> <session_id> <json_value> [ok]
#
# Example:
#   log_statusline_json "statusline_render" "$SESSION_ID" "$json_object"
#
log_statusline_json() {
    local type="$1"
    local session="$2"
    local json_value="$3"
    local ok="${4:-true}"

    local ts
    ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local short_session="${session:0:8}"

    mkdir -p "$(dirname "$STATUSLINE_LOG")"
    echo "{\"ts\":\"$ts\",\"session\":\"$short_session\",\"type\":\"$type\",\"value\":$json_value,\"ok\":$ok}" >> "$STATUSLINE_LOG"
}

# ============================================================================
# Registry operations (atomic with flock)
# ============================================================================

# Atomically update registry.json using flock
#
# Usage: update_registry <registry_path> <jq_args...> <jq_filter>
#
# All arguments after registry_path are passed directly to jq.
# Uses flock to prevent race conditions when multiple scripts write.
#
# Example:
#   update_registry "$REGISTRY" --arg sid "$SESSION_ID" --arg ts "$TS" \
#       '.[$sid].last_seen = $ts'
#
# Returns: 0 on success, 1 on failure
#
update_registry() {
    local registry="$1"
    shift

    # Ensure registry exists
    if [ ! -f "$registry" ]; then
        mkdir -p "$(dirname "$registry")"
        echo "{}" > "$registry"
    fi

    # Use flock for atomic update
    (
        flock -x 200 || { echo "Failed to acquire lock" >&2; exit 1; }
        if jq "$@" "$registry" > "$registry.tmp" 2>/dev/null; then
            mv "$registry.tmp" "$registry"
        else
            rm -f "$registry.tmp" 2>/dev/null
            exit 1
        fi
    ) 200>"$registry.lock"
}

# ============================================================================
# Path utilities
# ============================================================================

# Get the plugin root directory (parent of lib/)
# Useful when scripts need to reference other plugin files
#
# Usage: plugin_root=$(get_statusline_plugin_root)
#
get_statusline_plugin_root() {
    local lib_dir
    lib_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    dirname "$lib_dir"
}
