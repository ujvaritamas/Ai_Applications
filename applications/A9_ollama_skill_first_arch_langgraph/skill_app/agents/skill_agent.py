from langchain.tools import tool
from langchain_ollama import ChatOllama
from langchain.messages import SystemMessage

from typing import List
import langgraph.graph


from pydantic import BaseModel, Field

# Define Pydantic models for structured output
class Skill(BaseModel):
    """A single skill with name and description"""
    name: str = Field(description="The name of the skill")
    description: str = Field(description="Description of what the skill does")

class SkillSelection(BaseModel):
    """Collection of selected skills - should contain ONLY ONE skill"""
    skills: List[Skill] = Field(
        description="List containing the single most relevant skill",
        max_length=1,
        min_length=1
    )

model = ChatOllama(
    model="llama3.1:8b",
    temperature=0,
    # other params...
)

def load_skill(skill_name: str) -> str:
    """Load the full content of a skill into the agent's context.

    Use this when you need detailed information about how to handle a specific
    type of request. This will provide you with comprehensive instructions,
    policies, and guidelines for the skill area.

    Args:
        skill_name: The name of the skill to load (e.g., "dummy_skill", "expense_reporting")
    """
    # Import here to avoid circular imports
    from skill_registry import SKILLS
    
    # Find and return the requested skill
    for skill in SKILLS:
        if skill["name"] == skill_name:
            return f"Loaded skill: {skill_name}\n\n{skill['content']}"

    # Skill not found
    available = ", ".join(s["name"] for s in SKILLS)
    return f"Skill '{skill_name}' not found. Available skills: {available}"



#list_skill should not be a tool
def list_skill() -> str:
    """List the available skills.

    Use this when you need available skills. This will return with the skill names
    and basic descriptions

    Args:
        skill_name: The name of the skill to load (e.g., "dummy_skill", "expense_reporting")
    """
    # ANSI color codes for better visibility
    BOLD = '\033[1m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    RESET = '\033[0m'
    
    ret = f"\n{BOLD}Available skills:{RESET}\n"
    ret += "=" * 60 + "\n"
    
    # Import here to avoid circular imports
    from skill_registry import SKILLS
    
    # Find and return the requested skill
    for skill in SKILLS:
        ret += f"{CYAN}{BOLD}• {skill['name']}{RESET}\n"
        ret += f"  {GREEN}{skill['description']}{RESET}\n\n"

    return ret

structured_model = model.with_structured_output(SkillSelection)


def llm_call(state: dict):
    """LLM decides whether skill need to be used (if there is tools defined also decide which tools need to be called)"""

    available_skills = list_skill()

    print("skill_agent llm_call() function called")

    res = structured_model.invoke(
                [
                    SystemMessage(
                        content=f"""
                        You are a helpful AI assistant tasked with selecting the MOST relevant skill.
                        Available skills:
                        {available_skills}

                        Only these skills are available.

                        IMPORTANT: You MUST select ONLY ONE skill - the single most relevant skill for the user's query.

                        Guidelines:
                        - Analyze the user's query carefully
                        - Match keywords in the query to skill names and descriptions
                        - Select ONLY the skill that best matches the user's intent
                        - If the query mentions "customer notification", select customer_notification_skill
                        - If the query mentions "kubectl" or general kubernetes commands, select kubectl_skill
                        - If the query asks for diagnostics or pod troubleshooting, select k8s_diagnostic_skill

                        Return ONLY ONE skill in the specified format.
                        """
                    )
                ]
                + state["messages"]
            )
    
    print(res)

    return {
        "messages": [
            res
        ],
        "llm_calls": state.get('llm_calls', 0) + 1
    }



def get_corresponding_skills_and_descriptions(user_query) -> str:
    """This function load the skills

    Returns:
        str: loaded skills (detailed)
    """

    from states.state import MessagesState

    agent_builder = langgraph.graph.StateGraph(MessagesState)
    # Add nodes
    agent_builder.add_node("llm_call", llm_call)
    #agent_builder.add_node("tool_node", tool_node)

    # Add edges to connect nodes
    agent_builder.add_edge(langgraph.graph.START, "llm_call")

    agent_builder.add_edge("llm_call", langgraph.graph.END)

    # Compile the agent
    agent = agent_builder.compile()

    # Invoke
    from langchain.messages import HumanMessage
    messages = [HumanMessage(content=f"List the most relevant skills what are connected to this user query: {user_query}")]
    res = agent.invoke({"messages": messages})

    print(res)

    # Extract the SkillSelection object from the messages
    # The last message should be the SkillSelection object
    last_message = res["messages"][-1]

    if isinstance(last_message, SkillSelection):
        ret = "Skills:"
        for skill in last_message.skills:
            #print(skill)
            skill_details = load_skill(skill.name)
            ret += f"{skill_details} \n\n"
        return ret
    else:
        return "No skills selected"

