import os
import time
import json
from dotenv import load_dotenv
from pydantic import BaseModel
import google.oauth2.credentials
import google_auth_oauthlib.flow
import google.auth.transport.requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google import genai
from google.genai import types

# Pydantic schema for structured output from Gemini
class VideoTranslation(BaseModel):
    title: str
    description: str

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
    api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_AI_STUDIO_API_KEY")
    if not api_key:
        raise Exception("GOOGLE_API_KEY or GOOGLE_AI_STUDIO_API_KEY not found in .env file.")
    print("Initializing Gemini client...")
    return genai.Client(api_key=api_key)

def translate_metadata(gemini_client, title, description):
    prompt = f"""You are an expert YouTube content localizer and translator. 
Translate the following English video title and description into natural, engaging Brazilian Portuguese for a software developer audience.
Keep hashtags, emojis, URLs, and formatting identical. 

English Title: {title}
English Description: {description}"""

    try:
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=VideoTranslation,
            ),
        )
        # Parse the structured JSON response
        data = json.loads(response.text)
        return data.get('title', title), data.get('description', description)
    except Exception as e:
        print(f"Error translating metadata via Gemini: {e}")
        return None, None

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
        
        # 2. Retrieve uploads in 2026
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
                # Filter for 2026 videos only
                if published_at.startswith('2026'):
                    video_ids.append(item['snippet']['resourceId']['videoId'])
                elif published_at.startswith('2025') or published_at.startswith('2024'):
                    # Stops paginating since playlist is in reverse-chronological order
                    pass
            
            # Stop if we went past 2026
            latest_item_year = items[-1]['snippet']['publishedAt'][:4]
            if int(latest_item_year) < 2026:
                break
                
            next_page_token = playlist_items_response.get('nextPageToken')
            if not next_page_token:
                break
                
        print(f"Found {len(video_ids)} videos published in 2026.")
        
        # 3. Process each video to update localization
        updated_count = 0
        skipped_count = 0
        
        for idx, vid in enumerate(video_ids, 1):
            print(f"\n[{idx}/{len(video_ids)}] Processing Video ID: {vid}")
            try:
                # Fetch existing snippet AND localizations
                video_detail = youtube.videos().list(
                    part='snippet,localizations',
                    id=vid
                ).execute()
                
                if not video_detail.get('items'):
                    print(f"Video detail not found for ID: {vid}")
                    continue
                    
                video_item = video_detail['items'][0]
                snippet = video_item['snippet']
                localizations = video_item.get('localizations', {})
                
                title = snippet.get('title', '')
                description = snippet.get('description', '')
                print(f"Title: {title}")
                
                # Check if Portuguese localization ('pt' or 'pt-BR') already exists
                if 'pt' in localizations or 'pt-BR' in localizations:
                    print(f"Skipping: Portuguese localization already exists.")
                    skipped_count += 1
                    continue
                
                print("Translating title and description to Portuguese using Gemini...")
                translated_title, translated_desc = translate_metadata(gemini_client, title, description)
                
                if not translated_title or not translated_desc:
                    print("Translation failed. Skipping.")
                    continue
                
                print(f"Translated Title: {translated_title}")
                
                # Update snippet default language and localizations block
                snippet['defaultLanguage'] = snippet.get('defaultLanguage') or 'en'
                localizations['pt'] = {
                    'title': translated_title,
                    'description': translated_desc
                }
                
                # Execute update
                youtube.videos().update(
                    part='snippet,localizations',
                    body={
                        'id': vid,
                        'snippet': snippet,
                        'localizations': localizations
                    }
                ).execute()
                
                print(f"Successfully added Portuguese localization to video {vid}!")
                updated_count += 1
                
                time.sleep(1.5) # Sleep to respect API rate limits
                
            except HttpError as e:
                print(f"API Error processing video {vid}: {e}")
            except Exception as e:
                print(f"Error processing video {vid}: {e}")
                
        print(f"\n=== Retroactive Localization Completed ===")
        print(f"Total processed: {len(video_ids)}")
        print(f"Updated (Localized): {updated_count}")
        print(f"Skipped (Had translation): {skipped_count}")
        
    except Exception as e:
        print(f"Fatal Error: {e}")

if __name__ == '__main__':
    main()
