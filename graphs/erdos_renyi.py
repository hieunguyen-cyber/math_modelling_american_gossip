from typing import Optional
import networkx as nx

def generate_er(n: int, p: float, seed: Optional[int] = None) -> nx.Graph:
    """Generate Erdős-Rényi G(n,p) graph."""
    return nx.erdos_renyi_graph(n, p, seed=seed)
