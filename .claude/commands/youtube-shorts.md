Execute the YouTube Video to Shorts workflow from `workflows/youtube-shorts.workflow.md` for YouTube URL: {{youtube_url}} with {{num_shorts}} shorts, using website: {{user_website}}.

Follow each step in the workflow carefully:

1. Extract the video ID from the YouTube URL
2. Create the `shorts-{VIDEO_ID}` directory
3. Check for existing video and subtitles:
   - First check in `shorts-{VIDEO_ID}` directory
   - If not found, check and move from `cuts-{VIDEO_ID}` directory
   - If still not found, download: `yt-dlp -P shorts-{VIDEO_ID} --write-auto-subs --sub-format srt "{YOUTUBE_URL}"`
4. Analyze the subtitle file to identify the specified number of interesting cuts (30-55 seconds after 2.0x speed increase)
5. Generate shorts metadata file with titles and descriptions
6. **Execute in parallel for each short:**
   - Process video cuts with speed adjustment and subtitles using `generate_short.py`
7. Upload all shorts to YouTube with #Shorts tag

**Performance Optimization:**
- After generating the shorts metadata (step 5), execute all video processing in parallel
- All `generate_short.py` commands can run simultaneously
- This significantly reduces total processing time

Important:
- Stop the workflow if any critical step fails (download, cutting, upload)
- Each short should be 30-55 seconds long AFTER 2.0x speed increase (prefer longer cuts)
- Make sure cuts contain very interesting content
- Descriptions must be brief and engaging with 2-3 relevant hashtags
- Include original video name and URL in descriptions
- Include a call-to-action with the user's website
- Add "#Shorts" to titles for proper YouTube categorization
- Avoid timestamps in descriptions (less critical for short-form content)
- All outputs go to `shorts-{VIDEO_ID}` directory
