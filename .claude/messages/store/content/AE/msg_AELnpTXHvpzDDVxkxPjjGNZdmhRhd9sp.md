---
id: msg_AELnpTXHvpzDDVxkxPjjGNZdmhRhd9sp
kind: 103
account_id: claude
created_at: 1765929008783
imported_at: 1766005511844
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

The statusline **already receives the model**. Look at line 29:

```bash
MODEL=$(echo "$input" | jq -r '.model.display_name // "Claude"')
```

Claude Code sends `.model.display_name` to the statusline script. But currently it's only used as a fallback name (line 76), not displayed explicitly.

## Two Issues, One Solution

1. **Statusline doesn't show model** — It has the data but doesn't display it
2. **Registry doesn't have model** — session-start hook doesn't get it, but statusline does

The statusline runs continuously while Claude is active. It could:
1. Display the model in output
2. Update the registry with model info (since it has both session_id and model)

## Proposed Changes

**statusline.sh** — Show model and backfill registry:

```bash
# Current format:  [Phoenix:e05da] claude | ctx:5% | $0.42
# New format:      [Phoenix:e05da] Opus | claude | ctx:5% | $0.42
```

And add registry update logic:
```bash
# Backfill model to registry if missing
if [ -n "$REGISTRY" ] && [ -n "$SESSION_ID" ]; then
    STORED_MODEL=$(jq -r --arg sid "$SESSION_ID" '.[$sid].model // empty' "$REGISTRY" 2>/dev/null)
    if [ -z "$STORED_MODEL" ] && [ -n "$MODEL" ]; then
        jq --arg sid "$SESSION_ID" --arg model "$MODEL" \
           '.[$sid].model = $model' "$REGISTRY" > "$REGISTRY.tmp" && \
           mv "$REGISTRY.tmp" "$REGISTRY"
    fi
fi
```

Want me to implement this?
