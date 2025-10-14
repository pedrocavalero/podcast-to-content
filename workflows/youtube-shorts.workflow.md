# YouTube Video to Shorts Workflow

This document outlines the step-by-step process for downloading a YouTube video and its subtitles, analyzing the content to find valuable segments, creating YouTube Shorts from those segments, and generating metadata for a shorts channel.

**Executor:** Gemini CLI

---

### **Step 1: Initialization**

1.  **Ask the user for the YouTube video URL.**
    *   Store this value as `YOUTUBE_URL`.
2.  **Ask the user for their website URL.**
    *   Store this value as `USER_WEBSITE`.
3.  **Extract the video ID** from the `YOUTUBE_URL`.
    *   Store this value as `VIDEO_ID`.
4.  **Create a directory** named `shorts-{VIDEO_ID}` to store all generated assets.

### **Step 2: Video and Subtitle Download**

1.  **Check if video and subtitle already exist in the shorts directory.**
    *   Before downloading, check if a video file (`.mp4` or `.mkv`) and a `.srt` file exist in the `shorts-{VIDEO_ID}` directory.
    *   If both video (mp4 or mkv) and srt exist, skip to Step 3.
2.  **Check if video and subtitle exist in the cuts directory and move them.**
    *   If a video file (`.mp4` or `.mkv`) and a `.srt` file exist in the `cuts-{VIDEO_ID}` directory:
        *   Move the video file: `mv "cuts-{VIDEO_ID}/*.{mp4,mkv}" "shorts-{VIDEO_ID}/"`
        *   Move the `.srt` file: `mv "cuts-{VIDEO_ID}/*.srt" "shorts-{VIDEO_ID}/"`
        *   Skip to Step 3.
3.  **Execute the download script.**
    *   Run the command: `source .venv/bin/activate && yt-dlp -P shorts-{VIDEO_ID} --write-auto-subs --sub-format srt "{YOUTUBE_URL}"`
4.  **Note**:
    *   In case of error and the video or subtitles are not downloaded, stop the workflow.

### **Step 3: Content Analysis & Cut Point Identification**

1.  **Read the subtitle file** from `shorts-{VIDEO_ID}/*.srt`.
2.  **Analyze the transcript to identify 20 interesting and valuable cuts** for a developer audience. Each cut should be between 30 and 55 seconds long *after* a 2.0x speed increase (longer is preffered). Make sure the cuts has very interesting content.
3.  **For each cut, define the following:**
    *   Start time (`start_time`)
    *   End time (`end_time`)
    *   A catchy and descriptive title (`title`) - *Consider adding #Shorts or #YouTubeShorts here.*
    *   A concise and engaging `description` of the cut's content. The description must:
        *   Be brief and to the point, capturing attention quickly.
        *   Include relevant keywords and 2-3 highly relevant hashtags (e.g., #Programming #Tech #Developers).
        *   Mention the original video's name and provide the `YOUTUBE_URL`.
        *   Include a clear and concise call-to-action with a link to the user's website (`USER_WEBSITE`).
        *   Avoid timestamps, as they are less critical for short-form content.

### **Step 4: Shorts Metadata Generation**

1.  **Create a new file** named `shorts-{VIDEO_ID}/shorts.md`.
2.  **For each of the 20 cuts, add the following information** to the `shorts.md` file in a YouTube-friendly format:

    ```
    ## {title}

    **Start and End time:**
    Start Time: {start_time}
    End Time: {end_time}
    Name of the short file: short{number}.mp4

    **Description:**

    {description}

    ---
    ```

### **Step 5: Video Cutting and Speed Adjustment**

1.  **For each of the 20 cuts, execute the video processing script:**
    *   `python3 scripts/generate_short.py {VIDEO_ID} "shorts-{VIDEO_ID}/*.{mkv,mp4}" "shorts-{VIDEO_ID}/*.srt" {N} {start_time} {end_time} "{title}"`
    *   Where `{N}` is the cut number (1-20).


### **Step 6: Video Upload**

1.  **For each cut, upload the video to YouTube:**
    *   Run the command: `source .venv/bin/activate && python scripts/upload_youtube_short.py --file "shorts-{VIDEO_ID}/short{N}.mp4" --title "{title} #Shorts" --description "{description}"`
    *   Note: The title now includes `#Shorts` to help YouTube categorize it.

### **Step 7: Completion**

1.  **Notify the user** that the process is complete and all video shorts and the metadata file have been created and uploaded in the `shorts-{VIDEO_ID}` directory.
