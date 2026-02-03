
from langchain_ollama import ChatOllama

from youtube import youtube

used_model = "gemma3:1b"

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

    print(transcript)

    messages = [
        (
            "system",
            "You are an advanced summarization assistant. Your task is to provide a concise and accurate summary of the given transcript. Focus on the key points and main ideas while maintaining clarity and coherence.",
        ),
        ("human", f"Please summarize this transcript in 10 sentence: {transcript}"),
    ]
    ai_msg = llm.invoke(messages)

    print(ai_msg.content)

summarize_youtube_video("https://www.youtube.com/watch?v=eur8dUO9mvE")