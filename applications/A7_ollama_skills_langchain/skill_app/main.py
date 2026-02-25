from langchain_ollama import ChatOllama
from langchain.agents import create_agent
import middleware

llm = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
    # other params...
)

# Create the agent with skill support
agent = create_agent(
    llm,
    system_prompt=(
        "You are a skill AI assistant that helps users "
        "perform tasks what are defined as skills."
    ),
    middleware=[middleware.SkillMiddleware()],  
    #checkpointer=InMemorySaver(),
)


result = agent.invoke(  
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "List all avaialbe skills"
                ),
            }
        ]
    }
)


# Print the conversation
for message in result["messages"]:
    if hasattr(message, 'pretty_print'):
        message.pretty_print()
    else:
        print(f"{message.type}: {message.content}")

result = agent.invoke(  
    {
        "messages": [
            {
                "role": "user",
                "content": (
                    "List all avaialbe skills and print the skill content"
                ),
            }
        ]
    }
)

# Print the conversation
for message in result["messages"]:
    if hasattr(message, 'pretty_print'):
        message.pretty_print()
    else:
        print(f"{message.type}: {message.content}")