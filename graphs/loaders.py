from typing import Iterable, List
import networkx as nx

def load_edgelist(path: str, delimiter: str = " ") -> nx.Graph:
    """Load edge list into a NetworkX graph."""
    return nx.read_edgelist(path, delimiter=delimiter, nodetype=int)

def load_adjacency_list(path: str) -> nx.Graph:
    """Load adjacency list file into a NetworkX graph."""
    return nx.read_adjlist(path, nodetype=int)

def load_csv(path: str, source_col: str = "source", target_col: str = "target") -> nx.Graph:
    import pandas as pd
    df = pd.read_csv(path)
    edges = list(zip(df[source_col], df[target_col]))
    G = nx.Graph()
    G.add_edges_from(edges)
    return G
