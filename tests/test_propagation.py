import networkx as nx
from propagation import GossipPropagationEngine, ProbabilisticGossip

def test_basic_chain():
    G = nx.path_graph(5)
    # 0 - 1 - 2 - 3 - 4
    victim = 2
    origin = 1
    engine = GossipPropagationEngine(G)
    res = engine.run(victim, origin)
    # neighbors of victim are 1 and 3
    # path from 1 to 3 goes through 2
    # but 2 is the victim! Let's check sub_nodes.
    # sub_nodes = {1, 3} | {2} = {1, 2, 3}.
    # origin 1 -> 2 -> 3
    assert 3 in res['reached']

def test_base_constrain_to_neighbors_false():
    G = nx.path_graph(5)
    victim = 2
    origin = 0
    engine = GossipPropagationEngine(G)
    # By default constrain=True, so origin=0 not in sub_nodes => empty
    res1 = engine.run(victim, origin)
    assert not res1['reached']
    
    # constrain=False
    res2 = engine.run(victim, origin, constrain_to_neighbors=False)
    assert 1 in res2['reached']
    assert 3 in res2['reached']
    assert len(res2['visited']) == 5

def test_probabilistic_q0():
    G = nx.complete_graph(4)
    victim = 0
    origin = 1
    engine = ProbabilisticGossip(G)
    res = engine.run(victim, origin, q=0.0)
    assert len(res['reached']) == 1 # only origin
    assert len(res['visited']) == 1 # only origin

def test_probabilistic_q1():
    G = nx.complete_graph(4)
    victim = 0
    origin = 1
    engine = ProbabilisticGossip(G)
    res = engine.run(victim, origin, q=1.0)
    assert len(res['reached']) == 3 # 1, 2 and 3
    assert len(res['visited']) == 4 # 0, 1, 2, 3

def test_probabilistic_entire_network():
    G = nx.path_graph(5)
    victim = 2
    origin = 0
    engine = ProbabilisticGossip(G)
    res = engine.run(victim, origin, constrain_to_neighbors=False, q=1.0)
    assert len(res['visited']) == 5
    assert len(res['reached']) == 2 # neighbors of 2 are 1, 3

