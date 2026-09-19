#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
M4="${1:?usage: package_verifier_chain.sh <m4-material> <m5-material> <m6-material> <m7-material> <out-dir>}"
M5="${2:?m5 material}"; M6="${3:?m6 material}"; M7="${4:?m7 material}"; OUT="${5:?output directory}"
mkdir -p "$OUT"; chmod 700 "$OUT"
python3 "$ROOT/scripts/m7/verify_release_chain.py" --m4-material "$M4" --m5-material "$M5" --m6-material "$M6" --m7-material "$M7"
"$ROOT/deploy/m4/package_verifier_material.sh" "$M4" "$OUT/m4-verifier-material.tar.gz"
"$ROOT/deploy/m5/package_verifier_material.sh" "$M5" "$OUT/m5-verifier-material.tar.gz"
"$ROOT/deploy/m6/package_verifier_material.sh" "$M6" "$OUT/m6-verifier-material.tar.gz"
"$ROOT/deploy/m7/package_verifier_material.sh" "$M7" "$OUT/m7-verifier-material.tar.gz"
for f in "$OUT"/*.tar.gz; do
  if tar -tzf "$f" | grep -q 'signing-private.pem'; then echo "FAIL: private key in $f"; exit 2; fi
done
python3 - "$M4" "$M5" "$M6" "$M7" "$OUT/release-chain.json" <<'PY'
import hashlib,json,sys
from pathlib import Path
m4,m5,m6,m7,out=map(Path,sys.argv[1:])
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
payload={'schema':'pag-m7-verifier-chain-v1','sha256':{
'm4':h(m4/'ai-security-manifest.json'),'m5':h(m5/'compliance-risk-manifest.json'),
'm6':h(m6/'evidence-analyst-manifest.json'),'m7':h(m7/'tool-agent-manifest.json')}}
out.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n'); out.chmod(0o600)
PY
(cd "$OUT" && sha256sum *.tar.gz release-chain.json > verifier-chain.sha256)
chmod 600 "$OUT/verifier-chain.sha256"
echo "PASS: coherent M4-M7 verifier chain packaged at $OUT"
