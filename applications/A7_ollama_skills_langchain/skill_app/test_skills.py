#!/usr/bin/env python3
"""Simple test script to verify the Anthropic-format skill loading works."""

from tools import SKILLS, load_skill

def main():
    print("=== Skill Loading Test (Anthropic Format) ===\n")
    
    # Display loaded skills
    print(f"Number of skills loaded: {len(SKILLS)}\n")
    
    if SKILLS:
        print("Available skills:")
        for skill in SKILLS:
            print(f"  - {skill['name']}")
            print(f"    Description: {skill['description']}\n")
        
        # Test loading a skill
        print("\n=== Testing load_skill tool ===\n")
        skill_name = SKILLS[0]['name']
        result = load_skill.invoke({"skill_name": skill_name})
        print(f"Loaded skill '{skill_name}':")
        print("-" * 50)
        print(result[:500] + "..." if len(result) > 500 else result)
        print("-" * 50)
    else:
        print("No skills found. Please create skill markdown files in the skills directory.")

if __name__ == "__main__":
    main()
