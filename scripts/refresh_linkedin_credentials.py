#!/usr/bin/env python3
"""
LinkedIn API Credentials Refresh Tool

This script helps refresh or create new LinkedIn API credentials for posting automation.
It uses the OAuth 2.0 flow to authenticate with LinkedIn.

Prerequisites:
1. Create a LinkedIn App at https://www.linkedin.com/developers/apps
2. Add these permissions: openid, profile, w_member_social
3. Set redirect URL to: http://localhost:8000/callback
4. Create ~/.linkedin_credentials.json with your client_id and client_secret

Usage:
    python scripts/refresh_linkedin_credentials.py
"""

import sys
import os
from pathlib import Path

# Add scripts directory to path to import linkedin_poster module
sys.path.insert(0, str(Path(__file__).parent))

from linkedin_poster import (
    load_credentials,
    authorize,
    get_user_info,
    CONFIG_FILE
)


def refresh_credentials():
    """Refresh or create new LinkedIn API credentials."""
    print("\nChecking LinkedIn credentials...")

    # Check if config file exists
    if not CONFIG_FILE.exists():
        print(f"\n✗ Error: Credentials file not found: {CONFIG_FILE}")
        print("\nPlease create the file with your LinkedIn app credentials:")
        print("""
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "access_token": ""
}
        """)
        return False

    # Load current credentials
    credentials = load_credentials()

    # Check if we have an access token
    if credentials.get('access_token'):
        print(f"Found existing access token in: {CONFIG_FILE}")
        print("Testing current credentials...")

        try:
            user_info = get_user_info(credentials['access_token'])
            print(f"✓ Credentials are valid!")
            print(f"✓ Authenticated as: {user_info.get('name', 'Unknown')}")
            print(f"  Email: {user_info.get('email', 'N/A')}")
            print("\nNo refresh needed - credentials are working.")
            return True
        except Exception as e:
            print(f"✗ Current credentials are invalid: {e}")
            print("Starting re-authorization flow...")
    else:
        print("No access token found. Starting authorization flow...")

    # Perform OAuth authorization
    try:
        access_token = authorize()

        # Test the new credentials
        print("\nTesting new credentials with LinkedIn API...")
        user_info = get_user_info(access_token)
        print(f"✓ Successfully authenticated as: {user_info.get('name', 'Unknown')}")
        print(f"  Email: {user_info.get('email', 'N/A')}")

        return True

    except Exception as e:
        print(f"\n✗ Error during authorization: {e}")
        return False


if __name__ == '__main__':
    print("LinkedIn API Credentials Refresh Tool")
    print("=" * 50)

    success = refresh_credentials()

    if success:
        print("\n" + "=" * 50)
        print("All done! Your LinkedIn credentials are ready to use.")
        print(f"Credentials saved in: {CONFIG_FILE}")
    else:
        print("\n" + "=" * 50)
        print("There was an issue with the credentials.")
        print("Please check the error messages above and try again.")
        exit(1)
