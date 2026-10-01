#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)";NODE2_PROFILE="${1:?path to live Node2 profile JSON}";OUT="${2:-$ROOT/var/m19-material}";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
mkdir -p "$ROOT/var/m19-validation";NODE1_PROFILE="$ROOT/var/m19-validation/node1-runtime-profile.json"
python3 "$ROOT/scripts/m19/collect_node_profile.py" --role node1 --out "$NODE1_PROFILE"
python3 "$ROOT/scripts/m19/build_m19_material.py" --out "$OUT" --node1-profile "$NODE1_PROFILE" --node2-profile "$NODE2_PROFILE"
python3 "$ROOT/scripts/m19/validate_m19_node.py" --material "$OUT" --repo-root "$ROOT"
python3 - "$OUT/production-validation-summary.json" <<'LIVECHECK'
import json,sys
s=json.load(open(sys.argv[1]))
if s['validation_mode']!='LIVE' or not s['production_validation_complete']: raise SystemExit('FAIL: M19 Node1 one-shot requires LIVE complete validation')
print('PASS: LIVE Node1/Node2 production-validation gate complete')
LIVECHECK
"$ROOT/deploy/m19/deploy_node.sh" node1 "$OUT" "$HOME/.config/portable-ai-governance/m19";install -m600 "$OUT/signing-private.pem" "$HOME/.config/portable-ai-governance/m19/signing-private.pem"
echo "PASS: Node1 M19 production-validation authority complete at $OUT"
