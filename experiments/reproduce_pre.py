import sys
import os
import json
import argparse
import random
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graphs import generate_ba
from propagation import ProbabilisticGossip
from experiments.runner import parallel_sweep_graph, aggregate_by_degree

def reproduce_pre(n=1000, max_pairs=10000, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    
    os.makedirs('outputs', exist_ok=True)
    results_summary = {}

    print(f"Running PRE Probabilistic Sweep on BA(n={n}, m=7)...")
    G_ba = generate_ba(n, m=7, seed=seed)
    
    # 1. Local constraints (1-hop)
    q_vals = [0.1, 0.3, 0.5, 0.8, 1.0]
    
    local_results = {}
    for q in q_vals:
        print(f"  Sweeping q={q} (local constraint)")
        raw_res = parallel_sweep_graph(
            G=G_ba,
            engine_class=ProbabilisticGossip,
            run_kwargs={'q': q, 'one_shot': False, 'constrain_to_neighbors': True},
            max_pairs=max_pairs,
            n_jobs=-1
        )
        agg = aggregate_by_degree(raw_res)
        local_results[f'q_{q}'] = {
            'k': list(agg.keys()),
            'f': [agg[k]['f'] for k in agg.keys()],
            'tau': [agg[k]['tau'] for k in agg.keys()],
            'f_mean': np.mean([r['reached_friends_count']/max(1, r['victim_degree']) for r in raw_res]),
            'tau_mean': np.mean([r['timesteps'] for r in raw_res])
        }
    results_summary['local'] = local_results
    
    # 2. Entire network (F_N and tau_max)
    entire_results = {}
    print(f"Running PRE Entire Network Sweep on BA(n={n}, m=7)...")
    for q in [0.5, 1.0]:
        print(f"  Sweeping q={q} (entire network)")
        raw_res_ent = parallel_sweep_graph(
            G=G_ba,
            engine_class=ProbabilisticGossip,
            run_kwargs={'q': q, 'one_shot': False, 'constrain_to_neighbors': False},
            max_pairs=max_pairs // 5, # reduce pairs for entire network to save time
            n_jobs=-1
        )
        # For entire network, we care about F_N (visited / N)
        agg_ent = aggregate_by_degree(raw_res_ent)
        
        entire_results[f'q_{q}'] = {
            'k': list(agg_ent.keys()),
            'F_N': [np.mean([r['visited_count']/n for r in raw_res_ent if r['victim_degree'] == k]) for k in agg_ent.keys()],
            'tau_max': [np.mean([r['timesteps'] for r in raw_res_ent if r['victim_degree'] == k]) for k in agg_ent.keys()],
        }
    results_summary['entire'] = entire_results

    out_file = 'outputs/pre_results.json'
    with open(out_file, 'w') as f:
        json.dump(results_summary, f)
    print(f"Saved results to {out_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=1000)
    parser.add_argument('--max-pairs', type=int, default=20000)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    
    reproduce_pre(args.n, args.max_pairs, args.seed)
