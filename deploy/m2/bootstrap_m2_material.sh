#!/usr/bin/env bash
set -euo pipefail
umask 077
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
OUT="${1:-$ROOT/var/m2-bootstrap}"
TRUST_DOMAIN="${PAG_TRUST_DOMAIN:-pag.local}"
NODE1_DNS="${PAG_NODE1_DNS:-localhost}"
NODE1_IP="${PAG_NODE1_IP:-127.0.0.1}"
NODE2_DNS="${PAG_NODE2_DNS:-node2}"
NODE2_IP="${PAG_NODE2_IP:-127.0.0.2}"

command -v openssl >/dev/null || { echo 'ERROR: openssl required' >&2; exit 2; }
rm -rf "$OUT"
install -d -m 700 "$OUT/ca-private" "$OUT/node1/pki" "$OUT/node1/secrets" "$OUT/node2/pki" "$OUT/node2/secrets"

openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out "$OUT/ca-private/ca.key" >/dev/null 2>&1
chmod 600 "$OUT/ca-private/ca.key"
openssl req -x509 -new -sha256 -days 3650 \
  -key "$OUT/ca-private/ca.key" \
  -subj '/CN=PAG M2 Local Root CA' \
  -addext 'basicConstraints=critical,CA:TRUE' \
  -addext 'keyUsage=critical,keyCertSign,cRLSign' \
  -out "$OUT/ca-private/ca.crt"

make_cert() {
  node="$1"; dns="$2"; ip="$3"
  dir="$OUT/$node/pki"
  openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:3072 -out "$dir/$node.key" >/dev/null 2>&1
  chmod 600 "$dir/$node.key"
  cat > "$OUT/$node/$node.ext" <<EOF
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth,clientAuth
subjectAltName=DNS:${dns},IP:${ip},URI:spiffe://${TRUST_DOMAIN}/${node}
EOF
  openssl req -new -sha256 -key "$dir/$node.key" -subj "/CN=${node}" -out "$OUT/$node/$node.csr"
  openssl x509 -req -sha256 -days 825 \
    -in "$OUT/$node/$node.csr" \
    -CA "$OUT/ca-private/ca.crt" -CAkey "$OUT/ca-private/ca.key" -CAcreateserial \
    -extfile "$OUT/$node/$node.ext" \
    -out "$dir/$node.crt" >/dev/null 2>&1
  cp "$OUT/ca-private/ca.crt" "$dir/ca.crt"
  chmod 644 "$dir/ca.crt" "$dir/$node.crt"
  rm -f "$OUT/$node/$node.csr" "$OUT/$node/$node.ext"
}
make_cert node1 "$NODE1_DNS" "$NODE1_IP"
make_cert node2 "$NODE2_DNS" "$NODE2_IP"

REQUEST_KEY="$(openssl rand -hex 32)"
for node in node1 node2; do
  printf '%s\n' "$REQUEST_KEY" > "$OUT/$node/secrets/request_signing.key"
  openssl rand -hex 32 > "$OUT/$node/secrets/evidence_signing.key"
  openssl rand -hex 32 > "$OUT/$node/secrets/approval_signing.key"
  openssl rand -hex 32 > "$OUT/$node/secrets/audit_signing.key"
  chmod 600 "$OUT/$node/secrets/"*.key
  TOKEN="$(openssl rand -hex 32)"
  DIGEST="$(printf '%s' "$TOKEN" | sha256sum | awk '{print $1}')"
  printf '%s\n' "$TOKEN" > "$OUT/$node/bootstrap-admin.token"
  chmod 600 "$OUT/$node/bootstrap-admin.token"
  cat > "$OUT/$node/identities.json" <<EOF
{"identities":[{"name":"bootstrap-admin","token_sha256":"${DIGEST}","roles":["ai_governance_admin","security_admin"],"attributes":{"environment":"production","node":"${node}"}}]}
EOF
  chmod 600 "$OUT/$node/identities.json"
done

cat > "$OUT/node1/workloads.json" <<EOF
{"workloads":[{"uri":"spiffe://${TRUST_DOMAIN}/node2","principal_id":"node2","roles":["node_client"],"attributes":{"environment":"production","node":"node2"}}]}
EOF
chmod 600 "$OUT/node1/workloads.json"
cat > "$OUT/node2/workloads.json" <<EOF
{"workloads":[{"uri":"spiffe://${TRUST_DOMAIN}/node1","principal_id":"node1","roles":["node_server"],"attributes":{"environment":"production","node":"node1"}}]}
EOF
chmod 600 "$OUT/node2/workloads.json"

cat > "$OUT/README.txt" <<EOF
M2 bootstrap material generated for trust domain ${TRUST_DOMAIN}.
Node1 certificate SAN: DNS ${NODE1_DNS}, IP ${NODE1_IP}, URI spiffe://${TRUST_DOMAIN}/node1
Node2 certificate SAN: DNS ${NODE2_DNS}, IP ${NODE2_IP}, URI spiffe://${TRUST_DOMAIN}/node2
Transfer node2/ only over an authenticated encrypted channel. Never transfer ca-private/.
EOF
chmod 600 "$OUT/README.txt"
echo "PASS: M2 PKI/secret bootstrap created under $OUT"
echo "IMPORTANT: ca-private/ is CA custody material; do not deploy it to either node."
