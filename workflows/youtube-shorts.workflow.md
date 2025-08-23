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
2.  **Analyze the transcript to identify 10 interesting and valuable cuts** for a developer audience. Each cut should be between 30 and 50 seconds long *after* a 1.5x speed increase.
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
2.  **For each of the 10 cuts, add the following information** to the `shorts.md` file in a YouTube-friendly format:

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

1.  **For each of the 10 cuts, execute the following command:**
    *   `ffmpeg -i "shorts-{VIDEO_ID}/*.mkv" -ss {start_time} -to {end_time} -vf "scale=-1:1920,crop=1080:1920,setpts=PTS/1.5" -af "atempo=1.5" -c:a aac -b:a 128k "shorts-{VIDEO_ID}/short{N}.mp4"`
    *   Where `{N}` is the cut number (1-10).
    *   `-vf "scale=-1:1920,crop=1080:1920"` scales the video to a height of 1920 pixels, maintaining aspect ratio, and then crops the center 1080 pixels of width to create a vertical video.
    *   `-c:a aac -b:a 128k` is added to ensure audio is re-encoded to AAC, which is widely compatible, and to set a bitrate. This is important when changing video speed.

### **Step 6: Thumbnail Generation and Resizing**

1.  **For each cut, generate a thumbnail with a prompt that clearly describes the desired output:**
    *   Create a variable `PROMPT` with the following content: "Generate a YouTube Short thumbnail for a video about software development. The thumbnail must prominently feature the text: '{title}'. The design should be eye-catching, modern, and relevant to the video's content to maximize audience engagement. The image should be interesting enough to make a developer want to click on it. The image should have a vertical aspect ratio suitable for YouTube Shorts."
    *   Run the command: `source .venv/bin/activate && python scripts/generate_image.py "{PROMPT}" "shorts-{VIDEO_ID}/short{N}_thumbnail_raw.png" --model "gpt-image-1" --size "1024x1536"`
    NOTE: Do not change the model or the size! The size is set for a vertical image.
2.  **Resize the generated thumbnail to YouTube Shorts recommended size (720x1280):**
    *   Run the command: `source .venv/bin/activate && python scripts/resize_image.py "shorts-{VIDEO_ID}/short{N}_thumbnail_raw.png" "shorts-{VIDEO_ID}/short{N}_thumbnail_720x1280.png" --width 720 --height 1280`

### **Step 7: Video Upload**

1.  **For each cut, upload the video to YouTube with its generated thumbnail:**
    *   Run the command: `source .venv/bin/activate && python scripts/upload_youtube_short.py --file "shorts-{VIDEO_ID}/short{N}.mp4" --title "{title} #Shorts" --description "{description}" --thumbnail "shorts-{VIDEO_ID}/short{N}_thumbnail_720x1280.png"`
    *   Note: The title now includes `#Shorts` to help YouTube categorize it.

### **Step 8: Completion**

1.  **Notify the user** that the process is complete and all video shorts, thumbnails, and the metadata file have been created and uploaded in the `shorts-{VIDEO_ID}` directory.
