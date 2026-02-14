
import os
import re
import subprocess
import argparse

def parse_shorts_md(md_file_path):
    shorts = []
    current_short = {}
    
    with open(md_file_path, 'r') as f:
        content = f.read()
    
    # Split by separator
    sections = content.split('---')
    
    for section in sections:
        section = section.strip()
        if not section:
            continue
            
        # Parse Title
        title_match = re.search(r'^##\s+(.+)$', section, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
            # Add #Shorts to title if not present (as per workflow)
            if "#Shorts" not in title:
                title += " #Shorts"
            current_short['title'] = title
        
        # Parse Filename
        file_match = re.search(r'Name of the short file:\s+(.+)$', section, re.MULTILINE)
        if file_match:
            current_short['filename'] = file_match.group(1).strip()
            
        # Parse Description
        desc_match = re.search(r'\*\*Description:\*\*\s+(.+)', section, re.DOTALL)
        if desc_match:
            current_short['description'] = desc_match.group(1).strip()
            
        if 'title' in current_short and 'filename' in current_short and 'description' in current_short:
            shorts.append(current_short)
            current_short = {}
            
    return shorts

def upload_shorts(shorts_dir, DryRun=False):
    md_file_path = os.path.join(shorts_dir, 'shorts.md')
    if not os.path.exists(md_file_path):
        print(f"Error: {md_file_path} not found.")
        return

    shorts = parse_shorts_md(md_file_path)
    print(f"Found {len(shorts)} shorts to upload.")
    
    for short in shorts:
        video_path = os.path.join(shorts_dir, short['filename'])
        if not os.path.exists(video_path):
            print(f"Warning: Video file {video_path} not found. Skipping.")
            continue
            
        print(f"Uploading {short['filename']}...")
        print(f"Title: {short['title']}")
        
        cmd = [
            "python3", "scripts/upload_youtube_short.py",
            "--file", video_path,
            "--title", short['title'],
            "--description", short['description']
        ]
        
        if DryRun:
            print(f"Dry Run: {' '.join(cmd)}")
        else:
            try:
                subprocess.run(cmd, check=True)
                print(f"Successfully uploaded {short['filename']}")
            except subprocess.CalledProcessError as e:
                print(f"Failed to upload {short['filename']}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload shorts from a directory based on shorts.md')
    parser.add_argument('shorts_dir', help='Directory containing shorts.md and video files')
    parser.add_argument('--dry-run', action='store_true', help='Print commands without executing')
    
    args = parser.parse_args()
    
    upload_shorts(args.shorts_dir, args.dry_run)
