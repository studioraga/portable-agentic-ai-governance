#!/usr/bin/env bash
set -euo pipefail
M2="${1:?m2 env}"; M3="${2:?m3 env}"; M4="${3:?m4 env}"; ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
set -a; source "$M2"; source "$M3"; source "$M4"; set +a
export PAG_SECURITY_PROFILE=production PAG_FAIL_CLOSED=1 PAG_MTLS_REQUIRED=1 PAG_SUPPLY_CHAIN_REQUIRED=1 PAG_AI_SECURITY_REQUIRED=1
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 -m portable_ai_governance.cli validate-security
python3 "$ROOT/scripts/m4/validate_m4_node.py" "$M4"
echo 'PASS: combined M2+M3+M4 production node validation complete'
