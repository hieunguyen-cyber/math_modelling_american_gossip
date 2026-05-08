#!/usr/bin/env bash
set -euo pipefail

echo "Building dashboard assets..."
python scripts/build_dashboard.py
echo "Dashboard is available at outputs/dashboard/index.html"
