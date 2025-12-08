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
4.  **Get the current date** in `yy-mm-dd` format.
    *   Store this value as `DATE`.
5.  **Define the working directory** as `{DATE}-{VIDEO_ID}/cuts`.
    *   Store this value as `CUTS_DIR`.
6.  **Define the download directory** as `{DATE}-{VIDEO_ID}/download`.
    *   Store this value as `DOWNLOAD_DIR`.
7.  **Create the directories** `{CUTS_DIR}` and `{DOWNLOAD_DIR}` (and their parent `{DATE}-{VIDEO_ID}` if needed) to store all generated assets.
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
2.  **Analyze the transcript to identify 5 interesting and valuable cuts** for a developer audience. Each cut should be between 5 and 10 minutes long.
3.  **For each cut, define the following:**
    *   Start time (`start_time`)
    *   End time (`end_time`)
    *   A catchy and descriptive title (`title`)
    *   A detailed and engaging `description` of the cut's content. The description must:
        *   Be written in a compelling and engaging tone, using emojis to highlight key points and create visual interest.
        *   Integrate timestamps (e.g., `00:45`) naturally within the descriptive text, highlighting at least 3 key moments or topics discussed at those points. Use bulleted lists of timestamps but make the description of each line visually atractive with emojis. Make sure the timestamps are based on the cut video time, not from the original one.
        *   Clearly mention the original video's name and provide the `YOUTUBE_URL`.
        *   Include a clear and concise call-to-action with a link to the user's website (`USER_WEBSITE`).

### **Step 4: Cuts Metadata Generation**

1.  **Create a new file** named `{CUTS_DIR}/cuts.md`.
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

1.  **For each of the 5 cuts, calculate the duration** of the cut in seconds (`{duration}` = `{end_time}` - `{start_time}`).
2.  **Execute the following commands to cut the video with a 2-second fade-in and fade-out:**
    *   **Step 2.1: Apply fade-in and create a temporary file.**
        *   `ffmpeg -y -i "{DOWNLOAD_DIR}/{video_file}" -ss {start_time} -to {end_time} -vf "fade=t=in:st=0:d=2" -c:a copy "{CUTS_DIR}/cut{N}_temp.mp4"`
    *   **Step 2.2: Apply fade-out to the temporary file and create the final cut.**
        *   `ffmpeg -y -i "{CUTS_DIR}/cut{N}_temp.mp4" -vf "fade=t=out:st={duration}-2:d=2" -c:a copy "{CUTS_DIR}/cut{N}.mp4"`
    *   **Step 2.3: Delete the temporary file.**
        *   `rm "{CUTS_DIR}/cut{N}_temp.mp4"`
    *   Where `{video_file}` is the name of the source video file in `{DOWNLOAD_DIR}` (e.g., `.mp4`, `.mkv`), `{N}` is the cut number (1-5), and `{duration}` is the calculated duration in seconds.

### **Step 6: Thumbnail Generation and Resizing**

1.  **For each cut, generate a custom thumbnail prompt based on the `{title}`:**
    *   **Analyze the `{title}`** to determine the most appropriate:
        *   **Expression**: A facial expression that matches the emotion of the title (e.g., shocked, happy, serious, confused).
        *   **Background**: A visual setting that symbolizes the topic (e.g., code on a screen, futuristic city, office setting).
        *   **Text**: A short, punchy, high-contrast text overlay (max 3-4 words) derived from the title.
    *   **Construct the `PROMPT` variable** using these generated details:
        *   "Create a YouTube thumbnail using the provided reference image for a video titled '{title}'. 1. Focus: Crop and zoom in on the face from the reference photo. 2. Expression: {generated_expression}. 3. Background: {generated_background}. 4. Text: Include the text '{generated_text}' in large, bold, high-contrast typography. 5. Style: High-quality, 4k, professional YouTube thumbnail style, vibrant colors, 16:9 aspect ratio."
    *   Run the command: `source .venv/bin/activate && python scripts/generate_image_nano_banana.py "{PROMPT}" "{CUTS_DIR}/cut{N}_thumbnail_raw.png" --aspect_ratio "16:9" --reference_image "workflows/Foto-3x4.jpg"`
2.  **Resize the generated thumbnail to YouTube's recommended size (1280x720):**
    *   Run the command: `source .venv/bin/activate && python scripts/resize_image.py "{CUTS_DIR}/cut{N}_thumbnail_raw.png" "{CUTS_DIR}/cut{N}_thumbnail_1280x720.png" --width 1280 --height 720`

### **Step 7: Video Upload**

1.  **For each cut, upload the video to YouTube with its generated thumbnail:**
    *   Run the command: `source .venv/bin/activate && python scripts/upload_youtube_video.py --file "{CUTS_DIR}/cut{N}.mp4" --title "{title}" --description "{description}" --thumbnail "{CUTS_DIR}/cut{N}_thumbnail_1280x720.png"`

### **Step 8: Completion**

1.  **Notify the user** that the process is complete and all video cuts, thumbnails, and the metadata file have been created and uploaded in the `{CUTS_DIR}` directory.