#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";cd "$ROOT"
python3 -m pip install -e '.[dev]'
./scripts/m22/validate_m22_regression.sh
