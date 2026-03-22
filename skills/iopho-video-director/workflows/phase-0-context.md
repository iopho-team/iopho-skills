# Phase 0: Context Gathering

> Workflow detail for `iopho-video-director` Phase 0.

## Goal

Build complete project context: understand the product, research competitors, collect reference videos, analyze them into storyboards.

## Steps

### Step 0.1: Product Context

**Skill**: `/iopho-product-context`

```
/iopho-product-context {project-dir} [--quick] [--from-file README.md]
```

**If context.md already exists**: Read it, show summary, ask if updates needed.
**If no context.md**: Run full intake questionnaire.

**Output**: `{project-dir}/context.md`

### Step 0.2: Video Type Selection

Read `doc/saas-video-types-taxonomy.md` for the full taxonomy. Based on context.md, recommend 1-3 video types:

| Context Signal | Recommended Type | Duration |
|---------------|-----------------|----------|
| Pre-launch, need awareness | Teaser | 15-30s |
| Beta/launched, need signups | Explainer / Demo | 60-90s |
| Major feature release | Feature Announcement | 30-60s |
| Product Hunt / launch day | Launch Video | 60-120s |
| Competitive market | Comparison | 60-90s |
| App Store listing | App Preview | 15-30s |

Present options → user picks → record in project-plan.md.

**Multi-video strategy**: If the product needs 2+ videos, propose a content matrix showing shared assets:
```
90s YouTube Explainer ──┬──► 30s TikTok cut (scenes 3-7 only)
                        ├──► 15s App Store preview (hero feature only)
                        └──► 6s GIF (single "aha" moment)
```

### Step 0.3: Competitor Research

**Skill**: `/iopho-searching-videos`

```
/iopho-searching-videos "{product-category} product demo" --platform youtube --limit 10
/iopho-searching-videos "{competitor-name} launch video" --platform youtube --limit 5
```

Collect 5-10 reference URLs. Present to user for selection of top 3-5 to analyze.

### Step 0.4: Download References

**Skill**: `/iopho-getting-videos`

```
/iopho-getting-videos {url} --mode all --output {project-dir}/research/downloads/
```

Download selected references with metadata.

### Step 0.5: Analyze References

**Skill**: `/iopho-analyzing-videos`

```
/iopho-analyzing-videos {video-path} {project-dir}/research/storyboards/{name}.storyboard.md
```

Reverse-engineer each reference into `.storyboard.md` format. This gives:
- Scene-by-scene breakdown with timecodes
- Visual descriptions, text overlays, transitions
- Audio analysis (music style, VO approach, SFX)
- Keyframe screenshots in `frames/`

### Step 0.6: Pattern Synthesis

After analyzing 3+ references, synthesize patterns:
- Average scene count and duration
- Common narrative structures (problem→solution? tutorial? emotional?)
- Color palettes and visual styles
- Audio approaches (VO-heavy? music-only? SFX-rich?)
- What works well vs. what to avoid

Write findings to `{project-dir}/research/pattern-analysis.md`.

## Checkpoint

> **Phase 0 Complete.** Here's what we have:
> - Product context: `context.md` ✓
> - Video type: {type} ({duration})
> - References analyzed: {N} storyboards
> - Key patterns: {1-3 sentence summary}
>
> **Ready for Phase 1 (Storyboard)?** Or do you want to adjust anything?
