---
name: youtube-downloader
description: Downloads YouTube videos and subtitles using yt-dlp. Supports video-only, subtitles-only, or both. Handles auto-generated and manual captions. Use when downloading content from YouTube for processing, transcription, or analysis.
allowed-tools: [Bash, Read, Glob]
---

# YouTube Downloader

## Overview

This skill downloads YouTube videos and their subtitles using yt-dlp, a powerful command-line tool. It supports flexible download options including video-only, subtitles-only, or combined downloads.

## Features

- **Video Download**: Download videos in various formats and quality
- **Subtitle Download**: Retrieve auto-generated or manual subtitles
- **Format Conversion**: Convert subtitles to SRT format automatically
- **Browser Cookies**: Support for cookie extraction from browsers (Chrome, Firefox, Safari)
- **Smart Checking**: Verify existing files before re-downloading
- **Multiple Formats**: Support for .mp4, .mkv video formats and .srt subtitles

## Instructions

### Step 1: Prepare Download Parameters

1. **Get the YouTube URL** from user or extract from video ID
   - Format: `https://www.youtube.com/watch?v={VIDEO_ID}`

2. **Determine download directory**
   - Use workflow-specific directory (e.g., `{DATE}-{VIDEO_ID}/download`)
   - Or ask user for custom directory

3. **Decide download type**:
   - **Full**: Video + Subtitles
   - **Subtitles Only**: Just the captions (faster, for transcription)
   - **Video Only**: Just the video file

### Step 2: Check for Existing Files

Before downloading, verify if files already exist:

```bash
# Check for video files
ls {DOWNLOAD_DIR}/*.mp4 {DOWNLOAD_DIR}/*.mkv 2>/dev/null

# Check for subtitle files
ls {DOWNLOAD_DIR}/*.srt 2>/dev/null
```

If both exist and user hasn't requested re-download, skip to completion.

### Step 3: Execute Download

**Full Download (Video + Subtitles)**:
```bash
source .venv/bin/activate && yt-dlp \
  -P {DOWNLOAD_DIR} \
  --write-auto-subs \
  --sub-format srt \
  "{YOUTUBE_URL}"
```

**Subtitles Only** (faster, for transcription workflows):
```bash
source .venv/bin/activate && yt-dlp \
  -P {DOWNLOAD_DIR} \
  --write-auto-sub \
  --sub-lang en \
  --skip-download \
  --convert-subs srt \
  --cookies-from-browser chrome \
  "https://www.youtube.com/watch?v={VIDEO_ID}"
```

**Video Only**:
```bash
source .venv/bin/activate && yt-dlp \
  -P {DOWNLOAD_DIR} \
  --no-write-subs \
  "{YOUTUBE_URL}"
```

### Step 4: Verify Download

After download completes:
1. Check that files exist in `{DOWNLOAD_DIR}`
2. List downloaded files to user
3. Verify subtitle file is not empty (if downloaded)
4. Return file paths for next steps in workflow

### Step 5: Error Handling

If download fails:
- Check network connectivity
- Verify YouTube URL is valid
- Try alternative browser for cookies (`firefox`, `safari`)
- Check if video is private/restricted
- Verify yt-dlp is installed and updated

## Input Parameters

- **youtube_url** (required): Full YouTube URL or video ID
- **download_dir** (required): Directory to save downloaded files
- **download_type** (optional): "full", "subtitles", or "video" (default: "full")
- **subtitle_lang** (optional): Language code for subtitles (default: "en")
- **browser** (optional): Browser for cookie extraction (default: "chrome")

## Output Files

- **Video**: `{DOWNLOAD_DIR}/*.mp4` or `*.mkv`
- **Subtitles**: `{DOWNLOAD_DIR}/*.srt`
- **Metadata**: `{DOWNLOAD_DIR}/*.info.json` (optional)

## Examples

### Example 1: Download for Video Cuts Workflow
**User Request**: "Download video SDeHHMvq9NE with subtitles"

**Action**:
1. Create directory: `25-11-16-SDeHHMvq9NE/download`
2. Check if files exist
3. If not, run:
```bash
source .venv/bin/activate && yt-dlp \
  -P 25-11-16-SDeHHMvq9NE/download \
  --write-auto-subs \
  --sub-format srt \
  "https://www.youtube.com/watch?v=SDeHHMvq9NE"
```
4. Verify downloads and return paths

### Example 2: Subtitles Only for Blog Workflow
**User Request**: "Get subtitles for transcription of video ABC123"

**Action**:
```bash
source .venv/bin/activate && yt-dlp \
  -P 25-12-23-ABC123/download \
  --write-auto-sub \
  --sub-lang en \
  --skip-download \
  --convert-subs srt \
  --cookies-from-browser chrome \
  "https://www.youtube.com/watch?v=ABC123"
```

### Example 3: Re-download with Different Browser
**User Request**: "Download failed with Chrome, try Firefox"

**Action**:
```bash
source .venv/bin/activate && yt-dlp \
  -P {DOWNLOAD_DIR} \
  --write-auto-sub \
  --sub-lang en \
  --skip-download \
  --convert-subs srt \
  --cookies-from-browser firefox \
  "{YOUTUBE_URL}"
```

### Example 4: Batch Download
**User Request**: "Download these 3 videos: [URLs]"

**Action**:
For each URL:
1. Extract video ID
2. Create download directory
3. Check existing files
4. Download if needed
5. Report status

## Requirements

- **yt-dlp**: Installed and accessible in PATH
  - Install: `pip install yt-dlp` (usually in `.venv`)
  - Or: `brew install yt-dlp` (macOS)
  - Or: `apt install yt-dlp` (Linux)

- **Browser** (for subtitles-only mode): Chrome, Firefox, or Safari
- **Network**: Active internet connection
- **Storage**: Sufficient disk space (videos can be large)

## Browser Cookie Support

yt-dlp can extract cookies from browsers to access age-restricted or private videos:

- **Chrome**: `--cookies-from-browser chrome`
- **Firefox**: `--cookies-from-browser firefox`
- **Safari**: `--cookies-from-browser safari`
- **Edge**: `--cookies-from-browser edge`

**Note**: Browser must be closed during cookie extraction on some systems.

## Advanced Options

**Quality Selection**:
```bash
yt-dlp -f "best[height<=1080]" "{YOUTUBE_URL}"  # Max 1080p
yt-dlp -f "bestvideo+bestaudio" "{YOUTUBE_URL}"  # Best quality
```

**Playlist Download**:
```bash
yt-dlp --yes-playlist "{PLAYLIST_URL}"  # Download all videos in playlist
```

**Custom Filename**:
```bash
yt-dlp -o "{DOWNLOAD_DIR}/%(title)s.%(ext)s" "{YOUTUBE_URL}"
```

## Error Handling

Common errors and solutions:

- **HTTP Error 429**: Rate limited, wait and retry
- **Video unavailable**: Check URL, video may be deleted/private
- **Cookie extraction failed**: Close browser and retry
- **Subtitle not available**: Try `--write-sub` for manual subs
- **Disk space**: Clear old downloads or increase storage

## Notes

- Videos are downloaded in best available quality by default
- Auto-generated subtitles may have inaccuracies
- Some videos may not have subtitles available
- Download time depends on video length and internet speed
- Check existing files to avoid unnecessary re-downloads
- yt-dlp is actively maintained and frequently updated

## Performance Tips

- Use `--skip-download` when only subtitles are needed
- Check for existing files before downloading
- Use `--concurrent-fragments N` for faster downloads
- Consider `--limit-rate` if bandwidth is limited
- Use `--playlist-items` to download specific playlist items
