from typing import Optional
import networkx as nx

def generate_ba(n: int, m: int, seed: Optional[int] = None) -> nx.Graph:
    """Generate Barabási-Albert network using NetworkX wrapper.

    Args:
        n: number of nodes
        m: number of edges to attach from a new node to existing nodes
        seed: RNG seed

    Returns:
        networkx.Graph
    """
    return nx.barabasi_albert_graph(n, m, seed=seed)
