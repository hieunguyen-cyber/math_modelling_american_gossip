"""Collect distribution of spreading times and fit to exponential."""
from typing import Optional, List
import argparse
import os
import random
import numpy as np
from graphs import generate_ba
from propagation import GossipPropagationEngine
from propagation.metrics import spreading_time
import matplotlib.pyplot as plt
from scipy.stats import expon


def collect_taus(G, trials: int = 500, seed: Optional[int] = 42):
    random.seed(seed)
    nodes = list(G.nodes())
    taus = []
    for _ in range(trials):
        v = random.choice(nodes)
        if G.degree(v) == 0:
            continue
        origin = random.choice(list(G.neighbors(v)))
        engine = GossipPropagationEngine(G)
        res = engine.run(v, origin)
        tau = spreading_time(res['history'])
        taus.append(tau)
    return np.array(taus)


def run_distribution(n: int = 2000, trials: int = 500):
    G = generate_ba(n, m=3, seed=123)
    taus = collect_taus(G, trials=trials)
    # fit exponential
    loc, scale = expon.fit(taus, floc=0)
    lambda_hat = 1.0 / scale if scale != 0 else np.inf

    out_dir = 'outputs/figures'
    os.makedirs(out_dir, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6,4))
    counts, bins, _ = ax.hist(taus, bins=range(0, max(taus)+2), density=True, alpha=0.6, label='empirical')
    xs = np.linspace(0, bins[-1], 200)
    ax.plot(xs, expon.pdf(xs, loc=loc, scale=scale), 'r-', label=f'exp fit lambda={lambda_hat:.3f}')
    ax.set_xlabel('Spreading time tau')
    ax.set_ylabel('Probability')
    ax.legend()
    fig.tight_layout()
    out_file = f'{out_dir}/tau_distribution.png'
    fig.savefig(out_file, dpi=300)
    print('Saved', out_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=2000)
    parser.add_argument('--trials', type=int, default=500)
    args = parser.parse_args()
    run_distribution(args.n, args.trials)
