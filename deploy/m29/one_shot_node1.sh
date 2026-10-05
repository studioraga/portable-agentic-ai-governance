#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);cd "$ROOT";rm -rf var/m29-material;./scripts/m29/prepare_m29_inputs.sh;PYTHONPATH="$ROOT/src" python3 scripts/m29/build_m29_material.py --out var/m29-material;./scripts/m29/verify_node1.sh var/m29-material;./deploy/m29/package_verifier_material.sh var/m29-material var/m29-verifier.tar.gz;echo 'PASS: M29 Node1 cross-domain package generated'
