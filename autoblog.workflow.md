
# YouTube to WordPress Autoblog Workflow

This document outlines the step-by-step process for converting a YouTube video into a series of blog posts with featured images, and publishing them to WordPress.

**Executor:** Gemini CLI

---

### **Step 1: Initialization**

1.  **Ask the user for the YouTube video ID.**
    -   Store this value as `VIDEO_ID`.
2.  **Create a directory** named after the `VIDEO_ID` to store all generated assets.

### **Step 2: Transcription**

1.  **Execute the transcription script.**
    -   Run the command: `source .venv/bin/activate && python3 transcribe.py {VIDEO_ID}`
2.  **Save the output.**
    -   Save the resulting transcript to a file named `{VIDEO_ID}/transcript.txt`.
3.  **Note**: 
    -   In case of error and the transcript is not saved, stop the workflow

### **Step 3: Content Analysis & Summarization**

1.  **Read the transcript** from `{VIDEO_ID}/transcript.txt`.
2.  **Based on the transcript, what are the 5 main topics of the video?** For each topic, provide a one-paragraph summary.
3.  **Save the result** to a file named `{VIDEO_ID}/summary.md`.

### **Step 4: Blog Post Generation**

1.  **Parse the topics** from `{VIDEO_ID}/summary.md`.
2.  **For each of the 5 topics, perform the following:**
    a. **Generate Blog Post Content:** 
       Create a blog post based on the following topic and summary. The target audience is developers for whom English is a second language, so use an informal yet professional tone. The post should be engaging and use quotes from the provided transcript to support the points. Create a catchy, descriptive title for the post. 
       Always use the full transcript to support the points. Always identify the person that is speaking when getting the quotes.

       The post should follow this structure, similar to the example provided:
       - Start with a friendly greeting (e.g., "Hi team," or "Hey fellow devs!").
       - Introduce the topic and its relevance to software engineers.
       - Incorporate direct quotes from the transcript to support key points, clearly attributing them.
       - Break down complex ideas into clear, concise paragraphs, using bullet points or numbered lists if helpful.
       - Focus on actionable advice or insights for developers.
       - Conclude with a call to action or a thought-provoking question.
       - sign off with a friendly note (e.g., "Happy coding!").
       - use Pedro Cavalero as sender name in the signature.

       Topic: {topic_title}
       Summary: {topic_summary}
       Full Transcript:
       {transcript_content}
    b. **Save the post** to a file named `{VIDEO_ID}/post{N}.md`, where {N} is the post number (1-5).
3.  **Note**
    -   In case of error and the posts are not saved, stop the workflow

### **Step 5: Featured Image Generation**

1.  **For each of the 5 blog posts, perform the following:**
    a. **Generate an Image Prompt:** Call the Gemini API with the following prompt:
       ```
       Create a short, descriptive prompt for a text-to-image AI model. The image should be a feature image for a blog post with the title: "{post_title}". The style should be digital art, suitable for a tech blog.
       ```
    b. **Execute the image generation script:**
       - Run the command: `source .venv/bin/activate && python generate_image.py "{image_prompt}" {VIDEO_ID}/post{N}.png`
2.  **Note**
    -   In case of error and the images are not saved, stop the workflow

### **Step 6: WordPress Publication**

1.  **Check for WordPress credentials** (WP_URL, WP_USER, WP_PASSWORD) in the environment variables.
2.  **For each of the 5 blog posts, perform the following:**
    a. **Extract the title** from the first line of the markdown file.
    b. **Execute the WordPress uploader script:**
       - Run the command: `source .venv/bin/activate && python wordpress_uploader.py "{post_title}" {VIDEO_ID}/post{N}.md {VIDEO_ID}/post{N}.png`

### **Step 7: Completion**

1.  **Notify the user** that the process is complete and all posts have been published.
