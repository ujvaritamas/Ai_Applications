"""
Knowledge Graph Generation and Visualization Tool

This module provides functionality to extract entities and relationships from text
using LLM-based transformation and visualize them as interactive knowledge graphs.
"""

import argparse
import json
import logging
import os
import sys
import webbrowser
from pathlib import Path
from typing import List, Optional, Dict, Any

from LLMGraphTransformer import LLMGraphTransformer
from LLMGraphTransformer.schema import NodeSchema, RelationshipSchema, GraphDocument
from langchain_core.documents import Document
from langchain_ollama import ChatOllama
from pyvis.network import Network
import matplotlib.pyplot as plt
import networkx as nx


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Constants
DEFAULT_NODE_COLORS = {
    "Person": "#FF6B6B",
    "Organization": "#4ECDC4",
    "Location": "#45B7D1",
    "Award": "#FFA07A",
    "default": "#95E1D3"
}

DEFAULT_NETWORK_CONFIG = {
    "height": "750px",
    "width": "100%",
    "bgcolor": "#222222",
    "font_color": "white",
    "directed": True,
    "node_size": 25
}


#create in memory knowledge graph
def create_knowledge_graph(
    text: str,
    node_schemas: List[NodeSchema],
    relationship_schemas: List[RelationshipSchema],
    additional_instructions: str,
    llm: Any
) -> Optional[GraphDocument]:
    """
    Extract knowledge graph from text using LLM-based transformation.
    
    Args:
        text: Input text to extract entities and relationships from
        node_schemas: List of allowed node types and their properties
        relationship_schemas: List of allowed relationship types
        additional_instructions: Custom instructions for the LLM
        llm: Language model instance for graph extraction
        
    Returns:
        GraphDocument containing extracted nodes and relationships, or None if error
    """
    try:
        logger.info("Initializing LLM Graph Transformer...")
        llm_transformer = LLMGraphTransformer(
            llm=llm,
            allowed_nodes=node_schemas,
            allowed_relationships=relationship_schemas,
            additional_instructions=additional_instructions
        )

        document = Document(page_content=text)
        logger.info("Converting text to knowledge graph...")
        graph_document = llm_transformer.convert_to_graph_document(document)
        
        logger.info(f"Extraction complete: {len(graph_document.nodes)} nodes, "
                   f"{len(graph_document.relationships)} relationships")
        return graph_document
        
    except Exception as e:
        logger.error(f"Error creating knowledge graph: {e}", exc_info=True)
        return None


