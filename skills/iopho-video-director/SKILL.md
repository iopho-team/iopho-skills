---
name: iopho-video-director
description: >
  Master orchestrator for end-to-end product video production. Guides you through a 4-phase pipeline:
  Context (research + competitor analysis) → Storyboard (script + audio plan) → Production (Remotion +
  TTS + audio assembly) → Visual QA (brand compliance + review). Routes to all other iopho skills
  with checkpoints between phases. Use when starting a new video project, continuing an existing one,
  or jumping to a specific production phase. Triggers: "new video", "product video", "launch video",
  "demo video", "video project", "start production", "video pipeline".
user-invocable: true
argument-hint: "[project-dir] [--mode new|continue|jump] [--phase 0|1|2|3]"
updated: "2026-03-19"
---

# iopho-video-director

Master orchestrator for AI-powered product video production. One command → full pipeline.

## Quick Start

```
/iopho-video-director ./exp/my-project                    # new project (default)
/iopho-video-director ./exp/my-project --mode continue     # resume from last checkpoint
/iopho-video-director ./exp/my-project --phase 2           # jump to specific phase
```

## The Pipeline

```
Phase 0: CONTEXT ──── Phase 1: STORYBOARD ──── Phase 2: PRODUCTION ──── Phase 3: VISUAL QA
  │                     │                        │                        │
  ├ product-context     ├ vsl-storyboard-writer  ├ recording-checklist    ├ Brand audit
  ├ searching-videos    ├ storyboard (6-frame)   ├ remotion-best-prac.   ├ Animation check
  ├ getting-videos      ├ audio-director plan    ├ voiceover-tts         ├ Storyboard match
  └ analyzing-videos    └ seedance-prompts       ├ audio-director asm    └ User review
                                                 └ Export + subtitles
```

## Entry Modes

### `new` (default)
Start fresh. Create project directory, initialize `project-plan.md`, begin Phase 0.

**Onboarding questions** (ask ALL before starting):
1. **What product?** — Name + URL (or describe)
2. **What kind of video?** — Demo / Explainer / Launch / Teaser / Feature / Comparison
3. **How long?** — 15s / 30s / 60s / 90s / 120s+ (or "recommend based on type")
4. **Where will it live?** — YouTube / Product Hunt / TikTok / LinkedIn / App Store / B站 / XHS
5. **Any references?** — Videos you like (URLs welcome)

Then:
- Create `{project-dir}/` if needed
- Generate `project-plan.md` from `templates/project-plan.md`
- Begin Phase 0

### `continue`
Read `{project-dir}/project-plan.md` → find last completed phase → resume next.

**Detection logic**:
```
If no project-plan.md → switch to "new" mode
If context.md missing → Phase 0 (step 0.1)
If storyboard.md missing → Phase 1
If no out/video.mp4 → Phase 2
If no QA pass noted → Phase 3
```

### `jump`
Go directly to a specific phase. Verify prerequisites:
```
Phase 1 requires: context.md
Phase 2 requires: context.md + storyboard.md + audio-plan.md
Phase 3 requires: out/video.mp4
```
If prereqs missing, warn user and offer to run prerequisite phase first.

## Phase Details

### Phase 0: Context Gathering

See [workflows/phase-0-context.md](workflows/phase-0-context.md) for full workflow.

**Skills called**: `iopho-product-context` → `iopho-searching-videos` → `iopho-getting-videos` → `iopho-analyzing-videos`

**Outputs**: `context.md`, `research/storyboards/*.storyboard.md`, `research/pattern-analysis.md`

**Checkpoint**: Show context summary + reference analysis → user approves → Phase 1.

### Phase 1: Storyboard & Script

See [workflows/phase-1-storyboard.md](workflows/phase-1-storyboard.md) for full workflow.

**Skills called**: `vsl-storyboard-writer` → `storyboard` (optional) → `iopho-audio-director plan`

**Outputs**: `storyboard.md`, `vo-script.md`, `audio-plan.md`

**Checkpoint**: Show storyboard + asset list → user reviews → Phase 2.
> "Changes are cheapest at storyboard phase. Review carefully."

### Phase 2: Production

See [workflows/phase-2-production.md](workflows/phase-2-production.md) for full workflow.

