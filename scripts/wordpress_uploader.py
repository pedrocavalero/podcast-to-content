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

def get_post_id_by_title(title):
    """
    Get the ID of a post by its title.
    """
    if not all([WP_URL, WP_USER, WP_PASSWORD]):
        return None

    response = requests.get(
        f"{WP_URL}/wp-json/wp/v2/posts",
        params={"search": title, "per_page": 1}, # Limit to 1 result as we expect unique titles
        auth=(WP_USER, WP_PASSWORD)
    )

    if response.status_code == 200:
        results = response.json()
        for item in results:
            if item['title']['rendered'].lower() == title.lower(): # Exact title match
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

    # Remove the first line (title/subject) if it matches the title, starts with Subject/H1, to avoid double H1
    content_lines = content_markdown.splitlines()
    while content_lines and not content_lines[0].strip():
        content_lines.pop(0)

    if content_lines:
        first_line = content_lines[0].strip()
        first_line_clean = first_line.replace('#', '').strip()
        if (first_line_clean.lower() == title.strip().lower() or 
            first_line.startswith('# Subject:') or 
            first_line.startswith('Subject:') or
            (first_line.startswith('#') and not first_line.startswith('##'))):
            content_lines.pop(0)

    while content_lines and not content_lines[0].strip():
        content_lines.pop(0)

    content_body_markdown = "\n".join(content_lines)

    # Convert Markdown content to HTML
    content_html = markdown.markdown(content_body_markdown)

    # Auto-embed YouTube videos and make links clickable
    import re
    yt_regex = r"(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]+)(?:&\S*)?)"
    
    # 1. Turn plain text YouTube URLs into clickable links
    def make_clickable(match):
        url = match.group(1)
        start_idx = match.start()
        prefix = content_html[max(0, start_idx-15):start_idx]
        if 'href="' in prefix or 'src="' in prefix:
            return url
        return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>'
    
    content_html = re.sub(yt_regex, make_clickable, content_html)

    # 2. Append Gutenberg YouTube Embed Block for each unique video
    matches = re.findall(yt_regex, content_body_markdown)
    if matches:
        embeds = []
        seen_ids = set()
        for url, video_id in matches:
            if video_id not in seen_ids:
                seen_ids.add(video_id)
                embed_block = (
                    f'\n\n<!-- wp:embed {{"url":"{url}","type":"video","providerNameSlug":"youtube","responsive":true,"className":"wp-embed-aspect-16-9 wp-has-aspect-ratio"}} -->\n'
                    f'<figure class="wp-block-embed is-type-video is-provider-youtube wp-block-embed-youtube wp-embed-aspect-16-9 wp-has-aspect-ratio">\n'
                    f'<div class="wp-block-embed__wrapper">\n'
                    f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>\n'
                    f'</div>\n'
                    f'</figure>\n'
                    f'<!-- /wp:embed -->'
                )
                embeds.append(embed_block)
        if embeds:
            content_html += "\n" + "\n".join(embeds)

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

    # Check if a post with this title already exists
    existing_post_id = get_post_id_by_title(title)

    if existing_post_id:
        # Update existing post
        response = requests.post( # WordPress API uses POST for updates with _method=PUT
            f"{WP_URL}/wp-json/wp/v2/posts/{existing_post_id}",
            json=post_data,
            params={"_method": "PUT"}, # Explicitly tell WP to treat this as a PUT
            auth=(WP_USER, WP_PASSWORD)
        )
        if response.status_code == 200: # 200 OK for successful update
            print(f"Successfully updated blog post: {title} (ID: {existing_post_id})")
        else:
            print(f"Error updating blog post (ID: {existing_post_id}): {response.text}")
    else:
        # Create new post
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
