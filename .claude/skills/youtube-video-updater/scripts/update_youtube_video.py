import os
import argparse
import google.oauth2.credentials
import google_auth_oauthlib.flow
import google.auth.transport.requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# The CLIENT_SECRETS_FILE contains your OAuth 2.0 credentials for this application.
CLIENT_SECRETS_FILE = 'client_secret.json'

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's YouTube account.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CREDENTIALS_FILE = 'credentials_update.json'

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    
    # Check if credentials file exists and is valid
    credentials = None
    if os.path.exists(CREDENTIALS_FILE):
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(CREDENTIALS_FILE, SCOPES)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(google.auth.transport.requests.Request())
        else:
            flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob' # For desktop apps
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f'Please go to this URL: {auth_url}')
            code = input('Enter the authorization code: ')
            flow.fetch_token(code=code)
            credentials = flow.credentials
        
        with open(CREDENTIALS_FILE, 'w') as f:
            f.write(credentials.to_json())
    
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def update_video_schedule(youtube, video_id, publish_at):
    print(f"Scheduling video {video_id} for {publish_at}...")
    try:
        # First, ensure the video is private, as publishAt only works for private videos
        # However, usually we can set both in one go.
        # But to be safe and ensure the transition is correct, we send both.
        
        body = {
            'id': video_id,
            'status': {
                'privacyStatus': 'private',
                'publishAt': publish_at,
                'selfDeclaredMadeForKids': False 
            }
        }
        
        # We need to get the categoryId and Title/Description if we don't want to overwrite them?
        # Actually videos.update is a partial update if we use parts properly, 
        # BUT 'snippet' and 'status' are parts. 
        # If we only send 'status', 'snippet' should remain untouched?
        # The docs say: "The resource passed in the body must include the id property."
        # And "The list of parts that the request is updating."
        
        request = youtube.videos().update(
            part='status',
            body=body
        )
        response = request.execute()
        print(f"Successfully scheduled video {video_id} for date {response['status']['publishAt']}.")
        
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred during scheduling: {e.content.decode("utf-8")}')

def add_video_to_playlists(youtube, video_id, playlist_ids):
    for playlist_id in playlist_ids:
        print(f"Adding video {video_id} to playlist {playlist_id}...")
        try:
            body = {
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
            request = youtube.playlistItems().insert(
                part='snippet',
                body=body
            )
            response = request.execute()
            print(f"Successfully added to playlist {playlist_id}.")
            
        except HttpError as e:
            if e.resp.status == 409:
                print(f"Video {video_id} is already in playlist {playlist_id}.")
            else:
                print(f'An HTTP error {e.resp.status} occurred while adding to playlist {playlist_id}: {e.content.decode("utf-8")}')


def get_playlist_id_by_name(youtube, playlist_name):
    # Retrieve the user's playlists (first page only for now, can be paginated)
    # We might need to iterate through pages if the user has many playlists.
    print(f"Searching for playlist '{playlist_name}'...")
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
    
    print(f"Warning: Playlist '{playlist_name}' not found.")
    return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update a YouTube video schedule and playlists.')
    parser.add_argument('--video_id', required=True, help='The ID of the YouTube video.')
    parser.add_argument('--schedule', help='ISO 8601 date-time string to schedule the video (e.g., 2025-12-25T10:00:00Z).')
    parser.add_argument('--playlists', nargs='+', help='List of playlist IDs or Names to add the video to.')

    args = parser.parse_args()

    if not args.schedule and not args.playlists:
        print("No action specified. Please provide --schedule or --playlists.")
        exit(1)

    try:
        youtube = get_authenticated_service()
        
        if args.schedule:
            update_video_schedule(youtube, args.video_id, args.schedule)
            
        if args.playlists:
            # Resolve names to IDs
            final_playlist_ids = []
            for plist in args.playlists:
                # Simple heuristic: if it looks like an ID, keep it, else search.
                # Playlist IDs usually start with PL or UU or FL, etc. and are long.
                # But names can be anything. We'll search for everything that isn't obviously an ID?
                # Actually, searching by name is safer if we want to support names.
                # But we don't want to search if it IS an ID.
                # Let's try to find it. If we find it by name, use that ID.
                # If we don't find it, assume it might be an ID and try to use it?
                # Or just prioritize name lookup.
                
                found_id = get_playlist_id_by_name(youtube, plist)
                if found_id:
                    final_playlist_ids.append(found_id)
                else:
                    # If not found by name, assume it is an ID
                    print(f"Could not find playlist with name '{plist}', assuming it is an ID.")
                    final_playlist_ids.append(plist)

            if final_playlist_ids:
                add_video_to_playlists(youtube, args.video_id, final_playlist_ids)
            
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content.decode("utf-8")}')
    except Exception as e:
        print(f'An error occurred: {e}')
