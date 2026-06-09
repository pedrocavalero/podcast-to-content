# YouTube to LinkedIn Posts Workflow

This document outlines the step-by-step process for converting a YouTube video into a series of engaging, developer-focused LinkedIn posts and publishing or scheduling them.

**Executor:** Gemini CLI / Claude Agent

---

### **Step 1: Initialization**

1.  **Ask the user for the YouTube video ID.**
    -   Store this value as `VIDEO_ID`.
2.  **Determine the DATE value.**
    -   **Check if a folder exists** in the format `yy-mm-dd-{VIDEO_ID}` (e.g. using `ls -d *-{VIDEO_ID}`).
    -   **If found:** Extract the date part (`yy-mm-dd`) from the folder name and use it as `DATE`.
    -   **If not found:** Get the current date in `yy-mm-dd` format and use it as `DATE`.
3.  **Define the working directory** as `{DATE}-{VIDEO_ID}/linkedin`.
    -   Store this value as `LINKEDIN_DIR`.
4.  **Define the download directory** as `{DATE}-{VIDEO_ID}/download`.
    -   Store this value as `DOWNLOAD_DIR`.
5.  **Create the directories** `{LINKEDIN_DIR}` and `{DOWNLOAD_DIR}` (and their parent `{DATE}-{VIDEO_ID}` if needed) to store all generated assets.
6.  **When searching for files or folders, always include gitignored files.**

### **Step 2: Transcription**

1.  **Check if transcript already exists.**
    -   Check if a `.srt` file exists in `{DOWNLOAD_DIR}` (e.g. `{DOWNLOAD_DIR}/*.srt`).
    -   If it exists, skip the download step.
2.  **Download subtitles using yt-dlp.**
    -   Run the command: `source .venv/bin/activate && yt-dlp -P {DOWNLOAD_DIR} --write-auto-sub --sub-lang en --skip-download --convert-subs srt --cookies-from-browser chrome "https://www.youtube.com/watch?v={VIDEO_ID}"`
    -   *Note: If `chrome` is not available or you use a different browser, replace `chrome` with your browser's name (e.g., `firefox`, `safari`), or refer to yt-dlp documentation for more options.*
3.  **Convert to plain text.**
    -   Run the command: `source .venv/bin/activate && python3 scripts/srt_to_text.py {DOWNLOAD_DIR}/*.srt {LINKEDIN_DIR}/transcript.txt`
4.  **Verify and Save.**
    -   Ensure `{LINKEDIN_DIR}/transcript.txt` exists and contains text.
5.  **Note**: 
    -   In case of error (e.g., yt-dlp fails or transcript is empty), stop the workflow.

### **Step 3: Content Analysis & Topic Extraction**

1.  **Read the transcript** from `{LINKEDIN_DIR}/transcript.txt`.
2.  **Identify 5 Main Topics** optimized for software developer audiences:
    -   Ensure topics are relevant, specific, and actionable.
    -   For each topic, provide a brief title, key insight, and audience pain point.
3.  **Present Strategy for Approval**:
    -   Ask the user for approval on the extracted topics using the interactive interface or confirmation message.
    -   Ask clarifying questions regarding:
        -   **Tone**: Professional, conversational, technical, or mix (default: conversational).
        -   **Length**: Short (~200-300 words) or Medium (~400-500 words).
        -   **Emojis**: Yes, No, or Sparingly (default: sparingly).
    -   Wait for user confirmation before proceeding.

### **Step 4: LinkedIn Post Generation & Carousel Design**

1.  **Generate Post Variations**:
    -   For each of the 5 approved topics, generate **3-4 post variations** using the following copywriting structures:
        -   **Insight Post**: Focuses on data, findings, or main concepts.
        -   **Story Post**: Focuses on a real case study or experience from the transcript.
        -   **Quick Tip**: Short, highly actionable takeaways.
        -   **Contrarian Take**: Challenges common developer beliefs.
        -   **Personal Angle**: Shares vulnerable or relatable technical lessons.
