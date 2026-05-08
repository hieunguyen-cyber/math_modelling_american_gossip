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

Development server
------------------
To run the live API used by the dashboard (for interactive generation and replay):

```bash
python scripts/server.py
```

Then open `web/index.html` (dev copy) or `outputs/dashboard/index.html` (built copy) in a browser.

Project layout
--------------

See the top-level folder structure for modular components: `graphs/`, `propagation/`, `experiments/`, `visualization/`, `web/`, `scripts/`.

Reproduction and figures
------------------------
Detailed reproduction steps, mathematical definitions, and mappings to figures from the two papers are in `docs/REPRODUCTION.md`.

Contributing
------------
Pull requests welcome. For extensions (e.g., server-side streaming for very large graphs), prefer adding background workers and pagination rather than sending entire histories over HTTP.

