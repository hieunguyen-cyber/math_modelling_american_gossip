"""Lightweight Flask server to generate graphs and stream gossip histories.

Endpoints:
- POST /api/generate -> JSON payload {graph_type, n, params...} returns generated nodes, edges, history
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from typing import Any, Dict
import random
from graphs import generate_ba, generate_ws, generate_er, generate_apollonian
from propagation import GossipPropagationEngine, ProbabilisticGossip


app = Flask(__name__, static_folder='../web', static_url_path='')

@app.route('/')
def index():
    return app.send_static_file('index.html')


def build_graph(params: Dict[str, Any]):
    gtype = params.get('graph_type', 'ba')
    n = int(params.get('n', 200))
    seed = params.get('seed', None)
    if gtype == 'ba':
        return generate_ba(n, int(params.get('m', 3)), seed=seed)
    if gtype == 'ws':
        return generate_ws(n, int(params.get('k', 6)), float(params.get('p', 0.1)), seed=seed)
    if gtype == 'er':
        return generate_er(n, float(params.get('p', 0.01)), seed=seed)
    if gtype == 'apollonian':
        import math
        # n from UI is target nodes. N_n = 0.5 * (3**(gen+1) + 5) => 3**(gen+1) = 2*N_n - 5
        if n > 20:
            gen = int(round(math.log(2*n - 5, 3))) - 1
        else:
            gen = n
        gen = max(0, min(gen, 8)) # max 8 generations = 9845 nodes
        return generate_apollonian(generations=gen, seed=seed)
    raise ValueError('unknown graph type')


@app.route('/api/generate', methods=['POST'])
def api_generate():
    params = request.get_json() or {}
    
    if 'custom_edges' in params:
        import networkx as nx
        G = nx.Graph()
        if 'custom_nodes' in params:
            G.add_nodes_from([int(n['id']) for n in params['custom_nodes']])
        for e in params['custom_edges']:
            G.add_edge(int(e['from']), int(e['to']))
    else:
        G = build_graph(params)

    # choose victim with degree>0
    victims = [v for v,d in G.degree() if d>0]
    if not victims:
        victim = 0
        origin = 0
        history = []
    else:
        v_param = params.get('victim')
        victim = int(v_param) if v_param is not None else random.choice(victims)
        neigh = list(G.neighbors(victim))
        o_param = params.get('origin')
        origin = int(o_param) if o_param is not None else (neigh[0] if neigh else victim)
        mode = params.get('mode', 'local')
        q = float(params.get('q', 1.0))
        if mode.startswith('probabilistic'):
            engine = ProbabilisticGossip(G)
            one_shot = params.get('attempt') == 'one-shot'
            constrain = mode == 'probabilistic'
            res = engine.run(victim, origin, q=q, one_shot=one_shot, constrain_to_neighbors=constrain)
        elif mode == 'k-hop':
            from propagation.kth_neighbor import induced_k_hop_subgraph
            k = int(params.get('k', 2))
            subgraph = induced_k_hop_subgraph(G, victim, k)
            engine = GossipPropagationEngine(subgraph)
            res = engine.run(victim, origin, constrain_to_neighbors=False)
        else:
            engine = GossipPropagationEngine(G)
            res = engine.run(victim, origin)
        history = [[int(x) for x in frame] for frame in res['history']]

    nodes = [{'id': int(n), 'label': str(n)} for n in G.nodes()]
    edges = [{'from': int(u), 'to': int(v)} for u, v in G.edges()]
    return jsonify({'meta': {'graph_type': params.get('graph_type','ba'), 'n': G.number_of_nodes(), 'victim': victim, 'origin': origin}, 'nodes': nodes, 'edges': edges, 'history': history})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
