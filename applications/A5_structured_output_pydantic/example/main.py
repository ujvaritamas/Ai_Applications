import person.person as person
import json
from typing import Any

from langchain_ollama import ChatOllama
from langchain.agents import create_agent

json_schema: dict[str, Any] = person.Person.model_json_schema()
print(json.dumps(json_schema, indent=2))


model = "llama3.1:8b"   #model need to support tool calling
temperature = 0

llm = ChatOllama(
    model=model,
    temperature=temperature,
)

agent = create_agent(
    model=llm,
    response_format=person.Person
)

result = agent.invoke({
    "messages": [{"role": "user", 
                  "content": "Extract person info: John Doe is 30 years old, email: john@example.com, resides in Austria."
                  }]
})

print(result)
print(type(result["structured_response"]))

for i in result["structured_response"]:
    print(i)


#llm.invoke()


# Make structured output request
#response = llm.chat.complete(
#    model="mistral-large-latest",
#    messages=[{
#        "role": "user",
#        "content": "Extract person info: John Doe is 30 years old, email: john@example.com, resides in Austria."
#    }],
#    response_format={
#        "type": "json_object",
#        "schema": person.Person.model_json_schema()
#    }
#)