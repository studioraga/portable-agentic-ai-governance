#!/usr/bin/env bash
set -euo pipefail
ENVF="${1:?usage preflight_m7.sh m7.env}"
set -a; source "$ENVF"; set +a
for n in PAG_M7_MANIFEST PAG_M7_MANIFEST_SIG PAG_M7_PUBLIC_KEY PAG_M7_AGENT_POLICY PAG_M7_TOOL_REGISTRY PAG_M7_AUTHORIZATION_RULES PAG_M6_MANIFEST; do
  v="${!n:-}"; [ -f "$v" ] || { echo "FAIL $n $v"; exit 2; }; echo "PASS $n $v"
done
echo 'M7 PREFLIGHT: PASS'
