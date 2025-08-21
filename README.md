# Podcast to Content

This project automates the process of converting a YouTube video into a series of blog posts, complete with featured images, and publishing them to WordPress.

## Features

- **YouTube Video Transcription:** Automatically transcribes the audio from a YouTube video.
- **Content Summarization:** Analyzes the transcript and identifies the main topics.
- **Blog Post Generation:** Creates multiple blog posts based on the identified topics.
- **AI-Powered Image Generation:** Generates a unique featured image for each blog post.
- **WordPress Integration:** Uploads the generated blog posts and featured images to a WordPress site.

## Workflow

The project follows this workflow:

1.  **Initialization:** Takes a YouTube video ID as input and creates a directory to store the generated assets.
2.  **Transcription:** Transcribes the YouTube video and saves the transcript to a file.
3.  **Content Analysis & Summarization:** Analyzes the transcript to identify the main topics and generates a summary for each.
4.  **Blog Post Generation:** Creates a separate blog post for each topic, using the summary and the full transcript for context.
5.  **Featured Image Generation:** Generates a featured image for each blog post using an AI text-to-image model.
6.  **WordPress Publication:** Publishes the blog posts to WordPress as drafts, with their corresponding featured images.

## Video Cuts Workflow

This workflow automates the process of extracting valuable segments from a YouTube video, generating corresponding thumbnails, and uploading them as new videos to a YouTube channel.

### Features

-   **YouTube Video Download:** Downloads the full video and its subtitles.
-   **Content Analysis & Cut Point Identification:** Analyzes the transcript to identify interesting and valuable video segments.
-   **Cuts Metadata Generation:** Creates a markdown file with titles, descriptions, and timestamps for each cut.
-   **Video Cutting:** Extracts the identified segments as separate video files.
-   **AI-Powered Thumbnail Generation:** Generates unique and descriptive thumbnails for each video cut using OpenAI gpt-image-1.
-   **Image Resizing:** Resizes generated thumbnails to YouTube's recommended dimensions (1280x720).
-   **YouTube Upload Integration:** Uploads the video cuts along with their generated thumbnails to a YouTube channel.

### Workflow

The video cuts workflow follows these steps:

1.  **Initialization:** Takes a YouTube video URL as input and creates a dedicated directory for assets.
2.  **Video and Subtitle Download:** Downloads the video and its auto-generated subtitles.
3.  **Content Analysis & Cut Point Identification:** Identifies interesting segments (cuts) within the video based on the transcript.
4.  **Cuts Metadata Generation:** Compiles metadata (title, description, timestamps) for each identified cut into a markdown file.
5.  **Video Cutting:** Creates individual video files for each cut.
6.  **Thumbnail Generation and Resizing:** Generates an AI-powered image for each cut's title and resizes it to the optimal YouTube thumbnail format.
7.  **Video Upload:** Uploads each video cut to YouTube, including its generated thumbnail.
8.  **Completion:** Notifies the user upon successful completion of the entire process.

## Requirements

- Python 3.x
- **ffmpeg**: Required for video cutting and frame extraction. Ensure it's installed and accessible in your system's PATH.
- A YouTube API key
- An OpenAI API key
- WordPress credentials (URL, username, and password)
- **Google Cloud Project Configuration for YouTube Uploads**:
    To enable YouTube video uploads, you need to configure a Google Cloud Project, enable the YouTube Data API v3, and create OAuth 2.0 Client ID credentials (Desktop app type). Download the `client_secret.json` file and place it in the project's root directory. Refer to the detailed steps provided during the initial setup of the `upload_youtube_video.py` script.

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/podcast-to-content.git
    cd podcast-to-content
    ```

2.  Create a virtual environment and activate it:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

4.  Create a `.env` file by copying the example file:
    ```bash
    cp .env.example .env
    ```

5.  Edit the `.env` file and add your API keys and WordPress credentials:
    ```
    OPENAI_API_KEY="your-openai-api-key"
    WP_URL="your-wordpress-site-url"
    WP_USER="your-wordpress-username"
    WP_PASSWORD="your-wordpress-password"
    ```

## Usage

The project is designed to be run as an automated workflow. The `autoblog.workflow.md` file describes the steps in detail.

To run the individual scripts:

-   **Transcribe a video:**
    ```bash
    python transcribe.py <video_id>
    ```

-   **Generate an image:**
    ```bash
    python generate_image.py "<prompt>" <output_path>
    ```

-   **Upload a post to WordPress:**
    ```bash
    python wordpress_uploader.py "<title>" <content_path> [image_path]
    ```

-   **Run the video cuts workflow:**
    ```bash
    # Refer to video-cuts.workflow.md for detailed steps and execution
    # Example:
    # source .venv/bin/activate && python your_script_to_run_workflow.py <youtube_url>
    ```

## Configuration

The project is configured through environment variables. The following variables are required:

-   `OPENAI_API_KEY`: Your OpenAI API key for generating images.
-   `WP_URL`: The URL of your WordPress site.
-   `WP_USER`: Your WordPress username.
-   `WP_PASSWORD`: Your WordPress application password.
