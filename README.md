# iopho-skills

AI agent skills for [iopho](https://github.com/iopho-team) products. Works with Claude Code, Cursor, Windsurf, and [40+ other agents](https://skills.sh/).

## Available Skills

### Video Production Pipeline

| Skill | Description | Updated | Install |
|-------|-------------|---------|---------|
| [iopho-video-director](skills/iopho-video-director/) | Master orchestrator: 4-phase pipeline (Context → Storyboard → Production → Visual QA) | 2026-03-19 | `npx skills add iopho-team/iopho-skills --skill iopho-video-director` |
| [iopho-product-context](skills/iopho-product-context/) | Interactive intake questionnaire → context.md (product/audience/brand) | 2026-03-19 | `npx skills add iopho-team/iopho-skills --skill iopho-product-context` |
| [iopho-searching-videos](skills/iopho-searching-videos/) | Search videos across YouTube, Bilibili, and other platforms without downloading | 2026-02-27 | `npx skills add iopho-team/iopho-skills --skill iopho-searching-videos` |
| [iopho-getting-videos](skills/iopho-getting-videos/) | Download video, audio, subtitles, and metadata from 1800+ platforms | 2026-02-27 | `npx skills add iopho-team/iopho-skills --skill iopho-getting-videos` |
| [iopho-analyzing-videos](skills/iopho-analyzing-videos/) | Reverse-engineer videos into .storyboard.md files for AI video regeneration | 2026-03-13 | `npx skills add iopho-team/iopho-skills --skill iopho-analyzing-videos` |
| [iopho-recording-checklist](skills/iopho-recording-checklist/) | Generate per-project screen recording shot list from storyboard | 2026-03-19 | `npx skills add iopho-team/iopho-skills --skill iopho-recording-checklist` |
| [iopho-seedance-prompts](skills/iopho-seedance-prompts/) | 即梦 Seedance 2.0 prompt engineering — CN-first, 10 capability modes | 2026-02-28 | `npx skills add iopho-team/iopho-skills --skill iopho-seedance-prompts` |
| [iopho-voiceover-tts](skills/iopho-voiceover-tts/) | Generate voiceover with ElevenLabs/MiniMax/Edge TTS, voice audition, multi-lang assembly | 2026-03-19 | `npx skills add iopho-team/iopho-skills --skill iopho-voiceover-tts` |
| [iopho-audio-director](skills/iopho-audio-director/) | BGM + VO + SFX assembly with ducking, Suno prompt templates, FFmpeg export | 2026-03-19 | `npx skills add iopho-team/iopho-skills --skill iopho-audio-director` |

### Other Tools

| Skill | Description | Updated | Install |
|-------|-------------|---------|---------|
| [pnote](skills/pnote/) | [PromptNote](https://promptnoteapp.com/) CLI for managing prompts, notes, and snippets | 2026-03-22 | `npx skills add iopho-team/iopho-skills --skill pnote` |

## Quick Install

```bash
# Install a specific skill
npx skills add iopho-team/iopho-skills --skill pnote

# Install all skills
npx skills add iopho-team/iopho-skills --all

# Global install (available across all projects)
npx skills add iopho-team/iopho-skills --skill pnote -g -y
```

## Manual Install

Each skill is a directory under `skills/` with a `SKILL.md` file. Copy the skill directory into your agent's skill folder:

- **Claude Code**: `.claude/skills/`
- **Cursor / Windsurf / Other**: `.agents/skills/`

## License

MIT
