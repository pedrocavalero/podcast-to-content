---
name: youtube-thumbnail-generator
description: Generates AI-powered YouTube thumbnails with face from reference photo, custom expressions, backgrounds, and text overlays. Automatically resizes to YouTube's recommended 1280x720 format. Use when creating thumbnails for YouTube videos or updating existing video thumbnails.
allowed-tools: [Bash, Read]
---

# YouTube Thumbnail Generator

## Overview

This skill generates professional YouTube thumbnails using Google's Gemini AI with a reference photo. It creates eye-catching thumbnails with custom facial expressions, backgrounds, and text overlays optimized for YouTube's platform.

## Features

- **AI-Powered Generation**: Uses Gemini 2.5 Flash Image model
- **Reference Photo Integration**: Crops and zooms on face from provided reference image
- **Custom Expressions**: Generates appropriate facial expressions based on video title
- **Dynamic Backgrounds**: Creates relevant background scenes matching the topic
- **Text Overlays**: Adds bold, high-contrast text from the title
- **Auto-Resizing**: Automatically resizes to YouTube's recommended 1280x720 dimensions
- **Dual Output**: Generates both raw (16:9) and resized versions

## Instructions

### Step 1: Analyze the Title

When a user requests a thumbnail, analyze the video title to determine:
1. **Expression**: Facial expression matching the emotion (shocked, happy, serious, confused, etc.)
2. **Background**: Visual setting symbolizing the topic (code screen, futuristic city, office, etc.)
3. **Text**: Short, punchy text overlay (max 3-4 words) from the title

### Step 2: Generate the Thumbnail

1. **Construct the prompt** using this template:
   ```
   Create a YouTube thumbnail using the provided reference image for a video titled '{title}'.
   1. Focus: Crop and zoom in on the face from the reference photo.
   2. Expression: {generated_expression}.
   3. Background: {generated_background}.
   4. Text: Include the text '{generated_text}' in large, bold, high-contrast typography.
   5. Style: High-quality, 4k, professional YouTube thumbnail style, vibrant colors, 16:9 aspect ratio.
   ```

2. **Execute the generation command**:
   ```bash
   uv run python .claude/skills/youtube-thumbnail-generator/scripts/generate_image_nano_banana.py \
     "{prompt}" \
     "{output_dir}/thumbnail_raw.png" \
     --aspect_ratio "16:9" \
     --reference_image "workflows/Foto-3x4.jpg"
   ```

3. **Resize to YouTube dimensions**:
   ```bash
   uv run python .claude/skills/youtube-thumbnail-generator/scripts/resize_image.py \
     "{output_dir}/thumbnail_raw.png" \
     "{output_dir}/thumbnail_1280x720.png" \
     --width 1280 \
     --height 720
   ```

### Step 3: Return the Results

Inform the user that:
- Raw thumbnail saved to: `{output_dir}/thumbnail_raw.png`
- YouTube-ready thumbnail saved to: `{output_dir}/thumbnail_1280x720.png`

## Input Parameters

- **title** (required): The YouTube video title
- **output_dir** (required): Directory to save generated thumbnails
- **reference_image** (optional): Path to reference photo (default: `workflows/Foto-3x4.jpg`)
- **custom_expression** (optional): Override auto-generated expression
- **custom_background** (optional): Override auto-generated background
- **custom_text** (optional): Override auto-generated text

## Output Files

- `{output_dir}/thumbnail_raw.png`: Original generated image (16:9 aspect ratio)
- `{output_dir}/thumbnail_1280x720.png`: Resized for YouTube (1280x720 pixels)

## Examples

### Example 1: Basic Usage
**User Request**: "Generate a thumbnail for my video titled 'Why Microservices Failed'"

**Action**:
1. Analyze title → Expression: "disappointed/serious", Background: "broken microservices architecture diagram", Text: "Why They Failed"
2. Generate raw thumbnail
3. Resize to 1280x720

### Example 2: Updating Existing Video
**User Request**: "Create a new thumbnail for the video 'React Hooks Explained'"

**Action**:
1. Analyze title → Expression: "excited/teaching", Background: "React code on screen with hooks", Text: "Hooks Explained"
2. Generate thumbnails in specified directory
3. Provide paths for upload to YouTube

### Example 3: Batch Generation
**User Request**: "Generate thumbnails for these 5 video titles: [list]"

**Action**:
1. For each title, analyze and determine expression/background/text
2. Generate thumbnails sequentially
3. Save to numbered directories or with title-based filenames

## Requirements

- Python 3.9+ with uv installed
- Google API key configured in `.env` file (GOOGLE_API_KEY)
- Reference image at `workflows/Foto-3x4.jpg` (or custom path)
- Dependencies installed via `uv sync`

## Error Handling

- If GOOGLE_API_KEY is missing, inform user to set it in `.env`
- If reference image not found, proceed with text-only generation
- If quota exceeded (429 error), inform user about rate limits
- If generation fails, provide error details and suggest retrying

## Notes

- Thumbnails are optimized for YouTube's 16:9 aspect ratio
- Text should be short and punchy for maximum impact
- High contrast colors are automatically applied for readability
- The skill uses the Gemini 2.5 Flash Image model by default
