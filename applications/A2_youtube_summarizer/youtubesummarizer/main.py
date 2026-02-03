
from langchain_ollama import ChatOllama

from youtube import youtube

used_model = "gemma3:4b" #"gemma3:1b"

llm = ChatOllama(
    model=used_model,
    temperature=0,
    # other params...
)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "I love programming."),
]

def summarize_youtube_video(url: str):
    transcript = youtube.get_transcript(url)

    #print(transcript)

    messages = [
        (
            "system",
            "You are an expert summarization assistant. Your task is to analyze the provided transcript of a YouTube video and generate a clear, concise, and engaging summary. Focus on the main topic, key points, and any important details that capture the essence of the video. Avoid unnecessary details and ensure the summary is easy to understand.",
        ),
        ("human", f"The following is a transcript of a YouTube video. Please summarize it and explain what the video is about: {transcript}"),
    ]
    ai_msg = llm.invoke(messages)

    print(ai_msg.content)

#summarize_youtube_video("https://www.youtube.com/watch?v=eur8dUO9mvE")
summarize_youtube_video("https://www.youtube.com/watch?v=jb4AAFCRPrI")