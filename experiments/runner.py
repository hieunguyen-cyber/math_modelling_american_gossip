from typing import Type, Dict, Any, List
import networkx as nx
from joblib import Parallel, delayed
import numpy as np

from propagation import GossipPropagationEngine, ProbabilisticGossip

def run_single_pair(engine: GossipPropagationEngine, victim: int, originator: int, kwargs: dict) -> Dict[str, Any]:
    res = engine.run(victim, originator, **kwargs)
    
    # Calculate metrics here to avoid passing huge history arrays back if not needed
    visited_count = len(res.get('visited', set()))
    reached_friends_count = len(res.get('reached', set()))
    timesteps = res.get('timesteps', 0)
    
    return {
        'victim': victim,
        'originator': originator,
        'visited_count': visited_count,
        'reached_friends_count': reached_friends_count,
        'timesteps': timesteps,
        'victim_degree': engine.G.degree(victim)
    }

def parallel_sweep_graph(
    G: nx.Graph,
    engine_class: Type[GossipPropagationEngine],
    engine_kwargs: dict = None,
    run_kwargs: dict = None,
    n_jobs: int = -1,
    max_pairs: int = None
) -> List[Dict[str, Any]]:
    """
    Run propagation for multiple victim-originator pairs in a graph using joblib.
    If max_pairs is specified, samples pairs uniformly to bound execution time.
    """
    engine_kwargs = engine_kwargs or {}
    run_kwargs = run_kwargs or {}
    
    # Engine is instantiated once per pair currently because we can't share it across processes easily,
    # actually we can pass G and instantiate inside the worker.
    # To optimize, we pass the graph and instantiate engine inside the delayed function.
    
    def worker(v, o, g, ek, rk):
        eng = engine_class(g, **ek)
        return run_single_pair(eng, v, o, rk)
        
    pairs = []
    for victim in G.nodes():
        for originator in G.neighbors(victim):
            pairs.append((victim, originator))
            
    if not pairs:
        return []
        
    if max_pairs is not None and len(pairs) > max_pairs:
        idx = np.random.choice(len(pairs), size=max_pairs, replace=False)
        pairs = [pairs[i] for i in idx]
        
    results = Parallel(n_jobs=n_jobs)(
        delayed(worker)(v, o, G, engine_kwargs, run_kwargs) for v, o in pairs
    )
    
    return results

def aggregate_by_degree(results: List[Dict[str, Any]]) -> Dict[int, Dict[str, float]]:
    """Aggregate simulation results by victim degree to compute f(k) and tau(k)."""
    agg = {}
    for r in results:
        k = r['victim_degree']
        if k not in agg:
            agg[k] = {'f_sum': 0.0, 'tau_sum': 0.0, 'count': 0}
        
        # spread factor = reached friends / degree
        f = r['reached_friends_count'] / k if k > 0 else 0
        agg[k]['f_sum'] += f
        agg[k]['tau_sum'] += r['timesteps']
        agg[k]['count'] += 1
        
    return {
        k: {
            'f': val['f_sum'] / val['count'],
            'tau': val['tau_sum'] / val['count'],
            'count': val['count']
        }
        for k, val in agg.items()
    }
