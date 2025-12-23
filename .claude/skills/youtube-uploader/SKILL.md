---
name: youtube-uploader
description: Uploads videos to YouTube with metadata (title, description) and custom thumbnails. Supports resumable uploads with progress tracking. Videos are uploaded as private by default. Use when publishing video content to YouTube.
allowed-tools: [Bash, Read]
---

# YouTube Uploader

## Overview

This skill uploads videos to YouTube using the YouTube Data API v3. It handles video metadata, thumbnail uploads, OAuth authentication, and provides progress tracking for large file uploads.

## Features

- **Video Upload**: Upload videos in various formats (MP4, MOV, AVI, etc.)
- **Metadata Management**: Set title, description, and category
- **Thumbnail Upload**: Attach custom thumbnails automatically
- **Resumable Uploads**: Handle large files with progress tracking
- **OAuth Authentication**: Secure authentication with credential caching
- **Privacy Control**: Videos uploaded as private by default
- **Progress Tracking**: Real-time upload percentage display
- **Video ID Return**: Provides video ID and URL after successful upload

## Instructions

### Step 1: Prepare Upload Parameters

Gather the following information:
1. **Video file path**: Full path to the video file
2. **Title**: Video title (max 100 characters for optimal display)
3. **Description**: Video description (supports markdown, links, timestamps)
4. **Thumbnail path** (optional): Path to thumbnail image (1280x720 recommended)

### Step 2: Format Description

Descriptions can be provided in two ways:

**Inline Description** (for short descriptions):
```bash
--description "This is my video description"
```

**Description File** (for long descriptions with formatting):
1. Create a text file with the description
2. Use `--description_file` parameter
3. The file is read and used as description

### Step 3: Execute Upload

**Basic Upload** (without thumbnail):
```bash
uv run python .claude/skills/youtube-uploader/scripts/upload_youtube_video.py \
  --file "{video_path}" \
  --title "{title}" \
  --description "{description}"
```

**Upload with Thumbnail**:
```bash
uv run python .claude/skills/youtube-uploader/scripts/upload_youtube_video.py \
  --file "{video_path}" \
  --title "{title}" \
  --description "{description}" \
  --thumbnail "{thumbnail_path}"
```

**Upload with Description File**:
```bash
uv run python .claude/skills/youtube-uploader/scripts/upload_youtube_video.py \
  --file "{video_path}" \
  --title "{title}" \
  --description_file "{description_file_path}" \
  --thumbnail "{thumbnail_path}"
```

### Step 4: Handle Authentication

**First-time authentication**:
1. Script outputs OAuth authorization URL
2. User visits URL in browser
3. User grants permissions to YouTube account
4. User copies authorization code
5. User pastes code into terminal
6. Credentials saved to `credentials.json` for future use

**Subsequent uploads**:
- Credentials are automatically reused from `credentials.json`
- No user interaction needed unless credentials expire

### Step 5: Monitor Progress

During upload:
- Progress percentage is displayed
- Wait for completion message
- Video ID and URL are returned

### Step 6: Capture Video ID

After successful upload:
```
Video id "ABC123XYZ" was successfully uploaded.
Video URL: https://www.youtube.com/watch?v=ABC123XYZ
```

Save the video ID for subsequent operations:
- Scheduling with youtube-video-updater skill
- Adding to playlists
- Updating metadata later

## Input Parameters

- **--file** (required): Path to video file to upload
- **--title** (required): Video title
- **--description** (optional): Video description text
- **--description_file** (optional): Path to file containing description
- **--thumbnail** (optional): Path to thumbnail image (JPG/PNG)

**Note**: Either `--description` or `--description_file` must be provided.

## Output

- **Video ID**: Unique identifier for the uploaded video
- **Video URL**: Direct link to watch the video
- **Upload Progress**: Percentage completion during upload
- **Thumbnail Status**: Confirmation if thumbnail uploaded successfully

## Examples

### Example 1: Upload Video Cut with Thumbnail
**User Request**: "Upload cut1.mp4 with title and description"

**Given**:
- File: `cuts-SDeHHMvq9NE/cut1.mp4`
- Title: "From Code to Research: The Unexpected Career Path"
- Description: (multi-line text from workflow)
- Thumbnail: `cuts-SDeHHMvq9NE/cut1_thumbnail_1280x720.png`

**Action**:
```bash
uv run python .claude/skills/youtube-uploader/scripts/upload_youtube_video.py \
  --file "cuts-SDeHHMvq9NE/cut1.mp4" \
  --title "From Code to Research: The Unexpected Career Path" \
  --description "$(cat <<'EOF'
Ever wondered how developers transition into research? This fascinating journey takes you from the Brazilian Air Force to academia in Italy!

Join Eduardo as he shares his unexpected path from software developer to PhD researcher. Discover how working on test code refactoring during the early agile movement sparked a passion for research, and learn what it's really like to combine teaching, supervising students, and exploring cutting-edge software engineering topics.

Key moments:
- 00:45 From military developer to academic researcher - the unconventional career switch
- 03:15 Why falling in love with research happened during PhD, not before
- 05:30 The freedom to explore new technologies vs being stuck with legacy systems in industry
- 07:45 Software architecture as a specialization: from code to people

Watch the full conversation: https://www.youtube.com/watch?v=SDeHHMvq9NE

Want to level up your software engineering skills? Visit https://pedrocavalero.com for more insights!
EOF
)" \
  --thumbnail "cuts-SDeHHMvq9NE/cut1_thumbnail_1280x720.png"
```

