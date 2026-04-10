from pydantic import BaseModel, Field
from langchain_ollama import ChatOllama
from typing import  List
from langchain.agents import create_agent

class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")

class Contacts(BaseModel):
    contacts: List[ContactInfo] = Field(default_factory=list, description="Contacts")

llm = ChatOllama(
    model="gemma4:e4b", #"gemma4:e4b",
    temperature=0,
    # other params...
)

agent = create_agent(
    model=llm,
    response_format=Contacts  # Auto-selects ProviderStrategy
)

test = """
1. Alice Smith, email: alice.smith@example.com, resides in Germany, age: 28
2. Bob Johnson resides in France, 35 years old, email: bob.johnson@example.com
3. Carol White, age: 40-2, email: carol.white@example.com, Europe
4. David Brown is 31 years old, resides in Italy
5. Emma Davis, email: emma.davis@example.com, age: 20+7, resides in Netherlands
6. Frank Miller, resides in Belgium, email: frank.miller@example.com
7. Grace Wilson, 33 years old, Europe, email: grace.wilson@example.com
8. Henry Moore, age: 29, email: henry.moore@example.com
9. Irene Taylor resides in Denmark, email: irene.taylor@example.com, age: 38
10. Jack Anderson, 41 years old, America
11. Karen Thomas, email: karen.thomas@example.com, resides in Switzerland
12. Liam Jackson, age: 30+6, Ireland
13. Mia Martin resides in Portugal, 30 years old, email: mia.martin@example.com
14. Noah Lee, email: noah.lee@example.com, Europe
15. Olivia Perez, 25 years old, resides in Czech Republic
16. Paul Thompson, email: paul.thompson@example.com, age: 39
17. Quinn Garcia, resides in Hungary, 16+16 years old, email: quinn.garcia@example.com
18. Ryan Martinez, age: 37, America, email: ryan.martinez@example.com
19. Sophia Robinson, resides in Slovenia
20. Thomas Clark, email: thomas.clark@example.com, 43 years old, Europe
21. Uma Rodriguez, age: 31, resides in Bulgaria
"""


def main():
    result = agent.invoke({
    "messages": [{"role": "user", "content": f"Extract contact info from: {test}"}]
})

    print(result["messages"])
    print("LLLLLLLLLL")

    print(result["structured_response"])


if __name__ == "__main__":
    main()
