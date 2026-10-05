#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);cd "$ROOT";python3 -m pip install -e . pytest >/dev/null;./scripts/m26/validate_m26_regression.sh
