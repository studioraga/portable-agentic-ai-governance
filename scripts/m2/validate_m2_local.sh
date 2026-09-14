#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
WORK="${1:-$ROOT/var/m2-validation}"
rm -rf "$WORK"
install -d -m 700 "$WORK"
export PAG_NODE1_DNS=localhost PAG_NODE1_IP=127.0.0.1 PAG_NODE2_DNS=node2 PAG_NODE2_IP=127.0.0.2
"$ROOT/deploy/m2/bootstrap_m2_material.sh" "$WORK/material"
"$ROOT/deploy/m2/deploy_node1.sh" "$WORK/material" "$WORK/node1-config"
"$ROOT/deploy/m2/deploy_node2.sh" "$WORK/material" "$WORK/node2-config"
"$ROOT/scripts/m2/validate_m2_node.sh" "$WORK/node1-config/production.env"
"$ROOT/scripts/m2/validate_m2_node.sh" "$WORK/node2-config/production.env"
PYTHONPATH="$ROOT/src" python "$ROOT/scripts/m2/validate_m2_transport.py" --node1-env "$WORK/node1-config/production.env" --node2-env "$WORK/node2-config/production.env"
# Production must fail closed if mandatory dependencies disappear or weaken.
negative_env() {
  name="$1"; sed_expr="$2"
  cp "$WORK/node1-config/production.env" "$WORK/node1-config/broken.env"
  sed -i "$sed_expr" "$WORK/node1-config/broken.env"
  set +e
  "$ROOT/scripts/m2/validate_m2_node.sh" "$WORK/node1-config/broken.env" >/dev/null 2>&1
  rc=$?
  set -e
  [ "$rc" -ne 0 ] || { echo "FAIL: production accepted $name"; exit 2; }
  echo "PASS $name-fails-closed"
}
negative_env missing-identity 's#^PAG_IDENTITY_FILE=.*#PAG_IDENTITY_FILE=/nonexistent/identity.json#'
negative_env missing-policy 's#^PAG_POLICY_CATALOG=.*#PAG_POLICY_CATALOG=/nonexistent/policy.json#'
negative_env mtls-disabled 's#^PAG_MTLS_REQUIRED=1#PAG_MTLS_REQUIRED=0#'
negative_env missing-ca 's#^PAG_TLS_CA_FILE=.*#PAG_TLS_CA_FILE=/nonexistent/ca.crt#'

chmod 644 "$WORK/node1-config/secrets/request_signing.key"
set +e; "$ROOT/scripts/m2/validate_m2_node.sh" "$WORK/node1-config/production.env" >/dev/null 2>&1; rc=$?; set -e
[ "$rc" -ne 0 ] || { echo 'FAIL: production accepted permissive secret permissions'; exit 2; }
echo 'PASS permissive-secret-permissions-fail-closed'
chmod 600 "$WORK/node1-config/secrets/request_signing.key"

chmod 644 "$WORK/node1-config/pki/node1.key"
set +e; "$ROOT/scripts/m2/validate_m2_node.sh" "$WORK/node1-config/production.env" >/dev/null 2>&1; rc=$?; set -e
[ "$rc" -ne 0 ] || { echo 'FAIL: production accepted permissive TLS key permissions'; exit 2; }
echo 'PASS permissive-tls-key-permissions-fail-closed'
chmod 600 "$WORK/node1-config/pki/node1.key"
echo 'PASS: Milestone 2 local/distributed security validation complete'
