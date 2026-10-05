#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd);cd "$ROOT";rm -rf var/m28-material;PYTHONPATH="$ROOT/src" python3 scripts/m28/build_m28_material.py --out var/m28-material;./scripts/m28/verify_node1.sh var/m28-material;./deploy/m28/package_verifier_material.sh var/m28-material var/m28-verifier.tar.gz;echo 'PASS: M28 Node1 material and verifier package generated'
