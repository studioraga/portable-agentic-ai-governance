#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
NODE_ID="${1:?usage: deploy_node.sh node1|node2 MATERIAL_DIR [CONFIG_ROOT]}"
MATERIAL="${2:?material directory required}"
CONFIG_ROOT="${3:-$HOME/.config/portable-ai-governance/m2}"
case "$NODE_ID" in node1|node2) ;; *) echo 'ERROR: node must be node1 or node2' >&2; exit 2;; esac
SRC="$MATERIAL/$NODE_ID"
[ -d "$SRC/pki" ] && [ -d "$SRC/secrets" ] || { echo "ERROR: invalid material source $SRC" >&2; exit 2; }
install -d -m 700 "$CONFIG_ROOT" "$CONFIG_ROOT/pki" "$CONFIG_ROOT/secrets" "$CONFIG_ROOT/runtime" "$CONFIG_ROOT/runtime/evidence" "$CONFIG_ROOT/runtime/state"
cp "$SRC/pki/ca.crt" "$CONFIG_ROOT/pki/ca.crt"
cp "$SRC/pki/$NODE_ID.crt" "$CONFIG_ROOT/pki/$NODE_ID.crt"
install -m 600 "$SRC/pki/$NODE_ID.key" "$CONFIG_ROOT/pki/$NODE_ID.key"
chmod 644 "$CONFIG_ROOT/pki/ca.crt" "$CONFIG_ROOT/pki/$NODE_ID.crt"
for f in evidence_signing request_signing approval_signing audit_signing; do
  install -m 600 "$SRC/secrets/$f.key" "$CONFIG_ROOT/secrets/$f.key"
done
install -m 600 "$SRC/identities.json" "$CONFIG_ROOT/identities.json"
install -m 600 "$SRC/workloads.json" "$CONFIG_ROOT/workloads.json"

cat > "$CONFIG_ROOT/production.env" <<EOF
PAG_SECURITY_PROFILE=production
PAG_FAIL_CLOSED=1
PAG_NODE_ID=$NODE_ID
PAG_IDENTITY_PROVIDER=file
PAG_IDENTITY_FILE=$CONFIG_ROOT/identities.json
PAG_SECRET_PROVIDER=file
PAG_SECRETS_DIR=$CONFIG_ROOT/secrets
PAG_POLICY_CATALOG=$ROOT/governance/controls/control-catalog.json
PAG_MTLS_REQUIRED=1
PAG_TLS_CA_FILE=$CONFIG_ROOT/pki/ca.crt
PAG_TLS_CERT_FILE=$CONFIG_ROOT/pki/$NODE_ID.crt
PAG_TLS_KEY_FILE=$CONFIG_ROOT/pki/$NODE_ID.key
PAG_WORKLOAD_REGISTRY=$CONFIG_ROOT/workloads.json
PAG_TRUST_DOMAIN=${PAG_TRUST_DOMAIN:-pag.local}
PAG_SECURITY_AUDIT_LOG=$CONFIG_ROOT/runtime/evidence/security-audit.jsonl
PAG_REPLAY_CACHE=$CONFIG_ROOT/runtime/state/security-probe-nonces.json
PAG_RATE_LIMIT=${PAG_RATE_LIMIT:-60}
PAG_RATE_WINDOW_SEC=${PAG_RATE_WINDOW_SEC:-60}
EOF
chmod 600 "$CONFIG_ROOT/production.env"
find "$CONFIG_ROOT" -type d -exec chmod 700 {} +
find "$CONFIG_ROOT" -type f -name '*.key' -exec chmod 600 {} +

echo "PASS: deployed M2 material for $NODE_ID to $CONFIG_ROOT"
echo "Run: set -a; source '$CONFIG_ROOT/production.env'; set +a"
