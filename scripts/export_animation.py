"""Export propagation histories as GIF/MP4 animations.

Usage:
    python scripts/export_animation.py --source outputs/dashboard/assets/data.json --out outputs/animations/run.gif
"""
import argparse
import json
import os
import imageio
import matplotlib.pyplot as plt
import networkx as nx


def render_animation(data_path: str, out_path: str, fps: int = 4):
    with open(data_path, 'r') as fh:
        data = json.load(fh)
    G = nx.Graph()
    for n in data['nodes']:
        G.add_node(n['id'])
    for e in data['edges']:
        G.add_edge(e['from'], e['to'])

    history = data.get('history', [])
    pos = nx.spring_layout(G, seed=42)
    frames = []
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    # render frames to temporary PNGs in memory
    for t, frame in enumerate(history):
        plt.figure(figsize=(6,4))
        node_colors = ['red' if n in frame else '#888888' for n in G.nodes()]
        nx.draw(G, pos=pos, with_labels=True, node_color=node_colors, node_size=120)
        tmp = f'_anim_frame_{t}.png'
        plt.savefig(tmp, dpi=150)
        plt.close()
        frames.append(imageio.v2.imread(tmp))
        os.remove(tmp)

    if out_path.lower().endswith('.gif'):
        imageio.mimsave(out_path, frames, fps=fps)
    else:
        # write mp4
        imageio.mimsave(out_path, frames, fps=fps, format='FFMPEG')
    print('Saved animation to', out_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='web/assets/data.json')
    parser.add_argument('--out', default='outputs/animations/propagation.gif')
    args = parser.parse_args()
    render_animation(args.source, args.out)
