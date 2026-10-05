#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
rm -rf var/m26-material;python3 scripts/m26/build_m26_material.py --out var/m26-material
./scripts/m26/verify_node1.sh var/m26-material
./deploy/m26/package_verifier_material.sh var/m26-material var/m26-verifier.tar.gz
