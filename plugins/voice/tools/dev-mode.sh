#!/usr/bin/env bash
# dev-mode.sh - Enable hot-reload development for voice plugin
#
# Voice plugin hooks execute external Bun processes, which means
# the TypeScript code is read from disk on EVERY hook invocation.
# By symlinking the cache to source, edits take effect immediately
# without restarting Claude Code.
#
# Usage:
#   ./dev-mode.sh enable   # Symlink cache → source (hot reload)
#   ./dev-mode.sh disable  # Restore copy-based cache
#   ./dev-mode.sh status   # Check current mode
#
# What hot-reloads (no restart needed):
#   - hooks/voice-hook.ts     Main hook logic
#   - src/adapters/tts/*.ts   TTS backends
#   - src/identity/*.ts       Voice resolution
#   - src/ports/*.ts          Port interfaces
#
# What still requires restart:
#   - .claude-plugin/plugin.json  (skills, commands, agents declarations)
#   - New skill files
#   - New command files
#   - Agent markdown files

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$SCRIPT_DIR"
CACHE_BASE="$HOME/.claude/plugins/cache/linuxiscool-claude-plugins/voice"
VERSION="0.1.0"
CACHE_DIR="$CACHE_BASE/$VERSION"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

show_status() {
    echo "Voice Plugin Development Mode"
    echo "=============================="
    echo ""
    echo "Source: $SOURCE_DIR"
    echo "Cache:  $CACHE_DIR"
    echo ""

    if [[ -L "$CACHE_DIR" ]]; then
        local target
        target=$(readlink -f "$CACHE_DIR")
        echo -e "Mode: ${GREEN}DEV (symlink)${NC}"
        echo "  Cache → $target"
        echo ""
        echo "Hot-reload is ACTIVE. Edit source files and changes"
        echo "take effect on the next hook invocation."
    elif [[ -d "$CACHE_DIR" ]]; then
        echo -e "Mode: ${YELLOW}STANDARD (copy)${NC}"
        echo "  Cache is a copy of source (not linked)"
        echo ""
        echo "Run './dev-mode.sh enable' for hot-reload."
    else
        echo -e "Mode: ${RED}NO CACHE${NC}"
        echo "  Cache directory doesn't exist."
        echo ""
        echo "Install the plugin first, or run 'enable' to create symlink."
    fi
}

enable_dev_mode() {
    echo "Enabling development mode..."
    echo ""

    # Backup existing cache if it's a directory (not symlink)
    if [[ -d "$CACHE_DIR" && ! -L "$CACHE_DIR" ]]; then
        local backup="${CACHE_DIR}.backup.$(date +%s)"
        echo "  Backing up existing cache → $backup"
        mv "$CACHE_DIR" "$backup"
    fi

    # Remove symlink if exists
    if [[ -L "$CACHE_DIR" ]]; then
        rm "$CACHE_DIR"
    fi

    # Create parent directory
    mkdir -p "$CACHE_BASE"

    # Create symlink
    ln -s "$SOURCE_DIR" "$CACHE_DIR"
    echo -e "  ${GREEN}Created symlink:${NC} $CACHE_DIR → $SOURCE_DIR"
    echo ""
    echo "Development mode enabled!"
    echo ""
    echo "Hot-reload is now active for:"
    echo "  - hooks/voice-hook.ts"
    echo "  - src/**/*.ts"
    echo ""
    echo "Changes take effect on next hook invocation (no restart needed)."
    echo ""
    echo "NOTE: Changes to plugin.json, skills/, commands/, agents/"
    echo "      still require Claude Code restart."
}

disable_dev_mode() {
    echo "Disabling development mode..."
    echo ""

    if [[ -L "$CACHE_DIR" ]]; then
        rm "$CACHE_DIR"
        echo "  Removed symlink"
    fi

    # Restore backup if exists
    local latest_backup
    latest_backup=$(ls -td "${CACHE_DIR}.backup."* 2>/dev/null | head -1 || true)

    if [[ -n "$latest_backup" && -d "$latest_backup" ]]; then
        mv "$latest_backup" "$CACHE_DIR"
        echo "  Restored cache from backup"
    else
        # Copy source to cache
        mkdir -p "$CACHE_DIR"
        cp -r "$SOURCE_DIR"/* "$CACHE_DIR/"
        echo "  Created fresh cache copy from source"
    fi

    echo ""
    echo -e "${YELLOW}Development mode disabled.${NC}"
    echo "Cache is now a static copy. Changes require:"
    echo "  1. /dev-tools:refresh voice"
    echo "  2. Restart Claude Code"
}

case "${1:-status}" in
    enable)
        enable_dev_mode
        ;;
    disable)
        disable_dev_mode
        ;;
    status)
        show_status
        ;;
    *)
        echo "Usage: $0 {enable|disable|status}"
        exit 1
        ;;
esac
