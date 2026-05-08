#!/usr/bin/env bash
set -euo pipefail

echo "Generating figures..."
python scripts/generate_figures.py
python experiments/scaling_laws.py --n 2000 --samples 800
python experiments/distributions.py --n 2000 --trials 800

echo "Figures generated in outputs/figures"
