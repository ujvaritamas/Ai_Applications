# Ollama with antropic skills

```
ollama pull llama3.1:8b
```

This app is created to handle skills feature with ollama.

This should dynamically load skills, and the agent can decide that skill should be used or not.


- Prompt-driven specialization: Skills are primarily defined by specialized prompts
- Progressive disclosure: Skills become available based on context or user needs
- Lightweight composition: Skills are simpler than full sub-agents
- Reference awareness: Skills can reference scripts, templates, and other resources


custom middleware that injects skill descriptions into the system prompt

```
uv init skill_app
uv add langchain
uv add langchain-ollama
```

```
cd skill_app
uv run main.py
```