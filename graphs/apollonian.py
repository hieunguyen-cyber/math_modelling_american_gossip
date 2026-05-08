from typing import Tuple, List
import networkx as nx

def generate_apollonian(target_nodes: int = 100, seed: int | None = None) -> nx.Graph:
    """Generate an Apollonian network by recursive triangular subdivision.

    Start with a single triangle of 3 nodes fully connected. At each step,
    pick a triangular face and add a new node connected to the three vertices
    of that face, which produces three new faces. Continue until reaching
    target_nodes.
    """
    G = nx.Graph()
    # initial triangle
    G.add_nodes_from([0, 1, 2])
    G.add_edges_from([(0,1),(1,2),(2,0)])

    # faces stored as tuples of node ids (a,b,c) with a < b < c
    faces: List[Tuple[int,int,int]] = [(0,1,2)]
    next_node = 3

    # deterministic face selection: iterate faces in FIFO order
    idx = 0
    while next_node < target_nodes and faces:
        face = faces[idx % len(faces)]
        a,b,c = face
        # add new node connected to vertices of face
        G.add_node(next_node)
        G.add_edges_from([(next_node,a),(next_node,b),(next_node,c)])

        # remove the used face and add the three subdivided faces
        # removing the old face from list
        faces.pop(idx % (len(faces)))
        faces.extend([
            tuple(sorted((next_node,a,b))),
            tuple(sorted((next_node,b,c))),
            tuple(sorted((next_node,c,a)))
        ])
        next_node += 1
        # keep idx within bounds
        if faces:
            idx = idx % len(faces)

    return G
