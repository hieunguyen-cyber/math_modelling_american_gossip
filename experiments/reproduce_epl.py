import sys
import os
import json
import argparse
import random
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from graphs import generate_ba, generate_apollonian
from propagation import GossipPropagationEngine
from experiments.runner import parallel_sweep_graph, aggregate_by_degree

def reproduce_epl(n=1000, max_pairs=10000, seed=42):
    random.seed(seed)
    np.random.seed(seed)
    
    os.makedirs('outputs', exist_ok=True)
    results_summary = {}

    print("Running BA networks...")
    for m in [3, 5, 7]:
        print(f"  Generating BA(n={n}, m={m})")
        G_ba = generate_ba(n, m=m, seed=seed)
        
        print(f"  Sweeping BA m={m}")
        # constrain_to_neighbors=True is default for GossipPropagationEngine
        raw_res = parallel_sweep_graph(
            G=G_ba,
            engine_class=GossipPropagationEngine,
            max_pairs=max_pairs,
            n_jobs=-1
        )
        
        agg = aggregate_by_degree(raw_res)
        results_summary[f'ba_m{m}'] = {
            'k': list(agg.keys()),
            'f': [agg[k]['f'] for k in agg.keys()],
            'tau': [agg[k]['tau'] for k in agg.keys()],
            'raw_tau': [r['timesteps'] for r in raw_res], # for P(tau)
            'raw_f': [r['reached_friends_count']/max(1, r['victim_degree']) for r in raw_res]
        }

    print("Running Apollonian network...")
    # generation 6 is 3284 nodes
    gen = 6 if n > 3000 else 5
    G_apl = generate_apollonian(generations=gen, seed=seed)
    print(f"  Generated APL(generations={gen}), N={G_apl.number_of_nodes()}")
    
    raw_res_apl = parallel_sweep_graph(
        G=G_apl,
        engine_class=GossipPropagationEngine,
        max_pairs=max_pairs,
        n_jobs=-1
    )
    agg_apl = aggregate_by_degree(raw_res_apl)
    results_summary[f'apl_gen{gen}'] = {
        'k': list(agg_apl.keys()),
        'f': [agg_apl[k]['f'] for k in agg_apl.keys()],
        'tau': [agg_apl[k]['tau'] for k in agg_apl.keys()],
        'raw_tau': [r['timesteps'] for r in raw_res_apl],
        'raw_f': [r['reached_friends_count']/max(1, r['victim_degree']) for r in raw_res_apl]
    }

    out_file = 'outputs/epl_results.json'
    with open(out_file, 'w') as f:
        json.dump(results_summary, f)
    print(f"Saved results to {out_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=1000)
    parser.add_argument('--max-pairs', type=int, default=50000)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    
    reproduce_epl(args.n, args.max_pairs, args.seed)
