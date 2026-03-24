---
name: reedle
description: reedle - The Reedle CLI for managing your intelligent reading library and extracting content
allowed-tools: Bash(reedle *), mcp__reedle__reedle_list_articles, mcp__reedle__reedle_get_article, mcp__reedle__reedle_get_article_content, mcp__reedle__reedle_create_article, mcp__reedle__reedle_update_article, mcp__reedle__reedle_delete_article, mcp__reedle__reedle_search_articles, mcp__reedle__reedle_search_semantic, mcp__reedle__reedle_find_similar_articles, mcp__reedle__reedle_list_tags, mcp__reedle__reedle_tag_article, mcp__reedle__reedle_list_lists, mcp__reedle__reedle_get_list, mcp__reedle__reedle_list_highlights, mcp__reedle__reedle_get_highlight, mcp__reedle__reedle_list_comments, mcp__reedle__reedle_save, mcp__reedle__reedle_save_youtube, mcp__reedle__reedle_save_bilibili, mcp__reedle__reedle_read, mcp__reedle__reedle_read_youtube, mcp__reedle__reedle_read_bilibili, mcp__reedle__reedle_get_processing_status, mcp__reedle__reedle_get_credit_balance, mcp__reedle__reedle_list_decks, mcp__reedle__reedle_list_cards_due, mcp__reedle__reedle_get_study_stats
user-invocable: true
argument-hint: <command> [options]
updated: "2026-03-24"
---

# reedle — Intelligent Reading Companion CLI

Manage your Reedle reading library and extract content from the terminal or as an AI agent.

**Tool preference:** Use `reedle` CLI (Bash) for all operations — it's faster, token-efficient, and composable with `grep`, `jq`, and pipes. Use `mcp__reedle__*` MCP tools as fallback when the CLI is not installed or when complex multi-step MCP tool chains are more appropriate.

**Install:** `npm install -g reedle-cli`

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

## CRITICAL: Save vs Read Decision Rule

**Before using any save/read tool, determine user intent:**

| User says… | Use |
|---|---|
| "save", "add", "keep", "bookmark" | `reedle save` / `reedle_save*` |
| "read", "summarize", "check", "fetch", "what does this say" | `reedle read` / `reedle_read*` |
| Unclear | **Default to `reedle_read*`** — never pollute library without clear intent |

**After `reedle read`:** Offer "This article was interesting — want me to save it to your Reedle library?"

**Why this matters:** The user's Reedle library is their curated knowledge base. Saving content they didn't ask to save degrades it. When in doubt, extract first, ask to save after.

---

## Save to Library

Saves content permanently to the user's Reedle library. Full LLM pipeline runs (fetch → parse → embed). Processing is async — use `reedle show <id>` or `reedle_get_processing_status` to check when ready.

```bash
reedle save <url>                          # Save a web article
reedle save <url> -t research -t ai        # Save with tags
```

**MCP tools (when CLI not available):**
```
mcp__reedle__reedle_save            — save web article URL to library
mcp__reedle__reedle_save_youtube    — save YouTube video (transcript) to library; params: video_url_or_id, language_code?
mcp__reedle__reedle_save_bilibili   — save Bilibili video (transcript) to library; params: video_url_or_id, cookie (required), page?
mcp__reedle__reedle_get_processing_status — check save pipeline status
```

---

## Read / Extract (ephemeral, no library save)

Extracts content inline without saving. Credit costs: web=5cr, YouTube=10cr, Bilibili=15cr, +20cr if `--llm`.

```bash
reedle read <url>                          # Extract web article → stdout
reedle read <url> --llm                    # With LLM cleanup (better quality, +20cr)
reedle read <url> | head -100             # First 100 lines
reedle read <url> --json                  # JSON with metadata

reedle read <youtube-url>                  # Auto-detects YouTube URLs
reedle read <video-id> --youtube           # Force YouTube mode
reedle read <video-id> --youtube --lang zh # Chinese transcript
reedle read <youtube-url> --save          # Extract + also save to library

reedle read <bvid> --bilibili --cookie "..." # Bilibili transcript
```

