# Dummy Skill

This is a demonstration skill that helps with basic mathematical calculations and unit conversions.

## Features
- Basic arithmetic operations
- Common unit conversions (length, weight, temperature)
- Percentage calculations

## Skill Format (Anthropic Style)

Skills use YAML frontmatter following the Anthropic format:

```markdown
---
name: skill-name
description: Brief description of when to use this skill
---

[Skill instructions and content]
```

## How It Works
The skill provides detailed instructions to the agent on:
- When to use this skill (via the description in frontmatter)
- How to perform calculations
- Response formatting guidelines
- Common conversion factors

## Usage Example
When a user asks "What is 15% of 240?", the agent can load this skill to get detailed instructions on how to calculate and format the response properly.

## Adding New Skills
To add a new skill:
1. Create a new folder in the `skills/` directory
2. Create a markdown file with the same name as the folder (e.g., `my_skill/my_skill.md`)
3. Use the Anthropic format with YAML frontmatter:
   ```markdown
   ---
   name: my-skill
   description: Brief description of when to use this skill. Include specific triggers or use cases.
   ---

   [Your skill instructions here]
   ```

The skill will be automatically loaded by the tools module and made available to the agent.
