import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
import google.auth.transport.requests
from googleapiclient.discovery import build

# The CLIENT_SECRETS_FILE contains your OAuth 2.0 credentials for this application.
CLIENT_SECRETS_FILE = 'client_secret.json'

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's YouTube account.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CREDENTIALS_FILE = 'credentials_update.json'

def refresh_credentials():
    """Refresh or create new YouTube API credentials."""
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)

    credentials = None

    # Check if credentials file exists
    if os.path.exists(CREDENTIALS_FILE):
        print(f"Found existing credentials file: {CREDENTIALS_FILE}")
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(
            CREDENTIALS_FILE, SCOPES)

    # Try to refresh or create new credentials
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print("Credentials expired. Refreshing...")
            try:
                credentials.refresh(google.auth.transport.requests.Request())
                print("✓ Credentials refreshed successfully!")
            except Exception as e:
                print(f"Failed to refresh credentials: {e}")
                print("Re-authenticating...")
                credentials = None

        if not credentials:
            # Need full re-authentication
            print("\nStarting new authentication flow...")
            flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'  # For desktop apps
            auth_url, _ = flow.authorization_url(prompt='consent')
            print(f'\nPlease go to this URL and authorize the application:')
            print(f'{auth_url}\n')
            code = input('Enter the authorization code: ')
            flow.fetch_token(code=code)
            credentials = flow.credentials
            print("✓ Authentication successful!")

        # Save credentials
        with open(CREDENTIALS_FILE, 'w') as f:
            f.write(credentials.to_json())
        print(f"✓ Credentials saved to {CREDENTIALS_FILE}")
    else:
        print("✓ Credentials are already valid!")

    # Test the credentials by making a simple API call
    print("\nTesting credentials with YouTube API...")
    try:
        youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
        request = youtube.channels().list(part='snippet', mine=True)
        response = request.execute()

        if 'items' in response and len(response['items']) > 0:
            channel_title = response['items'][0]['snippet']['title']
            print(f"✓ Successfully connected to YouTube as: {channel_title}")
        else:
            print("✓ API connection successful!")

    except Exception as e:
        print(f"✗ Error testing credentials: {e}")
        return False

    return True

if __name__ == '__main__':
    print("YouTube API Credentials Refresh Tool")
    print("=" * 50)

    if not os.path.exists(CLIENT_SECRETS_FILE):
        print(f"✗ Error: {CLIENT_SECRETS_FILE} not found!")
        print("Please ensure your OAuth client secrets file is in the current directory.")
        exit(1)

    success = refresh_credentials()

    if success:
        print("\n" + "=" * 50)
        print("All done! Your credentials are ready to use.")
    else:
        print("\n" + "=" * 50)
        print("There was an issue with the credentials.")
        exit(1)