**MCP tools (when CLI not available):**
```
mcp__reedle__reedle_read            — extract web content; params: url, llm_cleanup?
mcp__reedle__reedle_read_youtube    — extract YouTube transcript; params: video_url_or_id, language_code?
mcp__reedle__reedle_read_bilibili   — extract Bilibili transcript; params: video_url_or_id, cookie (required), page?
```

---

## Articles (Library Management)

```bash
reedle list                                # List recent articles
reedle list --tag research                 # Filter by tag
reedle list --list <list-id>              # Filter by list
reedle list --starred                      # Starred only
reedle list --status ready                 # Filter by status
reedle list -n 100                         # Increase limit (default: 50)
reedle show <id>                           # Show article metadata
reedle cat <id>                            # Output full article text to stdout (pipe-friendly)
reedle open <id>                           # Open in browser
```

---

## Actions

```bash
reedle star <id>                           # Star an article
reedle unstar <id>                         # Unstar an article
reedle archive <id>                        # Archive an article
reedle unarchive <id>                      # Unarchive an article
reedle delete <id> --force                 # Delete (--force required to confirm)
reedle tag <id> <tag>                      # Add a tag
reedle untag <id> <tag>                    # Remove a tag
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

## Browse TUI (fzf)

Interactive two-pane browser powered by `fzf`. Requires `fzf` in PATH; `glow` or `bat` enhance the preview.

```bash
reedle browse                              # Open interactive article browser
```

**Keyboard shortcuts:**
- `Enter` — open in web browser
- `Ctrl-O` — also opens in browser
- `Esc / Ctrl-C` — exit

**Install fzf:** `brew install fzf` / `apt install fzf` / `scoop install fzf`

---

## Agentic Patterns

### Research without polluting library (use read_* tools)
```bash
# Extract and analyze without saving
reedle read <url> | wc -w                 # Word count before deciding to save

# MCP pattern for research:
# 1. mcp__reedle__reedle_read (url)        — get content
# 2. Analyze content
# 3. Ask user: "Want me to save this to your library?"
# 4. If yes: mcp__reedle__reedle_save (url)
```

### Save and tag batch URLs
```bash
for url in https://arxiv.org/... https://papers.with...
do
  reedle save "$url" -t papers -t 2025
done
```

### YouTube workflow
```bash
# Just read the transcript:
reedle read https://youtube.com/watch?v=xxx --youtube

# Read then save:
reedle read https://youtube.com/watch?v=xxx --youtube --save

# MCP: read first, offer to save
# mcp__reedle__reedle_read_youtube (video_url_or_id, language_code?)
# → returns transcript inline
# → offer: "Want me to save this video to your library?"
# mcp__reedle__reedle_save_youtube (video_url_or_id, language_code?)
```

### Pipe article content to another tool
```bash
reedle cat <id> | wc -w                   # Word count
reedle cat <id> | glow                    # Render markdown in terminal
reedle read <url> | head -50              # Preview before deciding to save
reedle read <url> --json | jq '.content'  # Extract content field
```

### Export article list as JSON for processing
```bash
reedle list --tag research --json | jq '.[] | {id, title, url}'
```

---

## MCP Fallback (when CLI not available)

Use `mcp__reedle__*` tools directly for operations the CLI doesn't yet cover:

- `mcp__reedle__reedle_list_highlights` — article highlights
- `mcp__reedle__reedle_list_comments` — comments
- `mcp__reedle__reedle_find_similar_articles` — similarity search
- `mcp__reedle__reedle_list_decks` / `reedle_list_cards_due` — flashcards
- `mcp__reedle__reedle_get_credit_balance` — credit balance

---

## Credit Costs (Extraction Only)

| Operation | Credits | Notes |
|---|---|---|
| `reedle_read` (web) | 5 cr | Jina Reader fetch |
| `reedle_read_youtube` | 10 cr | Transcript via reedle-server-py |
| `reedle_read_bilibili` | 15 cr | Requires cookie |
| `+llm_cleanup` add-on | +20 cr | Gemini Flash content cleanup |
| Save operations | Dynamic | LLM cost deducted by server post-completion |

1 credit = $0.001 USD. Check balance: `mcp__reedle__reedle_get_credit_balance`

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
