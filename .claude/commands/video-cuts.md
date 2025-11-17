Execute the YouTube Video to Cuts workflow from `workflows/video-cuts.workflow.md` for YouTube URL: {{youtube_url}} with {{num_cuts}} cuts, using website: {{user_website}}.

Follow each step in the workflow carefully:

1. Extract the video ID from the YouTube URL
2. Create the `cuts-{VIDEO_ID}` directory
3. Download video and subtitles: `yt-dlp -P cuts-{VIDEO_ID} --write-auto-subs --sub-format srt "{YOUTUBE_URL}"`
4. Analyze the subtitle file to identify the specified number of interesting cuts (5-10 minutes each)
5. Generate cuts metadata file with titles and descriptions
6. **Execute in parallel for each cut:**
   - Cut the videos with 2-second fade-in and fade-out effects (two-step process)
   - Generate and resize thumbnails (1536x1024 -> 1280x720)
7. Upload all cuts to YouTube with thumbnails

**Performance Optimization:**
- After generating the cuts metadata (step 5), execute video cutting and thumbnail generation in parallel
- All cutting commands can run simultaneously, and all thumbnail generation commands can run simultaneously
- This significantly reduces total processing time

Important:
- Stop the workflow if any critical step fails (download, cutting, thumbnail generation)
- Each cut should be 5-10 minutes long
- Descriptions must be engaging with emojis and timestamps (adjusted to cut time, not original video time)
- Include at least 3 key moments with timestamps in each description
- Always mention the original video name and URL
- Include a call-to-action with the user's website
- Use model "gpt-image-1" and size "1536x1024" for thumbnail generation (DO NOT CHANGE!)
- All outputs go to `cuts-{VIDEO_ID}` directory
