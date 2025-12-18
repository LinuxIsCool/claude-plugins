#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Stale plugin cache detection.

SessionStart hook that compares plugin source mtimes against cached versions.
Warns if any caches are out of date so you know to restart.
"""

import json
import os
import sys
from pathlib import Path


def get_plugin_cache_dir() -> Path:
    """Get the Claude Code plugin cache directory."""
    return Path.home() / ".claude" / "plugins" / "cache"


def get_local_plugins_dir() -> Path:
    """Get the local plugins directory."""
    cwd = os.environ.get('CWD', os.getcwd())
    return Path(cwd) / "plugins"


def get_newest_mtime(directory: Path) -> float:
    """Get the newest modification time of any file in a directory tree."""
    newest = 0.0
    try:
        for f in directory.rglob('*'):
            if f.is_file():
                mtime = f.stat().st_mtime
                if mtime > newest:
                    newest = mtime
    except Exception:
        pass
    return newest


def check_for_stale_caches() -> list[str]:
    """Check for plugins where source is newer than cache."""
    stale = []

    plugins_dir = get_local_plugins_dir()
    cache_base = get_plugin_cache_dir()

    if not plugins_dir.exists() or not cache_base.exists():
        return []

    # Check each local plugin
    for plugin_dir in plugins_dir.iterdir():
        if not plugin_dir.is_dir():
            continue

        plugin_name = plugin_dir.name
        source_mtime = get_newest_mtime(plugin_dir)

        if source_mtime == 0:
            continue

        # Check all cache sources for this plugin
        for source_dir in cache_base.iterdir():
            if source_dir.is_dir():
                plugin_cache = source_dir / plugin_name
                if plugin_cache.exists():
                    cache_mtime = get_newest_mtime(plugin_cache)
                    if source_mtime > cache_mtime:
                        stale.append(plugin_name)
                        break

    return stale


def main():
    """SessionStart hook entry point."""
    # Read stdin (required by hook protocol) but we don't need it
    try:
        sys.stdin.read()
    except:
        pass

    stale = check_for_stale_caches()

    if stale:
        plugins_list = ', '.join(stale)
        if len(stale) == 1:
            cmd_hint = f"Run: /dev-tools:reload {stale[0]}"
        else:
            cmd_hint = "Run: /dev-tools:reload all"
        print(f"Stale plugin cache detected: {plugins_list}. {cmd_hint} then restart Claude Code.")


if __name__ == "__main__":
    main()
