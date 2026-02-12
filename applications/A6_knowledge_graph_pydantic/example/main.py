import knowledge_graph.knowledge_graph as knowledge_graph
import json
from typing import Any

from langchain_ollama import ChatOllama
from langchain.agents import create_agent

from bs4 import BeautifulSoup
import requests
import vizualization.vizualization as vizualization

json_schema: dict[str, Any] = knowledge_graph.KnowledgeGraph.model_json_schema()
print(json.dumps(json_schema, indent=2))


model = "llama3.1:8b"   #model need to support tool calling
temperature = 0

llm = ChatOllama(
    model=model,
    temperature=temperature,
)

agent = create_agent(
    model=llm,
    response_format=knowledge_graph.KnowledgeGraph,
    system_prompt="""
            Your job is to create a knowledge graph based on the given article text.
            Example:
                John and Jane Doe are siblings. Jane is 25 and 5 years younger than John.
                Node(id="John Doe", type="Person", properties={{"age": 30}})
                Node(id="Jane Doe", type="Person", properties={{"age": 25}})
                Edge(source="John Doe", target="Jane Doe", relationship="Siblings")
            """
)

def generate_knowledge_graph(url: str) -> knowledge_graph.KnowledgeGraph:
    headers = {
        "User-Agent": f"YourAppName/1.0 ({url}; your_email@example.com)"
    }
    html = requests.get(url, headers=headers).text
    text = BeautifulSoup(html, "html.parser").get_text()

    #text = "John and Jane Doe are siblings."
#    text = """
#    Steven Paul Jobs (February 24, 1955 – October 5, 2011) was an American businessman, co-inventor, and investor. A pioneer of the personal computer revolution of the 1970s and 1980s, Jobs co-founded Apple Inc. (as Apple Computer Company) with Steve Wozniak and Ronald Wayne in 1976. After the company's board of directors fired him in 1985, he founded NeXT the same year and purchased Pixar in 1986, becoming its chairman and majority shareholder until 2007. Jobs returned to Apple in 1997 as CEO, where he was closely involved with the creation and promotion of many of the company's most influential products until his resignation in 2011.
#
#Jobs was born in San Francisco in 1955 and adopted shortly afterwards. He attended Reed College in 1972 before withdrawing that same year. In 1974, he traveled through India, seeking enlightenment before later studying Zen Buddhism. He and Wozniak co-founded Apple in 1976 to further develop and sell Wozniak's Apple I personal computer. Together, the duo gained fame and wealth a year later with production and sale of the Apple II, one of the first highly successful mass-produced microcomputers.
#
#Jobs saw the commercial potential of the Xerox Alto in 1979, which was mouse-driven and had a graphical user interface (GUI). This led to the development of the largely unsuccessful Apple Lisa in 1983, followed by the breakthrough Macintosh in 1984, the first mass-produced computer with a GUI. The Macintosh launched the desktop publishing industry in 1985 (for example, the Aldus PageMaker) with the addition of the Apple LaserWriter, the first laser printer to feature vector graphics and PostScript.
#
#In 1985, Jobs departed Apple after a long power struggle with the company's board and its then-CEO, John Sculley. That same year, Jobs took some Apple employees with him to found NeXT, a computer platform development company that specialized in computers for higher-education and business markets, serving as its CEO. In 1986, he bought the computer graphics division of Lucasfilm, which was spun off independently as Pixar.[2] Pixar produced the first computer-animated feature film, Toy Story (1995), and became a leading animation studio, producing dozens of commercially successful and critically acclaimed films.
#
#
#"""
    
    #print(text[2000:6000])

    #make the text smaller
    text = text[2000:3000]
    print(text)
    #exit(0)

    prompt = {
        "messages": [
            {"role": "user", 
            "content": f"USER: Generate a knowledge graph based on this article text: {text}"
            }
        ]
    }

    print(f"calling the agent -> {model}")
    result = agent.invoke(prompt)

    return result["structured_response"]


kg = generate_knowledge_graph("https://en.wikipedia.org/wiki/Ant%C3%B3nio_Jos%C3%A9_Seguro")
print(f"result: {kg}")

#vizualization.render_graph(kg)
vizualization.visualize_knowledge_graph_pyvis(kg)