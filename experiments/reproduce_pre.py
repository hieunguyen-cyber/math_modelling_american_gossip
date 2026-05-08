"""Experiment driver to reproduce key figures from PRE 2007."""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import Optional
import argparse
import random
import numpy as np
from graphs import generate_ws, generate_er
from propagation import ProbabilisticGossip
from propagation.metrics import spread_factor, spreading_time

def run_probability_experiment(n=1000, q=0.5, seed: Optional[int]=42):
    random.seed(seed)
    np.random.seed(seed)
    G = generate_er(n, p=0.01, seed=seed)
    victim = 0
    neighbors = list(G.neighbors(victim))
    if not neighbors:
        print("victim has no neighbors")
        return
    origin = neighbors[0]
    engine = ProbabilisticGossip(G)
    res = engine.run(victim, origin, q=q, one_shot=False)
    f = spread_factor(res['reached'], G.degree(victim))
    tau = spreading_time(res['history'])
    print(f"ER q={q:.2f} f={f:.3f} tau={tau}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=1000)
    parser.add_argument('--q', type=float, default=0.5)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    run_probability_experiment(args.n, args.q, args.seed)
