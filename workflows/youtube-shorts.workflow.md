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
4.  **Get the current date** in `yy-mm-dd` format.
    *   Store this value as `DATE`.
5.  **Define the working directory** as `{DATE}-{VIDEO_ID}/shorts`.
    *   Store this value as `SHORTS_DIR`.
    *   Also define `CUTS_DIR` as `{DATE}-{VIDEO_ID}/cuts`.
6.  **Define the download directory** as `{DATE}-{VIDEO_ID}/download`.
    *   Store this value as `DOWNLOAD_DIR`.
7.  **Create the directories** `{SHORTS_DIR}` and `{DOWNLOAD_DIR}` (and their parent `{DATE}-{VIDEO_ID}` if needed) to store all generated assets.
8.  **When searching for files or folders, always include gitignored files.**

### **Step 2: Video and Subtitle Download**

1.  **Check if video and subtitle already exist in the download directory.**
    *   Before downloading, check if a video file (`.mp4` or `.mkv`) and a `.srt` file exist in the `{DOWNLOAD_DIR}` directory.
    *   If both video (mp4 or mkv) and srt exist, skip to Step 3.
2.  **Execute the download script.**
    *   Run the command: `source .venv/bin/activate && yt-dlp -P {DOWNLOAD_DIR} --write-auto-subs --sub-format srt "{YOUTUBE_URL}"`
3.  **Note**:
    *   In case of error and the video or subtitles are not downloaded, stop the workflow.

### **Step 3: Content Analysis & Cut Point Identification**

1.  **Read the subtitle file** from `{DOWNLOAD_DIR}/*.srt`.
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

1.  **Create a new file** named `{SHORTS_DIR}/shorts.md`.
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
    *   `python3 scripts/generate_short.py "{SHORTS_DIR}" "{DOWNLOAD_DIR}"/*.{mkv,mp4} "{DOWNLOAD_DIR}"/*.srt {N} {start_time} {end_time} "{title}"`
    *   Where `{N}` is the cut number (1-20).


### **Step 6: Video Upload**

1.  **For each cut, upload the video to YouTube:**
    *   Run the command: `source .venv/bin/activate && python scripts/upload_youtube_short.py --file "{SHORTS_DIR}/short{N}.mp4" --title "{title} #Shorts" --description "{description}"`
    *   Note: The title now includes `#Shorts` to help YouTube categorize it.

### **Step 7: Completion**

1.  **Notify the user** that the process is complete and all video shorts and the metadata file have been created and uploaded in the `{SHORTS_DIR}` directory.