**Skills called**: `iopho-recording-checklist` → `remotion-best-practices` → `iopho-voiceover-tts` → `iopho-audio-director assemble` → `iopho-seedance-prompts` (if needed)

**Outputs**: `out/video.mp4`, `out/*.srt`, `audio/master-audio.mp3`

**Checkpoint**: Video rendered → user watches → Phase 3.

### Phase 3: Visual QA

Brand compliance and quality review. No separate workflow file — it's short enough to live here.

**Step 3.1: Brand Compliance Audit**

Read `context.md` brand section. Check rendered video against:
- [ ] Colors match hex values from brand guidelines
- [ ] Fonts match specified typefaces
- [ ] Logo usage follows guidelines (if applicable)
- [ ] Tone matches brand voice (authoritative? playful? professional?)

Auto-detect: Look for `*DesignPrompts*`, `brand.ts`, or brand section in README.

**Step 3.2: Animation Restraint Check**

Common AI over-animation patterns to catch:
- [ ] Excessive zoom/pan on static screens (should be subtle or none)
- [ ] Too many simultaneous animations (one focal animation per scene)
- [ ] Transition effects that distract from content
- [ ] Text animations that are too fast to read
- [ ] Motion that doesn't serve the narrative

**Step 3.3: Storyboard Conformance**

Side-by-side review:
- Does each rendered scene match the storyboard intent?
- Are VO lines synced to correct visuals?
- Does the emotional arc play as planned?
- Is the CTA clear and prominent?

**Step 3.4: Platform-Specific Check**
| Platform | Check |
|----------|-------|
| YouTube | Thumbnail-worthy first frame? End screen space? |
| Product Hunt | Auto-play friendly? Works without sound? |
| TikTok/Reels | Vertical crop preserves key content? |
| LinkedIn | Professional tone? Subtitles visible? |
| App Store | Within 30s limit? Shows real app UI? |

**Checkpoint**:
> QA passed. Final deliverables ready for upload/distribution.

If issues found → iterate (re-render specific scenes) → re-check.

## Project Structure

A typical project directory after full pipeline:
```
{project-dir}/
├── project-plan.md          ← phase tracker + decision log
├── context.md               ← product/brand/audience context
├── storyboard.md            ← scene-by-scene breakdown
├── vo-script.md             ← VO lines + timecodes
├── audio-plan.md            ← BGM + VO + SFX strategy
├── recording-checklist.md   ← shot list for screen recording
├── research/
│   ├── storyboards/         ← reference .storyboard.md files
│   ├── downloads/           ← downloaded reference videos
│   └── pattern-analysis.md  ← cross-reference insights
├── public/
│   ├── videos/              ← raw screen recordings
│   ├── voiceover/           ← VO segments + master-vo.mp3
│   ├── audio/               ← BGM + master-audio.mp3
│   └── fonts/
├── src/                     ← Remotion source (if applicable)
└── out/
    ├── video.mp4            ← final render
    ├── video-vertical.mp4   ← 9:16 cut (if needed)
    ├── video.srt            ← subtitles
    └── video.vtt            ← web subtitles
```

## Skill Ecosystem Map

| Skill | Phase | Purpose |
|-------|-------|---------|
| `iopho-product-context` | 0 | Intake questionnaire → context.md |
| `iopho-searching-videos` | 0 | Cross-platform video search |
| `iopho-getting-videos` | 0 | Download video/audio/subtitles |
| `iopho-analyzing-videos` | 0 | Reverse-engineer → .storyboard.md |
| `vsl-storyboard-writer` | 1 | VSL/marketing script writing |
| `storyboard` | 1 | 6-frame emotional narrative arc |
| `iopho-seedance-prompts` | 1-2 | Seedance AI video generation |
| `iopho-audio-director` | 1-2 | Audio planning + assembly |
| `iopho-voiceover-tts` | 2 | Multi-engine TTS + assembly |
| `iopho-recording-checklist` | 2 | Screen recording shot list |
| `remotion-best-practices` | 2 | Remotion implementation rules |
| `suno-music-creator` | 2 | BGM generation (external) |

## Related Skills

All skills listed in the Ecosystem Map above. The director orchestrates; it does not replace.
