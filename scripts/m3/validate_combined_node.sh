#!/usr/bin/env bash
set -euo pipefail
M2_ENV="${1:?usage validate_combined_node.sh <m2-production.env> <m3.env>}"; M3_ENV="${2:?}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
set -a; source "$M2_ENV"; source "$M3_ENV"; set +a
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m portable_ai_governance.cli validate-security
python3 "$ROOT/scripts/m3/validate_m3_node.py" "$M3_ENV"
echo 'PASS: combined M2+M3 production node validation complete'
