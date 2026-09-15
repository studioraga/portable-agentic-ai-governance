#!/usr/bin/env bash
set -euo pipefail
ENV_FILE="${1:?usage: preflight_m4.sh <m4.env>}"
[ -f "$ENV_FILE" ] || { echo "FAIL env missing: $ENV_FILE"; exit 2; }
set -a; source "$ENV_FILE"; set +a
[ "${PAG_AI_SECURITY_REQUIRED:-0}" = 1 ] || { echo 'FAIL ai-security-required'; exit 2; }
for n in PAG_M4_MANIFEST PAG_M4_MANIFEST_SIG PAG_M4_PUBLIC_KEY PAG_M4_MODEL_GOVERNANCE PAG_M4_DATA_PROVENANCE PAG_M4_RETRIEVAL_POLICY PAG_M4_EMBEDDING_POLICY PAG_M4_EVAL_SUITE PAG_M4_EVAL_RESULTS PAG_M4_THREAT_MODEL PAG_M3_LOCK_FILE; do
  p="${!n:-}"; [ -f "$p" ] || { echo "FAIL $n $p"; exit 2; }; echo "PASS $n $p"
done
echo 'M4 PREFLIGHT: PASS'
