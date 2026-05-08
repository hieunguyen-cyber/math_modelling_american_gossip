#!/usr/bin/env bash
set -euo pipefail

echo "Probability experiments (BA)..."
python experiments/probability_experiments.py --graph ba --n 2000 --reps 50

echo "Scaling laws..."
python experiments/scaling_laws.py --n 2000 --samples 800

echo "Distributions..."
python experiments/distributions.py --n 2000 --trials 800

echo "Experiments finished."
