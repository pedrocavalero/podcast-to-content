import os
import argparse
import google.oauth2.credentials
import google_auth_oauthlib.flow
import google.auth.transport.requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

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

def update_thumbnail(youtube, video_id, thumbnail_path):
    print(f"Updating thumbnail for video {video_id}...")

    if not os.path.exists(thumbnail_path):
        print(f"Error: Thumbnail file not found at {thumbnail_path}")
        return False

    try:
        request = youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumbnail_path, chunksize=-1, resumable=True)
        )
        response = request.execute()
        print(f"Successfully updated thumbnail for video {video_id}.")
        print(f"Thumbnail URL: {response['items'][0]['default']['url']}")
        return True

    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content.decode("utf-8")}')
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update a YouTube video thumbnail.')
    parser.add_argument('--video_id', required=True, help='The ID of the YouTube video.')
    parser.add_argument('--thumbnail', required=True, help='Path to the thumbnail image file.')

    args = parser.parse_args()

    try:
        youtube = get_authenticated_service()
        update_thumbnail(youtube, args.video_id, args.thumbnail)

    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content.decode("utf-8")}')
    except Exception as e:
        print(f'An error occurred: {e}')
