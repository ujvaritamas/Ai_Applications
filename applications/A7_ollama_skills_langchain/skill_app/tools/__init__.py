"""Tools module - loads skills and provides skill-related tools."""

import os
import re
from pathlib import Path
from .skill_tool import load_skill, Skill

# Load skills from the skills directory
def load_skills_from_directory():
    """Load all skills from markdown files in the skills directory.
    
    Skills should be in Anthropic format with YAML frontmatter:
    ---
    name: skill-name
    description: Brief description
    ---
    [skill content]
    """
    skills = []
    skills_dir = Path(__file__).parent.parent / "skills"
    
    if not skills_dir.exists():
        return skills
    
    # Iterate through each skill folder
    for skill_folder in skills_dir.iterdir():
        if not skill_folder.is_dir():
            continue
        
        # Look for a markdown file with the same name as the folder
        skill_file = skill_folder / f"{skill_folder.name}.md"
        
        if skill_file.exists():
            # Read the skill content
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML frontmatter (Anthropic format)
            frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
            
            if frontmatter_match:
                frontmatter = frontmatter_match.group(1)
                skill_content = frontmatter_match.group(2)
                
                # Parse name and description from frontmatter
                name_match = re.search(r'name:\s*(.+)', frontmatter)
                desc_match = re.search(r'description:\s*(.+)', frontmatter)
                
                skill_name = name_match.group(1).strip() if name_match else skill_folder.name
                description = desc_match.group(1).strip() if desc_match else "A skill to help with specific tasks"
            else:
                # Fallback: use folder name and first line as description
                skill_name = skill_folder.name
                description = "A skill to help with specific tasks"
                skill_content = content
            
            # Create the skill dictionary
            skill: Skill = {
                "name": skill_name,
                "description": description,
                "content": skill_content
            }
            skills.append(skill)
    
    return skills

# Load all skills
SKILLS = load_skills_from_directory()

# Export the load_skill tool and SKILLS
__all__ = ['load_skill', 'SKILLS', 'Skill']
