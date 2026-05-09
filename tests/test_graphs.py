import networkx as nx
from graphs.apollonian import generate_apollonian
from graphs.utils import degree_distribution, average_nearest_neighbor_degree

def test_apollonian_nodes():
    # n=0 -> 4
    # n=1 -> 7
    # n=2 -> 16
    assert generate_apollonian(0).number_of_nodes() == 4
    assert generate_apollonian(1).number_of_nodes() == 7
    assert generate_apollonian(2).number_of_nodes() == 16

def test_graph_utils():
    G = nx.complete_graph(4)
    # nodes 0,1,2,3 all have degree 3.
    # knn is 3 for all nodes.
    k_vals, p_k = degree_distribution(G)
    assert len(k_vals) == 1
    assert k_vals[0] == 3
    assert p_k[0] == 1.0
    
    knn = average_nearest_neighbor_degree(G)
    assert knn[3] == 3.0
