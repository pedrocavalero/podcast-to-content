import sys
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id):
    """
    Retrieves the transcript for a given YouTube video ID.

    Args:
        video_id: The ID of the YouTube video.

    Returns:
        A string containing the transcript of the video.
    """
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ""
        for item in transcript_list:
            transcript += item['text'] + " "
        return transcript
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python transcribe.py <video_id>")
    else:
        video_id = sys.argv[1]
        transcript = get_transcript(video_id)
        print(transcript)