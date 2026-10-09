# pnote

[![npm](https://img.shields.io/npm/v/pnote)](https://www.npmjs.com/package/pnote)

Agent skill for [PromptNote](https://promptnoteapp.com/) CLI. Works with Claude Code, Cursor, Windsurf, and [40+ agents](https://skills.sh/).

## Installation

### Option A: Via skills.sh (Recommended)

**Interactive** (choose agents and confirm):
```bash
npx skills add iopho-team/iopho-skills --skill pnote
```

**Non-interactive** (install to all agents, skip prompts):
```bash
npx skills add iopho-team/iopho-skills --skill pnote --all
```

**Global install** (user-level, available across all projects):
```bash
npx skills add iopho-team/iopho-skills --skill pnote -g -y
```

### Option B: Manual Installation

#### 1. Install the CLI

```bash
npm install -g pnote
```

#### 2. Authenticate

[Generate an API token](https://app.promptnoteapp.com/?action=mcp-access) from the web app, then:

```bash
pnote auth token pn_your_token_here
```

#### 3. Use the Skill

In Claude Code, use `/pnote` to invoke:

```
/pnote notes
/pnote search "AI art"
/pnote notes snippet copy abc123
```

## What This Skill Does

This skill wraps the `pnote` CLI to let Claude help you:

- **List and search** your notes and snippets
- **Read and copy** prompt content to clipboard
- **Create and manage** notes, tags, and versions
- **Access PIN-protected** notes securely

## CLI Commands

| Command | Description |
|---------|-------------|
| `pnote notes` | List all notes |
| `pnote notes get <id>` | Get note with all snippet versions |
| `pnote notes get <id> --latest` | Get note with only latest snippet |
| `pnote notes snippet <id>` | Show latest snippet (pipe-friendly) |
| `pnote notes snippet list <id>` | Show all snippet versions |
| `pnote notes snippet copy <id>` | Copy latest snippet to clipboard |
| `pnote notes snippet add <id>` | Add new snippet version from stdin |
| `pnote search <query>` | Search notes and snippets |
| `pnote tags` | List all tags |
| `pnote skills` | List skills in cloud |
| `pnote skills pull` | Pull all skills globally (`~/.agents/skills/` + agent symlinks) |
| `pnote skills pull <name>` | Pull a specific skill globally |
| `pnote skills pull --project` | Pull project-level (`.agents/skills/` + `.claude/skills/` etc.) |
| `pnote skills push <dir>` | Upload a local skill to cloud |
| `pnote skills diff [name]` | Compare local skill files with the cloud |
| `pnote skills scan` | Read-only inventory of local skills (drift, dangling links, cleanup hints) |

See `pnote --help` for full documentation.

## Links

- [PromptNote App](https://app.promptnoteapp.com/)
- [Documentation](https://www.promptnoteapp.com/docs/)
- [Feedback & Bugs](https://iohpo.featurebase.app/?b=695f9152f13092ad189fb4de)

## License

MIT