2.  **Generate Carousel Slides (Optional - for high reach)**:
    -   For chosen topics, draft a `slides.txt` file in the topic directory.
    -   The slides file should be divided by `---` lines.
    -   Use the following format for slides:
        ```markdown
        # Slide 1 (Title)
        Title: [Compelling Slide Deck Title]
        Subtitle: [Engaging Subtitle]
        Branding: Pedro Cavalero

        ---

        # Slide 2
        Title: [Slide title or concept]
        - [Key takeaway 1]
        - [Key takeaway 2]
        - [Key takeaway 3]

        ---

        # Slide 3 (CTA)
        Title: Read the full article
        Subtitle: Link in first comment
        Branding: Pedro Cavalero
        ```
3.  **Ensure Post Quality and Formatting**:
    -   **Hook**: Start with a scroll-stopping statement in the first 2 lines (visible in mobile preview).
    -   **Body**: Keep paragraphs short (1-2 sentences maximum) with generous white space.
    -   **Bullets**: Use unicode bullets (e.g. `→`, `•`, `✓`) instead of standard markdown dashes to ensure formatting is preserved.
    -   **Call to Action / Hook at the End**: End with a single, clear, thought-provoking question or call-to-action to invite comments and boost algorithm engagement.
    -   **No Redundant Sign-off**: Do NOT include sign-offs like "Cheers, Pedro Cavalero" at the end of the post, as they are redundant and discourage readers from commenting.
    -   **First Comment Content**: Clearly define the first comment text block containing only the YouTube video link `https://www.youtube.com/watch?v={VIDEO_ID}` (and any brief link context).
4.  **Save the generated files**:
    -   Create a directory for each topic: `{LINKEDIN_DIR}/topic-{N}-{slug}/`.
    -   Save individual posts to `{LINKEDIN_DIR}/topic-{N}-{slug}/post-{M}-{type}.md`.
    -   Save carousel slide text to `{LINKEDIN_DIR}/topic-{N}-{slug}/slides.txt`.
    -   Create a `{LINKEDIN_DIR}/README.md` file listing all topics, posts, and a suggested 4-5 week posting schedule (e.g. posting every Monday, Wednesday, and Friday).

### **Step 5: Content Review and Refinement**

1.  **Review generated posts**:
    -   Read through the generated markdown files.
    -   Check that hooks are compelling, scannability is high, and unicode bullets are used.
    -   Verify that no external URLs are placed in the main post body (must be in the first comment block).

### **Step 6: PDF Compilation & Publishing**

1.  **Prepare LinkedIn Credentials**:
    -   Remind the user to run the credentials refresh script if they haven't already:
        `source .venv/bin/activate && python scripts/refresh_linkedin_credentials.py`
2.  **Generate PDF Carousel (if slides.txt was created)**:
    -   Run the command:
        `source .venv/bin/activate && python scripts/generate_linkedin_carousel.py --input {LINKEDIN_DIR}/topic-{N}-{slug}/slides.txt --output {LINKEDIN_DIR}/topic-{N}-{slug}/carousel.pdf`
3.  **Publish Posts**:
    -   Inform the user of the generated post paths.
    -   The user can publish a post (text-only) automatically using the poster script:
        `source .venv/bin/activate && python scripts/linkedin_poster.py --markdown {LINKEDIN_DIR}/topic-{N}-{slug}/post-{M}-{type}.md`
    -   To publish a post with a PDF carousel:
        `source .venv/bin/activate && python scripts/linkedin_poster.py --markdown {LINKEDIN_DIR}/topic-{N}-{slug}/post-{M}-{type}.md --pdf {LINKEDIN_DIR}/topic-{N}-{slug}/carousel.pdf`
    -   *(Optional)* If an image is available instead of a PDF carousel, they can attach it using:
        `--image path/to/image.png`
4.  **Manual Posting Option**:
    -   Remind the user that they can also copy/paste the content directly to LinkedIn or their social scheduler (Buffer, Hootsuite, etc.).

### **Step 7: Completion**

1.  **Notify the user** that all LinkedIn post drafts and carousels have been generated, compiled, and saved, and outline their posting schedule.
