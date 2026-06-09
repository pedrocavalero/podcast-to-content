#!/usr/bin/env python3
"""
LinkedIn PDF Carousel Generator
Generates high-engagement, modern dark-mode slide decks (1080x1080) from markdown text files.

Usage:
    python scripts/generate_linkedin_carousel.py --input slides.txt --output carousel.pdf
"""

import argparse
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


# Design Constants
SLIDE_SIZE = (1080, 1080)
BG_START = (15, 23, 42)    # Slate 900
BG_END = (30, 41, 59)      # Slate 800
COLOR_WHITE = (255, 255, 255)
COLOR_GRAY = (156, 163, 175)  # Gray 400
COLOR_ACCENT = (14, 165, 233)  # Sky 500
MARGIN_LEFT = 80
MARGIN_RIGHT = 80
MAX_TEXT_WIDTH = SLIDE_SIZE[0] - MARGIN_LEFT - MARGIN_RIGHT


def load_font(font_type='regular', size=32):
    """Load standard macOS system font or fallback to default PIL font"""
    paths = []
    if font_type in ('bold', 'title'):
        paths = [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/Library/Fonts/Arial Bold.ttf",
            "/System/Library/Fonts/Supplemental/Helvetica-Bold.ttf",
            "/System/Library/Fonts/SFNSDisplayCondensed-Bold.otf"
        ]
    else:
        paths = [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/Library/Fonts/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Helvetica.ttf",
            "/System/Library/Fonts/SFNSDisplayCondensed-Regular.otf"
        ]
        
    for path in paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


def create_gradient_background():
    """Create a premium linear gradient background image"""
    base = Image.new('RGB', SLIDE_SIZE, BG_START)
    draw = ImageDraw.Draw(base)
    for y in range(SLIDE_SIZE[1]):
        ratio = y / SLIDE_SIZE[1]
        r = int(BG_START[0] + (BG_END[0] - BG_START[0]) * ratio)
        g = int(BG_START[1] + (BG_END[1] - BG_START[1]) * ratio)
        b = int(BG_START[2] + (BG_END[2] - BG_START[2]) * ratio)
        draw.line([(0, y), (SLIDE_SIZE[0], y)], fill=(r, g, b))
    return base


def wrap_text(text, font, max_width, draw):
    """Wrap plain text to fit within max_width"""
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        test_line = ' '.join(current_line)
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]
        if width > max_width:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines


def draw_branding_and_page(draw, page_num, total_pages, branding="Pedro Cavalero"):
    """Draw branding and page counter on the footer of the slide"""
    font_footer = load_font('regular', 24)
    
    # Draw branding at bottom left
    draw.text((MARGIN_LEFT, SLIDE_SIZE[1] - 80), branding, fill=COLOR_GRAY, font=font_footer)
    
    # Draw page counter at bottom right
    counter_text = f"{page_num} / {total_pages}"
    bbox = draw.textbbox((0, 0), counter_text, font=font_footer)
    counter_w = bbox[2] - bbox[0]
    draw.text((SLIDE_SIZE[0] - MARGIN_RIGHT - counter_w, SLIDE_SIZE[1] - 80), counter_text, fill=COLOR_GRAY, font=font_footer)


def parse_slides(file_content):
    """Parse slide file separated by '---'"""
    # Split content by standard markdown thematic breaks
    raw_slides = file_content.strip().split('\n---')
    slides = []
    for raw in raw_slides:
        raw = raw.strip()
        if not raw:
            continue
        
        slide_type = "content"
        title = ""
        subtitle = ""
        body_items = []
        branding = "Pedro Cavalero"
        
        lines = raw.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Slide headers or indicators
            if line.startswith('# '):
                slide_header = line[2:].strip().lower()
                if "title" in slide_header or "welcome" in slide_header:
                    slide_type = "title"
                elif "cta" in slide_header or "call to action" in slide_header or "thanks" in slide_header:
                    slide_type = "cta"
            elif line.startswith('Title:'):
                title = line[6:].strip()
            elif line.startswith('Subtitle:'):
                subtitle = line[9:].strip()
            elif line.startswith('Branding:'):
                branding = line[9:].strip()
            elif line.startswith('-') or line.startswith('*') or line.startswith('•') or line.startswith('→') or line.startswith('✓'):
                # Extract bullet character and clean the item
                bullet_char = line[0]
                item_content = line[1:].strip()
                body_items.append((bullet_char, item_content))
            else:
                if not title and not line.startswith('#'):
                    title = line
                else:
                    body_items.append(('text', line))
                    
        slides.append({
            'type': slide_type,
            'title': title,
            'subtitle': subtitle,
            'items': body_items,
            'branding': branding
        })
    return slides


