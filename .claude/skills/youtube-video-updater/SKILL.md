---
name: youtube-video-updater
description: Updates existing YouTube videos by scheduling publication dates, managing playlist assignments, and updating thumbnails. Supports both playlist IDs and names. Use when updating video metadata, scheduling videos for future publication, organizing videos into playlists, or changing video thumbnails.
allowed-tools: [Bash, Read]
---

# YouTube Video Updater

## Overview

This skill updates existing YouTube videos with new scheduling, playlist assignments, and thumbnails. It uses the YouTube Data API v3 to modify video properties without re-uploading content.

## Features

- **Schedule Publication**: Set future publication dates for private videos
- **Playlist Management**: Add videos to playlists by name or ID
- **Thumbnail Updates**: Change video thumbnails with custom images
- **Flexible Input**: Supports both playlist IDs and playlist names
- **OAuth Authentication**: Secure authentication using OAuth 2.0
- **Batch Operations**: Update multiple playlists in a single command

## Current Capabilities

✅ **Supported**:
- Schedule videos for future publication (ISO 8601 format)
- Add videos to playlists (by ID or name)
- Update video thumbnails with custom images
- Automatic playlist name → ID resolution

⚠️ **Limitations**:
- Description updates: Not currently implemented (can be added via YouTube API videos.update)
- Title updates: Not currently implemented (can be added via YouTube API videos.update)

## Instructions

### Step 1: Identify the Video

Get the video ID from:
- YouTube URL: `https://www.youtube.com/watch?v={VIDEO_ID}`
- Or ask user for the video ID directly

### Step 2: Determine Update Type

**For Scheduling**:
- Get the desired publication date in ISO 8601 format
- Examples: `2025-12-25T10:00:00Z`, `2025-01-15T14:30:00-05:00`

**For Playlist Assignment**:
- Get playlist name(s) or ID(s) from user
- The script will automatically resolve names to IDs
- Playlist IDs typically start with `PL`, `UU`, or `FL`

**For Thumbnail Updates**:
- Get the path to the thumbnail image file
- Thumbnails should be 1280x720 pixels (YouTube recommended)
- Supported formats: JPG, PNG
- File size: Under 2MB

### Step 3: Execute the Update

**Schedule Only**:
```bash
uv run python .claude/skills/youtube-video-updater/scripts/update_youtube_video.py \
  --video_id {VIDEO_ID} \
  --schedule "{ISO_8601_DATETIME}"
```

**Playlist Only**:
```bash
uv run python .claude/skills/youtube-video-updater/scripts/update_youtube_video.py \
  --video_id {VIDEO_ID} \
  --playlists "{PLAYLIST_1}" "{PLAYLIST_2}"
```

**Thumbnail Only**:
```bash
uv run python .claude/skills/youtube-video-updater/scripts/update_youtube_thumbnail.py \
  --video_id {VIDEO_ID} \
  --thumbnail "{THUMBNAIL_PATH}"
```

**Schedule and Playlist**:
```bash
uv run python .claude/skills/youtube-video-updater/scripts/update_youtube_video.py \
  --video_id {VIDEO_ID} \
  --schedule "{ISO_8601_DATETIME}" \
  --playlists "{PLAYLIST_1}" "{PLAYLIST_2}"
```

### Step 4: Handle Authentication

If this is the first run or credentials are expired:
1. The script will output an OAuth authorization URL
2. User must visit the URL and grant permissions
3. User will receive an authorization code
4. Enter the code when prompted
5. Credentials are saved to `credentials_update.json` for future use

## Input Parameters

### For update_youtube_video.py:
- **--video_id** (required): The YouTube video ID
- **--schedule** (optional): ISO 8601 datetime for publication (e.g., `2025-12-25T10:00:00Z`)
- **--playlists** (optional): Space-separated list of playlist names or IDs

**Note**: At least one of `--schedule` or `--playlists` must be provided.

### For update_youtube_thumbnail.py:
- **--video_id** (required): The YouTube video ID
- **--thumbnail** (required): Path to the thumbnail image file (1280x720 recommended, under 2MB)

## Examples

### Example 1: Schedule a Video
**User Request**: "Schedule video ABC123 for Christmas Day 2025 at 10 AM UTC"

**Action**:
```bash
uv run python .claude/skills/youtube-video-updater/scripts/update_youtube_video.py \
  --video_id ABC123 \
  --schedule "2025-12-25T10:00:00Z"
```

### Example 2: Add to Playlists
**User Request**: "Add video XYZ789 to my 'Tutorial Series' and 'Best Of' playlists"

**Action**:
```bash
uv run python .claude/skills/youtube-video-updater/scripts/update_youtube_video.py \
  --video_id XYZ789 \
  --playlists "Tutorial Series" "Best Of"
```

### Example 3: Schedule and Organize
**User Request**: "Schedule video DEF456 for next Wednesday at 2 PM EST and add it to 'Weekly Updates' playlist"

**Action**:
1. Calculate next Wednesday at 2 PM EST in ISO 8601 format
2. Run:
```bash
uv run python .claude/skills/youtube-video-updater/scripts/update_youtube_video.py \
  --video_id DEF456 \
  --schedule "2025-01-15T14:00:00-05:00" \
  --playlists "Weekly Updates"
```

### Example 4: Update Thumbnail
**User Request**: "Update the thumbnail for video HqlAGSPi3jk with the image at thumbnails/thumbnail_1280x720.png"

**Action**:
```bash
uv run python .claude/skills/youtube-video-updater/scripts/update_youtube_thumbnail.py \
  --video_id HqlAGSPi3jk \
  --thumbnail "thumbnails/thumbnail_1280x720.png"
```

### Example 5: Batch Scheduling Strategy
**User Request**: "Schedule these 5 videos on Wednesdays and Saturdays at 12 PM, starting from 2025-12-25"

**Action**:
1. Calculate schedule dates following Wed/Sat pattern
2. For each video (indexed i):
   - Find next Wednesday or Saturday
   - Set time to 12:00:00
   - Run update command with calculated date

## Requirements

- Python 3.9+ with uv installed
- Google Cloud Project with YouTube Data API v3 enabled
- OAuth 2.0 Client ID credentials (Desktop app type)
- `client_secret.json` in project root directory
- Dependencies installed via `uv sync`

## Error Handling

- **No action specified**: Ensure at least `--schedule` or `--playlists` is provided
- **Playlist not found**: Script will warn and attempt to use input as ID
- **Video already in playlist**: HTTP 409 error, script continues gracefully
- **Authentication failure**: Check `client_secret.json` exists and is valid
- **Invalid video ID**: YouTube API will return 404 error
- **Thumbnail file not found**: Script will report error if thumbnail path is invalid
- **Invalid thumbnail format**: YouTube API will reject non-supported image formats
- **Thumbnail too large**: Ensure file size is under 2MB

## Notes

- Videos must be in **private** status to use scheduled publishing
- The script automatically sets privacy to private when scheduling
- Scheduled videos will automatically become public at the specified time
- Playlist names are case-insensitive when searching
- Multiple playlists can be assigned in a single command
- Both scripts use `credentials_update.json` (separate from upload credentials)
- Thumbnails should be 1280x720 pixels for best quality
- Supported thumbnail formats: JPG, PNG (under 2MB)
- Thumbnail updates take effect immediately

## Future Enhancements

Potential additions:
- Update video descriptions
- Update video titles
- Change privacy status without scheduling
- Update video tags and categories
- Bulk operations from CSV files
