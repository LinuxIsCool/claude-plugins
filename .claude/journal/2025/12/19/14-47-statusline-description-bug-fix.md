---
title: "Statusline Description Generation Bug Fix"
created: 2025-12-19T14:47:00-08:00
parent_daily: "[[2025-12-19]]"
tags:
  - statusline
  - bug-fix
  - hooks
type: technical
---

# Statusline Description Generation Bug Fix

## Problem

User reported that the statusline description field was failing on all agents. Investigation revealed two separate issues:

1. **Description generation skipped**: The `check_needs_description()` function in `auto-identity.py` only checked if the description file *existed*, not its *content*
2. **Placeholder hidden instead of displayed**: The formatter was hiding "Awaiting instructions." instead of showing it

## Root Cause Analysis

### Issue 1: Race Condition Between Hooks

The `UserPromptSubmit` hook chain has two scripts:
1. `user-prompt-submit.sh` - Creates placeholder files with "Awaiting instructions."
2. `auto-identity-wrapper.sh` → `auto-identity.py` - Should generate real descriptions

The problem: `user-prompt-submit.sh` runs first and creates the file. Then `auto-identity.py` sees the file exists and skips generation entirely.

```python
# OLD CODE (bug)
def check_needs_description(instances_dir, session_id):
    desc_file = instances_dir / "descriptions" / f"{session_id}.txt"
    if desc_file.exists():  # <-- Only checks existence!
        return False
    return True
```

### Issue 2: Formatter Hiding Placeholder

The `statusline.sh` and `statusline-formatter.sh` were intentionally filtering out "Awaiting instructions." from display:

```bash
if [[ "$desc" != "Awaiting instructions." ]]; then
    line2="$desc"
fi
```

This was likely added to avoid showing the placeholder, but the user expected to see it.

## Fixes Applied

### Fix 1: Check Content, Not Just Existence

Updated `auto-identity.py` to check if the file contains the placeholder:

```python
def check_needs_description(instances_dir, session_id):
    desc_file = instances_dir / "descriptions" / f"{session_id}.txt"
    if desc_file.exists():
        content = desc_file.read_text().strip()
        if content == "Awaiting instructions." or content == "":
            return True  # Regenerate!
        return False
    return True
```

### Fix 2: Show Placeholder in White Bold

Updated both `statusline.sh` and `statusline-formatter.sh` to display "Awaiting instructions." prominently when both description and summary are placeholders:

```bash
if [ "$DESCRIPTION" = "Awaiting instructions." ] && [ "$SUMMARY" = "Awaiting instructions." ]; then
    echo -e "${BOLD}${WHITE}Awaiting instructions.${RST}"
else
    # ... show real content with pane title
fi
```

## Files Changed

| File | Change |
|------|--------|
| `plugins/statusline/hooks/auto-identity.py` | Check placeholder content, not just file existence |
| `plugins/statusline/tools/statusline.sh` | Show "Awaiting instructions." in white bold |
| `plugins/statusline/lib/statusline-formatter.sh` | Show "Awaiting instructions." in white bold |

## Verification

After the fix:
- New sessions show "Awaiting instructions." in white bold on line 2
- After first prompt, real descriptions are generated (e.g., "Statusline Alchemist", "Voice Architect")
- Pane title only appears when there's real content

## Lessons Learned

1. **Hook ordering matters**: When multiple hooks modify the same resource, the order of execution creates race conditions
2. **Check content, not existence**: File existence checks can be misleading when placeholders are involved
3. **Display vs hide decisions**: What seems like a good UX decision (hiding placeholder text) may conflict with user expectations

---

*Parent: [[2025-12-19]] → [[2025-12]] → [[2025]]*
