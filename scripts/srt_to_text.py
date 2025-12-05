import sys
import re

def srt_to_text(srt_path, output_path):
    try:
        with open(srt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        output = []
        for line in lines:
            line = line.strip()
            # Skip numeric counters
            if re.match(r'^\d+$', line):
                continue
            # Skip timestamps
            if re.match(r'^\d{2}:\d{2}:\d{2}', line):
                continue
            # Skip empty lines
            if not line:
                continue
            output.append(line)
            
        # Join with spaces for a continuous text block
        text = ' '.join(output)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
            
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python srt_to_text.py <input_srt_path> <output_txt_path>")
        sys.exit(1)
        
    srt_path = sys.argv[1]
    output_path = sys.argv[2]
    srt_to_text(srt_path, output_path)
