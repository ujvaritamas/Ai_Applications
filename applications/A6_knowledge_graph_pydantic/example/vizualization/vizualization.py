import matplotlib.pyplot as plt
import networkx as nx

from knowledge_graph.knowledge_graph import KnowledgeGraph

from pyvis.network import Network

def render_graph(kg: KnowledgeGraph):
    G = nx.DiGraph()

    for node in kg.nodes:
        G.add_node(node.id, label=node.type, **(node.properties or {}))

    for edge in kg.edges:
        G.add_edge(edge.source, edge.target, label=edge.relationship)

    plt.figure(figsize=(15, 10))
    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="lightblue")
    nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=70)
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")

    edge_labels = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")

    plt.title("Knowledge Graph Visualization", fontsize=15)
    plt.show()


def visualize_knowledge_graph_pyvis(kg: KnowledgeGraph, output_file: str = "knowledge_graph.html"):
    """
    Visualize a knowledge graph using pyvis with interactive features.
    
    Args:
        kg: KnowledgeGraph object containing nodes and edges
        output_file: Name of the output HTML file (default: "knowledge_graph.html")
    """
    # Create a pyvis network with cdn_resources set to 'remote'
    net = Network(
        notebook=True,
        height="1200px", 
        width="100%", 
        bgcolor="#222222", 
        font_color="white",
        #dn_resources='remote'
        directed=True
    )
    
    # Enable physics for interactive movement
    #net.barnes_hut()

    # Configure physics for better layout
    net.force_atlas_2based()
    
    # Add nodes to the network
    for node in kg.nodes:
        # Create label with properties
        label = f"{node.id}\n({node.type})"
        if node.properties:
            props_str = "\n".join([f"{k}: {v}" for k, v in node.properties.items()])
            label += f"\n{props_str}"
        
        # Add node with color based on type
        net.add_node(
            node.id,
            label=label,
            title=f"Type: {node.type}\nProperties: {node.properties}",
            shape="dot",
            size=25
        )
    
    # Add edges to the network
    for edge in kg.edges:
        net.add_edge(
            edge.source,
            edge.target,
            label=edge.relationship,
            title=edge.relationship
        )
    
    # Configure physics options for better interactivity
    net.set_options("""
    {
        "physics": {
            "enabled": true,
            "barnesHut": {
                "gravitationalConstant": -30000,
                "centralGravity": 0.3,
                "springLength": 200,
                "springConstant": 0.04,
                "damping": 0.09
            }
        },
        "interaction": {
            "dragNodes": true,
            "dragView": true,
            "zoomView": true
        }
    }
    """)
    
    # Save and show the graph
    try:
        net.show(output_file)
        print(f"Knowledge graph saved to {output_file}")
    except Exception as e:
        # Fallback: use write_html instead
        print(f"Error with show(): {e}")
        print("Trying alternative method...")
        net.write_html(output_file)
        print(f"Knowledge graph saved to {output_file}")
    
    return output_file