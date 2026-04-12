from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.messages import AIMessage, HumanMessage, ToolMessage, SystemMessage

from langchain.agents import create_agent




@tool
def appendData(inp: str, data_to_append: str) -> str:
    """This function concat 2 string by appending the second arg to the first arg

    Args:
        inp (str): original string
        data_to_append (str): data what we want to append to the original string

    Returns:
        str: extended str
    """

    return inp + data_to_append


model = ChatOllama(
    model="gemma4:e4b",
    temperature=0.0,
)

messages = []
human = HumanMessage(
    content="Plase append the hello string with bello"
)
system = SystemMessage(
    content="""
    you are a tool calling llm, your job is to perform the human message.
    Call the available tools to perform the job, when you finished -> summarize the called tool resoults
    Summarization process:
    please mention the tool name and what was the output.
    """
)


messages = [human, system]

tools = [appendData]
model_with_tools = model.bind_tools(tools)

def my_react_loop(model_with_tools, messages):
    # Create a tool map for easy lookup
    tool_map = {tool.name: tool for tool in tools}

    # Loop until the model stops calling tools
    while True:
        # Get AI response
        res = model_with_tools.invoke(messages)
        messages.append(res)
        
        # Check if AI wants to call tools
        if isinstance(res, AIMessage) and res.tool_calls:
            print(f"AI wants to call {len(res.tool_calls)} tool(s)")
            
            # Execute each tool call
            for tool_call in res.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_id = tool_call["id"]
                
                print(f"Calling tool: {tool_name} with args: {tool_args}")
                
                # Get the actual tool function
                selected_tool = tool_map[tool_name]
                
                # Execute the tool
                tool_output = selected_tool.invoke(tool_args)
                
                print(f"Tool output: {tool_output}")
                
                # Send the result back to the model
                tool_message = ToolMessage(
                    content=str(tool_output),
                    tool_call_id=tool_id
                )
                messages.append(tool_message)
        else:
            # No more tool calls, we're done
            print("\n=== No more tool calls - AI has final response ===\n")
            break

    return res

res = my_react_loop(model_with_tools, messages)

print(messages)
print("\n=== Final Response ===")
print(res.content)

messages1 = [human, system]

agent = create_agent(
    model=model,
    tools=tools
)

res = agent.invoke({"messages": messages1})
print("LLLLLLLL")
print(res['messages'][-1].content)