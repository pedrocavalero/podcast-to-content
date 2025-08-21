# YouTube Video to Cuts Workflow

This document outlines the step-by-step process for downloading a YouTube video and its subtitles, analyzing the content to find valuable segments, creating video cuts from those segments, and generating metadata for a cuts channel.

**Executor:** Gemini CLI

---

### **Step 1: Initialization**

1.  **Ask the user for the YouTube video URL.**
    *   Store this value as `YOUTUBE_URL`.
2.  **Extract the video ID** from the `YOUTUBE_URL`.
    *   Store this value as `VIDEO_ID`.
3.  **Create a directory** named `cuts-{VIDEO_ID}` to store all generated assets.

### **Step 2: Video and Subtitle Download**

1.  **Execute the download script.**
    *   Run the command: `source .venv/bin/activate && yt-dlp -P cuts-{VIDEO_ID} --write-auto-subs --sub-format srt "{YOUTUBE_URL}"`
2.  **Note**:
    *   In case of error and the video or subtitles are not downloaded, stop the workflow.

### **Step 3: Content Analysis & Cut Point Identification**

1.  **Read the subtitle file** from `cuts-{VIDEO_ID}/*.srt`.
2.  **Analyze the transcript to identify 5 interesting and valuable cuts** for a developer audience. Each cut should be between 5 and 10 minutes long.
3.  **For each cut, define the following:**
    *   Start time (`start_time`)
    *   End time (`end_time`)
    *   A catchy and descriptive title (`title`)
    *   A two-paragraph summary of the cut's content (`description`). Always mention the name of the Video and the link to the video this cut came from.

### **Step 4: Cuts Metadata Generation**

1.  **Create a new file** named `cuts-{VIDEO_ID}/cuts.md`.
2.  **For each of the 5 cuts, add the following information** to the `cuts.md` file in a YouTube-friendly format:

    ```
    ## {title}

    **Start and End time:**
    Start Time: {start_time}
    End Time: {end_time}
    Name of the cut file: cut{number}.mp4

    **Description:**

    {description}

    --- 
    ```

### **Step 5: Video Cutting**

1.  **For each of the 5 cuts, execute the following command:**
    *   `ffmpeg -i "cuts-{VIDEO_ID}/*.mp4" -ss {start_time} -to {end_time} -c copy "cuts-{VIDEO_ID}/cut{N}.mp4"`
    *   Where `{N}` is the cut number (1-5).

### **Step 6: Completion**

1.  **Notify the user** that the process is complete and all video cuts and the metadata file have been created in the `cuts-{VIDEO_ID}` directory.
