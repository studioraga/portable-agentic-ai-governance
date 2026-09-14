#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ENV_FILE="${1:?usage: validate_m2_node.sh production.env}"
set -a
source "$ENV_FILE"
set +a
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
echo "=== M2 node validation: ${PAG_NODE_ID:-unknown} ==="
python -m portable_ai_governance.cli validate-security
python - <<'PY'
from portable_ai_governance.security.runtime import build_runtime_dependencies
from portable_ai_governance.kernel.identity import FileIdentityProvider

d=build_runtime_dependencies()
print('PASS identity-health', d.identity.health())
print('PASS secret-health', d.secrets.health())
for n in ('evidence_signing','request_signing','approval_signing','audit_signing'):
    d.secrets.get(n); print('PASS secret',n)
PY
find "$(dirname "$PAG_IDENTITY_FILE")" -type f -name '*.key' -perm /077 -print | grep -q . && { echo 'FAIL: open private key/secret permissions'; exit 2; } || true
echo 'PASS: M2 node configuration validation complete'
