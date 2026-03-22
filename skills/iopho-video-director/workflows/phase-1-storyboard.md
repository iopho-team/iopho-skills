# Phase 1: Storyboard & Script

> Workflow detail for `iopho-video-director` Phase 1.

## Goal

Write the video script and storyboard: narrative arc, scene-by-scene breakdown, VO script, and audio plan.

## Steps

### Step 1.1: Narrative Framework Selection

Based on video type from Phase 0:

| Video Type | Framework | Scene Count |
|-----------|-----------|-------------|
| Explainer (60-90s) | AIDA | 10-14 |
| Demo (30-60s) | Hook → Feature → CTA | 6-10 |
| Launch (60-120s) | Spectacle → Position → Value → Authority → CTA | 10-16 |
| Teaser (15-30s) | Hook → Tease → CTA | 3-5 |
| Feature Announcement | Problem → Solution → Proof → CTA | 6-8 |

### Step 1.2: Script Writing

**Skill**: `/vsl-storyboard-writer`

```
/vsl-storyboard-writer
```

Feed it: context.md + video type + duration + reference storyboards.

**Output**: VSL script with:
- Script header (type, duration, objective, framework)
- Scene-by-scene storyboard (narrative purpose, on-screen copy, VO, visual description, transitions)
- Production requirements (assets needed, copy elements, brand guidelines)

### Step 1.3: 6-Frame Narrative (Optional)

**Skill**: `/storyboard`

If the user wants a high-level narrative check BEFORE detailed scene writing:

```
/storyboard
```

Produces 6-frame problem→solution arc. Helps validate emotional journey before committing to full storyboard.

### Step 1.4: Technical Storyboard

Convert the VSL script into a production-ready `.storyboard.md`:

```yaml
---
title: "{Product} {Type} Video"
duration: "{X}s"
fps: 30
total_frames: {N}
scenes: {count}
audio: {VO + BGM + SFX | BGM only | ...}
---
```

Each scene:
```markdown
## Scene {N}: {Title} [{start_time} - {end_time}]

**Duration**: {X}s ({Y} frames)
**Visual**: {detailed description of what's on screen}
**Text Overlay**: {any text shown}
**VO**: "{voiceover line}" | NONE
**Transition**: {cut | dissolve | morph | push}
**Assets Needed**:
- [ ] {Screen recording / MG animation / stock footage / Seedance generated}
**Motion Designer Notes**: {animation style, easing, constraints}
```

### Step 1.5: VO Script

Extract all VO lines from the storyboard into a dedicated VO script:

```markdown
# VO Script: {Project}

**Voice**: {recommended voice from context.md brand tone}
**Total words**: {N} (~{X}s at 150 wpm)
**Coverage**: {Y}% of scenes

| Scene | Time | VO Text | Words | Est. Duration | Emotional Beat |
|-------|------|---------|-------|---------------|----------------|
```

Reference: `{project}/vo-script.md` for proven format.

### Step 1.6: Audio Plan

**Skill**: `/iopho-audio-director plan`

```
/iopho-audio-director plan --project-dir {dir}
```

Generates `audio-plan.md` with BGM spec, VO timing, SFX placement, duck schedule.

Includes Suno prompt for BGM generation (if using AI music).

## Checkpoint

> **Phase 1 Complete.** Deliverables:
> - VSL Script: `{project-dir}/storyboard.md` ✓
> - VO Script: `{project-dir}/vo-script.md` ✓
> - Audio Plan: `{project-dir}/audio-plan.md` ✓
>
> **Assets needed for Phase 2**: {list from storyboard}
> - Screen recordings: {N}
> - MG animations: {N}
> - AI-generated segments: {N} (Seedance)
>
> **Ready for Phase 2 (Production)?** Review the storyboard carefully — changes are cheapest now.
