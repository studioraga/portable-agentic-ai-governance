#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
"$ROOT/scripts/m9/preflight_dependencies.sh"
python3 -m pytest -q tests/security_ops/test_m9_security_ops.py
echo 'PASS: M9 SIEM/incident/containment/recovery/evidence positive-negative suite'
echo 'PASS: Milestone 9 security operations validation complete'
