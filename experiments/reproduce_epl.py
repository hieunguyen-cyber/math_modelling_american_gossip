"""Experiment driver to reproduce key figures from EPL 2007.

This script is a high-level orchestrator. Detailed reproduction code
should follow the paper; this file runs baseline experiments.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from typing import Optional
import argparse
import random
import networkx as nx
import numpy as np
from graphs import generate_ba, generate_ws, generate_er, generate_apollonian
from propagation import GossipPropagationEngine, ProbabilisticGossip
from propagation.metrics import spread_factor, spreading_time

def run_basic(n=1000, seed: Optional[int]=42):
    random.seed(seed)
    np.random.seed(seed)
    G = generate_ba(n, m=3, seed=seed)
    victim = 0
    origin = list(G.neighbors(victim))[0]
    engine = GossipPropagationEngine(G)
    res = engine.run(victim, origin)
    f = spread_factor(res['reached'], G.degree(victim))
    tau = spreading_time(res['history'])
    print(f"BA f={f:.3f} tau={tau}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=1000)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    run_basic(args.n, args.seed)
