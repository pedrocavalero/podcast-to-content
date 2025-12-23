# LinkedIn Poster Setup Guide

This guide will help you set up the LinkedIn poster script to automatically post markdown articles with images to your LinkedIn profile.

## Prerequisites

- Python 3.6 or higher
- A LinkedIn account
- LinkedIn Developer App credentials

## Step 1: Create a LinkedIn App

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/apps)
2. Click "Create app"
3. Fill in the required information:
   - **App name**: Choose any name (e.g., "My Content Poster")
   - **LinkedIn Page**: Select or create a LinkedIn page (required)
   - **App logo**: Upload any logo
   - **Legal agreement**: Check the box
4. Click "Create app"

## Step 2: Add Required Products

1. Go to the "Products" tab of your app
2. Find and add these products:
   - **"Sign In with LinkedIn using OpenID Connect"** - Click "Request access"
   - **"Share on LinkedIn"** or **"Community Management"** - For posting permissions

Note: Some products may require review/approval. You can start development immediately in Development mode.

## Step 3: Configure App Settings

1. Go to the "Auth" tab of your app
2. Under "OAuth 2.0 settings":
   - Add redirect URL: `http://localhost:8000/callback`
3. The required scopes (`openid`, `profile`, `w_member_social`) will be automatically available once you add the products above
4. Click "Update"

## Step 4: Get Your Credentials

1. In the "Auth" tab, find:
   - **Client ID**
   - **Client Secret** (click "Show" to reveal it)
2. Copy these values

## Step 5: Install Python Dependencies

```bash
pip install requests markdown
```

Or add to your `requirements.txt`:
```
requests>=2.31.0
markdown>=3.5.0
```

## Step 6: Create Credentials File

Create a file at `~/.linkedin_credentials.json` with your credentials:

```json
{
  "client_id": "YOUR_CLIENT_ID_HERE",
  "client_secret": "YOUR_CLIENT_SECRET_HERE",
  "access_token": ""
}
```

Replace `YOUR_CLIENT_ID_HERE` and `YOUR_CLIENT_SECRET_HERE` with your actual credentials from Step 3.

Make sure the file has secure permissions:
```bash
chmod 600 ~/.linkedin_credentials.json
```

## Step 7: Authorize the App (First Time Only)

Run the script with the `--auth` flag:

```bash
python scripts/linkedin_poster.py --auth --markdown test.md
```

This will:
1. Open your browser to LinkedIn's authorization page
2. Ask you to grant permissions to the app
3. Redirect back to localhost and automatically capture the authorization code
4. Exchange the code for an access token
5. Save the token to your credentials file

## Usage

### Post markdown article without image:
```bash
python scripts/linkedin_poster.py --markdown article.md
```

### Post markdown article with image:
```bash
python scripts/linkedin_poster.py --markdown article.md --image featured.png
```

### Force re-authorization (if token expires):
```bash
python scripts/linkedin_poster.py --auth --markdown article.md
```

## Notes

- **Access tokens expire**: LinkedIn access tokens are valid for 60 days. When it expires, run with `--auth` to get a new one
- **Character limit**: LinkedIn posts are limited to 3000 characters. The script will automatically truncate longer posts
- **Markdown conversion**: The script converts markdown to plain text. Formatting like bold, italics, and links will be lost
- **Image requirements**:
  - Supported formats: JPG, PNG
  - Max file size: 5 MB
  - Recommended size: 1200x627 pixels

## Troubleshooting

### "Authorization failed!"
- Make sure the redirect URI in your LinkedIn app matches exactly: `http://localhost:8000/callback`
- Check that port 8000 is not in use by another application
- Try using `--auth` flag to force re-authorization

### "401 Unauthorized"
- Your access token has expired. Run with `--auth` to get a new one

### "403 Forbidden" or "Insufficient permissions"
- Make sure you've added the "Sign In with LinkedIn using OpenID Connect" product
- Add "Share on LinkedIn" or "Community Management" product for posting permissions
- Some products require approval - check the "Products" tab for status
- In Development mode, you can test with your own account before approval

### "Image upload failed"
- Check image file size (must be < 5 MB)
- Verify image format (JPG or PNG)
- Ensure file path is correct

## Example

```bash
# Create a test markdown file
echo "# Test Post

This is a test post from my automation script!

- Point 1
- Point 2" > test.md

# Post it to LinkedIn
python scripts/linkedin_poster.py --markdown test.md
```

## Security Notes

- **Never commit** `.linkedin_credentials.json` to version control
- The credentials file is automatically set to read-only for your user (chmod 600)
- Access tokens should be kept secure and rotated regularly
- Consider using environment variables for production deployments
