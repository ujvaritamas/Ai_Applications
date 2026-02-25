from langchain.tools import tool
from typing import TypedDict

class Skill(TypedDict):  
    """A skill that can be progressively disclosed to the agent."""
    name: str  # Unique identifier for the skill
    description: str  # 1-2 sentence description to show in system prompt
    content: str  # Full skill content with detailed instructions

# SKILLS will be populated by the __init__.py module
SKILLS = []

@tool
def load_skill(skill_name: str) -> str:
    """Load the full content of a skill into the agent's context.

    Use this when you need detailed information about how to handle a specific
    type of request. This will provide you with comprehensive instructions,
    policies, and guidelines for the skill area.

    Args:
        skill_name: The name of the skill to load (e.g., "dummy_skill", "expense_reporting")
    """
    # Import here to avoid circular imports
    from . import SKILLS
    
    # Find and return the requested skill
    for skill in SKILLS:
        if skill["name"] == skill_name:
            return f"Loaded skill: {skill_name}\n\n{skill['content']}"

    # Skill not found
    available = ", ".join(s["name"] for s in SKILLS)
    return f"Skill '{skill_name}' not found. Available skills: {available}"


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
    from . import SKILLS
    
    # Find and return the requested skill
    for skill in SKILLS:
        ret += f"{CYAN}{BOLD}• {skill['name']}{RESET}\n"
        ret += f"  {GREEN}{skill['description']}{RESET}\n\n"

    return ret