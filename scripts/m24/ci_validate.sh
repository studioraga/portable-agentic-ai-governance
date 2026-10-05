#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);cd "$ROOT";python3 -m pip install -e '.[dev]';./scripts/m24/validate_m24_regression.sh
