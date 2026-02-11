from LLMGraphTransformer import LLMGraphTransformer
from LLMGraphTransformer.schema import NodeSchema, RelationshipSchema, GraphDocument
from langchain_core.documents import Document
from langchain_ollama import ChatOllama




def create_knowledge_graph(text: str, node_schemas: list, relationship_schemas: list, additional_instructions: str) -> GraphDocument:
    llm_transformer = LLMGraphTransformer(
        llm=llm,
        allowed_nodes=node_schemas,
        allowed_relationships=relationship_schemas,
        additional_instructions=additional_instructions
    )

    document = Document(page_content=text)
    #create graph document with the llm
    graph_document = llm_transformer.convert_to_graph_document(document)

    print(f"Nodes: {graph_document.nodes}")
    print(f"Relationships: {graph_document.relationships}")

    return graph_document


def vizualize(graph_document: GraphDocument):
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

    # # Add edges (relationships) to the graph
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

graph_document = create_knowledge_graph(text, node_schemas, relationship_schemas, additional_instructions)

print(f"Nodes: {graph_document.nodes}")
print(f"Relationships: {graph_document.relationships}")

vizualize(graph_document)
