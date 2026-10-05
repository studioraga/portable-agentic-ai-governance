#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);cd "$ROOT";python3 -m pip install -e . pytest;./scripts/m29/validate_m29_regression.sh