def generate_slide_image(slide, page_num, total_pages):
    """Generate Pillow slide image based on type and content"""
    img = create_gradient_background()
    draw = ImageDraw.Draw(img)
    
    # Draw premium top accent bar (sky blue)
    draw.rectangle([0, 0, SLIDE_SIZE[0], 12], fill=COLOR_ACCENT)
    
    if slide['type'] == "title":
        # Draw Title Slide
        font_title = load_font('bold', 56)
        font_sub = load_font('regular', 34)
        
        # Wrap title
        title_lines = wrap_text(slide['title'], font_title, MAX_TEXT_WIDTH, draw)
        
        # Calculate vertical position to center both title & subtitle
        line_height_t = 68
        total_h = len(title_lines) * line_height_t
        if slide['subtitle']:
            sub_lines = wrap_text(slide['subtitle'], font_sub, MAX_TEXT_WIDTH, draw)
            total_h += 40 + len(sub_lines) * 42
            
        start_y = (SLIDE_SIZE[1] - total_h) // 2
        
        # Draw title lines
        current_y = start_y
        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=font_title)
            line_w = bbox[2] - bbox[0]
            draw.text(((SLIDE_SIZE[0] - line_w) // 2, current_y), line, fill=COLOR_WHITE, font=font_title)
            current_y += line_height_t
            
        # Draw subtitle lines
        if slide['subtitle']:
            current_y += 40
            sub_lines = wrap_text(slide['subtitle'], font_sub, MAX_TEXT_WIDTH, draw)
            for line in sub_lines:
                bbox = draw.textbbox((0, 0), line, font=font_sub)
                line_w = bbox[2] - bbox[0]
                draw.text(((SLIDE_SIZE[0] - line_w) // 2, current_y), line, fill=COLOR_GRAY, font=font_sub)
                current_y += 42
                
    elif slide['type'] == "cta":
        # Draw Call To Action Slide
        font_cta = load_font('bold', 52)
        font_sub = load_font('regular', 34)
        
        title_lines = wrap_text(slide['title'] or "Thanks for reading!", font_cta, MAX_TEXT_WIDTH, draw)
        
        line_height_c = 64
        total_h = len(title_lines) * line_height_c
        if slide['subtitle']:
            sub_lines = wrap_text(slide['subtitle'], font_sub, MAX_TEXT_WIDTH, draw)
            total_h += 40 + len(sub_lines) * 42
            
        start_y = (SLIDE_SIZE[1] - total_h) // 2
        
        # Draw CTA title
        current_y = start_y
        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=font_cta)
            line_w = bbox[2] - bbox[0]
            draw.text(((SLIDE_SIZE[0] - line_w) // 2, current_y), line, fill=COLOR_WHITE, font=font_cta)
            current_y += line_height_c
            
        # Draw CTA subtitle
        if slide['subtitle']:
            current_y += 40
            sub_lines = wrap_text(slide['subtitle'], font_sub, MAX_TEXT_WIDTH, draw)
            for line in sub_lines:
                bbox = draw.textbbox((0, 0), line, font=font_sub)
                line_w = bbox[2] - bbox[0]
                draw.text(((SLIDE_SIZE[0] - line_w) // 2, current_y), line, fill=COLOR_ACCENT, font=font_sub)
                current_y += 42
                
    else:
        # Draw Content Slide
        font_header = load_font('bold', 44)
        font_body = load_font('regular', 32)
        font_bullet = load_font('bold', 34)
        
        # Draw slide title
        draw.text((MARGIN_LEFT, 120), slide['title'], fill=COLOR_ACCENT, font=font_header)
        
        # Draw thin visual accent line below header
        draw.rectangle([MARGIN_LEFT, 190, MARGIN_LEFT + 120, 194], fill=COLOR_ACCENT)
        
        # Draw body items (bullets or paragraph text)
        current_y = 250
        for item_type, content in slide['items']:
            if item_type == 'text':
                wrapped = wrap_text(content, font_body, MAX_TEXT_WIDTH, draw)
                for line in wrapped:
                    draw.text((MARGIN_LEFT, current_y), line, fill=COLOR_WHITE, font=font_body)
                    current_y += 42
                current_y += 20  # paragraph spacing
            else:
                # Custom Bullet layout
                # Determine display bullet character
                bullet_char = "→" if item_type in ('-', '*', '→') else item_type
                
                # Draw the bullet symbol in accent color
                draw.text((MARGIN_LEFT, current_y - 2), bullet_char, fill=COLOR_ACCENT, font=font_bullet)
                
                # Draw the wrapped bullet text indented
                wrapped = wrap_text(content, font_body, MAX_TEXT_WIDTH - 50, draw)
                for line in wrapped:
                    draw.text((MARGIN_LEFT + 50, current_y), line, fill=COLOR_WHITE, font=font_body)
                    current_y += 42
                current_y += 24  # bullet item spacing
                
    # Draw standard footer
    draw_branding_and_page(draw, page_num, total_pages, slide['branding'])
    
    return img


def main():
    parser = argparse.ArgumentParser(description='Generate LinkedIn PDF Carousel from text')
    parser.add_argument('--input', '-i', required=True, help='Path to slide input text/markdown file')
    parser.add_argument('--output', '-o', required=True, help='Path to output PDF file')
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file {args.input} does not exist.")
        sys.exit(1)
        
    with open(input_path, 'r', encoding='utf-8') as f:
        file_content = f.read()
        
    slides = parse_slides(file_content)
    if not slides:
        print("Error: No slides parsed from the input file.")
        sys.exit(1)
        
    print(f"Parsed {len(slides)} slides from {args.input}")
    
    images = []
    total_pages = len(slides)
    for idx, slide in enumerate(slides):
        page_num = idx + 1
        print(f"Generating slide {page_num}/{total_pages} (Type: {slide['type']}, Title: '{slide['title']}')")
        slide_img = generate_slide_image(slide, page_num, total_pages)
        images.append(slide_img)
        
    # Save slide images as multi-page PDF
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Compiling and saving PDF to {args.output}...")
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        resolution=100.0,
        quality=95
    )
    print("✓ PDF Carousel generated successfully!")


if __name__ == '__main__':
    main()
