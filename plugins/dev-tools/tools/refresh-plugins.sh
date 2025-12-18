#!/usr/bin/env bash
# refresh-plugins.sh - Clear cache and trigger rebuild via headless Claude
#
# Usage:
#   ./refresh-plugins.sh              # Refresh all plugins
#   ./refresh-plugins.sh awareness    # Refresh specific plugin
#
# This clears the cache then runs a minimal headless Claude instance
# which triggers cache rebuild. Other running instances will see the
# fresh cache on their next plugin access.

set -euo pipefail

PLUGIN="${1:-}"
CACHE_BASE="$HOME/.claude/plugins/cache"
MARKETPLACE="linuxiscool-claude-plugins"

echo "Plugin Cache Refresh"
echo "===================="

# Step 1: Clear cache
if [[ -z "$PLUGIN" ]]; then
    echo "Clearing all plugin caches..."
    rm -rf "$CACHE_BASE/$MARKETPLACE/"
    echo "  Cleared: $CACHE_BASE/$MARKETPLACE/"
else
    echo "Clearing cache for: $PLUGIN"
    rm -rf "$CACHE_BASE/$MARKETPLACE/$PLUGIN/"
    echo "  Cleared: $CACHE_BASE/$MARKETPLACE/$PLUGIN/"
fi

# Step 2: Trigger cache rebuild via headless Claude
# The --setting-sources "" prevents recursive hook issues
echo ""
echo "Triggering cache rebuild via headless Claude..."
claude -p "exit" --setting-sources "" --output-format text 2>/dev/null || true

echo ""
echo "Done! Plugin cache has been refreshed."
echo "Other running Claude instances should see the updated plugins."
