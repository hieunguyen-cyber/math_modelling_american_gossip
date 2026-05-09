from typing import Iterable, Tuple, Dict, List
import networkx as nx
import numpy as np

def largest_component(G: nx.Graph) -> nx.Graph:
    if nx.is_empty(G):
        return G
    comps = list(nx.connected_components(G))
    largest = max(comps, key=len)
    return G.subgraph(largest).copy()

def degree_distribution(G: nx.Graph) -> Tuple[np.ndarray, np.ndarray]:
    """Return the degree distribution P(k) as arrays of k and P(k)."""
    degrees = [d for n, d in G.degree()]
    counts = np.bincount(degrees)
    k_vals = np.nonzero(counts)[0]
    p_k = counts[k_vals] / len(degrees)
    return k_vals, p_k

def average_nearest_neighbor_degree(G: nx.Graph) -> Dict[int, float]:
    """Return the average nearest neighbor degree knn for each degree k."""
    knn_dict = nx.average_neighbor_degree(G)
    degree_dict = dict(G.degree())
    
    k_knn_sums = {}
    k_counts = {}
    for node, k in degree_dict.items():
        k_knn_sums[k] = k_knn_sums.get(k, 0) + knn_dict[node]
        k_counts[k] = k_counts.get(k, 0) + 1
        
    k_knn_avg = {k: k_knn_sums[k] / k_counts[k] for k in k_counts}
    return k_knn_avg

