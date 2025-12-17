---
id: msg_CHfWnTamz12kPGJSkrcjgfRvSTdB9BFM
kind: 103
account_id: claude
created_at: 1765928926741
imported_at: 1766005511832
author_name: Claude
thread_id: cc_e05dab22
platform: claude-code
session_id: e05dab22-0e00-4995-bf56-e7657c004d36
tags: [["event_type","AssistantResponse"]]
---

The model is blank because **Claude Code doesn't pass model info to hooks**.

Looking at the hook (`session-start.sh:17-19`), it receives:
```json
{
  "session_id": "...",
  "cwd": "/path/to/dir",
  "source": "startup|resume|clear|compact"
}
```

No `model` field exists in the hook payload. Line 72 sets `"model": ""` as a placeholder.

## The Gap

The hook runs *before* Claude is active, so it can't know the model. And when Claude names itself later:

```bash
python3 registry.py register "$SESSION_ID" "Phoenix" --task "..."
```

The `--model` flag exists but isn't being used.

## Fix Options

1. **Self-detection** — I know I'm `claude-opus-4-5-20251101`. I can update my entry:
   ```bash
   python3 registry.py register "$SESSION_ID" "Phoenix" --task "..." --model "opus-4.5"
   ```

2. **Prompt the instance** — Update the hook's prompt to remind instances to include model

3. **Feature request** — Ask Anthropic to include model in hook payloads

Want me to update my registry entry with the correct model, and improve the self-naming prompt to include model going forward?
