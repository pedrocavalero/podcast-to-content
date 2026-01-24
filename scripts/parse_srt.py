#!/usr/bin/env python3
"""Parse SRT subtitle file and extract clean text content."""

import sys
import re

def parse_srt(srt_file):
    """Extract text content from SRT file, removing timestamps and numbers."""
    with open(srt_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by double newlines to get subtitle blocks
    blocks = content.strip().split('\n\n')

    text_lines = []
    for block in blocks:
        lines = block.split('\n')
        # Skip the number and timestamp lines, keep only text
        for line in lines[2:]:  # First two lines are number and timestamp
            if line.strip() and not re.match(r'^\d+$', line.strip()) and not '-->' in line:
                text_lines.append(line.strip())

    return ' '.join(text_lines)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python parse_srt.py <srt_file>")
        sys.exit(1)

    srt_file = sys.argv[1]
    text = parse_srt(srt_file)
    print(text)
