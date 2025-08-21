import sys
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id, preserve_formatting=False):
    """
    Retrieves the transcript for a given YouTube video ID.

    Args:
        video_id: The ID of the YouTube video.

    Returns:
        A string containing the transcript of the video in the format Start-duration: text.
    """
    try:
        transcript_list = YouTubeTranscriptApi().fetch(video_id, preserve_formatting=preserve_formatting)
        transcript = ""
        for item in transcript_list:
            if preserve_formatting:
                transcript += f"{item.start}-{item.duration}: {item.text}\n"
            else:
                # If formatting is not preserved, just concatenate the text
                transcript += item.text + " "
        return transcript
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("Usage: python transcribe.py <video_id> -s")
    else:
        video_id = sys.argv[1]
        preserve_formatting = '-s' in sys.argv
        transcript = get_transcript(video_id, preserve_formatting=preserve_formatting)
        print(transcript)