---
name: iopho-product-context
description: >
  Generate structured product context files for video production projects. Runs an interactive intake
  questionnaire (or auto-detects from existing docs), outputs a context.md that all other iopho skills
  read. Use when starting a new video project, onboarding a client, or when any iopho skill needs
  product/audience/brand information. Triggers: "product context", "video project setup", "new project",
  "context file", "onboarding questionnaire", "client intake".
user-invocable: true
argument-hint: "[project-dir] [--quick] [--from-file README.md] [--lang en|zh|mixed]"
updated: "2026-03-19"
---

# iopho-product-context

Generate structured `context.md` for video production — the foundation file all other iopho skills read.

## When to Use

- Starting a new video project (product demo, launch video, explainer, VSL)
- Onboarding a client project (like a client project)
- Any iopho skill asks for context but none exists yet
- Updating an existing context file with new information

## Quick Start

```
/iopho-product-context ./exp/my-project
/iopho-product-context ./exp/my-project --quick           # 5 core questions only
/iopho-product-context ./exp/my-project --from-file README.md  # pre-fill from docs
```

## How It Works

### Mode 1: Interactive (default)

Ask the user these questions IN ORDER. Accept answers in any language (CN/EN/mixed).

**Core Questions (always ask)**:

1. **What's the product?** — Name, URL, one-sentence description
2. **Who is it for?** — Primary audience + their pain point
3. **What makes it different?** — Top 3 differentiators from competitors
4. **What video do you want?** — Type (demo/explainer/launch/teaser), duration, platforms
5. **Any brand rules?** — Colors, fonts, tone of voice, design system files

**Deep-Dive Questions (ask unless `--quick`)**:

6. **Who are the competitors?** — List 2-5 competitors, their strengths/weaknesses
7. **Founder visibility?** — Should founders/team appear? (public / anonymous / team-only)
8. **Hero feature?** — The ONE feature that must be the centerpiece of the video
9. **What to avoid?** — Anything off-limits (features, messaging, visuals)
10. **Reference videos?** — Any video styles they like (provide URLs → feed to iopho-searching-videos)
11. **Languages?** — Which languages for VO and subtitles
12. **Call to action?** — What should viewers do after watching

### Mode 2: Auto-Detect (`--from-file`)

Before asking questions, scan the project directory for existing context:

```
Look for and read (if present):
├── README.md              → product name, description, features
├── package.json           → name, description, keywords
├── **/brand.ts            → colors, fonts (Remotion projects)
├── **/*DesignPrompts*     → design system (client project pattern)
├── **/questionaire.md     → existing intake (client project pattern)
├── **/context.md          → previous context file (update mode)
└── website URL            → scrape tagline, features, pricing (if provided)
```

Pre-fill answers from detected files, then ask user to CONFIRM or CORRECT each field. Skip questions already answered by auto-detection.

### Mode 3: Update

If `context.md` already exists in the project directory, read it and ask:
> "Found existing context.md. What needs updating?"

Only modify the fields the user mentions. Preserve everything else.

## Output

Generate `{project-dir}/context.md` using the template at `templates/context-template.md`.

**Output rules**:
- YAML frontmatter: machine-readable fields (name, URL, colors as hex, platforms as array)
- Markdown body: human-readable prose (features, audience, competitors, notes)
- All hex colors validated (6-char format)
- All URLs as full https:// format
- Bilingual content preserved as-is (don't translate user's words)

## Validation

After generating context.md, verify:
- [ ] Product name is not empty
- [ ] At least 1 target audience defined
- [ ] At least 1 video platform specified
- [ ] At least 1 language specified
- [ ] Brand colors are valid hex (if provided)
- [ ] Founder visibility preference is set

If any critical field is missing, ask the user — don't guess.

## Real-World Examples

**[App Name]** (a reader/learning app):
- Product: AI read-later app → Explainer video, 78s, YouTube/Product Hunt
- Brand: `#007AFF` primary, SF Pro font, warm/approachable tone
- Hero feature: AI reflow + instant summary
- Context existed in: `{project}/video-strategy.md`

**[CLI Tool]** (a developer networking tool):
- Product: P2P agent collaboration → Launch video, 90s, YouTube/GitHub
- Brand: `#1D3557` deep ocean, `#E63946` lobster red, cinematic/authoritative
- Hero feature: ASCII globe + npx install
- Context existed in: `{project}/questionaire.md` + `{project}/product-codex.md`
- Founder visibility: **anonymous** (user requested)

## Related Skills

- `/iopho-video-director` — calls this skill as Phase 0 step 1
- `/iopho-searching-videos` — uses reference video URLs from context
- `/vsl-storyboard-writer` — reads context for audience/positioning
- `/storyboard` — reads context for product understanding
