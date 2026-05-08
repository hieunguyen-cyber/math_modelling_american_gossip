"""Sweep propagation probability q and record spread factor and tau."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import Optional, List
import argparse
import os
import csv
import random
import numpy as np
from graphs import generate_er, generate_ba, generate_ws
from propagation import ProbabilisticGossip
from propagation.metrics import spread_factor, spreading_time


def run_sweep(graph_type: str, n: int, qs: List[float], repetitions: int = 20, seed: Optional[int] = 42):
    random.seed(seed)
    np.random.seed(seed)
    out_dir = 'outputs/processed'
    os.makedirs(out_dir, exist_ok=True)
    results = []
    for q in qs:
        f_vals = []
        tau_vals = []
        for rep in range(repetitions):
            if graph_type == 'er':
                G = generate_er(n, p=0.01, seed=seed+rep)
            elif graph_type == 'ba':
                G = generate_ba(n, m=3, seed=seed+rep)
            else:
                G = generate_ws(n, k=6, p=0.1, seed=seed+rep)

            # pick a victim with degree>0
            victims = [v for v,d in G.degree() if d>0]
            if not victims:
                continue
            victim = random.choice(victims)
            origin = random.choice(list(G.neighbors(victim)))
            engine = ProbabilisticGossip(G)
            res = engine.run(victim, origin, q=q, one_shot=False)
            f = spread_factor(res['reached'], G.degree(victim))
            tau = spreading_time(res['history'])
            f_vals.append(f)
            tau_vals.append(tau)

        results.append({'q': q, 'f_mean': float(np.mean(f_vals)) if f_vals else 0.0, 'f_std': float(np.std(f_vals)), 'tau_mean': float(np.mean(tau_vals)) if tau_vals else 0.0, 'tau_std': float(np.std(tau_vals))})

    out_file = os.path.join(out_dir, f'probability_sweep_{graph_type}.csv')
    with open(out_file, 'w', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=['q','f_mean','f_std','tau_mean','tau_std'])
        writer.writeheader()
        for row in results:
            writer.writerow(row)
    print('Saved', out_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph', default='ba')
    parser.add_argument('--n', type=int, default=2000)
    parser.add_argument('--reps', type=int, default=20)
    args = parser.parse_args()
    qs = list(np.linspace(0.0, 1.0, 11))
    run_sweep(args.graph, args.n, qs, repetitions=args.reps)
