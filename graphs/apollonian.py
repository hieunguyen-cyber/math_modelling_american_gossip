from typing import Tuple, List
import networkx as nx

def generate_apollonian(generations: int = 5, seed: int | None = None) -> nx.Graph:
    """Generate an Apollonian network by recursive triangular subdivision.

    Starts with a single triangle (3 nodes).
    At generation 0, adds 1 node (4 nodes total).
    At generation 1, adds 3 nodes (7 nodes total).
    The number of nodes N_n = 0.5 * (3**(n+1) + 5).
    """
    G = nx.Graph()
    # initial triangle
    G.add_nodes_from([0, 1, 2])
    G.add_edges_from([(0,1),(1,2),(2,0)])

    # faces stored as tuples of node ids
    faces: List[Tuple[int,int,int]] = [(0,1,2)]
    next_node = 3

    for gen in range(generations + 1):
        current_faces = faces[:]
        faces = []
        for face in current_faces:
            a, b, c = face
            G.add_node(next_node)
            G.add_edges_from([(next_node, a), (next_node, b), (next_node, c)])
            faces.extend([
                (next_node, a, b),
                (next_node, b, c),
                (next_node, c, a)
            ])
            next_node += 1

    return G
