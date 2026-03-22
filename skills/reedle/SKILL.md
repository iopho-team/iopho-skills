---
name: reedle
description: reedle - The Reedle CLI for managing your intelligent reading library
allowed-tools: Bash(reedle *), mcp__reedle__reedle_list_articles, mcp__reedle__reedle_get_article, mcp__reedle__reedle_get_article_content, mcp__reedle__reedle_create_article, mcp__reedle__reedle_update_article, mcp__reedle__reedle_delete_article, mcp__reedle__reedle_search_articles, mcp__reedle__reedle_search_semantic, mcp__reedle__reedle_find_similar_articles, mcp__reedle__reedle_list_tags, mcp__reedle__reedle_tag_article, mcp__reedle__reedle_list_lists, mcp__reedle__reedle_get_list, mcp__reedle__reedle_list_highlights, mcp__reedle__reedle_get_highlight, mcp__reedle__reedle_list_comments, mcp__reedle__reedle_process_url, mcp__reedle__reedle_get_processing_status, mcp__reedle__reedle_get_credit_balance, mcp__reedle__reedle_list_decks, mcp__reedle__reedle_list_cards_due, mcp__reedle__reedle_get_study_stats
user-invocable: true
argument-hint: <command> [options]
---

# reedle — Intelligent Reading Companion CLI

Manage your Reedle reading library from the terminal or as an AI agent.

**Tool preference:** Use `reedle` CLI (Bash) for all operations — it's faster, token-efficient, and composable with `grep`, `jq`, and pipes. Use `mcp__reedle__*` MCP tools as fallback when the CLI is not installed or when complex multi-step MCP tool chains are more appropriate.

**Install:** `cd apps/reedle-cli && pnpm build && npm install -g .` (monorepo) or `npm install -g reedle`

**Auth:** Generate a CLI token at `app.reedle.iopho.com → Settings → Integrations → CLI Token`, then:
```bash
reedle auth token rdk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Global Flags

| Flag | Description |
|---|---|
| `--json` | Output as JSON (for scripting / jq) |
| `--no-color` | Disable color output |
| `-V, --version` | Show version |

---

## Auth

```bash
reedle auth token <rdk_xxx>   # Set PAT (get from web Settings → Integrations → CLI Token)
reedle auth whoami             # Verify token + show status
reedle auth logout             # Remove stored credentials
```

Token stored in `~/.config/reedle/credentials.json` (or `~/Library/Application Support/reedle/` on macOS).
Override with env var: `REEDLE_TOKEN=rdk_xxx reedle list`

---

## Articles

```bash
reedle save <url>                          # Save a URL (processing happens in background)
reedle save <url> -t research -t ai        # Save with tags
reedle list                                # List recent articles
reedle list --tag research                 # Filter by tag
reedle list --list <list-id>              # Filter by list
reedle list --starred                      # Starred only
reedle list --status ready                 # Filter by status
reedle list -n 100                         # Increase limit (default: 50)
reedle get <id>                            # Get article metadata
reedle get <id> --content                  # Get full article text (markdown)
reedle open <id>                           # Open in browser
```

---

## Search

```bash
reedle search "machine learning"           # Keyword search (title + excerpt)
reedle search "attention mechanism" -s     # Semantic (AI) search
reedle search "neural nets" -n 10          # Limit results
reedle search "topic" --json | jq '.'     # JSON output for scripting
```

---

## Tags & Lists

```bash
reedle tags                                # List all tags with counts
reedle lists                               # List all reading lists
```

---

## Agentic Patterns

### Research assistant workflow
```bash
# Find relevant articles on a topic
reedle search "transformer architecture" -s --json | jq '.articles[].id'

# Read the top result
reedle get <id> --content

# Find similar articles
# (use MCP fallback: mcp__reedle__reedle_find_similar_articles)
```

### Save and tag batch URLs
```bash
for url in https://arxiv.org/... https://papers.with...
do
  reedle save "$url" -t papers -t 2025
done
```

### Export article list as JSON for processing
```bash
reedle list --tag research --json | jq '.[] | {id, title, url}'
```

### Pipe article content to another tool
```bash
reedle get <id> --content | wc -w        # Word count
reedle get <id> --content | head -50     # First 50 lines
```

---

## MCP Fallback (when CLI not available)

Use `mcp__reedle__*` tools directly for operations the CLI doesn't yet cover:

- `mcp__reedle__reedle_list_highlights` — article highlights
- `mcp__reedle__reedle_list_comments` — comments
- `mcp__reedle__reedle_find_similar_articles` — similarity search
- `mcp__reedle__reedle_list_decks` / `reedle_list_cards_due` — flashcards
- `mcp__reedle__reedle_get_credit_balance` — credit balance
- `mcp__reedle__reedle_process_url` — trigger URL processing

---

## Config

| Item | Value |
|---|---|
| Token env var | `REEDLE_TOKEN` |
| Config dir | `~/.config/reedle/` |
| Credentials file | `~/.config/reedle/credentials.json` |
| API endpoint override | `REEDLE_API_ENDPOINT=<url>` |
| Web app | `https://app.reedle.iopho.com` |
| MCP endpoint | `https://fhgxapmrciwlhsffdeyj.supabase.co/functions/v1/reedle-mcp` |
