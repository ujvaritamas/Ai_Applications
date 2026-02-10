# Knowledge graph example

Building knowledge graph from text:
- prompt based approach:
```
You are a top-tier algorithm designed to extract information in structured formats for building a knowledge graph. Your task is to identify the entities and relations requests with the user prompt from a given text. You must generate the output in a json format containing a list with json objects. Each object should have the keys: "head", "head_type", "relation", "tail" and "tail_type". Here is one example:
---
Give the text: "Aadam is a software engineer in Microsoft since 2009"
You can extract a relationship in the following format:
{
    "head": "Adam",
    "head_type": "Person",
    "relation": "WORKS_FOR",
    "tail": "Microsoft",
    "tail_type: "Company"
}
```
promp based approach is not the ideal solution

- some llm support structured output (this is better approach) (using tools -> structured output)

- Langchain [LLMGraphTransformer](https://pypi.org/project/LLMGraphTransformer/)


```
ollama list                                                                           01:31:42 PM
NAME         ID              SIZE      MODIFIED   
gemma3:4b    a2af6cc3eb7f    3.3 GB    7 days ago    
gemma3:1b    8648f39daa8f    815 MB    7 days ago    
```

```
uv init example
cd example

uv add langchain
uv add langchain-experimental
uv add langchain_ollama #we will use ollama llms

uv add LLMGraphTransformer

#uv add python-dotenv
uv add pyvis #network graph visualization
```