# YouTube to Newsletter Workflow

This document outlines the step-by-step process for converting a YouTube video into a series of engaging newsletters for developers, and scheduling them on WordPress.

**Executor:** Gemini CLI

---

### **Step 1: Initialization**

1.  **Ask the user for the YouTube video ID.**
    -   Store this value as `VIDEO_ID`.
2.  **Determine the DATE value.**
    -   **Check if a folder exists** in the format `yy-mm-dd-{VIDEO_ID}` (e.g. using `ls -d *-{VIDEO_ID}`).
    -   **If found:** Extract the date part (`yy-mm-dd`) from the folder name and use it as `DATE`.
    -   **If not found:** Get the current date in `yy-mm-dd` format and use it as `DATE`.
3.  **Define the working directory** as `{DATE}-{VIDEO_ID}/newsletter`.
    -   Store this value as `NEWSLETTER_DIR`.
4.  **Define the download directory** as `{DATE}-{VIDEO_ID}/download`.
    -   Store this value as `DOWNLOAD_DIR`.
5.  **Create the directories** `{NEWSLETTER_DIR}` and `{DOWNLOAD_DIR}` (and their parent `{DATE}-{VIDEO_ID}` if needed) to store all generated assets.
6.  **When searching for files or folders, always include gitignored files.**

### **Step 2: Transcription**

1.  **Check if transcript already exists.**
    -   Check if a `.srt` file exists in `{DOWNLOAD_DIR}` (e.g. `{DOWNLOAD_DIR}/*.srt`).
    -   If it exists, skip the download step.
2.  **Download subtitles using yt-dlp.**
    -   Run the command: `source .venv/bin/activate && yt-dlp -P {DOWNLOAD_DIR} --write-auto-sub --sub-lang en --skip-download --convert-subs srt --cookies-from-browser chrome "https://www.youtube.com/watch?v={VIDEO_ID}"`
    -   *Note: If `chrome` is not available or you use a different browser, replace `chrome` with your browser's name (e.g., `firefox`, `safari`), or refer to yt-dlp documentation for more options.*
3.  **Convert to plain text.**
    -   Run the command: `source .venv/bin/activate && python3 scripts/srt_to_text.py {DOWNLOAD_DIR}/*.srt {NEWSLETTER_DIR}/transcript.txt`
4.  **Verify and Save.**
    -   Ensure `{NEWSLETTER_DIR}/transcript.txt` exists and contains text.
5.  **Note**: 
    -   In case of error (e.g., yt-dlp fails or transcript is empty), stop the workflow.

### **Step 3: Content Analysis & Summarization**

1.  **Read the transcript** from `{NEWSLETTER_DIR}/transcript.txt`.
2.  **Based on the transcript, what are the 3 main topics of the video?** For each topic, provide a one-paragraph summary.
3.  **Save the result** to a file named `{NEWSLETTER_DIR}/summary.md`.

### **Step 4: Newsletter Generation**

