#!/usr/bin/env bash
set -euo pipefail

echo "Running pytest..."
python -m pytest -q
