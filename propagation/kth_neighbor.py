from typing import Set
import networkx as nx

def induced_k_hop_subgraph(G: nx.Graph, center: int, k: int) -> nx.Graph:
    """Return the induced subgraph of nodes within k hops from center (including center).

    For k=1 this is the center plus its neighbors. For k=0 returns node alone.
    """
    if k < 0:
        raise ValueError("k must be >= 0")
    nodes = {center}
    frontier = {center}
    for _ in range(k):
        next_frontier = set()
        for u in frontier:
            next_frontier.update(set(G.neighbors(u)))
        next_frontier -= nodes
        if not next_frontier:
            break
        nodes.update(next_frontier)
        frontier = next_frontier
    return G.subgraph(nodes).copy()
