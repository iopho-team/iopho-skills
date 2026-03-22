---
name: iopho-audio-director
description: >
  Plan and assemble the complete audio layer for product videos — BGM selection/generation,
  voiceover assembly with ducking, SFX placement, and master audio export. Two modes: PLAN
  (generate audio-plan.md strategy) and ASSEMBLE (execute with FFmpeg). Includes Suno AI music
  prompt templates with timecodes and proven duck levels. Use when planning audio strategy for a
  video, generating BGM prompts, mixing voiceover with music, adding sound effects, or exporting
  final audio. Triggers: "audio plan", "BGM", "music", "ducking", "audio mix", "sound design",
  "Suno prompt", "master audio", "audio assembly".
allowed-tools: Bash(ffmpeg), Bash(python3), Bash(pip)
user-invocable: true
argument-hint: "<mode: plan|assemble|analyze> [--project-dir DIR] [--bgm FILE] [--vo FILE] [--duration SEC]"
updated: "2026-03-19"
---

# iopho-audio-director

Plan and produce the complete audio layer for product videos: BGM + VO + SFX → master audio.

## Modes

### Mode 1: `plan` — Generate audio strategy

Read the project's storyboard and context, then output an `audio-plan.md` with:

**1. Architecture Decision**
```
Total duration: {X}s @ {fps}fps = {frames} frames
VO coverage: {Y}% of scenes have voiceover
BGM strategy: {continuous bed | scene-matched segments | minimal/ambient}
SFX density: {minimal | moderate | rich}
```

**2. BGM Specification**
- Genre, BPM, mood, instrument palette
- Suno prompt (use template from [references/audio-recipes.md](references/audio-recipes.md) §3)
- Scene-by-scene music energy map:
  ```
  Scene 1 (0:00-0:08): Low energy — ambient pad, space for hook
  Scene 2 (0:08-0:15): Rising — add percussion, build
  Scene 3 (0:15-0:30): Peak — full arrangement for demo
  ...
  ```

**3. VO Timing Table**
| Scene | Start (s) | Start (f) | VO Text | Est. Duration | Engine |
|-------|----------|----------|---------|---------------|--------|
| hook-1a | 5.3 | 160 | "..." | 3.5s | ElevenLabs |

**4. SFX Placement**
| Timestamp | SFX | Trigger | Duration |
|-----------|-----|---------|----------|
| 0:05 | UI click | Button press in demo | 0.3s |

**5. Duck Schedule**
| Time Range | BGM Level | Reason |
|-----------|-----------|--------|
| 0:00-0:05 | 0dB | Music-only intro |
| 0:05-0:09 | -18dB | VO speaking |
| 0:09-0:12 | -12dB | Instrumental visual |

### Mode 2: `assemble` — Execute the audio plan

Takes individual audio files and combines them into the master audio track.

**Inputs needed**:
- `bgm.mp3` — background music (trimmed to video length)
- `master-vo.mp3` — assembled voiceover (from `/iopho-voiceover-tts assemble`)
- SFX files (if any) — with target timestamps

**Assembly sequence**:
1. **Trim BGM** to video length with fade-out:
   ```bash
   ffmpeg -i bgm-full.mp3 -t {duration} -af "afade=t=out:st={duration-3}:d=3" bgm.mp3
   ```

2. **Duck BGM under VO** (sidechain compress):
   See [references/audio-recipes.md](references/audio-recipes.md) §2b for the ffmpeg command.

3. **Layer SFX** at timestamps:
   See [references/audio-recipes.md](references/audio-recipes.md) §2d for adelay placement.

4. **Normalize** to platform target:
   - YouTube: -16 LUFS
   - Social media: -14 LUFS
   See [references/audio-recipes.md](references/audio-recipes.md) §2c.

5. **Export** master audio:
   ```
   {project}/audio/master-audio.mp3       — final mix
   {project}/audio/master-audio-loud.mp3  — social media version (-14 LUFS)
   ```

### Mode 3: `analyze` — Inspect existing audio

Run `scripts/analyze_audio.py` on any audio file to get:
- BPM (global + dynamic), beats, onsets
- Energy envelope, key moments
- Structural sections

```bash
python3 scripts/analyze_audio.py path/to/audio.mp3 --output analysis.json
python3 scripts/analyze_audio.py path/to/audio.mp3 --gemini  # optional AI analysis
```

Use analysis output to:
- Match BGM tempo to scene cuts
- Verify duck timing aligns with VO segments
- Find beat-sync points for MG animations

## Decision Guide

| Question | Answer | Action |
|----------|--------|--------|
| Have a storyboard? | Yes | Start with `plan` mode |
| Have a storyboard? | No | Run `/iopho-video-director` Phase 1 first |
| Need BGM? | Generate new | Use Suno prompt template from recipes §3 |
| Need BGM? | Have a track | Skip to `assemble` mode |
| Need VO? | Yes | Run `/iopho-voiceover-tts` first, then `assemble` |
| Need VO? | No (music video / MG) | Simpler: just trim + normalize BGM |
| Platform? | YouTube | Target -16 LUFS |
| Platform? | TikTok/Reels | Target -14 LUFS (louder) |

## Proven Values

These settings are battle-tested in production (78s explainer, 10 VO segments):

| Parameter | Value | Source |
|-----------|-------|--------|
| VO duck level | -18dB | {project}-audio-plan.md |
| Instrumental duck | -12dB | {project}-audio-plan.md |
| Duck fade-down | 200ms | tested in ffmpeg |
| Duck fade-up | 500ms | tested in ffmpeg |
| VO rate-limit (ElevenLabs) | 0.5s between calls | API throttle |
| MP3 bitrate | 128-192kbps | balance quality/size |
| Sample rate | 44100Hz | standard (48kHz for App Store) |
| FPS constant | 30 | project-wide |

## Audio Recipes Reference

See [references/audio-recipes.md](references/audio-recipes.md) for:
- §1: Duck levels table (full reference)
- §2: FFmpeg commands (duck, sidechain, normalize, SFX, trim, analyze)
- §3: Suno music prompt templates with examples (reader app + CLI tool)
- §4: SFX catalog
- §5: 3-layer architecture diagram
- §6: Platform-specific audio specs

## Related Skills

- `/iopho-voiceover-tts` — produces master-vo.mp3 that this skill ducks under BGM
- `/iopho-video-director` — calls this at Phase 1 (plan) and Phase 2 (assemble)
- `/suno-music-creator` — generates BGM from Suno prompts (external skill)
- `/remotion-best-practices` → `rules/audio.md` — integrates master-audio into Remotion
- `/iopho-product-context` — reads context.md for brand tone → influences BGM mood
