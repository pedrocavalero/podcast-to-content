
import os
import requests
import argparse
from dotenv import load_dotenv
import markdown

def upload_to_wordpress(title, content_markdown, image_path=None):
    """
    Uploads a blog post to WordPress, optionally with a featured image.

    Args:
        title: The title of the blog post.
        content_markdown: The content of the blog post in Markdown format.
        image_path: The path to the featured image (optional).
    """
    load_dotenv() # Load environment variables from .env file

    # Get credentials from environment variables (now loaded from .env)
    wp_url = os.getenv("WP_URL")
    wp_user = os.getenv("WP_USER")
    wp_password = os.getenv("WP_PASSWORD")

    if not all([wp_url, wp_user, wp_password]):
        print("Error: WordPress credentials (WP_URL, WP_USER, WP_PASSWORD) are not set in .env file or environment variables.")
        return

    # Remove the first line (title) from the Markdown content
    content_lines = content_markdown.splitlines()
    content_body_markdown = "\n".join(content_lines[1:])

    # Convert Markdown content to HTML
    content_html = markdown.markdown(content_body_markdown)

    image_id = None
    if image_path and os.path.exists(image_path):
        # 1. Upload the image
        with open(image_path, "rb") as f:
            image_data = f.read()

        headers = {
            "Content-Disposition": f"attachment; filename={os.path.basename(image_path)}",
            "Content-Type": "image/png",
        }

        response = requests.post(
            f"{wp_url}/wp-json/wp/v2/media",
            headers=headers,
            data=image_data,
            auth=(wp_user, wp_password)
        )

        if response.status_code == 201:
            image_id = response.json()["id"]
        else:
            print(f"Error uploading image: {response.text}")

    # 2. Create the post
    post_data = {
        "title": title,
        "content": content_html, # Use HTML content here
        "status": "draft",
    }
    if image_id:
        post_data["featured_media"] = image_id

    response = requests.post(
        f"{wp_url}/wp-json/wp/v2/posts",
        json=post_data,
        auth=(wp_user, wp_password)
    )

    if response.status_code == 201:
        print(f"Successfully published blog post: {title}")
    else:
        print(f"Error publishing blog post: {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a blog post to WordPress.")
    parser.add_argument("title", type=str, help="The title of the blog post.")
    parser.add_argument("content_path", type=str, help="The path to the file containing the blog post content.")
    parser.add_argument("image_path", type=str, nargs='?', default=None, help="The path to the featured image (optional).")
    args = parser.parse_args()

    with open(args.content_path, "r") as f:
        content_markdown = f.read()

    upload_to_wordpress(args.title, content_markdown, args.image_path)
