from typing import Iterable, Tuple
import networkx as nx

def largest_component(G: nx.Graph) -> nx.Graph:
    if nx.is_empty(G):
        return G
    comps = list(nx.connected_components(G))
    largest = max(comps, key=len)
    return G.subgraph(largest).copy()
