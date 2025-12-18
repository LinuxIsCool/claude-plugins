---
name: transcripts
description: Manage transcripts - transcribe, list, search, and work with speakers
allowed-tools: Read, Glob, Grep, Bash, Skill, Task
---

# /transcripts Command

## Usage

```
/transcripts [action] [options]
```

## Actions

### transcribe <file>
Transcribe an audio or video file.

```
/transcripts transcribe /path/to/recording.mp3
/transcripts transcribe ~/Downloads/meeting.wav --model large-v3
```

### list
List all transcripts.

```
/transcripts list
/transcripts list --status complete
/transcripts list --speaker "Alice Chen"
```

### get <id>
View a specific transcript.

```
/transcripts get tx_abc123...
```

### search <query>
Search across transcripts.

```
/transcripts search "quarterly budget"
/transcripts search "machine learning" --speaker "John"
```

### speakers
Manage speaker database.

```
/transcripts speakers                    # List all speakers
/transcripts speakers create "Alice Chen"
/transcripts speakers get spk_abc123
/transcripts speakers link spk_abc123 messages:alice_chen
```

### stats
Show transcript statistics.

```
/transcripts stats
```

### emit <id>
Emit transcript to messages plugin.

```
/transcripts emit tx_abc123...
```

## Implementation

When the user runs `/transcripts`, invoke the transcript-master skill and use the appropriate MCP tools.

### For transcription:
1. Read the transcription sub-skill: `plugins/transcripts/skills/transcript-master/subskills/transcription.md`
2. Use `transcripts_transcribe` MCP tool
3. Report progress and results

### For speaker management:
1. Read the speaker-database sub-skill
2. Use `transcripts_speakers_list`, `transcripts_speaker_create`, `transcripts_speaker_get` MCP tools

### For entity analysis:
1. Spawn the `transcripts:analyst` agent for deep analysis
2. Or read entity-extraction sub-skill for quick extraction

### For messages integration:
1. Read messages-integration sub-skill
2. Use `transcripts_emit_to_messages` MCP tool

## Examples

### Quick transcription
```
/transcripts transcribe ~/recording.mp3
```

### Full analysis pipeline
```
/transcripts transcribe ~/meeting.mp4 --analyze
```
This runs transcription + speaker identification + entity extraction.

### Find what someone said
```
/transcripts search "budget concerns" --speaker "CFO"
```

### Export to messages
```
/transcripts emit tx_abc123 --link-speakers
```
