import networkx as nx
from propagation import GossipPropagationEngine

def test_basic_chain():
    G = nx.path_graph(5)
    victim = 2
    origin = 1
    engine = GossipPropagationEngine(G)
    res = engine.run(victim, origin)
    # neighbors of victim are 1 and 3; origin 1 should reach 3 via constrained BFS
    assert 3 in res['reached']
