import os
import argparse
import google.oauth2.credentials
import google_auth_oauthlib.flow
import google.auth.transport.requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import dateutil.parser

# Reuse the credentials file from the update script
CLIENT_SECRETS_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CREDENTIALS_FILE = 'credentials_update.json'

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    
    credentials = None
    if os.path.exists(CREDENTIALS_FILE):
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f'Please go to this URL: {auth_url}')
            code = input('Enter the authorization code: ')
            flow.fetch_token(code=code)
            credentials = flow.credentials
        
        with open(CREDENTIALS_FILE, 'w') as f:
            f.write(credentials.to_json())
    
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def get_playlist_id_by_name(youtube, playlist_name):
    # Same logic as update_youtube_video.py
    request = youtube.playlists().list(
        part='snippet',
        mine=True,
        maxResults=50
    )
    while request:
        response = request.execute()
        for item in response['items']:
            if item['snippet']['title'].lower() == playlist_name.lower():
                return item['id']
        request = youtube.playlists().list_next(request, response)
    return None

def list_videos(youtube, query):
    print(f"Fetching all uploads to search for query: '{query}'...")
    videos = []
    
    # 1. Get Uploads Playlist ID
    channels_response = youtube.channels().list(
        mine=True,
        part='contentDetails'
    ).execute()
    
    if not channels_response['items']:
        print("No channel found.")
        return []
        
    uploads_playlist_id = channels_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    # 2. Iterate through Uploads Playlist
    request = youtube.playlistItems().list(
        part='snippet,status',
        playlistId=uploads_playlist_id,
        maxResults=50
    )
    
    matching_videos = []
    
    while request:
        response = request.execute()
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            published_at = item['snippet']['publishedAt']
            privacy = item['status']['privacyStatus']
            
            # Check if query matches title or description (case-insensitive)
            if query.lower() in title.lower() or query.lower() in description.lower():
                matching_videos.append({
                    'id': video_id,
                    'title': title,
                    'published_at': published_at,
                    'privacy': privacy
                })
        
        request = youtube.playlistItems().list_next(request, response)
        
    # Sort by published_at ascending (Oldest first)
    matching_videos.sort(key=lambda x: x['published_at'])
    return matching_videos

def calculate_next_schedule_date(start_date, index, interval_days=1):
    # Daily strategy: Start Date + index * interval
    # Start date is a datetime object
    return start_date + timedelta(days=index * interval_days)

def main():
    parser = argparse.ArgumentParser(description='List and Schedule Channel Videos.')
    parser.add_argument('--query', required=True, help='Search query to filter videos (e.g. original video ID or title).')
    parser.add_argument('--start_date', help='Start date for scheduling (ISO 8601, e.g. 2025-12-07T12:00:00).')
    parser.add_argument('--interval', type=int, default=1, help='Interval in days between videos (default: 1).')
    parser.add_argument('--playlists', nargs='+', help='List of playlist IDs or Names.')
    parser.add_argument('--confirm', action='store_true', help='Execute the scheduling (otherwise dry-run).')
    parser.add_argument('--include_public', action='store_true', help='Include public videos in the list/schedule.')
    
    args = parser.parse_args()
    
    try:
        youtube = get_authenticated_service()
        all_videos = list_videos(youtube, args.query)
        
        # Filter videos
        videos = []
        for v in all_videos:
            if v['privacy'] == 'public' and not args.include_public:
                continue
            videos.append(v)
        
        if not videos:
            print("No videos found matching the query (excluding public ones).")
            return

        print(f"\nFound {len(videos)} videos:")
        for v in videos:
            print(f"[{v['privacy']}] {v['published_at']} - {v['title']} ({v['id']})")
            
        if not args.start_date:
            print("\nTo schedule these videos, provide --start_date and --confirm.")
            return

        # Prepare scheduling
        start_date_dt = dateutil.parser.parse(args.start_date)
        
        print("\nProposed Schedule:")
        for i, v in enumerate(videos):
            sched_date = calculate_next_schedule_date(start_date_dt, i, args.interval)
            print(f"Video {v['id']} -> {sched_date.isoformat()}")

        if not args.confirm:
            print("\nDry run complete. Use --confirm to apply changes.")
            return

        print("\nApplying changes...")
        
        # Resolve playlists
        playlist_ids = []
        if args.playlists:
            for plist in args.playlists:
                pid = get_playlist_id_by_name(youtube, plist)
                if pid:
                    playlist_ids.append(pid)
                else:
                    # Assume ID
                    playlist_ids.append(plist)
                    
        for i, v in enumerate(videos):
            video_id = v['id']
            sched_date = calculate_next_schedule_date(start_date_dt, i, args.interval)
            sched_str = sched_date.strftime('%Y-%m-%dT%H:%M:%S.000Z') # Force expected format
            
            print(f"Scheduling {video_id} for {sched_str}...")
            
            # Update Video
            try:
                youtube.videos().update(
                    part='status',
                    body={
                        'id': video_id,
                        'status': {
                            'privacyStatus': 'private',
                            'publishAt': sched_str,
                            'selfDeclaredMadeForKids': False
                        }
                    }
                ).execute()
                print("  - Scheduled.")
            except HttpError as e:
                print(f"  - Error scheduling: {e}")

            # Add to Playlists
            for pid in playlist_ids:
                try:
                    youtube.playlistItems().insert(
                        part='snippet',
                        body={
                            'snippet': {
                                'playlistId': pid,
                                'resourceId': {
                                    'kind': 'youtube#video',
                                    'videoId': video_id
                                }
                            }
                        }
                    ).execute()
                    print(f"  - Added to playlist {pid}.")
                except HttpError as e:
                    if e.resp.status == 409:
                        print(f"  - Already in playlist {pid}.")
                    else:
                        print(f"  - Error adding to playlist: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
