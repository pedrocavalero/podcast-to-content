import os
import requests
import argparse
from dotenv import load_dotenv
import markdown
from datetime import datetime

load_dotenv() # Load environment variables from .env file

WP_URL = os.getenv("WP_URL")
WP_USER = os.getenv("WP_USER")
WP_PASSWORD = os.getenv("WP_PASSWORD")

def get_headers():
    return {
        "Authorization": f"Basic {requests.auth._basic_auth_str(WP_USER, WP_PASSWORD)}"
    }

def get_id_by_slug(term_type, name):
    """
    Get the ID of a category or tag by its name (slugified search not always accurate, 
    so we search by name and fallback to create if needed for tags).
    """
    if not all([WP_URL, WP_USER, WP_PASSWORD]):
        return None

    # Search by name matches
    response = requests.get(
        f"{WP_URL}/wp-json/wp/v2/{term_type}",
        params={"search": name},
        auth=(WP_USER, WP_PASSWORD)
    )
    
    if response.status_code == 200:
        results = response.json()
        for item in results:
            if item['name'].lower() == name.lower():
                return item['id']
    return None

def create_tag(name):
    """Creates a new tag."""
    if not all([WP_URL, WP_USER, WP_PASSWORD]):
        return None
        
    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/tags",
        json={"name": name},
        auth=(WP_USER, WP_PASSWORD)
    )
    if response.status_code == 201:
        return response.json()['id']
    return None

def upload_to_wordpress(title, content_markdown, image_path=None, categories=None, tags=None, publish_date=None, status='draft'):
    """
    Uploads a blog post to WordPress, optionally with a featured image, categories, tags, and schedule.

    Args:
        title: The title of the blog post.
        content_markdown: The content of the blog post in Markdown format.
        image_path: The path to the featured image (optional).
        categories: List of category names (optional).
        tags: List of tag names (optional).
        publish_date: ISO 8601 formatted date string (optional) for scheduling.
        status: Post status ('draft', 'publish', 'future').
    """
    
    if not all([WP_URL, WP_USER, WP_PASSWORD]):
        print("Error: WordPress credentials (WP_URL, WP_USER, WP_PASSWORD) are not set in .env file or environment variables.")
        return

    # Remove the first line (title) from the Markdown content if it matches the title argument
    content_lines = content_markdown.splitlines()
    if content_lines and content_lines[0].strip().replace('#', '').strip() == title.strip():
         content_body_markdown = "\n".join(content_lines[1:])
    else:
         content_body_markdown = content_markdown

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
            f"{WP_URL}/wp-json/wp/v2/media",
            headers=headers,
            data=image_data,
            auth=(WP_USER, WP_PASSWORD)
        )

        if response.status_code == 201:
            image_id = response.json()["id"]
        else:
            print(f"Error uploading image: {response.text}")

    # Prepare categories and tags IDs
    category_ids = []
    if categories:
        for cat_name in categories:
            cat_id = get_id_by_slug('categories', cat_name.strip())
            if cat_id:
                category_ids.append(cat_id)
            else:
                print(f"Warning: Category '{cat_name}' not found. Skipping.")

    tag_ids = []
    if tags:
        for tag_name in tags:
            t_id = get_id_by_slug('tags', tag_name.strip())
            if not t_id:
                # Try creating the tag if it doesn't exist
                t_id = create_tag(tag_name.strip())
            
            if t_id:
                tag_ids.append(t_id)
            else:
                print(f"Warning: Could not find or create tag '{tag_name}'. Skipping.")

    # 2. Create the post
    post_data = {
        "title": title,
        "content": content_html, 
        "status": status,
        "categories": category_ids,
        "tags": tag_ids
    }
    
    if publish_date:
        post_data['date'] = publish_date
        if status == 'draft': 
            # If date is set, status usually should be 'future' if we want it scheduled, 
            # or 'publish' if the date is in the past. 
            # If the user specifically requested 'draft', WP keeps it as draft regardless of date.
            pass
            
    if image_id:
        post_data["featured_media"] = image_id

    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/posts",
        json=post_data,
        auth=(WP_USER, WP_PASSWORD)
    )

    if response.status_code == 201:
        print(f"Successfully published/scheduled blog post: {title}")
    else:
        print(f"Error publishing blog post: {response.text}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a blog post to WordPress.")
    
    # Positional arguments (for backward compatibility)
    parser.add_argument("title", type=str, help="The title of the blog post.")
    parser.add_argument("content_path", type=str, help="The path to the file containing the blog post content.")
    parser.add_argument("image_path", type=str, nargs='?', default=None, help="The path to the featured image (optional).")
    
    # Optional arguments
    parser.add_argument("--categories", type=str, help="Comma-separated list of category names.")
    parser.add_argument("--tags", type=str, help="Comma-separated list of tags.")
    parser.add_argument("--publish_date", type=str, help="ISO 8601 date string to schedule the post (e.g., 2023-10-27T10:00:00).")
    parser.add_argument("--status", type=str, default="draft", choices=['draft', 'publish', 'future'], help="Post status.")

    args = parser.parse_args()

    with open(args.content_path, "r") as f:
        content_markdown = f.read()

    cat_list = args.categories.split(',') if args.categories else []
    tag_list = args.tags.split(',') if args.tags else []

    upload_to_wordpress(
        args.title, 
        content_markdown, 
        args.image_path, 
        categories=cat_list, 
        tags=tag_list, 
        publish_date=args.publish_date,
        status=args.status
    )
