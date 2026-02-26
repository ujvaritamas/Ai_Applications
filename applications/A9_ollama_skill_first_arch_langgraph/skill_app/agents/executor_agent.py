from langchain.messages import SystemMessage
from langchain_ollama import ChatOllama

from states.state import MessagesState
from langchain.messages import ToolMessage

from typing import Literal, LiteralString
from langgraph.graph import StateGraph, START, END
import  tools.kubernetes_tools
import tools.customer_notification_tools

import agents.skill_agent

model = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
    format="",  # Don't force JSON format, let tool calling work naturally
    # other params...
)

tools = tools.kubernetes_tools.tools + tools.customer_notification_tools.tools
tools_by_name = {tool.name: tool for tool in tools}

# Bind tools with strict mode if available
model_with_tools = model.bind_tools(tools)

def llm_call(state: dict):
    """LLM decides whether to call a tool or not"""

    print("executor llm_call() called")

    # Check if this is the first call and we have skill instructions
    messages_to_send = [
        SystemMessage(
            content=f"""
            You are a helpful assistant with access to tools.

            CRITICAL: When you see instructions telling you to call specific tools, you MUST call them immediately.
            DO NOT write explanations like "I will call the following tools" or describe what you're going to do.
            JUST MAKE THE TOOL CALLS DIRECTLY.

            If the instructions say:
            - "Use the tool X" → Call tool X immediately
            - "Call tool Y with parameters Z" → Call tool Y with parameters Z immediately

            Your job is to ACT, not to describe actions.
            """
        )
    ] + state["messages"]

    return {
        "messages": [
            model_with_tools.invoke(messages_to_send)
        ],
        "llm_calls": state.get('llm_calls', 0) + 1
    }





def tool_node(state: dict):
    """Performs the tool call"""

    print("executor tool_node() called")

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])

        # Convert observation to string if it's not already
        if isinstance(observation, str):
            content = observation
        else:
            import json
            content = json.dumps(observation, indent=2)

        result.append(ToolMessage(content=content, tool_call_id=tool_call["id"]))
    return {"messages": result}


def should_continue(state: MessagesState) -> LiteralString:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we stop (reply to the user)
    return END

def build_and_compile_agent():

    from states.state import MessagesState
    # Build workflow
    agent_builder = StateGraph(MessagesState)

    # Add nodes
    agent_builder.add_node("llm_call", llm_call)
    agent_builder.add_node("tool_node", tool_node)

    # Add edges to connect nodes
    agent_builder.add_edge(START, "llm_call")
    agent_builder.add_conditional_edges(
        "llm_call",
        should_continue,
        ["tool_node", END]
    )
    agent_builder.add_edge("tool_node", "llm_call")

    # Compile the agent
    agent = agent_builder.compile()


    return agent

    # Show the agent
    #from IPython.display import Image, display
    #display(Image(agent.get_graph(xray=True).draw_mermaid_png()))

    # Invoke
    #from langchain.messages import HumanMessage
    #messages = [HumanMessage(content="Add 3 and 4.")]
    #messages = agent.invoke({"messages": messages})
    #for m in messages["messages"]:
    #    m.pretty_print()


def invoke_agent(agent, user_query):

    from langchain.messages import HumanMessage

    skills = agents.skill_agent.get_corresponding_skills_and_descriptions(user_query)

    skills_message = SystemMessage(
        content=f"""
        You are an AI assistant that EXECUTES tasks using tools.

        INSTRUCTIONS:
        {skills}

        CRITICAL RULES:
        1. Read the instructions above
        2. Make the required tool calls IMMEDIATELY
        3. Do NOT write "I will call" or "Here are the tool calls"
        4. Do NOT explain what you're going to do
        5. Just execute the tool calls directly with proper parameters

        When instructions say "Call X with Y", you must invoke that tool immediately.
        """
    )

    messages = [skills_message, HumanMessage(content=user_query)]

    print("executor agent called", messages)

    messages = agent.invoke({"messages": messages})
    for m in messages["messages"]:
        m.pretty_print()