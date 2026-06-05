import os
import re
import time
from dotenv import load_dotenv
import google.oauth2.credentials
import google_auth_oauthlib.flow
import google.auth.transport.requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google import genai

# YouTube configurations
CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
CREDENTIALS_PATHS = ['credentials_update.json', 'credentials.json']

def get_youtube_service():
    credentials = None
    for path in CREDENTIALS_PATHS:
        if os.path.exists(path):
            try:
                print(f"Loading YouTube credentials from {path}...")
                credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(path, SCOPES)
                if credentials and credentials.valid:
                    break
                elif credentials and credentials.expired and credentials.refresh_token:
                    print("Refreshing expired credentials...")
                    credentials.refresh(google.auth.transport.requests.Request())
                    break
            except Exception as e:
                print(f"Error loading credentials from {path}: {e}")
                
    if not credentials or not credentials.valid:
        raise Exception("No valid YouTube credentials found. Please authenticate first.")
    return build('youtube', 'v3', credentials=credentials)

def get_gemini_client():
    load_dotenv()
    # Check both keys, preferring GOOGLE_API_KEY then GOOGLE_AI_STUDIO_API_KEY
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_AI_STUDIO_API_KEY")
    if not api_key:
        raise Exception("GOOGLE_API_KEY or GOOGLE_AI_STUDIO_API_KEY not found in .env file.")
    print(f"Initializing Gemini client...")
    return genai.Client(api_key=api_key)

def generate_tags(gemini_client, title, description):
    prompt = f"""Analyze the title and description of this YouTube video for a software developer audience. 
Generate a list of 10 to 15 relevant, high-search-volume keywords/tags for YouTube SEO. 
Return ONLY a comma-separated list of these tags (e.g., "tag1, tag2, tag3"). 
Do not include numbering, explanation, formatting, markdown, or any other text. Keep tags concise.

Title: {title}
Description: {description}"""
    
    try:
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        tags_text = response.text.strip()
        # Clean up tags formatting if the model included quotes or markdown code blocks
        tags_text = re.sub(r'^```[a-zA-Z]*\n', '', tags_text)
        tags_text = re.sub(r'\n```$', '', tags_text)
        tags_text = tags_text.replace('"', '').replace('`', '').strip()
        
        tags = [t.strip() for t in tags_text.split(',') if t.strip()]
        return tags
    except Exception as e:
        print(f"Error generating tags via Gemini: {e}")
        return []

def main():
    try:
        youtube = get_youtube_service()
        gemini_client = get_gemini_client()
        
        # 1. Get the Uploads Playlist ID
        channels_response = youtube.channels().list(
            mine=True,
            part='contentDetails'
        ).execute()
        
        uploads_playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        
        # 2. Retrieve uploads in 2025/2026
        video_ids = []
        next_page_token = None
        print("Retrieving upload playlist items...")
        
        while True:
            playlist_items_response = youtube.playlistItems().list(
                part='snippet',
                playlistId=uploads_playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()
            
            items = playlist_items_response.get('items', [])
            if not items:
                break
                
            for item in items:
                published_at = item['snippet']['publishedAt']
                # Filter for 2025 and 2026 videos
                if published_at.startswith('2025') or published_at.startswith('2026'):
                    video_ids.append(item['snippet']['resourceId']['videoId'])
                elif published_at.startswith('2024') or published_at.startswith('2023') or published_at.startswith('2022'):
                    # Since uploads playlist is ordered by reverse publish date, we can stop early
                    pass
            
            # Stop paginating if we reached older videos
            latest_item_year = items[-1]['snippet']['publishedAt'][:4]
            if int(latest_item_year) < 2025:
                break
                
            next_page_token = playlist_items_response.get('nextPageToken')
            if not next_page_token:
                break
                
        print(f"Found {len(video_ids)} videos published in 2025-2026.")
        
        # 3. For each video, get full snippet, check tags, generate if empty, and update
        updated_count = 0
        skipped_count = 0
        
        for idx, vid in enumerate(video_ids, 1):
            print(f"\n[{idx}/{len(video_ids)}] Processing Video ID: {vid}")
            try:
                # Fetch full video details to get the existing snippet (to avoid wiping other metadata during update)
                video_detail = youtube.videos().list(
                    part='snippet',
                    id=vid
                ).execute()
                
                if not video_detail.get('items'):
                    print(f"Video detail not found for ID: {vid}")
                    continue
                    
                video_item = video_detail['items'][0]
                snippet = video_item['snippet']
                title = snippet.get('title', '')
                existing_tags = snippet.get('tags', [])
                
                print(f"Title: {title}")
                
                if existing_tags:
                    print(f"Skipping: Already has {len(existing_tags)} tags: {existing_tags}")
                    skipped_count += 1
                    continue
                
                description = snippet.get('description', '')
                print("Generating tags using Gemini...")
                generated = generate_tags(gemini_client, title, description)
                
                if not generated:
                    print("No tags generated. Skipping.")
                    continue
                    
                print(f"Generated {len(generated)} tags: {generated}")
                
                # Update the snippet object with new tags
                snippet['tags'] = generated
                
                # Execute the video update
                # Crucial: we must send the entire snippet to prevent resetting other fields!
                youtube.videos().update(
                    part='snippet',
                    body={
                        'id': vid,
                        'snippet': snippet
                    }
                ).execute()
                
                print(f"Successfully updated tags for video {vid}!")
                updated_count += 1
                
                # Small sleep to respect rate limits
                time.sleep(1)
                
            except HttpError as e:
                print(f"API Error processing video {vid}: {e}")
            except Exception as e:
                print(f"Error processing video {vid}: {e}")
                
        print(f"\n=== Retroactive Tagging Completed ===")
        print(f"Total processed: {len(video_ids)}")
        print(f"Updated:         {updated_count}")
        print(f"Skipped (had tags): {skipped_count}")
        
    except Exception as e:
        print(f"Fatal Error: {e}")

if __name__ == '__main__':
    main()
