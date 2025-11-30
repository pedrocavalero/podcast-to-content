#!/usr/bin/env python3
"""
LinkedIn Post Automation Script
Posts markdown articles with images to LinkedIn using the official LinkedIn API.

Prerequisites:
1. Create a LinkedIn App at https://www.linkedin.com/developers/apps
2. Add these permissions: w_member_social, r_liteprofile
3. Set redirect URL to: http://localhost:8000/callback
4. Get your Client ID and Client Secret

Usage:
    python scripts/linkedin_poster.py --markdown post.md --image image.png
"""

import argparse
import json
import os
import sys
import webbrowser
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests
import markdown


# Configuration
CONFIG_FILE = Path.home() / ".linkedin_credentials.json"
REDIRECT_URI = "http://localhost:8000/callback"
AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
API_BASE = "https://api.linkedin.com/v2"
LINKEDIN_VERSION = "202501"  # YYYYMM format


class AuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP server to handle OAuth callback"""
    auth_code = None

    def do_GET(self):
        """Handle GET request from OAuth redirect"""
        query = urlparse(self.path).query
        params = parse_qs(query)

        if 'code' in params:
            AuthCallbackHandler.auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html>
                <body>
                    <h1>Authorization successful!</h1>
                    <p>You can close this window and return to the terminal.</p>
                </body>
                </html>
            """)
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Authorization failed")

    def log_message(self, format, *args):
        """Suppress log messages"""
        pass


def load_credentials():
    """Load LinkedIn app credentials from config file"""
    if not CONFIG_FILE.exists():
        print(f"\nCredentials file not found: {CONFIG_FILE}")
        print("\nPlease create the file with your LinkedIn app credentials:")
        print(json.dumps({
            "client_id": "YOUR_CLIENT_ID",
            "client_secret": "YOUR_CLIENT_SECRET",
            "access_token": ""
        }, indent=2))
        sys.exit(1)

    with open(CONFIG_FILE) as f:
        return json.load(f)


