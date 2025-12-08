# YouTube to WordPress Autoblog Workflow

This document outlines the step-by-step process for converting a YouTube video into a series of blog posts with featured images, and publishing them to WordPress.

**Executor:** Gemini CLI

---

### **Step 1: Initialization**

1.  **Ask the user for the YouTube video ID.**
    -   Store this value as `VIDEO_ID`.
2.  **Determine the DATE value.**
    -   **Check if a folder exists** in the format `yy-mm-dd-{VIDEO_ID}` (e.g. using `ls -d *-{VIDEO_ID}`).
    -   **If found:** Extract the date part (`yy-mm-dd`) from the folder name and use it as `DATE`.
    -   **If not found:** Get the current date in `yy-mm-dd` format and use it as `DATE`.
3.  **Define the working directory** as `{DATE}-{VIDEO_ID}/blog`.
    -   Store this value as `BLOG_DIR`.
4.  **Define the download directory** as `{DATE}-{VIDEO_ID}/download`.
    -   Store this value as `DOWNLOAD_DIR`.
5.  **Create the directories** `{BLOG_DIR}` and `{DOWNLOAD_DIR}` (and their parent `{DATE}-{VIDEO_ID}` if needed) to store all generated assets.
6.  **When searching for files or folders, always include gitignored files.**

### **Step 2: Transcription**

1.  **Check if transcript already exists.**
    -   Check if a `.srt` file exists in `{DOWNLOAD_DIR}` (e.g. `{DOWNLOAD_DIR}/*.srt`).
    -   If it exists, skip the download step.
2.  **Download subtitles using yt-dlp.**
    -   Run the command: `source .venv/bin/activate && yt-dlp -P {DOWNLOAD_DIR} --write-auto-sub --sub-lang en --skip-download --convert-subs srt --cookies-from-browser chrome "https://www.youtube.com/watch?v={VIDEO_ID}"`
    -   *Note: If `chrome` is not available or you use a different browser, replace `chrome` with your browser's name (e.g., `firefox`, `safari`), or refer to yt-dlp documentation for more options.*
3.  **Convert to plain text.**
    -   Run the command: `source .venv/bin/activate && python3 scripts/srt_to_text.py {DOWNLOAD_DIR}/*.srt {BLOG_DIR}/transcript.txt`
3.  **Verify and Save.**
    -   Ensure `{BLOG_DIR}/transcript.txt` exists and contains text.
4.  **Note**: 
    -   In case of error (e.g., yt-dlp fails or transcript is empty), stop the workflow.

### **Step 3: Content Analysis & Summarization**

1.  **Read the transcript** from `{BLOG_DIR}/transcript.txt`.
2.  **Based on the transcript, what are the 5 main topics of the video?** For each topic, provide a one-paragraph summary.
3.  **Save the result** to a file named `{BLOG_DIR}/summary.md`.

### **Step 4: Blog Post Generation**

1.  **Parse the topics** from `{BLOG_DIR}/summary.md`.
2.  **For each of the 5 topics, perform the following:**
    a. **Generate Blog Post Content:** 
       Create a high-quality blog post based on the provided topic, summary, and full transcript. The post should be optimized for engagement and readability, especially for developers who are non-native English speakers.

       **Instructions:**

       - **Title:** Create a catchy and descriptive title (6-10 words). The title should be in title case and include keywords from the topic.
       - **Tone:** Use an informal, friendly, and professional tone. Imagine you're a senior developer mentoring a junior colleague. Use contractions (e.g., "you're", "it's") to make it more conversational.
       - **Audience:** The target audience is developers for whom English is a second language. Use clear and simple language. Avoid jargon where possible, or explain it clearly.
       - **Structure & Formatting:**
         - Start with a friendly and engaging greeting (e.g., "Hey fellow devs!", "Hi team,").
         - Write a short introduction (2-3 sentences) to grab the reader's attention and explain the post's value.
         - Use Markdown for formatting. Use `##` for subheadings to break up the content.
         - Use bullet points or numbered lists to present complex information or steps.
         - Keep paragraphs short (2-4 sentences).
       - **Content:**
         - The post must be based on the provided `topic_title` and `topic_summary`.
         - Use the `full_transcript` to extract direct quotes that support your points.
         - **Quote Handling:** When you use a quote, you must:
           1.  Identify the speaker by name.
           2.  Clean up the raw transcription: remove filler words (like "um", "ah"), false starts, and repeated words. Correct grammatical errors. Ensure the final quote is fluent and readable but preserves the original meaning and informal tone. *Do not summarize the quote.*
         - Provide actionable advice and practical insights for developers.
         - Ask rhetorical questions to keep the reader engaged.
       - **Conclusion:**
         - Write a concluding paragraph that summarizes the key takeaways.
         - End with a specific and engaging call to action or a thought-provoking question. Examples: "What are your thoughts on this? Share in the comments below!", "Try this out in your next project and let me know how it goes!".
       - **Signature:**
         - Sign off with a friendly closing (e.g., "Happy coding!", "Cheers,").
         - The sender's name must be "Pedro Cavalero".

       **Inputs:**
       - Topic: {topic_title}
       - Summary: {topic_summary}
       - Full Transcript: {transcript_content}
    b. **Save the post** to a file named `{BLOG_DIR}/post{N}.md`, where {N} is the post number (1-5).
3.  **Note**
    -   In case of error and the posts are not saved, stop the workflow

### **Step 5: Content Review and Refinement**

1.  **For each of the 5 blog posts, always perform the following:**
    a. **Review the post:** Read the content of `{BLOG_DIR}/post{N}.md`.
    b. **Act as a content reviewer.** Based on the rules defined in Step 4.2.a, review the blog post. Pay special attention to the quotes.
    c. **Quote Refinement:**
        - **Identify the speaker:** Ensure each quote clearly identifies the speaker by name (e.g., "**Pedro:**").
        - **Clean up the transcription:** Remove filler words (like "um", "ah", "you know"), false starts, and repeated words.
        - **Correct grammatical errors:** Ensure the quote is grammatically correct and flows naturally in English.
        - **Preserve the meaning:** The final quote must be fluent and readable but preserve the original meaning and informal tone of the speaker. *Do not summarize the quote.*
    d. **Rewrite and Update:** If the post can be improved, rewrite it to make it even better, following all the rules from step 4.2.a and the quote refinement guidelines above. Save the potentially rewritten post back to `{BLOG_DIR}/post{N}.md`.

### **Step 6: Featured Image Generation**

1.  **For each of the 5 blog posts, perform the following:**
    a. **Generate an Image Prompt:** Call the Gemini API with the following prompt:
       ```
       Create a short, descriptive prompt for a text-to-image AI model. The image should be a feature image for a blog post with the title: "{post_title}". The style should be digital art, suitable for a tech blog.
       ```
    b. **Execute the image generation script:**
       - Run the command: `source .venv/bin/activate && python scripts/generate_image.py "{image_prompt}" {BLOG_DIR}/post{N}.png --model "dall-e-3"`
2.  **Note**
    -   In case of error and the images are not saved, stop the workflow

### **Step 7: WordPress Publication**

1.  **Check for WordPress credentials** (WP_URL, WP_USER, WP_PASSWORD) in the environment variables.
2.  **For each of the 5 blog posts, perform the following:**
    a. **Extract the title** from the first line of the markdown file.
    b. **Execute the WordPress uploader script:**
       - Run the command: `source .venv/bin/activate && python wordpress_uploader.py "{post_title}" {BLOG_DIR}/post{N}.md {BLOG_DIR}/post{N}.png`

### **Step 8: Completion**

1.  **Notify the user** that the process is complete and all posts have been published.