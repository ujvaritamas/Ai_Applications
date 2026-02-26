from langchain_ollama import ChatOllama
from langchain_core.tools import tool
import subprocess
import inquirer

@tool
def shell_command(command: str) -> str:
    """Execute a shell command and return the output.

    Args:
        command: The shell command to execute

    Returns:
        The output of the command
    """
    try:
        questions = [
            inquirer.List('action',
                         message=f"Do you want to execute this command: {command}",
                         choices=['Yes', 'No', 'View command details'],
                         ),
        ]
        answers = inquirer.prompt(questions)
        
        if answers['action'] == 'No':
            return "Command execution cancelled by user."
        elif answers['action'] == 'View command details':
            print(f"\nCommand: {command}")
            print("This command will be executed in a shell with 30 second timeout.")
            # Ask again after showing details
            confirm = inquirer.List('confirm',
                                   message="Proceed with execution?",
                                   choices=['Yes', 'No'])
            if inquirer.prompt([confirm])['confirm'] == 'No':
                return "Command execution cancelled by user."

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Error executing command: {str(e)}"

shell_tool = shell_command



model = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
    # other params...
)

tools = [shell_tool]
tools_by_name = {tool.name: tool for tool in tools}

# Bind tools with strict mode if available
model_with_tools = model.bind_tools(tools)


messages = [
    (
        "system",
        "You are a helpful assistant with access to shell commands. Help the user with their tasks.",
    ),
    ("human", "List pods on the default namespace"),
]

# Invoke the model with tools
ai_msg = model_with_tools.invoke(messages)

print("AI Response:", ai_msg.content)
print("\nTool Calls:", ai_msg.tool_calls if hasattr(ai_msg, 'tool_calls') else "None")

# If there are tool calls, execute them and get final response
if hasattr(ai_msg, 'tool_calls') and ai_msg.tool_calls:
    # Add the AI message to the conversation
    messages.append(ai_msg)

    for tool_call in ai_msg.tool_calls:
        tool_name = tool_call.get('name')
        tool_args = tool_call.get('args', {})

        if tool_name in tools_by_name:
            print(f"\nExecuting tool: {tool_name}")
            print(f"Arguments: {tool_args}")
            result = tools_by_name[tool_name].invoke(tool_args)
            print(f"Result: {result}")

            # Add tool result to messages
            messages.append({
                "role": "tool",
                "content": result,
                "tool_call_id": tool_call.get('id'),
                "name": tool_name
            })

    # Get final response from model with tool results
    print("\n" + "="*50)
    print("Getting final response from model...")
    print("="*50)
    final_response = model_with_tools.invoke(messages)
    print("\nFinal AI Response:", final_response.content)