def save_credentials(credentials):
    """Save credentials to config file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(credentials, f, indent=2)
    os.chmod(CONFIG_FILE, 0o600)  # Make file readable only by owner


def get_authorization_url(client_id):
    """Generate LinkedIn authorization URL"""
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': REDIRECT_URI,
        'state': 'random_string_for_security',
        'scope': 'openid profile w_member_social'  # Updated to use OpenID Connect
    }

    url_parts = []
    for key, value in params.items():
        url_parts.append(f"{key}={requests.utils.quote(value)}")

    return f"{AUTH_URL}?{'&'.join(url_parts)}"


def get_access_token(client_id, client_secret, auth_code):
    """Exchange authorization code for access token"""
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(TOKEN_URL, data=data)
    response.raise_for_status()

    return response.json()['access_token']


def authorize():
    """Perform OAuth authorization flow"""
    credentials = load_credentials()

    # Generate authorization URL
    auth_url = get_authorization_url(credentials['client_id'])

    print("\n=== LinkedIn Authorization ===")
    print("\nOpening browser for authorization...")
    print(f"If browser doesn't open, visit this URL:\n{auth_url}\n")

    # Open browser
    webbrowser.open(auth_url)

    # Start local server to receive callback
    print("Waiting for authorization (this will start a local server on port 8000)...")
    server = HTTPServer(('localhost', 8000), AuthCallbackHandler)
    server.handle_request()  # Handle one request then stop

    if not AuthCallbackHandler.auth_code:
        print("Authorization failed!")
        sys.exit(1)

    # Exchange code for token
    print("\nExchanging authorization code for access token...")
    access_token = get_access_token(
        credentials['client_id'],
        credentials['client_secret'],
        AuthCallbackHandler.auth_code
    )

    # Save token
    credentials['access_token'] = access_token
    save_credentials(credentials)

    print("✓ Authorization successful! Token saved.")
    return access_token


def get_user_info(access_token):
    """Get LinkedIn user information using OpenID Connect"""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    # Use OpenID Connect userinfo endpoint
    response = requests.get(f"{API_BASE}/userinfo", headers=headers)
    response.raise_for_status()

    return response.json()


def upload_image(access_token, image_path, person_urn):
    """Upload image to LinkedIn"""
    # Step 1: Register upload
    headers = {
        'Authorization': f'Bearer {access_token}',
        'LinkedIn-Version': LINKEDIN_VERSION,
        'Content-Type': 'application/json'
    }

    register_data = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": person_urn,
            "serviceRelationships": [{
                "relationshipType": "OWNER",
                "identifier": "urn:li:userGeneratedContent"
            }]
        }
    }

    response = requests.post(
        f"{API_BASE}/assets?action=registerUpload",
        headers=headers,
        json=register_data
    )
    response.raise_for_status()
    upload_info = response.json()['value']

    # Step 2: Upload image
    upload_url = upload_info['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
    asset_urn = upload_info['asset']

    with open(image_path, 'rb') as f:
        image_data = f.read()

    upload_headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.put(upload_url, headers=upload_headers, data=image_data)
    response.raise_for_status()

    return asset_urn


def markdown_to_text(markdown_path):
    """Convert markdown file to plain text"""
    with open(markdown_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert markdown to HTML then strip tags for plain text
    html = markdown.markdown(md_content)

    # Simple HTML tag removal (for better results, use BeautifulSoup)
    import re
    text = re.sub('<[^<]+?>', '', html)

    # Clean up extra whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)

    return text.strip()


def create_post(access_token, text, image_asset_urn=None):
    """Create a LinkedIn post"""
    # Get user info using OpenID Connect
    user_info = get_user_info(access_token)
    # OpenID Connect returns 'sub' instead of 'id'
    person_urn = f"urn:li:person:{user_info['sub']}"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'LinkedIn-Version': LINKEDIN_VERSION,
        'Content-Type': 'application/json'
    }

    # Prepare post data
    post_data = {
        "author": person_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    # Add image if provided
    if image_asset_urn:
        post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
        post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [{
            "status": "READY",
            "media": image_asset_urn
        }]

    # Create post
    response = requests.post(
        f"{API_BASE}/ugcPosts",
        headers=headers,
        json=post_data
    )
    response.raise_for_status()

    return response.json()


def main():
    parser = argparse.ArgumentParser(description='Post markdown article with image to LinkedIn')
    parser.add_argument('--markdown', '-m', required=True, help='Path to markdown file')
    parser.add_argument('--image', '-i', help='Path to image file (optional)')
    parser.add_argument('--auth', action='store_true', help='Force re-authorization')

    args = parser.parse_args()

    # Load credentials
    credentials = load_credentials()

    # Check if we need to authorize
    if args.auth or not credentials.get('access_token'):
        access_token = authorize()
    else:
        access_token = credentials['access_token']

    # Convert markdown to text
    print("\n=== Preparing Post ===")
    print(f"Reading markdown from: {args.markdown}")
    text = markdown_to_text(args.markdown)

    # Limit text to LinkedIn's character limit (3000 for posts)
    if len(text) > 3000:
        print(f"⚠ Warning: Text is {len(text)} characters, truncating to 3000")
        text = text[:2997] + "..."

    print(f"Post text length: {len(text)} characters")

    # Upload image if provided
    image_asset_urn = None
    if args.image:
        print(f"\nUploading image: {args.image}")
        try:
            user_info = get_user_info(access_token)
            person_urn = f"urn:li:person:{user_info['sub']}"  # OpenID Connect uses 'sub'
            image_asset_urn = upload_image(access_token, args.image, person_urn)
            print("✓ Image uploaded successfully")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                print("Token expired. Re-authorizing...")
                access_token = authorize()
                user_info = get_user_info(access_token)
                person_urn = f"urn:li:person:{user_info['sub']}"  # OpenID Connect uses 'sub'
                image_asset_urn = upload_image(access_token, args.image, person_urn)
            else:
                raise

    # Create post
    print("\n=== Creating LinkedIn Post ===")
    try:
        result = create_post(access_token, text, image_asset_urn)
        print("✓ Post created successfully!")
        print(f"\nPost ID: {result.get('id')}")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            print("Token expired. Re-authorizing...")
            access_token = authorize()
            result = create_post(access_token, text, image_asset_urn)
            print("✓ Post created successfully!")
        else:
            print(f"\n✗ Error creating post: {e}")
            print(f"Response: {e.response.text}")
            sys.exit(1)


if __name__ == '__main__':
    main()
