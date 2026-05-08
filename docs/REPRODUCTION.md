# Reproduction Report — Gossip Propagation Experiments

This document describes the problem, mathematical formulation, experimental protocol, implementation details, and instructions to reproduce figures and interactive dashboards for the gossip propagation experiments from:

- G. M. Viswanathan et al., "The spread of gossip in American schools" (EPL, 2007)
- A. P. S. de Moura et al., "Spreading gossip in social networks" (Phys. Rev. E, 2007)

## Problem statement

We study the constrained propagation of a rumor/gossip about a single victim node v. The key constraint is that gossip only spreads among neighbors of the victim; i.e., transmission occurs on the induced subgraph G[N(v)]. We measure:

- Spread factor: $f = n_f / k$, where $n_f$ is the number of victim's neighbors reached, and $k$ is degree of victim.
- Spreading time: $\tau$, the minimum number of discrete timesteps required for the propagation to reach its final set of reachable neighbors.

Propagation can be deterministic (BFS-like) or probabilistic (each attempted transmission succeeds with probability $q$). We implement both one-shot attempts and repeated attempts per timestep as in the literature.

## Mathematical formulation

Let $G=(V,E)$ and fix victim $v$. Define $S_0=\{u\}$ the originator in $N(v)$. For each timestep $t\ge1$:
$$S_t = \{ w\in N(v) : \exists u\in S_{t-1} \text{ with } (u,w)\in E \text{ and infection succeeds} \} \setminus \bigcup_{i< t} S_i.$$ 

In the deterministic mode infection succeeds for all eligible edges. In the probabilistic mode, each eligible edge succeeds with probability $q$. Two variants:

- One-shot: an edge is only attempted once across the whole process.
- Repeated: infected nodes attempt again each timestep.

The spread factor is computed as $f = |\bigcup_t S_t| / k$. The spreading time $\tau$ equals the index of the last non-empty $S_t$.

## Implementation overview

- Language: Python 3.11+
- Core libraries: `networkx`, `numpy`, `pandas`, `scipy`, `matplotlib`.
- Visualization: `plotly`, `pyvis`, `vis-network` (frontend), `tailwindcss` for styling.
- Project layout: see repository top-level structure.

Major modules:
- `graphs/`: generators and loaders (BA, WS, ER; Apollonian implemented from scratch).
- `propagation/`: `GossipPropagationEngine`, `ProbabilisticGossip`, k-hop helpers, metrics.
- `experiments/`: high-level drivers to reproduce figures.
- `web/`: interactive dashboard (HTML + JS) and `scripts/build_dashboard.py` exports `web/assets/data.json` used by the dashboard.

## How to reproduce the dashboard (quick)

1. Install dependencies (prefer virtualenv or poetry):

```bash
python -m pip install -r requirements.txt
```

2. Build the dashboard data and copy static files:

```bash
python scripts/build_dashboard.py
```

3. Open `outputs/dashboard/index.html` in a web browser. Alternatively open `web/index.html` for the development copy.

## Reproducing paper figures

The `experiments/` folder contains scripts to run batches of simulations. Typical workflow:

1. Use graph generators to create networks of various sizes and parameters.
2. For each victim node degree k, run multiple realizations of the gossip process; compute $f(k)$ and $\tau(k)$.
3. Fit functions using `scipy.optimize.curve_fit` for logarithmic and exponential laws.

Example command (quick):

```bash
python experiments/reproduce_epl.py --n 2000 --seed 42
python experiments/reproduce_pre.py --n 2000 --q 0.5
```

## Notes on Apollonian generator

Apollonian networks are implemented by recursive subdivision of triangular faces. The generator starts from a single triangle and repeatedly picks a face, inserting a new vertex connected to the three vertices of the face and replacing the face with three new faces.

## Next steps and extensions

- Add full experiment pipelines that sweep degrees and q values and save results in `data/processed/`.
- Add SciPy-based fitting and produce publication-quality figures (SVG/PDF) in `outputs/figures/`.
- Implement server-backed live simulation endpoint for very large graphs to avoid shipping full histories to the frontend.

## References

- "The spread of gossip in American schools" (EPL, 2007)
- "Spreading gossip in social networks" (Physical Review E, 2007)
