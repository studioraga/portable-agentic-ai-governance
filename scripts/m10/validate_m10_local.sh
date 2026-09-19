#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.."&&pwd)";cd "$ROOT";export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
"$ROOT/scripts/m10/preflight_dependencies.sh"
python3 -m pytest -q tests/multi_agent/test_m10_multi_agent.py
echo 'PASS: M10 typed multi-agent topology/handoff/assurance/human-decision positive-negative suite'
echo 'PASS: Milestone 10 multi-agent workflows validation complete'
