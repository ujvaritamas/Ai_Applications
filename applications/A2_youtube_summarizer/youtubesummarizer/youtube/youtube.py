import re
from youtube_transcript_api import YouTubeTranscriptApi




def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from various URL formats."""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/)([^&\n?#]+)',
        r'youtube\.com/embed/([^&\n?#]+)',
        r'youtube\.com/v/([^&\n?#]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return url


def get_transcript(url: str) -> str:
    video_id = extract_video_id(url) or url

    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(video_id)
    ret = ""
    for snippet in fetched_transcript.snippets:
        ret += snippet.text

    return ret


get_transcript("https://www.youtube.com/watch?v=eur8dUO9mvE")