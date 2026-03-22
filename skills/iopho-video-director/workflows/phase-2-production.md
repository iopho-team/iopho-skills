# Phase 2: Production

> Workflow detail for `iopho-video-director` Phase 2.

## Goal

Produce all assets and assemble the final video: recordings, Remotion code, voiceover, BGM, assembly, subtitles, export.

## Steps

### Step 2.1: Recording Checklist

**Skill**: `/iopho-recording-checklist`

```
/iopho-recording-checklist {project-dir}
```

Generates `recording-checklist.md` from storyboard with:
- Shot-by-shot instructions (what to record, at what resolution, what app state)
- Device setup (terminal font size, browser zoom, dark/light mode)
- Pre-recording prep (test data, feature flags, demo accounts)

User goes and records all screen captures. Returns with raw footage.

### Step 2.2: Remotion Setup

**Skill**: `/remotion-best-practices`

Set up the Remotion project structure:
```
{project-dir}/
├── package.json
├── remotion.config.ts
├── tsconfig.json
├── public/
│   ├── videos/          ← raw screen recordings
│   ├── voiceover/       ← VO files (from Step 2.4)
│   ├── audio/           ← BGM + master audio (from Step 2.5)
│   └── fonts/
└── src/
    ├── Root.tsx          ← registers compositions
    ├── index.ts          ← Remotion entry
    ├── brand.ts          ← colors, fonts, brand constants
    ├── components/
    │   ├── AudioLayer.tsx     ← 3-layer audio integration
    │   ├── SubtitleLayer.tsx  ← caption overlay
    │   └── DeviceFrame.tsx    ← device mockup wrapper
    └── scenes/
        ├── Scene01-Hook.tsx
        ├── Scene02-Problem.tsx
        └── ...
```

Each scene component: `useCurrentFrame()` + `interpolate()` for all animations.
**FORBIDDEN**: CSS transitions, Tailwind animation classes, requestAnimationFrame.

### Step 2.3: AI Video Segments (if needed)

**Skill**: `/iopho-seedance-prompts`

For scenes that need AI-generated video (transitions, abstract visuals, product concepts):
```
/iopho-seedance-prompts {scene description}
```

### Step 2.4: Voiceover Production

**Skill**: `/iopho-voiceover-tts`

```
/iopho-voiceover-tts audition --lang {lang}    # Step 1: Pick voice
/iopho-voiceover-tts generate --output-dir {project}/public/voiceover/  # Step 2: All segments
/iopho-voiceover-tts assemble --output-dir {project}/public/voiceover/  # Step 3: Master track
```

**Output**: `master-vo.mp3` + `master-vo-positions.json`

### Step 2.5: Audio Assembly

**Skill**: `/iopho-audio-director assemble`

```
/iopho-audio-director assemble \
  --bgm {project}/public/audio/bgm.mp3 \
  --vo {project}/public/voiceover/master-vo.mp3 \
  --duration {total_seconds}
```

BGM source options:
1. **Suno AI**: Use prompt from audio-plan.md → `/suno-music-creator` → download → trim
2. **Artlist/Epidemic Sound**: Licensed track → trim to length
3. **Custom**: Compose or commission

**Output**: `master-audio.mp3` (ducked, normalized), `master-audio-loud.mp3` (social media version)

### Step 2.6: Remotion Integration

Wire audio into Remotion:
1. Import `master-vo-positions.json` into `AudioLayer.tsx`
2. Set `<Audio src={masterAudio} />` at composition level
3. Sync SubtitleLayer with VO positions (frame-accurate captions)
4. Preview in Remotion Studio: `npx remotion studio`

### Step 2.7: Subtitles & Captions

Generate subtitle files from VO positions:
- `.srt` file for YouTube upload
- `.vtt` file for web embedding
- Burn-in CC option: `scripts/build-cc.sh` (ffmpeg subtitle overlay)

For multi-language: generate separate VO + subtitles per language.

### Step 2.8: Export

```bash
# Remotion render
npx remotion render src/index.ts {CompositionId} out/video.mp4

# Add burned-in subtitles (optional)
bash scripts/build-cc.sh

# Multi-format export
ffmpeg -i out/video.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:-1:-1" out/video-vertical.mp4  # 9:16
ffmpeg -i out/video.mp4 -t 30 -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:-1:-1" out/video-square.mp4  # 1:1
```

## Checkpoint

> **Phase 2 Complete.** Deliverables:
> - Final video: `out/video.mp4` ✓
> - Vertical cut: `out/video-vertical.mp4` (if platforms include TikTok/Reels)
> - Subtitles: `.srt` + `.vtt` ✓
> - Master audio: `audio/master-audio.mp3` ✓
>
> **Ready for Phase 3 (Visual QA)?** Watch the full video before proceeding.
