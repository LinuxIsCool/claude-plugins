---
id: 2025-12-18-0754
title: "Company Plugin: Board Mentor Output Style Completion"
type: atomic
created: 2025-12-18T07:54:30
author: claude-opus-4
description: "Completed board-mentor output style with auto-install, fixed naming issues, and documented symlink propagation pattern"
tags: [plugin-development, company, output-style, hooks, patterns]
parent_daily: [[2025-12-18]]
related:
  - [[2025-12-17]]
references_date: 2025-12-17
---

# Company Plugin: Board Mentor Output Style Completion

Completed the `board-mentor` output style for the company plugin, including diagnosing and fixing activation issues and implementing auto-installation.

## Context

Continuation of yesterday's work creating the company plugin's always-on advisory persona. User attempted `/output-style board-mentor` and received "Invalid output style: board-mentor" error despite the file existing.

## Work Completed

### 1. Diagnosed Output Style Activation Issue

**Problem**: `/output-style board-mentor` failed, but the picker UI showed and selected "Board Mentor" correctly.

**Root Cause**: Claude Code matches the command argument against the **frontmatter `name` field**, not the filename.
- Filename: `board-mentor.md`
- Frontmatter: `name: Board Mentor` (with space)
- Command: `/output-style board-mentor` (no match)

**Fix**: Changed frontmatter to `name: board-mentor` to match the filename convention.

### 2. Implemented Auto-Install via SessionStart Hook

Added `ensure_output_style_installed()` function to `hooks/session-start.py`:

```python
def ensure_output_style_installed(plugin_root: Path) -> bool:
    """
    Auto-install the board-mentor output style via symlink.
    Creates ~/.claude/output-styles/board-mentor.md -> plugin source.
    """
    source = plugin_root / "output-styles" / "board-mentor.md"
    target = Path.home() / ".claude" / "output-styles" / "board-mentor.md"

    # Check if already correct symlink
    if target.is_symlink() and target.resolve() == source.resolve():
        return False

    # Create symlink (or copy as fallback)
    target.symlink_to(source)
    return True
```

**Benefits**:
- No manual installation needed
- Symlink ensures edits to plugin source propagate automatically
- Replaces stale copies with symlinks on session start

### 3. Fixed File Permissions

Source file had restrictive permissions (`600`), causing symlink read failures. Fixed to `644`.

### 4. Documented Pattern

Updated README.md with:
- Auto-install behavior documentation
- How the symlink propagation works
- Changelog entry for v0.2.0

## Key Insights

### Output Style Naming Convention
| Component | Value | Used For |
|-----------|-------|----------|
| Filename | `board-mentor.md` | File discovery |
| Frontmatter `name` | `board-mentor` | Command matching |
| Display in picker | Uses `name` field | UI display |

**Rule**: Keep frontmatter `name` aligned with filename (lowercase, hyphenated) for consistent command-line activation.

### Plugin Asset Distribution Pattern

Output styles live in `~/.claude/output-styles/` but plugins live elsewhere. Solutions:

1. **Manual install**: User creates symlink (documented but friction)
2. **Auto-install via hook**: SessionStart hook checks and creates symlink (implemented)
3. **Project-level**: Put in `.claude/output-styles/` (project-specific only)

The hook-based auto-install is the best UX - zero friction, auto-updates.

## Files Modified

| File | Change |
|------|--------|
| `plugins/company/hooks/session-start.py` | Added `ensure_output_style_installed()` |
| `plugins/company/output-styles/board-mentor.md` | Fixed `name` field |
| `~/.claude/output-styles/board-mentor.md` | Converted to symlink |
| `plugins/company/README.md` | Documented auto-install |

## Next Steps

- Test output style activation in fresh session
- Verify SessionStart hook creates symlink correctly
- Consider applying auto-install pattern to other plugins with output styles

---

*Parent: [[2025-12-18]]*