### Example 2: Batch Upload Multiple Cuts
**User Request**: "Upload all 5 video cuts with their metadata"

**Action**:
For each cut (1-5):
1. Read title and description from `cuts.md`
2. Upload video with corresponding thumbnail
3. Save returned video ID
4. Proceed to next cut

```bash
# Cut 1
uv run python .claude/skills/youtube-uploader/scripts/upload_youtube_video.py \
  --file "cuts/cut1.mp4" \
  --title "{title_1}" \
  --description "{description_1}" \
  --thumbnail "cuts/cut1_thumbnail_1280x720.png"

# Cut 2
uv run python .claude/skills/youtube-uploader/scripts/upload_youtube_video.py \
  --file "cuts/cut2.mp4" \
  --title "{title_2}" \
  --description "{description_2}" \
  --thumbnail "cuts/cut2_thumbnail_1280x720.png"
# ... continue for all cuts
```

### Example 3: Upload with Description File
**User Request**: "Upload with a pre-written description from a file"

**Action**:
1. Create `description.txt` with formatted content
2. Upload using `--description_file`:
```bash
uv run python .claude/skills/youtube-uploader/scripts/upload_youtube_video.py \
  --file "my-video.mp4" \
  --title "My Awesome Video" \
  --description_file "description.txt" \
  --thumbnail "thumbnail.png"
```

### Example 4: Simple Upload without Thumbnail
**User Request**: "Quick upload without custom thumbnail"

**Action**:
```bash
uv run python .claude/skills/youtube-uploader/scripts/upload_youtube_video.py \
  --file "video.mp4" \
  --title "My Video Title" \
  --description "A brief description of my video"
```

## Requirements

- Python 3.9+ with uv installed
- Google Cloud Project with YouTube Data API v3 enabled
- OAuth 2.0 Client ID credentials (Desktop app type)
- `client_secret.json` in project root directory
- Dependencies installed via `uv sync`
- Valid video file in supported format
- Internet connection with sufficient upload bandwidth

## Video Requirements

**Supported Formats**:
- MP4 (recommended)
- MOV
- AVI
- WMV
- FLV
- 3GP
- MPEG

**File Size**: Up to 256 GB or 12 hours (whichever is less)

**Recommended Settings**:
- Resolution: 1920x1080 (1080p) or 1280x720 (720p)
- Frame Rate: 30fps or 60fps
- Codec: H.264
- Audio: AAC, 128kbps or higher

## Thumbnail Requirements

**Specifications**:
- Resolution: 1280x720 pixels (16:9 aspect ratio)
- Format: JPG, PNG, BMP, or GIF
- File Size: Under 2MB
- Minimum Width: 640 pixels

**Best Practices**:
- Use high-contrast text
- Include faces for better engagement
- Keep important elements in center
- Test readability at small sizes

## Privacy Settings

Videos are uploaded as **private** by default (line 51 in script):
- **Private**: Only you and people you choose can watch
- **Unlisted**: Anyone with the link can watch
- **Public**: Everyone can search for and watch

To change default privacy, modify the script or use YouTube Studio after upload.

## Category ID Reference

Default category is **28** (Science & Technology). Common categories:

- 1: Film & Animation
- 2: Autos & Vehicles
- 10: Music
- 15: Pets & Animals
- 17: Sports
- 19: Travel & Events
- 20: Gaming
- 22: People & Blogs
- 23: Comedy
- 24: Entertainment
- 25: News & Politics
- 26: Howto & Style
- 27: Education
- 28: Science & Technology (default)

## Error Handling

Common errors and solutions:

- **Missing description**: Provide either `--description` or `--description_file`
- **File not found**: Verify video and thumbnail paths are correct
- **Authentication failed**: Delete `credentials.json` and re-authenticate
- **Quota exceeded**: YouTube API has daily upload quotas, wait 24 hours
- **Invalid video format**: Convert video to supported format
- **Thumbnail too large**: Resize to under 2MB
- **Network error**: Check internet connection, upload may auto-resume

## Performance Tips

- Use resumable uploads for files > 100MB (handled automatically)
- Upload during off-peak hours for faster speeds
- Compress videos before upload if file size is very large
- Use `--description_file` for complex descriptions to avoid shell escaping issues
- Cache credentials by keeping `credentials.json` (don't delete unless needed)

## Security Notes

- **credentials.json**: Contains OAuth tokens, keep secure, don't commit to git
- **client_secret.json**: Contains OAuth client credentials, keep private
- Both files should be in `.gitignore`
- Tokens expire after ~1 hour, refresh tokens last longer
- Revoke access in Google Account settings if needed

## Integration with Other Skills

After uploading, use these skills for further management:

**youtube-video-updater**:
- Schedule publication date
- Add to playlists
- Update metadata

**youtube-thumbnail-generator**:
- Generate thumbnails before upload
- Create consistent branding

## Notes

- Videos upload as private to prevent accidental public publishing
- Video processing on YouTube may take several minutes
- High-quality videos take longer to process
- Thumbnails can be changed later via YouTube Studio
- Descriptions support limited HTML and markdown
- Include timestamps in format `00:00` for chapter markers
- First 2-3 lines of description appear in search results
- Add links, hashtags, and calls-to-action in descriptions
- Video ID is permanent and never changes
