from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.1:8b", #"gemma4:e4b",
    temperature=0,
    # other params...
)


def main():
    messages = [
        (
            "system",
            "You are a helpful assistant that translates English to French. Translate the user sentence.",
        ),
        ("human", "I love programmingdsfsd."),
    ]
    ai_msg = llm.invoke(messages)

    print(ai_msg.content)


if __name__ == "__main__":
    main()
