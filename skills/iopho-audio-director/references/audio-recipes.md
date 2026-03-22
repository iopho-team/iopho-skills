# Audio Production Recipes & Reference

> For `/iopho-audio-director`. Proven values from production.

## 1. Duck Levels (Tested)

| Scenario | BGM Volume | Rationale |
|----------|-----------|-----------|
| VO speaking | **-18dB** (duck) | VO must be clearly audible over music |
| Instrumental/visual-only | **-12dB** (light duck) | Music supports visuals without dominating |
| Full music (no VO, no SFX) | **0dB** (full) | Intro/outro/transitions |
| SFX hit | **-6dB** (brief duck) | Brief dip for click/whoosh, recovers fast |
| Silent CTA | **-∞ (mute)** | Silence = confidence (proven in production) |

**Duck transition**: 200ms fade-down, 500ms fade-up (gradual return feels natural).

## 2. FFmpeg Recipes

### 2a. Duck VO over BGM (single VO track)
```bash
ffmpeg -i bgm.mp3 -i master-vo.mp3 \
  -filter_complex "
    [1]silencedetect=n=-40dB:d=0.3[silence];
    [0]volume=0.125[bgm_ducked];
    [bgm_ducked][1]amix=inputs=2:duration=first:normalize=0
  " \
  -codec:a libmp3lame -b:a 192k -ar 44100 master-audio.mp3
```

### 2b. Advanced: Sidechain duck (uses VO as trigger)
```bash
ffmpeg -i bgm.mp3 -i master-vo.mp3 \
  -filter_complex "
    [0]asplit=2[bgm1][bgm2];
    [bgm1][1]sidechaincompress=threshold=0.02:ratio=8:attack=50:release=500:level_sc=1[ducked];
    [ducked][1]amix=inputs=2:duration=first:normalize=0
  " \
  -codec:a libmp3lame -b:a 192k -ar 44100 master-audio.mp3
```

### 2c. Normalize final mix
```bash
ffmpeg -i master-audio.mp3 \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11" \
  -codec:a libmp3lame -b:a 192k master-audio-normalized.mp3
```
Target: **-16 LUFS** (YouTube standard), **-14 LUFS** (social media).

### 2d. Add SFX at specific timestamps
```bash
ffmpeg -i master-audio.mp3 -i sfx-click.wav \
  -filter_complex "
    [1]adelay=5000|5000[sfx];
    [0][sfx]amix=inputs=2:duration=first:normalize=0
  " \
  master-with-sfx.mp3
```

### 2e. Trim audio to match video length
```bash
ffmpeg -i bgm-full.mp3 -t 78.2 -af "afade=t=out:st=75:d=3.2" bgm-trimmed.mp3
```

### 2f. Analyze audio properties
```bash
ffmpeg -i audio.mp3 -af "volumedetect" -f null /dev/null 2>&1 | grep -E "mean_volume|max_volume"
```

## 3. Suno Music Prompt Template

Proven format from production. Suno AI responds best to structured prompts with timecodes.

### Template
```
[Style: {genre}, {mood}, {tempo} BPM]
[Instruments: {primary}, {secondary}, {accent}]
[Reference: {artist/track style}]

[0:00] {Opening description — energy level, key instrument}
[0:15] {Build — what changes, new elements enter}
[0:30] {Peak/development — full arrangement}
[0:45] {Variation — subtle shift for scene change}
[1:00] {Resolution — energy drops for CTA/ending}
[1:10] {Fade out / clean ending}
```

### Example: Reader App Demo BGM
```
[Style: Light electronic ambient, hopeful, 95 BPM]
[Instruments: Synth pads, soft piano, subtle percussion, warm bass]
[Reference: Similar to Notion/Linear product video music]

[0:00] Gentle synth pad, minimal — creates space for hook VO
[0:15] Soft piano enters, light hi-hat — builds anticipation
[0:30] Full but restrained — pads + bass + light percussion
[0:45] Melodic variation — new synth line, maintains energy
[1:00] Elements drop out gradually — piano + pad only
[1:10] Single sustained note, fade to silence
```

### Example: Developer Tool Launch BGM
```
[Style: Dark electronic ambient, cinematic, 95 BPM]
[Instruments: Deep synth, sub-bass, glitch percussion, atmospheric textures]
[Reference: Palantir/Superhuman product video style]

[0:00] Deep drone, single pulse — tension for terminal scene
[0:08] Sub-bass enters, glitch hits on beat — ASCII globe moment
[0:20] Full dark electronic — position statement
[0:35] Driving but controlled — value proposition scenes
[0:55] Atmospheric shift — economy/identity section
[1:10] Elements reduce — authority builds through simplicity
[1:20] Final pulse + silence — CTA
```

## 4. SFX Catalog (Lightweight)

| Category | Sound | Source | When to Use |
|----------|-------|--------|-------------|
| UI Click | Soft tap/click | Remotion built-in, freesound.org | Screen transitions, button presses |
| Whoosh | Quick swoosh L→R | freesound.org | Scene transitions, element entrances |
| Notification | Gentle chime | Web Audio API generation | Alert/notification demos |
| Type | Keyboard clatter | freesound.org | Terminal/typing scenes |
| Success | Rising arpeggio | Suno/generated | Feature reveal, "aha" moment |
| Ambient | Room tone / digital hum | Generated | Fill silence in demo scenes |

## 5. 3-Layer Audio Architecture

```
Layer 3: SFX        ┊ Spot effects at exact timestamps
                     ┊ Volume: Original (-6dB brief duck on BGM)
─────────────────────┊────────────────────────────────────
Layer 2: VOICEOVER   ┊ Master VO track (from iopho-voiceover-tts)
                     ┊ Volume: Original, triggers -18dB duck on Layer 1
─────────────────────┊────────────────────────────────────
Layer 1: BGM         ┊ Full-length music bed
                     ┊ Volume: 0dB default, ducks when L2/L3 active
```

## 6. Audio Specs by Platform

| Platform | Format | Loudness | Sample Rate | Notes |
|----------|--------|----------|-------------|-------|
| YouTube | AAC/MP3 | -14 to -16 LUFS | 44100/48000 | Normalizes loudly if too quiet |
| Product Hunt | MP3 | -16 LUFS | 44100 | Often watched without sound — VO optional |
| TikTok/Reels | AAC | -14 LUFS | 44100 | Louder is better for feed competition |
| LinkedIn | MP3/AAC | -16 LUFS | 44100 | Professional context, moderate volume |
| App Store Preview | AAC | -16 LUFS | 48000 | Apple requires 48kHz |