1.  **Parse the topics** from `{NEWSLETTER_DIR}/summary.md`.
2.  **For each of the 3 topics, perform the following:**
    a. **Generate Newsletter Content:** 
       Create an engaging, friendly newsletter email based on the provided topic, summary, and full transcript.

       **Instructions:**

       - **Tone:** Friendly, First-Person ("I"). You are Pedro Cavalero, a senior developer talking to your fellow subscribers. Authentic, "Developer-to-Developer". No marketing fluff.
       - **Audience:** Developers interested in Software Development, AI, Programming, Architecture, and Career.
       - **Structure:**
         - **Subject Line:** *Critical*: High-impact, short (< 50 chars), and intriguing. (e.g., "The end of coding?", "Why your architecture fails").
         - **Preheader Text:** A separate line at the very top. One sentence that teases the content to boost open rates.
         - **Opening (The Hook):** Do *not* start with "In this episode...". Start with a relatable problem, a controversial opinion, or a surprising fact from the transcript to grab attention immediately. Then connect it to the episode.
         - **Body:** 
           - Discuss the topic in depth.
           - **Value First:** Focus on *insights* and *solutions*, not just a summary of what happened.
           - **Scannability:** Use **bold** for key phrases. Keep paragraphs extremely short (1-3 sentences).
           - Use bullet points for lists.
         - **Key Takeaways:** 3 distinct, actionable bullet points.
         - **Call to Action (CTA):** 
            - Primary: "Listen to the full episode here: [Link]"
            - Secondary (Engagement): "What's your take? Hit reply and let me know."
         - **Sign-off:** "Cheers," or "Happy coding," followed by "Pedro Cavalero".
         - **P.S.:** Add a short "P.S." with a quick tip, a personal note, or a reminder to share the newsletter.
       - **Category:** The content should fit into "AI" or "Carreiras" (Careers).

       **Inputs:**
       - Topic: {topic_title}
       - Summary: {topic_summary}
       - Full Transcript: {transcript_content}
    b. **Save the newsletter** to a file named `{NEWSLETTER_DIR}/newsletter{N}.md`, where {N} is the number (1-3).

### **Step 5: Content Review and Refinement**

1.  **For each of the 3 newsletters, always perform the following:**
    a. **Review the newsletter:** Read the content of `{NEWSLETTER_DIR}/newsletter{N}.md`.
    b. **Act as a content reviewer.** Ensure the tone is consistent (Pedro Cavalero, friendly, first-person), the CTA is present, and the content is valuable for developers.
    c. **Rewrite if necessary:** If improvements are needed, rewrite and save back to `{NEWSLETTER_DIR}/newsletter{N}.md`.

### **Step 6: Featured Image Generation**

1.  **For each of the 3 newsletters, perform the following:**
    a. **Generate an Image Prompt:** Call the Gemini API:
       ```
       Create a descriptive prompt for a text-to-image AI model. The image should be a featured image for a newsletter about: "{newsletter_subject}". Style: Digital art, modern, suitable for a tech newsletter.
       ```
    b. **Execute the image generation script:**
       - Run the command: `source .venv/bin/activate && python scripts/generate_image.py "{image_prompt}" {NEWSLETTER_DIR}/newsletter{N}.png --model "dall-e-3"`

### **Step 7: WordPress Scheduling**

1.  **Calculate Schedule Dates:**
    - The first newsletter should be scheduled for the **next Sunday**.
    - Subsequent newsletters should be scheduled weekly (every Sunday).
    - Use python to calculate these dates.
    - Run: `python3 -c "import datetime; today = datetime.date.today(); days_ahead = 6 - today.weekday(); print((today + datetime.timedelta(days=days_ahead + (7 if days_ahead <= 0 else 0))).isoformat())"` to get the first Sunday.
    - Store this as `START_DATE`.

2.  **Check for WordPress credentials** (WP_URL, WP_USER, WP_PASSWORD) in the environment variables.

3.  **For each of the 3 newsletters (N=1 to 3), perform the following:**
    a. **Calculate Date for this post:**
       - Run: `python3 -c "import datetime; start = datetime.date.fromisoformat('{START_DATE}'); print((start + datetime.timedelta(weeks={N}-1)).isoformat())"`
       - Store as `PUBLISH_DATE`.
    b. **Extract the title** from the markdown file (Subject Line).
    c. **Execute the WordPress uploader script:**
       - Run the command: 
         `source .venv/bin/activate && python scripts/wordpress_uploader.py "{newsletter_subject}" {NEWSLETTER_DIR}/newsletter{N}.md {NEWSLETTER_DIR}/newsletter{N}.png --tags "newsletter" --categories "AI,Carreiras" --publish_date "{PUBLISH_DATE}T10:00:00" --status "future"`

### **Step 8: Completion**

1.  **Notify the user** that the newsletters have been generated and scheduled.
