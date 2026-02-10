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

### visualization
from pyvis.network import Network

# Create a network graph
net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white", directed=True)

# Configure physics for better layout
net.force_atlas_2based()

# Add nodes to the graph
node_colors = {
    "Person": "#FF6B6B",
    "Organization": "#4ECDC4",
    "Location": "#45B7D1",
    "Award": "#FFA07A"
}

for node in graph_document.nodes:
    color = node_colors.get(node.type, "#95E1D3")
    title = f"Type: {node.type}<br>" + "<br>".join([f"{k}: {v}" for k, v in node.properties.items()])
    net.add_node(node.id, label=node.id, color=color, title=title, size=25)

# Add edges (relationships) to the graph
for relationship in graph_document.relationships:
    title = relationship.type
    if relationship.properties:
        title += "<br>" + "<br>".join([f"{k}: {v}" for k, v in relationship.properties.items()])
    net.add_edge(
        relationship.source.id, 
        relationship.target.id, 
        label=relationship.type,
        title=title,
        arrows="to"
    )

# Save and display the graph
output_file = "knowledge_graph.html"
net.save_graph(output_file)
print(f"Knowledge graph saved to {output_file}")
print("Open the file in your browser to view the interactive graph.")

try:
    import webbrowser
    import os
    webbrowser.open(f"file://{os.path.abspath(output_file)}")
except:
    print("Could not open browser automatically")

# Function to query the knowledge graph
def query_knowledge_graph(query_text, graph_document):
    """
    Query the knowledge graph using the query text and return relevant results.
    """
    results = []
    
    # Clean the query text (remove special characters)
    query_text = query_text.replace("?", "").strip()

    # Search for matching relationships
    for relationship in graph_document.relationships:
        # Check if query matches relationship type
        if query_text.lower() in relationship.type.lower():
            results.append({
                "source": relationship.source.id,
                "target": relationship.target.id,
                "type": relationship.type,
                "properties": relationship.properties
            })
        # Check if query matches relationship source or target
        elif (query_text.lower() in relationship.source.id.lower() or 
              query_text.lower() in relationship.target.id.lower()):
            results.append({
                "source": relationship.source.id,
                "target": relationship.target.id,
                "type": relationship.type,
                "properties": relationship.properties
            })

    # Search for nodes matching the query
    for node in graph_document.nodes:
        # Check node ID
        if query_text.lower() in node.id.lower():
            results.append({
                "id": node.id,
                "type": node.type,
                "properties": node.properties
            })
        # Check node type
        elif query_text.lower() in node.type.lower():
            results.append({
                "id": node.id,
                "type": node.type,
                "properties": node.properties
            })
        # Check node properties
        elif any(query_text.lower() in str(value).lower() for value in node.properties.values()):
            results.append({
                "id": node.id,
                "type": node.type,
                "properties": node.properties
            })

    # Print the query result
    if not results:
        print("No results found for the query.")
    else:
        print("Query Result:")
        for result in results:
            print(result)

    return results

# Example usage (simple query)
query_text = "Marie Curie"
query_result = query_knowledge_graph(query_text, graph_document)

# Display the query result
for result in query_result:
    if "id" in result:
        # This is a node
        print(f"Node: {result['id']} ({result['type']}) - Properties: {result['properties']}")
    else:
        # This is a relationship
        print(f"Relationship: {result['source']} --[{result['type']}]--> {result['target']} - Properties: {result['properties']}")
