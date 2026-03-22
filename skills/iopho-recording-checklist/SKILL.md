---
name: iopho-recording-checklist
description: >
  Generate a per-project screen recording checklist from a storyboard. Produces a shot-by-shot guide
  with device specs, resolution, app state, action steps, and timing. Reads the project storyboard
  and context to create a production-ready recording plan. Use when preparing to record screen
  captures for a product video, onboarding a recording team, or planning demo footage. Triggers:
  "recording checklist", "screen recording", "shot list", "what to record", "recording guide",
  "capture plan", "demo recording".
user-invocable: true
argument-hint: "[project-dir] [--storyboard FILE] [--format checklist|table]"
updated: "2026-03-19"
---

# iopho-recording-checklist

Generate a shot-by-shot screen recording guide from a video storyboard.

## When to Use

- Before recording screen captures for a product video
- When handing off recording tasks to a team member or designer
- When the storyboard is final and you need to plan capture sessions

## Input

Reads from the project directory:
1. **Storyboard** — `storyboard.md` or any `.storyboard.md` (scene descriptions, durations, visuals)
2. **Context** — `context.md` (brand, product info, platform specs)
3. **Audio Plan** — `audio-plan.md` (to know which scenes have VO → affects recording approach)

## How It Works

### Step 1: Parse Storyboard

Read the storyboard and extract every scene that requires recorded footage:

| Scene Type | Needs Recording? | Example |
|-----------|-----------------|---------|
| Screen demo | **YES** | "User opens app, taps Save" |
| Terminal demo | **YES** | "npx install sequence" |
| MG animation | NO (Remotion/After Effects) | "Logo animation" |
| AI-generated | NO (Seedance) | "Abstract transition" |
| Text overlay | NO (Remotion) | "Title card" |
| Stock footage | NO (library) | "People working" |

### Step 2: Determine Specs

For each recording, determine technical specs from context:

**Desktop recordings**:
- Resolution: Retina display → record at 2× then downscale, OR match target (1920×1080)
- FPS: 30fps (standard) or 60fps (if showing smooth scrolling/animations)
- Browser zoom: 125-150% if content is small on high-DPI
- Terminal: Specific font + size for readability (some projects require specific terminal aesthetics)

**Mobile recordings**:
- Use device screen recording (iOS/Android) or simulator
- Resolution: Native device resolution
- Frame: May need device mockup frame in Remotion (DeviceFrame component)

**Tablet recordings**:
- Landscape for productivity apps, portrait for reading apps

### Step 3: Define App State

For EACH recording, specify the exact state the app should be in:

- What screen/page to start on
- What data should be visible (real or demo data)
- What user account to use
- Any feature flags or settings to enable
- Theme: dark/light (from brand guidelines)

This prevents wasted recordings from wrong app state.

### Step 4: Generate Checklist

Output `recording-checklist.md` using template at `templates/checklist-template.md`.

Each shot entry includes:
- Scene reference (number + title from storyboard)
- Duration (recording time = storyboard time + 5s margin for trimming)
- Resolution + FPS
- Device type
- Detailed action steps (what to click, type, scroll)
- The key moment (the specific thing the viewer needs to see)
- Special notes (cursor position, scroll speed, timing)

### Step 5: Recording Tool Recommendations

| OS | Free Tool | Pro Tool | Notes |
|----|-----------|----------|-------|
| macOS | QuickTime Player | CleanShot X ($29) | CleanShot = cursor highlighting, auto-trim |
| macOS | | ScreenFlow ($169) | Best for multi-source + editing |
| Windows | OBS Studio | Camtasia ($313) | OBS = free + powerful |
| Linux | OBS Studio | SimpleScreenRecorder | |
| iOS | Built-in Screen Recording | | Settings → Control Center → Screen Recording |
| Android | Built-in Screen Recording | AZ Screen Recorder | |

## Output Example

For a CLI tool project (e.g., `exp/{project}/`), the checklist would have:

```markdown
### Shot 1: Terminal Install (Scene 2)
| Field | Value |
|-------|-------|
| Duration | 8s (record 13s) |
| Resolution | 1920×1080 |
| Device | Desktop terminal |
| App state | Clean terminal, dark theme, ~14pt mono font |
| Action | Type "npx {tool}" → watch install scroll → "{N} peers connected" |
| Key moment | The peer count appearing after install completes |
| Notes | Type at natural speed, not too fast. Pause 1s after completion. |

### Shot 2: ASCII Globe (Scene 3)
| Field | Value |
|-------|-------|
| Duration | 7s (record 12s) |
| Resolution | 1920×1080 |
| Device | Desktop terminal |
| App state | {CLI tool} running, main command ready |
| Action | Run globe command → watch nodes light up → slow rotation |
| Key moment | The globe fully populated with node indicators |
| Notes | HERO SHOT — ensure terminal fills entire screen |
```

## Tips

- **Record longer than needed** — trimming is easier than re-recording
- **Multiple takes** — record each shot 2-3 times, pick the best
- **Cursor discipline** — move cursor deliberately, no jittery movements
- **Clean desktop** — hide all non-relevant windows, notifications OFF
- **Consistent mouse speed** — match the energy of the video (calm video = slow cursor)
- **Demo data quality** — no "test123", no "lorem ipsum", no empty states unless intentional

## Related Skills

- `/iopho-video-director` — calls this at Phase 2, Step 2.1
- `/vsl-storyboard-writer` — produces the storyboard this skill reads
- `/iopho-product-context` — provides brand/device context
- `/remotion-best-practices` — recordings feed into Remotion compositions
