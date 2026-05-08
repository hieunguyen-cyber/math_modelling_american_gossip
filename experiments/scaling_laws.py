"""Compute spreading time vs degree and fit logarithmic law tau = A + B log(k)."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import Optional, List, Tuple
import argparse
import os
import random
import math
import numpy as np
import csv
from scipy.optimize import curve_fit
from graphs import generate_ba
from propagation import GossipPropagationEngine
from propagation.metrics import spreading_time
import matplotlib.pyplot as plt


def log_model(x, A, B):
    return A + B * np.log(x)


def sample_tau_vs_k(G, samples: int = 200, seed: Optional[int] = 42) -> List[Tuple[int,int]]:
    random.seed(seed)
    nodes = list(G.nodes())
    pairs = []
    for _ in range(samples):
        v = random.choice(nodes)
        k = G.degree(v)
        if k <= 0:
            continue
        origin = random.choice(list(G.neighbors(v)))
        engine = GossipPropagationEngine(G)
        res = engine.run(v, origin)
        tau = spreading_time(res['history'])
        pairs.append((k, tau))
    return pairs


def run_fit(n: int = 2000, samples: int = 400):
    G = generate_ba(n, m=3, seed=42)
    pairs = sample_tau_vs_k(G, samples=samples)
    ks = np.array([k for k,t in pairs if k>0])
    taus = np.array([t for k,t in pairs if k>0])
    # aggregate by degree: mean tau per k
    uniq = {}
    for k,t in pairs:
        if k<=0: continue
        uniq.setdefault(k, []).append(t)
    x = np.array(sorted(uniq.keys()))
    y = np.array([np.mean(uniq[k]) for k in x])

    # fit log model
    popt, pcov = curve_fit(log_model, x, y, p0=[1.0, 1.0])
    A, B = popt

    from visualization.static_plots import plot_tau_vs_k_hexbin
    out_dir = 'outputs/figures'
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Plot normal scatter with log fit
    fig, ax = plt.subplots(figsize=(6,4))
    ax.scatter(x, y, s=20, alpha=0.7, label='data')
    xs = np.linspace(x.min(), x.max(), 200)
    ax.plot(xs, log_model(xs, *popt), color='r', label=f'fit: tau={A:.2f}+{B:.2f} ln(k)')
    ax.set_xscale('log')
    ax.set_xlabel('Degree k')
    ax.set_ylabel('Spreading time tau')
    ax.legend()
    fig.tight_layout()
    out_file = os.path.join(out_dir, 'tau_vs_k_fit.png')
    fig.savefig(out_file, dpi=300)
    plt.close(fig)
    print('Saved', out_file)
    
    # 2. Plot hexbin density plot
    out_hexbin = os.path.join(out_dir, 'tau_vs_k_hexbin.png')
    fig2 = plot_tau_vs_k_hexbin(ks, taus, title="Spreading Time vs Degree Density (BA Network)", outpath=out_hexbin)
    plt.close(fig2)
    print('Saved', out_hexbin)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=2000)
    parser.add_argument('--samples', type=int, default=400)
    args = parser.parse_args()
    run_fit(args.n, args.samples)
