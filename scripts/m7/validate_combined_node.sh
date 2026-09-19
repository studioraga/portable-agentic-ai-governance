#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"; M2="${1:?m2 env}"; M3="${2:?m3 env}"; M4="${3:?m4 env}"; M5="${4:?m5 env}"; M6="${5:?m6 env}"; M7="${6:?m7 env}"
set -a; source "$M2"; source "$M3"; source "$M4"; source "$M5"; source "$M6"; source "$M7"; set +a
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
python3 - <<'PY2'
import json
from portable_ai_governance.kernel.security_profile import evaluate_security_profile
r=evaluate_security_profile(); print(json.dumps({'profile':r.profile,'ok':r.ok,'checks':[{'name':x.name,'ok':x.ok,'detail':x.detail} for x in r.checks]},indent=2)); raise SystemExit(0 if r.ok else 2)
PY2
python3 "$ROOT/scripts/m7/validate_m7_node.py" "$M7" >/dev/null
echo 'PASS: combined M2+M3+M4+M5+M6+M7 production node validation complete'
