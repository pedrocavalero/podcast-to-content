import sys
import re
from datetime import timedelta

def parse_time(time_str):
    time_str = time_str.replace(',', '.')
    try:
        if '.' in time_str:
            parts = time_str.split('.')
            h, m, s = parts[0].split(':')
            ms = parts[1]
        else:
            h, m, s = time_str.split(':')
            ms = '0'
        return timedelta(hours=int(h), minutes=int(m), seconds=int(s), milliseconds=int(ms))
    except Exception as e:
        return None

def format_time(td):
    if td.total_seconds() < 0:
        td = timedelta(0)
    total_seconds = int(td.total_seconds())
    milliseconds = int(td.microseconds / 1000)
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02}:{m:02}:{s:02},{milliseconds:03}"

def adjust_srt_timestamps(input_srt_path, start_offset_str, output_srt_path):
    start_offset = parse_time(start_offset_str)
    if start_offset is None:
        return

    with open(input_srt_path, 'r', encoding='utf-8') as infile, \
         open(output_srt_path, 'w', encoding='utf-8') as outfile:
        for line in infile:
            time_match = re.match(r'(\d{2}:\d{2}:\d{2}[,.]\d{3}) --> (\d{2}:\d{2}:\d{2}[,.]\d{3})', line)
            if time_match:
                start_time_str, end_time_str = time_match.groups()
                
                start_time = parse_time(start_time_str)
                end_time = parse_time(end_time_str)

                if start_time is None or end_time is None:
                    outfile.write(line)
                    continue

                adjusted_start_time = start_time - start_offset
                adjusted_end_time = end_time - start_offset

                outfile.write(f"{format_time(adjusted_start_time)} --> {format_time(adjusted_end_time)}\n")
            else:
                outfile.write(line)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python adjust_srt.py <input_srt_path> <start_offset_hh:mm:ss> <output_srt_path>")
        sys.exit(1)

    input_srt_path = sys.argv[1]
    start_offset_str = sys.argv[2]
    output_srt_path = sys.argv[3]

    adjust_srt_timestamps(input_srt_path, start_offset_str, output_srt_path)
