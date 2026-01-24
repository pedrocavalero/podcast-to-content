---
name: video-cutter
description: Cuts video segments from source videos using ffmpeg with professional fade-in and fade-out effects. Supports precise timestamp-based cutting and batch processing. Use when extracting clips, creating highlights, or splitting videos into segments.
allowed-tools: [Bash, Read, Glob]
---

# Video Cutter

## Overview

This skill extracts video segments from source videos using ffmpeg with professional transitions. It applies 2-second fade-in and fade-out effects for smooth, polished cuts suitable for YouTube and social media.

## Features

- **Precise Cutting**: Extract segments using exact timestamps
- **Professional Transitions**: Automatic 2-second fade-in and fade-out
- **Batch Processing**: Cut multiple segments from the same source
- **Format Preservation**: Maintains video quality and audio sync
- **Clean Workflow**: Automatic cleanup of temporary files
- **Flexible Input**: Supports various video formats (.mp4, .mkv, .avi, etc.)

## Instructions

### Step 1: Gather Cut Information

For each cut, collect:
1. **Source video path**: Full path to the input video file
2. **Start time**: When the cut begins (format: `HH:MM:SS` or `MM:SS` or seconds)
3. **End time**: When the cut ends (same format as start time)
4. **Output path**: Where to save the cut video
5. **Cut number** (optional): For naming in batch operations

### Step 2: Calculate Duration

Calculate the duration for fade-out timing:
```
duration_seconds = end_time - start_time
```

**Example**:
- Start: `00:02:00` (120 seconds)
- End: `00:10:00` (600 seconds)
- Duration: `480 seconds` (8 minutes)

### Step 3: Execute the Cut with Fades

The cutting process uses a two-step approach for optimal quality:

**Step 3.1: Apply fade-in and extract segment**:
```bash
ffmpeg -y -i "{source_video_path}" \
  -ss {start_time} \
  -to {end_time} \
  -vf "fade=t=in:st=0:d=2" \
  -c:a copy \
  "{output_dir}/cut{N}_temp.mp4"
```

**Step 3.2: Apply fade-out to create final cut**:
```bash
ffmpeg -y -i "{output_dir}/cut{N}_temp.mp4" \
  -vf "fade=t=out:st={duration-2}:d=2" \
  -c:a copy \
  "{output_dir}/cut{N}.mp4"
```

**Step 3.3: Clean up temporary file**:
```bash
rm "{output_dir}/cut{N}_temp.mp4"
```

### Step 4: Verify Output

After cutting:
1. Check that final file exists
2. Verify file size is reasonable
3. Optionally check duration matches expected length
4. Return path to final cut file

### Step 5: Handle Multiple Cuts

For batch processing:
```bash
# Cut 1
ffmpeg -y -i "{source}" -ss 00:02:00 -to 00:10:00 -vf "fade=t=in:st=0:d=2" -c:a copy "cuts/cut1_temp.mp4"
ffmpeg -y -i "cuts/cut1_temp.mp4" -vf "fade=t=out:st=478:d=2" -c:a copy "cuts/cut1.mp4"
rm "cuts/cut1_temp.mp4"

# Cut 2
ffmpeg -y -i "{source}" -ss 00:18:00 -to 00:26:00 -vf "fade=t=in:st=0:d=2" -c:a copy "cuts/cut2_temp.mp4"
ffmpeg -y -i "cuts/cut2_temp.mp4" -vf "fade=t=out:st=478:d=2" -c:a copy "cuts/cut2.mp4"
rm "cuts/cut2_temp.mp4"
```

## Input Parameters

- **source_video_path** (required): Path to source video file
- **start_time** (required): Start timestamp (HH:MM:SS, MM:SS, or seconds)
- **end_time** (required): End timestamp (same format as start_time)
- **output_path** (required): Path for the output cut file
- **fade_duration** (optional): Fade effect duration in seconds (default: 2)

## Output Files

- **Final Cut**: `{output_path}/cut{N}.mp4` - The finished video segment
- **Temporary**: `{output_path}/cut{N}_temp.mp4` - Automatically deleted after processing

## Examples

### Example 1: Single Cut with Fades
**User Request**: "Cut the segment from 2:00 to 10:00 from video.mp4"

**Action**:
1. Calculate duration: 480 seconds (8 minutes)
2. Execute commands:
```bash
ffmpeg -y -i "download/video.mp4" \
  -ss 00:02:00 \
  -to 00:10:00 \
  -vf "fade=t=in:st=0:d=2" \
  -c:a copy \
  "cuts/cut1_temp.mp4"

ffmpeg -y -i "cuts/cut1_temp.mp4" \
  -vf "fade=t=out:st=478:d=2" \
  -c:a copy \
  "cuts/cut1.mp4"

rm "cuts/cut1_temp.mp4"
```

