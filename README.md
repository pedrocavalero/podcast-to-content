# Podcast to Content

This project provides a set of workflows to automate content creation from podcasts and videos. It helps you repurpose your existing content into different formats like blog posts and short video clips.

Currently, there are three main workflows available:

1.  **Autoblog Workflow:** Converts a YouTube video into a series of blog posts, complete with featured images, and publishes them to WordPress.
2.  **Video Cuts Workflow:** Extracts interesting segments from a YouTube video, generates thumbnails, and uploads them as new short videos to YouTube.
3.  **YouTube Video to Shorts Workflow:** Downloads a YouTube video and its subtitles, analyzes the content to find valuable segments, creates YouTube Shorts from those segments, and generates metadata for a shorts channel.
4.  **Newsletter Workflow:** Converts a YouTube video into a series of engaging weekly newsletters for developers and schedules them on WordPress.

---

## Autoblog Workflow

This workflow automates the process of converting a YouTube video into a series of blog posts and publishing them to WordPress.

### Features

-   **YouTube Video Transcription:** Automatically transcribes the audio from a YouTube video.
-   **Content Summarization:** Analyzes the transcript and identifies the main topics.
-   **Blog Post Generation:** Creates multiple blog posts based on the identified topics.
-   **AI-Powered Image Generation:** Generates a unique featured image for each blog post.
-   **WordPress Integration:** Uploads the generated blog posts and featured images to a WordPress site.

### Requirements

-   Python 3.x
-   An OpenAI API key.
-   WordPress credentials (URL, username, and application password).

### Workflow

1.  **Initialization:** Takes a YouTube video ID as input and creates a directory to store the generated assets.
2.  **Transcription:** Transcribes the YouTube video and saves the transcript to a file.
3.  **Content Analysis & Summarization:** Analyzes the transcript to identify the main topics and generates a summary for each.
4.  **Blog Post Generation:** Creates a separate blog post for each topic, using the summary and the full transcript for context.
5.  **Featured Image Generation:** Generates a featured image for each blog post using an AI text-to-image model.
6.  **WordPress Publication:** Publishes the blog posts to WordPress as drafts, with their corresponding featured images.

### Usage

The `workflows/autoblog.workflow.md` file describes the manual steps of the workflow. It can be used inside a AI Agent tool. Using Gemini CLI a prompt like: "Run the @autblog.workflow.md script" can do the trick.

To run the individual scripts:

-   **Transcribe a video:**
    ```bash
    python scripts/transcribe.py <video_id>
    ```
-   **Generate an image:**
    ```bash
    python scripts/generate_image.py "<prompt>" <output_path>
    ```
-   **Upload a post to WordPress:**
    ```bash
    python scripts/wordpress_uploader.py "<title>" <content_path> [image_path] --tags "newsletter" --categories "AI" --status "future" --publish_date "2023-12-25T10:00:00"
    ```

---

## Newsletter Workflow

This workflow converts a YouTube video into engaging, weekly newsletters for developers.

### Features
-   **Podcast to Newsletter:** Converts video transcripts into friendly, first-person newsletters.
-   **Engagement Focused:** Uses best practices like hooks, scannability, and clear CTAs.
-   **Weekly Scheduling:** Automatically schedules newsletters to be published every Sunday on WordPress.
-   **AI Images:** Generates custom featured images for each newsletter.

### Usage
Run the workflow using the Gemini CLI:
```bash
gemini run workflows/newsletter.workflow.md
```
Or use the Claude command: `Run the newsletter workflow for video ID ...`

---

## Video Cuts Workflow

This workflow automates the process of extracting valuable segments from a YouTube video, generating corresponding thumbnails, and uploading them as new videos to a YouTube channel.

### Features

-   **YouTube Video Download:** Downloads the full video and its subtitles.
-   **Content Analysis & Cut Point Identification:** Analyzes the transcript to identify interesting and valuable video segments.
-   **Cuts Metadata Generation:** Creates a markdown file with titles, descriptions, and timestamps for each cut.
-   **Video Cutting:** Extracts the identified segments as separate video files.
-   **AI-Powered Thumbnail Generation:** Generates unique and descriptive thumbnails for each video cut.
-   **Image Resizing:** Resizes generated thumbnails to YouTube's recommended dimensions (1280x720).
-   **YouTube Upload Integration:** Uploads the video cuts along with their generated thumbnails to a YouTube channel.

### Requirements

-   Python 3.x
-   **ffmpeg**: Required for video cutting and frame extraction. Ensure it's installed and accessible in your system's PATH.
-   A YouTube API key.
-   An OpenAI API key.
-   **Google Cloud Project Configuration for YouTube Uploads**:
    To enable YouTube video uploads, you need to configure a Google Cloud Project, enable the YouTube Data API v3, and create OAuth 2.0 Client ID credentials (Desktop app type). Download the `client_secret.json` file and place it in the project's root directory.

### Workflow

