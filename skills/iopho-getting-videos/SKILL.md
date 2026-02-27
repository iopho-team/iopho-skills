---
name: iopho-getting-videos
description: Download video, audio, subtitles, and metadata from YouTube, Bilibili, Vimeo, and 1800+ platforms
allowed-tools: Bash(yt-dlp *), Bash(python3 *), Bash(ffmpeg *), Bash(BBDown *), Bash(lux *), Bash(you-get *)
user-invocable: true
argument-hint: <url> [--mode video|audio|transcript|metadata|all] [--quality best|720p|480p] [--output DIR]
---

# iopho-getting-videos — Cross-Platform Video/Audio/Subtitle Downloader

Download video, audio, subtitles, thumbnails, and metadata from 1800+ platforms with intelligent tool routing and fallback chains.

## Prerequisites

Check what's available:

!`which yt-dlp 2>/dev/null && echo "yt-dlp: ✓ (primary — covers 1800+ sites)" || echo "yt-dlp: ✗ — install: pip install yt-dlp"`

!`which ffmpeg 2>/dev/null && echo "ffmpeg: ✓ (needed for merging/conversion)" || echo "ffmpeg: ✗ — install: brew install ffmpeg"`

!`python3 -c "from youtube_transcript_api import YouTubeTranscriptApi; print('youtube-transcript-api: ✓ (fast YouTube transcripts)')" 2>/dev/null || echo "youtube-transcript-api: ✗ (optional) — install: pip install youtube-transcript-api"`

!`which BBDown 2>/dev/null && echo "BBDown: ✓ (Bilibili specialist)" || echo "BBDown: ✗ (optional for Bilibili) — install: dotnet tool install -g BBDown"`

!`which lux 2>/dev/null && echo "lux: ✓ (Chinese platforms)" || echo "lux: ✗ (optional) — install: go install github.com/iawia002/lux@latest"`

**Minimum**: `yt-dlp` + `ffmpeg` covers 95% of use cases.

## Modes

| Mode | What You Get | Primary Tool |
|------|-------------|-------------|
| `video` | Video file (best quality) | yt-dlp |
| `audio` | Audio-only (MP3/M4A) | yt-dlp -x |
| `transcript` | Subtitles/captions text | youtube-transcript-api → yt-dlp --write-subs |
| `metadata` | JSON with title, duration, tags, etc. | yt-dlp --dump-json |
| `all` | Video + audio + subs + metadata + thumbnail | yt-dlp (combined flags) |

## Quick Reference

**Download video** (best quality):
```bash
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best" --merge-output-format mp4 -o "$OUTPUT_DIR/%(title)s.%(ext)s" "$URL"
```

**Audio only** (MP3):
```bash
yt-dlp -x --audio-format mp3 --audio-quality 0 -o "$OUTPUT_DIR/%(title)s.%(ext)s" "$URL"
```

**Transcript only** (fastest — YouTube):
```bash
python3 -c "
from youtube_transcript_api import YouTubeTranscriptApi
import re, sys
video_id = re.search(r'(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})', '$URL').group(1)
try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    for entry in transcript:
        m, s = divmod(int(entry['start']), 60)
        print(f'[{m}:{s:02d}] {entry[\"text\"]}')
except Exception:
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['zh-Hans','zh-Hant','ja','ko','en'])
    for entry in transcript:
        m, s = divmod(int(entry['start']), 60)
        print(f'[{m}:{s:02d}] {entry[\"text\"]}')
"
```

**Transcript via yt-dlp** (any platform):
```bash
yt-dlp --write-subs --write-auto-subs --sub-lang "en,zh-Hans,zh-Hant" --sub-format srt --skip-download -o "$OUTPUT_DIR/%(title)s" "$URL"
```

**Metadata only** (no download):
```bash
yt-dlp --dump-json "$URL" 2>/dev/null | python3 -c "
import sys, json
v = json.loads(sys.stdin.read())
print(f\"Title: {v['title']}\")
print(f\"Duration: {v.get('duration','?')}s\")
print(f\"Resolution: {v.get('width','?')}x{v.get('height','?')}\")
print(f\"FPS: {v.get('fps','?')}\")
print(f\"Channel: {v.get('channel', v.get('uploader','?'))}\")
print(f\"Upload date: {v.get('upload_date','?')}\")
print(f\"View count: {v.get('view_count','?')}\")
print(f\"URL: {v.get('webpage_url', v.get('url','?'))}\")
"
```