### Example 2: Multiple Cuts from Same Video
**User Request**: "Extract 5 interesting segments from this video"

**Given cuts**:
1. 00:02:00 → 00:10:00 (8 min)
2. 00:18:00 → 00:26:00 (8 min)
3. 00:14:30 → 00:23:00 (8.5 min)
4. 00:35:00 → 00:40:00 (5 min)
5. 00:40:30 → 00:48:00 (7.5 min)

**Action**:
Process each cut sequentially with proper duration calculations.

### Example 3: YouTube Shorts (Vertical Video)
**User Request**: "Cut a 45-second segment for YouTube Shorts"

**Action**:
```bash
# Apply vertical format and cut
ffmpeg -y -i "source.mp4" \
  -ss 00:05:30 \
  -to 00:06:15 \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fade=t=in:st=0:d=2" \
  -c:a copy \
  "shorts/short1_temp.mp4"

ffmpeg -y -i "shorts/short1_temp.mp4" \
  -vf "fade=t=out:st=43:d=2" \
  -c:a copy \
  "shorts/short1.mp4"

rm "shorts/short1_temp.mp4"
```

### Example 4: Custom Fade Duration
**User Request**: "Cut segment with 3-second fades"

**Action**:
Modify fade parameters:
- Fade-in: `fade=t=in:st=0:d=3`
- Fade-out: `fade=t=out:st={duration-3}:d=3`

## Requirements

- **ffmpeg**: Installed and accessible in PATH
  - Install macOS: `brew install ffmpeg`
  - Install Linux: `apt install ffmpeg`
  - Install Windows: Download from ffmpeg.org

- **Storage**: Sufficient disk space (cuts are typically large)
- **Source Video**: Valid video file in supported format

## FFmpeg Parameters Explained

- **`-y`**: Overwrite output files without asking
- **`-i`**: Input file path
- **`-ss`**: Start time (seek to position)
- **`-to`**: End time (cut until position)
- **`-vf`**: Video filter (for fade effects)
- **`-c:a copy`**: Copy audio without re-encoding (faster)
- **`fade=t=in:st=0:d=2`**: Fade in starting at 0s for 2s duration
- **`fade=t=out:st=X:d=2`**: Fade out starting at X seconds for 2s duration

## Time Format Options

ffmpeg accepts multiple time formats:

- **Seconds**: `120` (2 minutes)
- **MM:SS**: `02:30` (2 minutes 30 seconds)
- **HH:MM:SS**: `01:02:30` (1 hour 2 minutes 30 seconds)
- **Decimal**: `90.5` (90.5 seconds)

## Advanced Options

**Change Video Quality**:
```bash
ffmpeg -y -i "source.mp4" -ss 00:02:00 -to 00:10:00 \
  -vf "fade=t=in:st=0:d=2" \
  -c:v libx264 -crf 23 \  # Re-encode with quality 23
  -c:a aac -b:a 128k \     # Re-encode audio at 128kbps
  "output.mp4"
```

**Add Speed Adjustment**:
```bash
# 2x speed
-vf "setpts=0.5*PTS,fade=t=in:st=0:d=2"
-af "atempo=2.0"
```

**Extract Audio Only**:
```bash
ffmpeg -y -i "source.mp4" -ss 00:02:00 -to 00:10:00 \
  -vn -c:a copy "output.m4a"
```

## Error Handling

Common issues and solutions:

- **File not found**: Verify source video path is correct
- **Codec errors**: Try re-encoding with `-c:v libx264 -c:a aac`
- **Timing issues**: Ensure start_time < end_time
- **Permission denied**: Check write permissions on output directory
- **Out of memory**: Process fewer cuts simultaneously
- **Audio sync issues**: Remove `-c:a copy` to re-encode audio

## Performance Tips

- Use `-c:a copy` to avoid audio re-encoding (much faster)
- Process cuts sequentially for stability
- Use absolute paths to avoid path resolution issues
- Pre-calculate all durations before starting batch operations
- Monitor disk space when processing many/large cuts
- Consider using `-threads N` for faster encoding

## Notes

- Fade effects are applied to video only, audio remains untouched
- The 2-second fade is optimal for professional-looking transitions
- Temporary files are essential for proper fade-out timing
- Always verify final output file exists and has correct duration
- For very short clips (< 5 seconds), reduce fade duration
- The two-step process ensures both fades render correctly
- Audio remains perfectly synchronized with `-c:a copy`

## Quality Considerations

- Using `-c:a copy` preserves original audio quality
- Video quality may be slightly reduced due to re-encoding for fades
- For highest quality, use `-c:v libx264 -crf 18` (larger files)
- For web/YouTube, default settings are usually sufficient
- Consider target platform requirements (YouTube, Instagram, TikTok)
