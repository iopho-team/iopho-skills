---
name: pnote
description: pnote - The PromptNote CLI for managing prompts, notes, and snippets
allowed-tools: Bash(pnote *), mcp__promptnote__check_pin_status, mcp__promptnote__create_note, mcp__promptnote__create_snippet, mcp__promptnote__delete_note, mcp__promptnote__get_note, mcp__promptnote__get_shared_tag_notes, mcp__promptnote__get_snippet, mcp__promptnote__list_notes, mcp__promptnote__list_protected_notes, mcp__promptnote__list_shared_notes, mcp__promptnote__list_shared_tags, mcp__promptnote__list_snippets, mcp__promptnote__list_tags, mcp__promptnote__merge_tags, mcp__promptnote__rename_tag, mcp__promptnote__search, mcp__promptnote__toggle_favorite, mcp__promptnote__update_note, mcp__promptnote__update_snippet
user-invocable: true
argument-hint: <command> [options]
updated: "2026-03-22"
---

# pnote — PromptNote CLI

Manage prompts, notes, and snippets from the terminal or as an AI agent.

**Tool preference:** Use `pnote` CLI (Bash) for all operations — it's faster, token-efficient, and composable with `grep`, `jq`, pipes. Use `mcp__promptnote__*` tools as fallback when: (1) pnote is not installed, (2) accessing PIN-protected notes and `PNOTE_PIN` env is not set (MCP handles PIN transparently via its own config).

**Install:** `npm install -g pnote`
**Auth:** `pnote auth token <your-pat>` (get PAT from PromptNote web app → Settings → API Tokens)

---

## Global Flags (apply to all commands)

| Flag | Description |
|---|---|
| `--json` | Output as JSON (for scripting / jq) |
| `--plain` | Plain text, no color/formatting |
| `--no-color` | Disable color only |
| `-p, --pin <pin>` | PIN for protected notes (avoid: visible in shell history) |
| `--pin-stdin` | Read PIN from first line of stdin |
| `-V, --version` | Show version |

---

## Auth

```bash
pnote auth login            # Open browser OAuth login
pnote auth token <pat>      # Set PAT directly (pn_xxx format)
pnote auth whoami           # Show current user + token info
pnote auth logout           # Remove stored credentials
```

---

## Notes

```bash
# List
pnote notes                             # All active notes
pnote notes --tag "AI/art"              # Filter by tag (supports hierarchy)
pnote notes --archived                  # Show archived notes
pnote notes --pinned                    # Show only pinned notes
pnote notes --deleted                   # Show deleted notes
pnote notes --protected                 # Show only PIN-protected notes
pnote notes --search "query"            # Search by title
pnote notes --limit 20                  # Limit results (default: 50)

# Read
pnote notes get <id>                    # Get note + all snippet versions
pnote notes get <id> --latest           # Get note + latest snippet only

# Create & manage
pnote notes create "Title"              # Create note
pnote notes create "Title" --tags AI/art work  # With tags
pnote notes create "Title" --content "..."     # With initial snippet
pnote notes update <id> --title "New"   # Update title
pnote notes update <id> --tags AI work  # Replace all tags
pnote notes archive <id>                # Archive note
pnote notes archive <id> --undo         # Unarchive note
pnote notes pin <id>                    # Toggle pin on note
pnote notes delete <id>                 # Soft delete (goes to trash)
pnote notes delete <id> --force         # Skip confirmation
```

---

## Snippets (prompt versions)

```bash
pnote notes snippet <note-id>           # Show latest snippet content (pipe-friendly)
pnote notes snippet list <note-id>      # List all versions
pnote notes snippet copy <note-id>      # Copy latest to clipboard
pnote notes snippet copy <note-id> --version 2  # Copy specific version
pnote notes snippet add <note-id>       # Add new version from stdin
pnote notes snippet update <snippet-id> # Update snippet from stdin
pnote notes snippet favorite <snippet-id>  # Toggle favorite (★)
```

**stdin examples:**
```bash
echo "My prompt text" | pnote notes snippet add <note-id>
cat prompt.txt | pnote notes snippet add <note-id>
pbpaste | pnote notes snippet add <note-id>
```

---

