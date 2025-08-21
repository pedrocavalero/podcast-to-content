
import os
import argparse
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# The CLIENT_SECRETS_FILE contains your OAuth 2.0 credentials for this application.
CLIENT_SECRETS_FILE = 'client_secret.json'

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's YouTube account.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    
    # Check if credentials.json exists and is valid
    credentials = None
    if os.path.exists('credentials.json'):
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_file('credentials.json', SCOPES)

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
        
        with open('credentials.json', 'w') as f:
            f.write(credentials.to_json())
    
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def upload_video(youtube, video_path, title, description):
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'categoryId': '28' # Science & Technology. You can change this.
        },
        'status': {
            'privacyStatus': 'private' # 'public', 'private', or 'unlisted'
        }
    }

    # Call the API's videos.insert method to upload the video.
    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=MediaFileUpload(video_path, chunksize=-1, resumable=True)
    )

    print('Uploading video...')
    response = None
    while response is None:
        status, response = insert_request.next_chunk()
        if status:
            print(f'Uploaded {int(status.resumable_progress * 100)}%')

    print(f'Video id "{response.get("id")}" was successfully uploaded.')
    print(f'Video URL: https://www.youtube.com/watch?v={response.get("id")}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload a video to YouTube.')
    parser.add_argument('--file', required=True, help='Path to the video file.')
    parser.add_argument('--title', required=True, help='Title of the video.')
    parser.add_argument('--description', required=True, help='Description of the video.')

    args = parser.parse_args()

    try:
        youtube = get_authenticated_service()
        upload_video(youtube, args.file, args.title, args.description)
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content.decode("utf-8")}')
    except Exception as e:
        print(f'An error occurred: {e}')
