#!/usr/bin/env bash
set -euo pipefail
ENV="${1:?usage preflight_m6.sh <m6.env>}"; [ -f "$ENV" ] || { echo "FAIL env missing: $ENV"; exit 2; }
set -a; source "$ENV"; set +a
for n in PAG_M6_MANIFEST PAG_M6_MANIFEST_SIG PAG_M6_PUBLIC_KEY PAG_M6_AGENT_POLICY PAG_M6_EVIDENCE_CATALOG PAG_M6_EVIDENCE_ROOT PAG_M5_MANIFEST; do v="${!n:-}"; [ -e "$v" ] || { echo "FAIL $n $v"; exit 2; }; echo "PASS $n $v"; done
echo 'M6 PREFLIGHT: PASS'
