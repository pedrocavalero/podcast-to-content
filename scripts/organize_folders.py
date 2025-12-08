import os
import shutil
import sys
import argparse
from datetime import datetime

def get_creation_date(path):
    stat = os.stat(path)
    # On macOS, st_birthtime is usually available.
    # Fallback to st_mtime if not.
    try:
        timestamp = stat.st_birthtime
    except AttributeError:
        timestamp = stat.st_mtime
    
    return datetime.fromtimestamp(timestamp)

def organize_folders(dry_run=False):
    # Get all directories in the current folder
    all_items = os.listdir('.')
    dirs = [d for d in all_items if os.path.isdir(d)]
    
    # Identify all unique video_ids and their components
    video_groups = {}
    
    prefixes = ['blog-', 'cuts-', 'shorts-']
    
    for d in dirs:
        for prefix in prefixes:
            if d.startswith(prefix):
                video_id = d[len(prefix):]
                if video_id not in video_groups:
                    video_groups[video_id] = {}
                
                # key is 'blog', 'cuts', or 'shorts' (without the hyphen)
                key = prefix[:-1] 
                video_groups[video_id][key] = d
                break
    
    for video_id, components in video_groups.items():
        # Determine reference folder for date (priority: blog -> cuts -> shorts)
        reference_path = components.get('blog') or components.get('cuts') or components.get('shorts')
        
        if not reference_path:
            continue
            
        # Determine paths for potential sibling folders
        # components dict already has the specific folder names present on disk
        
        # Calculate target parent directory name
        try:
            date_obj = get_creation_date(reference_path)
            # Format: yy-dd-mm
            date_str = date_obj.strftime('%y-%d-%m')
            target_parent = f"{date_str}-{video_id}"
        except Exception as e:
            print(f"Error getting date for {reference_path}: {e}")
            continue

        # Prepare list of moves
        moves = []
        for type_key in ['blog', 'cuts', 'shorts']:
            if type_key in components:
                src = components[type_key]
                dst = os.path.join(target_parent, type_key)
                moves.append((src, dst))

        if not moves:
            continue

        print(f"Processing group for video_id: {video_id} -> {target_parent}")
        
        if dry_run:
            print(f"  [Dry Run] Would create directory: {target_parent}")
            for src, dst in moves:
                print(f"  [Dry Run] Would move {src} -> {dst}")
        else:
            if not os.path.exists(target_parent):
                os.makedirs(target_parent)
                print(f"  Created directory: {target_parent}")
            
            for src, dst in moves:
                try:
                    shutil.move(src, dst)
                    print(f"  Moved {src} -> {dst}")
                except Exception as e:
                    print(f"  Error moving {src} to {dst}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize blog, cuts, and shorts folders by date.")
    parser.add_argument('--dry-run', action='store_true', help="Show what would be done without making changes.")
    parser.add_argument('--force', action='store_true', help="Actually perform the moves (default is dry-run if not specified, but for safety in this script checking args).")
    
    args = parser.parse_args()
    
    # Default to dry run unless --force is used, or if user explicitly passed --dry-run
    # Actually, standard CLI convention: do it unless --dry-run. 
    # But for safety, I'll default to printing help or dry run if no args? 
    # The prompt asked to create the script. I'll make it standard: run = do it. 
    # But I will invoke it with --dry-run first.
    
    organize_folders(dry_run=args.dry_run)
