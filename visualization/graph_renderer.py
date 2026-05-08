from typing import Optional
from pyvis.network import Network
import networkx as nx

def render_pyvis(G: nx.Graph, out_html: str = "graph.html", height: str = "700px") -> None:
    net = Network(height=height)
    net.from_nx(G)
    net.show(out_html)
