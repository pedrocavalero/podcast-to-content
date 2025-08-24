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
2.  **Analyze the transcript to identify 10 interesting and valuable cuts** for a developer audience. Each cut should be between 30 and 55 seconds long *after* a 2.0x speed increase (longer is preffered). Make sure the cuts has very interesting content.
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

1.  **Before proceeding, identify the original SRT filename and its version without spaces:**
    *   Find the downloaded SRT file (e.g., by running `find "shorts-{VIDEO_ID}" -name "*.srt"`). Let's call this `{ORIGINAL_SRT_FILENAME}`.
    *   Create a version of this filename with spaces replaced by underscores. Let's call this `{ORIGINAL_SRT_FILENAME_NO_SPACES}`. (e.g., `How_to_Become_an_AI-powered_Developer_[ZnCY5zV9B80].en.srt`)

2.  **For each of the 10 cuts, prepare the subtitle and title files:**
    *   **Rename the original SRT file** to remove spaces (if not already done): `mv "shorts-{VIDEO_ID}/{ORIGINAL_SRT_FILENAME}" "shorts-{VIDEO_ID}/{ORIGINAL_SRT_FILENAME_NO_SPACES}"`
    *   **Adjust subtitle timestamps:** Run `source .venv/bin/activate && python scripts/adjust_srt.py "shorts-{VIDEO_ID}/{ORIGINAL_SRT_FILENAME_NO_SPACES}" {start_time} "shorts-{VIDEO_ID}/short{N}_temp_sub.srt"`
    *   **Write a multi-line title to a temporary file:** `TITLE="{title}" python -c 'import os, textwrap; print("\n".join(textwrap.wrap(os.environ["TITLE"], width=25)))' > "shorts-{VIDEO_ID}/temp_title.txt"`

3.  **Execute the video cutting and speed adjustment command:**
    *   `ffmpeg -y -ss {start_time} -to {end_time} -i "shorts-{VIDEO_ID}/*.mkv" -filter_complex "[0:v]scale=-1:1152,crop=1080:1152,pad=1080:1920:0:480[padded];[padded]subtitles=filename='shorts-{VIDEO_ID}/short{N}_temp_sub.srt':force_style='Fontsize=12,PrimaryColour=&H00FFFF'[subtitled];[subtitled]drawtext=textfile=shorts-{VIDEO_ID}/temp_title.txt:fontfile='/System/Library/Fonts/Supplemental/Arial Bold.ttf':fontsize=70:fontcolor=yellow:x=(w-text_w)/2:y=(480-text_h)/2[drawn];[drawn]setpts=PTS/2.0[v]" -map "[v]" -map 0:a -af "atempo=2.0" -c:a aac -b:a 128k "shorts-{VIDEO_ID}/short{N}.mp4"`
    *   Where `{N}` is the cut number (1-10).
    *   The `-filter_complex` chain now includes:
        *   `scale=-1:1152,crop=1080:1152,pad=1080:1920:0:480`: Scales, crops, and pads the video. The top padding is increased to 480 pixels.
        *   `subtitles=filename='shorts-{VIDEO_ID}/short{N}_temp_sub.srt':force_style='Fontsize=12,PrimaryColour=&H00FFFF'`: Applies the time-shifted subtitles from the temporary SRT file, with yellow color and smaller font.
        *   `drawtext=textfile=shorts-{VIDEO_ID}/temp_title.txt:fontfile='/System/Library/Fonts/Supplemental/Arial Bold.ttf':fontsize=70:fontcolor=yellow:x=(w-text_w)/2:y=(480-text_h)/2`: Overlays the multi-line, bold, yellow title from the temporary text file. The `y` coordinate is adjusted for the increased padding.
        *   `setpts=PTS/2.0`: Adjusts video speed.
    *   `-ss {start_time} -to {end_time}` are now placed before `-i` for accurate cutting.
    *   `-c:a aac -b:a 128k` ensures audio re-encoding.

4.  **Clean up temporary files:**
    *   `rm "shorts-{VIDEO_ID}/short{N}_temp_sub.srt"`
    *   `rm "shorts-{VIDEO_ID}/temp_title.txt"`
    *   **Rename the original SRT file back:** `mv "shorts-{VIDEO_ID}/{ORIGINAL_SRT_FILENAME_NO_SPACES}" "shorts-{VIDEO_ID}/{ORIGINAL_SRT_FILENAME}"`


### **Step 6: Video Upload**

1.  **For each cut, upload the video to YouTube:**
    *   Run the command: `source .venv/bin/activate && python scripts/upload_youtube_short.py --file "shorts-{VIDEO_ID}/short{N}.mp4" --title "{title} #Shorts" --description "{description}"`
    *   Note: The title now includes `#Shorts` to help YouTube categorize it.

### **Step 7: Completion**

1.  **Notify the user** that the process is complete and all video shorts and the metadata file have been created and uploaded in the `shorts-{VIDEO_ID}` directory.