**Everything** (video + subs + metadata + thumbnail):
```bash
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best" --merge-output-format mp4 \
  --write-subs --write-auto-subs --sub-lang "en,zh-Hans,zh-Hant" --sub-format srt \
  --write-info-json --write-thumbnail \
  -o "$OUTPUT_DIR/%(title)s.%(ext)s" "$URL"
```

## Execute

Parse the user's arguments and run the appropriate download:

```bash
# Parse arguments from: $ARGUMENTS
# Expected: <url> [--mode video|audio|transcript|metadata|all] [--quality best|720p|480p] [--output DIR]
#
# Default: --mode video --quality best --output ./
#
# The agent should:
# 1. Detect platform from URL domain
# 2. Choose optimal tool (see Routing Logic below)
# 3. Run download with appropriate flags
# 4. Report: file path, size, duration, format
```

## Routing Logic

The agent should auto-detect the best tool based on URL:

```
URL contains youtube.com / youtu.be:
  transcript-only? → youtube-transcript-api (fastest, no download)
  else → yt-dlp

URL contains bilibili.com / b23.tv:
  yt-dlp fails? → BBDown (handles multi-part, interactive videos)
  transcript-only? → yt-dlp --write-subs (Bilibili CC subs)

URL contains youku/iqiyi/qq.com/mgtv:
  yt-dlp fails? → lux (Chinese platform specialist)

URL contains vimeo.com:
  yt-dlp (works for most public videos)
  private/embedded? → try yt-dlp --referer <page_url>

URL contains tiktok.com / douyin.com:
  yt-dlp (usually works)

URL contains twitter.com / x.com:
  yt-dlp (usually works)

Any other URL:
  yt-dlp (covers 1800+ extractors)
  yt-dlp fails? → you-get (80+ sites, different extraction logic)
```

## Fallback Chain

When the primary tool fails, try the next option:

```
1. yt-dlp (standard)
   ↓ fails?
2. yt-dlp --cookies-from-browser chrome (auth/age-restricted)
   ↓ fails?
3. yt-dlp --geo-bypass (geo-restricted)
   ↓ fails?
4. Platform-specific tool (BBDown / lux / you-get)
   ↓ fails?
5. Report error with diagnostic info
```

## Advanced Usage

**List available formats** (before downloading):
```bash
yt-dlp --list-formats "$URL"
```

**Download specific format** (by format ID):
```bash
yt-dlp -f "FORMAT_ID" -o "$OUTPUT_DIR/%(title)s.%(ext)s" "$URL"
```

**Download with aria2c acceleration** (2-5x faster):
```bash
yt-dlp --downloader aria2c --downloader-args aria2c:"-x 16 -s 16" "$URL"
```

**Bilibili with BBDown** (when yt-dlp fails):
```bash
BBDown "$URL" -tv --work-dir "$OUTPUT_DIR"
```

**Chinese platforms with lux**:
```bash
lux -o "$OUTPUT_DIR" "$URL"
```

**Extract audio from already-downloaded video**:
```bash
ffmpeg -i "$VIDEO_FILE" -vn -acodec libmp3lame -q:a 2 "${VIDEO_FILE%.*}.mp3"
```

**Local transcription** (when no subtitles exist):
```bash
# Requires: pip install faster-whisper
python3 -c "
from faster_whisper import WhisperModel
model = WhisperModel('base', compute_type='int8')
segments, _ = model.transcribe('$AUDIO_FILE')
for seg in segments:
    m, s = divmod(int(seg.start), 60)
    print(f'[{m}:{s:02d}] {seg.text}')
"
```

## Combine with Other iopho Skills

```
# 1. Search for videos
/iopho-searching-videos SaaS product demo under 30s

# 2. Download the best match
/iopho-getting-videos https://youtube.com/watch?v=... --mode all

# 3. Analyze into storyboard
/iopho-analyzing-videos ./video.mp4
```

## Tips

- For YouTube shorts, the same URL format works with yt-dlp
- Use `--match-filter "duration<60"` during search (in iopho-searching-videos) to pre-filter
- `--write-info-json` creates a `.info.json` file that iopho-analyzing-videos can use for metadata
- For Bilibili, login cookies help access higher quality: `yt-dlp --cookies-from-browser chrome`
- Use `--no-playlist` to download a single video from a playlist URL