## Tags

```bash
pnote tags                              # List all tags with counts (tree view)
pnote tags --include-archived           # Include tags from archived notes
pnote tags rename "old" "new"           # Rename tag (also renames children)
pnote tags merge "AI" "ML" --into "AI/ML"  # Merge multiple tags into one
```

Tags are hierarchical: `AI/art/portrait` — filtering by `AI` matches all children.

---

## Search

```bash
pnote search "query"                    # Search notes + snippets
pnote search "query" --notes-only       # Notes only
pnote search "query" --snippets-only    # Snippets only
pnote search "query" --limit 10
```

---

## Share

```bash
pnote share tags                        # List shared tags (owned + shared with me)
pnote share tags <shared-tag-id>        # View notes in a shared tag
pnote share notes                       # List your public share links
pnote share notes --include-revoked     # Include revoked links
```

---

## PIN Protection

Protected notes encrypt content server-side. PIN is set in PromptNote app → Settings.

**PIN resolution order (CLI):**
1. `-p <pin>` flag — direct (⚠️ visible in shell history)
2. `--pin-stdin` — first line of stdin
3. `PNOTE_PIN` env var — **recommended for agents and automation**
4. Session cache — 5-min TTL in `$TMPDIR/pnote-pin-<uid>`
5. Interactive prompt — TTY only; 3 attempts; hidden input
6. Fails gracefully — error: "PIN required but not provided. Use -p <pin> or set PNOTE_PIN environment variable."

**In agent/non-TTY context** — step 5 is skipped. Always use `PNOTE_PIN`:
```bash
PNOTE_PIN=1234 pnote notes --protected
PNOTE_PIN=1234 pnote notes get <protected-note-id>
echo "1234" | pnote notes get <id> --pin-stdin
```

**Check PIN status:**
```bash
pnote pin status          # Is PIN configured? N protected notes? Cache valid?
pnote pin list            # List protected notes (metadata only, no content)
```

**MCP fallback for PIN:** If MCP tools are configured with `PROMPTNOTE_PIN` in `claude_desktop_config.json`, use `mcp__promptnote__*` tools instead — PIN is handled transparently.

---

## Agent Skills Sync

Notes with `note_type=skill` and title `skill-name/filename.md` are agent skill files.

```bash
pnote skills                            # List skills in cloud
pnote skills pull                       # Pull all globally (~/.agents/skills/ + symlinks)
pnote skills pull <name>                # Pull a specific skill globally
pnote skills pull --project             # Pull project-level (.agents/skills/ + .claude/skills/ etc.)
pnote skills pull --project <name>      # Pull specific skill project-level
pnote skills pull --dry-run             # Preview without writing
pnote skills push <dir>                 # Upload local skill directory to cloud
```

**Scope behaviour:**
- **Global (default):** writes to `~/.agents/skills/<name>/`, symlinks into `~/.claude/skills/`, `~/.windsurf/skills/`, `~/.augment/skills/` etc. for every agent installed on the system. Layout matches `npx skills` exactly — the two coexist without conflict.
- **Project (`--project`):** same layout but relative to cwd (`.agents/skills/`, `.claude/skills/`, etc.). Use when skills should be scoped to a single project.
- **Custom (`--dir <path>`):** writes files directly to `<path>/<name>/`, no symlinks. For manual control.

---

## Scripting & Composability

The CLI's advantage over MCP: composable with Unix tools.

```bash
# Get note IDs for a tag, pipe to further processing
pnote notes --tag "AI" --json | jq '.[].id'

# Find all pinned notes containing "GPT"
pnote notes --pinned --json | jq '.[] | select(.title | test("GPT"))'

# Search and get full content of first result
pnote search "prompt" --json | jq -r '.notes[0].id' | xargs pnote notes get

# List protected notes, copy first one's content to clipboard
pnote pin list --json | jq -r '.[0].id' | xargs -I{} bash -c 'PNOTE_PIN=1234 pnote notes snippet {}'

# Bulk: add new snippet to multiple notes
for id in abc123 def456; do echo "updated content" | pnote notes snippet add $id; done
```

---

## Execute

Run the user's pnote command:

```bash
pnote $ARGUMENTS
```
