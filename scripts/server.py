"""Lightweight Flask server to generate graphs and stream gossip histories.

Endpoints:
- POST /api/generate -> JSON payload {graph_type, n, params...} returns generated nodes, edges, history
"""
from flask import Flask, request, jsonify
from typing import Any, Dict
import random
from graphs import generate_ba, generate_ws, generate_er, generate_apollonian
from propagation import GossipPropagationEngine, ProbabilisticGossip

app = Flask(__name__)


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
        return generate_apollonian(n, seed=seed)
    raise ValueError('unknown graph type')


@app.route('/api/generate', methods=['POST'])
def api_generate():
    params = request.get_json() or {}
    G = build_graph(params)
    # choose victim with degree>0
    victims = [v for v,d in G.degree() if d>0]
    if not victims:
        victim = 0
        origin = 0
        history = []
    else:
        victim = int(params.get('victim', random.choice(victims)))
        neigh = list(G.neighbors(victim))
        origin = int(params.get('origin', neigh[0] if neigh else victim))
        mode = params.get('mode', 'local')
        q = float(params.get('q', 1.0))
        if mode == 'probabilistic':
            engine = ProbabilisticGossip(G)
            res = engine.run(victim, origin, q=q, one_shot=False)
        else:
            engine = GossipPropagationEngine(G)
            res = engine.run(victim, origin)
        history = [[int(x) for x in frame] for frame in res['history']]

    nodes = [{'id': int(n), 'label': str(n)} for n in G.nodes()]
    edges = [{'from': int(u), 'to': int(v)} for u, v in G.edges()]
    return jsonify({'meta': {'graph_type': params.get('graph_type','ba'), 'n': G.number_of_nodes(), 'victim': victim, 'origin': origin}, 'nodes': nodes, 'edges': edges, 'history': history})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
