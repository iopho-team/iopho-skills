# iopho-skills

[English](README.md) | [简体中文](README.zh-CN.md)

AI agent skills for [iopho](https://github.com/iopho-team) products. Works with Claude Code, Cursor, Windsurf, and [40+ other agents](https://skills.sh/).

## Available Skills

### iopho Apps

Skills for iopho's own products — reading, notes, and knowledge management.

| Skill | Description |
|-------|-------------|
| [reedle](skills/reedle/) | Intelligent reading library CLI — save/read articles, YouTube & Bilibili transcripts, semantic search, highlights, flashcard decks<br>`npx skills add iopho-team/iopho-skills --skill reedle` · _updated 2026-03-22_ |
| [pnote](skills/pnote/) | [PromptNote](https://promptnoteapp.com/) CLI for managing prompts, notes, and snippets<br>`npx skills add iopho-team/iopho-skills --skill pnote` · _updated 2026-03-22_ |

### Video Production — Orchestrator

Start here. The director skill guides you through the full pipeline and routes to all other skills.

| Skill | Description |
|-------|-------------|
| [iopho-video-director](skills/iopho-video-director/) | Master orchestrator: 4-phase pipeline (Context → Storyboard → Production → Visual QA)<br>`npx skills add iopho-team/iopho-skills --skill iopho-video-director` · _updated 2026-03-19_ |

### Video Production — Specialized Skills

Individual skills for each stage of the pipeline. Can be used standalone or invoked by the orchestrator.

| Skill | Description |
|-------|-------------|
| [iopho-product-context](skills/iopho-product-context/) | Interactive intake questionnaire → context.md (product/audience/brand)<br>`npx skills add iopho-team/iopho-skills --skill iopho-product-context` · _updated 2026-03-19_ |
| [iopho-searching-videos](skills/iopho-searching-videos/) | Search videos across YouTube, Bilibili, and other platforms without downloading<br>`npx skills add iopho-team/iopho-skills --skill iopho-searching-videos` · _updated 2026-02-27_ |
| [iopho-getting-videos](skills/iopho-getting-videos/) | Download video, audio, subtitles, and metadata from 1800+ platforms<br>`npx skills add iopho-team/iopho-skills --skill iopho-getting-videos` · _updated 2026-02-27_ |
| [iopho-analyzing-videos](skills/iopho-analyzing-videos/) | Reverse-engineer videos into .storyboard.md files for AI video regeneration<br>`npx skills add iopho-team/iopho-skills --skill iopho-analyzing-videos` · _updated 2026-03-13_ |
| [iopho-recording-checklist](skills/iopho-recording-checklist/) | Generate per-project screen recording shot list from storyboard<br>`npx skills add iopho-team/iopho-skills --skill iopho-recording-checklist` · _updated 2026-03-19_ |
| [iopho-seedance-prompts](skills/iopho-seedance-prompts/) | 即梦 Seedance 2.0 prompt engineering — CN-first, 10 capability modes<br>`npx skills add iopho-team/iopho-skills --skill iopho-seedance-prompts` · _updated 2026-02-28_ |
| [iopho-voiceover-tts](skills/iopho-voiceover-tts/) | Generate voiceover with ElevenLabs/MiniMax/Edge TTS, voice audition, multi-lang assembly<br>`npx skills add iopho-team/iopho-skills --skill iopho-voiceover-tts` · _updated 2026-03-19_ |
| [iopho-audio-director](skills/iopho-audio-director/) | BGM + VO + SFX assembly with ducking, Suno prompt templates, FFmpeg export<br>`npx skills add iopho-team/iopho-skills --skill iopho-audio-director` · _updated 2026-03-19_ |

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
