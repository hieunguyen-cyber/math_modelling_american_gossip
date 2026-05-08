"""Build static dashboard assets (placeholder).

This script will later compile data outputs into `web/reports` and embed plots.
"""
import os
import json
import shutil
from typing import Dict, Any
from graphs import generate_ba, generate_ws, generate_er, generate_apollonian
from propagation import GossipPropagationEngine


def build_sample_graph(graph_type: str = 'ba', n: int = 100, **kwargs):
    if graph_type == 'ba':
        return generate_ba(n, kwargs.get('m', 3), seed=kwargs.get('seed'))
    if graph_type == 'ws':
        return generate_ws(n, kwargs.get('k', 6), kwargs.get('p', 0.1), seed=kwargs.get('seed'))
    if graph_type == 'er':
        return generate_er(n, kwargs.get('p', 0.01), seed=kwargs.get('seed'))
    if graph_type == 'apollonian':
        return generate_apollonian(n, seed=kwargs.get('seed'))
    raise ValueError('unknown graph type')


def export_dashboard_data(out_path: str = 'web/assets/data.json') -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    # create a small BA graph and run a constrained gossip for demo
    G = build_sample_graph('ba', n=80, m=2, seed=42)
    victim = 0
    neighbors = list(G.neighbors(victim))
    origin = neighbors[0] if neighbors else 0
    engine = GossipPropagationEngine(G)
    res = engine.run(victim, origin)

    data: Dict[str, Any] = {}
    data['meta'] = {
        'graph_type': 'BA',
        'n': G.number_of_nodes(),
        'm': 2,
        'victim': victim,
        'origin': origin,
    }
    data['nodes'] = [{'id': int(n), 'label': str(n)} for n in G.nodes()]
    data['edges'] = [{'from': int(u), 'to': int(v)} for u, v in G.edges()]
    # history: array of frontiers per timestep
    data['history'] = [[int(x) for x in frame] for frame in res['history']]

    with open(out_path, 'w') as fh:
        json.dump(data, fh, indent=2)


def build():
    # Export data and copy web static files to outputs/dashboard
    export_dashboard_data('web/assets/data.json')
    dst = 'outputs/dashboard'
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree('web', dst)
    print('Dashboard built to', dst)


if __name__ == '__main__':
    build()
