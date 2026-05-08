#!/usr/bin/env bash
# Run full reproduction pipeline: experiments, figures, tests, dashboard
set -euo pipefail

echo "Installing Python requirements..."
python -m pip install -r requirements.txt

echo "Running tests..."
python -m pytest -q || true

echo "Running probability experiments (BA, ER, WS)..."
python experiments/probability_experiments.py --graph ba --n 2000 --reps 50
python experiments/probability_experiments.py --graph er --n 2000 --reps 50
python experiments/probability_experiments.py --graph ws --n 2000 --reps 50

echo "Running scaling laws experiments..."
python experiments/scaling_laws.py --n 2000 --samples 800

echo "Running distribution experiments..."
python experiments/distributions.py --n 2000 --trials 800

echo "Generating figures..."
python scripts/generate_figures.py

echo "Building dashboard..."
echo "Starting server for live demo (temporary)..."
nohup python scripts/server.py > server.log 2>&1 &
echo $! > .server.pid
sleep 1
python scripts/build_dashboard.py
if [ -f .server.pid ]; then
	kill $(cat .server.pid) || true
	rm -f .server.pid
fi

echo "All done. Outputs are in outputs/"