def export_to_json(graph_document: GraphDocument, output_path: str) -> bool:
    """
    Export graph document to JSON format.
    
    Args:
        graph_document: The graph document to export
        output_path: Path to save the JSON file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        graph_data = {
            "nodes": [
                {
                    "id": node.id,
                    "type": node.type,
                    "properties": node.properties
                }
                for node in graph_document.nodes
            ],
            "relationships": [
                {
                    "source": rel.source.id,
                    "target": rel.target.id,
                    "type": rel.type,
                    "properties": rel.properties
                }
                for rel in graph_document.relationships
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Graph exported to JSON: {output_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error exporting to JSON: {e}", exc_info=True)
        return False


def visualize(
    graph_document: GraphDocument,
    output_file: str = "knowledge_graph.html",
    node_colors: Optional[Dict[str, str]] = None,
    network_config: Optional[Dict[str, Any]] = None,
    auto_open: bool = True
) -> bool:
    """
    Visualize knowledge graph as an interactive HTML network.
    
    Args:
        graph_document: The graph document to visualize
        output_file: Path to save the HTML file
        node_colors: Custom color mapping for node types
        network_config: Custom network visualization configuration
        auto_open: Whether to automatically open the graph in browser
        
    Returns:
        True if visualization was successful, False otherwise
    """
    try:
        # Use defaults if not provided
        colors = node_colors or DEFAULT_NODE_COLORS
        config = network_config or DEFAULT_NETWORK_CONFIG
        
        logger.info("Creating network visualization...")
        
        # Create a network graph
        net = Network(
            height=config["height"],
            width=config["width"],
            bgcolor=config["bgcolor"],
            font_color=config["font_color"],
            directed=config["directed"]
        )

        # Configure physics for better layout
        net.force_atlas_2based()

        # Add nodes to the graph
        for node in graph_document.nodes:
            color = colors.get(node.type, colors["default"])
            title = f"Type: {node.type}<br>" + "<br>".join(
                [f"{k}: {v}" for k, v in node.properties.items()]
            )
            net.add_node(
                node.id,
                label=node.id,
                color=color,
                title=title,
                size=config.get("node_size", 25)
            )

        # Add edges (relationships) to the graph
        for relationship in graph_document.relationships:
            title = relationship.type
            if relationship.properties:
                title += "<br>" + "<br>".join(
                    [f"{k}: {v}" for k, v in relationship.properties.items()]
                )
            net.add_edge(
                relationship.source.id,
                relationship.target.id,
                label=relationship.type,
                title=title,
                arrows="to"
            )

        # Save the graph
        net.save_graph(output_file)
        logger.info(f"Knowledge graph saved to {output_file}")

        # Auto-open in browser
        if auto_open:
            try:
                abs_path = os.path.abspath(output_file)
                webbrowser.open(f"file://{abs_path}")
                logger.info("Graph opened in browser")
            except Exception as e:
                logger.warning(f"Could not open browser automatically: {e}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during visualization: {e}", exc_info=True)
        return False


def visualize_matplotlib(
    graph_document: GraphDocument,
    output_file: str = "knowledge_graph.png",
    figsize: tuple = (12, 8),
    node_colors: Optional[Dict[str, str]] = None,
    show_plot: bool = True
) -> bool:
    """
    Visualize knowledge graph using matplotlib and networkx.
    
    Args:
        graph_document: The graph document to visualize
        output_file: Path to save the PNG file
        figsize: Figure size as (width, height) tuple
        node_colors: Custom color mapping for node types
        show_plot: Whether to display the plot interactively
        
    Returns:
        True if visualization was successful, False otherwise
    """
    try:
        # Use defaults if not provided
        colors = node_colors or DEFAULT_NODE_COLORS
        
        logger.info("Creating matplotlib/networkx visualization...")
        
        # Create a directed graph
        nx_g = nx.DiGraph()
        
        # Add nodes with attributes
        node_color_list = []
        node_labels = {}
        
        for node in graph_document.nodes:
            nx_g.add_node(node.id, type=node.type, **node.properties)
            node_labels[node.id] = node.id
            node_color_list.append(colors.get(node.type, colors["default"]))
        
        # Add edges with attributes
        edge_labels = {}
        
        for relationship in graph_document.relationships:
            nx_g.add_edge(
                relationship.source.id,
                relationship.target.id,
                type=relationship.type,
                **relationship.properties
            )
            edge_labels[(relationship.source.id, relationship.target.id)] = relationship.type
        
        # Create visualization
        plt.figure(figsize=figsize)
        
        # Use spring layout for node positioning
        pos = nx.spring_layout(nx_g, seed=42, k=1, iterations=50)
        
        # Draw nodes
        nx.draw_networkx_nodes(
            nx_g,
            pos,
            node_color=node_color_list,
            node_size=2000,
            alpha=0.9,
            edgecolors='black',
            linewidths=2
        )
        
        # Draw labels
        nx.draw_networkx_labels(
            nx_g,
            pos,
            labels=node_labels,
            font_size=10,
            font_weight="bold",
            font_color="black"
        )
        
        # Draw edges
        nx.draw_networkx_edges(
            nx_g,
            pos,
            edge_color="gray",
            arrows=True,
            arrowsize=20,
            arrowstyle="->",
            width=2,
            alpha=0.6,
            connectionstyle="arc3,rad=0.1"
        )
        
        # Draw edge labels
        nx.draw_networkx_edge_labels(
            nx_g,
            pos,
            edge_labels=edge_labels,
            font_color="red",
            font_size=8,
            font_weight="bold"
        )
        
        plt.title("Knowledge Graph Visualization", fontsize=16, fontweight="bold")
        plt.axis("off")
        plt.tight_layout()
        
        # Save the figure
        plt.savefig(output_file, dpi=300, bbox_inches="tight", facecolor="white")
        logger.info(f"Knowledge graph saved to {output_file}")
        
        # Show plot if requested
        if show_plot:
            plt.show()
        else:
            plt.close()
        
        return True
        
    except Exception as e:
        logger.error(f"Error during matplotlib visualization: {e}", exc_info=True)
        return False



def get_default_schemas() -> tuple[List[NodeSchema], List[RelationshipSchema]]:
    """
    Get default node and relationship schemas for knowledge graph extraction.
    
    Returns:
        Tuple containing (node_schemas, relationship_schemas)
    """
    node_schemas = [
        NodeSchema(
            "Person",
            ["name", "birth_year", "death_year", "nationality", "profession"],
            "Represents an individual"
        ),
        NodeSchema(
            "Organization",
            ["name", "founding_year", "industry"],
            "Represents a group, company, or institution"
        ),
        NodeSchema(
            "Location",
            ["name"],
            "Represents a geographical area such as a city, country, or region"
        ),
        NodeSchema(
            "Award",
            ["name", "field"],
            "Represents an honor, prize, or recognition"
        )
    ]

    relationship_schemas = [
        RelationshipSchema("Person", "SPOUSE_OF", "Person"),
        RelationshipSchema("Person", "MEMBER_OF", "Organization", ["start_year", "end_year", "year"]),
        RelationshipSchema("Person", "AWARDED", "Award", ["year"]),
        RelationshipSchema("Person", "LOCATED_IN", "Location"),
        RelationshipSchema("Organization", "LOCATED_IN", "Location")
    ]
    
    return node_schemas, relationship_schemas


def get_example_text() -> str:
    """Get example text for demonstration."""
    return """Marie Curie, born in 1867, was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity.
