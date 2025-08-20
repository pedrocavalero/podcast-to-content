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

## Requirements

- Python 3.x
- A YouTube API key
- An OpenAI API key
- WordPress credentials (URL, username, and password)

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

## Configuration

The project is configured through environment variables. The following variables are required:

-   `OPENAI_API_KEY`: Your OpenAI API key for generating images.
-   `WP_URL`: The URL of your WordPress site.
-   `WP_USER`: Your WordPress username.
-   `WP_PASSWORD`: Your WordPress application password.
