# iopho-team/skills

AI agent skills for [iopho](https://github.com/iopho-team) products. Works with Claude Code, Cursor, Windsurf, and [40+ other agents](https://skills.sh/).

## Available Skills

| Skill | Description | Install |
|-------|-------------|---------|
| [pnote](skills/pnote/) | [PromptNote](https://promptnoteapp.com/) CLI for managing prompts, notes, and snippets | `npx skills add iopho-team/skills --skill pnote` |
| [iopho-searching-videos](skills/iopho-searching-videos/) | Search videos across YouTube, Bilibili, and other platforms without downloading | `npx skills add iopho-team/skills --skill iopho-searching-videos` |
| [iopho-getting-videos](skills/iopho-getting-videos/) | Download video, audio, subtitles, and metadata from 1800+ platforms | `npx skills add iopho-team/skills --skill iopho-getting-videos` |
| [iopho-analyzing-videos](skills/iopho-analyzing-videos/) | Reverse-engineer videos into .storyboard.md files for AI video regeneration | `npx skills add iopho-team/skills --skill iopho-analyzing-videos` |

## Quick Install

```bash
# Install a specific skill
npx skills add iopho-team/skills --skill pnote

# Install all skills
npx skills add iopho-team/skills --all

# Global install (available across all projects)
npx skills add iopho-team/skills --skill pnote -g -y
```

## Manual Install

Each skill is a directory under `skills/` with a `SKILL.md` file. Copy the skill directory into your agent's skill folder:

- **Claude Code**: `.claude/skills/`
- **Cursor / Windsurf / Other**: `.agents/skills/`

## License

MIT
