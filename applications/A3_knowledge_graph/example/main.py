
from LLMGraphTransformer import LLMGraphTransformer
from LLMGraphTransformer.schema import NodeSchema, RelationshipSchema
from langchain_core.documents import Document
from langchain_ollama import ChatOllama

node_schemas = [
    NodeSchema("Person", ["name", "birth_year", "death_year", "nationalitie", "profession"], "Represents an individual"),
    NodeSchema("Organization", ["name", "founding_year", "industrie"], "Represents a group, company, or institution"),
    NodeSchema("Location", ["name"], "Represents a geographical area such as a city, country, or region"),
    NodeSchema("Award", ["name", "field"], "Represents an honor, prize, or recognition")
]

relationship_schemas = [
    RelationshipSchema("Person", "SPOUSE_OF", "Person"),
    RelationshipSchema("Person", "MEMBER_OF", "Organization", ["start_year", "end_year", "year"]),
    RelationshipSchema("Person", "AWARDED", "Award", ["year"]),
    RelationshipSchema("Person", "LOCATED_IN", "Location"),
    RelationshipSchema("Organization", "LOCATED_IN", "Location")
]

additional_instructions="""- all names must be extracted as uppercase"""

text="""Marie Curie, born in 1867, was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity.
She was the first woman to win a Nobel Prize, the first person to win a Nobel Prize twice, and the only person to win a Nobel Prize in two scientific fields.
Her husband, Pierre Curie, was a co-winner of her first Nobel Prize, making them the first-ever married couple to win the Nobel Prize and launching the Curie family legacy of five Nobel Prizes.
She was, in 1906, the first woman to become a professor at the University of Paris."""

llm = ChatOllama(
    model="gemma3:4b",
    temperature=0,
    # other params...
)

llm_transformer = LLMGraphTransformer(
    llm=llm,
    allowed_nodes=node_schemas,
    allowed_relationships=relationship_schemas,
    additional_instructions=additional_instructions
)

document = Document(page_content=text)
graph_document = llm_transformer.convert_to_graph_document(document)

print(f"Nodes: {graph_document.nodes}")
print(f"Relationships: {graph_document.relationships}")