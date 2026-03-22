---
name: iopho-voiceover-tts
description: >
  Generate voiceover audio for product videos using ElevenLabs, MiniMax, or Edge TTS. Handles
  multi-language VO (EN/ZH/mixed), voice audition (compare 3 voices), multi-segment assembly with
  cascade timing, and master track export. Wraps battle-tested scripts from production.
  Use when creating voiceover for a video, doing voice auditions, assembling VO segments, or
  generating TTS in any language. Triggers: "voiceover", "TTS", "generate voice", "voice audition",
  "VO assembly", "text to speech", "narration".
allowed-tools: Bash(python3), Bash(pip), Bash(ffmpeg), Bash(edge-tts)
user-invocable: true
argument-hint: "<mode: audition|generate|assemble> [--engine elevenlabs|minimax|edge] [--voice NAME] [--lang en|zh] [--output-dir DIR]"
updated: "2026-03-19"
---

# iopho-voiceover-tts

Multi-engine TTS voiceover production for video projects. Three modes: audition → generate → assemble.

## Prerequisites

```bash
# Check tools
python3 --version    # ✓ 3.10+
pip show edge-tts    # ✓ for free TTS (pip install edge-tts if missing)
ffmpeg -version      # ✓ for assembly

# Check API keys (only for paid engines)
echo $ELEVENLABS_API_KEY   # for ElevenLabs
echo $MINIMAX_API_KEY      # for MiniMax
# Edge TTS = FREE, no key needed
```

## Modes

### Mode 1: `audition` — Compare voices before committing

Generate the SAME line with 2-3 different voices so the user can listen and pick.

**Workflow**:
1. User provides a sample line (ideally the hero line from the VO script)
2. Detect language (or use `--lang`)
3. Generate with 2-3 voices from the appropriate engine(s)
4. Present files for user to listen and choose

**Engine routing for audition**:
- English → ElevenLabs (Will, Adam, Antoni) — if API key available
- English (no key) → Edge TTS (JennyNeural, GuyNeural, SoniaNeural)
- Chinese → MiniMax (Gentleman) + Edge TTS (XiaoxiaoNeural, YunxiNeural)

**Example**:
```bash
# English audition — generates 3 files
python3 scripts/generate-voiceover.py --voice will --scene hook-1a
python3 scripts/generate-voiceover.py --voice adam --scene hook-1a
python3 scripts/generate-voiceover.py --voice antoni --scene hook-1a
```

**For new projects**: Write a minimal script or use the engine API directly:

```python
# ElevenLabs one-shot
import requests
resp = requests.post(
    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
    headers={"xi-api-key": api_key, "Content-Type": "application/json"},
    json={
        "text": "Your sample line here",
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.50, "similarity_boost": 0.75, "style": 0.35}
    }
)
with open("audition-sample.mp3", "wb") as f:
    f.write(resp.content)
```

```python
# Edge TTS one-shot (FREE)
import asyncio, edge_tts
async def gen():
    tts = edge_tts.Communicate("Your sample line", "en-US-GuyNeural", rate="-5%")
    await tts.save("audition-sample.mp3")
asyncio.run(gen())
```

### Mode 2: `generate` — Produce all VO segments

Generate all voiceover segments for the project from a VO script or cue list.

**Input formats accepted**:
1. **VO script markdown** — like `{project}/vo-script.md` (scenes with text + timecodes)
2. **JSON cue file** — like `src/i18n/video-strings.json` (`{lang}.subtitles.cues[]`)
3. **Storyboard** — extract VO lines from `.storyboard.md` scene descriptions
4. **Inline text** — direct text for one-off generation

**Workflow**:
1. Read the cue source (script, JSON, or storyboard)
2. For each segment: detect language → route to engine → generate MP3
3. Rate-limit API calls (0.5s between ElevenLabs calls)
4. Report: segment name, duration, file size, cost estimate

**Output**: Individual MP3 files in `{output-dir}/voiceover/` named by segment:
```
voiceover/
├── hook-1a.mp3
├── hook-1b.mp3
├── save-1.mp3
├── read-1.mp3
├── ...
└── remember-2.mp3
```

### Mode 3: `assemble` — Build master VO track

Combine individual segments into a single master track with precise timing.

**The Cascade Algorithm** (proven in production):
```
For each segment:
  actual_start = max(previous_segment_end, intended_start)
  delay_ms = actual_start / fps * 1000
```
This ensures NO overlap and NO unintended gaps. If a segment runs long, subsequent segments cascade (shift later) rather than overlap.

**ffmpeg assembly command structure**:
```bash
ffmpeg -i seg1.mp3 -i seg2.mp3 ... -i segN.mp3 \
  -filter_complex "
    [0]adelay=D1|D1[a0];
    [1]adelay=D2|D2[a1];
    ...
    [N]adelay=DN|DN[aN];
    [a0][a1]...[aN]amix=inputs=N:normalize=0
  " \
  -codec:a libmp3lame -b:a 128k -ar 44100 master-vo.mp3
```

Key: `normalize=0` prevents amix from reducing volume.

**Output**: 
- `master-vo.mp3` — single combined track
- `master-vo-positions.json` — timeline metadata for Remotion AudioLayer integration:
```json
[{"name": "hook-1a", "intended_f": 160, "actual_f": 160, "delay_ms": 5333, "duration_s": 3.5, "end_f": 265}]
```

## Existing Scripts Reference

These scripts in `scripts/` are PROVEN in production. Adapt them for new projects:

| Script | Engine | Language | Key Config |
|--------|--------|----------|------------|
| `generate-voiceover.py` | ElevenLabs | EN | Will/Adam/Antoni, stability=0.50, style=0.35 |
| `generate-voiceover-zh.py` | ElevenLabs | ZH | Aria, stability=0.55, style=0.20 |
| `generate-voiceover-zh-edge.py` | Edge TTS | ZH | XiaoxiaoNeural, rate=-5% — **FREE** |
| `generate-voiceover-zh-minimax.py` | MiniMax | ZH | Gentleman, speech-01-hd, 32kHz |
| `assemble-master-vo.py` | ffmpeg | EN | 10 segments, cascade, 30fps |
| `assemble-master-vo-zh.py` | ffmpeg | ZH | 12 segments, cascade, 30fps |

**Adapting for new projects**: The scripts have hardcoded project-specific paths. For new projects:
1. Copy the relevant script to your project dir
2. Update `VO_DIR`, `INTENDED` array (scene names + frame offsets), and output path
3. Or use the one-shot API snippets above for simpler projects

## Voice Catalog

See [references/voice-catalog.md](references/voice-catalog.md) for:
- All voices × engines × languages with quality ratings
- Proven ElevenLabs settings from production
- Cost estimates by video length
- API key setup instructions

## Quality Checklist

- [ ] Auditioned 2+ voices before committing
- [ ] Language detection correct for each segment
- [ ] No clipping or distortion in generated audio
- [ ] Segment durations fit within intended timing windows
- [ ] Master track has no overlaps (cascade algorithm applied)
- [ ] `positions.json` frame offsets match Remotion composition
- [ ] Cost within budget (check voice-catalog.md estimates)

## Related Skills

- `/iopho-audio-director` — uses master-vo.mp3 for ducking + assembly with BGM
- `/iopho-video-director` — calls this at Phase 2 (production)
- `/iopho-product-context` — reads context.md for language preferences
- `/remotion-best-practices` — master-vo-positions.json feeds AudioLayer.tsx
