# Skills Directory

This directory contains skills in Anthropic format that can be dynamically loaded by the agent.

## Format

Each skill should be in its own folder with a markdown file that has the same name as the folder:

```
skills/
  my_skill/
    my_skill.md
  another_skill/
    another_skill.md
```

## Anthropic Skill Format

Skills use YAML frontmatter with this structure:

```markdown
---
name: skill-name
description: Brief description of when to use this skill. Include specific triggers or use cases.
---

[Skill content and instructions]
```

### Frontmatter Fields

- **name**: The skill identifier (kebab-case recommended)
- **description**: A 1-2 sentence description that appears in the system prompt. This tells the agent when to use the skill.

### Content Guidelines

The content after the frontmatter should include:

1. **Opening statement**: Brief intro about what the skill handles
2. **Instructions**: Detailed, structured guidance
3. **Examples**: Show how to apply the skill
4. **Format guidelines**: How to structure responses

## Example

See [dummy_skill/dummy_skill.md](dummy_skill/dummy_skill.md) for a complete working example.

Use [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md) as a starting point for new skills.

## How Skills Work

1. Skills are automatically discovered and loaded from this directory
2. The `description` field is injected into the system prompt
3. The agent can use the `load_skill` tool to fetch full skill content when needed
4. This enables progressive disclosure - keeping the context manageable while making detailed instructions available on demand
