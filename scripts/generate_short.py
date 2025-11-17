import subprocess
import sys
import textwrap

def run_command(command):
    """Runs a command and prints its output."""
    print(f"Executing: {command}")
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(process.stderr)
        raise subprocess.CalledProcessError(process.returncode, command)
    print(process.stdout)

def generate_short(video_id, input_video_path, srt_path, short_number, start_time, end_time, title):
    """Generates a single YouTube Short with title and subtitles."""

    shorts_dir = f"shorts-{video_id}"
    temp_title_file = f'{shorts_dir}/temp_title_{short_number}.txt'
    temp_srt_file = f'{shorts_dir}/short{short_number}_temp_sub.srt'
    temp_ass_file = f'{shorts_dir}/short{short_number}_temp_sub.ass'
    temp_cut_file = f'{shorts_dir}/short{short_number}_temp_cut.mp4'
    temp_padded_file = f'{shorts_dir}/short{short_number}_temp_padded.mp4'
    temp_subtitled_file = f'{shorts_dir}/short{short_number}_temp_subtitled.mp4'
    temp_spedup_file = f'{shorts_dir}/short{short_number}_temp_spedup.mp4'
    output_file = f'{shorts_dir}/short{short_number}.mp4'

    # Create title file
    with open(temp_title_file, "w") as f:
        f.write("\n".join(textwrap.wrap(title, width=25)))

    # Adjust SRT timestamps
    run_command(f'python3 scripts/adjust_srt.py "{srt_path}" {start_time} "{temp_srt_file}"')

    # Convert SRT to ASS
    run_command(f'ffmpeg -i "{temp_srt_file}" "{temp_ass_file}"')

    # Modify ASS file
    with open(temp_ass_file, "r+") as f:
        content = f.read()
        content = content.replace("PlayResX: 384", "PlayResX: 1080")
        content = content.replace("PlayResY: 288", "PlayResY: 1920")
        content = content.replace("Style: Default,Arial,16,&Hffffff,&Hffffff,&H0,&H0,0,0,0,0,100,100,0,0,1,1,0,2,10,10,10,1", "Style: Default,Arial,36,&H00FFFFFF,&H00000000,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,300,1")
        f.seek(0)
        f.write(content)
        f.truncate()

    # Run ffmpeg commands
    run_command(f'ffmpeg -y -ss {start_time} -to {end_time} -i "{input_video_path}" -c:v libx264 -c:a aac -b:a 128k "{temp_cut_file}"')
    run_command(f'ffmpeg -y -i "{temp_cut_file}" -filter_complex "[0:v]scale=1080:-2,pad=1080:1920:-1:(1920-ih)/2:color=black[v]" -map "[v]" -map 0:a "{temp_padded_file}"')
    run_command(f'ffmpeg -y -i "{temp_padded_file}" -vf "subtitles=filename=\'{temp_ass_file}\'" -c:a copy "{temp_subtitled_file}"')
    run_command(f'ffmpeg -y -i "{temp_subtitled_file}" -filter_complex "[0:v]setpts=PTS/2.0[v];[0:a]atempo=2.0[a]" -map "[v]" -map "[a]" "{temp_spedup_file}"')
    command = [
        "ffmpeg", "-y", "-i", temp_spedup_file,
        "-filter_complex", f"'drawtext=textfile={temp_title_file}:fontfile=/System/Library/Fonts/Supplemental/Arial Bold.ttf:fontsize=70:fontcolor=yellow:x=(w-text_w)/2:y=100'",
        "-c:a", "copy",
        output_file
    ]
    run_command(" ".join(command))

    # Clean up temporary files
    run_command(f'rm "{temp_srt_file}" "{temp_ass_file}" "{temp_title_file}" "{temp_cut_file}" "{temp_padded_file}" "{temp_subtitled_file}" "{temp_spedup_file}"')

if __name__ == "__main__":
    if len(sys.argv) != 8:
        print("Usage: python generate_short.py <video_id> <input_video_path> <srt_path> <short_number> <start_time> <end_time> <title>")
        sys.exit(1)

    video_id = sys.argv[1]
    input_video_path = sys.argv[2]
    srt_path = sys.argv[3]
    short_number = sys.argv[4]
    start_time = sys.argv[5]
    end_time = sys.argv[6]
    title = sys.argv[7]

    generate_short(video_id, input_video_path, srt_path, short_number, start_time, end_time, title)
