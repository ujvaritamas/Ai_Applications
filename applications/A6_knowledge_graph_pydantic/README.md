# Knowledge graph

- Entities are the primary subjects within the graph - whether people, organizations, places, or events - and each holds attributes relevant to that subject, like a "Person" entity with attributes of name, age, and occupation.
- Relationships between entities - often called edges - show how these entities connect and interact, such as a "Person" node being linked to a "Company" node by a "works for" relationship
- Properties add additional context, or metadata like dates or locations, to entities and edges.

Today, you no longer need to be an expert in graph theory or taxonomies to build your own graph, especially when LLMs can help simplify entity recognition and relationship extraction.


Language models change the game when it comes to automating the extraction of entities and relationships from unstructured data, because they understand context and identify complex patterns.


Building a Knowledge Graph: Start with Your Data
An ontology outlines the graph’s structure, relationships, and properties, and defines how entities are connected and categorized. It’s basically the way you represent information in your knowledge graph.
Some ontologies are simple to design, covering only basic entities and straightforward relationships, whereas others are complex, encompassing detailed hierarchies, multiple layers of relationships, and domain-specific attributes.

Depending on your project’s requirements, you might even consider working with a domain expert to define an ontology with a structure that accurately reflects the data’s entities and relationships.

2 main knowledge graph:
-  RDF triple stores (rdf - resource description framework)
   -  An example of this is "Alice works for AcmeCorp," which has three parts: Alice (subject), worksFor (predicate), and AcmeCorp (object).
   -   Alice is 30 years old, we add a triple: Alice - hasAge - 30.
   -   SPARQL query language
-  property graphs
   -  they store multiple properties in nodes and edges, and support attribute-rich queries directly on these.
   -  For instance, each node (like a Person node) can contain several key-value pairs, such as name, age, and occupation. Relationships (edges) between nodes can also carry properties, such as reportsTo making this type of graph advantageous for applications requiring complex queries.
   -  supported by Neo4j, Cypher query language

For example, a Person entity may relate to an Organization entity through an employed_by relationship.

Analyzing patterns within highly connected, continuously changing data, then you might go with a property graph database  (Neo4j)



```
uv init example
cd example

uv add pydantic
uv add langchain
uv add langchain_ollama
uv add beautifulsoup4
uv add requests
git add matplotlib
git add networkx
```