She was the first woman to win a Nobel Prize, the first person to win a Nobel Prize twice, and the only person to win a Nobel Prize in two scientific fields.
Her husband, Pierre Curie, was a co-winner of her first Nobel Prize, making them the first-ever married couple to win the Nobel Prize and launching the Curie family legacy of five Nobel Prizes.
She was, in 1906, the first woman to become a professor at the University of Paris."""


def parse_arguments() -> argparse.Namespace:
    """
    Parse command line arguments.
    
    Returns:
        Parsed command line arguments
    """
    parser = argparse.ArgumentParser(
        description="Generate and visualize knowledge graphs from text using LLM"
    )
    
    parser.add_argument(
        "--text",
        type=str,
        help="Input text to process. If not provided, uses example text"
    )
    
    parser.add_argument(
        "--text-file",
        type=str,
        help="Path to text file to process"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="gemma3:4b",
        help="Ollama model to use (default: gemma3:4b)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="knowledge_graph.html",
        help="Output HTML file path (default: knowledge_graph.html)"
    )
    
    parser.add_argument(
        "--viz-type",
        type=str,
        choices=["pyvis", "matplotlib", "both"],
        default="pyvis",
        help="Visualization type: pyvis (interactive HTML), matplotlib (static image), or both (default: pyvis)"
    )
    
    parser.add_argument(
        "--matplotlib-output",
        type=str,
        default="knowledge_graph.png",
        help="Output PNG file path for matplotlib visualization (default: knowledge_graph.png)"
    )
    
    parser.add_argument(
        "--json-export",
        type=str,
        help="Export graph data to JSON file"
    )
    
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Don't automatically open the graph in browser"
    )
    
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="LLM temperature (default: 0.0)"
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    return parser.parse_args()


def main():
    """Main execution function."""
    # Parse arguments
    args = parse_arguments()
    
    # Set logging level
    logger.setLevel(getattr(logging, args.log_level))
    
    # Get input text
    if args.text_file:
        try:
            with open(args.text_file, 'r', encoding='utf-8') as f:
                text = f.read()
            logger.info(f"Loaded text from {args.text_file}")
        except Exception as e:
            logger.error(f"Error reading file {args.text_file}: {e}")
            sys.exit(1)
    elif args.text:
        text = args.text
    else:
        text = get_example_text()
        logger.info("Using example text")
    
    # Validate input
    if not text.strip():
        logger.error("Input text is empty")
        sys.exit(1)
    
    # Get schemas
    node_schemas, relationship_schemas = get_default_schemas()
    
    # Additional instructions for extraction
    additional_instructions = "- All names must be extracted as uppercase"
    
    # Initialize LLM
    try:
        logger.info(f"Initializing Ollama model: {args.model}")
        llm = ChatOllama(
            model=args.model,
            temperature=args.temperature,
        )
    except Exception as e:
        logger.error(f"Error initializing LLM: {e}")
        sys.exit(1)
    
    # Create knowledge graph
    graph_document = create_knowledge_graph(
        text=text,
        node_schemas=node_schemas,
        relationship_schemas=relationship_schemas,
        additional_instructions=additional_instructions,
        llm=llm
    )
    
    if not graph_document:
        logger.error("Failed to create knowledge graph")
        sys.exit(1)
    
    # Display results
    logger.info(f"\n--- Extraction Results ---")
    logger.info(f"Nodes ({len(graph_document.nodes)}):")
    for node in graph_document.nodes:
        logger.info(f"  - {node.id} ({node.type}): {node.properties}")
    
    logger.info(f"\nRelationships ({len(graph_document.relationships)}):")
    for rel in graph_document.relationships:
        logger.info(f"  - {rel.source.id} --[{rel.type}]--> {rel.target.id}")
    
    # Export to JSON if requested
    if args.json_export:
        if export_to_json(graph_document, args.json_export):
            logger.info(f"Successfully exported to {args.json_export}")
    
    # Visualize based on selected type
    success = True
    
    if args.viz_type in ["pyvis", "both"]:
        success = visualize(
            graph_document=graph_document,
            output_file=args.output,
            auto_open=not args.no_browser
        ) and success
    
    if args.viz_type in ["matplotlib", "both"]:
        success = visualize_matplotlib(
            graph_document=graph_document,
            output_file=args.matplotlib_output,
            show_plot=not args.no_browser
        ) and success
    
    if success:
        logger.info("Knowledge graph generation complete!")
        sys.exit(0)
    else:
        logger.error("Visualization failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

