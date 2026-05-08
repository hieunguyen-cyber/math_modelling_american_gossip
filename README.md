Gossip Propagation Reproduction — Research-Grade Toolkit
======================================================

This repository reproduces and modernizes the experiments from:

- G. M. Viswanathan et al., "The spread of gossip in American schools" (EPL, 2007)
- A. P. S. de Moura et al., "Spreading gossip in social networks" (Phys. Rev. E, 2007)

Goal
----

Provide a reproducible, extensible, and publication-quality toolkit to:

- Generate synthetic and empirical networks (BA, WS, ER, Apollonian, edge lists).
- Run constrained gossip propagation processes (deterministic and probabilistic).
- Compute and fit key metrics: spread factor $f$, spreading time $\tau$, distributions.
- Produce publication-quality static figures, animations (GIF/MP4), and an interactive HTML dashboard with live simulation via a lightweight Flask API.

Quickstart
----------

1. Create a Python 3.11+ virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

2. Run the full pipeline (experiments, figures, dashboard):

```bash
bash scripts/run_all.sh
```

3. To run only experiments or build assets, use the other shell wrappers in `scripts/`.

Development server (Interactive Dashboard)
----------------------------------------
To run the live API used by the dashboard (for interactive generation, graph customization, and gossip animation):

```bash
python scripts/server.py
```

Then open your browser and navigate to **http://127.0.0.1:5000/**

**Dashboard Features:**
- Generate base graphs using custom topological parameters ($N$, $m$, $p$, $k$).
- Visually customize the graph layout (add/delete nodes and edges manually) right on the canvas.
- Run multi-mode propagation (Local, Probabilistic, k-Hop) to trace timeline dynamics.
- Animate the exact spread path from origin to final reach.

Generating Scientific Figures
-----------------------------
To run the simulations and generate publication-quality figures:

```bash
python experiments/scaling_laws.py
python scripts/generate_figures.py
```

The script will automatically compute and output to `outputs/figures/`:
1. **Degree Distributions** ($P(k)$ vs $k$) for BA, ER, WS, and Apollonian networks on log-log scales.
2. **Probability Sweeps** ($f$ and $\tau$ vs $q$) for Probabilistic Gossip mechanics.
3. **Scaling Laws** ($\tau$ vs $k$) fitted with logarithmic models.

Project layout
--------------

See the top-level folder structure for modular components: `graphs/`, `propagation/`, `experiments/`, `visualization/`, `web/`, `scripts/`.

Reproduction and figures
------------------------
Detailed reproduction steps, mathematical definitions, and mappings to figures from the two papers are in `docs/REPRODUCTION.md`.

Contributing
------------
Pull requests welcome. For extensions (e.g., server-side streaming for very large graphs), prefer adding background workers and pagination rather than sending entire histories over HTTP.

