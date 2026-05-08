from typing import Optional
import networkx as nx

def generate_ws(n: int, k: int, p: float, seed: Optional[int] = None) -> nx.Graph:
    """Generate Watts-Strogatz small-world network."""
    return nx.watts_strogatz_graph(n, k, p, seed=seed)