1.  **Initialization:** Takes a YouTube video URL as input and creates a dedicated directory for assets.
2.  **Video and Subtitle Download:** Downloads the video and its auto-generated subtitles.
3.  **Content Analysis & Cut Point Identification:** Identifies interesting segments (cuts) within the video based on the transcript.
4.  **Cuts Metadata Generation:** Compiles metadata (title, description, timestamps) for each identified cut into a markdown file.
5.  **Video Cutting:** Creates individual video files for each cut.
6.  **Thumbnail Generation and Resizing:** Generates an AI-powered image for each cut's title and resizes it to the optimal YouTube thumbnail format.
7.  **Video Upload:** Uploads each video cut to YouTube, including its generated thumbnail.
8.  **Completion:** Notifies the user upon successful completion of the entire process.

### Usage

The `workflows/video-cuts.workflow.md` file describes the manual steps of the workflow. It can be used inside a AI Agent tool. Using Gemini CLI a prompt like: "Run the @video-cuts.workflow.md script" can do the trick.

---

## YouTube Video to Shorts Workflow

This workflow outlines the step-by-step process for downloading a YouTube video and its subtitles, analyzing the content to find valuable segments, creating YouTube Shorts from those segments, and generating metadata for a shorts channel.

### Features

-   **YouTube Video Download:** Downloads the full video and its subtitles.
-   **Content Analysis & Cut Point Identification:** Analyzes the transcript to identify interesting and valuable video segments.
-   **Shorts Metadata Generation:** Creates a markdown file with titles, descriptions, and timestamps for each cut.
-   **Video Cutting and Speed Adjustment:** Extracts the identified segments as separate video files and adjusts their speed.
-   **Video Upload:** Uploads the video cuts along with their generated thumbnails to a YouTube channel.

### Requirements

-   Python 3.x
-   **ffmpeg**: Required for video cutting and frame extraction. Ensure it's installed and accessible in your system's PATH.
-   A YouTube API key.
-   An OpenAI API key.
-   **Google Cloud Project Configuration for YouTube Uploads**:
    To enable YouTube video uploads, you need to configure a Google Cloud Project, enable the YouTube Data API v3, and create OAuth 2.0 Client ID credentials (Desktop app type). Download the `client_secret.json` file and place it in the project's root directory.

### Workflow

1.  **Initialization:** Ask the user for the YouTube video URL and their website URL, extract the video ID, and create a directory for assets.
2.  **Video and Subtitle Download:** Download the video and its auto-generated subtitles, or move them from the cuts directory if they already exist.
3.  **Content Analysis & Cut Point Identification:** Analyze the transcript to identify 10 interesting and valuable cuts for a developer audience, each between 30 and 55 seconds long after a 2.0x speed increase. Define start/end times, catchy titles, and concise descriptions with relevant hashtags and a call-to-action.
4.  **Shorts Metadata Generation:** Create a `shorts.md` file with detailed information for each of the 10 cuts.
5.  **Video Cutting and Speed Adjustment:** Prepare subtitle and title files, then use `ffmpeg` to cut, scale, crop, pad, subtitle, overlay title, and speed up each video segment. Clean up temporary files.
6.  **Video Upload:** Upload each video short to YouTube with its title and description.
7.  **Completion:** Notify the user upon successful completion.

### Usage

The `workflows/youtube-shorts.workflow.md` file describes the manual steps of the workflow. It can be used inside a AI Agent tool. Using Gemini CLI a prompt like: "Run the @youtube-shorts.workflow.md script" can do the trick.

---

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/podcast-to-content.git
    cd podcast-to-content
    ```

2.  **Install ffmpeg:**

    **On macOS (using Homebrew):**
    ```bash
    brew install ffmpeg
    ```

    **On Windows:**
    1. Download the latest static build from the [FFmpeg downloads page](https://ffmpeg.org/download.html).
    2. Extract the files to a folder on your computer (e.g., `C:\ffmpeg`).
    3. Add the `bin` directory to your system's PATH environment variable.

    **On Linux (using APT):**
    ```bash
    sudo apt update
    sudo apt install ffmpeg
    ```

3.  **Install uv (if not already installed):**
    ```bash
    # On macOS/Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # On Windows
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

4.  **Install the required Python packages:**
    ```bash
    uv sync
    ```

5.  **Create a `.env` file by copying the example file:**
    ```bash
    cp .env.example .env
    ```

6.  **Edit the `.env` file and add your API keys and WordPress credentials.**

### Running Python Scripts

With uv, you have two options to run Python scripts:

1. **Using `uv run` (recommended):**
   ```bash
   uv run python scripts/transcribe.py <video_id>
   ```

2. **Activating the virtual environment:**
   ```bash
   source .venv/bin/activate
   python scripts/transcribe.py <video_id>
   ```

Both methods work identically. The `uv run` method automatically ensures you're using the correct Python version and dependencies.

## Configuration

The project is configured through environment variables in the `.env` file.

-   `OPENAI_API_KEY`: Your OpenAI API key for generating images.
-   `WP_URL`: The URL of your WordPress site.
-   `WP_USER`: Your WordPress username.
-   `WP_PASSWORD`: Your WordPress application password.