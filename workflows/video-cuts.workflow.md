# YouTube Video to Cuts Workflow

This document outlines the step-by-step process for downloading a YouTube video and its subtitles, analyzing the content to find valuable segments, creating video cuts from those segments, and generating metadata for a cuts channel.

**Executor:** Gemini CLI

---

### **Step 1: Initialization**

1.  **Ask the user for the YouTube video URL.**
    *   Store this value as `YOUTUBE_URL`.
2.  **Ask the user for their website URL.**
    *   Store this value as `USER_WEBSITE`.
3.  **Extract the video ID** from the `YOUTUBE_URL`.
    *   Store this value as `VIDEO_ID`.
4.  **Create a directory** named `cuts-{VIDEO_ID}` to store all generated assets.

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
    *   A detailed and engaging `description` of the cut's content. The description must:
        *   Be written in a compelling and engaging tone, using emojis to highlight key points.
        *   Include timestamps (e.g., `00:45`) for at least 3 key moments within the cut to help viewers navigate.
        *   Clearly mention the original video's name and provide the `YOUTUBE_URL`.
        *   Include a call-to-action with a link to the user's website (`USER_WEBSITE`).

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

### **Step 6: Thumbnail Generation and Resizing**

1.  **For each cut, generate a thumbnail with a prompt that clearly describes the desired output:**
    *   Create a variable `PROMPT` with the following content: "Generate a YouTube thumbnail for a video about software development. The thumbnail must prominently feature the text: '{title}'. The design should be eye-catching, modern, and relevant to the video's content to maximize audience engagement. The image should be interesting enough to make a developer want to click on it."
    *   Run the command: `source .venv/bin/activate && python scripts/generate_image.py "{PROMPT}" "cuts-{VIDEO_ID}/cut{N}_thumbnail_raw.png" --model "gpt-image-1" --size "1536x1024"`
    NOTE: Do not change the model or the size!!!!!
2.  **Resize the generated thumbnail to YouTube's recommended size (1280x720):**
    *   Run the command: `source .venv/bin/activate && python scripts/resize_image.py "cuts-{VIDEO_ID}/cut{N}_thumbnail_raw.png" "cuts-{VIDEO_ID}/cut{N}_thumbnail_1280x720.png" --width 1280 --height 720`

### **Step 7: Video Upload**

1.  **For each cut, upload the video to YouTube with its generated thumbnail:**
    *   Run the command: `source .venv/bin/activate && python scripts/upload_youtube_video.py --file "cuts-{VIDEO_ID}/cut{N}.mp4" --title "{title}" --description "{description}" --thumbnail "cuts-{VIDEO_ID}/cut{N}_thumbnail_1280x720.png"`

### **Step 8: Completion**

1.  **Notify the user** that the process is complete and all video cuts, thumbnails, and the metadata file have been created and uploaded in the `cuts-{VIDEO_ID}` directory.
